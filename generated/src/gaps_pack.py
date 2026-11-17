"""Gap-fill pack: everything in the external roadmap the kit did not already cover. Run from the repo root: python3 generated/src/gaps_pack.py"""
import html, subprocess, pathlib, io, tempfile
from pypdf import PdfReader, PdfWriter
from pypdf.generic import Fit
from reportlab.pdfgen import canvas
ROOT = pathlib.Path(__file__).resolve().parents[2]; OUT = ROOT / "generated"; SRC = OUT / "src"; LLD = OUT / "gaps"
E = lambda s: html.escape(str(s), quote=True)
KB = "https://claude.ai/artifact/McuS723LTAb16Q6SpdUsAT#"
D = [
 ("invert_tree", "Invert Binary Tree (the one DSA gap)", "The only must-solve problem from the external roadmap that is in neither your worked solutions nor your A2Z sheet.",
  ["Swap the left and right child of every node", "Return the root", "Empty tree returns null"],
  """invertRec(root):  swap children, recurse on both     O(n) time, O(h) stack
invertBfs(root):  queue; swap children of each node   O(n) time, O(width) queue""",
  ["Recursion is the 3-line answer; BFS avoids deep recursion on a skewed tree.", "The test checks the level order 4, 7, 2, 9, 6, 3, 1 for both versions."],
  ["Is a tree symmetric? (compare left with the mirror of right)", "Do it without extra space (Morris-style traversal)."]),
 ("atm", "ATM (LLD)", "A classic state-machine LLD round; the external roadmap lists it and LLD packs I–II did not have it.",
  ["Insert card, enter PIN (3 tries, then the card is retained), withdraw, eject", "Withdrawals in multiples of 100, limited by balance and by the notes in the machine", "Only one card at a time"],
  """ATM ──> Bank (accounts: card -> {pin, balance})
  - state: Idle | CardInserted | Authenticated
  - notes: note value -> count
  + insert(card)  + enterPin(pin)  + withdraw(amount)  + eject()
  - plan(amount) -> notes?     (greedy, largest note first)""",
  ["Explicit state enum: every operation checks the state first, so illegal sequences are rejected.", "Debit the bank only after the machine knows it can dispense; otherwise money is taken but not given.", "Greedy note selection is optimal for 100/200/500/2000; the test proves it against brute force for every amount up to 5,000."],
  ["Model states as classes (State pattern) when each state has many operations.", "Concurrency between the ATM and the bank: reserve, dispense, then commit.", "What if the dispenser jams after debiting? (reversal transaction)"]),
 ("food_ordering", "Food ordering (machine coding)", "Zomato/Swiggy-style machine-coding round: entities, a state machine and pricing rules.",
  ["Restaurants with menus; unavailable items cannot be added", "A cart holds items from one restaurant only", "Coupons (flat or percentage with a cap) and 5% tax", "Order states PLACED → ACCEPTED → PREPARING → OUT_FOR_DELIVERY → DELIVERED; cancel only before PREPARING"],
  """FoodApp
  - restaurants: id -> Restaurant { menu: id -> MenuItem }
  - carts: user -> (restaurant, items)
  - orders[]
Coupon <<interface>> discount(subtotal)  ├── FlatOff  └── PercentOff
  + addToCart  + price(user, coupon) -> Bill  + checkout  + advance(orderId, status)""",
  ["Coupons are a Strategy: a new offer is a new class.", "Transitions are checked in one function, so illegal jumps (PLACED → PREPARING, cancelling after PREPARING) are rejected.", "Money in whole rupees as integers; the test checks a full bill (280 − 50 + 11 = 241)."],
  ["Assign a delivery agent (nearest free agent) and track location.", "Restaurant opening hours and item stock.", "Splitting one cart across restaurants into several orders."]),
 ("eviction_cache", "Cache with pluggable eviction (machine coding)", "Tests interfaces and O(1) data structures together: LRU and LFU behind one EvictionPolicy.",
  ["get and put in O(1)", "Fixed capacity; evict according to a policy chosen at construction", "LRU and LFU (ties in LFU: least recently used first)"],
  """EvictionPolicy<K> <<interface>> touched(k) added(k) removed(k) victim()
   ├── LRU<K>  (list + map to list positions)
   └── LFU<K>  (frequency -> list buckets, map to positions, minFreq)
Cache<K, V> ◆── data map, ──> EvictionPolicy""",
  ["The cache never knows which policy it uses (Strategy + dependency injection).", "LFU tracks the minimum frequency so victim() is O(1) amortised.", "Tests cover LRU order, LFU frequency and tie-break, and capacity 0."],
  ["TTL on top (see the key–value store in LLD pack II).", "Thread safety: one mutex, or sharding by key.", "FIFO or random policies as one more class each."]),
 ("inventory", "Inventory management (machine coding)", "Entities, validation and an Observer for low-stock alerts.",
  ["Products with SKU, category, quantity and reorder level", "Stock in and stock out with validation", "Alert subscribers once when stock falls to the reorder level", "List by category and list low-stock items"],
  """Inventory
  - items: sku -> Product { name, category, qty, reorderLevel }
  - subscribers: function(Product)
  + add  + stockIn  + stockOut -> bool  + byCategory  + lowStock  + subscribe""",
  ["Alerts fire on crossing the level, not on every sale below it, so subscribers are not spammed.", "Invalid quantities and duplicate SKUs are rejected.", "Observer as a list of callbacks: email, dashboard and reorder service can subscribe independently."],
  ["Multiple warehouses and transfers between them.", "Reservations for pending orders (see the checkout design in system design II).", "Audit log of every stock change."]),
 ("ds_math", "Segment tree, Fenwick tree and number theory", "Phase 7 of the external roadmap: range queries and the maths that OAs reuse.",
  ["Range sum with point updates in O(log n): segment tree and Fenwick tree", "All primes up to N: sieve of Eratosthenes", "Fast modular power, modular inverse (prime modulus), gcd and lcm"],
  """SegTree(a)   set(i, v)   sum(l, r)   iterative, 2n array
BIT(n)       add(i, d)   prefix(i)   sum(l, r)
sieve(n) -> primes   modpow(b, e, m)   modinv(a, p) = a^(p-2) mod p""",
  ["Both trees are checked against brute-force sums over 2,000 random updates and queries.", "The sieve gives 78,498 primes below 10^6 (the known count).", "modpow uses 128-bit products so b × b never overflows for moduli near 10^18."],
  ["Range updates with lazy propagation; range minimum instead of sum.", "Count inversions or 'smaller after self' with a BIT (OA pack II has one).", "Segmented sieve for primes in a range [L, R]."]),
]
def run_all():
    tmp = tempfile.mkdtemp()
    for slug, *_ in D:
        exe = f"{tmp}/{slug}"
        c = subprocess.run(["g++", "-std=c++17", "-Wall", "-Wextra", "-O1", "-fsanitize=address,undefined", "-fno-sanitize-recover=all", "-pthread", str(LLD / f"{slug}.cpp"), "-o", exe], capture_output=True, text=True)
        assert c.returncode == 0 and "warning" not in c.stderr, c.stderr
        r = subprocess.run([exe], capture_output=True, text=True); assert r.returncode == 0, r.stderr
    return "all six programs compile with -Wall -Wextra and pass their checks under AddressSanitizer and UndefinedBehaviorSanitizer"
