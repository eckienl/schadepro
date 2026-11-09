#!/usr/bin/env python3
"""Bouwt de statische SchadePro-site.

Gebruik:  python3 tools/build.py
Bron:     src/layout.html, src/partials/*.html, src/pages/*.html
Uitvoer:  *.html in de hoofdmap + sitemap.xml (deze bestanden worden door Vercel geserveerd).

Pas teksten aan in src/pages/ en draai daarna het script opnieuw.
"""
import html
import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
SITE = "https://schadepro.nl"
VERSION = date.today().strftime("%Y%m%d")
PHONE = "+31655367559"

NAV = [
    ("/", "Home"),
    ("/schilderwerk", "Schilderwerk"),
    ("/latexspuitwerk", "Latexspuitwerk"),
    ("/onderhoud-schadeherstel", "Onderhoud &amp; schadeherstel"),
    ("/werkgebied", "Werkgebied"),
    ("/contact", "Contact"),
]

PLACES = ["Utrecht", "Houten", "Nieuwegein", "Zeist", "Bilthoven", "Bosch en Duin",
          "Doorn", "Odijk", "Maarssen", "IJsselstein", "Woerden", "Vianen", "Amsterdam"]

BUSINESS = {
    "@type": ["HousePainter", "LocalBusiness"],
    "@id": f"{SITE}/#bedrijf",
    "name": "SchadePro",
    "alternateName": "SchadePro.nl",
    "description": "Schilder, latexspuiter en specialist in onderhoud en schadeherstel voor particulieren en bedrijven in regio Utrecht.",
    "slogan": "Uw herstelpartner van alle schades voor particulieren en bedrijven",
    "url": f"{SITE}/",
    "logo": f"{SITE}/apple-touch-icon.png",
    "image": [f"{SITE}/assets/img/og-schadepro.jpg", f"{SITE}/assets/img/schadepro-schilder-bus-spuitmachines.jpg"],
    "telephone": PHONE,
    "email": "schadepro@ziggo.nl",
    "founder": {"@type": "Person", "name": "P.G.A. van Eck"},
    "address": {"@type": "PostalAddress", "addressLocality": "Utrecht", "addressRegion": "Utrecht", "addressCountry": "NL"},
    "geo": {"@type": "GeoCoordinates", "latitude": 52.0907, "longitude": 5.1214},
    "areaServed": [{"@type": "City", "name": p} for p in PLACES],
    "knowsAbout": ["Schilderwerk", "Latexspuitwerk", "Latex spuiten", "Schadeherstel", "Onderhoud", "Glasvlies behangen", "Houtrotreparatie"],
    "hasOfferCatalog": {
        "@type": "OfferCatalog",
        "name": "Diensten SchadePro",
        "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Schilderwerk", "url": f"{SITE}/schilderwerk"}},
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Latexspuitwerk", "url": f"{SITE}/latexspuitwerk"}},
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Onderhoud en schadeherstel", "url": f"{SITE}/onderhoud-schadeherstel"}},
        ],
    },
    "sameAs": ["https://www.instagram.com/schadepro/"],
}

WEBSITE = {"@type": "WebSite", "@id": f"{SITE}/#website", "url": f"{SITE}/", "name": "SchadePro.nl",
           "inLanguage": "nl-NL", "publisher": {"@id": f"{SITE}/#bedrijf"}}

