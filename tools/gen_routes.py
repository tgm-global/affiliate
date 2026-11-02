"""Route pages (flights / trains / buses) and city pages (travel / tours / packages / taxi)."""
from gen_common import *

KIND_LABEL = {"flights": "Flights", "trains": "Trains", "buses": "Buses & Coaches"}
KIND_HUB = {"flights": "flights.html", "trains": "trains.html", "buses": "buses.html"}

def country_list_file(kind, a, b):
    if kind == "flights" and a["country"] != b["country"]:
        return "flights-uk-to-usa.html" if a["country"] == "UK" else "flights-usa-to-uk.html"
    return f"{kind}-{'uk' if a['country'] == 'UK' else 'usa'}.html"

def country_list_label(kind, a, b):
    if kind == "flights" and a["country"] != b["country"]:
        return "UK to USA flights" if a["country"] == "UK" else "USA to UK flights"
    return f"{KIND_LABEL[kind]} in the {'UK' if a['country'] == 'UK' else 'USA'}"

def air_sentence(p):
    if p["own"]:
        return f"{p['disp']} is served by {p['air']}."
    return f"{p['disp']} does not have a major commercial airport of its own, so most travellers fly via {p['short_air']}."

def others_from(kind, p, skip=None, n=8):
    out = [(rfile(kind, x, y), f"{KIND_LABEL[kind][:-1] if kind != 'buses' else 'Bus'} {x['disp']} to {y['disp']}") for x, y, _ in RT[kind] if x is p and y is not skip]
    return out

def label(kind, x, y):
    noun = {"flights": "Flights", "trains": "Trains", "buses": "Buses"}[kind]
    return f"{x['disp']} to {y['disp']} {noun.lower()}"

def related_routes(kind, a_, b_, n=8):
    frm = [(rfile(kind, x, y), label(kind, x, y)) for x, y, _ in RT[kind] if x is a_ and y is not b_]
    to = [(rfile(kind, x, y), label(kind, x, y)) for x, y, _ in RT[kind] if y is b_ and x is not a_]
    frm = pick_n(frm, n, kind, a_["slug"], "f") if len(frm) > n else frm
    to = pick_n(to, n, kind, b_["slug"], "t") if len(to) > n else to
    return frm, to

FLIGHT_TIPS = [
    "Compare nearby airports. Fares and ground-transport time can differ between the airports around {A} and {B}, so check each before you decide.",
    "Check the baggage rules. Hand-luggage-only fares are common on shorter routes, and checked bags can cost extra.",
    "Read the fare conditions for changes and refunds before you pay. Lower fares are usually less flexible.",
    "Allow time for the journey between the airport and your final stop in {B}, especially if you arrive late at night.",
    "Midweek and off-peak departures are often quieter than Fridays and Sundays, although prices vary with season and demand.",
    "Make sure the name on your booking matches your photo ID or passport exactly.",
    "Book earlier for school holidays, public holidays and major events in {A} or {B}.",
    "Compare a return fare with two one-way fares. The best option depends on your plans.",
    "Turn on fare or schedule alerts with your booking partner so you hear about changes early.",
    "Check the full journey time, including airport transfers and security, before you decide that flying beats other options.",
]
TRANS_TIPS_UK_US = [
    "Check US entry requirements well before you travel. Depending on your nationality you may need an ESTA or a visa.",
    "Check that your passport is valid for the whole stay, and read the airline's rules on documents for transatlantic flights.",
    "Plan for jet lag. Westbound daytime flights often suit a first day of sightseeing, while overnight flights suit people who can sleep on board.",
]
TRANS_TIPS_US_UK = [
    "Check UK entry requirements before you travel. Many visitors need a UK Electronic Travel Authorisation (ETA) or a visa, depending on nationality.",
    "Check that your passport is valid for the whole stay, and read the airline's rules on documents for transatlantic flights.",
    "Plan for jet lag. Overnight eastbound flights usually land early in the morning, so think about how you will spend your first day.",
]
TRAIN_TIPS_UK = [
    "Advance tickets are tied to a specific train and are often cheaper, while off-peak and anytime tickets are more flexible. Check the rules before you buy.",
    "Railcards can reduce fares for eligible travellers, so check whether one applies to you before you book.",
    "Splitting a journey into separate tickets can sometimes lower the cost. Read the conditions carefully because you must stay on the same train.",
    "Reserve a seat on busy long-distance trains, particularly on Fridays, Sundays and around holidays.",
    "Check for planned engineering work, which is more common at weekends and can add time or require a replacement bus.",
    "Look at which station you will arrive at in {B}. Large cities can have several, and the best one depends on where you are staying.",
    "Travelling off-peak is usually quieter and can be cheaper than commuter hours on weekdays.",
    "Keep your ticket or digital ticket available until you leave the arrival station, since gates and inspections can require it.",
]
TRAIN_TIPS_US = [
    "Check whether your train has reserved or unreserved coach seating, because this varies by route.",
    "Corridor routes with frequent departures are easier to plan than long-distance routes that may run once a day, so check the timetable first.",
    "Allow extra time for connections. Longer routes can run late, and a missed connection can be difficult on routes with limited service.",
    "Compare coach seats with business or sleeper options on overnight services if comfort matters more than cost.",
    "Check luggage allowances and carry-on rules before you travel, and label your bags.",
    "Look at which station you will arrive at in {B} and how you will reach your hotel or meeting from there.",
    "Booking earlier can help on popular routes and around holidays, since lower fare levels can sell out.",
    "Check whether a coach connection is included for part of the journey, as some rail itineraries use a bus link.",
]
BUS_TIPS_UK = [
    "Check where coaches stop in {A} and {B}. The coach station is often not the same place as the main railway station.",
    "Compare daytime and overnight services. Overnight journeys can be cheaper but you arrive tired and early.",
    "Allow for traffic. Coach journey times can change at busy times, especially on roads into large cities.",
    "Check luggage rules and any extra charge for large bags or oversized items.",
    "Book earlier for weekends, school holidays and events, since lower fares can sell out.",
    "Arrive at the stop early and keep your ticket or digital ticket ready to show the driver.",
    "Look for services with comfort features you need, such as power sockets, Wi-Fi or space for wheelchairs, because these vary by operator.",
]
BUS_TIPS_US = [
    "Check exactly where the bus departs and arrives in {A} and {B}. Some intercity services use curbside stops rather than a central terminal.",
    "Compare daytime and overnight services. Overnight trips can save a hotel night but you arrive tired.",
    "Allow for traffic and weather. Intercity journey times can change at busy times and on longer routes.",
    "Check luggage rules and any extra charge for additional or oversized bags.",
    "Book earlier for holiday weekends and events, since lower fares can sell out.",
    "Arrive at the stop early and keep your ticket or digital ticket ready to show the driver.",
    "Look for services with the comfort features you need, such as power sockets or Wi-Fi, because these vary by operator.",
]