STATUS = run_all()
IG = dict(dau=100e6, uploads_per_user=0.1, photo_mb=2, thumbs_factor=0.2, feed_views=20, peak=3)
IG_EST = [("Photos uploaded per day", IG["dau"] * IG["uploads_per_user"]), ("Photo storage per day incl. thumbnails (bytes)", IG["dau"] * IG["uploads_per_user"] * IG["photo_mb"] * 1e6 * (1 + IG["thumbs_factor"])),
          ("Storage per year (bytes)", IG["dau"] * IG["uploads_per_user"] * IG["photo_mb"] * 1e6 * (1 + IG["thumbs_factor"]) * 365), ("Feed requests per day", IG["dau"] * IG["feed_views"]),
          ("Average feed requests/s", IG["dau"] * IG["feed_views"] / 86400), ("Peak feed requests/s", IG["dau"] * IG["feed_views"] / 86400 * IG["peak"])]
assert IG_EST[0][1] == 10e6 and round(IG_EST[1][1]) == 24e12 and round(IG_EST[4][1]) == 23148
def hum(x): return next((f"{x / d:,.1f} {u}" for d, u in ((1e15, "P"), (1e12, "T"), (1e9, "G"), (1e6, "M"), (1e3, "K")) if x >= d), f"{x:,.0f}")
HLD_HTML = f'''<section class="sec" id="instagram"><h2><span class="num">07</span>Instagram-style photo sharing (HLD)<a class="back" href="#top">↑ Index</a></h2><p class="meta">The one HLD from the external roadmap that the two system design packs did not cover end to end (the news-feed design covers the feed half).</p>
<div class="two"><div><h3>Requirements</h3><ul><li>Upload photos with captions; view a profile grid</li><li>Follow users; home feed of followed users' photos, newest first</li><li>Likes and comments</li><li>Fast feed loads worldwide; uploads durable; feed can be a few seconds stale</li></ul></div>
<div><h3>Estimates (assumptions: 100 M daily users, 0.1 uploads and 20 feed views per user a day, 2 MB per photo)</h3><ul>{"".join(f"<li>{E(k)}: <b>{hum(v)}</b></li>" for k, v in IG_EST)}</ul></div></div>
<h3>Design</h3><pre class="cls">Client ──> CDN (images) ──> Object storage (originals + resized versions)
Client ──> Load balancer ──> API servers ──> Post service ──> Posts DB (sharded by user_id)
                                 │                  └──> upload event ──> Queue ──> Resize workers ──> Object storage
                                 ├──> Feed service ──> Feed cache (Redis: user -> recent post ids)
                                 └──> Graph service ──> Follows DB       Fan-out workers <── Queue (new post)</pre>
<ul><li><b>Upload:</b> the client gets a pre-signed URL and uploads straight to object storage; a queue event triggers resizing into thumbnails; the post row stores the object keys.</li>
<li><b>Feed:</b> fan-out on write for normal users (push the new post id into each follower's feed cache); for accounts with millions of followers, pull their recent posts at read time and merge (the "celebrity problem").</li>
<li><b>Reads:</b> the feed service returns post ids from cache, hydrates them from a post cache, and image URLs point at the CDN.</li>
<li><b>Data:</b> posts(post_id, user_id, caption, keys, created_at) sharded by user_id; follows(follower, followee) indexed both ways; likes counted asynchronously.</li></ul>
<h3>Trade-offs and follow-ups</h3><ul><li>Push vs pull feeds: push makes reads cheap but writes heavy for big accounts; the hybrid fixes both.</li><li>Ranking instead of newest-first: a ranking service scores candidate posts.</li><li>Deleting a post must remove it from every pushed feed: store ids only and filter deleted ones at read time.</li></ul></section>'''
def body(pages):
    pg = lambda k: str(pages.get(k, "000")) if pages else "000"
    rows = "".join(f'<tr><td class="n">{i + 1}</td><td><a href="#{s}">{E(t)}</a><div class="f">{E(w)}</div></td><td><code>gaps/{s}.cpp</code></td><td class="pg"><a href="#{s}">{pg(s)}</a></td></tr>' for i, (s, t, w, *_r) in enumerate(D)) + f'<tr><td class="n">7</td><td><a href="#instagram">Instagram-style photo sharing (HLD)</a><div class="f">Upload pipeline, hybrid push/pull feed, estimates</div></td><td>—</td><td class="pg"><a href="#instagram">{pg("instagram")}</a></td></tr>'
    out = [f'''<section class="cover"><p class="eb">GAP-FILL · FROM THE EXTERNAL ROADMAP</p><h1>The missing pieces<br><span>with code that runs</span></h1>
<p class="lead">Everything the external 6-month roadmap (Google Doc) lists that your kit did not already cover: one DSA problem, the ATM LLD, three machine-coding problems, segment and Fenwick trees with number theory, and an Instagram-style HLD at the end. Each has the requirements to state first, a class diagram in text, the key design decisions, follow-up questions, and a complete C++17 program with a demo that checks its own behaviour. Status: {E(STATUS)}.</p>
<p class="how"><b>How to practise.</b> Read the requirements, set a 45-minute timer, and write your own design and code before you look. Then compare decisions, not just syntax. In the interview: clarify requirements, list entities, draw classes and relationships, write the core methods, then discuss extensions. See the <a href="{KB}oop">OOP</a> and <a href="{KB}solid">SOLID</a> Knowledge Base pages.</p>
<table class="ix"><thead><tr><th>#</th><th>Design</th><th>Code</th><th>Page</th></tr></thead><tbody>{rows}</tbody></table>
<p class="src">Compile any design: <code>g++ -std=c++17 -Wall -pthread gaps/atm.cpp &amp;&amp; ./a.out</code></p></section>''']
    for i, (s, t, w, req, cls, dec, fol) in enumerate(D):
        code = (LLD / f"{s}.cpp").read_text()
        out.append(f'''<section class="sec" id="{s}"><h2><span class="num">{i + 1:02d}</span>{E(t)}<a class="back" href="#top">↑ Index</a></h2><p class="meta">{E(w)}</p>
<div class="two"><div><h3>Requirements to confirm</h3><ul>{"".join(f"<li>{E(x)}</li>" for x in req)}</ul></div><div><h3>Design decisions</h3><ul>{"".join(f"<li>{E(x)}</li>" for x in dec)}</ul></div></div>
<h3>Classes</h3><pre class="cls">{E(cls)}</pre><h3>Follow-up questions</h3><ul>{"".join(f"<li>{E(x)}</li>" for x in fol)}</ul>
<h3>C++17 code (<code>gaps/{s}.cpp</code>)</h3><pre>{E(code)}</pre></section>''')
    out.append(HLD_HTML)
    return "".join(out)
