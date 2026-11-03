"""Shared data preparation, helpers and HTML components for the generator."""
import os, re, json, math, hashlib, html
from collections import Counter
from places_data import *

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
esc = lambda s: html.escape(str(s), quote=True)
PAGES = {}   # filename -> {"title","kind"}

def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

def hnum(*parts):
    return int(hashlib.md5("|".join(map(str, parts)).encode()).hexdigest(), 16)

def pick(lst, *key):
    return lst[hnum(*key) % len(lst)]

def pick_n(lst, n, *key):
    idx = sorted(range(len(lst)), key=lambda i: hnum(i, *key))[:n]
    return [lst[i] for i in idx]

# ---------------------------------------------------------------- places
PLACES = []
for name, nation, lat, lon, code, air, own, blurb in UK:
    PLACES.append(dict(name=name, country="UK", cname="the United Kingdom", region=nation, rslug=slugify(nation),
                       st="", lat=lat, lon=lon, code=code, air=air, own=own, amtrak=0, mainland=1,
                       gb=(nation != "Northern Ireland"), blurb=blurb))
for name, st, lat, lon, code, air, own, amtrak, mainland, blurb in US:
    PLACES.append(dict(name=name, country="USA", cname="the United States", region=US_STATES[st],
                       rslug=slugify(US_STATES[st]), st=st, lat=lat, lon=lon, code=code, air=air, own=own,
                       amtrak=amtrak, mainland=mainland, gb=False, blurb=blurb))
_cnt = Counter(slugify(p["name"]) for p in PLACES)
for p in PLACES:
    base = slugify(p["name"])
    p["slug"] = f"{base}-{p['st'].lower()}" if (_cnt[base] > 1 and p["country"] == "USA") else base
    p["disp"] = p["name"] if p["slug"] == base else f"{p['name']}, {p['st']}"
    if p["country"] == "UK":
        p["label"] = f"{p['name']}, {p['region']}"
    else:
        p["label"] = p["name"] if p["st"] == "DC" else f"{p['name']}, {p['st']}"
    p["short_air"] = re.sub(r"^nearest:\s*", "", p["air"])
    p["pop"] = PLACES.index(p) if False else 0
for i, p in enumerate(PLACES):
    p["idx"] = i
BYSLUG = {p["slug"]: p for p in PLACES}
assert len(BYSLUG) == len(PLACES), "duplicate slugs"

def find(key, country):
    for p in PLACES:
        if p["country"] != country:
            continue
        if p["name"] == key or f"{p['name']}, {p['st']}" == key:
            return p
    raise KeyError(key)

REGIONS = {}
for p in PLACES:
    REGIONS.setdefault((p["country"], p["region"]), []).append(p)
REGION_HUB = {k: f"visit-{slugify(k[1])}.html" for k, v in REGIONS.items() if len(v) >= 2}

def region_link(p):
    return REGION_HUB.get((p["country"], p["region"]))

