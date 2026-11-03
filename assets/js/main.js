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
    /* Type-ahead over every UK and US place name (guide places first). */
    var ALL = null;
    function buildAll() {
      if (ALL) return ALL;
      ALL = []; var seen = {};
      P.forEach(function (p) { var k = p[1].toLowerCase(); seen[k] = 1; ALL.push([p[1], k]); });
      var S = window.TRAVEL_SEARCH || {};
      ["UK", "US"].forEach(function (c) {
        var regs = S[c] || {};
        Object.keys(regs).forEach(function (r) {
          regs[r].forEach(function (n) { var l = n + ", " + r, k = l.toLowerCase(); if (!seen[k]) { seen[k] = 1; ALL.push([l, k]); } });
        });
      });
      return ALL;
    }
    function suggest(q) {
      q = q.trim().toLowerCase();
      if (q.length < 1) return [];
      var all = buildAll(), pre = [], inc = [], i, k;
      for (i = 0; i < all.length && pre.length < 10; i++) { k = all[i][1]; if (k.indexOf(q) === 0) pre.push(all[i][0]); }
      if (pre.length < 10 && q.length > 1) {
        for (i = 0; i < all.length && inc.length < 10 - pre.length; i++) { k = all[i][1]; if (k.indexOf(q) > 0) inc.push(all[i][0]); }
      }
      return pre.concat(inc);
    }
    function attachSuggest(input) {
      var box = document.createElement("ul"); box.className = "ac-list"; box.setAttribute("role", "listbox"); box.hidden = true;
      input.parentNode.appendChild(box);
      var items = [], cur = -1;
      function hide() { box.hidden = true; cur = -1; }
      function mark() { var li = box.children; for (var j = 0; j < li.length; j++) li[j].className = j === cur ? "on" : ""; }
      function pickIt(v) { input.value = v; hide(); }
      function show() {
        items = suggest(input.value);
        box.innerHTML = items.map(function (t) { return '<li role="option">' + esc(t) + "</li>"; }).join("");
        box.hidden = !items.length; cur = -1;
      }
      input.addEventListener("input", show);
      input.addEventListener("focus", function () { if (input.value) show(); });
      input.addEventListener("blur", function () { setTimeout(hide, 150); });
      input.addEventListener("keydown", function (e) {
        if (box.hidden) return;
        if (e.key === "ArrowDown") { e.preventDefault(); cur = (cur + 1) % items.length; mark(); }
        else if (e.key === "ArrowUp") { e.preventDefault(); cur = (cur <= 0 ? items.length : cur) - 1; mark(); }
        else if (e.key === "Enter" && cur >= 0) { e.preventDefault(); pickIt(items[cur]); }
        else if (e.key === "Escape") hide();
      });
      box.addEventListener("mousedown", function (e) { var li = e.target.closest("li"); if (li) { e.preventDefault(); pickIt(li.textContent); } });
    }
    attachSuggest(from); attachSuggest(to);
    function clean(t) { return t.trim().replace(/,\s*[^,]+$/, ""); }
    function find(t) {
      t = (t || "").trim().toLowerCase();
      if (!t) return null;
      for (var i = 0; i < P.length; i++) if (P[i][1].toLowerCase() === t) return P[i];
      for (i = 0; i < P.length; i++) if (P[i][0].toLowerCase() === t) return P[i];
      return null;
    }
    var routeModes = { flights: 1, trains: 1, buses: 1 };
    var prefix = { tours: "tours-in-", packages: "holiday-packages-", taxi: "taxi-in-" };
    var btnLabel = { flights: "Search flights", trains: "Search trains", buses: "Search buses", tours: "Search tours", packages: "Search packages", taxi: "Search taxis" };
    var btn = f.querySelector("button[type=submit]");
    function slug(t) { return clean(t).toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, ""); }
    function sync() {
      var isRoute = !!routeModes[mode.value];
      fromWrap.hidden = !isRoute;
      to.placeholder = isRoute ? "To (city or town)" : "City or town";
      btn.textContent = btnLabel[mode.value] || "Search";
      msg.textContent = "";
    }
    mode.addEventListener("change", sync);
    sync();
    f.addEventListener("submit", function (e) {
      e.preventDefault();
      var m = mode.value, a = find(from.value), b = find(to.value);
      if (routeModes[m] && !from.value.trim()) { msg.textContent = "Please choose where you are travelling from."; return; }
      if (!to.value.trim()) { msg.textContent = "Please choose a destination."; return; }
      var ds = routeModes[m]
        ? { from: a ? a[0] : clean(from.value), to: b ? b[0] : clean(to.value), fromCode: a ? a[3] : "", toCode: b ? b[3] : "", fromSlug: a ? a[2] : slug(from.value), toSlug: b ? b[2] : slug(to.value) }
        : { city: b ? b[0] : clean(to.value), cityCode: b ? b[3] : "", citySlug: b ? b[2] : slug(to.value) };
      var href = affHref(m, ds);
      if (!href || href === "#") { msg.textContent = "The partner link for this category is not set yet."; return; }
      var guide = "";
      if (routeModes[m] && a && b && sets[m] && sets[m][a[2] + "-to-" + b[2]]) guide = m + "-" + a[2] + "-to-" + b[2] + ".html";
      else if (!routeModes[m] && b) guide = prefix[m] + b[2] + ".html";
      msg.innerHTML = "Opening our partner's search" + (guide ? ' &middot; <a href="' + guide + '">read our guide</a>' : "") + "&hellip;";
      var w = (C.openInNewTab !== false) ? window.open(href, "_blank") : null;
      if (w) { try { w.opener = null; } catch (err) {} } else location.href = href;
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
