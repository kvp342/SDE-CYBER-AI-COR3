"""LLD pack PDF: six designs with requirements, class diagrams in text, decisions, follow-ups and the tested C++17 code.
Run from the repo root: python3 generated/src/lld_pack.py (compiles and runs every design first)."""
import html, subprocess, pathlib, io, tempfile
from pypdf import PdfReader, PdfWriter
from pypdf.generic import Fit
from reportlab.pdfgen import canvas
ROOT = pathlib.Path(__file__).resolve().parents[2]; OUT = ROOT / "generated"; SRC = OUT / "src"; LLD = OUT / "lld"
E = lambda s: html.escape(str(s), quote=True)
KB = "https://claude.ai/artifact/McuS723LTAb16Q6SpdUsAT#"
D = [
 ("parking_lot", "Parking lot", "A common machine-coding question; tests modelling and extensibility.",
  ["Levels with spots of three sizes; bikes, cars and trucks", "Park in the nearest spot that fits; issue a ticket", "Charge on exit by started hour and vehicle size", "Report free spots"],
  """Vehicle { plate, size }            Spot { level, number, size, plate? }
Ticket { id, plate, level, spot, entryMinute }
PricingStrategy <<interface>>  fee(size, minutes)
   └── HourlyPricing
ParkingLot ◆── Spot[levels][spots]
           ◆── Ticket (active, by id)
           ──> PricingStrategy
  park(vehicle, minute) -> Ticket?    leave(ticketId, minute) -> fee""",
  ["Strategy pattern for pricing: weekend or flat-rate pricing is a new class, not an edit to ParkingLot (open/closed).", "Smallest spot that fits on the lowest level keeps large spots free for trucks.", "Money as integers; time passed in so tests are deterministic."],
  ["Multiple entry gates at once: lock per level, or an atomic spot claim.", "Electric-vehicle charging spots and reservations.", "How would you find a free spot in O(1)? (free lists per size per level)"]),
 ("library", "Library management", "Classic OOP question: entities, state transitions and notifications.",
  ["Books with several copies; members with a loan limit", "Check out and return with a due date; fine for late returns", "Reserve a book when no copy is free; notify the first waiting member", "A held copy can only be taken by that member"],
  """Book { isbn, title }   Copy { id, isbn, status: Available | Loaned | OnHold }
Member { id, name, maxLoans }   Loan { copyId, memberId, day, due }
Library ◆── Book, Copy, Member, Loan
        ◆── holds: isbn -> queue<memberId>
        ──> listeners (Observer)  notify(memberId, message)
  checkout(member, isbn, day)  giveBack(copy, day) -> fine  reserve(member, isbn)""",
  ["Copy status is a small state machine: Available → Loaned → (OnHold →) Loaned → Available.", "Observer for notifications: email or SMS senders subscribe without the Library knowing about them.", "FIFO queue per ISBN makes holds fair."],
  ["Hold expiry if the member does not collect in 3 days.", "Search by title or author (an index or full-text search).", "Concurrency: two members checking out the last copy at once."]),
 ("splitwise", "Splitwise (expense sharing)", "A common machine-coding question; tests money handling and a small algorithm.",
  ["Add an expense paid by one person and split among several", "Equal, exact-amount and percentage splits", "Show each person's net balance", "Suggest a short list of payments that settles everyone"],
  """SplitStrategy <<interface>>  shares(total, people) -> amounts
   ├── EqualSplit   ├── ExactSplit(amounts)   └── PercentSplit(percentages)
Ledger ◆── net: user -> paise (positive = is owed)
  addExpense(payer, total, people, strategy)   balance(user)   settle() -> [(from, to, amount)]""",
  ["Paise as 64-bit integers: no floating-point rounding; remainders go to named people so totals always match.", "Validation in each strategy (exact amounts add up, percentages add to 100).", "Settlement: greedy largest debtor pays largest creditor, at most n − 1 payments (minimum count is NP-hard in general)."],
  ["Groups, currencies and exchange rates.", "Editing or deleting an expense (store expenses, recompute balances).", "Why is the minimum number of transactions hard? (subset-sum style partitioning)"]),
 ("elevator", "Elevator system", "Tests state modelling and a scheduling policy; interviewers care about the reasoning.",
  ["Several cars; hall calls (from a floor) and car calls (from inside)", "Assign each hall call to the best car", "Cars serve stops in their direction before reversing (LOOK)", "Simulate time in ticks"],
  """Dir { Idle, Up, Down }
Elevator { id, floor, dir, stops: ordered set<int> }
  addStop(f)  cost(f)  step()
Controller ◆── Elevator[]
  hallCall(floor) -> car id   carCall(car, floor)   tick(n)""",
  ["An ordered set of stops gives the next stop up or down in O(log n).", "LOOK scheduling avoids starvation better than nearest-first.", "Cost = distance, plus the detour if the car must finish its sweep first."],
  ["Capacity and weight limits; express elevators for high floors.", "Peak-hour policies (morning up-peak).", "Making controller and cars run on separate threads safely."]),
 ("rate_limiter", "Rate limiter", "Common in backend and security interviews; also a system design building block.",
  ["Limit requests per client", "Allow short bursts but cap the average rate", "Exact limits for sensitive endpoints such as login", "Safe under concurrent requests"],
  """RateLimiter <<interface>>  allow(client) -> bool
   ├── TokenBucket(capacity, ratePerSec, clock)      buckets: client -> {tokens, last}
   └── SlidingWindowLog(limit, windowSec, clock)    log: client -> deque<timestamps>
Clock = function<double()>  (injected; tests use a fake clock)""",
  ["Token bucket: O(1) memory per client, allows bursts; sliding log: exact but stores every timestamp.", "Clock injection makes time-based tests deterministic.", "A mutex guards shared state; tested with 8 threads (exactly capacity granted) and ThreadSanitizer."],
  ["Distributed limiting: Redis with atomic scripts, or a gateway.", "Sliding window counter (two fixed windows weighted) as a cheaper approximation.", "What to return: HTTP 429 with Retry-After."]),
 ("lru_cache", "LRU cache", "Asked as both DSA (LeetCode 146) and LLD; generic and O(1) is expected.",
  ["get(key) and put(key, value) in O(1)", "Evict the least recently used item when full", "Updating a key refreshes it", "Generic key and value types"],
  """LRUCache<K, V>
  cap
  items: list<pair<K, V>>          front = most recent
  pos:   unordered_map<K, list iterator>
  get(k) -> optional<V>   put(k, v)   size()""",
  ["list::splice moves a node to the front without invalidating iterators.", "optional<V> instead of a sentinel value such as -1.", "Capacity 0 rejected in the constructor."],
  ["Thread safety: one mutex, or sharded caches.", "LFU, TTL expiry, or size-based eviction.", "Why not std::map? (O(log n) and no recency order)"]),
]
def run_all():
    tmp = tempfile.mkdtemp()
    for slug, *_ in D:
        exe = f"{tmp}/{slug}"
        c = subprocess.run(["g++", "-std=c++17", "-Wall", "-Wextra", "-O1", "-fsanitize=address,undefined", "-fno-sanitize-recover=all", "-pthread", str(LLD / f"{slug}.cpp"), "-o", exe], capture_output=True, text=True)
        assert c.returncode == 0 and "warning" not in c.stderr, c.stderr
        r = subprocess.run([exe], capture_output=True, text=True); assert r.returncode == 0, r.stderr
    return "all six compile with -Wall -Wextra and pass their checks under AddressSanitizer and UndefinedBehaviorSanitizer"
