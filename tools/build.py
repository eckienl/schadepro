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
import hashlib
VERSION = hashlib.sha1(b"".join((ROOT / f).read_bytes() for f in ("assets/css/style.css", "assets/js/main.js"))).hexdigest()[:10]
PHONE = "+31655367559"
MAILTO = "mailto:schadepro@ziggo.nl?subject=Aanvraag%20via%20schadepro.nl"

NAV = [
    ("/", "Home", []),
    ("/#diensten", "Diensten", [
        ("/onderhoud", "Onderhoud &amp; inspectie"),
        ("/schilderwerk", "Schilderwerk binnen &amp; buiten"),
        ("/latexspuitwerk", "Latexspuitwerk"),
        ("/kozijnen-spuiten", "Kozijnen spuiten"),
        ("/woning-verkoopklaar-maken", "Woning verkoopklaar maken"),
        ("/kitwerk", "Kitwerk sanitair &amp; keuken"),
        ("/kinderdagverblijven", "Kinderdagverblijven"),
    ]),
    ("/schadeherstel", "Schadeherstel", [
        ("/brandschade-herstel", "Brandschade herstel"),
        ("/nicotine-behandeling", "Nicotinebehandeling"),
        ("/schimmel-verwijderen", "Schimmelbehandeling"),
        ("/houtrot-herstel", "Houtrot &amp; houtschade"),
        ("/schadeherstel#lekkage-en-overige-schade", "Herstel &amp; reparatie"),
    ]),
    ("/over-ons", "Over ons", []),
    ("/werkgebied", "Werkgebied", []),
    ("/contact", "Contact", []),
]

PLACES = ["Utrecht", "Houten", "Nieuwegein", "Zeist", "Bilthoven", "Bosch en Duin",
          "Doorn", "Odijk", "Maarssen", "IJsselstein", "Woerden", "Vianen",
          "Amsterdam", "Amstelveen", "Diemen", "Weesp", "Haarlem", "Zaandam", "Hoofddorp",
          "Purmerend", "Hilversum", "Bussum", "Huizen"]