def km_between(a, b):
    r = 6371.0
    la1, lo1, la2, lo2 = map(math.radians, (a["lat"], a["lon"], b["lat"], b["lon"]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 2 * r * math.asin(math.sqrt(h))

def miles(km): return int(round(km * 0.621371))
def fnum(n): return f"{int(n):,}"

def hm(h):
    m = max(5, int(round(h * 60 / 5.0)) * 5)
    hh, mm = divmod(m, 60)
    if hh == 0: return f"{mm} min"
    return f"{hh} h" if mm == 0 else f"{hh} h {mm:02d} min"

def drange(lo, hi):
    return f"{hm(lo)} to {hm(hi)}"

def nearby(p, n=6, maxkm=None):
    others = [(km_between(p, q), q) for q in PLACES if q is not p and q["country"] == p["country"]]
    others.sort(key=lambda t: t[0])
    if maxkm: others = [t for t in others if t[0] <= maxkm]
    return others[:n]

# ---------------------------------------------------------------- routes
RT = {"flights": [], "trains": [], "buses": []}
RS = {"flights": set(), "trains": set(), "buses": set()}

def _add(kind, a, b, km):
    if a is b or (a["slug"], b["slug"]) in RS[kind]: return
    RS[kind].add((a["slug"], b["slug"]))
    RT[kind].append((a, b, km))

def flight_time(a, b, km):
    if a["country"] == "UK" and b["country"] == "USA": base = km / 760 + 0.6
    elif a["country"] == "USA" and b["country"] == "UK": base = km / 860 + 0.6
    else: base = km / 780 + 0.55
    return base * 0.9, base * 1.12

def train_time(a, b, km):
    if a["country"] == "UK": return km * 1.15 / 150 + 0.1, km * 1.25 / 90 + 0.2
    if a["name"] in NE_SET and b["name"] in NE_SET and a["country"] == "USA":
        return km * 1.15 / 150 + 0.3, km * 1.25 / 95 + 0.5
    return km * 1.25 / 110 + 0.3, km * 1.35 / 70 + 0.5

def bus_time(a, b, km):
    if a["country"] == "UK": return km * 1.25 / 85 + 0.2, km * 1.35 / 60 + 0.5
    return km * 1.25 / 90 + 0.3, km * 1.35 / 65 + 0.6

def drive_time(km): return km * 1.25 / 85, km * 1.3 / 65

NE_SET = {"Boston", "New York", "Philadelphia", "Baltimore", "Washington, DC", "Providence", "Wilmington", "Hartford"}

def build_routes():
    uk_air = [find(n, "UK") for n in UK_AIR_HUBS]
    us_air = [find(n, "USA") for n in US_AIR_HUBS]
    for a in uk_air:
        for b in uk_air:
            km = km_between(a, b) if a is not b else 0
            if a is not b and km >= 180: _add("flights", a, b, km)
    for a in us_air:
        for b in us_air:
            km = km_between(a, b) if a is not b else 0
            if a is not b and km >= 250: _add("flights", a, b, km)
    uk_t = [find(n, "UK") for n in UK_TRANSATLANTIC]
    us_t = [find(n, "USA") for n in US_TRANSATLANTIC]
    for a in uk_t:
        for b in us_t:
            km = km_between(a, b)
            _add("flights", a, b, km); _add("flights", b, a, km)
    gb = [p for p in PLACES if p["country"] == "UK" and p["gb"]][:UK_ROUTE_TOP]
    for a in gb:
        for b in gb:
            if a is not b:
                km = km_between(a, b)
                _add("trains", a, b, km); _add("buses", a, b, km)
    rail = [find(n, "USA") for n in US_RAIL_HUBS]
    for a in rail:
        for b in rail:
            if a is not b and a["amtrak"] and b["amtrak"]:
                km = km_between(a, b)
                if 120 <= km <= 1000: _add("trains", a, b, km)
    bus = [p for p in PLACES if p["country"] == "USA" and p["mainland"]][:US_BUS_TOP]
    for a in bus:
        for b in bus:
            if a is not b:
                km = km_between(a, b)
                if 80 <= km <= 900: _add("buses", a, b, km)

def rfile(kind, a, b): return f"{kind}-{a['slug']}-to-{b['slug']}.html"
def cfile(kind, p):
    return {"travel": f"travel-{p['slug']}.html", "tours": f"tours-in-{p['slug']}.html",
            "packages": f"holiday-packages-{p['slug']}.html", "taxi": f"taxi-in-{p['slug']}.html"}[kind]

# ---------------------------------------------------------------- html components
def attrs(**d):
    m = {"from": "data-from", "to": "data-to", "fromCode": "data-from-code", "toCode": "data-to-code",
         "fromSlug": "data-from-slug", "toSlug": "data-to-slug", "city": "data-city", "cityCode": "data-city-code",
         "citySlug": "data-city-slug"}
    return " ".join(f'{m[k]}="{esc(v)}"' for k, v in d.items() if v)

def ds_route(a, b): return dict(**{"from": a["disp"] if False else a["name"]}, to=b["name"], fromCode=a["code"], toCode=b["code"], fromSlug=a["slug"], toSlug=b["slug"])
def ds_city(p): return dict(city=p["name"], cityCode=p["code"], citySlug=p["slug"])

def aff(cat, text, ds, cls="btn btn-aff"):
    return f'<a class="{cls}" data-aff="{cat}" {attrs(**ds)} href="#" rel="sponsored nofollow noopener">{esc(text)}</a>'

def a(href, text, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<a{c} href="{href}">{esc(text)}</a>'

def link_list(items):
    return '<ul class="link-list">' + "".join(f"<li>{a(h, t)}</li>" for h, t in items) + "</ul>"

def pills(items):
    return '<div class="pill-row">' + "".join(a(h, t, "pill") for h, t in items) + "</div>"

def facts(rows):
    return '<div class="facts">' + "".join(f'<div class="fact"><b>{esc(v)}</b><span>{esc(l)}</span></div>' for v, l in rows) + "</div>"

def note(text=None, warn=False):
    inner = f'<span data-disclosure>{esc(text)}</span>' if text is None else esc(text)
    if text is None:
        inner = '<span data-disclosure>This site contains affiliate links. If you book through them we may earn a commission at no extra cost to you.</span>'
    return f'<p class="note{" warn" if warn else ""}">{inner} <a href="affiliate-disclosure.html">Read more</a></p>'

def cta(cat, text, ds, sub="You will leave this site and complete your booking with our partner."):
    return f'<div class="cta-box">{aff(cat, text, ds)}<p>{esc(sub)}</p></div>'

def tips_ul(items):
    return '<ul class="tips">' + "".join(f"<li>{esc(t)}</li>" for t in items) + "</ul>"

def faq_block(faqs):
    h = '<section class="faq"><h2>Frequently asked questions</h2>' + "".join(
        f"<details><summary>{esc(q)}</summary><p>{esc(an)}</p></details>" for q, an in faqs) + "</section>"
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": an}} for q, an in faqs]}
    s = '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False).replace("</", "<\\/") + "</script>"
    return h, s

def hero(crumbs, h1, intro, extra=""):
    items = "".join(f"<li>{a(h, t) if h else esc(t)}</li>" for t, h in crumbs)
    return (f'<section class="hero"><div class="container"><nav class="breadcrumb" aria-label="Breadcrumb"><ol>{items}</ol></nav>'
            f"<h1>{esc(h1)}</h1><p>{esc(intro)}</p>{extra}</div></section>")

FINDER = ('<form class="finder" data-finder autocomplete="off"><div class="f-mode"><label for="fm">I want</label>'
          '<select id="fm" name="mode">{opts}</select></div>'
          '<div class="f-from"><label for="ff">From</label><input id="ff" name="from" placeholder="From (city or town)" autocomplete="off"></div>'
          '<div class="f-to"><label for="ft">To</label><input id="ft" name="to" placeholder="To (city or town)" autocomplete="off"></div>'
          '<button class="btn btn-aff" type="submit">Search flights</button><p class="finder-msg" role="status"></p></form>'
          '')
def finder(default="flights"):
    modes = [("flights", "Flights"), ("trains", "Trains"), ("buses", "Buses & Coaches"), ("tours", "Tours"),
             ("packages", "Holiday Packages"), ("taxi", "Taxi & Transfers")]
    opts = "".join(f'<option value="{k}"{" selected" if k == default else ""}>{esc(v)}</option>' for k, v in modes)
    return FINDER.replace("{opts}", opts)

def trim(s, n):
    s = re.sub(r"\s+", " ", s).strip()
    if len(s) <= n: return s
    cut = s[:n - 1].rsplit(" ", 1)[0].rstrip(",;:-")
    return cut + "…"

def render(fname, title, desc, keywords, body, kind, faqs=None, finder_on=False, extra_head=""):
    schema = ""
    if faqs:
        fh, schema = faq_block(faqs)
        body = body.replace("<!--FAQ-->", fh)
    kw = ", ".join(dict.fromkeys(k.strip() for k in keywords if k.strip()))
    scripts = '<script src="assets/js/places-data.js"></script>\n<script src="assets/js/search-cities.js"></script>\n' if finder_on else ""
    doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(trim(desc, 160))}">
<meta name="keywords" content="{esc(kw)}">
<meta name="robots" content="index,follow,max-snippet:-1,max-image-preview:large">
<link rel="icon" href="assets/img/logo.svg" type="image/svg+xml">
<link rel="stylesheet" href="assets/css/style.css">
{schema}{extra_head}
</head>
<body>
<div id="site-header"></div>
<main>
{body}
</main>
<div id="site-footer"></div>
<div id="site-bottombar"></div>
<script src="assets/js/config.js"></script>
{scripts}<script src="assets/js/main.js"></script>
</body>
</html>
"""
    with open(os.path.join(ROOT, fname), "w", encoding="utf-8") as f:
        f.write(doc)
    PAGES[fname] = {"title": title, "kind": kind}
