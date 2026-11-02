/*
 * ONE PLACE TO EDIT: brand, logo and affiliate links for EVERY page.
 * ---------------------------------------------------------------
 * 1) brandName / tagline / logoImage  -> header, footer, page titles, schema
 * 2) affiliates.<category>.url        -> general link for that category
 * 3) affiliates.<category>.deepLink   -> optional route/city link. Leave "" to always use `url`.
 *
 * Tokens you can use inside deepLink (values are URL-encoded automatically):
 *   {from} {to}            place names, e.g. London, New York
 *   {fromCode} {toCode}    city or airport codes, e.g. LON, NYC
 *   {fromSlug} {toSlug}    url-friendly names, e.g. london, new-york
 *   {city} {cityCode} {citySlug}   used on single-city pages (tours, packages, taxi)
 *
 * Example: "https://partner.example/flights?origin={fromCode}&destination={toCode}&ref=MY_ID"
 *
 * The example.com links below are PLACEHOLDERS. Replace them with your own affiliate links.
 */
window.SITE_CONFIG = {
  brandName: "TicketBooking",
  tagline: "Independent guides to flights, trains, coaches, tours and transfers across the UK and USA",
  logoImage: "assets/img/logo.svg",   // set "" to show only the brand name
  showBrandText: true,                // false = logo image only

  // Your live address, no trailing slash. Used for canonical URLs, Open Graph and schema.
  siteUrl: "https://your-username.github.io/your-repo",

  affiliates: {
    flights:  { label: "Flights",          url: "https://example.com/flights?ref=YOUR_ID",  deepLink: "" },
    trains:   { label: "Trains",           url: "https://example.com/trains?ref=YOUR_ID",   deepLink: "" },
    buses:    { label: "Buses & Coaches",  url: "https://example.com/buses?ref=YOUR_ID",    deepLink: "" },
    tours:    { label: "Tours",            url: "https://example.com/tours?ref=YOUR_ID",    deepLink: "" },
    packages: { label: "Holiday Packages", url: "https://example.com/packages?ref=YOUR_ID", deepLink: "" },
    taxi:     { label: "Taxi & Transfers", url: "https://example.com/taxi?ref=YOUR_ID",     deepLink: "" }
  },

  openInNewTab: true,

  // Shown in the fixed bottom bar and in the disclosure boxes.
  disclosure: "This site contains affiliate links. If you book through them we may earn a commission at no extra cost to you. We do not sell tickets ourselves.",

  // Optional. The site shows no phone, WhatsApp, form or email. If your privacy law
  // obligations need a contact method, put it here (for example a postal address or
  // a contact page URL) and it will appear on the privacy page. Leave "" to hide.
  legalContact: "",

  // Shown on legal pages.
  lastUpdated: "1 November 2026"
};
