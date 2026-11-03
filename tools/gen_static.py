"""Home, category hubs, directory pages, region hubs and legal/standard pages."""
from gen_common import *
from gen_routes import KIND_LABEL, label, air_sentence

CATS = [
    ("flights", "Flights", "flights.html", "Compare flights between UK and US cities, with airport notes and flight-time estimates for every route."),
    ("trains", "Trains", "trains.html", "City-to-city rail guides for Great Britain and the main US corridors, with journey-time ranges."),
    ("buses", "Buses & Coaches", "buses.html", "Intercity coach and bus guides, including stop tips, luggage notes and typical journey times."),
    ("tours", "Tours", "tours.html", "Tours, day trips and activities for UK and US cities, with nearby places for excursions."),
    ("packages", "Holiday Packages", "holiday-packages.html", "Package-holiday guides covering what is included, departures and entry checks."),
    ("taxi", "Taxi & Transfers", "taxi.html", "Airport transfer and taxi guides, including pre-booking tips and intercity drive estimates."),
]
CITY_KIND = {"tours": "tours", "packages": "packages", "taxi": "taxi"}

def route_by_names(kind, an, ac, bn, bc):
    a_, b_ = find(an, ac), find(bn, bc)
    return (rfile(kind, a_, b_), label(kind, a_, b_)) if (a_["slug"], b_["slug"]) in RS[kind] else None

POP = {
    "flights": [("London","UK","New York","USA"),("New York","USA","London","UK"),("London","UK","Los Angeles","USA"),("Manchester","UK","New York","USA"),
                ("Edinburgh","UK","New York","USA"),("London","UK","Edinburgh","UK"),("London","UK","Glasgow","UK"),("Manchester","UK","London","UK"),
                ("New York","USA","Los Angeles","USA"),("Chicago","USA","Miami","USA"),("Los Angeles","USA","Las Vegas","USA"),("Boston","USA","London","UK")],
    "trains": [("London","UK","Manchester","UK"),("London","UK","Edinburgh","UK"),("London","UK","Birmingham","UK"),("Leeds","UK","London","UK"),
               ("New York","USA","Washington, DC","USA"),("Boston","USA","New York","USA"),("Philadelphia","USA","New York","USA"),("Chicago","USA","Milwaukee","USA"),
               ("Los Angeles","USA","San Diego","USA"),("Seattle","USA","Portland, OR","USA"),("Glasgow","UK","Edinburgh","UK"),("Bristol","UK","London","UK")],
    "buses": [("London","UK","Birmingham","UK"),("London","UK","Manchester","UK"),("London","UK","Bristol","UK"),("Leeds","UK","Manchester","UK"),
              ("New York","USA","Boston","USA"),("New York","USA","Washington, DC","USA"),("Los Angeles","USA","San Francisco","USA"),("Chicago","USA","Detroit","USA"),
              ("Houston","USA","Dallas","USA"),("Atlanta","USA","Charlotte","USA"),("Glasgow","UK","Edinburgh","UK"),("Liverpool","UK","Manchester","UK")],
}
def popular(kind):
    out = []
    for an, ac, bn, bc in POP[kind]:
        r = route_by_names(kind, an, ac, bn, bc)
        if r: out.append(r)
    return out

def cat_ds_none(): return {}

