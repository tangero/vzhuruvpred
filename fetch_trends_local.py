#!/usr/bin/env python3
"""
Lokální skript pro stažení Google Trends z RSS feedu
Instalace: pip install requests beautifulsoup4
"""

import json
import requests
from datetime import datetime
import xml.etree.ElementTree as ET

print("Načítám Google Trends RSS feed pro Česko...")

# Načteme RSS feed
rss_url = 'https://trends.google.cz/trending/rss?geo=CZ'

try:
    response = requests.get(rss_url, timeout=30)
    response.raise_for_status()
    
    print(f"RSS odpověď: {response.status_code}")
    
    # Parsujeme XML
    root = ET.fromstring(response.content)
    
    trends_data = []
    
    # Najdeme všechny item elementy
    items = root.findall('.//item')
    print(f"Nalezeno {len(items)} trendových položek")
    
    for idx, item in enumerate(items[:8]):  # Prvních 8 trendů
        # Základní informace
        title = item.find('title')
        title_text = title.text if title is not None else ''
        
        # Traffic information
        traffic = item.find('.//{http://www.google.com/trends/hottrends}approx_traffic')
        traffic_text = traffic.text if traffic is not None else 'Trending'
        
        # Obrázek - hlavní obrázek trendu
        picture = item.find('.//{http://www.google.com/trends/hottrends}picture')
        picture_url = picture.text if picture is not None else ''
        
        # Opravíme relativní URL
        if picture_url and picture_url.startswith('//'):
            picture_url = 'https:' + picture_url
        
        # Zdroj obrázku
        picture_source = item.find('.//{http://www.google.com/trends/hottrends}picture_source')
        source_text = picture_source.text if picture_source is not None else 'Google Trends'
        
        # První související článek
        news_items = item.findall('.//{http://www.google.com/trends/hottrends}news_item')
        
        if news_items:
            first_news = news_items[0]
            news_title = first_news.find('.//{http://www.google.com/trends/hottrends}news_item_title')
            news_url = first_news.find('.//{http://www.google.com/trends/hottrends}news_item_url')
            news_source = first_news.find('.//{http://www.google.com/trends/hottrends}news_item_source')
            
            # Zkusíme najít obrázek článku jako fallback
            news_picture = first_news.find('.//{http://www.google.com/trends/hottrends}news_item_picture')
            if not picture_url and news_picture is not None:
                picture_url = news_picture.text
                if picture_url and picture_url.startswith('//'):
                    picture_url = 'https:' + picture_url
            
            news_title_text = news_title.text if news_title is not None else title_text
            news_url_text = news_url.text if news_url is not None else f"https://www.google.com/search?q={title_text}&tbm=nws"
            news_source_text = news_source.text if news_source is not None else source_text
        else:
            news_title_text = title_text
            news_url_text = f"https://www.google.com/search?q={title_text}&tbm=nws"
            news_source_text = source_text
        
        # Vytvoříme trend item
        trend_item = {
            'rank': idx + 1,
            'query': title_text,
            'news_title': news_title_text,
            'news_url': news_url_text,
            'picture': picture_url,
            'traffic': f"{traffic_text}+ hledání" if traffic_text != 'Trending' else 'Trending',
            'source': news_source_text,
            'explore_url': f"https://trends.google.cz/trends/explore?q={title_text}&geo=CZ"
        }
        
        trends_data.append(trend_item)
        
        print(f"\nTrend #{idx+1}: {title_text}")
        print(f"  - Článek: {news_title_text[:60]}...")
        print(f"  - Obrázek: {'✓ ' + picture_url[:50] + '...' if picture_url else '✗ Bez obrázku'}")
        print(f"  - Traffic: {traffic_text}")
        print(f"  - Zdroj: {news_source_text}")
        
except Exception as e:
    print(f"Chyba při načítání RSS: {e}")
    import traceback
    traceback.print_exc()
    trends_data = []

# Uložení do JSON
if trends_data:
    output = {
        'updated': datetime.now().isoformat(),
        'trends': trends_data
    }
    
    with open('_data/trends.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Úspěšně načteno {len(trends_data)} trendů z RSS feedu")
    print("📄 Data uložena do _data/trends.json")
else:
    print("\n❌ Nepodařilo se načíst žádné trendy")