# ---------------------------------------------------------------- pagina's
PAGES = {
    "home": {
        "out": "index.html", "path": "/",
        "title": "Schilder & schadeherstel regio Utrecht | SchadePro",
        "description": "SchadePro: schilderwerk, latexspuitwerk, onderhoud en schadeherstel voor particulieren en bedrijven in Utrecht, Houten, Nieuwegein, Zeist en omgeving. Vraag vrijblijvend advies aan.",
        "preload": "schadepro-schilder-bus-spuitmachines",
        "bodyclass": "page-home",
        "faq": [
            ("Wat doet SchadePro?",
             "SchadePro is uw herstelpartner voor particulieren en bedrijven. We verzorgen schilderwerk binnen en buiten, latexspuitwerk voor wanden en plafonds, glasvlies- en behangwerk en onderhoud en herstel van schade aan wanden, plafonds en houtwerk."),
            ("In welke regio werken jullie?",
             "We werken in de regio Utrecht, waaronder Utrecht, Houten, Nieuwegein, Zeist, Bilthoven, Bosch en Duin, Doorn, Odijk, Maarssen, IJsselstein, Woerden en Vianen. Voor grotere klussen komen we ook naar Amsterdam."),
            ("Werken jullie voor particulieren én bedrijven?",
             "Ja. We werken voor huiseigenaren en huurders, maar ook voor bedrijven, VvE's, verhuurders en aannemers. Voor zakelijke klanten plannen we flexibel, bijvoorbeeld tussen twee huurders in of buiten kantooruren."),
            ("Is een offerte vrijblijvend?",
             "Ja. We komen graag langs om de situatie te bekijken en u advies te geven. Daarna ontvangt u een duidelijke offerte, zonder verplichtingen."),
            ("Hoe snel kunnen jullie beginnen?",
             "Dat hangt af van de planning en de omvang van de klus. Neem contact op via 06 55 36 75 59 of schadepro@ziggo.nl; we reageren snel en denken mee over een passende startdatum."),
        ],
    },
    "schilderwerk": {
        "out": "schilderwerk.html", "path": "/schilderwerk",
        "title": "Schilder regio Utrecht – binnen & buiten | SchadePro",
        "description": "Schilder nodig in regio Utrecht? SchadePro verzorgt binnen- en buitenschilderwerk, kozijnen, deuren, trappen en glasvlies- en behangwerk. Netjes, vakkundig en met een heldere offerte.",
        "crumb": "Schilderwerk",
        "service": ("Schilderwerk", "Binnen- en buitenschilderwerk, kozijnen, deuren, trappen, glasvlies- en behangwerk."),
        "faq": [
            ("Wat kost een schilder per m²?",
             "De prijs hangt af van de ondergrond, de staat van het werk, het aantal lagen en de verfsoort. Daarom geven we geen standaardprijs, maar komen we vrijblijvend kijken en ontvangt u een offerte op maat."),
            ("Wanneer kan er buiten geschilderd worden?",
             "Buitenschilderwerk doen we bij voorkeur bij droog weer en temperaturen boven ongeveer 7 °C, meestal van het voorjaar tot in het najaar. Binnenschilderwerk kan het hele jaar door."),
            ("Moet ik zelf de ruimte leegmaken?",
             "Het helpt als kleine spullen en breekbare zaken weg zijn. Meubels die blijven staan, schuiven we samen en dekken we zorgvuldig af. Vloeren, kozijnen en hang- en sluitwerk worden afgeplakt of afgedekt."),
            ("Hangen jullie ook glasvlies of behang?",
             "Ja. Met onze inplakmachine brengen we glasvlies en behang snel en gelijkmatig aan. Glasvlies is daarna direct over te schilderen of te spuiten en geeft een sterke, strakke wand."),
        ],
    },
    "latexspuitwerk": {
        "out": "latexspuitwerk.html", "path": "/latexspuitwerk",
        "title": "Latex spuiten wanden & plafonds Utrecht | SchadePro",
        "description": "Latex laten spuiten in regio Utrecht? SchadePro spuit wanden en plafonds met professionele airless apparatuur: snel, egaal en zonder rolstrepen. Voor nieuwbouw, renovatie en bedrijfspanden.",
        "crumb": "Latexspuitwerk",
        "preload": "latexspuitwerk-airless-spuitmachines",
        "service": ("Latexspuitwerk", "Latex spuiten van wanden en plafonds met professionele airless spuitapparatuur, voor nieuwbouw, renovatie en bedrijfspanden."),
        "faq": [
            ("Wat is het verschil tussen latex spuiten en rollen?",
             "Bij spuiten wordt de latex met hoge druk als een fijne nevel aangebracht. Dat geeft een egale laag zonder rolstrepen of aanzetten en gaat bij grote oppervlakken veel sneller dan rollen."),
            ("Moet alles worden afgeplakt bij latex spuiten?",
             "Ja, goed afplakken en afdekken is de basis van strak spuitwerk. Wij plakken kozijnen, vloeren, stopcontacten en andere onderdelen zorgvuldig af en halen alles na afloop weer netjes weg."),
            ("Kan ik latex laten spuiten in een bewoond huis?",
             "Dat kan, maar het werkt het snelst in een lege of grotendeels lege ruimte. In een bewoonde woning bespreken we vooraf hoe we de ruimte indelen en wat er wordt afgedekt."),
            ("Hoeveel lagen latex zijn nodig?",
             "Meestal zijn twee lagen nodig voor een dekkend, egaal resultaat. Op nieuwe of zuigende ondergronden brengen we eerst een voorstrijkmiddel aan, zodat de latex goed hecht."),
            ("Hoe lang duurt latex spuiten?",
             "Spuiten gaat aanzienlijk sneller dan rollen. Een complete woning is vaak in enkele dagen klaar, afhankelijk van het oppervlak en het voorbereidende werk. In de offerte noemen we een duidelijke planning."),
        ],
    },
    "onderhoud": {
        "out": "onderhoud-schadeherstel.html", "path": "/onderhoud-schadeherstel",
        "title": "Schadeherstel & onderhoud woning en pand | SchadePro Utrecht",
        "description": "Schade aan wand, plafond of houtwerk? SchadePro herstelt waterschade, scheuren, gaten en houtrot en verzorgt periodiek onderhoud voor particulieren, VvE's en bedrijven in regio Utrecht.",
        "crumb": "Onderhoud & schadeherstel",
        "service": ("Onderhoud en schadeherstel", "Herstel van schade aan wanden, plafonds en houtwerk na lekkage, verbouwing of slijtage, en periodiek onderhoud voor woningen en bedrijfspanden."),
        "faq": [
            ("Wat moet ik doen na een lekkage?",
             "Zorg eerst dat de oorzaak van de lekkage is verholpen en laat de plek goed drogen. Daarna kunnen we de vlek isoleren, de ondergrond herstellen en het plafond of de wand weer egaal afwerken, zodat de vlek niet terugkomt."),
            ("Kunnen jullie een waterschade herstellen die via de verzekering loopt?",
             "Neem gerust contact op. We bekijken de schade en stellen een duidelijke omschrijving en offerte van het herstel op, die u kunt gebruiken in het contact met uw verzekeraar."),
            ("Herstellen jullie ook houtrot?",
             "Ja. Aangetaste delen worden verwijderd, aangevuld met een duurzaam reparatiesysteem en daarna strak geschilderd. Zo voorkomt u dat kozijnen of deuren verder worden aangetast."),
            ("Doen jullie ook onderhoud voor VvE's en bedrijven?",
             "Ja. We verzorgen periodiek onderhoud aan trappenhuizen, gangen, kantoren en bedrijfsruimtes en plannen flexibel, zodat bewoners en medewerkers zo weinig mogelijk last hebben."),
        ],
    },
    "werkgebied": {
        "out": "werkgebied.html", "path": "/werkgebied",
        "title": "Werkgebied: schilder in Utrecht, Houten, Zeist e.o. | SchadePro",
        "description": "SchadePro werkt in Utrecht, Houten, Nieuwegein, Zeist, Bilthoven, Bosch en Duin, Doorn, Odijk, Maarssen, IJsselstein, Woerden, Vianen en Amsterdam. Bekijk ons werkgebied.",
        "crumb": "Werkgebied",
    },
    "contact": {
        "out": "contact.html", "path": "/contact",
        "title": "Contact & vrijblijvende offerte | SchadePro regio Utrecht",
        "description": "Neem contact op met SchadePro voor vrijblijvend advies of een offerte voor schilderwerk, latexspuitwerk of schadeherstel. Bel 06 55 36 75 59 of mail schadepro@ziggo.nl.",
        "crumb": "Contact",
        "schema_type": "ContactPage",
    },
    "404": {
        "out": "404.html", "path": "/404",
        "title": "Pagina niet gevonden | SchadePro",
        "description": "Deze pagina bestaat niet (meer). Ga terug naar de homepage van SchadePro.",
        "robots": "noindex, follow",
        "sitemap": False,
        "crumb": "Pagina niet gevonden",
    },
}