def hub_page(kind):
    label_, fname, blurb = next((c[1], c[2], c[3]) for c in CATS if c[0] == kind)
    titles = {"flights": "Flights UK & USA: Routes, Airports & Guides", "trains": "Train Travel UK & USA: City-to-City Guides",
              "buses": "Bus & Coach Travel UK & USA: Route Guides", "tours": "Tours & Day Trips in UK & USA Cities",
              "packages": "Holiday Packages to UK & USA Cities", "taxi": "Taxi & Airport Transfers in UK & USA Cities"}
    descs = {"flights": "Browse flight guides between UK and US cities, with airports, flight-time estimates and booking tips, then check live options with our partner.",
             "trains": "Browse train guides for Great Britain and the main US corridors, with journey-time ranges and ticket tips, then check live fares with our partner.",
             "buses": "Browse intercity bus and coach guides for the UK and USA, with stop tips, luggage notes and journey-time estimates.",
             "tours": "Browse tours, day trips and activity guides for UK and US cities and compare options with our booking partner.",
             "packages": "Browse holiday-package guides for UK and US cities, covering inclusions, departures and entry checks before you book.",
             "taxi": "Browse taxi and airport-transfer guides for UK and US cities, with pre-booking tips and drive-time estimates."}
    kws = {"flights": ["flights UK USA", "flights between UK and USA", "cheap flights UK", "domestic flights USA", "transatlantic flights", "flight booking guide", "UK to USA flights", "USA to UK flights"],
           "trains": ["train tickets UK", "train travel USA", "UK rail guide", "Amtrak style routes", "city to city trains", "train journey times", "book train tickets online", "rail travel UK USA"],
           "buses": ["bus tickets UK", "coach tickets UK", "intercity bus USA", "cheap coach travel", "bus journey times", "city to city buses", "book bus tickets online", "coach travel guide"],
           "tours": ["tours UK", "tours USA", "city tours", "day trips UK", "day trips USA", "sightseeing tours", "book tours online", "guided tours"],
           "packages": ["holiday packages UK", "holiday packages USA", "flight and hotel packages", "city break packages", "vacation packages USA", "package holidays", "book holiday package", "UK to USA holidays"],
           "taxi": ["taxi UK", "taxi USA", "airport transfers UK", "airport transfers USA", "private transfers", "book taxi online", "airport taxi", "pre-book taxi"]}[kind]
    h1 = {"flights": "Flights Across the UK and USA", "trains": "Train Travel Across the UK and USA", "buses": "Buses and Coaches Across the UK and USA",
          "tours": "Tours and Day Trips in UK and US Cities", "packages": "Holiday Packages to UK and US Cities", "taxi": "Taxi and Airport Transfers in UK and US Cities"}[kind]
    intro = blurb + " Choose a directory below, search by city, or open one of the popular guides."
    ds = {}
    hero_html = hero([("Home", "index.html"), (label_, None)], h1, intro,
                     '<div class="btn-row">' + aff(kind, f"Search {label_.lower()} with our partner", ds) + "</div>" + finder(kind))
    parts = [note()]
    if kind in ("flights", "trains", "buses"):
        files = {"flights": [("flights-uk.html", "UK domestic flights"), ("flights-usa.html", "USA domestic flights"), ("flights-uk-to-usa.html", "UK to USA flights"), ("flights-usa-to-uk.html", "USA to UK flights")],
                 "trains": [("trains-uk.html", "Trains in Great Britain"), ("trains-usa.html", "Trains in the USA")],
                 "buses": [("buses-uk.html", "Coaches in Great Britain"), ("buses-usa.html", "Buses in the USA")]}[kind]
        parts.append("<h2>Browse by country</h2>" + pills(files))
        pop = popular(kind)
        parts.append(f"<h2>Popular {label_.lower()} guides</h2>" + link_list(pop))
        total = len(RT[kind])
        parts.append(f"<p>This section currently includes {fnum(total)} route guides. Each one covers distance, typical travel time, practical tips and a button to our partner's live search.</p>")
    else:
        files = [(f"{kind if kind != 'packages' else 'holiday-packages'}-uk.html", "UK cities and towns"), (f"{kind if kind != 'packages' else 'holiday-packages'}-usa.html", "US cities and towns")]
        parts.append("<h2>Browse by country</h2>" + pills(files))
        top = [p for p in PLACES if p["country"] == "UK"][:8] + [p for p in PLACES if p["country"] == "USA"][:8]
        parts.append(f"<h2>Popular destinations</h2>" + link_list([(cfile(kind, p), {"tours": f"Tours in {p['disp']}", "packages": f"Holiday packages to {p['disp']}", "taxi": f"Taxi in {p['disp']}"}[kind]) for p in top]))
    how = {"flights": ["Use the search box or choose a route guide.", "Read the airport and time notes for both ends.", "Click the booking button to compare live fares with our partner."],
           "trains": ["Pick a route guide or search for your cities.", "Check the journey-time range and ticket tips.", "Click through to our partner to see timetables and prices."],
           "buses": ["Find your route in the directory.", "Check stop, luggage and timing notes.", "Continue to our partner to see departures and fares."],
           "tours": ["Choose the city you will visit.", "Read which tour types and day trips to compare.", "Continue to our partner to see availability."],
           "packages": ["Choose the city you want to visit.", "Check inclusions, departures and entry checks.", "Continue to our partner to compare packages."],
           "taxi": ["Choose the city where you need a ride.", "Read the airport and pre-booking notes.", "Continue to our partner to check transfer options."]}[kind]
    parts.append("<h2>How to use this section</h2><ol>" + "".join(f"<li>{esc(x)}</li>" for x in how) + "</ol>")
    parts.append(cta(kind, f"Search {label_.lower()} with our partner", ds))
    faqs = [(f"Do you sell {label_.lower()}?", f"No. We publish guides and link to a partner that sells {label_.lower()}. You complete your booking on the partner's website."),
            ("Are prices shown on this site?", "No. Prices change quickly, so we do not publish them. The partner's page shows current prices."),
            ("Does it cost extra to use your links?", "No. The price you pay is set by the partner. We may earn a commission if you book.")]
    parts.append("<!--FAQ-->")
    render(fname, titles[kind], descs[kind], kws, hero_html + '<div class="container page-body">' + "".join(parts) + "</div>", "hub", faqs=faqs, finder_on=True)

