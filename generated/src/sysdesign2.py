"""System design case studies: five designs with requirements, computed estimates, API, data model, a diagram (SVG + PNG) and trade-offs.
Estimates are computed from stated assumptions (no hand arithmetic). Each design is checked to use building blocks from the System Design
one-pager. Run from the repo root: python3 generated/src/sysdesign.py"""
import html, io, pathlib, subprocess
from pypdf import PdfReader, PdfWriter
from pypdf.generic import Fit
from reportlab.pdfgen import canvas
ROOT = pathlib.Path(__file__).resolve().parents[2]; OUT = ROOT / "generated"; SRC = OUT / "src"; DIA = OUT / "sysdesign2"
E = lambda s: html.escape(str(s), quote=True)
KB = "https://claude.ai/artifact/McuS723LTAb16Q6SpdUsAT#"
DAY = 86_400
def human(x, unit=""):
    for div, suf in ((1e15, " P"), (1e12, " T"), (1e9, " G"), (1e6, " M"), (1e3, " K")):
        if x >= div: return f"{x / div:,.1f}{suf}{unit}"
    return f"{x:,.1f} {unit}".strip()
BLOCKS = {"load balancer", "cache", "cdn", "database", "replication", "sharding", "queue", "rate limiting", "object storage", "websocket", "consistent hashing", "monitoring"}
D = [
 dict(id="gateway", title="API gateway with rate limiting", kb="hld",
  func=["Route each request to the right backend service by path", "Authenticate requests (verify a JWT once, at the edge)", "Enforce per-client rate limits across all gateway instances", "Log every request for audit and debugging"],
  nonf=["Adds only a few milliseconds of latency", "Highly available: no single gateway instance is critical", "Limits hold even when a client's requests hit different instances"],
  assume=dict(avg_rps=20e3, peak=3, clients=1e6, counter_bytes=64, log_bytes=500),
  est=lambda a: [("Requests per day", a["avg_rps"] * DAY), ("Peak requests/s", a["avg_rps"] * a["peak"]), ("Rate-limit counter ops/s at peak (1 per request)", a["avg_rps"] * a["peak"]),
                 ("Counter memory for all clients (bytes)", a["clients"] * a["counter_bytes"]), ("Request logs per day (bytes)", a["avg_rps"] * DAY * a["log_bytes"])],
  api=["ANY /api/{service}/… → proxied to that service", "429 Too Many Requests + Retry-After when a client is over its limit", "401 when the token is missing or invalid"],
  data=["routes(prefix PK, service, timeout_ms) in a config store, cached in every gateway", "Redis: rl:{client}:{window} → count, with a TTL of one window", "Logs streamed to a queue, then to storage and a search index"],
  design=["Stateless gateway instances behind a load balancer; each loads the route table into memory and refreshes it on change.",
          "Rate limiting with a shared Redis: INCR the client's counter for the current window and set its TTL; over the limit → 429. A sliding window (two windows weighted) avoids bursts at window edges.",
          "Authentication at the edge: verify the JWT signature and expiry once, then pass the user id to services in a trusted header.",
          "If Redis is down, fail open with a local per-instance limit (keeps the API up) or fail closed for sensitive endpoints; decide per route."],
  blocks=["load balancer", "rate limiting", "cache", "monitoring", "queue"],
  trade=[("Fixed vs sliding window", "Fixed windows are one counter but allow double bursts at the edge; sliding windows or token buckets are smoother at slightly more cost."), ("Central vs local counters", "Central Redis is accurate but adds a network hop; local counters are free but let a client exceed the limit by the number of instances.")],
  nodes=[("Clients", 0, 1), ("Load balancer", 1, 1), ("Gateway instances", 2, 1), ("Redis (counters)", 3, 0), ("Services A / B / C", 3, 1), ("Log queue", 3, 2), ("Log store + search", 4, 2)],
  edges=[(0, 1), (1, 2), (2, 3), (2, 4), (2, 5), (5, 6)]),
 dict(id="ride", title="Ride matching (Uber-style)", kb="hld",
  func=["Riders request a ride from a pickup point", "Match the nearest available driver; driver accepts or declines", "Track the driver's live location and ETA", "Trip lifecycle: requested → matched → in progress → completed"],
  nonf=["Match within a few seconds", "Location updates every few seconds from every online driver", "A driver is never assigned to two riders at once"],
  assume=dict(drivers=1e6, update_secs=4, update_bytes=100, rides_per_day=20e6, peak=3),
  est=lambda a: [("Location updates/s", a["drivers"] / a["update_secs"]), ("Location ingest (bytes/s)", a["drivers"] / a["update_secs"] * a["update_bytes"]),
                 ("Average ride requests/s", a["rides_per_day"] / DAY), ("Peak ride requests/s", a["rides_per_day"] / DAY * a["peak"])],
  api=["POST /rides {pickup, drop} → {ride_id}", "WS /drivers/{id}/location ← {lat, lng} every 4 s", "POST /rides/{id}/accept (driver)", "GET /rides/{id} → status, driver, ETA"],
  data=["Driver locations in memory, indexed by geohash cell (Redis GEO or an in-memory grid); not in the main database", "rides(ride_id PK, rider_id, driver_id, status, pickup, drop, times) in a relational DB", "Location history to a queue → cheap storage for analytics"],
  design=["Drivers keep a WebSocket open and stream locations to location servers, which update the geo index (sharded by city or geohash prefix).",
          "Matching: query the geo index for available drivers in the pickup cell and its neighbours, rank by ETA, offer to the best; on decline or timeout, offer to the next.",
          "Assignment must be atomic: set the driver's status from available to busy with a conditional write (compare-and-set), so two matchers cannot claim one driver.",
          "Trip state lives in the rides table; status changes are published to a queue for notifications, billing and analytics."],
  blocks=["load balancer", "websocket", "cache", "database", "sharding", "queue"],
  trade=[("Geohash vs quadtree", "Geohash cells are simple and shard well but uneven in dense areas; a quadtree adapts to density but is harder to distribute."), ("Push vs pull locations", "Pushing every 4 s is fresh but costly; adapt the interval to speed and trip state.")],
  nodes=[("Rider / driver apps", 0, 1), ("Load balancer", 1, 1), ("Location servers (WS)", 2, 0), ("Geo index (sharded)", 3, 0), ("Matching service", 2, 1), ("Rides DB", 3, 1), ("Event queue", 3, 2), ("Billing / notify", 4, 2)],
  edges=[(0, 1), (1, 2), (2, 3), (1, 4), (4, 3), (4, 5), (4, 6), (6, 7)]),
 dict(id="checkout", title="E-commerce checkout and inventory", kb="hld",
  func=["Cart, checkout and payment", "Reserve stock at checkout; release it if payment fails or times out", "Order confirmation and history"],
  nonf=["Never oversell, even in a flash sale", "Charge a customer at most once per order, even with retries", "Catalog reads can be slightly stale; stock counts cannot"],
  assume=dict(orders_per_day=2e6, items_per_order=3, peak=10),
  est=lambda a: [("Average orders/s", a["orders_per_day"] / DAY), ("Peak orders/s (sale ×10)", a["orders_per_day"] / DAY * a["peak"]),
                 ("Peak stock decrements/s", a["orders_per_day"] / DAY * a["peak"] * a["items_per_order"]), ("Orders per year", a["orders_per_day"] * 365)],
  api=["POST /cart/items {sku, qty}", "POST /checkout {cart_id, Idempotency-Key} → {order_id, status: pending}", "POST /payments/webhook (from the payment provider)", "GET /orders/{id}"],
  data=["stock(sku PK, available, reserved) in a relational DB (strong consistency)", "orders(order_id PK, user_id, status, total, idempotency_key UNIQUE)", "reservations(order_id, sku, qty, expires_at)", "Catalog in a cache and search index (read-heavy, can lag)"],
  design=["Reserve with one conditional update: UPDATE stock SET available = available − q, reserved = reserved + q WHERE sku = ? AND available ≥ q; zero rows updated means out of stock. No read-then-write race.",
          "Idempotency: the client sends an Idempotency-Key; a UNIQUE constraint makes a retried checkout return the same order instead of creating a second one.",
          "Payment is asynchronous: order 'pending' until the provider's webhook; a saga confirms the reservation on success or releases it on failure; a sweeper releases expired reservations.",
          "Outbox pattern: write the order and an 'order created' event in one transaction; a relay publishes events to the queue so they are never lost."],
  blocks=["load balancer", "database", "queue", "cache", "rate limiting"],
  trade=[("Reserve at add-to-cart vs at checkout", "Cart reservations hold stock hostage; checkout reservations risk 'sold out' at the last step. Most shops reserve at checkout with a short TTL."), ("One database vs per-service databases", "One database makes transactions easy; per-service databases need sagas and idempotent steps.")],
  nodes=[("Web / app", 0, 1), ("Load balancer", 1, 1), ("Checkout service", 2, 1), ("Stock + orders DB", 3, 1), ("Catalog cache", 3, 0), ("Payment provider", 2, 2), ("Outbox → queue", 3, 2), ("Email / fulfilment", 4, 2)],
  edges=[(0, 1), (1, 2), (2, 3), (2, 4), (2, 5), (5, 2), (3, 6), (6, 7)]),
 dict(id="autocomplete", title="Search autocomplete", kb="hld",
  func=["Show the top suggestions for the prefix the user has typed", "Suggestions reflect popular queries and update daily", "Filter offensive suggestions"],
  nonf=["Under about 100 ms per keystroke", "Very read-heavy and highly available", "Tolerates suggestions being a day old"],
  assume=dict(dau=100e6, searches_per_user=5, requests_per_search=4, peak=3, unique_queries=1e9, bytes_per_query=30),
  est=lambda a: [("Suggestion requests per day", a["dau"] * a["searches_per_user"] * a["requests_per_search"]), ("Average requests/s", a["dau"] * a["searches_per_user"] * a["requests_per_search"] / DAY),
                 ("Peak requests/s", a["dau"] * a["searches_per_user"] * a["requests_per_search"] / DAY * a["peak"]), ("Raw query text to aggregate (bytes)", a["unique_queries"] * a["bytes_per_query"])],
  api=["GET /suggest?q={prefix}&limit=10 → [suggestions] (cacheable)"],
  data=["Trie (or prefix → top-k table) with the top 10 completions stored at every node, built offline", "Query logs → daily aggregation job → new trie snapshot", "Sharded by prefix range; replicated for reads"],
  design=["Clients debounce keystrokes (about 4 requests per search instead of one per character) and cache results in the browser.",
          "Serving: requests go through a CDN and cache, then to suggestion servers holding the trie in memory; each lookup is O(prefix length) because top-k is precomputed per node.",
          "Building: a daily batch job counts queries from the logs, drops rare and blocked queries, builds new trie snapshots and swaps them in atomically.",
          "Freshness for trending topics: a small real-time layer adds recent spikes on top of the daily snapshot."],
  blocks=["cdn", "cache", "sharding", "queue", "database", "load balancer"],
  trade=[("Precomputed top-k vs search at query time", "Precomputing makes reads O(prefix) but uses more memory and needs rebuilds; searching the subtree at query time is slow for short prefixes."), ("Daily vs real-time updates", "Daily is simple and stable; real-time catches trends but complicates consistency and abuse filtering.")],
  nodes=[("Browser (debounce)", 0, 1), ("CDN / cache", 1, 1), ("Suggestion servers", 2, 1), ("Trie snapshots (sharded)", 3, 1), ("Query logs", 2, 2), ("Daily build job", 3, 2), ("Snapshot store", 4, 2)],
  edges=[(0, 1), (1, 2), (2, 3), (2, 4), (4, 5), (5, 6), (6, 3)]),
 dict(id="video", title="Video upload and streaming", kb="hld",
  func=["Upload a video; process it into several resolutions", "Stream with adaptive quality (the player switches resolution with bandwidth)", "Title, thumbnail and view counts"],
  nonf=["Smooth playback worldwide", "Uploads are never lost; processing can take minutes", "Storage and bandwidth cost is the main constraint"],
  assume=dict(uploads_per_day=500e3, upload_mb=300, rendition_factor=1.5, views_per_day=100e6, watch_secs=300, mbps=3),
  est=lambda a: [("New raw video per day (bytes)", a["uploads_per_day"] * a["upload_mb"] * 1e6), ("Stored per day incl. renditions (bytes)", a["uploads_per_day"] * a["upload_mb"] * 1e6 * (1 + a["rendition_factor"])),
                 ("Streaming egress per day (bytes)", a["views_per_day"] * a["watch_secs"] * a["mbps"] * 1e6 / 8), ("Average egress (bits/s)", a["views_per_day"] * a["watch_secs"] * a["mbps"] * 1e6 / DAY)],
  api=["POST /videos → {video_id, upload_url} (pre-signed, direct to object storage)", "GET /videos/{id}/manifest.m3u8 (HLS) → segment URLs on the CDN", "POST /videos/{id}/views (batched)"],
  data=["Object storage: originals and renditions as small segments (a few seconds each)", "videos(video_id PK, owner, title, status, renditions, created_at)", "View counts aggregated from a queue, not written per view"],
  design=["Clients upload straight to object storage with a pre-signed URL (resumable, multipart), so app servers never carry video bytes.",
          "Upload complete → event on a queue → transcoding workers produce several resolutions as HLS/DASH segments plus a manifest; status 'ready' when done.",
          "Playback: the player fetches the manifest and segments from a CDN close to the user and switches quality per segment based on measured bandwidth.",
          "Views and likes are counted asynchronously; popular videos stay hot in the CDN, old ones move to cheaper storage tiers."],
  blocks=["cdn", "object storage", "queue", "database", "load balancer", "cache"],
  trade=[("Transcode everything vs on demand", "Pre-transcoding all resolutions costs storage for videos nobody watches; on-demand saves storage but delays the first viewer."), ("Segment length", "Short segments adapt faster and start sooner; long ones are more efficient for the CDN and encoder.")],
  nodes=[("Uploader / player", 0, 1), ("API servers", 1, 1), ("Object storage", 2, 0), ("Videos DB", 2, 1), ("Transcode queue", 2, 2), ("Transcoders", 3, 2), ("CDN", 3, 0)],
  edges=[(0, 1), (0, 2), (1, 3), (2, 4), (4, 5), (5, 2), (2, 6), (6, 0)]),
]
for d in D:   # check against the System Design one-pager: approach steps present, building blocks from its vocabulary
    assert set(d["blocks"]) <= BLOCKS and len(d["blocks"]) >= 4, d["id"]
    assert d["func"] and d["nonf"] and d["api"] and d["data"] and d["design"] and d["trade"]
    d["estimates"] = [(k, v) for k, v in d["est"](d["assume"])]