def esc(s):
    return html.escape(s, quote=True)


def render_faq(items):
    out = ['<div class="faq">']
    for i, (q, a) in enumerate(items):
        out.append(
            f'<details class="faq__item"{" open" if i == 0 else ""}><summary><h3>{esc(q)}</h3><span class="faq__icon" aria-hidden="true"></span></summary>'
            f'<div class="faq__a"><p>{esc(a)}</p></div></details>')
    out.append("</div>")
    return "\n".join(out)


def render_breadcrumbs(page):
    if "crumb" not in page:
        return ""
    return (f'<nav class="crumbs" aria-label="Kruimelpad"><ol><li><a href="/">Home</a></li>'
            f'<li aria-current="page">{esc(page["crumb"])}</li></ol></nav>')


def render_nav(path):
    links = []
    for href, label in NAV:
        cur = ' aria-current="page"' if href == path else ""
        links.append(f'<a href="{href}"{cur}>{label}</a>')
    return "\n        ".join(links)


def build_schema(key, page):
    url = SITE + ("/" if page["path"] == "/" else page["path"])
    graph = [BUSINESS, WEBSITE]
    webpage = {"@type": page.get("schema_type", "WebPage"), "@id": url + "#pagina", "url": url,
               "name": page["title"], "description": page["description"], "inLanguage": "nl-NL",
               "isPartOf": {"@id": f"{SITE}/#website"}, "about": {"@id": f"{SITE}/#bedrijf"}}
    if "crumb" in page:
        crumbs = {"@type": "BreadcrumbList", "@id": url + "#kruimelpad", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": page["crumb"], "item": url}]}
        webpage["breadcrumb"] = {"@id": url + "#kruimelpad"}
        graph.append(crumbs)
    graph.append(webpage)
    if "service" in page:
        name, desc = page["service"]
        graph.append({"@type": "Service", "@id": url + "#dienst", "name": name, "serviceType": name,
                      "description": desc, "url": url, "provider": {"@id": f"{SITE}/#bedrijf"},
                      "areaServed": [{"@type": "City", "name": p} for p in PLACES]})
    if page.get("faq"):
        graph.append({"@type": "FAQPage", "@id": url + "#faq", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in page["faq"]]})
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))