CSS = """@page { size: A4; margin: 12mm 12mm 14mm; } @page :first { margin: 0; }
* { box-sizing: border-box; } html { -webkit-print-color-adjust: exact; print-color-adjust: exact; } body { margin: 0; font: 400 8.8pt/1.42 Inter, sans-serif; color: #1e293b; }
a { color: #c2410c; text-decoration: none; } .cover { padding: 16mm 15mm; break-after: page; } code { font: 600 7.8pt "JetBrains Mono"; }
.eb { font: 600 8pt "JetBrains Mono"; letter-spacing: .14em; color: #c2410c; margin: 0 0 3mm; } h1 { font: 700 34pt/1.02 "Space Grotesk"; margin: 0 0 4mm; color: #0f172a; } h1 span { color: #c2410c; font-size: 20pt; }
.lead { font-size: 10pt; color: #475569; } .how { background: #fff7ed; border-left: 3px solid #c2410c; padding: 2mm 3mm; } table { border-collapse: collapse; width: 100%; }
th { font: 600 7pt "JetBrains Mono"; text-transform: uppercase; color: #64748b; background: #f1f5f9; padding: 1.3mm 2mm; text-align: left; }
.ix td { padding: 2mm; border-bottom: 1px solid #e2e8f0; vertical-align: top; } .ix td a { color: #0f172a; font-weight: 600; font-size: 10pt; } .ix .f { font-size: 8pt; color: #64748b; } .ix .n { color: #94a3b8; font-family: "JetBrains Mono"; } .ix .pg { text-align: right; } .ix .pg a { color: #c2410c; font-family: "JetBrains Mono"; }
.src { font-size: 8pt; color: #64748b; margin-top: 4mm; } .sec { break-before: page; } h2 { font: 700 15pt "Space Grotesk"; color: #0f172a; border-bottom: 3px solid #c2410c; padding-bottom: 1.5mm; margin: 0 0 2mm; display: flex; align-items: baseline; gap: 3mm; }
.num { font: 600 10pt "JetBrains Mono"; color: #c2410c; } .back { margin-left: auto; font: 600 7.5pt "JetBrains Mono"; border: 1px solid #fdba74; background: #fff7ed; border-radius: 99px; padding: 0 7px; }
.meta { color: #475569; margin: 0 0 2mm; } h3 { font: 700 9.8pt "Space Grotesk"; color: #1d4ed8; margin: 3mm 0 1mm; } ul { padding-left: 5mm; margin: 0; } li { margin-bottom: .8mm; } .two { display: grid; grid-template-columns: 1fr 1fr; gap: 6mm; }
pre { font: 400 6.9pt/1.36 "JetBrains Mono"; background: #f8fafc; border: 1px solid #e2e8f0; border-left: 3px solid #1d4ed8; padding: 2mm 2.5mm; white-space: pre-wrap; margin: 0; }
pre.cls { border-left-color: #16a34a; font-size: 7.6pt; } pre { font-variant-ligatures: none; font-feature-settings: "liga" 0, "calt" 0; }"""
js = SRC / "r.js"
def render(pages, name):
    (SRC / "gaps.html").write_text(f'<!doctype html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700&family=Inter:wght@400;600&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet"><style>{CSS}</style></head><body><div id="top"></div>{body(pages)}</body></html>')
    js.write_text("const { chromium } = require('playwright'); (async () => { const b = await chromium.launch(); const p = await b.newPage(); await p.goto('file://' + __dirname + '/gaps.html', { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready); await p.pdf({ path: __dirname + '/" + name + "', format: 'A4', printBackground: true, preferCSSPageSize: true }); await b.close(); })();")
    subprocess.run(["node", str(js)], check=True)
    r = PdfReader(str(SRC / name)); return {k.lstrip("/"): r.get_destination_page_number(v) + 1 for k, v in r.named_destinations.items()}, len(r.pages)