est = {d["id"]: dict(d["estimates"]) for d in D}
assert est["ride"]["Location updates/s"] == 250_000 and est["gateway"]["Peak requests/s"] == 60_000 and round(est["checkout"]["Peak orders/s (sale ×10)"]) == 231
assert est["video"]["Streaming egress per day (bytes)"] == 1.125e16 and round(est["autocomplete"]["Average requests/s"]) == 23_148   # 11.25 PB/day: why a CDN
def diagram(d):
    W, H, cw, ch = 1100, 360, 190, 64
    cols = max(c for _, c, _ in d["nodes"]) + 1; gx = (W - 40 - cols * cw) / max(cols - 1, 1)
    pos = [(20 + c * (cw + gx), 30 + r * 110) for _, c, r in d["nodes"]]
    F = "font-family='Inter, Arial, sans-serif'"
    s = ["<defs><marker id='a' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='7' markerHeight='7' orient='auto-start-reverse'><path d='M0,0 L10,5 L0,10 z' fill='#334155'/></marker></defs>", f"<rect width='{W}' height='{H}' fill='#fff'/>"]
    for a, b in d["edges"]:
        (x1, y1), (x2, y2) = pos[a], pos[b]
        if x2 > x1: sx, sy, ex, ey = x1 + cw, y1 + ch / 2, x2, y2 + ch / 2
        elif x2 < x1: sx, sy, ex, ey = x1, y1 + ch / 2, x2 + cw, y2 + ch / 2
        else: sx, sy, ex, ey = x1 + cw / 2, (y1 + ch if y2 > y1 else y1), x2 + cw / 2, (y2 if y2 > y1 else y2 + ch)
        s.append(f"<line x1='{sx:.0f}' y1='{sy:.0f}' x2='{ex:.0f}' y2='{ey:.0f}' stroke='#334155' stroke-width='1.8' marker-end='url(#a)'/>")
    for (name, c, r), (x, y) in zip(d["nodes"], pos):
        col = "#8c4fff" if c == 0 else "#3f8624" if any(k in name.lower() for k in ("db", "store", "storage", "cache")) else "#ed7100" if "queue" in name.lower() else "#1d4ed8"
        s.append(f"<rect x='{x:.0f}' y='{y}' width='{cw}' height='{ch}' rx='8' fill='#fff' stroke='{col}' stroke-width='2'/><rect x='{x:.0f}' y='{y}' width='{cw}' height='6' rx='3' fill='{col}'/>")
        words, lines, cur = name.split(), [], ""
        for w_ in words:
            if len(cur + " " + w_) > 22: lines.append(cur); cur = w_
            else: cur = (cur + " " + w_).strip()
        lines.append(cur)
        for i, ln in enumerate(lines): s.append(f"<text x='{x + cw / 2:.0f}' y='{y + 30 + i * 15 - (len(lines) - 1) * 7}' text-anchor='middle' {F} font-size='13' font-weight='600' fill='#0f172a'>{E(ln)}</text>")
    return f"<svg xmlns='http://www.w3.org/2000/svg' width='{W}' height='{H}' viewBox='0 0 {W} {H}'>{''.join(s)}</svg>"