def directory_pages():
    # route directories
    spec = {
        "flights-uk.html": ("flights", lambda a_, b_: a_["country"] == "UK" and b_["country"] == "UK", "UK Domestic Flights", "Flights within the UK: routes between major airports, with distance and airport notes."),
        "flights-usa.html": ("flights", lambda a_, b_: a_["country"] == "USA" and b_["country"] == "USA", "USA Domestic Flights", "Flights within the USA between the busiest airport hubs, with distance and airport notes."),
        "flights-uk-to-usa.html": ("flights", lambda a_, b_: a_["country"] == "UK" and b_["country"] == "USA", "UK to USA Flights", "Flights from UK cities to US cities, with airports, flight-time estimates and entry reminders."),
        "flights-usa-to-uk.html": ("flights", lambda a_, b_: a_["country"] == "USA" and b_["country"] == "UK", "USA to UK Flights", "Flights from US cities to UK cities, with airports, flight-time estimates and entry reminders."),
        "trains-uk.html": ("trains", lambda a_, b_: a_["country"] == "UK", "Trains in Great Britain", "City-to-city train guides across Great Britain, with journey-time ranges."),
        "trains-usa.html": ("trains", lambda a_, b_: a_["country"] == "USA", "Trains in the USA", "City-to-city train guides for the main US rail corridors, with journey-time ranges."),
        "buses-uk.html": ("buses", lambda a_, b_: a_["country"] == "UK", "Coaches in Great Britain", "Intercity coach guides across Great Britain, with typical journey times."),
        "buses-usa.html": ("buses", lambda a_, b_: a_["country"] == "USA", "Buses in the USA", "Intercity bus guides for the USA, with typical journey times."),
    }
    for fname, (kind, test, h1, intro) in spec.items():
        rows = [(x, y) for x, y, _ in RT[kind] if test(x, y)]
        groups = {}
        for x, y in rows: groups.setdefault(x["slug"], (x, [])) ; groups[x["slug"]][1].append(y)
        parts = [note(), f"<p>{fnum(len(rows))} route guides, grouped by departure place. Select a route for distance, time estimates and booking tips.</p>"]
        parts.append(pills([(f"#from-{s}", x["disp"]) for s, (x, _) in groups.items()]))
        for s, (x, ys) in groups.items():
            parts.append(f'<h2 id="from-{s}">From {esc(x["disp"])}</h2>' + link_list([(rfile(kind, x, y), f"{x['disp']} to {y['disp']}") for y in ys]))
        title = trim(f"{h1}: All Routes and Guides", 62)
        desc = trim(f"{intro} Browse every route guide in this directory.", 160)
        kw = [h1.lower(), f"{h1.lower()} routes", f"{KIND_LABEL[kind].lower()} guide", f"{KIND_LABEL[kind].lower()} directory", f"book {KIND_LABEL[kind].lower()} online"]
        hh = hero([("Home", "index.html"), (KIND_LABEL[kind], f"{kind}.html"), (h1, None)], h1, intro)
        render(fname, title, desc, kw, hh + '<div class="container page-body">' + "".join(parts) + cta(kind, f"Search {KIND_LABEL[kind].lower()} with our partner", {}) + "</div>", "directory")
    # city directories
    for kind, prefix, h1b in (("tours", "tours", "Tours and Day Trips"), ("packages", "holiday-packages", "Holiday Packages"), ("taxi", "taxi", "Taxi and Airport Transfers")):
        for ctry, cl, cn in (("UK", "uk", "the UK"), ("USA", "usa", "the USA")):
            fname = f"{prefix}-{cl}.html"
            h1 = f"{h1b} in {cn}" if kind != "packages" else f"Holiday Packages to {cn.replace('the ', '')} Destinations"
            ps = [p for p in PLACES if p["country"] == ctry]
            parts = [note(), f"<p>{len(ps)} cities and towns, grouped by {'nation' if ctry == 'UK' else 'state'}.</p>"]
            regs = {}
            for p in ps: regs.setdefault(p["region"], []).append(p)
            for r, lst in regs.items():
                parts.append(f"<h2>{esc(r)}</h2>" + link_list([(cfile(kind, p), p["disp"]) for p in lst]))
            title = trim(f"{h1}: All Cities and Towns", 62)
            desc = trim(f"Browse {h1b.lower()} guides for {len(ps)} places in {cn}, grouped by {'nation' if ctry == 'UK' else 'state'}.", 160)
            kw = [h1.lower(), f"{h1b.lower()} {cl}", f"{h1b.lower()} {cn}", "city guides", "book online"]
            hh = hero([("Home", "index.html"), (CATS[[c[0] for c in CATS].index(kind)][1], f"{prefix}.html"), (h1, None)], h1, f"Choose a place to see {h1b.lower()} options, nearby places and booking tips.")
            render(fname, title, desc, kw, hh + '<div class="container page-body">' + "".join(parts) + cta(kind, f"Search {h1b.lower()} with our partner", {}) + "</div>", "directory")

