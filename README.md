# Vzhůru a vpřed - Zpravodajský portál

Nezávislý zpravodajský portál zaměřený na digitalizace, transparentnost a technologické inovace.

## 🚀 Lokální spuštění

### Prerekvizity
- Ruby 2.7+ 
- Bundler gem

### Instalace
```bash
# Naklonujte repository
git clone [URL]
cd Vzhuruvpred

# Instalujte dependencies
bundle install

# Spusťte lokální server
bundle exec jekyll serve

# Otevřete v prohlížeči
http://localhost:4000
```

## 📁 Struktura projektu

```
├── _config.yml          # Jekyll konfigurace
├── _layouts/            # Layout templates
│   ├── default.html     # Základní layout
│   ├── home.html        # Homepage layout  
│   ├── post.html        # Layout pro články
│   └── category.html    # Layout pro kategorie
├── _includes/           # Komponenty
│   ├── header.html      # Navigace
│   ├── footer.html      # Patička
│   └── breaking-news.html
├── _posts/              # Články (Markdown)
├── assets/              # Statické soubory
│   ├── css/style.css    # Hlavní styly
│   └── js/main.js       # JavaScript
├── udalosti.html        # Stránka kategorie Události
├── nazory.html          # Stránka kategorie Názory  
├── analyzy.html         # Stránka kategorie Analýzy
├── kultura.html         # Stránka kategorie Kultura
└── index.html           # Homepage
```

## ✍️ Přidání nového článku

Vytvořte nový soubor v `_posts/` s názvem `YYYY-MM-DD-nazev-clanku.md`:

```yaml
---
layout: post
title: "Název článku"
date: 2024-01-15 10:00:00 +0100
categories: [udalosti] # udalosti, nazory, analyzy, kultura
author: "Jméno Autora"
author_title: "Pozice autora"
author_image: "URL k avataru"
image: "URL k hlavnímu obrázku"
excerpt: "Krátký popis článku"
tags: [tag1, tag2, tag3]
category: "Kategorie"
read_time: "5 min"
---

Obsah článku v Markdownu...
```

## 🎨 Přizpůsobení

### Barvy
Hlavní barvy jsou definované v CSS proměnných v `assets/css/style.css`:

```css
:root {
    --pirate-black: #000000;
    --pirate-white: #ffffff;  
    --pirate-yellow: #FEC900;
    --pirate-yellow-dark: #F2C700;
}
```

### Navigace
Upravte navigaci v `_config.yml`:

```yaml
navigation:
  - name: "Domů"
    link: "/"
  - name: "Události" 
    link: "/udalosti/"
  # ...
```

## 📱 Responzivní design

Stránka je plně responzivní s breakpointy:
- Desktop: 1280px+
- Tablet: 768px - 1279px  
- Mobile: 480px - 767px
- Small mobile: <480px

## 🔧 Deployment

### GitHub Pages
1. Push do GitHub repository
2. V Settings -> Pages vyberte Source: GitHub Actions
3. Site se automaticky buildne a deployuje

### Cloudflare Pages  
1. Připojte GitHub repository
2. Build command: `bundle exec jekyll build`
3. Build output directory: `_site`
4. Environment variables: `RUBY_VERSION=2.7`

### Netlify
1. Připojte repository
2. Build command: `bundle exec jekyll build`
3. Publish directory: `_site`

## 🎯 Features

- ✅ Responzivní design
- ✅ Dark/Light mode toggle
- ✅ Rychlé vyhledávání
- ✅ Newsletter signup
- ✅ Social media sharing
- ✅ SEO optimalizace
- ✅ RSS feed
- ✅ Sitemap.xml
- ✅ Progressive Web App ready

## 📄 Licence

Obsah pod Creative Commons licencí. Kód pod MIT licencí.

## 🤝 Přispívání

1. Forkněte repository
2. Vytvořte feature branch
3. Commitněte změny  
4. Pushněte do branch
5. Otevřete Pull Request

## 📞 Kontakt

- Email: ahoj@vzhuruavpred.cz
- Matrix: @news:piraten.chat