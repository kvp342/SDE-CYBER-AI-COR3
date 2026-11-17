"""LLD pack II PDF: six more designs with requirements, class diagrams in text, decisions, follow-ups and tested C++17 code.
Run from the repo root: python3 generated/src/lld_pack2.py (compiles and runs every design first)."""
import html, subprocess, pathlib, io, tempfile
from pypdf import PdfReader, PdfWriter
from pypdf.generic import Fit
from reportlab.pdfgen import canvas
ROOT = pathlib.Path(__file__).resolve().parents[2]; OUT = ROOT / "generated"; SRC = OUT / "src"; LLD = OUT / "lld2"
E = lambda s: html.escape(str(s), quote=True)
KB = "https://claude.ai/artifact/McuS723LTAb16Q6SpdUsAT#"
D = [
 ("tic_tac_toe", "Tic-tac-toe (N × N)", "A favourite warm-up machine-coding round: clean state, validation and an O(1) win check.",
  ["Board size N, two players, X starts", "Reject moves outside the board, on a taken cell, out of turn, or after the game ends", "Detect win and draw after every move"],
  """Game
  - n, moves, turn
  - board[n][n]
  - rows[n], cols[n], diag, anti     (+1 for X, -1 for O)
  + play(player, r, c) -> Ok | Win | Draw   (throws on illegal moves)
  + current() -> 'X' | 'O'""",
  ["Counters per row, column and diagonal make the win check O(1) instead of scanning the board (O(N)).", "Illegal moves throw with a clear message; the caller decides how to show them.", "The game owns its state; a UI or network layer only calls play()."],
  ["K-in-a-row on an M × N board (Gomoku): check runs from the last move.", "Undo: keep a move stack and reverse the counters.", "A bot player behind a Player interface (Strategy)."]),
 ("vending_machine", "Vending machine", "Tests state, money handling and an algorithm (change-making) in one design.",
  ["Items with codes, prices and stock", "Accept only some coins; show the balance", "Sell if the item exists, is in stock and is paid for, and exact change can be given", "Refund on request"],
  """VendingMachine
  - items: code -> Item { name, price, qty }
  - coins: value -> count      (machine's float)
  - inserted[], credit
  + insert(coin) -> bool       + select(code) -> Sale { ok, reason, change }
  + refund() -> coins          - makeChange(amount, stock) -> coins?  (bounded coin DP)""",
  ["Inserted coins join the float before change is computed, so they can be used for the change itself.", "Change uses a bounded-coin DP, not greedy: greedy fails when coins run out.", "Money as integers (smallest unit) to avoid floating-point errors."],
  ["Model states explicitly (Idle, HasMoney, Dispensing) with the State pattern.", "Card payments and a timeout that refunds automatically.", "Maintenance mode for restocking and collecting coins."]),
 ("movie_booking", "Movie ticket booking with seat holds", "The concurrency question behind BookMyShow-style designs: two people must never get one seat.",
  ["Show with named seats", "Hold several seats all-or-nothing for a few minutes", "Confirm only your own unexpired hold", "Expired holds free the seat", "Many users at once"],
  """Show
  - seats: id -> State { Free | Held | Booked, user, until }
  - mutex, clock, holdSecs
  + hold(user, seatIds) -> bool       (all or nothing)
  + confirm(user, seatIds) -> bool
  + status(seatId) -> Seat""",
  ["One mutex per show makes hold() atomic: the test races 16 threads for one seat and exactly one wins.", "Lazy expiry: a hold is checked when touched, so no timer thread is needed.", "The clock is injected, so expiry is tested without sleeping."],
  ["Scale out: per-show locks, or a database row lock / conditional update (UPDATE … WHERE status = 'Free').", "Payment failure after a hold: release, with an idempotent confirm.", "Distributed holds with Redis SET NX and a TTL."]),
 ("logger", "Logger with levels and sinks", "Shows interfaces, the open/closed principle and thread safety in a small space.",
  ["Levels DEBUG < INFO < WARN < ERROR", "Several outputs (console, memory, file), each with its own minimum level", "Consistent line format", "Safe to call from many threads"],
  """Sink <<interface>>  { min: Level; write(line) }
   ├── StreamSink(ostream)
   └── MemorySink (lines[])
Logger ◆── Sink[]
  + add(sink)   + log(level, msg)   + debug/info/warn/error(msg)""",
  ["New outputs are new Sink classes; Logger never changes (open/closed).", "Format once per call, then fan out to the sinks.", "One mutex around the fan-out: the test writes 2,000 lines from 8 threads with none lost."],
  ["Asynchronous logging with a queue and a background writer.", "Log rotation by size or date in a FileSink.", "Structured (JSON) logs for a SIEM."]),
 ("kv_store_ttl", "Key–value store with TTL", "A small Redis: data structures, expiry and a subtle overwrite bug.",
  ["set(key, value, ttl?) / get / del", "Expired keys behave as missing", "Expired keys are cleaned up without scanning everything", "Overwriting a key replaces its expiry"],
  """KV
  - map: key -> Entry { value, expires, version }
  - heap: min (expires, version, key)
  - clock
  + set(k, v, ttl)   + get(k) -> value?   + del(k)   + cleanup() -> removed""",
  ["Two expiry paths: lazy on get, and cleanup() popping the min-heap (Redis also combines lazy and active expiry).", "A version number per write: an old heap entry for an overwritten key is skipped instead of deleting the new value (the test checks exactly this).", "Expiry is exclusive at the deadline; the test pins it."],
  ["LRU eviction when memory is full (combine with the LRU cache from pack I).", "Persistence: append-only log and snapshots.", "Thread safety and sharding by key hash."]),
 ("snake_ladder", "Snake and ladder", "Machine-coding staple: rules as data, players in a queue, testable randomness.",
  ["Board size and a set of snakes and ladders", "Players take turns; a six gives another roll", "Overshooting the last square means staying put", "First to land exactly on the last square wins", "Reject invalid boards"],
  """Game
  - size, jumps: from -> to       (snakes go down, ladders go up)
  - players: queue<(name, pos)>
  - dice: function<int()>         (injected: random in play, scripted in tests)
  + turn() -> name   + won() -> winner   + position(name)""",
  ["Snakes and ladders are one map of jumps; no separate classes are needed.", "Dice are injected, so tests script exact rolls (the 14 → 20 → snake → extra roll path is tested).", "The constructor validates the board (no jump from the last square, no jump onto another jump)."],
  ["Multiple dice, or a crooked dice for testing.", "Saving and resuming a game.", "Rule variations behind a Rules interface (Strategy)."]),
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
    rows = "".join(f'<tr><td class="n">{i + 1}</td><td><a href="#{s}">{E(t)}</a><div class="f">{E(w)}</div></td><td><code>lld2/{s}.cpp</code></td><td class="pg"><a href="#{s}">{pg(s)}</a></td></tr>' for i, (s, t, w, *_r) in enumerate(D))
    out = [f'''<section class="cover"><p class="eb">LOW-LEVEL DESIGN · 6 MORE DESIGNS</p><h1>LLD pack II<br><span>with code that runs</span></h1>
<p class="lead">Six more designs that come up in machine-coding and LLD rounds, none repeated from LLD pack I. Each has the requirements to state first, a class diagram in text, the key design decisions, follow-up questions, and a complete C++17 program with a demo that checks its own behaviour. Status: {E(STATUS)}.</p>
<p class="how"><b>How to practise.</b> Read the requirements, set a 45-minute timer, and write your own design and code before you look. Then compare decisions, not just syntax. In the interview: clarify requirements, list entities, draw classes and relationships, write the core methods, then discuss extensions. See the <a href="{KB}oop">OOP</a> and <a href="{KB}solid">SOLID</a> Knowledge Base pages.</p>
<table class="ix"><thead><tr><th>#</th><th>Design</th><th>Code</th><th>Page</th></tr></thead><tbody>{rows}</tbody></table>
<p class="src">Compile any design: <code>g++ -std=c++17 -Wall -pthread lld2/tic_tac_toe.cpp &amp;&amp; ./a.out</code></p></section>''']
    for i, (s, t, w, req, cls, dec, fol) in enumerate(D):
        code = (LLD / f"{s}.cpp").read_text()
        out.append(f'''<section class="sec" id="{s}"><h2><span class="num">{i + 1:02d}</span>{E(t)}<a class="back" href="#top">↑ Index</a></h2><p class="meta">{E(w)}</p>
<div class="two"><div><h3>Requirements to confirm</h3><ul>{"".join(f"<li>{E(x)}</li>" for x in req)}</ul></div><div><h3>Design decisions</h3><ul>{"".join(f"<li>{E(x)}</li>" for x in dec)}</ul></div></div>
<h3>Classes</h3><pre class="cls">{E(cls)}</pre><h3>Follow-up questions</h3><ul>{"".join(f"<li>{E(x)}</li>" for x in fol)}</ul>
<h3>C++17 code (<code>lld2/{s}.cpp</code>)</h3><pre>{E(code)}</pre></section>''')
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
    (SRC / "lld2.html").write_text(f'<!doctype html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700&family=Inter:wght@400;600&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet"><style>{CSS}</style></head><body><div id="top"></div>{body(pages)}</body></html>')
    js.write_text("const { chromium } = require('playwright'); (async () => { const b = await chromium.launch(); const p = await b.newPage(); await p.goto('file://' + __dirname + '/lld2.html', { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready); await p.pdf({ path: __dirname + '/" + name + "', format: 'A4', printBackground: true, preferCSSPageSize: true }); await b.close(); })();")
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
w.add_metadata({"/Title": "LLD pack II: six more designs"}); w.write(str(OUT / "lld-pack-2.pdf"))
for f in ("p1.pdf", "p2.pdf", "r.js", "lld2.html"): (SRC / f).unlink()
print(NP, "pages", {s: d2[s] for s, *_ in D})