d1, n1 = render(None, "p1.pdf"); d2, n2 = render(d1, "p2.pdf"); assert n1 == n2 and all(d1[s] == d2[s] for s, *_ in D)
w = PdfWriter(clone_from=PdfReader(str(SRC / "p2.pdf"))); w.add_outline_item("Index", 0, fit=Fit.fit())
for s, t, *_ in D: w.add_outline_item(t, d2[s] - 1, fit=Fit.fit())
NP = len(w.pages)
for i, pg in enumerate(w.pages):
    if i == 0: continue
    buf = io.BytesIO(); c = canvas.Canvas(buf, pagesize=(float(pg.mediabox.width), float(pg.mediabox.height))); c.setFont("Helvetica", 7.5); c.setFillGray(.55)
    c.drawRightString(float(pg.mediabox.width) - 26, 14, f"{i + 1} / {NP}"); c.save(); buf.seek(0); pg.merge_page(PdfReader(buf).pages[0]); pg.compress_content_streams(level=9)
w.add_outline_item("7. Instagram-style photo sharing (HLD)", d2["instagram"] - 1, fit=Fit.fit())
w.add_metadata({"/Title": "Gap-fill pack"}); w.write(str(OUT / "gap-fill-pack.pdf"))
for f in ("p1.pdf", "p2.pdf", "r.js", "gaps.html"): (SRC / f).unlink()
print(NP, "pages", {s: d2[s] for s, *_ in D})
