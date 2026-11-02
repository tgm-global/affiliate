# Travel Affiliate Website (UK and USA)

Static site, no build step, ready for GitHub Pages. About 2,860 pages: flights, trains and bus/coach route guides, plus travel, tours, holiday-package and taxi pages for 163 UK and US cities and towns.

## Change brand, logo and affiliate links in ONE place
Edit `assets/js/config.js`:
- `brandName`, `tagline`, `logoImage` (replace `assets/img/logo.svg` or point to your own file)
- `affiliates.flights / trains / buses / tours / packages / taxi`: each has a `url` and an optional `deepLink` with tokens `{from} {to} {fromCode} {toCode} {fromSlug} {toSlug} {city} {cityCode} {citySlug}`
- `siteUrl`, `disclosure`, `legalContact` (optional, empty by default)

The example.com links are placeholders. Replace them with your real affiliate links.

## Go live on GitHub Pages
1. Upload everything in this folder to a repository root.
2. Settings > Pages > Deploy from a branch > `main` / root.
3. Set `siteUrl` in `config.js`, then run `python3 tools/make_sitemap.py` (or pass your URL) to rebuild `sitemap.xml` and `robots.txt`. Submit the sitemap in Google Search Console.

## Add places or routes
Edit `tools/places_data.py` (places, hubs, route limits), then run:
```
python3 tools/generate_site.py
python3 tools/make_sitemap.py
```
`generate_site.py` rebuilds all `.html` pages in the root, so do not hand-edit them.

## Notes
- No phone, WhatsApp, email or query form. The search box only opens a page or a partner link.
- Affiliate links use `rel="sponsored nofollow noopener"`. Disclosure appears on every page.
- No prices or ratings are published. Times and distances are labelled estimates.
