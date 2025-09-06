# 🔄 Automatická aktualizace CHANGELOG.md

Tento dokument obsahuje systém pro zajištění pravidelné aktualizace changelogu.

## 📋 Kontrolní seznam po každé změně

Když provedete změnu v projektu, zkontrolujte tento seznam:

### ✅ Před commitem:
- [ ] Přidal jsem změnu do `CHANGELOG.md` sekce `[Unreleased]`?
- [ ] Specifikoval jsem typ změny (Přidáno/Změněno/Opraveno/atd.)?
- [ ] Popsal jsem změnu srozumitelně pro uživatele?
- [ ] Přidal jsem technické detaily, pokud je to relevantní?

### ✅ Při vytváření release:
- [ ] Přesunul jsem všechny položky z `[Unreleased]` do nové verze?
- [ ] Přidal jsem datum release ve formátu YYYY-MM-DD?
- [ ] Inkrementoval jsem verzi podle sémantického verzování?
- [ ] Vytvořil jsem Git tag pro novou verzi?

## 🤖 Automatické připomínky

### Pre-commit hook
Přidejte do `.git/hooks/pre-commit`:

```bash
#!/bin/bash
# Kontrola, zda byla aktualizován CHANGELOG.md

if git diff --cached --name-only | grep -E "(\.js|\.html|\.md|\.yml|\.css)$" > /dev/null; then
    if ! git diff --cached --name-only | grep "CHANGELOG.md" > /dev/null; then
        echo "⚠️  UPOZORNĚNÍ: Provádíte změny, ale neaktualizovali jste CHANGELOG.md"
        echo "   Zvažte přidání změny do sekce [Unreleased]"
        echo ""
        echo "   Pro pokračování bez aktualizace použijte: git commit --no-verify"
        read -p "   Pokračovat? (y/N) " -n 1 -r
        echo ""
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
fi
```

### GitHub Action (připraveno k použití)

Vytvořte `.github/workflows/changelog-check.yml`:

```yaml
name: Changelog Check
on:
  pull_request:
    branches: [ main ]

jobs:
  changelog:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
      with:
        fetch-depth: 0
    
    - name: Check if CHANGELOG was updated
      run: |
        if git diff --name-only origin/main...HEAD | grep -E "(\.js|\.html|\.md|\.yml|\.css)$" > /dev/null; then
          if ! git diff --name-only origin/main...HEAD | grep "CHANGELOG.md" > /dev/null; then
            echo "⚠️ CHANGELOG.md nebyl aktualizován"
            echo "::warning::Zvažte přidání změn do CHANGELOG.md"
          else
            echo "✅ CHANGELOG.md byl aktualizován"
          fi
        fi
```

## 📝 Template pro changelog entries

### Formát pro nové položky:

```markdown
### Přidáno
- **Název funkce** - stručný popis co to dělá
  - Technické detaily
  - Související soubory: `file1.html`, `file2.js`

### Opraveno  
- **Problém XYZ** - jak bylo řešeno
  - Impact: kdo to ovlivňuje
  - Soubory: `problematic-file.js:123`
```

### Příklady dobrých changelog položek:

```markdown
### Přidáno
- **Dark mode toggle** - uživatelé mohou přepínat mezi světlým a tmavým motivem
  - LocalStorage persistence nastavení
  - Automatická detekce systémového nastavení
  - Soubory: `_includes/header.html`, `assets/js/theme.js`

### Opraveno
- **Mobilní navigace se nezavírá** - oprava event listeneru pro dotykové obrazovky  
  - Impact: všichni mobilní uživatelé
  - Root cause: chybějící touchend event
  - Soubor: `assets/js/main.js:45-62`
```

## 🎯 Sémantické verzování

### Kdy inkrementovat verzi:

- **MAJOR (x.0.0)** - breaking changes, nekompatibilní API změny
- **MINOR (x.y.0)** - nové funkcionality, zpětně kompatibilní
- **PATCH (x.y.z)** - opravy chyb, zpětně kompatibilní

### Příklady:
- Nový rating systém → `2.1.0` (minor - nová funkcionalita)
- Oprava 404 chyby → `2.0.1` (patch - bug fix)
- Změna URL struktury → `3.0.0` (major - breaking change)

## 🔧 Užitečné příkazy

### Git aliasy pro changelog:
```bash
git config alias.changelog "log --pretty=format:'- %s (%h)' --since='1 week ago'"
git config alias.release-notes "log --pretty=format:'### %s%n%b%n' --since='last tag'"
```

### Automatické generování changelog z commitů:
```bash
# Zobrazit commity od posledního release
git log --oneline $(git describe --tags --abbrev=0)..HEAD

# Generovat changelog template
git log --pretty=format:"- **%s** - %b" --since="last tag" > temp-changelog.md
```

## 📊 Monitoring changelog aktuálnosti

Pro pravidelnou kontrolu vytvořte script `check-changelog-freshness.sh`:

```bash
#!/bin/bash
LAST_CHANGE=$(git log -1 --format=%ct -- CHANGELOG.md)
LAST_CODE_CHANGE=$(git log -1 --format=%ct --grep="feat\|fix\|add" .)
DAYS_DIFF=$(( (LAST_CODE_CHANGE - LAST_CHANGE) / 86400 ))

if [ $DAYS_DIFF -gt 7 ]; then
    echo "⚠️  CHANGELOG.md je starší než 7 dní od poslední významné změny"
    echo "   Zvažte aktualizaci changelogu"
fi
```

---

**💡 Tip:** Přidejte si připomínku do kalendáře každý týden na kontrolu changelogu!