def fill(s, A, B): return s.replace("{A}", A["disp"]).replace("{B}", B["disp"])

def route_page(kind, a_, b_, km):
    A, B = a_["disp"], b_["disp"]
    mi = fnum(miles(km)); kms = fnum(km)
    cross = a_["country"] != b_["country"]
    ds = ds_route(a_, b_)
    fname = rfile(kind, a_, b_)
    rev = (b_["slug"], a_["slug"]) in RS[kind]
    revlink = rfile(kind, b_, a_) if rev else None
    alt = {k: ((a_["slug"], b_["slug"]) in RS[k]) for k in ("flights", "trains", "buses") if k != kind}
    frm, to = related_routes(kind, a_, b_)
    parts = []
    if kind == "flights":
        lo, hi = flight_time(a_, b_, km)
        tt = drange(lo, hi)
        title = trim(f"{A} to {B} Flights: Airports, Times & Tips", 62)
        desc = f"Flying from {A} to {B}? See the {mi} mile route, typical flight time of {tt}, airports at both ends and booking tips, then check live options with our partner."
        kws = [f"{A} to {B} flights", f"flights from {A} to {B}", f"{A} to {B} flight tickets", f"{a_['code']} to {b_['code']} flights",
               f"book {A} to {B} flights", f"{A} to {B} airfare", f"{A} to {B} flight time", f"cheap flights {A} to {B}", f"{A} {B} air tickets"]
        phrase = "the fastest option" if km > 700 else ("a quick option" if km > 400 else "worth considering mainly when you are connecting to a longer trip")
        intro = pick([
            f"Looking for flights from {A} to {B}? This guide covers the {mi} mile ({kms} km) journey, the airports you can use at each end, how long the flight usually takes and what to check before you book.",
            f"The air route between {A} and {B} covers roughly {mi} miles. Below you will find typical flight times, the airports around both places and practical tips, followed by a button to our partner's live search for current schedules and fares.",
            f"Planning a trip from {A} to {B}? For a distance of about {kms} km, flying is {phrase}. Use this page to understand your airport options and travel time, then check live availability with our booking partner."],
            fname, "intro")
        fts = [(tt, "Typical flight time"), (f"{mi} mi / {kms} km", "Approximate distance"),
               (a_["code"] + " → " + b_["code"], "City or airport codes"), ("Partner search", "Live fares and schedules")]
        glance = pick([
            f"The straight-line distance between {A} and {B} is about {mi} miles. Allowing for taxiing, climbing and approach, airlines usually schedule a flight of {tt}, although the time on your ticket can be longer if you connect.",
            f"Expect a flight of {tt} for the {kms} km between {A} and {B}. Your door-to-door time is longer once you add travel to the airport, check-in, security and the journey from the arrival airport.",
            f"On the map, {A} and {B} are roughly {kms} km apart. A typical flying time is {tt}, but the total journey depends on how early you arrive, which airports you use and whether your flight is direct."],
            fname, "glance")
        parts.append(f"<h2>{esc(A)} to {esc(B)} at a glance</h2><p>{esc(glance)}</p>")
        parts.append(f"<h2>Airports for this route</h2><h3>Departing from {esc(A)}</h3><p>{esc(air_sentence(a_))}</p>"
                     f"<h3>Arriving in {esc(B)}</h3><p>{esc(air_sentence(b_))}</p>"
                     f"<p>When prices look similar, choose the airport that makes your onward journey simplest. Check transfer time as well as the fare.</p>")
        pool = FLIGHT_TIPS
        extra = (TRANS_TIPS_UK_US if a_["country"] == "UK" else TRANS_TIPS_US_UK) if cross else []
        tips = extra + [fill(t, a_, b_) for t in pick_n(pool, 5, fname, "tips")]
        parts.append(f"<h2>Tips for booking {esc(A)} to {esc(B)} flights</h2>{tips_ul(tips)}")
        options = []
        if alt["trains"]: options.append(f'a <a href="{rfile("trains", a_, b_)}">train from {esc(A)} to {esc(B)}</a>')
        if alt["buses"]: options.append(f'a <a href="{rfile("buses", a_, b_)}">coach from {esc(A)} to {esc(B)}</a>')
        if options:
            parts.append(f"<h2>Other ways to travel</h2><p>If you would rather stay on the ground, compare {' or '.join(options)}. Which is best depends on your budget, luggage and how much time you have.</p>")
        elif cross:
            parts.append(f"<h2>Other ways to travel</h2><p>Because {A} and {B} are on opposite sides of the Atlantic, flying is the practical option for nearly every traveller. Our hotel-and-flight guides can help if you want a package instead: see {a(cfile('packages', b_), 'holiday packages to ' + b_['disp'])}.</p>")
        else:
            parts.append(f"<h2>Other ways to travel</h2><p>At {kms} km, most travellers choose between flying and a long surface journey. We do not have a dedicated rail or coach guide for this pair, but you can browse {a(KIND_HUB['trains'], 'train guides')} and {a(KIND_HUB['buses'], 'bus and coach guides')} for related routes.</p>")
        faqs = [
            (f"How long is the flight from {A} to {B}?", f"A typical flight takes {tt} for the distance of about {kms} km. Actual time depends on the route flown, winds and any connection."),
            (f"Which airports can I use for {A} to {B}?", f"{air_sentence(a_)} {air_sentence(b_)}"),
            (f"Is there a direct flight from {A} to {B}?", "Whether a non-stop service operates depends on airlines and the season. The partner search shows current direct and connecting options for your dates."),
            (f"Can I travel from {A} to {B} another way?", ("Yes. " + " and ".join(["there is a train guide on this site" if alt["trains"] else "", "there is a coach guide on this site" if alt["buses"] else ""]).strip(" and") + ".") if (alt["trains"] or alt["buses"]) else "For most travellers on this route, flying is the practical option."),
            ("Do you sell the tickets?", "No. This website is an independent affiliate guide. When you click a booking button you go to a partner's website, where you complete the purchase."),
        ]
        cta_text = f"Search {A} to {B} flights"
        cat = "flights"
    elif kind == "trains":
        lo, hi = train_time(a_, b_, km)
        tt = drange(lo, hi)
        uk = a_["country"] == "UK"
        title = trim(f"{A} to {B} Train: Journey Time, Tips & Tickets", 62)
        desc = f"Taking the train from {A} to {B}? See the {mi} mile route, typical journey time of {tt}, planning tips and how to check current tickets with our partner."
        kws = [f"{A} to {B} train", f"train from {A} to {B}", f"{A} to {B} train tickets", f"{A} to {B} rail", f"book {A} to {B} train",
               f"{A} to {B} train time", f"{A} to {B} by train", f"cheap train tickets {A} to {B}", f"{A} {B} railway"]
        intro = pick([
            f"Travelling by train from {A} to {B}? This guide explains the {mi} mile ({kms} km) route, a realistic journey-time range, how to choose between ticket types and what to check before you travel.",
            f"Rail is a comfortable way to cover the {kms} km between {A} and {B}. Read the planning notes below, then use our partner's search for current timetables and fares.",
            f"Here is what to know before taking a train from {A} to {B}: roughly {mi} miles, typically {tt}, and a few practical tips for choosing tickets and avoiding delays."], fname, "intro")
        fts = [(tt, "Typical journey time"), (f"{mi} mi / {kms} km", "Approximate distance"),
               ("Rail", "Mode of travel"), ("Partner search", "Live timetables and fares")]
        ne = (a_["name"] in NE_SET and b_["name"] in NE_SET and not uk)
        extra_line = (" Both cities are on the Northeast Corridor, where trains run more frequently than on most other US routes." if ne else
                      (" This is a US route, so frequency can be much lower than in Great Britain. Check the timetable before you plan around a specific departure." if not uk else
                       " Great Britain has a dense rail network, so many pairs of large cities have frequent services, though some need a change of train."))
        glance = pick([
            f"The straight-line distance from {A} to {B} is about {mi} miles, but the railway is usually longer than the direct line. We estimate {tt} for the trip, which varies with the service, stops and any change.{extra_line}",
            f"For the roughly {kms} km between {A} and {B}, expect a journey of {tt}. Faster services stop less, and a journey with a change takes longer.{extra_line}",
            f"A train from {A} to {B} typically takes {tt}. These figures are estimates based on distance, so always confirm the timetable for your date.{extra_line}"], fname, "glance")
        parts.append(f"<h2>{esc(A)} to {esc(B)} by train at a glance</h2><p>{esc(glance)}</p>")
        parts.append(f"<h2>Stations and getting around</h2><p>{esc(A)}: large places can have more than one station, so check which one your booking uses. {esc(B)}: plan how you will get from the arrival station to your final stop, whether by foot, local transport or {a(cfile('taxi', b_), 'taxi in ' + b_['disp'])}.</p>")
        pool = TRAIN_TIPS_UK if uk else TRAIN_TIPS_US
        tips = [fill(t, a_, b_) for t in pick_n(pool, 5, fname, "tips")]
        parts.append(f"<h2>Tips for {esc(A)} to {esc(B)} train tickets</h2>{tips_ul(tips)}")
        options = []
        if alt["flights"]: options.append(f'a <a href="{rfile("flights", a_, b_)}">flight from {esc(A)} to {esc(B)}</a>')
        if alt["buses"]: options.append(f'a <a href="{rfile("buses", a_, b_)}">coach from {esc(A)} to {esc(B)}</a>')
        parts.append("<h2>Other ways to travel</h2><p>" + (f"If rail does not suit your plans, compare {' or '.join(options)}." if options else f"Browse our {a('flights.html', 'flight guides')} and {a('buses.html', 'bus guides')} if you want to compare other modes.") + "</p>")
        faqs = [
            (f"How long does the train from {A} to {B} take?", f"We estimate {tt} for about {kms} km. Your actual time depends on the service, number of stops and any change."),
            (f"Is there a direct train from {A} to {B}?", "That depends on the timetable. The partner search shows direct and connecting options for the date you choose."),
            (f"How can I find the best ticket for {A} to {B}?", "Compare ticket types, travel at quieter times if you can, and book early where lower fares are released in advance. Always read the change and refund rules."),
            (f"Can I travel from {A} to {B} another way?", "Yes. " + ("There is " + ("a flight guide" if alt["flights"] else "") + (" and " if alt["flights"] and alt["buses"] else "") + ("a coach guide" if alt["buses"] else "") + " on this site." if (alt["flights"] or alt["buses"]) else "See our flight and bus guides for related routes.")),
            ("Do you sell the tickets?", "No. This website is an independent affiliate guide. When you click a booking button you go to a partner's website, where you complete the purchase."),
        ]
        cta_text = f"Check {A} to {B} train tickets"
        cat = "trains"
    else:
        lo, hi = bus_time(a_, b_, km)
        tt = drange(lo, hi)
        uk = a_["country"] == "UK"
        word = "coach" if uk else "bus"
        title = trim(f"{A} to {B} {word.title()}: Times, Stops & Tips", 62)
        desc = f"Booking a {word} from {A} to {B}? See the {mi} mile route, typical journey time of {tt}, where to check stops and how to find current tickets with our partner."
        kws = [f"{A} to {B} bus", f"{A} to {B} coach", f"bus from {A} to {B}", f"{A} to {B} bus tickets", f"coach tickets {A} to {B}",
               f"{A} to {B} bus time", f"cheap bus {A} to {B}", f"{A} to {B} by bus", f"{A} {B} intercity bus"]
        intro = pick([
            f"A {word} can be a practical way to travel from {A} to {B}. This guide covers the {mi} mile ({kms} km) route, a realistic journey-time range and the checks that save you trouble on the day.",
            f"Thinking about taking the {word} from {A} to {B}? Below are the key numbers, tips on stops and luggage, and a link to our partner's search for current departures.",
            f"The {kms} km between {A} and {B} can be covered by intercity {word}. Here is what to expect, how long it may take and what to look at before you buy a ticket."], fname, "intro")
        fts = [(tt, "Typical journey time"), (f"{mi} mi / {kms} km", "Approximate distance"),
               ("Road", "Mode of travel"), ("Partner search", "Live departures and fares")]
        glance = pick([
            f"By road, {A} to {B} is about {mi} miles, and we estimate {tt} on a {word}. Traffic, rest stops and the number of pick-ups all affect the real time.",
            f"Expect roughly {tt} for the {kms} km between {A} and {B}. Express services with few stops are faster, and busy periods on the road can add time.",
            f"A {word} from {A} to {B} typically takes {tt}. We base this on distance, so use the partner search for the actual timetable on your date."], fname, "glance")
        parts.append(f"<h2>{esc(A)} to {esc(B)} by {word} at a glance</h2><p>{esc(glance)}</p>")
        parts.append(f"<h2>Stops and arrival</h2><p>{esc(A)} and {esc(B)} may each have more than one place where {word}es stop, and these are not always next to the main railway station. Check the exact pick-up and drop-off point on your booking, and plan the last part of your journey, for example with {a(cfile('taxi', b_), 'a taxi or transfer in ' + b_['disp'])}.</p>")
        pool = BUS_TIPS_UK if uk else BUS_TIPS_US
        tips = [fill(t, a_, b_) for t in pick_n(pool, 5, fname, "tips")]
        parts.append(f"<h2>Tips for {esc(A)} to {esc(B)} {word} tickets</h2>{tips_ul(tips)}")
        options = []
        if alt["trains"]: options.append(f'a <a href="{rfile("trains", a_, b_)}">train from {esc(A)} to {esc(B)}</a>')
        if alt["flights"]: options.append(f'a <a href="{rfile("flights", a_, b_)}">flight from {esc(A)} to {esc(B)}</a>')
        parts.append("<h2>Other ways to travel</h2><p>" + (f"If a {word} is not right for you, compare {' or '.join(options)}." if options else f"Browse our {a('trains.html', 'train guides')} and {a('flights.html', 'flight guides')} if you want to compare other modes.") + "</p>")
        faqs = [
            (f"How long is the {word} from {A} to {B}?", f"We estimate {tt} for about {kms} km. Real time depends on traffic, stops and the operator."),
            (f"Where does the {word} stop in {B}?", "Stops differ by operator. Your booking shows the exact drop-off point, so check it before you travel."),
            (f"Are {word} tickets cheaper than other options?", "Often they can be, but prices change with date, demand and how early you book. Compare options for your own dates rather than assuming."),
            (f"Can I travel from {A} to {B} another way?", "Yes. " + (("There is " + ("a train guide" if alt["trains"] else "") + (" and " if alt["trains"] and alt["flights"] else "") + ("a flight guide" if alt["flights"] else "") + " on this site.") if (alt["trains"] or alt["flights"]) else "See our train and flight guides for related routes.")),
            ("Do you sell the tickets?", "No. This website is an independent affiliate guide. When you click a booking button you go to a partner's website, where you complete the purchase."),
        ]
        cta_text = f"Check {A} to {B} {word} tickets"
        cat = "buses"
    main_cta = cta(cat, cta_text, ds)
    extra_btns = [aff(cat, cta_text, ds)]
    if revlink: extra_btns.append(a(revlink, f"{B} to {A}", "btn btn-ghost"))
    extra = '<div class="btn-row">' + "".join(extra_btns) + "</div>" + facts(fts)
    crumbs = [("Home", "index.html"), (KIND_LABEL[kind], KIND_HUB[kind]), (country_list_label(kind, a_, b_), country_list_file(kind, a_, b_)), (f"{A} to {B}", None)]
    h = hero(crumbs, f"{KIND_LABEL[kind][:-1] if kind != 'buses' else 'Bus'} from {A} to {B}" if kind != "flights" else f"Flights from {A} to {B}", intro, extra)
    more = "<h2>More routes and places</h2>"
    if frm: more += f"<h3>More {KIND_LABEL[kind].lower()} from {esc(A)}</h3>{link_list(frm)}"
    if to: more += f"<h3>More {KIND_LABEL[kind].lower()} to {esc(B)}</h3>{link_list(to)}"
    more += (f"<h3>City guides</h3>" + link_list([(cfile('travel', a_), f"Travel guide: {A}"), (cfile('travel', b_), f"Travel guide: {B}"),
             (cfile('tours', b_), f"Tours in {B}"), (cfile('packages', b_), f"Holiday packages to {B}"), (cfile('taxi', b_), f"Taxi and transfers in {B}")]))
    body = h + '<div class="container page-body">' + note() + "".join(parts) + main_cta + more + "<!--FAQ-->" + main_cta.replace("cta-box", "cta-box") + "</div>"
    render(fname, title, desc, kws, body, kind, faqs=faqs)