def main():
    layout = (SRC / "layout.html").read_text(encoding="utf-8")
    partials = {p.stem: p.read_text(encoding="utf-8") for p in (SRC / "partials").glob("*.html")}
    sitemap = []
    for key, page in PAGES.items():
        content = (SRC / "pages" / f"{key}.html").read_text(encoding="utf-8")
        # partials invoegen: {{> naam}}
        for _ in range(2):
            content = re.sub(r"\{\{>\s*([\w-]+)\s*\}\}", lambda m: partials[m.group(1)], content)
        content = content.replace("{{faq}}", render_faq(page.get("faq", [])))
        content = content.replace("{{breadcrumbs}}", render_breadcrumbs(page))
        canonical = SITE + ("/" if page["path"] == "/" else page["path"])
        preload = ""
        if page.get("preload"):
            preload = f'<link rel="preload" as="image" href="/assets/img/{page["preload"]}.webp" type="image/webp" fetchpriority="high">'
        vals = {
            "title": esc(page["title"]), "description": esc(page["description"]),
            "robots": page.get("robots", "index, follow, max-image-preview:large"),
            "canonical": canonical, "site": SITE, "preload": preload, "version": VERSION,
            "schema": build_schema(key, page), "bodyclass": page.get("bodyclass", "page-sub"),
            "nav": render_nav(page["path"]), "content": content,
        }
        out = layout
        for k, v in vals.items():
            out = out.replace("{{" + k + "}}", v)
        leftover = re.findall(r"\{\{[^}]+\}\}", out)
        if leftover:
            raise SystemExit(f"{key}: onvervangen placeholders {leftover}")
        (ROOT / page["out"]).write_text(out, encoding="utf-8")
        if page.get("sitemap", True):
            sitemap.append((canonical, "1.0" if page["path"] == "/" else "0.8"))
        print("✓", page["out"])

    today = date.today().isoformat()
    xml = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, prio in sitemap:
        xml.append(f"  <url><loc>{loc}</loc><lastmod>{today}</lastmod><priority>{prio}</priority></url>")
    xml.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(xml) + "\n", encoding="utf-8")
    print("✓ sitemap.xml")


if __name__ == "__main__":
    main()