DIA.mkdir(exist_ok=True)
for d in D: (DIA / f"{d['id']}.svg").write_text(diagram(d))
js = SRC / "r.js"
js.write_text("const { chromium } = require('playwright'); (async () => { const b = await chromium.launch(); const p = await b.newPage({ deviceScaleFactor: 2 }); for (const n of process.argv.slice(3)) { await p.goto('file://' + process.argv[2] + '/' + n + '.svg'); await (await p.$('svg')).screenshot({ path: process.argv[2] + '/' + n + '.png' }); } await b.close(); })();")
subprocess.run(["node", str(js), str(DIA)] + [d["id"] for d in D], check=True)
def body(pages):
    pg = lambda k: str(pages.get(k, "000")) if pages else "000"
    rows = "".join(f'<tr><td><a href="#{d["id"]}">{E(d["title"])}</a></td><td class="pg"><a href="#{d["id"]}">{pg(d["id"])}</a></td></tr>' for d in D)
    out = [f'''<section class="cover"><p class="eb">SYSTEM DESIGN · CASE STUDIES II</p><h1>Five more designs<br><span>worked end to end</span></h1>
<p class="lead">An API gateway with rate limiting, ride matching, e-commerce checkout and inventory, search autocomplete, and video upload and streaming (none repeated from the first case-studies pack), each following the approach on the System Design one-pager: requirements → estimates → API → data model → design → trade-offs, with a diagram. Every estimate is computed from the stated assumptions, so you can change an assumption and redo the maths the same way.</p>
<p class="how"><b>In the interview.</b> Spend 5 minutes on requirements and estimates, 10 on the API, data and high-level diagram, 15 on one or two deep dives the interviewer picks, and the rest on trade-offs and failure cases. Freshers are mostly judged on clear reasoning, not on knowing every tool. See the <a href="{KB}hld">system design</a> Knowledge Base page.</p>
<table class="ix"><tbody>{rows}</tbody></table></section>''']
    li = lambda xs: "".join(f"<li>{E(x)}</li>" for x in xs)
    for d in D:
        assume = ", ".join(f"{k.replace('_', ' ')} = {v:,.0f}" if v == int(v) else f"{k.replace('_', ' ')} = {v:g}" for k, v in d["assume"].items())
        est = "".join(f"<tr><td>{E(k)}</td><td class=v>{human(v, 'B' if 'bytes' in k else '')}</td></tr>" for k, v in d["estimates"])
        out.append(f'''<section class="sec" id="{d["id"]}"><h2>{E(d["title"])}<a class="back" href="#top">↑ Index</a></h2>
<img src="file://{DIA}/{d["id"]}.png" style="width:100%">
<div class="two"><div><h3>Functional requirements</h3><ul>{li(d["func"])}</ul><h3>Non-functional</h3><ul>{li(d["nonf"])}</ul></div>
<div><h3>Estimates</h3><p class="meta">Assumptions: {E(assume)}.</p><table class="est"><tbody>{est}</tbody></table><h3>API</h3><ul class="mono">{li(d["api"])}</ul></div></div>
<h3>Data model</h3><ul class="mono">{li(d["data"])}</ul><h3>Design</h3><ul>{li(d["design"])}</ul>
<h3>Trade-offs</h3><table class="t"><tbody>{"".join(f"<tr><td class=k>{E(a)}</td><td>{E(b)}</td></tr>" for a, b in d["trade"])}</tbody></table>
<p class="meta">Building blocks used: {E(", ".join(d["blocks"]))}.</p></section>''')
    return "".join(out)