# ---------------------------------------------------------------- city pages
def city_faq_common(p):
    return ("Do you sell the tickets or bookings?", "No. This website is an independent affiliate guide. When you click a booking button you go to a partner's website, where you complete the purchase.")

def region_phrase(p):
    return f"{p['region']}" if p["country"] == "UK" else f"{p['region']}"

def travel_city(p):
    N = p["disp"]; ds = ds_city(p)
    fname = cfile("travel", p)
    near = nearby(p, 6)
    fl_in = [(rfile("flights", x, y), label("flights", x, y)) for x, y, _ in RT["flights"] if y is p]
    fl_out = [(rfile("flights", x, y), label("flights", x, y)) for x, y, _ in RT["flights"] if x is p]
    tr = [(rfile("trains", x, y), label("trains", x, y)) for x, y, _ in RT["trains"] if x is p]
    bu = [(rfile("buses", x, y), label("buses", x, y)) for x, y, _ in RT["buses"] if x is p]
    title = trim(f"Travel to {N}: Flights, Trains, Buses & Tours", 62)
    desc = f"Plan travel to and from {N}, {p['region']}: airports, rail and coach options, nearby places and links to tours, holiday packages and transfers."
    kws = [f"travel to {N}", f"{N} travel guide", f"how to get to {N}", f"flights to {N}", f"trains to {N}", f"buses to {N}",
           f"{N} airport", f"getting to {N}", f"visit {N}", f"{N} transport"]
    intro = f"{p['blurb']} This page brings together the ways to reach {N} in {p['region']}, from airports to rail and coach links, and points you to tours, holiday packages and transfers."
    btns = '<div class="btn-row">' + aff("flights", f"Search flights to {N}", ds) + aff("trains", f"Search trains to {N}", ds, "btn btn-ghost") + aff("buses", f"Search buses to {N}", ds, "btn btn-ghost") + "</div>"
    nairports = len([x for x in re.split(r",| and ", p["short_air"]) if "(" in x])
    f = facts([(p["region"], "Region" if p["country"] == "USA" else "Nation"), (p["code"], "City or airport code"),
               (str(nairports) if nairports else "None", "Airports named in this guide"), ("Yes" if (p["gb"] or p["amtrak"]) else "Limited", "Intercity rail guide")])
    crumbs = [("Home", "index.html"), ("UK" if p["country"] == "UK" else "USA", "travel-uk.html" if p["country"] == "UK" else "travel-usa.html")]
    if region_link(p): crumbs.append((p["region"], region_link(p)))
    crumbs.append((N, None))
    h = hero(crumbs, f"Travel to and from {N}", intro, btns + f)
    parts = [note(),
             f"<h2>Getting to {esc(N)} by air</h2><p>{esc(air_sentence(p))} Fares, schedules and baggage rules depend on the airline, so use the partner search for current options.</p>"]
    if fl_in: parts.append(f"<h3>Flights into {esc(N)} on this site</h3>{link_list(fl_in[:14])}" + (f"<p>See all of them in the {a('flights-uk.html' if p['country']=='UK' else 'flights-usa.html', 'flight directory')}.</p>" if len(fl_in) > 14 else ""))
    parts.append(f"<h2>By train</h2>")
    if tr: parts.append(f"<p>Rail is a common way to reach {esc(N)} from other large places. These guides start from {esc(N)}; each also has a matching return guide.</p>{link_list(tr[:14])}")
    elif p["country"] == "UK" and p["gb"]: parts.append(f"<p>{esc(N)} is on the Great Britain rail network, but we do not have a dedicated route guide that starts here. Use the button below to check journeys from your own station.</p>")
    elif p["amtrak"]: parts.append(f"<p>{esc(N)} has intercity rail service, but we do not have a dedicated route guide for it. Use the button below to check journeys from your own station.</p>")
    else: parts.append(f"<p>{esc(N)} has limited or no intercity passenger rail, so flying, a coach or a pre-booked transfer is often the practical choice.</p>")
    parts.append(f'<div class="btn-row">{aff("trains", f"Search trains to {N}", ds)}</div>')
    parts.append(f"<h2>By coach or bus</h2>")
    if bu: parts.append(f"<p>Long-distance coaches and buses can be a flexible way to reach {esc(N)}.</p>{link_list(bu[:14])}")
    else: parts.append(f"<p>Intercity coaches and buses often serve {esc(N)}, even though we do not have a dedicated route guide starting here. Use the button below to check what runs from your own location.</p>")
    parts.append(f'<div class="btn-row">{aff("buses", f"Search buses to {N}", ds)}</div>')
    parts.append(f"<h2>Things to book for {esc(N)}</h2>" + link_list([(cfile('tours', p), f"Tours and day trips in {N}"), (cfile('packages', p), f"Holiday packages to {N}"), (cfile('taxi', p), f"Taxi and airport transfers in {N}")]))
    nl = [(cfile("travel", q), f"{q['disp']}: about {fnum(km)} km away") for km, q in near]
    parts.append(f"<h2>Places near {esc(N)}</h2><p>These are the closest places in our guide, with approximate straight-line distances.</p>{link_list(nl)}")
    if region_link(p): parts.append(f"<p>Browse more of {a(region_link(p), 'travel in ' + p['region'])} or the {a('travel-uk.html' if p['country']=='UK' else 'travel-usa.html', 'wider ' + ('UK' if p['country']=='UK' else 'US') + ' guide')}.</p>")
    faqs = [(f"What is the nearest airport to {N}?", air_sentence(p)),
            (f"Can I get to {N} by train?", "Yes, in many cases." if (p["gb"] or p["amtrak"]) else f"{N} has limited intercity rail, so check other options first."),
            (f"What else can I book for {N}?", f"You can compare tours, holiday packages and taxi or airport transfers using the guides linked above."),
            city_faq_common(p)]
    parts.append("<!--FAQ-->")
    body = h + '<div class="container page-body">' + "".join(parts) + "</div>"
    render(fname, title, desc, kws, body, "city", faqs=faqs)

