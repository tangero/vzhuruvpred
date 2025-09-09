# Changelog

Všechny významné změny v projektu "Vzhůru a vpřed" jsou dokumentovány v tomto souboru.

Formát je založený na [Keep a Changelog](https://keepachangelog.com/cs/1.1.0/),
a projekt dodržuje [Sémantické verzování](https://semver.org/lang/cs/).

## [2.3.0] - 2025-09-09
- počasí, jeho následný přesun na spodek stránky 

## [2.2.0] - 2025-09-08

### Přidáno
- **SEO optimalizace** - kompletní Open Graph meta tagy pro Facebook/Twitter sdílení
- **JSON-LD structured data** - Organization, Website, Article a Breadcrumb schéma pro vyhledávače
- **Robots.txt** - optimalizovaný pro crawlery s odkazy na sitemap a feed
- **Stránka Ochrana soukromí** - transparentní informace o žádném sledování a cookies
- **Stránka Podmínky užití** - Creative Commons licence a pravidla komentářů
- **Stránka Podpořte nás** - transparentní účet pro dary s QR kódem pro platby
- **Page layout** - stylový layout pro statické stránky s pirátským designem

### Změněno
- **Footer odkazy** - aktualizované na reálné stránky místo placeholder #
- **SEO konfigurace** - production URL a social media nastavení v _config.yml
- **Meta tagy** - rozšířené o keywords, canonical URL a Twitter Cards
- **Kontaktní informace** - konfigurovatelné přes _config.yml místo hardcoded

### Opraveno
- **Překrývající text** v trending boxech - odstraněn zdroj a počet hledání
- **Chybějící obrázky** ve světových zprávách - placeholder systém s fallback obsahem

### Plánované
- Povolení Cloudflare API pro hodnocení článků
- Rozšíření systému komentářů
- Vylepšení responsivního designu
- Pokročilé vyhledávání v článcích

## [2.1.0] - 2025-09-05

### Přidáno
- **Systém hodnocení článků** s 5 emotikony (😍 😊 🤔 😕 😢)
  - Interaktivní hodnocení bez nutnosti registrace
  - LocalStorage pro persistenci hlasů
  - Animace a vizuální zpětná vazba
  - Responsivní design pro všechna zařízení
- **Cloudflare Workers + D1 Backend** (připraveno k nasazení)
  - API endpoints pro hodnocení (`/api/ratings`)
  - Rate limiting (10 hlasů/hodinu na IP)
  - User fingerprinting proti duplicate voting
  - SQL databáze s optimalizovanými indexy
- **Vylepšený systém komentářů**
  - Giscus integrace s GitHub Discussions
  - Modernější design s Pirate Party tématikou
  - Lepší vizuální oddělení od hodnocení
- **Setup dokumentace**
  - `CLOUDFLARE_SETUP.md` - detailní návod pro deployment
  - `README_RATING_API.md` - povolení API módu

### Změněno
- **Struktura URL článků** - zjednodušeno na `/kategorie/podkategorie/YYYY-MM-DD/nazev/`
- **Design komentářů** - modernější vzhled s gradient bordarmi
- **Responsivní layout** - vylepšené zobrazení na mobilních zařízeních

### Opraveno
- **API fallback mechanismus** - spolehlivý localStorage fallback při API chybách
- **Jekyll build proces** - přidány chybějící Ruby gems pro 3.4+ kompatibilitu
- **Permalink struktura** - konzistentní URL formát napříč celým webem

### Technické detaily
- Nové soubory: `_includes/rating.html`, `functions/api/ratings.js`, `migrations/001_create_ratings.sql`
- Aktualizace: `_layouts/post.html`, `_includes/comments.html`, `wrangler.toml`
- Dependencies: přidáno `ostruct` gem pro Ruby 3.4+

## [2.0.0] - 2025-08-31

### Přidáno
- **Kompletní redesign webu** - moderní Pirate Party design
- **Automatické získávání světových zpráv** pomocí Python scriptů
- **Trendové sekce** na hlavní stránce
- **Autor database** - centralizovaná správa autorů v `_data/authors.yml`
- **Media kolekce** - podpora pro audio a video obsah
- **YouTube integrace** - embed přehrávač pro videa
- **Rozšířená navigace** - nové sekce (Technologie, Přednášky)
- **GitHub Workflows** - automatizace obsahu a trendů

### Změněno
- **Struktura webu** - přechod z jednoduchého layoutu na komplexní CMS
- **CSS framework** - vlastní Pirate Party design system
- **Kategorizace článků** - rozšíření a lepší organizace
- **Typography** - Bebas Neue pro nadpisy, Roboto pro text

### Technické vylepšení
- **Performance optimalizace** - lazy loading obrázků, optimalizované CSS
- **SEO vylepšení** - strukturovaná data, meta tagy, sitemap
- **Build proces** - Jekyll s pokročilými plugins a automation
- **Mobile-first design** - plně responsivní napříč všemi zařízeními

## [1.0.0] - 2024-01-15

### Přidáno
- **Základní Jekyll struktura** - přechod ze statického HTML
- **Responsive design** - mobilní optimalizace
- **Základní kategorie** - Události, Názory, Analýzy, Kultura  
- **RSS feed** - automatické generování pomocí jekyll-feed
- **Sitemap.xml** - SEO optimalizace
- **Sample články** - demonstrační obsah pro testování

### Technické základy
- Jekyll 4.3+ s modern Ruby kompatibilitou
- Pirate Party color scheme (černá, žlutá, bílá)
- Mobile-first responsive breakpoints
- Základní SEO meta tagy
- Git repository struktura

---

## Konvence pro changelog

### Typy změn
- **Přidáno** (`Added`) - nové funkcionality
- **Změněno** (`Changed`) - změny existujících funkcí
- **Zastaralé** (`Deprecated`) - funkce označené k odstranění
- **Odstraněno** (`Removed`) - odstraněné funkcionality  
- **Opraveno** (`Fixed`) - opravy chyb
- **Bezpečnost** (`Security`) - bezpečnostní záplaty

### Formát položek
- Použít **tučný text** pro klíčové funkce
- Přidat technické detaily pod hlavní popis
- Uvést související soubory při větších změnách
- Datovat verze ve formátu YYYY-MM-DD
- Používat česky pro uživatelské funkce, anglicky pro technické termíny