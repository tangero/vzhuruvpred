-- D1 Database Schema for Article Ratings
-- Create ratings table

CREATE TABLE IF NOT EXISTS ratings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    article_id TEXT NOT NULL,
    rating_type TEXT NOT NULL CHECK (rating_type IN ('love', 'like', 'neutral', 'dislike', 'bad')),
    user_fingerprint TEXT NOT NULL,
    ip_address TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_ratings_article_id ON ratings(article_id);
CREATE INDEX IF NOT EXISTS idx_ratings_fingerprint ON ratings(user_fingerprint);
CREATE INDEX IF NOT EXISTS idx_ratings_article_user ON ratings(article_id, user_fingerprint);
CREATE INDEX IF NOT EXISTS idx_ratings_created_at ON ratings(created_at);

-- Create trigger to update updated_at timestamp
CREATE TRIGGER IF NOT EXISTS ratings_updated_at 
    AFTER UPDATE ON ratings
    FOR EACH ROW
    BEGIN
        UPDATE ratings SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
    END;

-- Insert some sample data for testing (optional)
-- INSERT INTO ratings (article_id, rating_type, user_fingerprint, ip_address) VALUES
-- ('test-article-1', 'love', 'sample_fingerprint_1', '127.0.0.1'),
-- ('test-article-1', 'like', 'sample_fingerprint_2', '127.0.0.1'),
-- ('test-article-2', 'neutral', 'sample_fingerprint_3', '127.0.0.1');