BUSINESS = {
    "@type": ["HousePainter", "LocalBusiness"],
    "@id": f"{SITE}/#bedrijf",
    "name": "SchadePro",
    "alternateName": "SchadePro.nl",
    "description": "VCA-gecertificeerd specialist in onderhoud, schadeherstel, schilderwerk, latexspuitwerk en kitwerk voor particulieren en bedrijven in regio Utrecht en Noord-Holland.",
    "slogan": "Uw herstelpartner van alle schades voor particulieren en bedrijven",
    "url": f"{SITE}/",
    "logo": f"{SITE}/apple-touch-icon.png",
    "image": [f"{SITE}/assets/img/og-schadepro.jpg", f"{SITE}/assets/img/schadepro-bedrijfsbus-zijkant.jpg", f"{SITE}/assets/img/schadepro-schilder-bus-spuitmachines.jpg"],
    "hasCredential": {"@type": "EducationalOccupationalCredential", "name": "VCA-certificaat", "credentialCategory": "certificate"},
    "telephone": PHONE,
    "email": "schadepro@ziggo.nl",
    "founder": {"@type": "Person", "name": "P.G.A. van Eck"},
    "address": {"@type": "PostalAddress", "addressLocality": "Utrecht", "addressRegion": "Utrecht", "addressCountry": "NL"},
    "geo": {"@type": "GeoCoordinates", "latitude": 52.0907, "longitude": 5.1214},
    "areaServed": [{"@type": "City", "name": p} for p in PLACES],
    "knowsAbout": ["Schilderwerk", "Binnenschilderwerk", "Buitenschilderwerk", "Latexspuitwerk", "Spuitwerk", "Schadeherstel", "Brandschade herstel", "Nicotinebehandeling", "Houtrotherstel", "Lekkageschade herstel", "Onderhoud", "Inspectie", "Glasvlies", "Kitwerk", "Kozijnen spuiten", "Schimmel verwijderen", "Schimmelwerende coating"],
    "hasOfferCatalog": {
        "@type": "OfferCatalog",
        "name": "Diensten SchadePro",
        "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Onderhoud", "url": f"{SITE}/onderhoud"}},
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Schadeherstel", "url": f"{SITE}/schadeherstel"}},
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Brandschade herstel", "url": f"{SITE}/brandschade-herstel"}},
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Nicotinebehandeling", "url": f"{SITE}/nicotine-behandeling"}},
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Houtrot herstel", "url": f"{SITE}/houtrot-herstel"}},
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Schimmel verwijderen", "url": f"{SITE}/schimmel-verwijderen"}},
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Kitwerk", "url": f"{SITE}/kitwerk"}},
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Kozijnen spuiten", "url": f"{SITE}/kozijnen-spuiten"}},
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Woning verkoopklaar maken", "url": f"{SITE}/woning-verkoopklaar-maken"}},
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Onderhoud en schilderwerk kinderdagverblijven", "url": f"{SITE}/kinderdagverblijven"}},
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Schilderwerk", "url": f"{SITE}/schilderwerk"}},
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Latexspuitwerk", "url": f"{SITE}/latexspuitwerk"}}
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
        "title": "Schilder & schadeherstel Utrecht & Noord-Holland | SchadePro",
        "description": "VCA-gecertificeerd vakbedrijf voor onderhoud, schadeherstel (brand, nicotine, schimmel, houtrot), schilderwerk, latexspuitwerk en kitwerk. Particulier en zakelijk in regio Utrecht en Noord-Holland.",
        "preload": "hero-bus-schadepro",
        "bodyclass": "page-home",
    },
    "onderhoud": {
        "out": "onderhoud.html", "path": "/onderhoud",
        "title": "Onderhoudswerkzaamheden & inspectie woning | SchadePro",
        "description": "Onderhoud aan woning of bedrijfspand in regio Utrecht en Noord-Holland. SchadePro inspecteert de ondergrond, signaleert beginnende schade en slijtage op tijd en herstelt deze vakkundig. Vraag vrijblijvend advies.",
        "crumb": "Onderhoud",
        "service": ("Onderhoudswerkzaamheden", "Inspectie, voorbereidende en instandhoudende onderhoudswerkzaamheden aan woningen en bedrijfspanden."),
        "hero": {"img": ("schilderwerk-voorbereiding-rolsteiger", 1400, 932),
                 "h1": 'Onderhouds<wbr>werkzaamheden <span class="red">woning &amp; pand</span>',
                 "tagline": "Tijdig signaleren en herstellen, zodat kleine gebreken geen grote kostenposten worden.",
                 "cta": "Inspectie aanvragen"},
        "faq": [
            ("Waarom is periodiek onderhoud belangrijk?",
             "Kleine gebreken zoals haarscheurtjes, loszittende verf of open kitnaden lijken onschuldig, maar laten vocht toe. Daardoor ontstaat sneller houtrot, vochtschade of verkleuring. Met tijdig onderhoud voorkomt u dure reparaties en blijft uw pand er verzorgd uitzien."),
            ("Wat houdt scanwerk en inspectie in?",
             "We beoordelen de ondergrond en de situatie ter plaatse. We kijken naar zichtbare schade, maar ook naar onderliggende problemen zoals vocht, scheurvorming, verkleuring en verouderde afwerkingen. Op basis daarvan adviseren we de juiste aanpak en materialen."),
            ("Hoe vaak moet buitenschilderwerk worden onderhouden?",
             "Dat hangt af van de ligging, de verfsoort en de staat van het houtwerk. Vaak is een onderhoudsbeurt na zo'n 5 tot 7 jaar verstandig. Bij een inspectie geven we een eerlijk advies over wat nu nodig is en wat kan wachten."),
            ("Doen jullie ook onderhoud voor VvE's en bedrijven?",
             "Ja. We verzorgen onderhoud aan trappenhuizen, galerijen, kantoren en bedrijfsruimtes en maken huurwoningen tussen twee huurders weer gebruiksklaar. We plannen flexibel, zodat bewoners en medewerkers zo weinig mogelijk last hebben."),
        ],
    },
    "schadeherstel": {
        "out": "schadeherstel.html", "path": "/schadeherstel",
        "title": "Schadeherstel woning & bedrijfspand Utrecht | SchadePro",
        "description": "Schadeherstel in regio Utrecht en Noord-Holland: brandschade, rook- en roetschade, nicotine, houtrot, lekkage, vochtplekken en scheuren. SchadePro pakt de oorzaak aan en werkt alles strak af. Vraag vrijblijvend advies.",
        "crumb": "Schadeherstel",
        "service": ("Schadeherstel", "Herstel van brandschade, nicotine, houtrot, lekkage, vochtplekken, scheurvorming en slijtage aan woningen en bedrijfspanden."),
        "hero": {"img": ("trappenhuis-wanden-strak-afgewerkt", 509, 488),
                 "h1": 'Schadeherstel voor woning <span class="red">&amp; bedrijfspand</span>',
                 "tagline": "Uw herstelpartner van alle schades: van brand en nicotine tot houtrot en lekkage.",
                 "cta": "Schade laten bekijken"},
        "faq": [
            ("Welke soorten schade herstellen jullie?",
             "We herstellen onder meer brandschade en rook- en roetschade, nicotineaanslag, houtrot en houtschade, lekkage- en vochtschade, scheurvorming in muren en plafonds, beschadigde afwerkingen en algemene slijtage."),
            ("Wat moet ik doen na een lekkage?",
             "Zorg eerst dat de oorzaak van de lekkage is verholpen en laat de plek goed drogen. Daarna isoleren we de vlek, herstellen we de ondergrond en werken we het plafond of de wand weer egaal af, zodat de vlek niet terugkomt."),
            ("Kunnen jullie schade herstellen die via de verzekering loopt?",
             "Neem gerust contact op. We bekijken de schade en stellen een duidelijke omschrijving en offerte van het herstel op, die u kunt gebruiken in het contact met uw verzekeraar."),
            ("Kan ik schade niet gewoon overschilderen?",
             "Bij de meeste schade niet. Vocht, roet, nicotine en vlekken slaan door een gewone verflaag heen en komen na korte tijd terug. Daarom reinigen en isoleren we de ondergrond eerst, en pas daarna volgt de afwerking."),
        ],
    },
    "brandschade": {
        "out": "brandschade-herstel.html", "path": "/brandschade-herstel",
        "title": "Brandschade herstellen, rook & roet | SchadePro Utrecht",
        "description": "Brandschade laten herstellen in regio Utrecht? SchadePro reinigt rook- en roetaanslag, isoleert verkleuring en geur en herstelt muren, plafonds en houtwerk. Daarna strak afgewerkt met verf of spuitwerk.",
        "crumb": "Brandschade herstel", "parent": ("/schadeherstel", "Schadeherstel"),
        "service": ("Brandschade herstel", "Reinigen, isoleren en herstellen van rook-, roet- en brandschade aan muren, plafonds en houtwerk, met strakke afwerking in verf of spuitwerk."),
        "hero": {"img": ("overloop-wanden-latex-afgewerkt", 472, 488),
                 "h1": 'Brandschade <span class="red">herstellen</span>',
                 "tagline": "Rook, roet en geur zorgvuldig aangepakt. Uw ruimte weer fris, schoon en bruikbaar.",
                 "cta": "Brandschade laten bekijken"},
        "faq": [
            ("Kan ik na een brand de muren gewoon overschilderen?",
             "Nee. Roet en rook bevatten vetten en stoffen die door een gewone verflaag heen trekken. Dan ontstaan na korte tijd opnieuw gele of grijze vlekken en blijft de brandlucht hangen. De ondergrond moet eerst gereinigd en geïsoleerd worden."),
            ("Verdwijnt de brandlucht na het herstel?",
             "Door aangetaste delen te reinigen en de ondergrond te isoleren, sluiten we geur en verkleuring in. In de meeste gevallen is de ruimte daarna weer fris. Bij zware brandschade kan aanvullende specialistische reiniging nodig zijn; dat bespreken we eerlijk vooraf."),
            ("Wanneer kunnen jullie beginnen na een brand?",
             "Zodra de ruimte veilig is vrijgegeven en eventueel bluswater is opgedroogd. Neem gerust zo snel mogelijk contact op, dan bekijken we samen de schade en de planning."),
            ("Loopt brandschade via de verzekering?",
             "Vaak wel. We stellen een duidelijke omschrijving en offerte van het herstelwerk op, die u kunt gebruiken in het contact met uw verzekeraar."),
        ],
    },
    "nicotine": {
        "out": "nicotine-behandeling.html", "path": "/nicotine-behandeling",
        "title": "Nicotine verwijderen van muren & plafonds | SchadePro",
        "description": "Nicotineaanslag en rooklucht in woning of huurwoning? SchadePro behandelt en isoleert de ondergrond met speciale producten, zodat vlekken en geur niet terugkomen. Daarna strak geschilderd of gespoten.",
        "crumb": "Nicotinebehandeling", "parent": ("/schadeherstel", "Schadeherstel"),
        "service": ("Nicotinebehandeling", "Reinigen en isoleren van nicotineaanslag en rookgeur op muren, plafonds en houtwerk, met afwerking in verf of latexspuitwerk."),
        "hero": {"img": ("nicotine-na-achterkamer", 1000, 1333),
                 "h1": 'Nicotine<wbr>behandeling <span class="red">muren &amp; plafonds</span>',
                 "tagline": "Reinigen, sausen en spuiten: gele aanslag en rooklucht blijvend weg. Wij spuiten het weer als nieuw.",
                 "cta": "Nicotinebehandeling aanvragen"},
        "faq": [
            ("Waarom komt nicotine door nieuwe verf heen?",
             "Nicotine en teer trekken diep in de ondergrond en zijn oplosbaar in water. Gewone muurverf of latex is waterbasis, waardoor de aanslag erdoorheen trekt en na korte tijd weer gele vlekken geeft. Een nicotine-isolerende grondlaag voorkomt dat."),
            ("Verdwijnt de rooklucht ook?",
             "Ja, in de meeste gevallen wel. Door de ondergrond te reinigen en te isoleren, sluiten we de geur in. Ook plafonds, kozijnen en deuren nemen we mee, want daar zit vaak veel aanslag."),
            ("Is een nicotinebehandeling geschikt voor huurwoningen?",
             "Zeker. Verhuurders en woningcorporaties laten een woning vaak behandelen tussen twee huurders in. We werken snel, zodat de woning weer kort daarna verhuurd kan worden."),
            ("Welke verf gebruiken jullie tegen nicotine?",
             "We sausen met een dekkende, isolerende muurverf voor binnen, zoals van Veveo. Die sperrende verf voorkomt dat nicotine en vlekken doorbloeden. Daarna spuiten of rollen we de eindlaag."),
            ("Hoe lang duurt een nicotinebehandeling?",
             "Dat hangt af van de grootte van de woning en de ernst van de aanslag. Door te spuiten in plaats van te rollen is een complete woning vaak in enkele dagen klaar. In de offerte noemen we een duidelijke planning."),
        ],
    },
    "houtrot": {
        "out": "houtrot-herstel.html", "path": "/houtrot-herstel",
        "title": "Houtrot herstellen kozijnen & deuren Utrecht | SchadePro",
        "description": "Houtrot in kozijnen, deuren of boeidelen? SchadePro verwijdert aangetast hout, bouwt het op met duurzame reparatiematerialen en schildert het strak af. Vervangen is vaak niet nodig.",
        "crumb": "Houtrot & houtschade", "parent": ("/schadeherstel", "Schadeherstel"),
        "service": ("Houtrot herstel", "Herstel van houtrot en houtschade aan kozijnen, ramen, deuren en boeidelen met duurzame reparatiematerialen en schilderwerk."),
        "hero": {"img": ("schadepro-schilder-bus-spuitmachines", 1672, 941),
                 "h1": 'Houtrot en houtschade <span class="red">herstellen</span>',
                 "tagline": "Vervangen is vaak niet nodig. Wij herstellen aangetast hout duurzaam en werken het strak af.",
                 "cta": "Houtrot laten bekijken"},
        "faq": [
            ("Hoe herken ik houtrot?",
             "Let op afbladderende of blazende verf, donkere verkleuring en zacht hout, vooral onderin kozijnen, bij dorpels en in de hoeken van ramen en deuren. Kunt u met een schroevendraaier gemakkelijk in het hout prikken, dan is er vaak sprake van houtrot."),
            ("Moet een kozijn met houtrot vervangen worden?",
             "Meestal niet. Zolang de constructie nog goed is, verwijderen we alleen het aangetaste hout en bouwen we het op met een duurzaam reparatiesysteem. Dat is sneller en vaak een stuk voordeliger dan vervangen."),
            ("Hoe voorkom ik houtrot?",
             "Door houtwerk goed in de verf te houden, kitnaden tijdig te vernieuwen en beschadigingen snel te herstellen. Periodiek onderhoud en een inspectie helpen om beginnende houtrot op tijd te signaleren."),
            ("Wanneer kan houtrot het beste hersteld worden?",
             "Het liefst zo snel mogelijk, voordat het zich verder verspreidt. Houtrotherstel buiten doen we bij voorkeur bij droog weer, zodat het hout droog genoeg is om goed te kunnen repareren en schilderen."),
        ],
    },
    "schilderwerk": {
        "out": "schilderwerk.html", "path": "/schilderwerk",
        "title": "Schilder regio Utrecht – binnen & buiten | SchadePro",
        "description": "Schilder nodig in regio Utrecht of Noord-Holland? SchadePro verzorgt binnen- en buitenschilderwerk van muren, plafonds, kozijnen, deuren en gevelonderdelen, met veel aandacht voor voorbereiding en afwerking.",
        "crumb": "Schilderwerk",
        "service": ("Schilderwerk", "Binnen- en buitenschilderwerk van muren, plafonds, kozijnen, deuren, trappen en gevelonderdelen."),
        "hero": {"img": ("schilderwerk-voorbereiding-rolsteiger", 1400, 932),
                 "h1": 'Schilderwerk <span class="red">binnen &amp; buiten</span>',
                 "tagline": "Binnen en buiten, met veel aandacht voor voorbereiding, detail en afwerking.",
                 "cta": "Offerte aanvragen"},
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
        "description": "Latex spuitwerk in regio Utrecht en Noord-Holland: strak en egaal zonder strepen of structuur. SchadePro spuit muren en plafonds met professionele apparatuur, voor nieuwbouw, renovatie en bestaande woningen.",
        "crumb": "Latexspuitwerk",
        "preload": "latexspuitwerk-airless-spuitmachines",
        "service": ("Latexspuitwerk", "Latex spuiten en spuitwerk van muren en plafonds met professionele spuitapparatuur, voor nieuwbouw, renovatie, bestaande woningen en bedrijfspanden."),
        "hero": {"img": ("latexspuitwerk-airless-spuitmachines", 936, 1024),
                 "h1": 'Wanden &amp; plafonds <span class="red">laten spuiten</span>',
                 "tagline": "Strak en egaal, zonder strepen of structuur. Met professionele spuittechniek.",
                 "cta": "Offerte voor spuitwerk"},
        "faq": [
            ("Wat is het verschil tussen latex spuiten en rollen?",
             "Bij spuiten wordt de verf met hoge druk als een fijne nevel aangebracht. Dat geeft een egale laag zonder rolstrepen of aanzetten en gaat bij grote oppervlakken veel sneller dan rollen."),
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
    "schimmel": {
        "out": "schimmel-verwijderen.html", "path": "/schimmel-verwijderen",
        "title": "Schimmel verwijderen plafond & muren | SchadePro",
        "description": "Schimmel op plafond of muren? SchadePro verwijdert schimmel en sporen, reinigt en desinfecteert met HEPA-gefilterde apparatuur en behandelt met een schimmelwerende coating tegen terugkeer.",
        "crumb": "Schimmel verwijderen", "parent": ("/schadeherstel", "Schadeherstel"),
        "service": ("Schimmel verwijderen", "Verwijderen van schimmel en sporen, reinigen en desinfecteren en schimmelwerend behandelen van plafonds en muren in badkamers, keukens en woonruimtes."),
        "hero": {"img": ("overloop-wanden-latex-afgewerkt", 472, 488),
                 "h1": 'Schimmel <span class="red">verwijderen</span>',
                 "tagline": "Verwijderen, reinigen en behandelen. Zo blijft schimmel weg en wordt uw ruimte weer gezond.",
                 "cta": "Schimmel laten bekijken"},
        "faq": [
            ("Is overschilderen genoeg om schimmel weg te krijgen?",
             "Nee. Schimmel groeit door een gewone verflaag heen. De schimmel en sporen moeten eerst worden verwijderd en de ondergrond moet worden gereinigd en gedesinfecteerd. Daarna volgt een schimmelwerende behandeling."),
            ("Hoe voorkomen jullie dat schimmel terugkomt?",
             "Na het reinigen brengen we een schimmelwerende coating aan, zoals Inducoat Fungi, die schimmelgroei tegengaat. Daarnaast adviseren we over de oorzaak, bijvoorbeeld ventilatie of vocht, want zonder die aan te pakken kan schimmel altijd terugkomen."),
            ("Waar komt schimmel op het plafond vandaan?",
             "Meestal door vocht in combinatie met te weinig ventilatie, zoals in badkamers, keukens en slaapkamers. Ook koudebruggen en lekkages kunnen schimmel veroorzaken. Bij de inspectie kijken we naar de oorzaak."),
            ("Is schimmel verwijderen stofvrij?",
             "We werken met een professionele reinigingsmachine met HEPA-filtratie, zodat sporen en stof zoveel mogelijk worden opgevangen en de ruimte schoon blijft."),
        ],
    },
    "kitwerk": {
        "out": "kitwerk.html", "path": "/kitwerk",
        "title": "Kitwerk badkamer, toilet & keuken | SchadePro",
        "description": "Professioneel kitwerk voor badkamer, toilet en keuken: waterdicht, schimmelwerend en strak afgewerkt. SchadePro vernieuwt kitvoegen met hoogwaardige sanitairkit in regio Utrecht en Noord-Holland.",
        "crumb": "Kitwerk",
        "service": ("Kitwerk", "Vernieuwen en aanbrengen van kitvoegen in badkamer, toilet en keuken met waterdichte, schimmelwerende sanitairkit."),
        "hero": {"img": ("kitwerk-sanitair-kitspuit", 445, 470),
                 "h1": 'Professioneel <span class="red">kitwerk</span>',
                 "tagline": "Voor sanitair, toilet en keuken. Strak afgewerkt, waterdicht en duurzaam.",
                 "cta": "Kitwerk aanvragen"},
        "faq": [
            ("Wanneer moet kitwerk vervangen worden?",
             "Als de kit zwart verkleurt door schimmel, loslaat, scheurt of hard wordt. Dan is de voeg niet meer waterdicht en kan water achter tegels of het aanrecht komen, met lekkage of vochtschade als gevolg."),
            ("Kan nieuwe kit over oude kit heen?",
             "Nee. Nieuwe kit hecht niet goed op oude kit. We verwijderen de oude kit volledig, reinigen en ontvetten de voeg en brengen pas dan nieuwe kit aan."),
            ("Welke kit gebruiken jullie?",
             "We werken met hoogwaardige sanitairkit, zoals Ottoseal S100, S110 en S125. Welke het beste past hangt af van de plek: binnen of buiten, nat of droog en de ondergrond."),
            ("Hoe snel kan ik de douche weer gebruiken?",
             "Sanitairkit heeft tijd nodig om uit te harden. Meestal kunt u de douche of het bad na ongeveer 24 uur weer gebruiken. We geven bij oplevering het precieze advies."),
        ],
    },
    "kinderdagverblijven": {
        "out": "kinderdagverblijven.html", "path": "/kinderdagverblijven",
        "title": "Onderhoud & schilderwerk kinderdagverblijven | SchadePro",
        "description": "Onderhoud en schilderwerk aan kinderdagverblijven: veilig, fris en duurzaam, met minimale hinder. VCA-gecertificeerd, met een vast aanspreekpunt. Regio Utrecht en Noord-Holland.",
        "crumb": "Kinderdagverblijven",
        "service": ("Onderhoud en schilderwerk kinderdagverblijven", "Onderhoud en binnen- en buitenschilderwerk aan kinderdagverblijven, met veilige producten en minimale hinder voor kinderen en personeel."),
        "hero": {"img": ("schilderwerk-hoge-wanden-rolsteiger", 537, 488),
                 "h1": 'Onderhoud en schilderwerk aan <span class="red">kinderdagverblijven</span>',
                 "tagline": "Een veilige, frisse en duurzame omgeving waar kinderen elke dag met plezier kunnen spelen en leren.",
                 "cta": "Offerte aanvragen"},
        "faq": [
            ("Kunnen jullie werken terwijl het kinderdagverblijf open is?",
             "Dat kan in overleg. Vaak plannen we de werkzaamheden buiten openingstijden, in vakanties of per ruimte, zodat de opvang gewoon door kan gaan en kinderen geen hinder hebben."),
            ("Welke verf gebruiken jullie bij kinderdagverblijven?",
             "We gebruiken waar mogelijk watergedragen, geurarme producten van bekende merken, en slijtvaste en afwasbare verf op plekken die veel te verduren krijgen."),
            ("Zijn jullie VCA-gecertificeerd?",
             "Ja. SchadePro is VCA-gecertificeerd: veiligheid, gezondheid en milieu staan bij ons voorop. Dat is extra belangrijk in een omgeving met jonge kinderen."),
        ],
    },
    "kozijnen": {
        "out": "kozijnen-spuiten.html", "path": "/kozijnen-spuiten",
        "title": "Kozijnen spuiten binnen & buiten | SchadePro",
        "description": "Kozijnen laten spuiten? SchadePro spuit houten en kunststof kozijnen, ramen en deuren strak en egaal, zonder kwaststrepen. Netjes afgeplakt, duurzaam afgewerkt. Regio Utrecht en Noord-Holland.",
        "crumb": "Kozijnen spuiten",
        "service": ("Kozijnen spuiten", "Spuiten van houten en kunststof kozijnen, ramen en deuren, binnen en buiten, met een strakke en duurzame afwerking."),
        "hero": {"img": ("dienst-kozijnen-spuiten", 480, 211),
                 "h1": 'Kozijnen <span class="red">spuiten</span>',
                 "tagline": "Houten en kunststof kozijnen, ramen en deuren: strak, egaal en zonder kwaststrepen.",
                 "cta": "Offerte kozijnen spuiten"},
        "faq": [
            ("Kunnen kunststof kozijnen gespoten worden?",
             "Ja. Met de juiste voorbehandeling (reinigen, licht opschuren en een speciale hechtprimer) kunnen kunststof kozijnen prima gespoten worden. Zo geeft u ze een nieuwe kleur zonder ze te vervangen."),
            ("Wat is het verschil tussen kozijnen spuiten en schilderen?",
             "Spuiten geeft een gladdere, egalere laag zonder kwaststrepen, vergelijkbaar met een fabrieksafwerking. Bij veel kozijnen gaat het bovendien sneller. Voor kleine reparaties of bijwerkwerk kiezen we soms voor de kwast."),
            ("Kunnen de ramen open tijdens het spuiten?",
             "Draaiende delen worden vooraf goed afgeplakt en na het drogen weer vrijgemaakt. Meestal zijn ramen en deuren dezelfde dag weer te gebruiken; we geven bij oplevering het precieze advies."),
            ("Wordt houtrot eerst hersteld?",
             "Ja. Bij een inspectie controleren we het houtwerk. Waar nodig herstellen we eerst de houtrot, zodat de nieuwe laag op een gezonde ondergrond komt en lang meegaat."),
        ],
    },
    "overons": {
        "out": "over-ons.html", "path": "/over-ons",
        "title": "Over SchadePro | VCA-gecertificeerd herstelpartner",
        "description": "Maak kennis met SchadePro: uw VCA-gecertificeerde herstelpartner voor particulieren, woningbouwverenigingen en bedrijven. Vakwerk, heldere afspraken en duurzame materialen.",
        "crumb": "Over ons",
        "schema_type": "AboutPage",
        "hero": {"img": ("hero-bus-schadepro", 1100, 526),
                 "h1": 'Over <span class="red">SchadePro</span>',
                 "tagline": "Uw herstelpartner van alle schades voor particulieren, woningbouwverenigingen en bedrijven.",
                 "cta": "Neem contact op"},
    },
    "verkoopklaar": {
        "out": "woning-verkoopklaar-maken.html", "path": "/woning-verkoopklaar-maken",
        "title": "Woning verkoopklaar maken | Schilder- & spuitwerk | SchadePro",
        "description": "Woning verkoopklaar maken? SchadePro herstelt kleine schades, schildert en spuit wanden en plafonds strak wit. Een frisse, representatieve uitstraling voor betere foto's en bezichtigingen.",
        "crumb": "Woning verkoopklaar maken",
        "service": ("Woning verkoopklaar maken", "Inspectie, herstel van kleine schades, schilderwerk en latexspuitwerk om een woning fris en representatief te maken voor de verkoop."),
        "hero": {"img": ("woning-verkoopklaar", 639, 530),
                 "h1": 'Uw woning <span class="red">verkoopklaar</span>',
                 "tagline": "Een frisse, representatieve uitstraling voor betere foto's, meer bezichtigingen en een sterkere verkoop.",
                 "cta": "Vraag een offerte aan"},
        "faq": [
            ("Loont het om een woning op te knappen voor de verkoop?",
             "Vaak wel. Kopers beslissen voor een groot deel op de eerste indruk, online en bij de bezichtiging. Strakke witte wanden en plafonds en herstelde beschadigingen laten een woning lichter, groter en beter onderhouden ogen."),
            ("Hoe snel kunnen jullie een woning verkoopklaar maken?",
             "Door wanden en plafonds te spuiten in plaats van te rollen gaat het snel. Een gemiddelde woning is vaak binnen enkele dagen klaar, afhankelijk van de omvang en het herstelwerk. We stemmen de planning af op de fotograaf of de eerste bezichtiging."),
            ("Werken jullie ook samen met makelaars?",
             "Ja. Makelaars, verkopers en erven kunnen ons rechtstreeks inschakelen. We maken een duidelijke offerte en plannen het werk zodat de woning op tijd klaar is voor de foto's."),
            ("Kunnen jullie ook nicotine- of vochtvlekken weghalen?",
             "Zeker. Juist bij verkoop zijn gele plafonds of vochtplekken een afknapper. Met een nicotinebehandeling of vlekisolatie en een nieuwe spuitlaag is de woning weer fris en wit."),
        ],
    },
    "werkgebied": {
        "out": "werkgebied.html", "path": "/werkgebied",
        "title": "Werkgebied: regio Utrecht en Noord-Holland | SchadePro",
        "description": "SchadePro werkt in regio Utrecht (Utrecht, Houten, Nieuwegein, Zeist, Woerden e.o.) en Noord-Holland (Amsterdam, Amstelveen, Haarlem, Zaandam, Hoofddorp, het Gooi e.o.).",
        "crumb": "Werkgebied",
        "hero": {"img": ("schadepro-schilder-bus-spuitmachines", 1672, 941),
                 "h1": 'Ons <span class="red">werkgebied</span>',
                 "tagline": "Onderhoud, schadeherstel, schilderwerk en latexspuitwerk in regio Utrecht en Noord-Holland."},
    },
    "contact": {
        "out": "contact.html", "path": "/contact",
        "title": "Contact & vrijblijvende offerte | SchadePro regio Utrecht",
        "description": "Neem contact op met SchadePro voor vrijblijvend advies of een offerte voor onderhoud, schadeherstel, schilderwerk, latexspuitwerk of kitwerk. Bel of mail schadepro@ziggo.nl.",
        "crumb": "Contact",
        "schema_type": "ContactPage",
        "hero": {"img": ("schadepro-schilder-bus-spuitmachines", 1672, 941), "short": True,
                 "h1": 'Contact &amp; <span class="red">offerte</span>',
                 "tagline": "Bel of mail ons voor vrijblijvend advies. We reageren snel."},
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
    mid = ""
    if page.get("parent"):
        ph, pl = page["parent"]
        mid = f'<li><a href="{ph}">{esc(pl)}</a></li>'
    return (f'<nav class="crumbs" aria-label="Kruimelpad"><ol><li><a href="/">Home</a></li>{mid}'
            f'<li aria-current="page">{esc(page["crumb"])}</li></ol></nav>')


def render_nav(path):
    links = []
    for href, label, children in NAV:
        active = href == path or any(c[0].split("#")[0] == path for c in children)
        cur = ' aria-current="page"' if active else ""
        if not children:
            links.append(f'<a href="{href}"{cur}>{label}</a>')
            continue
        sub = "".join(f'<a href="{c}">{l}</a>' for c, l in children)
        links.append(f'<div class="nav__group"><a href="{href}"{cur}>{label}</a>'
                     f'<button class="nav__toggle" aria-label="Submenu {label}" aria-expanded="false"></button>'
                     f'<div class="nav__sub">{sub}</div></div>')
    return "\n        ".join(links)


def render_hero(page):
    h = page.get("hero")
    if not h:
        return ""
    img = ""
    if h.get("img"):
        n, w, hh = h["img"]
        img = (f'<picture class="page-hero__bg"><source srcset="/assets/img/{n}.webp" type="image/webp">'
               f'<img src="/assets/img/{n}.jpg" alt="" width="{w}" height="{hh}" fetchpriority="high"></picture>')
    btns = ""
    if h.get("cta"):
        btns = (f'<div class="hero__actions"><a href="{MAILTO}" class="btn btn--red btn--lg"><svg><use href="#i-mail"/></svg> {h["cta"]}</a>'
                f'<a href="tel:+31655367559" class="btn btn--ghost btn--lg"><svg><use href="#i-phone"/></svg> Bel direct</a></div>')
    cls = "page-hero page-hero--short" if h.get("short") else "page-hero"
    return f'''    <section class="{cls}">
      {img}
      <div class="corner corner--br" aria-hidden="true"></div>
      <div class="container page-hero__content">
        {render_breadcrumbs(page)}
        <h1>{h["h1"]}</h1>
        <p class="tagline">{h["tagline"]}</p>
        {btns}
      </div>
    </section>'''


def build_schema(key, page):
    url = SITE + ("/" if page["path"] == "/" else page["path"])
    graph = [BUSINESS, WEBSITE]
    webpage = {"@type": page.get("schema_type", "WebPage"), "@id": url + "#pagina", "url": url,
               "name": page["title"], "description": page["description"], "inLanguage": "nl-NL",
               "isPartOf": {"@id": f"{SITE}/#website"}, "about": {"@id": f"{SITE}/#bedrijf"}}
    if "crumb" in page:
        items = [("Home", f"{SITE}/")]
        if page.get("parent"):
            items.append((page["parent"][1], SITE + page["parent"][0]))
        items.append((page["crumb"], url))
        crumbs = {"@type": "BreadcrumbList", "@id": url + "#kruimelpad", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(items)]}
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
        content = content.replace("{{hero}}", render_hero(page))
        content = content.replace("{{mailto}}", MAILTO)
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
