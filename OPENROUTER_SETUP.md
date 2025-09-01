# Nastavení OpenRouter.ai pro překlad trendů

Tento projekt používa OpenRouter.ai s modelem `mistralai/mistral-medium-2506` pro překlad anglických nadpisů do češtiny a sumarizaci na max 112 znaků.

## 1. Získání API klíče

1. Registrujte se na https://openrouter.ai
2. Jděte na https://openrouter.ai/keys  
3. Vytvořte nový API klíč
4. Zkopírujte klíč (začíná `sk-or-v1-...`)

## 2. Nastavení GitHub Secrets

1. Jděte do GitHub repozitáře: https://github.com/tangero/vzhuruvpred
2. Settings → Secrets and variables → Actions
3. Klikněte na "New repository secret"
4. Name: `OPENROUTER_API_KEY`
5. Secret: váš OpenRouter API klíč
6. Klikněte "Add secret"

## 3. Lokální testování

Pro lokální testování nastavte environment variable:

```bash
export OPENROUTER_API_KEY="sk-or-v1-your-key-here"
python3 fetch_trends_local.py
```

## 4. Jak to funguje

- **Detekce jazyka**: Automaticky detekuje anglické texty
- **Překlad**: Anglické nadpisy přeloží do češtiny  
- **Sumarizace**: Všechny nadpisy zkrátí na max 112 znaků
- **Fallback**: Pokud API nefunguje, použije se pouze zkrácení

## 5. Příklad výstup

```
🤖 Překládám a sumarizuji: Luis Suarez appears to spit at Seattle Sounders co...
✅ Výsledek: Suárez zřejmě plivl na trenéra Seattle po prohře Miami

🤖 Sumarizuji: Svobodná země stojí na vzdělanosti, vysvětluje spolumajitel...  
✅ Výsledek: Spolumajitel Tipsportu: Svobodná země stojí na vzdělanosti
```

## 6. Náklady

- Model `mistralai/mistral-medium-2506` stojí cca $0.002 per 1K tokens
- Každý nadpis = ~50-100 tokens  
- 8 trendů každé 3 hodiny = ~$0.05 měsíčně