#!/bin/bash

# NewsAPI klíč z environment variable
API_KEY="${NEWS_API_KEY}"

# Kontrola, jestli je API klíč nastaven
if [ -z "$API_KEY" ]; then
    echo "CHYBA: NEWS_API_KEY není nastaven!"
    echo "Nastavte ho pomocí: export NEWS_API_KEY='váš_klíč'"
    exit 1
fi

# Výstupní soubor
OUTPUT_FILE="../_data/world_news.json"

# Funkce pro získání vlaječky podle země
get_flag() {
    case $1 in
        "us") echo "🇺🇸" ;;
        "gb") echo "🇬🇧" ;;
        "de") echo "🇩🇪" ;;
        "fr") echo "🇫🇷" ;;
        "it") echo "🇮🇹" ;;
        "ua") echo "🇺🇦" ;;
        "cn") echo "🇨🇳" ;;
        "jp") echo "🇯🇵" ;;
        "ca") echo "🇨🇦" ;;
        "au") echo "🇦🇺" ;;
        *) echo "🌍" ;;
    esac
}

# Stáhnout zprávy z NewsAPI
echo "Stahuji světové zprávy..."

# Stáhnout top headlines
RESPONSE=$(curl -s "https://newsapi.org/v2/top-headlines?sources=bbc-news,cnn,reuters,associated-press&pageSize=20&apiKey=${API_KEY}")

# Uložit do JSON souboru
echo "$RESPONSE" | jq '{
    last_updated: (now | strftime("%Y-%m-%dT%H:%M:%S")),
    articles: [.articles[] | {
        flag: (
            if .source.id == "bbc-news" then "🇬🇧"
            elif .source.id == "cnn" then "🇺🇸"
            elif .source.id == "reuters" then "🌍"
            elif .source.id == "associated-press" then "🌍"
            else "🌍"
            end
        ),
        country: (
            if .source.id == "bbc-news" then "gb"
            elif .source.id == "cnn" then "us"
            else "global"
            end
        ),
        title: .title,
        original_title: .title,
        url: .url,
        source: .source.name,
        publishedAt: .publishedAt,
        description: (.description // "")
    }]
}' > "$OUTPUT_FILE"

echo "Zprávy uloženy do $OUTPUT_FILE"