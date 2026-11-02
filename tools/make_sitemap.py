#!/usr/bin/env python3
"""Build sitemap.xml and robots.txt.  Usage: python3 tools/make_sitemap.py [https://your-site-url]"""
import os, re, sys, glob, datetime
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
url = sys.argv[1] if len(sys.argv) > 1 else None
if not url:
    m = re.search(r'siteUrl:\s*"([^"]+)"', open(os.path.join(ROOT, "assets/js/config.js"), encoding="utf-8").read())
    url = m.group(1) if m else "https://example.com"
url = url.rstrip("/")
today = datetime.date.today().isoformat()
def prio(f):
    if f == "index.html": return "1.0", "weekly"
    if f in ("flights.html", "trains.html", "buses.html", "tours.html", "holiday-packages.html", "taxi.html", "destinations.html", "travel-uk.html", "travel-usa.html"): return "0.9", "weekly"
    if f.startswith(("flights-", "trains-", "buses-")) and "-to-" in f and f.count("-to-") == 1 and not f.endswith(("uk.html", "usa.html")): return "0.6", "monthly"
    if f.startswith(("travel-", "visit-")): return "0.7", "monthly"
    if f in ("disclaimer.html", "affiliate-disclosure.html", "privacy-policy.html", "cookie-policy.html", "terms.html", "copyright.html"): return "0.3", "yearly"
    return "0.5", "monthly"
files = sorted(os.path.basename(p) for p in glob.glob(os.path.join(ROOT, "*.html")))
files = [f for f in files if f != "404.html"]
out = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for f in files:
    loc = url + "/" + ("" if f == "index.html" else f)
    pr, ch = prio(f)
    out.append(f"  <url><loc>{loc}</loc><lastmod>{today}</lastmod><changefreq>{ch}</changefreq><priority>{pr}</priority></url>")
out.append("</urlset>")
open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write("\n".join(out) + "\n")
open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8").write(f"User-agent: *\nAllow: /\n\nSitemap: {url}/sitemap.xml\n")
print("sitemap.xml:", len(files), "URLs ->", url)
