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
