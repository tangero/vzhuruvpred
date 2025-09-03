# Správa autorů

Systém používá centralizovanou databázi autorů v souboru `_data/authors.yml` s fallback mechanismem pro výjimečné přispěvatele.

## Jak přidat nového autora

### Krok 1: Přidání do databáze
Editujte `_data/authors.yml` a přidejte nového autora:

```yaml
jmeno-prijmeni:  # slug autora (lowercase, pomlčky)
  name: "Jméno Příjmení"
  title: "pozice/titul autora"
  bio: "Krátký popisek o autorovi a jeho expertize"
  email: "email@example.com"  # volitelné
  avatar: "/assets/obrazky/jmeno-prijmeni.jpg"
  social:  # volitelné sociální média
    twitter: "@username"
    linkedin: "linkedin-profile"
    website: "https://website.com"
```

### Krok 2: Nahrání avataru
Umístěte obrázek autora do `/assets/obrazky/` s vhodným názvem.

### Krok 3: Použití v článku
V YAML hlavičce článku stačí uvést:
```yaml
author: "Jméno Příjmení"
```

Systém automaticky načte všechny informace z databáze.

## Fallback pro výjimečné přispěvatele

Pro autory, kteří nejsou v databázi, můžete použít klasické YAML pole:

```yaml
author: "Host Jednorázový"
author_title: "externí expert"
author_bio: "Krátký popis pro tohoto článek"
author_image: "/assets/obrazky/host.jpg"
```

## Struktura autor sekce

Autor sekce automaticky zobrazí:
- Avatar obrázek
- Jméno a titul
- Biografii (pokud je k dispozici)
- Sociální média (pokud jsou uvedena)
- Odkaz na všechny články autora

## Výhody centralizovaného systému

- **Konzistence**: Jednotné informace napříč články
- **Správa**: Změna informací o autorovi na jednom místě
- **Rozšiřitelnost**: Snadné přidání nových polí
- **Flexibilita**: Fallback pro výjimečné přispěvatele