def country_and_region_pages():
    for ctry, cl, cn, fname in (("UK", "uk", "United Kingdom", "travel-uk.html"), ("USA", "usa", "United States", "travel-usa.html")):
        ps = [p for p in PLACES if p["country"] == ctry]
        regs = {}
        for p in ps: regs.setdefault(p["region"], []).append(p)
        short = "UK" if ctry == "UK" else "USA"
        title = trim(f"Travel in the {short}: Cities, Towns & Guides", 62)
        desc = f"Explore {len(ps)} cities and towns across the {cn}, with travel guides for flights, trains, buses, tours, holiday packages and transfers."
        kw = [f"travel {short}", f"travel in the {cn}", f"{short} cities", f"{short} travel guide", f"{short} towns", f"visit {short}", f"{short} destinations"]
        hh = hero([("Home", "index.html"), (f"Travel in the {short}", None)], f"Travel in the {cn}",
                  f"Guides for {len(ps)} cities and towns across the {cn}. Choose a {'nation' if ctry == 'UK' else 'state'} or a place, then compare transport, tours, packages and transfers.")
        parts = [note(), f"<h2>Browse by {'nation' if ctry == 'UK' else 'state'}</h2>"]
        parts.append(pills([(REGION_HUB[(ctry, r)], r) if (ctry, r) in REGION_HUB else (cfile("travel", lst[0]), r) for r, lst in regs.items()]))
        parts.append("<h2>Largest places in this guide</h2>" + link_list([(cfile("travel", p), f"Travel to {p['disp']}") for p in ps[:20]]))
        parts.append("<h2>Services</h2>" + link_list([({"flights": f"flights-{cl}.html", "trains": f"trains-{cl}.html", "buses": f"buses-{cl}.html", "tours": f"tours-{cl}.html", "packages": f"holiday-packages-{cl}.html", "taxi": f"taxi-{cl}.html"}[k], f"{KIND_LABEL.get(k, dict((c[0], c[1]) for c in CATS)[k])} in the {short}") for k in ("flights", "trains", "buses", "tours", "packages", "taxi")]))
        render(fname, title, desc, kw, hh + '<div class="container page-body">' + "".join(parts) + "</div>", "hub")
    for (ctry, region), ps in REGIONS.items():
        if (ctry, region) not in REGION_HUB: continue
        fname = REGION_HUB[(ctry, region)]
        short = "UK" if ctry == "UK" else "USA"
        title = trim(f"Travel in {region}: Cities, Transport & Tours", 62)
        desc = f"Plan travel in {region}: guides for {len(ps)} places with links to flights, trains, buses, tours, holiday packages and transfers."
        kw = [f"travel {region}", f"visit {region}", f"{region} cities", f"{region} travel guide", f"things to do in {region}", f"getting around {region}"]
        hh = hero([("Home", "index.html"), (f"Travel in the {short}", f"travel-{'uk' if ctry == 'UK' else 'usa'}.html"), (region, None)], f"Travel in {region}",
                  f"Our guide covers {len(ps)} places in {region}. Open a place to see how to get there and what to book.")
        rows = "".join(f"<tr><th scope='row'>{a(cfile('travel', p), p['disp'])}</th><td>{a(cfile('tours', p), 'Tours')}</td><td>{a(cfile('packages', p), 'Packages')}</td><td>{a(cfile('taxi', p), 'Taxi')}</td></tr>" for p in ps)
        table = f'<div style="overflow-x:auto"><table class="plain"><thead><tr><th>Place</th><th>Tours</th><th>Packages</th><th>Taxi</th></tr></thead><tbody>{rows}</tbody></table></div>'
        parts = [note(), f"<h2>Places in {esc(region)}</h2>" + table, f"<p>Back to the {a('travel-uk.html' if ctry == 'UK' else 'travel-usa.html', 'full ' + short + ' guide')}.</p>"]
        render(fname, title, desc, kw, hh + '<div class="container page-body">' + "".join(parts) + "</div>", "hub")

