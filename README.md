# SchadePro.nl

Website van **SchadePro** – schilder, latexspuiter en specialist in onderhoud & schadeherstel voor particulieren en bedrijven in regio Utrecht.

## Pagina's
| URL | Bestand | Bron |
|---|---|---|
| `/` | index.html | src/pages/home.html |
| `/schilderwerk` | schilderwerk.html | src/pages/schilderwerk.html |
| `/latexspuitwerk` | latexspuitwerk.html | src/pages/latexspuitwerk.html |
| `/onderhoud-schadeherstel` | onderhoud-schadeherstel.html | src/pages/onderhoud.html |
| `/werkgebied` | werkgebied.html | src/pages/werkgebied.html |
| `/contact` | contact.html | src/pages/contact.html |

## Aanpassen
1. Pas teksten aan in `src/pages/` (inhoud) of `src/partials/` (blokken die op meerdere pagina's staan, zoals contact, galerij, kaart).
2. Titels, meta-omschrijvingen en veelgestelde vragen staan in `tools/build.py` (`PAGES`).
3. Draai `python3 tools/build.py` – dit maakt de `.html`-bestanden en `sitemap.xml` opnieuw.
4. Commit en push; Vercel zet het automatisch live.

> Bewerk de `.html`-bestanden in de hoofdmap niet direct: ze worden overschreven door het build-script.

## SEO
- Unieke title, meta description, canonical en Open Graph per pagina
- Gestructureerde data (JSON-LD): HousePainter/LocalBusiness, Service, FAQPage, BreadcrumbList
- `sitemap.xml` en `robots.txt`
- Foto's met beschrijvende bestandsnamen en alt-teksten, WebP met JPG-fallback, lazy loading
- Interne links tussen diensten, werkgebied en contact

## Techniek
Statische site, geen build-stap op Vercel nodig. `vercel.json` regelt nette URL's (zonder `.html`), caching en headers.
