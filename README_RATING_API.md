# Hodnocení článků - Přepnutí na API

Rating systém je momentálně nastaven na localStorage pro stabilní fungování. Když budou Cloudflare Functions připravené, přepněte na API podle tohoto návodu:

## Rychlé povolení API

### 1. Upravit konstantu v `/rating.html`:
```javascript
// Změnit z:
const USE_API = false;

// Na:
const USE_API = true;
```

### 2. Ověřit Cloudflare nastavení:
- D1 databáze vytvořena a nakonfigurována
- KV namespace vytvořen pro rate limiting  
- Bindings správně nastavené v Pages dashboard
- Functions nasazené a funkční

### 3. Test API endpoints:

**GET test:**
```bash
curl "https://vzhuruvpred.pages.dev/api/ratings?article=test"
```

**POST test:**
```bash
curl -X POST "https://vzhuruvpred.pages.dev/api/ratings?article=test" \
  -H "Content-Type: application/json" \
  -d '{"rating":"love","fingerprint":"test123"}'
```

## Aktuální stav - localStorage mód

### Výhody současného řešení:
- ✅ Funguje okamžitě bez backend
- ✅ Rychlé a responsivní
- ✅ Žádné API limity nebo chyby
- ✅ Funguje offline

### Nevýhody:
- ❌ Data pouze v prohlížeči uživatele
- ❌ Nesdílené mezi zařízeními
- ❌ Nelze agregovat globální statistiky

## Migrace na API později

Když přepnete `USE_API = true`:
- Existující localStorage data zůstanou jako fallback
- API se použije pro nová hodnocení
- Automatický fallback na localStorage při API chybách
- Postupná migrace dat z localStorage do databáze

## Cloudflare Functions status

Aktuální problém: HTTP 500 při volání `/api/ratings`

**Možné příčiny:**
1. Functions není nasazený na Cloudflare Pages
2. D1 databáze není správně propojena  
3. KV namespace není nakonfigurovaný
4. Missing bindings v Pages nastavení

**K vyřešení postupujte podle:** `CLOUDFLARE_SETUP.md`