TOUR_TYPES = [
    ("Guided walking tours", "A local guide can explain the history and layout of the centre in two to three hours, which is a useful first-day activity."),
    ("Food and drink tours", "Tastings and market visits give a flavour of local cooking, with group or private options."),
    ("Day trips to nearby places", "Coach or minibus excursions let you see places outside the centre without arranging your own transport."),
    ("Museum and heritage visits", "Timed-entry tickets and guided visits can save queueing at popular attractions."),
    ("Private guides", "A private guide can adapt the pace and route for families, accessibility needs or special interests."),
    ("Family-friendly activities", "Look for activities with age guidance, shorter durations and flexible cancellation."),
    ("Evening and night tours", "Evening walks and transport-based sightseeing can suit travellers who prefer to avoid daytime heat or crowds."),
    ("Hop-on hop-off sightseeing", "Where offered, multi-stop routes help you cover the main sights at your own pace."),
]
TOUR_TIPS = [
    "Check the meeting point and start time before you book, and arrive early.",
    "Read the cancellation policy. Flexible bookings help if the weather or your plans change.",
    "Check the language, group size and total duration of the tour.",
    "Look at what is included, such as entry fees, food or transport, so there are no surprises.",
    "Book earlier for peak season, weekends and major events.",
    "Check accessibility information if anyone in your group has mobility needs.",
    "Read recent traveller feedback on the partner's site before choosing an operator.",
]

