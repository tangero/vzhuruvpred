# 📋 Automatická aktualizace CHANGELOG.md - Návod k použití

Tento projekt má nastaven kompletní systém pro automatickou aktualizaci changelogu. Zde je přehled jak funguje a jak jej používat.

## 🚀 Co je nastaveno

### ✅ Automatické nástroje AKTIVNÍ:
- **Pre-commit hook** - kontrola před každým commitem
- **GitHub Action** - kontrola v pull requestech  
- **Git aliasy** - užitečné příkazy pro changelog
- **Helper scripty** - rychlé přidání entries
- **Templates** - formáty pro různé typy změn

## 🔄 Jak aktualizace funguje

### 1. **Před každým commitem:**
Když commitujete změny, pre-commit hook automaticky:
- 🔍 Zkontroluje, zda jste změnili zdrojové soubory
- ⚠️ Upozorní, pokud jste neaktualizovali CHANGELOG.md
- ✅ Potvrdí správný formát changelog entries
- 💡 Navrhne typ změny na základě commit message

### 2. **V Pull Requestech:**
GitHub Action automaticky:
- 📊 Analyzuje změněné soubory
- 💬 Přidá komentář k PR pokud changelog chybí
- ✅ Označí PR jako ready pokud je changelog aktuální
- 📋 Vygeneruje summary report

### 3. **Při vytváření release:**
- Manuálně přesunete entries z `[Unreleased]` do nové verze
- Přidáte datum a verzi podle sémantického verzování
- Vytvoříte Git tag pro release

## 📝 Jak přidat změnu do changelogu

### Metoda 1: Rychlý helper script
```bash
./add-to-changelog.sh
```
- Interaktivně se zeptá na typ změny
- Automaticky přidá správně formátovanou entry

### Metoda 2: Manuálně podle template
1. Otevřete `CHANGELOG.md`
2. Najděte sekci `## [Unreleased]`  
3. Přidejte entry podle vzoru v `.changelog/template.md`

### Metoda 3: Kopírování z templateu
```bash
# Zobrazit template
cat .changelog/template.md

# Zkopírovat relevantní část
```

## 🎯 Formát changelog entries

### Struktura:
```markdown
### [Typ změny]
- **[Název]** - [popis co to dělá]
  - [Technický detail 1]
  - [Technický detail 2]  
  - Soubory: `file1.html`, `file2.js`
```

### Typy změn:
- **Přidáno** - nové funkcionality
- **Změněno** - změny existujících funkcí
- **Opraveno** - opravy chyb  
- **Odstraněno** - odstraněné funkcionality
- **Bezpečnost** - bezpečnostní záplaty

## 🔧 Užitečné příkazy

### Git aliasy (automaticky nastavené):
```bash
git changelog          # Změny za poslední týden
git release-notes      # Release notes od posledního tagu
```

### Helper scripty:
```bash
./add-to-changelog.sh  # Rychle přidat entry
./setup-changelog.sh   # Znovu nastavit automatizaci (pokud potřeba)
```

### Bypass changelog kontroly:
```bash
git commit --no-verify # Commit bez changelog kontroly
```

## 📊 Monitoring a statistiky

### Zobrazit changelog aktivity:
```bash
# Kdy byl changelog naposledy aktualizován
git log -1 --format="%cd" -- CHANGELOG.md

# Počet changelog entries tento měsíc
git log --since="1 month ago" --oneline -- CHANGELOG.md | wc -l

# Nejčastější typy změn
grep -E "^### " CHANGELOG.md | sort | uniq -c | sort -nr
```

### GitHub Analytics:
- PR komentáře s changelog připomínkami
- Workflow runs changelog-check
- Release history a frequency

## 🎨 Customizace

### Změna formátu entries:
Upravte templates v `.changelog/template.md`

### Úprava pre-commit kontroly:
Upravte `hooks/pre-commit` nebo `.git/hooks/pre-commit`

### Změna GitHub Action:
Upravte `.github/workflows/changelog-check.yml`

## 🐛 Troubleshooting

### Pre-commit hook se nespouští:
```bash
# Zkontrolovat, zda je executable
ls -la .git/hooks/pre-commit

# Znovu nastavit
chmod +x .git/hooks/pre-commit
```

### GitHub Action nefunguje:
- Zkontrolujte, že je soubor v `.github/workflows/`
- Ověřte YAML syntaxi
- Zkontrolujte GitHub Actions tab v repository

### Chybný formát changelog:
```bash
# Použít template
cp .changelog/template.md temp.md
# Upravit a zkopírovat do CHANGELOG.md
```

## 📈 Výhody automatizace

### ✅ Pro vývojáře:
- Nikdy nezapomenete na changelog
- Konzistentní formát across team
- Automatické připomínky a návody
- Rychlé templates pro common změny

### ✅ Pro projekt:
- Kompletní historie změn
- Professional release notes  
- Lepší communication s uživateli
- Snadnější debugging a rollbacks

### ✅ Pro údržbu:
- Automated quality checks
- Standardizovaný proces
- Reduced manual work
- Better documentation culture

---

## 🎊 Gratulujeme!

Váš projekt má nyní nastaven plně automatizovaný changelog systém. 

**Každá změna bude automaticky trackována a dokumentována!** 📊✨

### Příští kroky:
1. 📝 Commit this documentation
2. 🧪 Test the system with your next feature
3. 🚀 Create your first release with proper changelog
4. 📊 Monitor and improve the process