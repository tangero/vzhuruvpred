#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import urllib.parse
import urllib.request
import time

def translate_text(text, source_lang='en', target_lang='cs'):
    """Přeloží text pomocí Google Translate API (neoficiální)"""
    try:
        # URL encode text
        text = urllib.parse.quote(text)
        
        # Google Translate URL
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl={source_lang}&tl={target_lang}&dt=t&q={text}"
        
        # Stáhnout překlad
        with urllib.request.urlopen(url) as response:
            data = response.read().decode('utf-8')
            
        # Parse JSON
        result = json.loads(data)
        
        # Získat přeložený text
        translated = result[0][0][0] if result and result[0] and result[0][0] else None
        
        return translated if translated else text
        
    except Exception as e:
        print(f"Chyba při překladu: {e}")
        return text

def main():
    # Načíst zprávy
    with open('/Users/patrickzandl/GitHub/vzhuruvpred/_data/world_news.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"Překládám {len(data['articles'])} zpráv...")
    
    # Přeložit každou zprávu
    for i, article in enumerate(data['articles']):
        # Přeložit titulek
        if article.get('title'):
            original = article['title']
            translated = translate_text(original)
            article['original_title'] = original
            article['title'] = translated
            print(f"{i+1}. {translated[:60]}...")
            
        # Přeložit popis (pokud existuje)
        if article.get('description'):
            article['description'] = translate_text(article['description'])[:200]
            
        # Krátká pauza mezi požadavky
        time.sleep(0.1)
    
    # Uložit přeložené zprávy
    with open('/Users/patrickzandl/GitHub/vzhuruvpred/_data/world_news.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("Překlad dokončen!")

if __name__ == "__main__":
    main()