CSS = """@page { size: A4; margin: 11mm 12mm 13mm; } @page :first { margin: 0; }
* { box-sizing: border-box; } html { -webkit-print-color-adjust: exact; print-color-adjust: exact; } body { margin: 0; font: 400 8.6pt/1.42 Inter, sans-serif; color: #1e293b; }
a { color: #c2410c; text-decoration: none; } .cover { padding: 16mm 15mm; break-after: page; } .eb { font: 600 8pt "JetBrains Mono"; letter-spacing: .14em; color: #c2410c; margin: 0 0 3mm; }
h1 { font: 700 34pt/1.02 "Space Grotesk"; margin: 0 0 4mm; color: #0f172a; } h1 span { color: #c2410c; font-size: 20pt; } .lead { font-size: 10pt; color: #475569; } .how { background: #fff7ed; border-left: 3px solid #c2410c; padding: 2mm 3mm; }
table { border-collapse: collapse; width: 100%; } .ix td { padding: 2.2mm 2mm; border-bottom: 1px solid #e2e8f0; font-size: 10.5pt; } .ix td a { color: #0f172a; font-weight: 600; } .ix .pg { text-align: right; } .ix .pg a { color: #c2410c; font-family: "JetBrains Mono"; }
.sec { break-before: page; } h2 { font: 700 15pt "Space Grotesk"; color: #0f172a; border-bottom: 3px solid #c2410c; padding-bottom: 1.5mm; margin: 0 0 2mm; display: flex; align-items: baseline; } .back { margin-left: auto; font: 600 7.5pt "JetBrains Mono"; border: 1px solid #fdba74; background: #fff7ed; border-radius: 99px; padding: 0 7px; }
h3 { font: 700 9.6pt "Space Grotesk"; color: #1d4ed8; margin: 2.2mm 0 .8mm; } ul { padding-left: 4.5mm; margin: 0; } li { margin-bottom: .6mm; } .two { display: grid; grid-template-columns: 1fr 1fr; gap: 5mm; }
.mono li { font: 400 7.6pt "JetBrains Mono"; font-variant-ligatures: none; } .est td { border-bottom: 1px solid #eef2f7; padding: .7mm 1.5mm; } .est .v { text-align: right; font: 600 8pt "JetBrains Mono"; color: #166534; }
.t td { border-bottom: 1px solid #e2e8f0; padding: 1.2mm 2mm; vertical-align: top; } .k { font-weight: 700; width: 36mm; } .meta { color: #64748b; font-size: 8pt; margin: .5mm 0; }"""
def render(pages, name):
    (SRC / "sd2.html").write_text(f'<!doctype html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700&family=Inter:wght@400;600;700&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet"><style>{CSS}</style></head><body><div id="top"></div>{body(pages)}</body></html>')
    js.write_text("const { chromium } = require('playwright'); (async () => { const b = await chromium.launch(); const p = await b.newPage(); await p.goto('file://' + __dirname + '/sd2.html', { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready); await p.pdf({ path: __dirname + '/" + name + "', format: 'A4', printBackground: true, preferCSSPageSize: true }); await b.close(); })();")
    subprocess.run(["node", str(js)], check=True)
    r = PdfReader(str(SRC / name)); return {k.lstrip("/"): r.get_destination_page_number(v) + 1 for k, v in r.named_destinations.items()}, len(r.pages)