def tours_city(p):
    N = p["disp"]; ds = ds_city(p); fname = cfile("tours", p)
    near = nearby(p, 6, 160)
    title = trim(f"Tours & Day Trips in {N}: Book Online", 62)
    desc = f"Find tours, day trips and activities in {N}, {p['region']}. See the types of experience to look for, nearby places for day trips and tips for booking with our partner."
    kws = [f"tours in {N}", f"{N} tours", f"things to do in {N}", f"{N} day trips", f"{N} sightseeing tours", f"book {N} tours", f"{N} guided tours", f"{N} activities"]
    intro = f"{p['blurb']} Use this page to understand which kinds of tours and activities to compare in {N}, how nearby places can make day trips, and what to check before you book."
    btns = '<div class="btn-row">' + aff("tours", f"Browse tours in {N}", ds) + a(cfile("travel", p), f"How to get to {N}", "btn btn-ghost") + "</div>"
    crumbs = [("Home", "index.html"), ("Tours", "tours.html"), ("UK" if p["country"] == "UK" else "USA", "tours-uk.html" if p["country"] == "UK" else "tours-usa.html"), (N, None)]
    h = hero(crumbs, f"Tours and Day Trips in {N}", intro, btns)
    types = pick_n(TOUR_TYPES, 5, fname, "types")
    parts = [note(), f"<h2>Types of tours to look for in {esc(N)}</h2>" + "".join(f"<h3>{esc(t)}</h3><p>{esc(d)}</p>" for t, d in types)]
    if near:
        parts.append(f"<h2>Day trips from {esc(N)}</h2><p>These places in our guide are within about 160 km (100 miles) of {esc(N)}. Check journey time before you plan a day trip.</p>" +
                     link_list([(cfile("tours", q), f"Tours in {q['disp']} ({fnum(km)} km, around {hm(drive_time(km)[0])} to {hm(drive_time(km)[1])} by road)") for km, q in near]))
    else:
        km, q = nearby(p, 1)[0]
        parts.append(f"<h2>Further afield</h2><p>{esc(N)} is fairly remote. The closest place in our guide is {a(cfile('tours', q), q['disp'])}, about {fnum(km)} km away, so plan extra travel time for any excursion.</p>")
    parts.append(f"<h2>Tips for booking tours in {esc(N)}</h2>{tips_ul(pick_n(TOUR_TIPS, 5, fname, 'tips'))}")
    parts.append(cta("tours", f"Browse tours in {N}", ds))
    parts.append(f"<h2>Plan the rest of your trip</h2>" + link_list([(cfile('travel', p), f"Travel guide: {N}"), (cfile('packages', p), f"Holiday packages to {N}"), (cfile('taxi', p), f"Taxi and transfers in {N}")]))
    faqs = [(f"What are the best types of tour in {N}?", f"It depends on your interests. Walking tours suit a first visit, food tours suit curious eaters, and day trips help you see the surrounding area."),
            (f"Can I book tours in {N} in advance?", "Yes. Booking ahead is a good idea in busy periods. Check the partner's cancellation terms first."),
            (f"Are there day trips from {N}?", (f"Yes. Nearby places in our guide include {', '.join(q['disp'] for _, q in near[:3])}.") if near else "Options are limited, so allow for longer journeys."),
            city_faq_common(p)]
    parts.append("<!--FAQ-->")
    render(fname, title, desc, kws, h + '<div class="container page-body">' + "".join(parts) + "</div>", "city", faqs=faqs)

