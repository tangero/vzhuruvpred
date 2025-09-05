# Cloudflare Pages + Workers Setup pro Hodnocení článků

Tento návod popisuje, jak nasadit rating systém na Cloudflare Pages s D1 databází a Workers.

## 1. Předpoklady

- Cloudflare účet
- Git repository připojené k Cloudflare Pages
- Wrangler CLI nainstalované: `npm install -g wrangler`

## 2. Vytvoření D1 databáze

```bash
# Přihlášení do Cloudflare
wrangler login

# Vytvoření D1 databáze
wrangler d1 create vzhuruvpred-ratings

# Poznačte si database_id z výstupu a aktualizujte wrangler.toml
```

## 3. Vytvoření KV úložiště

```bash
# Vytvoření KV namespace pro rate limiting
wrangler kv:namespace create "RATINGS_KV"

# Poznačte si id a aktualizujte wrangler.toml
```

## 4. Aktualizace wrangler.toml

Nahraďte placeholder hodnoty:

```toml
[[d1_databases]]
binding = "DB"
database_name = "vzhuruvpred-ratings"
database_id = "YOUR_ACTUAL_DATABASE_ID"

[[kv_namespaces]]
binding = "RATINGS_KV"
id = "YOUR_ACTUAL_KV_ID"
```

## 5. Spuštění migrace databáze

```bash
# Spuštění SQL migrace
wrangler d1 execute vzhuruvpred-ratings --file ./migrations/001_create_ratings.sql
```

## 6. Test lokálně (optional)

```bash
# Spuštění Workers v dev módu
wrangler dev

# Test API endpoint
curl "http://localhost:8787/api/ratings?article=test-article"
```

## 7. Nasazení na Cloudflare Pages

### Automatické nasazení:
1. Push kód do Git repository
2. Cloudflare Pages automaticky nasadí
3. Workers funkce budou dostupné na `/api/ratings`

### Ruční nasazení:
```bash
# Nasazení stránek
wrangler pages deploy _site

# Nasazení funkcí
wrangler pages functions deploy
```

## 8. Nastavení environment variables

V Cloudflare Pages dashboard:
1. Jděte do Settings > Environment variables
2. Přidejte:
   - `ENVIRONMENT=production`

## 9. Přidání Bindings v Pages

V Cloudflare Pages dashboard:
1. Jděte do Settings > Functions
2. Přidejte D1 database binding:
   - Variable name: `DB`
   - D1 database: `vzhuruvpred-ratings`
3. Přidejte KV namespace binding:
   - Variable name: `RATINGS_KV`
   - KV namespace: (váš vytvořený namespace)

## 10. Test produkčního API

```bash
# Test GET
curl "https://your-site.pages.dev/api/ratings?article=test-article"

# Test POST
curl -X POST "https://your-site.pages.dev/api/ratings?article=test-article" \
  -H "Content-Type: application/json" \
  -d '{"rating":"love","fingerprint":"test123"}'
```

## 11. Monitoring a debugování

### Cloudflare Dashboard:
- Analytics: Sledujte počet requests
- Logs: Real-time logi z Workers
- D1 Console: SQL queries na databázi

### Wrangler CLI:
```bash
# Zobrazení logů
wrangler pages functions tail

# Zobrazení dat v D1
wrangler d1 execute vzhuruvpred-ratings --command "SELECT * FROM ratings LIMIT 10"
```

## API Endpointy

### GET /api/ratings?article={articleId}
Vrací hodnocení pro článek:
```json
{
  "success": true,
  "ratings": {
    "love": 10,
    "like": 25,
    "neutral": 3,
    "dislike": 1,
    "bad": 0
  },
  "total": 39
}
```

### POST /api/ratings?article={articleId}
Přidá/aktualizuje hodnocení:
```json
{
  "rating": "love",
  "fingerprint": "abc123def456"
}
```

Odpověď:
```json
{
  "success": true,
  "message": "Rating added",
  "action": "added",
  "ratings": { ... },
  "total": 40
}
```

## Bezpečnostní features

- **Rate limiting**: 10 hlasů za hodinu na IP
- **Fingerprinting**: Prevence duplicate hlasů
- **CORS**: Nakonfigurováno pro cross-origin requests
- **Input validation**: Validace rating typů
- **SQL injection protection**: Parametrizované queries

## Troubleshooting

### API nefunguje:
1. Zkontrolujte Console v Developer Tools
2. Ověřte, že bindings jsou správně nastavené
3. Zkontrolujte Cloudflare Pages Functions logs

### Databáze chyby:
```bash
# Test připojení k databázi
wrangler d1 execute vzhuruvpred-ratings --command "SELECT COUNT(*) FROM ratings"
```

### CORS chyby:
- Zkontrolujte, že `Access-Control-Allow-Origin` je nastaveno
- Ověřte, že preflight OPTIONS requests fungují