def destinations_page():
    hh = hero([("Home", "index.html"), ("Destinations", None)], "All UK and USA Destinations", f"Every city and town in our guide: {len(PLACES)} places. Search for a route or pick a place to begin.", finder("flights"))
    parts = [note()]
    for ctry, nm in (("UK", "United Kingdom"), ("USA", "United States")):
        parts.append(f"<h2>{nm}</h2>")
        regs = {}
        for p in PLACES:
            if p["country"] == ctry: regs.setdefault(p["region"], []).append(p)
        for r, lst in regs.items():
            head = a(REGION_HUB[(ctry, r)], r) if (ctry, r) in REGION_HUB else esc(r)
            parts.append(f"<h3>{head}</h3>" + link_list([(cfile("travel", p), p["disp"]) for p in lst]))
    render("destinations.html", "All UK & USA Destinations: Cities and Towns", f"Browse {len(PLACES)} UK and US cities and towns and open a travel guide for flights, trains, buses, tours, holiday packages and taxi transfers.",
           ["UK cities", "USA cities", "travel destinations", "UK towns", "US towns", "travel guides", "city list"], hh + '<div class="container page-body">' + "".join(parts) + "</div>", "hub", finder_on=True)

def home_page():
    cards = "".join(f'<div class="card cat-card"><h3>{esc(c[1])}</h3><p>{esc(c[3])}</p>{a(c[2], "Open " + c[1] + " guides", "more")}</div>' for c in CATS)
    hh = hero([("Home", None)] if False else [("Home", None)], "Plan Your Trip Across the UK and USA",
              "Independent guides to flights, trains, coaches, tours, holiday packages and taxi transfers between cities and towns in the UK and USA. Find your route, then book with our partners.",
              finder("flights"))
    pf, pt = popular("flights")[:6], popular("trains")[:4]
    pb = popular("buses")[:4]
    ukc = [p for p in PLACES if p["country"] == "UK"][:12]
    usc = [p for p in PLACES if p["country"] == "USA"][:12]
    how = ("<div class='grid'><div class='card'><h3>1. Find your route</h3><p>Search by city or open a guide for flights, trains, buses, tours, packages or transfers.</p></div>"
           "<div class='card'><h3>2. Read the practical notes</h3><p>See distances, estimated times, airports, stations and tips written for each place.</p></div>"
           "<div class='card'><h3>3. Book with a partner</h3><p>Click a button to see live availability and prices on our travel partner's site.</p></div></div>")
    parts = [note(), "<h2>What are you looking for?</h2><div class='grid'>" + cards + "</div>",
             "<h2>Popular flights</h2>" + link_list(pf), "<h2>Popular train routes</h2>" + link_list(pt), "<h2>Popular bus and coach routes</h2>" + link_list(pb),
             "<h2>Popular UK destinations</h2>" + link_list([(cfile("travel", p), p["disp"]) for p in ukc]),
             "<h2>Popular US destinations</h2>" + link_list([(cfile("travel", p), p["disp"]) for p in usc]),
             f"<p>See the {a('destinations.html', 'full list of places')} or browse by {a('travel-uk.html', 'UK')} and {a('travel-usa.html', 'USA')}. A {a('sitemap.html', 'site map')} and our {a('disclaimer.html', 'disclaimer')} are also available.</p>",
             "<h2>How it works</h2>" + how, "<!--FAQ-->"]
    faqs = [("Do you sell tickets directly?", "No. We are an independent affiliate website. When you click a booking button you go to a partner's site to complete the purchase."),
            ("Do you show prices?", "No. Prices change often, so please check the partner's site for current prices."),
            ("Which places do you cover?", f"We cover {len(PLACES)} cities and towns in the UK and USA, with route guides between the busiest pairs."),
            ("Does it cost more to use your links?", "No. You pay the same price, and we may earn a commission if you book.")]
    render("index.html", "UK & USA Travel Guides: Flights, Trains, Buses & Tours",
           "Find flights, trains, buses, tours, holiday packages and taxi transfers across UK and US cities. Read route guides, then check live options with our partners.",
           ["UK USA travel", "flights UK USA", "train tickets UK", "bus tickets USA", "holiday packages", "airport transfers", "tours UK USA", "travel guide", "city to city travel"],
           hh + '<div class="container page-body">' + "".join(parts) + "</div>", "home", faqs=faqs, finder_on=True)

# ------------------------------------------------------------- legal & standard
def page_simple(fname, title, desc, kws, h1, intro, sections, kind="legal", updated=True):
    body = "".join(f"<h2>{esc(h)}</h2>" + "".join(f"<p>{x}</p>" if not x.startswith("<") else x for x in paras) for h, paras in sections)
    upd = '<p class="note">Last updated: <span data-cfg="lastUpdated">1 November 2026</span></p>' if updated else ""
    hh = hero([("Home", "index.html"), (h1, None)], h1, intro)
    render(fname, title, desc, kws, hh + '<div class="container page-body narrow">' + upd + body + "</div>", kind)