d1, n1 = render(None, "p1.pdf"); d2, n2 = render(d1, "p2.pdf"); assert n1 == n2 and all(d1[d["id"]] == d2[d["id"]] for d in D)
w = PdfWriter(clone_from=PdfReader(str(SRC / "p2.pdf"))); w.add_outline_item("Index", 0, fit=Fit.fit())
for d in D: w.add_outline_item(d["title"], d2[d["id"]] - 1, fit=Fit.fit())
NP = len(w.pages)
for i, pg in enumerate(w.pages):
    if i == 0: continue
    buf = io.BytesIO(); c = canvas.Canvas(buf, pagesize=(float(pg.mediabox.width), float(pg.mediabox.height))); c.setFont("Helvetica", 7.5); c.setFillGray(.55)
    c.drawRightString(float(pg.mediabox.width) - 26, 14, f"{i + 1} / {NP}"); c.save(); buf.seek(0); pg.merge_page(PdfReader(buf).pages[0]); pg.compress_content_streams(level=9)
w.add_metadata({"/Title": "System design case studies II"}); w.write(str(OUT / "system-design-case-studies-2.pdf"))
for f in ("p1.pdf", "p2.pdf", "r.js", "sd2.html"): (SRC / f).unlink()
print(NP, "pages", d2); [print(d["id"], [(k, human(v)) for k, v in d["estimates"]]) for d in D]
