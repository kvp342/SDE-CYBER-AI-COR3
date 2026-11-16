"""System design case studies: five designs with requirements, computed estimates, API, data model, a diagram (SVG + PNG) and trade-offs.
Estimates are computed from stated assumptions (no hand arithmetic). Each design is checked to use building blocks from the System Design
one-pager. Run from the repo root: python3 generated/src/sysdesign.py"""
import html, io, pathlib, subprocess
from pypdf import PdfReader, PdfWriter
from pypdf.generic import Fit
from reportlab.pdfgen import canvas
ROOT = pathlib.Path(__file__).resolve().parents[2]; OUT = ROOT / "generated"; SRC = OUT / "src"; DIA = OUT / "sysdesign"
E = lambda s: html.escape(str(s), quote=True)
KB = "https://claude.ai/artifact/McuS723LTAb16Q6SpdUsAT#"
DAY = 86_400
def human(x, unit=""):
    for div, suf in ((1e15, " P"), (1e12, " T"), (1e9, " G"), (1e6, " M"), (1e3, " K")):
        if x >= div: return f"{x / div:,.1f}{suf}{unit}"
    return f"{x:,.1f} {unit}".strip()
BLOCKS = {"load balancer", "cache", "cdn", "database", "replication", "sharding", "queue", "rate limiting", "object storage", "websocket", "consistent hashing", "monitoring"}
D = [
 dict(id="url", title="URL shortener", kb="hld",
  func=["Create a short link for a long URL, optionally with a custom alias and expiry", "Redirect a short link to the long URL", "Basic click counts"],
  nonf=["Redirects fast (tens of milliseconds) and highly available", "Short codes unguessable enough not to enumerate easily", "Read-heavy: reads far exceed writes"],
  assume=dict(new_per_month=100e6, read_write=100, bytes_per_row=500, years=5),
  est=lambda a: [("Write QPS", a["new_per_month"] / (30 * DAY)), ("Read QPS", a["new_per_month"] * a["read_write"] / (30 * DAY)),
                 ("Rows in 5 years", a["new_per_month"] * 12 * a["years"]), ("Storage in 5 years (bytes)", a["new_per_month"] * 12 * a["years"] * a["bytes_per_row"]),
                 ("7-char base62 codes available", 62 ** 7)],
  api=["POST /urls {long_url, alias?, expires_at?} → {code}", "GET /{code} → 302 Location: long_url", "GET /urls/{code}/stats → {clicks}"],
  data=["urls(code PK, long_url, owner_id, created_at, expires_at)", "Key-value store (DynamoDB or Cassandra) keyed by code; clicks counted asynchronously"],
  design=["ID generation: each app server takes a block of counter values from a coordinator and base62-encodes them (no collisions, no per-write coordination); add a random offset if codes must not be sequential.",
          "Reads: load balancer → app servers → Redis cache (hot codes, LRU) → database on a miss. The read path is stateless and scales horizontally.",
          "Clicks: the redirect handler publishes an event to a queue; a worker aggregates counts, so redirects never wait on analytics.",
          "Abuse: rate-limit creation per user or IP; check long URLs against a malware list."],
  blocks=["load balancer", "cache", "database", "sharding", "queue", "rate limiting"],
  trade=[("301 vs 302", "301 is cached by browsers (less load, but you lose click counts); 302 keeps every click visible."), ("Counter vs hash", "Counter blocks never collide; hashing the URL needs collision checks but gives the same code for the same URL.")],
  nodes=[("Client", 0, 1), ("Load balancer", 1, 1), ("App servers", 2, 1), ("Redis cache", 3, 0), ("Key-value DB", 3, 1), ("ID allocator", 2, 2), ("Click queue", 3, 2), ("Stats worker", 4, 2)],
  edges=[(0, 1), (1, 2), (2, 3), (2, 4), (2, 5), (2, 6), (6, 7), (7, 4)]),
 dict(id="chat", title="Chat app (one-to-one and groups)", kb="hld",
  func=["Send and receive messages in real time, one-to-one and in groups", "Message history across devices", "Delivered and read receipts, online status"],
  nonf=["Low latency for online users", "No lost messages; order preserved within a conversation", "Works when the receiver is offline (push notification, then sync)"],
  assume=dict(dau=50e6, msgs_per_user=40, bytes_per_msg=100, peak=3),
  est=lambda a: [("Messages per day", a["dau"] * a["msgs_per_user"]), ("Average messages/s", a["dau"] * a["msgs_per_user"] / DAY),
                 ("Peak messages/s (×3)", a["dau"] * a["msgs_per_user"] / DAY * a["peak"]), ("New storage per day (bytes)", a["dau"] * a["msgs_per_user"] * a["bytes_per_msg"])],
  api=["WebSocket: send {conversation_id, client_msg_id, text} → ack {message_id, seq}", "WebSocket push: message, receipt and presence events", "GET /conversations/{id}/messages?before=seq&limit=50"],
  data=["messages(conversation_id PARTITION, seq CLUSTERING, sender_id, text, sent_at) in a wide-column store", "conversations and members in a relational DB; presence in Redis with expiry"],
  design=["Clients keep a WebSocket to a gateway; a session registry (Redis) maps user → gateway so the message service can route to the right connection.",
          "The message service assigns a per-conversation sequence number, stores the message, then fans out to online members and queues push notifications for offline ones.",
          "Delivery is at-least-once; clients dedupe with client_msg_id and order by seq.", "Large groups: cap size or fan out through a queue so one message to 1,000 members does not block."],
  blocks=["load balancer", "websocket", "database", "sharding", "cache", "queue"],
  trade=[("Fan-out on write", "Simple and fast to read; expensive for very large groups."), ("Store-then-deliver", "Never loses a message; adds a write before delivery (milliseconds).")],
  nodes=[("Clients", 0, 1), ("Load balancer", 1, 1), ("WebSocket gateways", 2, 1), ("Session registry (Redis)", 3, 0), ("Message service", 3, 1), ("Message store (wide-column)", 4, 1), ("Push queue", 4, 2), ("Push notifications", 5, 2)],
  edges=[(0, 1), (1, 2), (2, 4), (4, 3), (4, 5), (4, 2), (4, 6), (6, 7)]),
 dict(id="feed", title="News feed", kb="hld",
  func=["Create posts", "Follow users", "See a feed of posts from people you follow, newest or ranked first"],
  nonf=["Feed loads fast (cached)", "Eventual consistency is fine: a post can take seconds to appear", "Very read-heavy"],
  assume=dict(dau=100e6, feed_loads=10, posts_per_user=1, avg_followers=200),
  est=lambda a: [("Feed reads per second", a["dau"] * a["feed_loads"] / DAY), ("Posts per second", a["dau"] * a["posts_per_user"] / DAY),
                 ("Feed inserts per second if fanned out on write", a["dau"] * a["posts_per_user"] * a["avg_followers"] / DAY)],
  api=["POST /posts {text, media_ids}", "GET /feed?cursor=…&limit=20", "POST /users/{id}/follow"],
  data=["posts(post_id PK, author_id, text, media_url, created_at)", "follows(follower_id, followee_id)", "feed cache: per-user list of recent post ids (Redis)"],
  design=["Hybrid fan-out: for normal users, a worker pushes each new post id into followers' feed caches (fan-out on write); for accounts with millions of followers, merge their posts at read time (fan-out on read).",
          "Feed read: fetch post ids from the user's cache, then post bodies from a post cache, then rank.", "Media goes to object storage and is served through a CDN.", "Posting publishes to a queue, so the write returns quickly."],
  blocks=["load balancer", "cache", "queue", "database", "sharding", "object storage", "cdn"],
  trade=[("Fan-out on write vs read", "Write: fast reads, heavy writes for popular authors. Read: cheap writes, slow reads. Hybrid uses each where it fits."), ("Ranking", "Chronological is simple and predictable; ranked needs a scoring service and more data.")],
  nodes=[("Clients", 0, 1), ("API gateway", 1, 1), ("Post service", 2, 0), ("Feed service", 2, 2), ("Fan-out queue + workers", 3, 0), ("Feed cache (Redis)", 3, 2), ("Posts DB", 3, 1), ("Object storage + CDN", 4, 0)],
  edges=[(0, 1), (1, 2), (1, 3), (2, 6), (2, 4), (4, 5), (3, 5), (3, 6), (2, 7)]),
 dict(id="notify", title="Notification service", kb="hld",
  func=["Send push, SMS and email notifications for other services", "Respect user preferences and quiet hours", "Templates and per-channel retries"],
  nonf=["No duplicates for the same event; no notification lost", "Absorb spikes (sales, outages)", "Each channel's provider failure must not block the others"],
  assume=dict(per_day=1e9, peak=5),
  est=lambda a: [("Average notifications/s", a["per_day"] / DAY), ("Peak notifications/s (×5)", a["per_day"] / DAY * a["peak"])],
  api=["POST /notifications {idempotency_key, user_id, template_id, data, channels, priority} → 202 Accepted", "GET /notifications/{id} → status per channel"],
  data=["requests(idempotency_key UNIQUE, user_id, template_id, status, created_at)", "preferences(user_id, channel, enabled, quiet_hours)", "templates(id, channel, body)"],
  design=["API validates, dedupes on the idempotency key, checks preferences and rate limits per user, then writes to one queue per channel (and priority).",
          "Channel workers render templates and call providers (APNs/FCM, an SMS gateway, an email service) with retries and exponential backoff; failures after N tries go to a dead-letter queue.",
          "Separate queues per channel isolate failures: an SMS outage does not delay push.", "Delivery status events are stored and exposed for debugging."],
  blocks=["load balancer", "queue", "database", "rate limiting", "monitoring"],
  trade=[("At-least-once delivery", "Simpler and safer than exactly-once; needs idempotency keys to avoid duplicates."), ("Priority queues", "Urgent messages (OTPs) bypass bulk campaigns; more queues to run.")],
  nodes=[("Calling services", 0, 1), ("Notification API", 1, 1), ("Prefs + dedupe DB", 2, 0), ("Push queue", 2, 1), ("SMS / email queues", 2, 2), ("Channel workers", 3, 1), ("Providers (FCM, SMS, email)", 4, 1), ("Dead-letter queue", 4, 2)],
  edges=[(0, 1), (1, 2), (1, 3), (1, 4), (3, 5), (4, 5), (5, 6), (5, 7)]),
 dict(id="files", title="File storage and sync", kb="hld",
  func=["Upload, download and share files", "Sync changes across a user's devices", "Version history"],
  nonf=["Never lose a file (high durability)", "Large files resume after a network drop", "Save bandwidth: only changed parts are uploaded"],
  assume=dict(dau=10e6, uploads_per_user=2, avg_file_mb=1, chunk_mb=4),
  est=lambda a: [("Uploads per second", a["dau"] * a["uploads_per_user"] / DAY), ("New data per day (bytes)", a["dau"] * a["uploads_per_user"] * a["avg_file_mb"] * 1e6),
                 ("New data per year (bytes)", a["dau"] * a["uploads_per_user"] * a["avg_file_mb"] * 1e6 * 365), ("Chunks for a 1 GB file (4 MB chunks)", 1000 / a["chunk_mb"])],
  api=["POST /files/{path}/uploads → {upload_id, missing_chunk_hashes}", "PUT pre-signed URL per chunk (directly to object storage)", "POST /uploads/{id}/commit → new version", "GET /changes?cursor=… (long poll) for sync"],
  data=["files(file_id, owner_id, path, latest_version)", "versions(file_id, version, chunk_hashes[], size, created_at)", "chunks stored in object storage by content hash (deduplicated)"],
  design=["Clients split files into 4 MB chunks and hash them; the server answers which hashes it does not have, so unchanged chunks are never uploaded again.",
          "Chunks go straight to object storage with pre-signed URLs; the metadata service records the new version only after all chunks exist (commit).",
          "Other devices learn about changes through a change log they long-poll (or a notification), then download only missing chunks.", "Metadata in a relational database (sharded by owner); downloads through a CDN for shared links."],
  blocks=["load balancer", "object storage", "database", "sharding", "cdn", "queue"],
  trade=[("Chunk size", "Smaller chunks save bandwidth on edits but mean more metadata and requests."), ("Conflicts", "Two devices editing offline: keep both versions and let the user choose, rather than silently overwriting.")],
  nodes=[("Desktop / phone client", 0, 1), ("Load balancer", 1, 1), ("Metadata service", 2, 1), ("Metadata DB (sharded)", 3, 0), ("Object storage (chunks)", 3, 2), ("Change log + notifier", 3, 1), ("CDN", 4, 2)],
  edges=[(0, 1), (1, 2), (2, 3), (2, 5), (0, 4), (5, 0), (4, 6)]),
]
for d in D:   # check against the System Design one-pager: approach steps present, building blocks from its vocabulary
    assert set(d["blocks"]) <= BLOCKS and len(d["blocks"]) >= 4, d["id"]
    assert d["func"] and d["nonf"] and d["api"] and d["data"] and d["design"] and d["trade"]
    d["estimates"] = [(k, v) for k, v in d["est"](d["assume"])]
