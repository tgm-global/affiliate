/* Shared behaviour for every page: header, bottom bar, footer, affiliate links, finder, schema. */
(function () {
  "use strict";
  var C = window.SITE_CONFIG || {};
  var AFF = C.affiliates || {};
  var BRAND = C.brandName || "Travel Guide";

  function esc(s) {
    return String(s == null ? "" : s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }
  function file() {
    var f = location.pathname.split("/").pop();
    return f || "index.html";
  }
  var base = String(C.siteUrl || "").replace(/\/+$/, "");
  function abs(href) {
    if (/^https?:/i.test(href)) return href;
    return base + "/" + href.replace(/^\.?\//, "");
  }

  /* ---------- Navigation data ---------- */
  var CATS = [
    ["flights", "Flights", "flights.html"],
    ["trains", "Trains", "trains.html"],
    ["buses", "Buses & Coaches", "buses.html"],
    ["tours", "Tours", "tours.html"],
    ["packages", "Holiday Packages", "holiday-packages.html"],
    ["taxi", "Taxi & Transfers", "taxi.html"]
  ];
  var NAV = [
    ["flights.html", "Flights"], ["trains.html", "Trains"], ["buses.html", "Buses"],
    ["tours.html", "Tours"], ["holiday-packages.html", "Packages"], ["taxi.html", "Taxi"],
    ["destinations.html", "Destinations"]
  ];
  var POPULAR = [
    ["flights-london-to-new-york.html", "London to New York flights"],
    ["flights-new-york-to-london.html", "New York to London flights"],
    ["flights-new-york-to-los-angeles.html", "New York to Los Angeles flights"],
    ["flights-london-to-edinburgh.html", "London to Edinburgh flights"],
    ["trains-london-to-manchester.html", "London to Manchester trains"],
    ["trains-london-to-edinburgh.html", "London to Edinburgh trains"],
    ["trains-new-york-to-washington-dc.html", "New York to Washington, DC trains"],
    ["buses-london-to-birmingham.html", "London to Birmingham coaches"],
    ["buses-new-york-to-boston.html", "New York to Boston buses"]
  ];
  var LEGAL = [
    ["disclaimer.html", "Disclaimer"], ["affiliate-disclosure.html", "Affiliate Disclosure"],
    ["privacy-policy.html", "Privacy Policy"], ["cookie-policy.html", "Cookie Policy"],
    ["terms.html", "Terms of Use"], ["copyright.html", "Copyright"], ["sitemap.html", "Site Map"]
  ];

  /* ---------- Affiliate links ---------- */
  function fill(tpl, d) {
    return tpl.replace(/\{(\w+)\}/g, function (m, k) {
      var v = d[k];
      return v == null ? "" : encodeURIComponent(v);
    });
  }
  function affHref(cat, ds) {
    var a = AFF[cat];
    if (!a || (!a.url && !a.deepLink)) return "#";
    var d = {
      from: ds.from, to: ds.to || ds.city, fromCode: ds.fromCode, toCode: ds.toCode || ds.cityCode,
      fromSlug: ds.fromSlug, toSlug: ds.toSlug || ds.citySlug,
      city: ds.city || ds.to, cityCode: ds.cityCode || ds.toCode, citySlug: ds.citySlug || ds.toSlug
    };
    var hasData = d.from || d.to || d.city;
    if (a.deepLink && hasData) return fill(a.deepLink, d);
    return a.url || "#";
  }
  function decorate(el, cat, ds) {
    var href = affHref(cat, ds);
    el.setAttribute("href", href);
    el.setAttribute("rel", "sponsored nofollow noopener");
    if (C.openInNewTab !== false && href !== "#") el.setAttribute("target", "_blank");
  }
  function applyAffiliates(root) {
    var els = (root || document).querySelectorAll("[data-aff]");
    for (var i = 0; i < els.length; i++) decorate(els[i], els[i].getAttribute("data-aff"), els[i].dataset);
  }

  /* ---------- Header / bottom bar / footer ---------- */
  function logoHtml() {
    var h = "";
    if (C.logoImage) h += '<img class="brand-logo" src="' + esc(C.logoImage) + '" alt="' + esc(BRAND) + ' logo" width="36" height="36">';
    if (C.showBrandText !== false || !C.logoImage) h += '<span class="brand-name">' + esc(BRAND) + "</span>";
    return h;
  }
  function buildHeader() {
    var host = document.getElementById("site-header");
    if (!host) return;
    var cur = file();
    var items = NAV.map(function (n) {
      return '<li><a href="' + n[0] + '"' + (n[0] === cur ? ' class="active" aria-current="page"' : "") + ">" + esc(n[1]) + "</a></li>";
    }).join("");
    host.className = "site-header";
    host.innerHTML =
      '<div class="container hbar">' +
      '<a class="brand" href="index.html" aria-label="' + esc(BRAND) + ' home">' + logoHtml() + "</a>" +
      '<button class="menu-btn" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="mainNav"><span></span></button>' +
      '<nav class="main-nav" id="mainNav" aria-label="Main"><ul>' + items + "</ul></nav></div>";
    var btn = host.querySelector(".menu-btn");
    function setOpen(o) {
      host.classList.toggle("nav-open", o);
      document.body.classList.toggle("nav-lock", o);
      btn.setAttribute("aria-expanded", o ? "true" : "false");
      btn.setAttribute("aria-label", o ? "Close menu" : "Open menu");
    }
    btn.addEventListener("click", function () { setOpen(!host.classList.contains("nav-open")); });
    host.querySelector("nav").addEventListener("click", function (e) { if (e.target.closest("a")) setOpen(false); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") setOpen(false); });
    window.addEventListener("resize", function () { if (window.innerWidth > 1080) setOpen(false); });
  }
  function buildBottomBar() {
    var host = document.getElementById("site-bottombar");
    if (!host) return;
    host.className = "bottombar";
    var chips = CATS.map(function (c) {
      return '<a class="chip" data-aff="' + c[0] + '" href="#">' + esc(c[1]) + "</a>";
    }).join("");
    host.innerHTML =
      '<div class="container bb"><a class="bb-note" href="affiliate-disclosure.html"><strong>Ad disclosure:</strong> <span class="bb-long">partner links, we may earn a commission.</span><span class="bb-short">partner links.</span></a>' +
      '<div class="bb-chips" role="navigation" aria-label="Book with partners">' + chips + "</div></div>";
  }
  function buildFooter() {
    var host = document.getElementById("site-footer");
    if (!host) return;
    host.className = "site-footer";
    var col = function (title, rows) {
      return '<div class="fcol"><h3>' + esc(title) + "</h3><ul>" + rows.map(function (r) {
        return '<li><a href="' + r[0] + '">' + esc(r[1]) + "</a></li>";
      }).join("") + "</ul></div>";
    };
    var explore = [["index.html", "Home"], ["destinations.html", "All destinations"], ["travel-uk.html", "Travel in the UK"],
      ["travel-usa.html", "Travel in the USA"], ["how-it-works.html", "How it works"], ["about.html", "About us"]];
    host.innerHTML =
      '<div class="container">' +
      '<div class="fgrid">' +
      '<div class="fcol fbrand"><a class="brand" href="index.html">' + logoHtml() + "</a><p>" + esc(C.tagline || "") + "</p>" +
      '<p class="fdisc">' + esc(C.disclosure || "") + "</p></div>" +
      col("Book travel", CATS.map(function (c) { return [c[2], c[1]]; })) +
      col("Popular routes", POPULAR) +
      col("Explore", explore) +
      col("Legal", LEGAL) +
      "</div>" +
      '<div class="fbottom"><p>&copy; ' + new Date().getFullYear() + " " + esc(BRAND) + ". All rights reserved.</p>" +
      '<p>Prices, availability and booking terms are set by our partners. Always check details before you pay.</p></div></div>';
  }

  /* ---------- Head: title, canonical, social, schema ---------- */
  function setMeta(sel, attr, key, val) {
    var m = document.head.querySelector(sel);
    if (!m) { m = document.createElement("meta"); m.setAttribute(attr, key); document.head.appendChild(m); }
    m.setAttribute("content", val);
  }
  function buildHead() {
    var page = file();
    var h1 = document.querySelector("h1");
    var baseTitle = document.title.replace(/\s*\|\s*.*$/, "");
    var desc = (document.head.querySelector('meta[name="description"]') || {}).content || "";
    document.title = page === "index.html" ? (baseTitle + " | " + BRAND) : (baseTitle + " | " + BRAND);
    var url = abs(page === "index.html" ? "" : page);
    var link = document.head.querySelector('link[rel="canonical"]');
    if (!link) { link = document.createElement("link"); link.rel = "canonical"; document.head.appendChild(link); }
    link.href = url;
    setMeta('meta[property="og:title"]', "property", "og:title", document.title);
    setMeta('meta[property="og:description"]', "property", "og:description", desc);
    setMeta('meta[property="og:url"]', "property", "og:url", url);
    setMeta('meta[property="og:type"]', "property", "og:type", "website");
    setMeta('meta[property="og:site_name"]', "property", "og:site_name", BRAND);
    setMeta('meta[name="twitter:card"]', "name", "twitter:card", "summary");
    if (C.logoImage) setMeta('meta[property="og:image"]', "property", "og:image", abs(C.logoImage));
    var fav = document.head.querySelector('link[rel="icon"]');
    if (!fav && C.logoImage) { fav = document.createElement("link"); fav.rel = "icon"; fav.href = C.logoImage; document.head.appendChild(fav); }

    var graph = [
      { "@type": "WebSite", name: BRAND, url: abs(""), description: C.tagline || "" },
      { "@type": "Organization", name: BRAND, url: abs(""), logo: C.logoImage ? abs(C.logoImage) : undefined }
    ];
    var crumbs = document.querySelectorAll(".breadcrumb li");
    if (crumbs.length) {
      var items = [];
      for (var i = 0; i < crumbs.length; i++) {
        var a = crumbs[i].querySelector("a");
        items.push({ "@type": "ListItem", position: i + 1, name: crumbs[i].textContent.trim(), item: a ? abs(a.getAttribute("href")) : url });
      }
      graph.push({ "@type": "BreadcrumbList", itemListElement: items });
    }
    var s = document.createElement("script");
    s.type = "application/ld+json";
    s.text = JSON.stringify({ "@context": "https://schema.org", "@graph": graph });
    document.head.appendChild(s);
    void h1;
  }

  /* ---------- Text placeholders ---------- */
  function fillText() {
    var nodes = document.querySelectorAll("[data-brand]");
    for (var i = 0; i < nodes.length; i++) nodes[i].textContent = BRAND;
    nodes = document.querySelectorAll("[data-cfg]");
    for (i = 0; i < nodes.length; i++) {
      var v = C[nodes[i].getAttribute("data-cfg")];
      var w = nodes[i].closest("[data-wrap]");
      if (v) { nodes[i].textContent = v; if (w) w.hidden = false; }
    }
    nodes = document.querySelectorAll("[data-disclosure]");
    for (i = 0; i < nodes.length; i++) if (C.disclosure) nodes[i].textContent = C.disclosure;
    nodes = document.querySelectorAll("[data-year]");
    for (i = 0; i < nodes.length; i++) nodes[i].textContent = new Date().getFullYear();
  }

  /* ---------- Route / destination finder ---------- */
  function initFinder() {
    var f = document.querySelector("[data-finder]");
    if (!f) return;
    var P = window.TRAVEL_PLACES || [];  // [name, label, slug, code, country]
    var R = window.TRAVEL_ROUTES || {};  // {flights:[ "a-to-b" ], trains:[], buses:[]}
    var sets = {};
    Object.keys(R).forEach(function (k) { sets[k] = {}; R[k].forEach(function (s) { sets[k][s] = 1; }); });
    var mode = f.querySelector("[name=mode]"), from = f.querySelector("[name=from]"),
      to = f.querySelector("[name=to]"), msg = f.querySelector(".finder-msg"), fromWrap = f.querySelector(".f-from");
    var dl = document.getElementById("place-list");
    if (dl) dl.innerHTML = P.map(function (p) { return '<option value="' + esc(p[1]) + '">'; }).join("");
    function find(t) {
      t = (t || "").trim().toLowerCase();
      if (!t) return null;
      for (var i = 0; i < P.length; i++) if (P[i][1].toLowerCase() === t) return P[i];
      for (i = 0; i < P.length; i++) if (P[i][0].toLowerCase() === t) return P[i];
      return null;
    }
    var routeModes = { flights: 1, trains: 1, buses: 1 };
    var prefix = { tours: "tours-in-", packages: "holiday-packages-", taxi: "taxi-in-" };
    function sync() {
      var isRoute = !!routeModes[mode.value];
      fromWrap.hidden = !isRoute;
      to.placeholder = isRoute ? "To (city or town)" : "City or town";
      msg.textContent = "";
    }
    mode.addEventListener("change", sync);
    sync();
    f.addEventListener("submit", function (e) {
      e.preventDefault();
      var m = mode.value, a = find(from.value), b = find(to.value), cat = m;
      if (!to.value.trim()) { msg.textContent = "Please enter a destination."; return; }
      if (routeModes[m]) {
        if (!from.value.trim()) { msg.textContent = "Please enter where you are travelling from."; return; }
        if (a && b && a !== b && sets[m] && sets[m][a[2] + "-to-" + b[2]]) { location.href = m + "-" + a[2] + "-to-" + b[2] + ".html"; return; }
      } else if (b) { location.href = prefix[m] + b[2] + ".html"; return; }
      var ds = routeModes[m]
        ? { from: a ? a[0] : from.value.trim(), to: b ? b[0] : to.value.trim(), fromCode: a ? a[3] : "", toCode: b ? b[3] : "", fromSlug: a ? a[2] : "", toSlug: b ? b[2] : "" }
        : { city: b ? b[0] : to.value.trim(), cityCode: b ? b[3] : "", citySlug: b ? b[2] : "" };
      var href = affHref(cat, ds);
      msg.textContent = "We have no guide page for this one yet, so we are opening our partner's search in a new tab.";
      if (href && href !== "#") window.open(href, "_blank", "noopener");
    });
  }

  /* ---------- Init ---------- */
  function init() {
    buildHeader();
    buildBottomBar();
    buildFooter();
    fillText();
    buildHead();
    applyAffiliates(document);
    initFinder();
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
