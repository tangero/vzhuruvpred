#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import urllib.request
import os
import time

def translate_text_with_openrouter(text):
    """Přeloží text pomocí OpenRouter.ai + Mistral"""
    if not text or len(text.strip()) == 0:
        return text
    
    try:
        api_key = os.environ.get('OPENROUTER_API_KEY')
        
        if api_key:
            print(f"  🤖 Překládám: {text[:50]}...")
            
            prompt = f"""Přelož tento anglický nadpis zprávy do přirozeně znějící češtiny. Nepoužívej anglicismy.

"{text}"

Český překlad:"""
            
            # OpenRouter.ai API volání
            data = {
                "model": "openai/gpt-4o",
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 100,
                "temperature": 0.7
            }
            
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://github.com/tangero/vzhuruvpred",
                "X-Title": "VzhúruVpřed News Translation"
            }
            
            req = urllib.request.Request(
                "https://openrouter.ai/api/v1/chat/completions",
                data=json.dumps(data).encode('utf-8'),
                headers=headers
            )
            
            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode('utf-8'))
                
            translated_title = result['choices'][0]['message']['content'].strip()
            
            # Zajistíme rozumnou délku
            if len(translated_title) > 200:
                translated_title = translated_title[:197] + '...'
                
            print(f"    ✅ Výsledek: {translated_title}")
            return translated_title
            
        else:
            raise ValueError("OPENROUTER_API_KEY není nastavený! Nelze překládat.")
        
    except Exception as e:
        print(f"  ❌ OpenRouter API selhalo: {e}")
        import traceback
        traceback.print_exc()
        raise

def main():
    # Načíst zprávy
    with open('_data/world_news.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"Překládám {len(data['articles'])} zpráv pomocí OpenRouter.ai...")
    
    # Přeložit každou zprávu
    for i, article in enumerate(data['articles']):
        # Přeložit titulek
        if article.get('title'):
            original = article['title']
            translated = translate_text_with_openrouter(original)
            article['original_title'] = original
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