assert abs(D[0]["estimates"][0][1] - 38.58) < 0.01 and D[0]["estimates"][4][1] == 3_521_614_606_208
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
    out = [f'''<section class="cover"><p class="eb">SYSTEM DESIGN · CASE STUDIES</p><h1>Five designs<br><span>worked end to end</span></h1>
<p class="lead">URL shortener, chat, news feed, notifications and file sync, each following the approach on the System Design one-pager: requirements → estimates → API → data model → design → trade-offs, with a diagram. Every estimate is computed from the stated assumptions, so you can change an assumption and redo the maths the same way.</p>
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
    (SRC / "sd.html").write_text(f'<!doctype html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700&family=Inter:wght@400;600;700&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet"><style>{CSS}</style></head><body><div id="top"></div>{body(pages)}</body></html>')
    js.write_text("const { chromium } = require('playwright'); (async () => { const b = await chromium.launch(); const p = await b.newPage(); await p.goto('file://' + __dirname + '/sd.html', { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready); await p.pdf({ path: __dirname + '/" + name + "', format: 'A4', printBackground: true, preferCSSPageSize: true }); await b.close(); })();")
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
w.add_metadata({"/Title": "System design case studies"}); w.write(str(OUT / "system-design-case-studies.pdf"))
for f in ("p1.pdf", "p2.pdf", "r.js", "sd.html"): (SRC / f).unlink()
print(NP, "pages", d2); [print(d["id"], [(k, human(v)) for k, v in d["estimates"]]) for d in D]