PACK_TIPS = [
    "Compare the package total with the price of booking each part separately, since the cheaper option varies.",
    "Check what is included: flights, hotel, transfers, baggage, meals and any resort or city fees.",
    "Read the cancellation and change terms for the whole package, not just the hotel.",
    "Look for financial protection. For example, flight-inclusive packages sold in the UK may carry ATOL protection, so check what applies to you.",
    "Check the location of the hotel. A lower price can mean longer transfers into the centre.",
    "Book earlier for school holidays and peak seasons, when availability narrows.",
    "Check passport and entry requirements for all travellers before you book.",
]

def packages_city(p):
    N = p["disp"]; ds = ds_city(p); fname = cfile("packages", p)
    title = trim(f"Holiday Packages to {N}: Flights + Hotel Guide", 62)
    desc = f"Compare holiday packages to {N}, {p['region']}: what a package includes, how to depart, entry checks and tips before you book with our partner."
    kws = [f"holiday packages to {N}", f"{N} holiday packages", f"{N} flight and hotel deals", f"{N} package holidays", f"{N} city break", f"book {N} holiday", f"{N} vacation packages", f"{N} trip packages"]
    intro = f"{p['blurb']} A package that combines travel and accommodation can simplify a trip to {N}. This page explains what to compare and where to start."
    btns = '<div class="btn-row">' + aff("packages", f"Compare packages to {N}", ds) + a(cfile("travel", p), f"How to get to {N}", "btn btn-ghost") + "</div>"
    crumbs = [("Home", "index.html"), ("Holiday Packages", "holiday-packages.html"), ("UK" if p["country"] == "UK" else "USA", "holiday-packages-uk.html" if p["country"] == "UK" else "holiday-packages-usa.html"), (N, None)]
    h = hero(crumbs, f"Holiday Packages to {N}", intro, btns)
    if p["country"] == "USA":
        dep = [find(n, "UK") for n in UK_TRANSATLANTIC if (find(n, "UK")["slug"], p["slug"]) in RS["flights"]]
        depline = (f"<h2>Departing from the UK</h2><p>Travellers from Britain and Northern Ireland often depart from {esc(', '.join(x['disp'] for x in dep[:6]))}. Check the airport, journey time and entry requirements such as ESTA or a visa. See, for example, "
                   + " or ".join(a(rfile('flights', x, p), f'flights from {x["disp"]} to {N}') for x in dep[:3]) + ".</p>") if dep else ""
        entry = "Check US entry requirements before you book."
    else:
        dep = [q for q in (find(n, "USA") for n in US_TRANSATLANTIC) if (q["slug"], p["slug"]) in RS["flights"]]
        depline = (f"<h2>Departing from the USA</h2><p>Travellers from the United States often depart from {esc(', '.join(x['disp'] for x in dep[:6]))}. Check the airport, journey time and entry requirements such as a UK ETA or a visa. See, for example, "
                   + " or ".join(a(rfile('flights', x, p), f'flights from {x["disp"]} to {N}') for x in dep[:3]) + ".</p>") if dep else ""
        entry = "Check UK entry requirements before you book."
    if not depline:
        depline = f"<h2>Getting there</h2><p>{esc(air_sentence(p))} You can also see {a(cfile('travel', p), 'all travel options for ' + N)}.</p>"
    parts = [note(), f"<h2>What a package to {esc(N)} usually includes</h2><p>Packages combine two or more parts of a trip, most often flights and a hotel, sometimes with transfers, car hire or tours. The partner's page lists what each offer includes. {esc(entry)}</p>",
             depline, f"<h2>Tips for booking a package to {esc(N)}</h2>{tips_ul(pick_n(PACK_TIPS, 5, fname, 'tips'))}",
             cta("packages", f"Compare packages to {N}", ds),
             f"<h2>Add to your trip</h2>" + link_list([(cfile('tours', p), f"Tours and day trips in {N}"), (cfile('taxi', p), f"Taxi and transfers in {N}"), (cfile('travel', p), f"Travel guide: {N}")]), "<!--FAQ-->"]
    faqs = [(f"What does a holiday package to {N} include?", "Most include flights and a hotel. Some add transfers or tours. Check each offer for exact inclusions."),
            (f"Is a package cheaper than booking separately?", "Sometimes, but not always. Compare the total for your dates before you decide."),
            (f"What should I check before booking a package to {N}?", f"{entry} Also check cancellation terms, baggage allowance and any financial protection."),
            city_faq_common(p)]
    render(fname, title, desc, kws, h + '<div class="container page-body">' + "".join(parts) + "</div>", "city", faqs=faqs)

