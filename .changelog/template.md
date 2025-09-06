# 📝 Changelog Entry Template

## Použití
Zkopírujte příslušnou sekci a přidejte do `CHANGELOG.md` pod `## [Unreleased]`

---

## 🆕 Nové funkcionality (Přidáno)

```markdown
### Přidáno
- **[Název funkce]** - [stručný popis co to dělá]
  - [Technický detail 1]  
  - [Technický detail 2]
  - Soubory: `file1.html`, `file2.js`
```

**Příklady:**
```markdown
### Přidáno
- **Dark mode toggle** - uživatelé mohou přepínat mezi světlým a tmavým motivem
  - LocalStorage persistence nastavení
  - Automatická detekce systémového nastavení  
  - Soubory: `_includes/header.html`, `assets/js/theme.js`

- **Search funkcionalita** - rychlé vyhledávání v článcích
  - Živé vyhledávání při psaní
  - Zvýrazňování výsledků
  - Podpora českých diakritiky
```

---

## 🔧 Opravy chyb (Opraveno) 

```markdown
### Opraveno
- **[Problém]** - [jak bylo řešeno]
  - Impact: [kdo to ovlivňuje]
  - Root cause: [původní příčina]
  - Soubor: `problematic-file.js:123`
```

**Příklady:**
```markdown
### Opraveno  
- **Mobilní navigace se nezavírá** - oprava event listeneru pro dotykové obrazovky
  - Impact: všichni mobilní uživatelé
  - Root cause: chybějící touchend event
  - Soubor: `assets/js/main.js:45-62`

- **404 chyby pro RSS feed** - opraven neplatný XML v jekyll-feed
  - Impact: RSS čtečky, SEO boti
  - Root cause: neescapované HTML v popisech
  - Soubor: `_config.yml`, `_layouts/post.html`
```

---

## 🔄 Změny funkcí (Změněno)

```markdown
### Změněno
- **[Funkce]** - [co se změnilo a proč]
  - Před: [předchozí stav]
  - Po: [nový stav] 
  - Důvod: [proč změna]
```

**Příklady:**
```markdown
### Změněno
- **URL struktura článků** - zjednodušeno z `/kat/rok/měsíc/den/název/` na `/kat/rok-měsíc-den/název/`
  - Před: `/udalosti/2024/09/05/clanek/`
  - Po: `/udalosti/2024-09-05/clanek/`
  - Důvod: jednodušší URL, lepší SEO

- **Výchozí téma** - změněno z světlého na automatické dle systému
  - Respektuje prefers-color-scheme
  - Fallback na světlé téma pro starší prohlížeče
```

---

## 🗑️ Odstraněné funkce (Odstraněno)

```markdown
### Odstraněno
- **[Funkce]** - [proč byla odstraněna]
  - Nahrazeno: [čím byla nahrazena]
  - Migration: [jak migrovat]
```

**Příklady:**
```markdown
### Odstraněno
- **jQuery dependency** - odstraněna pro zmenšení bundle size
  - Nahrazeno: vanilla JavaScript
  - Migration: všechny komponenty přepsány do ES6
  - Soubor: odstraněn `assets/js/jquery.min.js`
```

---

## 🔒 Bezpečnostní záplaty (Bezpečnost)

```markdown
### Bezpečnost
- **[Typ zranitelnosti]** - [jak bylo opraveno]
  - CVSS Score: [skóre pokud známe]
  - Affected: [postižené komponenty]
```

**Příklady:**
```markdown
### Bezpečnost
- **XSS v komentářích** - implementováno escapování HTML v user inputu
  - Affected: všechny uživatelské komentáře před 2024-09-05
  - Fix: automatické sanitizace všech HTML tagů
  - Soubor: `_includes/comments.html`
```

---

## 📊 Výkonnostní vylepšení

```markdown  
### Změněno
- **[Komponenta] výkon** - [zlepšení]
  - Před: [původní metrika]
  - Po: [nová metrika]
  - Metoda: [jak dosaženo]
```

**Příklady:**
```markdown
### Změněno
- **Načítání obrázků** - implementován lazy loading
  - Před: všechny obrázky načteny okamžitě (2.3s LCP)
  - Po: lazy loading s intersection observer (0.8s LCP) 
  - Metoda: native `loading="lazy"` + JS fallback
```

---

## 🎨 UI/UX změny

```markdown
### Změněno  
- **[UI komponenta]** - [vizuální/UX změna]
  - Vylepšení: [co je lepší]
  - Design: [designové změny]
```

**Příklady:**
```markdown
### Změněno
- **Navigation menu design** - modernější vzhled s animations
  - Vylepšení: lepší contrast ratio (4.7:1), hover states
  - Design: přechod na CSS Grid, micro-interactions
  - Accessibility: přidána ARIA labels, focus management
```

---

## ⚡ Rychlý checklist před přidáním

- [ ] Je popis srozumitelný pro uživatele (ne jen pro programátory)?
- [ ] Obsahuje technické detaily pro vývojáře?
- [ ] Specifikuje dopad na uživatele?
- [ ] Uvádí související soubory při větších změnách?
- [ ] Je kategorie správná (Přidáno/Změněno/Opraveno/...)?
- [ ] Datum je správné (nebo je v sekci Unreleased)?