STATUS = run_all()
def body(pages):
    pg = lambda k: str(pages.get(k, "000")) if pages else "000"
    rows = "".join(f'<tr><td class="n">{i + 1}</td><td><a href="#{s}">{E(t)}</a><div class="f">{E(w)}</div></td><td><code>lld/{s}.cpp</code></td><td class="pg"><a href="#{s}">{pg(s)}</a></td></tr>' for i, (s, t, w, *_r) in enumerate(D))
    out = [f'''<section class="cover"><p class="eb">LOW-LEVEL DESIGN · 6 DESIGNS</p><h1>LLD pack<br><span>with code that runs</span></h1>
<p class="lead">Six designs that come up in machine-coding and LLD rounds. Each has the requirements to state first, a class diagram in text, the key design decisions, follow-up questions, and a complete C++17 program with a demo that checks its own behaviour. Status: {E(STATUS)}.</p>
<p class="how"><b>How to practise.</b> Read the requirements, set a 45-minute timer, and write your own design and code before you look. Then compare decisions, not just syntax. In the interview: clarify requirements, list entities, draw classes and relationships, write the core methods, then discuss extensions. See the <a href="{KB}oop">OOP</a> and <a href="{KB}solid">SOLID</a> Knowledge Base pages.</p>
<table class="ix"><thead><tr><th>#</th><th>Design</th><th>Code</th><th>Page</th></tr></thead><tbody>{rows}</tbody></table>
<p class="src">Compile any design: <code>g++ -std=c++17 -Wall -pthread lld/parking_lot.cpp &amp;&amp; ./a.out</code></p></section>''']
    for i, (s, t, w, req, cls, dec, fol) in enumerate(D):
        code = (LLD / f"{s}.cpp").read_text()
        out.append(f'''<section class="sec" id="{s}"><h2><span class="num">{i + 1:02d}</span>{E(t)}<a class="back" href="#top">↑ Index</a></h2><p class="meta">{E(w)}</p>
<div class="two"><div><h3>Requirements to confirm</h3><ul>{"".join(f"<li>{E(x)}</li>" for x in req)}</ul></div><div><h3>Design decisions</h3><ul>{"".join(f"<li>{E(x)}</li>" for x in dec)}</ul></div></div>
<h3>Classes</h3><pre class="cls">{E(cls)}</pre><h3>Follow-up questions</h3><ul>{"".join(f"<li>{E(x)}</li>" for x in fol)}</ul>
<h3>C++17 code (<code>lld/{s}.cpp</code>)</h3><pre>{E(code)}</pre></section>''')
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
    (SRC / "lld.html").write_text(f'<!doctype html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700&family=Inter:wght@400;600&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet"><style>{CSS}</style></head><body><div id="top"></div>{body(pages)}</body></html>')
    js.write_text("const { chromium } = require('playwright'); (async () => { const b = await chromium.launch(); const p = await b.newPage(); await p.goto('file://' + __dirname + '/lld.html', { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready); await p.pdf({ path: __dirname + '/" + name + "', format: 'A4', printBackground: true, preferCSSPageSize: true }); await b.close(); })();")
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
w.add_metadata({"/Title": "LLD pack: six designs with tested C++17"}); w.write(str(OUT / "lld-pack.pdf"))
for f in ("p1.pdf", "p2.pdf", "r.js", "lld.html"): (SRC / f).unlink()
print(NP, "pages", {s: d2[s] for s, *_ in D})
