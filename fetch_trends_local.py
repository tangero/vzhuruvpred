#!/usr/bin/env python3
"""
Lokální skript pro stažení Google Trends z RSS feedu
Instalace: pip install requests beautifulsoup4
"""

import json
from urllib.request import urlopen
from urllib.error import URLError
from datetime import datetime
import xml.etree.ElementTree as ET

print("Načítám Google Trends RSS feed pro Česko...")

# Načteme RSS feed
rss_url = 'https://trends.google.cz/trending/rss?geo=CZ'

try:
    with urlopen(rss_url, timeout=30) as response:
        content = response.read()
    
    print(f"RSS odpověď: {response.status}")
    
    # Parsujeme XML
    root = ET.fromstring(content)
    
    trends_data = []
    
    # Najdeme všechny item elementy
    items = root.findall('.//item')
    print(f"Nalezeno {len(items)} trendových položek")
    
    # Nejdříve sesbíráme všechny trendy s traffic daty
    all_trends = []
    
    for item in items:
        # Základní informace
        title = item.find('title')
        title_text = title.text if title is not None else ''
        
        # Traffic information - zkusíme různé formáty namespace
        traffic = item.find('.//ht:approx_traffic', {'ht': 'http://www.google.com/trends/hottrends'})
        if traffic is None:
            # Zkusíme bez namespace
            for elem in item.iter():
                if elem.tag.endswith('approx_traffic'):
                    traffic = elem
                    break
        
        traffic_text = traffic.text if traffic is not None else '0'
        
        # Převedeme traffic na číslo pro řazení
        try:
            traffic_num = int(traffic_text.replace('+', '').replace(',', ''))
        except (ValueError, AttributeError):
            traffic_num = 0
        
        all_trends.append((item, traffic_num, traffic_text, title_text))
    
    # Seřadíme podle počtu hledání (sestupně)
    all_trends.sort(key=lambda x: x[1], reverse=True)
    
    # Vezmeme prvních 8 nejhledanějších
    for idx, (item, traffic_num, traffic_text, title_text) in enumerate(all_trends[:8]):
        
        # Obrázek - hlavní obrázek trendu
        picture = None
        for elem in item.iter():
            if elem.tag.endswith('picture') and not elem.tag.endswith('news_item_picture'):
                picture = elem
                break
        picture_url = picture.text if picture is not None else ''
        
        # Opravíme relativní URL
        if picture_url and picture_url.startswith('//'):
            picture_url = 'https:' + picture_url
        
        # Zdroj obrázku
        picture_source = None
        for elem in item.iter():
            if elem.tag.endswith('picture_source'):
                picture_source = elem
                break
        source_text = picture_source.text if picture_source is not None else 'Google Trends'
        
        # První související článek
        news_items = []
        for elem in item.iter():
            if elem.tag.endswith('news_item'):
                news_items.append(elem)
        
        if news_items:
            first_news = news_items[0]
            
            # Najdeme news elementy bez namespace
            news_title = None
            news_url = None  
            news_source = None
            news_picture = None
            
            for elem in first_news.iter():
                if elem.tag.endswith('news_item_title'):
                    news_title = elem
                elif elem.tag.endswith('news_item_url'):
                    news_url = elem
                elif elem.tag.endswith('news_item_source'):
                    news_source = elem
                elif elem.tag.endswith('news_item_picture'):
                    news_picture = elem
            
            # Zkusíme najít obrázek článku jako fallback
            if not picture_url and news_picture is not None:
                picture_url = news_picture.text or ''
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