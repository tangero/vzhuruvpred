#!/usr/bin/env python3
"""
Lokální skript pro stažení Google Trends s obrázky
Instalace: pip install pytrends pandas
"""

import json
from pytrends.request import TrendReq
from datetime import datetime
import time

# Inicializace pytrends pro Česko
print("Připojuji se k Google Trends...")
pytrends = TrendReq(hl='cs-CZ', tz=60, geo='CZ', timeout=(10,25))

trends_data = []

try:
    # Pokusíme se získat realtime trending searches
    print("Stahuji realtime trendy pro Českou republiku...")
    trending = pytrends.realtime_trending_searches(pn='CZ')
    
    if not trending.empty:
        print(f"Nalezeno {len(trending)} trendů")
        
        # Zpracování prvních 8 trendů
        for idx, row in trending.head(8).iterrows():
            # Google Trends vrací tyto sloupce pro realtime data:
            # entityNames, title, picture, picture_source, articles, shareUrl
            
            # Získáme první článek pokud existuje
            articles = row.get('articles', [])
            first_article = articles[0] if articles else {}
            
            trend_item = {
                'rank': idx + 1,
                'query': row.get('title', ''),
                'news_title': first_article.get('title', row.get('title', '')),
                'news_url': first_article.get('url', f"https://www.google.com/search?q={row.get('title', '')}&tbm=nws"),
                'picture': row.get('picture', ''),  # Toto by měl být skutečný obrázek z Google
                'traffic': row.get('formattedTraffic', 'Trending'),
                'source': first_article.get('source', row.get('picture_source', 'Google Trends')),
                'explore_url': f"https://trends.google.cz/trends/explore?q={row.get('title', '')}&geo=CZ"
            }
            
            # Debug výpis
            print(f"Trend #{idx+1}: {trend_item['query']}")
            print(f"  - Obrázek: {trend_item['picture'][:50]}..." if trend_item['picture'] else "  - Obrázek: Není k dispozici")
            print(f"  - Článek: {trend_item['news_title'][:50]}...")
            
            trends_data.append(trend_item)
            
except Exception as e:
    print(f"Realtime trends selhaly: {e}")
    print("Zkouším daily trending searches...")
    
    try:
        # Fallback na daily trending searches
        trending = pytrends.trending_searches(pn='czech_republic')
        
        print(f"Nalezeno {len(trending)} daily trendů")
        
        for idx, trend in enumerate(trending[0][:8]):
            # Daily trends nemají obrázky, ale můžeme zkusit získat související zprávy
            print(f"Hledám zprávy pro: {trend}")
            
            # Získáme související témata
            pytrends.build_payload([trend], cat=0, timeframe='now 1-d', geo='CZ')
            
            trend_item = {
                'rank': idx + 1,
                'query': trend,
                'news_title': f"Trending: {trend}",
                'news_url': f"https://www.google.com/search?q={trend}&tbm=nws",
                'picture': f"https://source.unsplash.com/400x225/?{trend}",  # Unsplash jako fallback
                'traffic': 'Trending',
                'source': 'Google Trends',
                'explore_url': f"https://trends.google.cz/trends/explore?q={trend}&geo=CZ"
            }
            trends_data.append(trend_item)
            
            # Pauza mezi požadavky
            time.sleep(0.5)
            
    except Exception as e2:
        print(f"Daily trends také selhaly: {e2}")

# Uložení do JSON
if trends_data:
    output = {
        'updated': datetime.now().isoformat(),
        'trends': trends_data
    }
    
    with open('_data/trends.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Úspěšně uloženo {len(trends_data)} trendů do _data/trends.json")
else:
    print("\n❌ Nepodařilo se získat žádné trendy")