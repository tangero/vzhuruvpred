#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import requests
import os
from datetime import datetime

# NewsAPI konfigurace
NEWS_API_KEY = os.environ.get('NEWS_API_KEY', 'YOUR_API_KEY_HERE')
NEWS_API_URL = 'https://newsapi.org/v2/top-headlines'

# Mapování zemí na emoji vlaječky
COUNTRY_FLAGS = {
    'us': '🇺🇸',
    'gb': '🇬🇧',
    'de': '🇩🇪',
    'fr': '🇫🇷',
    'it': '🇮🇹',
    'es': '🇪🇸',
    'cn': '🇨🇳',
    'jp': '🇯🇵',
    'ru': '🇷🇺',
    'ua': '🇺🇦',
    'pl': '🇵🇱',
    'sk': '🇸🇰',
    'at': '🇦🇹',
    'ch': '🇨🇭',
    'nl': '🇳🇱',
    'be': '🇧🇪',
    'se': '🇸🇪',
    'no': '🇳🇴',
    'dk': '🇩🇰',
    'fi': '🇫🇮',
    'ca': '🇨🇦',
    'au': '🇦🇺',
    'nz': '🇳🇿',
    'in': '🇮🇳',
    'br': '🇧🇷',
    'mx': '🇲🇽',
    'ar': '🇦🇷',
    'za': '🇿🇦',
    'eg': '🇪🇬',
    'il': '🇮🇱',
    'sa': '🇸🇦',
    'ae': '🇦🇪',
    'kr': '🇰🇷',
    'sg': '🇸🇬',
    'hk': '🇭🇰',
    'tw': '🇹🇼',
    'th': '🇹🇭',
    'id': '🇮🇩',
    'my': '🇲🇾',
    'ph': '🇵🇭',
    'vn': '🇻🇳',
    'tr': '🇹🇷',
    'gr': '🇬🇷',
    'pt': '🇵🇹',
    'ie': '🇮🇪',
    'hu': '🇭🇺',
    'ro': '🇷🇴',
    'bg': '🇧🇬',
    'rs': '🇷🇸',
    'hr': '🇭🇷',
    'si': '🇸🇮',
    'lt': '🇱🇹',
    'lv': '🇱🇻',
    'ee': '🇪🇪',
    'ma': '🇲🇦',
    'ng': '🇳🇬',
    'ke': '🇰🇪',
    'global': '🌍'
}

def get_country_from_source(source_id, source_name):
    """Pokusí se určit zemi ze zdroje zprávy"""
    source_lower = (source_id or source_name or '').lower()
    
    # Mapování známých zdrojů na země
    source_country_map = {
        'bbc': 'gb',
        'cnn': 'us',
        'fox': 'us',
        'nbc': 'us',
        'abc': 'us',
        'cbs': 'us',
        'washington-post': 'us',
        'new-york-times': 'us',
        'wsj': 'us',
        'wall-street': 'us',
        'usa-today': 'us',
        'reuters': 'global',
        'associated-press': 'global',
        'ap': 'global',
        'bloomberg': 'us',
        'financial-times': 'gb',
        'guardian': 'gb',
        'independent': 'gb',
        'daily-mail': 'gb',
        'telegraph': 'gb',
        'times': 'gb',
        'spiegel': 'de',
        'bild': 'de',
        'welt': 'de',
        'le-monde': 'fr',
        'le-figaro': 'fr',
        'liberation': 'fr',
        'corriere': 'it',
        'repubblica': 'it',
        'el-pais': 'es',
        'el-mundo': 'es',
        'rt': 'ru',
        'tass': 'ru',
        'pravda': 'ua',
        'globo': 'br',
        'folha': 'br',
        'times-of-india': 'in',
        'hindustan': 'in',
        'china-daily': 'cn',
        'xinhua': 'cn',
        'nhk': 'jp',
        'asahi': 'jp',
        'yomiuri': 'jp',
        'korea-herald': 'kr',
        'strait-times': 'sg',
        'sydney-morning': 'au',
        'herald-sun': 'au',
        'globe-and-mail': 'ca',
        'toronto-star': 'ca',
        'al-jazeera': 'global',
        'dw': 'de',
        'france24': 'fr',
        'euronews': 'global'
    }
    
    for key, country in source_country_map.items():
        if key in source_lower:
            return country
    
    # Pokud nenajdeme, vrátíme globální
    return 'global'

def translate_to_czech(text):
    """Přeloží text do češtiny pomocí MyMemory API (zdarma, bez klíče)"""
    try:
        # MyMemory API - zdarma bez registrace
        url = "https://api.mymemory.translated.net/get"
        params = {
            'q': text[:500],  # Limit 500 znaků pro free tier
            'langpair': 'en|cs'
        }
        
        response = requests.get(url, params=params, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('responseStatus') == 200:
                return data['responseData']['translatedText']
        
        return text  # Vrátíme původní text při chybě
        
    except Exception as e:
        print(f"Chyba při překladu: {e}")
        return text  # Vrátíme původní text při chybě

def fetch_world_news():
    """Stáhne nejdůležitější světové zprávy z různých zemí"""
    all_articles = []
    
    # Seznam zemí, ze kterých chceme zprávy
    countries = ['us', 'gb', 'de', 'fr', 'ua', 'cn', 'jp']
    
    for country in countries:
        try:
            params = {
                'country': country,
                'apiKey': NEWS_API_KEY,
                'pageSize': 3  # 3 zprávy z každé země
            }
            
            response = requests.get(NEWS_API_URL, params=params)
            
            if response.status_code == 200:
                data = response.json()
                
                if data['status'] == 'ok':
                    for article in data['articles'][:3]:
                        # Určíme zemi ze zdroje nebo použijeme aktuální zemi
                        article_country = get_country_from_source(
                            article.get('source', {}).get('id'),
                            article.get('source', {}).get('name')
                        )
                        if article_country == 'global':
                            article_country = country
                        
                        flag = COUNTRY_FLAGS.get(article_country, '🌍')
                        
                        # Přeložíme nadpis
                        original_title = article['title']
                        czech_title = translate_to_czech(original_title)
                        
                        news_item = {
                            'flag': flag,
                            'country': article_country,
                            'title': czech_title,
                            'original_title': original_title,
                            'url': article['url'],
                            'source': article.get('source', {}).get('name', 'Neznámý zdroj'),
                            'publishedAt': article['publishedAt'],
                            'description': translate_to_czech(article.get('description', ''))[:200] if article.get('description') else ''
                        }
                        
                        all_articles.append(news_item)
            else:
                print(f"Chyba při stahování zpráv pro {country}: {response.status_code}")
                
        except Exception as e:
            print(f"Chyba při zpracování zpráv pro {country}: {e}")
    
    # Seřadíme podle času publikace
    all_articles.sort(key=lambda x: x['publishedAt'], reverse=True)
    
    # Vezmeme jen 20 nejnovějších
    all_articles = all_articles[:20]
    
    return all_articles

def save_news_to_json(articles):
    """Uloží zprávy do JSON souboru"""
    output_path = os.path.join(os.path.dirname(__file__), '..', '_data', 'world_news.json')
    
    data = {
        'last_updated': datetime.now().isoformat(),
        'articles': articles
    }
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"Uloženo {len(articles)} zpráv do {output_path}")

def main():
    """Hlavní funkce"""
    print("Stahuji světové zprávy...")
    articles = fetch_world_news()
    
    if articles:
        save_news_to_json(articles)
        print("Zprávy úspěšně staženy a přeloženy!")
    else:
        print("Nepodařilo se stáhnout žádné zprávy.")

if __name__ == "__main__":
    main()