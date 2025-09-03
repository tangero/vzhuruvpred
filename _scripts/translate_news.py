#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import urllib.request
import os
import time
import random
from urllib.error import HTTPError

def clean_title(text):
    """Vyčistí nadpis od uvozovek a zdrojů"""
    if not text:
        return text
    
    # Odstranit uvozovky z začátku a konce
    text = text.strip('"').strip("'")
    
    # Odstranit zdroj za pomlčkou na konci (např. "- CNN", "- BBC News")
    # Hledáme pomlčku následovanou 1-3 slovy na konci
    import re
    text = re.sub(r'\s*[-–—]\s*[A-Z][A-Za-z\s&\.]{1,25}$', '', text)
    
    return text.strip()

def is_sports_news(title, description):
    """Zkontroluje, jestli je zpráva sportovní a netýká se českých týmů/hráčů"""
    # Klíčová slova pro sport
    sports_keywords = [
        'NFL', 'NBA', 'MLB', 'NHL', 'Premier League', 'Champions League',
        'Super Bowl', 'touchdown', 'quarterback', 'basketball', 'baseball',
        'hockey', 'tennis', 'golf', 'soccer', 'football', 'match', 'game',
        'victory', 'defeat', 'score', 'championship', 'tournament',
        'US Open', 'Grand Prix', 'Formula', 'ATP', 'WTA', 'FIFA',
        'playoff', 'finals', 'medal', 'Olympics', 'World Cup',
        'pitcher', 'striker', 'goalkeeper', 'coach', 'manager',
        'transfer', 'signing', 'injury', 'suspension'
    ]
    
    # Česká klíčová slova (tyto zprávy CHCEME zachovat)
    czech_keywords = [
        'Czech', 'Česk', 'Praha', 'Prague', 'Plzeň', 'Slavia', 'Sparta',
        'Liberec', 'Ostrava', 'Brno', 'Olomouc', 'Pardubice',
        'Lehečka', 'Kvitová', 'Plíšková', 'Macháč', 'Siniaková',
        'Veselý', 'Berdych', 'Šafářová', 'Strýcová', 'Krejčíková',
        'Vondroušová', 'Muchová', 'Nosková', 'Menšík'
    ]
    
    text_to_check = (title + ' ' + (description or '')).lower()
    
    # Pokud obsahuje české reference, ponechat
    for keyword in czech_keywords:
        if keyword.lower() in text_to_check:
            return False
    
    # Jinak zkontrolovat, jestli je to sport
    for keyword in sports_keywords:
        if keyword.lower() in text_to_check:
            return True
    
    return False

def translate_text_with_openrouter(text, max_retries=3):
    """Přeloží text pomocí OpenRouter.ai s rate limiting"""
    if not text or len(text.strip()) == 0:
        return text
    
    # Rate limiting - čekat mezi požadavky
    time.sleep(random.uniform(1.0, 2.0))
    
    api_key = os.environ.get('OPENROUTER_API_KEY')
    if not api_key:
        print(f"    ⚠️  OPENROUTER_API_KEY nenalezen, ponechávám: {text[:50]}...")
        return text
    
    for attempt in range(max_retries):
        try:
            print(f"  🤖 Překládám: {text[:50]}...")
            
            prompt = f"""Přelož tento anglický nadpis zprávy do češtiny. Odpověz pouze přeloženým nadpisem, nic jiného. Bez komentářů, bez variant, bez vysvětlení.

"{text}"

Překlad:"""
            
            # OpenRouter.ai API volání
            data = {
                "model": "deepseek/deepseek-chat-v3.1:free",
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 100,
                "temperature": 0.2
            }
            
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://github.com/tangero/vzhuruvpred",
                "X-Title": "VzhuruVpred News Translation"
            }
            
            req = urllib.request.Request(
                "https://openrouter.ai/api/v1/chat/completions",
                data=json.dumps(data).encode('utf-8'),
                headers=headers
            )
            
            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode('utf-8'))
                
            translated_title = result['choices'][0]['message']['content'].strip()
            
            # Očistíme odpověď od případných komentářů
            # Pokud obsahuje číslované seznam nebo "Nejvýstižnější", vezmeme jen první řádek
            lines = translated_title.split('\n')
            if len(lines) > 1:
                # Najdeme první řádek, který obsahuje skutečný překlad
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith('**') and not line.startswith('1.') and not line.startswith('2.') and not 'Nejvýstižnější' in line and not 'variant' in line.lower():
                        translated_title = line
                        break
                else:
                    translated_title = lines[0].strip()
            
            # Odstraníme případné uvozovky a jiné formátování
            translated_title = translated_title.strip('"\'*:')
            
            # Zajistíme rozumnou délku
            if len(translated_title) > 200:
                translated_title = translated_title[:197] + '...'
                
            print(f"    ✅ Výsledek: {translated_title}")
            return translated_title
            
        except HTTPError as e:
            if e.code == 429:  # Too Many Requests
                wait_time = (2 ** attempt) + random.uniform(1, 3)  # Exponential backoff
                print(f"    ⏳ Rate limit dosažen, čekám {wait_time:.1f}s... (pokus {attempt + 1}/{max_retries})")
                time.sleep(wait_time)
                continue
            else:
                print(f"    ❌ HTTP chyba {e.code}: {e}")
                return text
        except Exception as e:
            print(f"    ❌ Chyba při překladu: {e}")
            if attempt < max_retries - 1:
                wait_time = random.uniform(2, 4)
                print(f"    ⏳ Čekám {wait_time:.1f}s před dalším pokusem...")
                time.sleep(wait_time)
                continue
            else:
                # Poslední pokus selhal, vrátíme původní text
                break
    
    # Pokud všechny pokusy selhaly
    print(f"    ❌ OpenRouter API selhalo po {max_retries} pokusech: {text[:50]}...")
    return text

def main():
    # Načíst zprávy
    with open('_data/world_news.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"Načteno {len(data['articles'])} zpráv...")
    
    # Filtrovat sportovní zprávy (kromě českých)
    filtered_articles = []
    for article in data['articles']:
        title = clean_title(article.get('title', ''))
        article['title'] = title  # Uložit vyčištěný nadpis
        article['original_title'] = article.get('original_title', title)
        
        if not is_sports_news(title, article.get('description', '')):
            filtered_articles.append(article)
        else:
            print(f"  ⚽ Odstraňuji sportovní zprávu: {title[:60]}...")
    
    # Omezit na 40 zpráv
    filtered_articles = filtered_articles[:40]
    data['articles'] = filtered_articles
    
    print(f"Po filtrování: {len(filtered_articles)} zpráv")
    print(f"Překládám zprávy pomocí OpenRouter.ai...")
    
    # Přeložit každou zprávu
    for i, article in enumerate(data['articles']):
        # Přeložit titulek
        if article.get('title'):
            # Nadpis už je vyčištěný z clean_title(), jen ho přeložit
            translated = translate_text_with_openrouter(article['title'])
            article['title'] = translated
            print(f"{i+1}. {translated[:60]}...")
            
        # Přeložit popis (pokud existuje)
        if article.get('description'):
            original_desc = article['description']
            translated_desc = translate_text_with_openrouter(original_desc)
            article['description'] = translated_desc[:200] if translated_desc else ''
            
        # Krátká pauza mezi požadavky
        time.sleep(0.5)  # Delší pauza pro API
    
    # Uložit přeložené zprávy
    with open('_data/world_news.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("Překlad dokončen!")

if __name__ == "__main__":
    main()