TAXI_TIPS = [
    "Confirm whether the price is fixed or metered before you set off.",
    "Pre-book if you arrive late at night, with young children or with lots of luggage.",
    "Share your flight number so the driver can track delays.",
    "Check where the meeting point is. Airports often have a set pick-up area.",
    "Ask for a child seat when you book if you need one.",
    "Use licensed operators only, and check that the vehicle and driver match your booking.",
    "Check luggage space if you are travelling in a group.",
]

def taxi_city(p):
    N = p["disp"]; ds = ds_city(p); fname = cfile("taxi", p)
    near = nearby(p, 5, 250)
    uk = p["country"] == "UK"
    title = trim(f"Taxi & Airport Transfers in {N}: Pre-Book Guide", 62)
    desc = f"Plan taxi and airport transfers in {N}, {p['region']}: airports, pre-booking tips, intercity transfer times and how to check prices with our partner."
    kws = [f"taxi in {N}", f"{N} taxi", f"{N} airport transfer", f"{N} airport taxi", f"private transfer {N}", f"book taxi {N}", f"{N} car service", f"{N} airport pickup"]
    kinds = "licensed taxis and private hire vehicles" if uk else "taxis, rideshare services and pre-booked car services"
    intro = f"Getting from the airport or station to your hotel in {N} is easier when you plan ahead. This guide explains {kinds}, how to prepare for a smooth pickup and where pre-booked transfers can help."
    btns = '<div class="btn-row">' + aff("taxi", f"Check transfers in {N}", ds) + a(cfile("travel", p), f"How to get to {N}", "btn btn-ghost") + "</div>"
    crumbs = [("Home", "index.html"), ("Taxi & Transfers", "taxi.html"), ("UK" if uk else "USA", "taxi-uk.html" if uk else "taxi-usa.html"), (N, None)]
    h = hero(crumbs, f"Taxi and Airport Transfers in {N}", intro, btns)
    parts = [note(), f"<h2>Airport transfers for {esc(N)}</h2><p>{esc(air_sentence(p))} Transfer time and cost depend on the airport you use, the time of day and traffic, so check the details on your booking.</p>",
             f"<h2>Pre-booked or on the day?</h2><p>On-the-day {'taxis' if uk else 'taxis and rideshares'} are convenient for short trips. Pre-booking gives you a confirmed vehicle and a quoted price before you travel, which many people prefer after a long flight. Compare both and choose what suits your arrival time.</p>"]
    if near:
        rows = []
        for km, q in near:
            lo, hi = drive_time(km)
            rows.append((cfile("taxi", q), f"{N} to {q['disp']}: about {fnum(km)} km, roughly {hm(lo)} to {hm(hi)} by road"))
        parts.append(f"<h2>Intercity transfers from {esc(N)}</h2><p>For longer private journeys, these are the closest places in our guide. Times are rough estimates, so confirm them on your booking.</p>{link_list(rows)}")
    parts += [f"<h2>Tips for taxi and transfer bookings in {esc(N)}</h2>{tips_ul(pick_n(TAXI_TIPS, 5, fname, 'tips'))}",
              cta("taxi", f"Check transfers in {N}", ds),
              "<h2>Plan the rest of your trip</h2>" + link_list([(cfile('travel', p), f"Travel guide: {N}"), (cfile('tours', p), f"Tours in {N}"), (cfile('packages', p), f"Holiday packages to {N}")]), "<!--FAQ-->"]
    faqs = [(f"Should I pre-book a taxi in {N}?", "Pre-booking is helpful if you arrive late, travel with children or have a lot of luggage. For short daytime trips, an on-the-day taxi may be enough."),
            (f"How do I get from the airport to the centre of {N}?", air_sentence(p) + " Options usually include taxis, transfers and public transport. Check which suits your arrival time."),
            ("Are fares fixed?", "Pre-booked transfers are usually quoted in advance, while metered taxis depend on distance and time. Confirm before you travel."),
            city_faq_common(p)]
    render(fname, title, desc, kws, h + '<div class="container page-body">' + "".join(parts) + "</div>", "city", faqs=faqs)

def build_all():
    for kind in RT:
        for a_, b_, km in RT[kind]: route_page(kind, a_, b_, km)
    for p in PLACES:
        travel_city(p); tours_city(p); packages_city(p); taxi_city(p)
