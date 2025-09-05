// Cloudflare Workers API for Article Ratings
// Path: /functions/api/ratings.js

const CORS_HEADERS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-Requested-With',
  'Access-Control-Max-Age': '86400',
};

// Rate limiting: max 10 votes per IP per hour
const RATE_LIMIT = 10;
const RATE_LIMIT_WINDOW = 3600000; // 1 hour in milliseconds

export async function onRequest(context) {
  const { request, env } = context;
  const url = new URL(request.url);
  const method = request.method;

  // Handle CORS preflight
  if (method === 'OPTIONS') {
    return new Response(null, { 
      status: 204, 
      headers: CORS_HEADERS 
    });
  }

  try {
    // Parse article ID from query params
    const articleId = url.searchParams.get('article');
    if (!articleId) {
      return jsonResponse({ error: 'Article ID required' }, 400);
    }

    switch (method) {
      case 'GET':
        return await getRatings(env, articleId);
      case 'POST':
        return await addRating(env, request, articleId);
      default:
        return jsonResponse({ error: 'Method not allowed' }, 405);
    }
  } catch (error) {
    console.error('API Error:', error);
    return jsonResponse({ error: 'Internal server error' }, 500);
  }
}

// Get ratings for an article
async function getRatings(env, articleId) {
  try {
    const result = await env.DB.prepare(`
      SELECT rating_type, COUNT(*) as count
      FROM ratings 
      WHERE article_id = ? 
      GROUP BY rating_type
    `).bind(articleId).all();

    const ratings = {
      love: 0,
      like: 0,
      neutral: 0,
      dislike: 0,
      bad: 0
    };

    result.results.forEach(row => {
      if (ratings.hasOwnProperty(row.rating_type)) {
        ratings[row.rating_type] = row.count;
      }
    });

    // Get total count
    const totalResult = await env.DB.prepare(`
      SELECT COUNT(*) as total FROM ratings WHERE article_id = ?
    `).bind(articleId).first();

    return jsonResponse({
      success: true,
      ratings,
      total: totalResult.total
    });
  } catch (error) {
    console.error('Get ratings error:', error);
    return jsonResponse({ error: 'Failed to fetch ratings' }, 500);
  }
}

// Add or update rating
async function addRating(env, request, articleId) {
  try {
    const body = await request.json();
    const { rating, fingerprint } = body;

    // Validate rating type
    const validRatings = ['love', 'like', 'neutral', 'dislike', 'bad'];
    if (!validRatings.includes(rating)) {
      return jsonResponse({ error: 'Invalid rating type' }, 400);
    }

    // Get client IP for rate limiting
    const clientIP = request.headers.get('CF-Connecting-IP') || 
                    request.headers.get('X-Forwarded-For') || 
                    'unknown';

    // Check rate limit
    const rateLimitKey = `rate_limit_${clientIP}`;
    const rateLimitData = await env.RATINGS_KV.get(rateLimitKey);
    
    if (rateLimitData) {
      const { count, timestamp } = JSON.parse(rateLimitData);
      const now = Date.now();
      
      if (now - timestamp < RATE_LIMIT_WINDOW && count >= RATE_LIMIT) {
        return jsonResponse({ 
          error: 'Rate limit exceeded. Please try again later.' 
        }, 429);
      }
    }

    // Create user fingerprint (IP + User-Agent hash for basic deduplication)
    const userAgent = request.headers.get('User-Agent') || '';
    const userFingerprint = fingerprint || await generateFingerprint(clientIP, userAgent);

    // Check if user already voted for this article
    const existingVote = await env.DB.prepare(`
      SELECT id, rating_type FROM ratings 
      WHERE article_id = ? AND user_fingerprint = ?
    `).bind(articleId, userFingerprint).first();

    let success = false;
    let message = '';
    let action = '';

    if (existingVote) {
      if (existingVote.rating_type === rating) {
        // Same rating - remove it
        await env.DB.prepare(`
          DELETE FROM ratings 
          WHERE article_id = ? AND user_fingerprint = ?
        `).bind(articleId, userFingerprint).run();
        
        success = true;
        message = 'Rating removed';
        action = 'removed';
      } else {
        // Different rating - update it
        await env.DB.prepare(`
          UPDATE ratings 
          SET rating_type = ?, updated_at = datetime('now')
          WHERE article_id = ? AND user_fingerprint = ?
        `).bind(rating, articleId, userFingerprint).run();
        
        success = true;
        message = 'Rating updated';
        action = 'updated';
      }
    } else {
      // New rating
      await env.DB.prepare(`
        INSERT INTO ratings (article_id, rating_type, user_fingerprint, ip_address, created_at)
        VALUES (?, ?, ?, ?, datetime('now'))
      `).bind(articleId, rating, userFingerprint, clientIP).run();
      
      success = true;
      message = 'Rating added';
      action = 'added';
    }

    // Update rate limit
    await updateRateLimit(env, clientIP);

    // Get updated ratings
    const updatedRatings = await getRatings(env, articleId);
    const ratingsData = await updatedRatings.json();

    return jsonResponse({
      success,
      message,
      action,
      ratings: ratingsData.ratings,
      total: ratingsData.total
    });

  } catch (error) {
    console.error('Add rating error:', error);
    return jsonResponse({ error: 'Failed to save rating' }, 500);
  }
}

// Generate user fingerprint
async function generateFingerprint(ip, userAgent) {
  const text = `${ip}_${userAgent}`;
  const encoder = new TextEncoder();
  const data = encoder.encode(text);
  const hashBuffer = await crypto.subtle.digest('SHA-256', data);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  return hashArray.map(b => b.toString(16).padStart(2, '0')).join('').substr(0, 16);
}

// Update rate limit counter
async function updateRateLimit(env, clientIP) {
  const rateLimitKey = `rate_limit_${clientIP}`;
  const now = Date.now();
  
  try {
    const existingData = await env.RATINGS_KV.get(rateLimitKey);
    let count = 1;
    
    if (existingData) {
      const { count: existingCount, timestamp } = JSON.parse(existingData);
      if (now - timestamp < RATE_LIMIT_WINDOW) {
        count = existingCount + 1;
      }
    }
    
    await env.RATINGS_KV.put(rateLimitKey, JSON.stringify({
      count,
      timestamp: now
    }), {
      expirationTtl: RATE_LIMIT_WINDOW / 1000 // TTL in seconds
    });
  } catch (error) {
    console.error('Rate limit update error:', error);
  }
}

// Helper function for JSON responses
function jsonResponse(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: {
      'Content-Type': 'application/json',
      ...CORS_HEADERS
    }
  });
}