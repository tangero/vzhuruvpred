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

# Stáhnout top headlines z category general
RESPONSE=$(curl -s "https://newsapi.org/v2/top-headlines?category=general&language=en&pageSize=20&apiKey=${API_KEY}")

# Uložit do JSON souboru
echo "$RESPONSE" | jq '{
    last_updated: (now | strftime("%Y-%m-%dT%H:%M:%S")),
    articles: [.articles[] | {
        flag: (
            if (.source.name | test("BBC"; "i")) then "🇬🇧"
            elif (.source.name | test("CNN"; "i")) then "🇺🇸"
            elif (.source.name | test("Reuters"; "i")) then "🌍"
            elif (.source.name | test("Associated Press|AP"; "i")) then "🌍"
            elif (.source.name | test("Fox"; "i")) then "🇺🇸"
            elif (.source.name | test("Guardian"; "i")) then "🇬🇧"
            elif (.source.name | test("Times"; "i")) then "🇺🇸"
            elif (.source.name | test("Post"; "i")) then "🇺🇸"
            elif (.source.name | test("France|Le"; "i")) then "🇫🇷"
            elif (.source.name | test("Deutsche|Spiegel"; "i")) then "🇩🇪"
            else "🌍"
            end
        ),
        country: (
            if (.source.name | test("BBC|Guardian"; "i")) then "gb"
            elif (.source.name | test("CNN|Fox|Times|Post"; "i")) then "us"
            elif (.source.name | test("France|Le"; "i")) then "fr"
            elif (.source.name | test("Deutsche|Spiegel"; "i")) then "de"
            else "global"
            end
        ),
        title: .title,
        original_title: .title,
        url: .url,
        urlToImage: .urlToImage,
        source: .source.name,
        publishedAt: .publishedAt,
        description: (.description // "")
    }]
}' > "$OUTPUT_FILE"

echo "Zprávy uloženy do $OUTPUT_FILE"