CONTACT_BLOCK = '<p data-wrap hidden><strong>Contact:</strong> <span data-cfg="legalContact"></span></p>'

def legal_pages():
    page_simple("disclaimer.html", "Disclaimer", "Read our disclaimer: this site provides general travel information and affiliate links, not bookings, advice or guaranteed prices or times.",
        ["disclaimer", "travel disclaimer", "affiliate website disclaimer", "website terms"], "Disclaimer",
        "Please read this disclaimer before you use this website or click any booking link.", [
        ("We are not a travel seller", ["This website is an independent information site. We do not sell, issue or manage tickets, bookings, tours, packages or transfers. When you click a booking button you leave this site and deal directly with a third-party partner, whose terms apply to your purchase."]),
        ("Affiliate links", ["Some links on this site are affiliate links. If you buy through them we may earn a commission at no extra cost to you. See our <a href=\"affiliate-disclosure.html\">Affiliate Disclosure</a> for details."]),
        ("Information only", ["Distances, journey times, airport names and other details are general estimates intended to help you plan. Schedules, routes, fares, stations, stops and entry rules change. Always check the details with the operator or partner before you travel."]),
        ("No prices or availability", ["We do not publish prices, availability or ratings. Any figures you see on a partner's site are controlled by that partner."]),
        ("Travel documents and safety", ["Entry rules, visas, travel authorisations, health requirements and safety advice depend on your nationality and change often. Check official government sources for the UK and USA before you book or travel."]),
        ("Third-party websites", ["We are not responsible for the content, accuracy, privacy practices or availability of third-party websites we link to."]),
        ("Limitation of liability", ["To the fullest extent permitted by law, we are not liable for loss or damage arising from your use of this website or from any purchase made through a partner. Nothing in this disclaimer limits any liability that cannot be excluded by law."]),
        ("Changes", ["We may update this page at any time. The date at the top shows when it was last changed."])])
    page_simple("affiliate-disclosure.html", "Affiliate Disclosure", "How this website earns money: we use affiliate links for flights, trains, buses, tours, packages and taxi transfers and may earn commission at no extra cost to you.",
        ["affiliate disclosure", "affiliate links", "commission disclosure", "advertising disclosure"], "Affiliate Disclosure",
        "We want you to know exactly how this website is funded.", [
        ("How we earn", ["We are a participant in affiliate programmes. When you click certain links and then buy a flight, train or bus ticket, tour, holiday package or taxi transfer from our partner, we may receive a commission."]),
        ("No extra cost to you", ["Using our links does not increase the price you pay. Prices are set by our partners."]),
        ("Link markings", ["Booking buttons use <code>rel=\"sponsored nofollow\"</code> so that search engines can identify them as paid or affiliate links."]),
        ("Editorial approach", ["Our guides are written to help you plan. Commission does not change the distances, time estimates or tips we publish. We do not claim that any option is the cheapest or the best, and we do not publish prices."]),
        ("Legal context", ["This disclosure is intended to meet transparency rules for endorsements and affiliate marketing, including guidance from the US Federal Trade Commission and the UK Advertising Standards Authority and Competition and Markets Authority."]),
        ("Your purchase", ["Your contract is with the partner, not with us. Questions about a booking, refunds or changes must be sent to that partner."])])
    page_simple("privacy-policy.html", "Privacy Policy", "How this website handles personal data: we do not run accounts or forms, third-party partners may collect data after you click, and your rights under UK and US law.",
        ["privacy policy", "data protection", "privacy travel website", "GDPR privacy"], "Privacy Policy",
        "This policy explains what information is and is not collected when you use this website.", [
        ("What we collect", ["This website has no accounts, no contact or query forms and no ordering system, so we do not ask you to enter personal details. Route and place search boxes work in your browser to take you to a page or a partner link."]),
        ("Hosting and logs", ["The site is hosted on a static hosting service. Hosting providers may record technical data such as IP address, browser type and time of visit in server logs for security and operation."]),
        ("Partner websites", ["When you click a booking button you leave this site. The partner may use cookies and collect data under its own privacy policy. We encourage you to read it before you book."]),
        ("Cookies and analytics", ["This site does not set advertising cookies itself. See our <a href=\"cookie-policy.html\">Cookie Policy</a>. If analytics are added in future, this policy will be updated."]),
        ("Your rights", ["Depending on where you live, you may have rights over your personal data, for example under UK GDPR or US state privacy laws, including the right to ask what data is held, to correct or delete it, or to object to processing. Because we do not collect personal data through this website, requests normally relate to hosting logs or to partner sites."]),
        ("Children", ["This website is not directed at children under 13, and we do not knowingly collect their data."]),
        ("Changes", ["We may update this policy. The date at the top shows the latest version."]),
        ("Contact", ["If a contact method is published for privacy requests, it appears below."])] )
    # add contact block to privacy
    p = os.path.join(ROOT, "privacy-policy.html")
    s = open(p, encoding="utf-8").read()
    s = s.replace("If a contact method is published for privacy requests, it appears below.</p>", "If a contact method is published for privacy requests, it appears below.</p>" + CONTACT_BLOCK)
    open(p, "w", encoding="utf-8").write(s)
    page_simple("cookie-policy.html", "Cookie Policy", "What cookies and similar technologies this website uses, and how partner websites may use them after you click a booking link.",
        ["cookie policy", "cookies", "tracking", "affiliate cookies"], "Cookie Policy",
        "Cookies are small files stored by your browser. This page explains how they relate to this site.", [
        ("Cookies on this site", ["This website does not set advertising or tracking cookies itself. Your browser may store technical files, such as cached styles and scripts, to load pages faster."]),
        ("Affiliate cookies", ["When you click an affiliate link, the partner's website may set a cookie so that a purchase can be linked to us for commission. That cookie belongs to the partner and is covered by its policy."]),
        ("Managing cookies", ["You can block or delete cookies in your browser settings. Blocking some cookies may affect how partner websites work."]),
        ("Changes", ["If we add analytics or other tools in future, we will update this policy and, where required, ask for consent."])])
    page_simple("terms.html", "Terms of Use", "Terms of use for this travel guide website: acceptable use, no booking contract, intellectual property and limits of liability.",
        ["terms of use", "terms and conditions", "website terms", "travel website terms"], "Terms of Use",
        "By using this website you agree to these terms.", [
        ("Use of the site", ["You may use this website for personal, non-commercial planning. You must not misuse it, attempt to disrupt it or copy it in bulk without permission."]),
        ("No booking contract", ["Information on this site is not an offer to sell travel. Any booking is a contract between you and our partner."]),
        ("Accuracy", ["We aim to be accurate, but we do not guarantee that information is complete or current. See our <a href=\"disclaimer.html\">Disclaimer</a>."]),
        ("Intellectual property", ["The text, layout and design of this site are protected. See our <a href=\"copyright.html\">Copyright</a> page. Partner and place names belong to their owners."]),
        ("Links", ["You may link to our pages. We are not responsible for the content of third-party sites we link to."]),
        ("Liability and governing law", ["Nothing in these terms excludes liability that cannot be excluded by law. Subject to that, we are not liable for indirect or consequential loss. Disputes are subject to the law of the country in which the site owner is based."]),
        ("Changes", ["We may update these terms. Continued use means you accept the new version."])])
    page_simple("copyright.html", "Copyright Notice", "Copyright notice for this website: original text, layout and code are protected, brand names belong to their owners, and how to report concerns.",
        ["copyright", "copyright notice", "intellectual property", "trademark notice"], "Copyright Notice",
        "Information about ownership of the content on this website.", [
        ("Our content", ["&copy; <span data-year></span> <span data-brand></span>. The original text, page layout, design and code of this website are protected by copyright. You may quote short extracts with a link back to the source, but you may not republish pages or copy them in bulk without written permission."]),
        ("Trademarks", ["Airline, rail, bus, hotel, partner and place names mentioned on this site belong to their owners and are used only to describe services. Their use does not imply endorsement or affiliation."]),
        ("Reporting a concern", ["If you believe content on this site infringes your rights, please tell us with enough detail to identify the page and the material, and we will review it promptly."]),
        ("Contact", ["If a contact method is published, it appears below."])])
    p = os.path.join(ROOT, "copyright.html")
    s = open(p, encoding="utf-8").read()
    s = s.replace("If a contact method is published, it appears below.</p>", "If a contact method is published, it appears below.</p>" + CONTACT_BLOCK)
    open(p, "w", encoding="utf-8").write(s)
    page_simple("about.html", "About Us", "About this independent travel guide for the UK and USA: what we publish, how we write it and how we are funded.",
        ["about us", "about travel guide", "independent travel guide", "UK USA travel guide"], "About This Site",
        "We publish practical guides to help people plan journeys between cities and towns in the UK and USA.", [
        ("What we do", [f"We cover {len(PLACES)} cities and towns and {fnum(sum(len(v) for v in RT.values()))} city-to-city route guides for flights, trains and buses, plus city guides for tours, holiday packages and taxi transfers."]),
        ("How we write", ["Each page uses distances, typical travel-time ranges, airport and stop notes and booking tips. Figures are estimates for planning, and we say so clearly. We do not publish prices or ratings."]),
        ("How we are funded", ["We earn commission from affiliate partners if you book through our links. Read the <a href=\"affiliate-disclosure.html\">Affiliate Disclosure</a>."]),
        ("Not a seller", ["We are not a travel agent and do not sell tickets. Bookings are completed with our partners."]),
        ("Data credits", ["Place names in the search box come from the GeoNames gazetteer (licensed CC BY 4.0, geonames.org) and the open-source US Cities Database (MIT licence)."])], kind="info", updated=False)
    page_simple("how-it-works.html", "How It Works", "How to use this travel guide: find your route, read the planning notes and continue to a partner to see live availability and prices.",
        ["how it works", "how to book travel", "travel guide help", "affiliate travel site"], "How It Works",
        "Three simple steps from planning to booking.", [
        ("1. Find your route", ["Use the search box on the home page or browse the flights, trains, buses, tours, holiday packages and taxi sections. Each route and place has its own page."]),
        ("2. Read the planning notes", ["Every page shows distances, typical time ranges, airport or station notes and tips written for that place or route."]),
        ("3. Check live options", ["Press a booking button to open our partner's website in a new tab and see current availability, prices and terms."]),
        ("If we do not have a page", ["If you search for a route we do not have a guide for, the site opens the partner's search directly so you can still check options."]),
        ("Good to know", ["You never enter personal details on this site. Your booking and payment happen on the partner's website."])], kind="info", updated=False)

