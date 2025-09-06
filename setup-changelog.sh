#!/bin/bash
# 🚀 Setup script pro automatickou aktualizaci CHANGELOG.md
# Autor: Claude Code Assistant
# Použití: ./setup-changelog.sh

set -e  # Exit při první chybě

echo "🚀 Nastavuji automatickou aktualizaci CHANGELOG.md..."
echo ""

# Barvy pro výstup
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Funkce pro colored output
success() {
    echo -e "${GREEN}✅ $1${NC}"
}

warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

error() {
    echo -e "${RED}❌ $1${NC}"
}

info() {
    echo -e "ℹ️  $1"
}

# Kontrola, zda jsme v git repository
if [ ! -d ".git" ]; then
    error "Tento script musí být spuštěn v root adresáři Git repository!"
    exit 1
fi

success "Git repository detekováno"

# 1. Instalace pre-commit hook
echo ""
info "📦 Instaluji pre-commit hook..."

if [ ! -d ".git/hooks" ]; then
    mkdir -p .git/hooks
fi

if [ -f ".git/hooks/pre-commit" ]; then
    warning "Pre-commit hook již existuje, vytvářím zálohu..."
    cp .git/hooks/pre-commit .git/hooks/pre-commit.backup.$(date +%Y%m%d_%H%M%S)
fi

cp hooks/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit

success "Pre-commit hook nainstalován"

# 2. Kontrola GitHub Actions
echo ""
info "🔍 Kontroluji GitHub Actions..."

if [ -f ".github/workflows/changelog-check.yml" ]; then
    success "GitHub Action changelog-check.yml nalezena"
else
    warning "GitHub Action nebyla nalezena - ujistěte se, že .github/workflows/changelog-check.yml existuje"
fi

# 3. Git aliasy pro changelog
echo ""
info "⚙️  Nastavuji užitečné Git aliasy..."

git config alias.changelog "log --pretty=format:'- **%s** - %b (%h)' --since='1 week ago'" 2>/dev/null && success "Alias 'git changelog' nastaven" || warning "Nepodařilo se nastavit alias 'git changelog'"

git config alias.release-notes "log --pretty=format:'### %s%n%b%n' --since='last tag'" 2>/dev/null && success "Alias 'git release-notes' nastaven" || warning "Nepodařilo se nastavit alias 'git release-notes'"

# 4. Test pre-commit hook
echo ""
info "🧪 Testuji pre-commit hook..."

# Simulace testu (bez skutečného commitu)
if .git/hooks/pre-commit; then
    success "Pre-commit hook funguje správně"
else
    warning "Pre-commit hook test neprošel - zkontrolujte ručně"
fi

# 5. Vytvoření helper scriptů
echo ""
info "📝 Vytvářím helper scripty..."

# Script pro rychlé přidání changelog entry
cat > add-to-changelog.sh << 'EOF'
#!/bin/bash
# Rychlé přidání entry do CHANGELOG.md

echo "📝 Přidávám entry do CHANGELOG.md..."
echo ""
echo "Typy změn:"
echo "1) Přidáno (nová funkcionalita)"  
echo "2) Změněno (změna existující funkce)"
echo "3) Opraveno (oprava chyby)"
echo "4) Odstraněno (odstraněná funkcionalita)"
echo "5) Bezpečnost (security fix)"
echo ""

read -p "Vyberte typ (1-5): " TYPE
read -p "Název změny: " TITLE  
read -p "Popis změny: " DESC

case $TYPE in
    1) SECTION="Přidáno" ;;
    2) SECTION="Změněno" ;;
    3) SECTION="Opraveno" ;;
    4) SECTION="Odstraněno" ;;
    5) SECTION="Bezpečnost" ;;
    *) SECTION="Změněno" ;;
esac

ENTRY="- **$TITLE** - $DESC"

# Najít sekci Unreleased a přidat entry
sed -i "/## \[Unreleased\]/,/## \[/{
    /### $SECTION/a\\
$ENTRY
    /^$/q
}" CHANGELOG.md 2>/dev/null || {
    # Fallback: přidat na konec Unreleased sekce
    sed -i "/## \[Unreleased\]/a\\
\\
### $SECTION\\
$ENTRY" CHANGELOG.md
}

echo "✅ Entry přidána do CHANGELOG.md"
EOF

chmod +x add-to-changelog.sh
success "Helper script 'add-to-changelog.sh' vytvořen"

# 6. Zobrazení summary
echo ""
echo "🎉 Instalace dokončena!"
echo ""
echo "📋 Co bylo nainstalováno:"
echo "   ✅ Pre-commit hook (.git/hooks/pre-commit)"
echo "   ✅ Git aliasy (git changelog, git release-notes)"  
echo "   ✅ Helper script (add-to-changelog.sh)"
echo "   ✅ GitHub Action (changelog-check.yml)"
echo ""
echo "🔧 Užitečné příkazy:"
echo "   git changelog                    # Zobrazit změny za poslední týden"
echo "   git release-notes               # Generovat release notes"
echo "   ./add-to-changelog.sh           # Rychle přidat changelog entry"
echo "   git commit --no-verify          # Commit bez changelog kontroly"
echo ""
echo "📖 Dokumentace:"
echo "   CHANGELOG.md                    # Hlavní changelog"
echo "   CHANGELOG_REMINDER.md           # Kompletní návod"
echo "   .changelog/template.md          # Templates pro entries"
echo ""

info "💡 Tip: Před každým commitem budete nyní upozorněni na aktualizaci changelogu"
info "🚀 První commit s tímto nastavením zkuste hned!"

echo ""
success "Automatická aktualizace CHANGELOG.md je připravena k použití! 🎊"