def sitemap_page():
    parts = [note()]
    parts.append("<h2>Main pages</h2>" + link_list([("index.html", "Home"), ("destinations.html", "All destinations"), ("travel-uk.html", "Travel in the UK"), ("travel-usa.html", "Travel in the USA"), ("how-it-works.html", "How it works"), ("about.html", "About us")]))
    parts.append("<h2>Categories</h2>" + link_list([(c[2], c[1]) for c in CATS]))
    parts.append("<h2>Directories</h2>" + link_list([("flights-uk.html", "UK domestic flights"), ("flights-usa.html", "USA domestic flights"), ("flights-uk-to-usa.html", "UK to USA flights"), ("flights-usa-to-uk.html", "USA to UK flights"),
        ("trains-uk.html", "Trains in Great Britain"), ("trains-usa.html", "Trains in the USA"), ("buses-uk.html", "Coaches in Great Britain"), ("buses-usa.html", "Buses in the USA"),
        ("tours-uk.html", "Tours in the UK"), ("tours-usa.html", "Tours in the USA"), ("holiday-packages-uk.html", "Holiday packages UK"), ("holiday-packages-usa.html", "Holiday packages USA"),
        ("taxi-uk.html", "Taxi in the UK"), ("taxi-usa.html", "Taxi in the USA")]))
    parts.append("<h2>Regions</h2>" + link_list([(f, k[1]) for k, f in REGION_HUB.items()]))
    parts.append("<h2>Legal</h2>" + link_list([("disclaimer.html", "Disclaimer"), ("affiliate-disclosure.html", "Affiliate Disclosure"), ("privacy-policy.html", "Privacy Policy"), ("cookie-policy.html", "Cookie Policy"), ("terms.html", "Terms of Use"), ("copyright.html", "Copyright")]))
    hh = hero([("Home", "index.html"), ("Site Map", None)], "Site Map", "Every main section of the website. Route and city pages are listed in the directories.")
    render("sitemap.html", "Site Map: All Sections", "HTML site map for this travel guide: categories, directories, regions and legal pages.", ["site map", "sitemap", "travel guide pages"],
           hh + '<div class="container page-body">' + "".join(parts) + "</div>", "info")

def not_found():
    hh = hero([("Home", "index.html"), ("Page not found", None)], "Page Not Found", "That page does not exist or has moved. Try one of these instead.")
    parts = [link_list([("index.html", "Home"), ("destinations.html", "All destinations"), ("flights.html", "Flights"), ("trains.html", "Trains"), ("buses.html", "Buses"), ("tours.html", "Tours"), ("holiday-packages.html", "Holiday packages"), ("taxi.html", "Taxi and transfers")])]
    render("404.html", "Page Not Found", "The page you were looking for could not be found. Use these links to continue planning your trip.", ["page not found", "404"], hh + '<div class="container page-body">' + "".join(parts) + "</div>", "info", extra_head='<base href="/">' if False else "")

def build_all():
    home_page()
    for c in CATS: hub_page(c[0])
    directory_pages(); country_and_region_pages(); destinations_page()
    legal_pages(); sitemap_page(); not_found()
