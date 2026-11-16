"""Elite track pack PDF: 40 checked probability questions (answers on separate pages) and 8 low-latency C++ exercises with measured timings.
Run from the repo root: python3 generated/src/elite_prob.py && python3 generated/src/elite_pack.py"""
import html, io, pathlib, subprocess, sys, tempfile
from pypdf import PdfReader, PdfWriter
from pypdf.generic import Fit
from reportlab.pdfgen import canvas
ROOT = pathlib.Path(__file__).resolve().parents[2]; OUT = ROOT / "generated"; SRC = OUT / "src"; EL = OUT / "elite"
sys.path.insert(0, str(SRC)); from elite_prob import Q
E = lambda s: html.escape(str(s), quote=True); KB = "https://claude.ai/artifact/McuS723LTAb16Q6SpdUsAT#"
EX = [("e1_aos_soa", "Data layout: array of structs vs struct of arrays", "Summing one field drags whole 72-byte records through the cache in AoS; SoA reads only the field you need.", "Why does SoA help vectorisation too?"),
      ("e2_traversal", "Traversal order", "Row-major arrays read sequentially are prefetched; column order jumps a full row each step and misses the cache.", "What about a matrix multiply? (loop order i-k-j)"),
      ("e3_spsc", "Lock-free SPSC ring buffer", "One producer, one consumer, acquire/release on head and tail, power-of-two capacity, head and tail on separate cache lines.", "Why is relaxed enough for a thread's own index? What changes for multiple producers?"),
      ("e4_pool", "Object pool with a free list", "Preallocate and recycle objects: no allocator call and no fragmentation on the hot path.", "How would you make it thread-safe? Per-thread pools."),
      ("e5_branchless", "Branch-free min, abs and clamp", "Sign-mask tricks replace unpredictable branches; check against std:: and read the assembly, because compilers often do this already.", "When does a branch beat branch-free code? (predictable data)"),
      ("e6_false_sharing", "False sharing", "Two threads writing different variables on one cache line still fight over the line; alignas(64) separates them.", "How do you find false sharing in a real program? (perf c2c)"),
      ("e7_parse", "Fast integer parsing", "A tight loop over chars avoids locale handling and virtual calls in streams; feed handlers parse like this.", "How would you parse fixed-point prices without doubles?"),
      ("e8_book", "Array-based order book", "Integer ticks in a known band index an array: O(1) add and cancel; the best price moves by a short scan only when a level empties. Checked against a std::map reference on 200,000 random operations.", "What if the price band is unbounded? (hash map of levels plus a heap)")]
TIMES = [l for l in (EL / "timings-sample.txt").read_text().splitlines() if not l.startswith("===")]
def tmap():
    out, cur = {}, None
    for ln in TIMES:
        if ln and not ln.startswith(" "): cur = ln.strip(); out[cur] = []
        elif ln.strip(): out[cur].append(ln.strip())
    return out
TM = tmap()
def body(pages):
    pg = lambda k: str(pages.get(k, "000")) if pages else "000"
    ix = [("Probability and brain teasers: 40 questions", "prob"), ("Answers with working", "pans"), ("Low-latency C++: 8 exercises", "cpp")] + [(f"   {i + 1}. {t}", s) for i, (s, t, *_r) in enumerate(EX)]
    rows = "".join(f'<tr><td><a href="#{a}">{E(t)}</a></td><td class="pg"><a href="#{a}">{pg(a)}</a></td></tr>' for t, a in ix)
    out = [f'''<section class="cover"><p class="eb">ELITE TRACK · HFT CHECKPOINT</p><h1>Elite pack<br><span>probability and low-latency C++</span></h1>
<p class="lead">For the checkpoint on 31 March 2027, if you take the Elite track: 40 probability and expected-value questions of the kind quant and HFT interviews ask (every answer checked by exact calculation, and 27 also by simulation), and 8 C++ exercises on the habits low-latency code depends on, each with tests and a timing harness.</p>
<p class="how"><b>How to use.</b> Probability: 10 questions a week, answer on paper first, then check the working. C++: build each exercise, predict which version is faster and by how much, then run it. Compile with <code>g++ -std=c++17 -O2 -pthread generated/elite/e3_spsc.cpp</code>. See the <a href="{KB}hft-overview">HFT overview</a> and <a href="{KB}low-latency-cpp">low-latency C++</a> pages.</p>
<table class="ix"><tbody>{rows}</tbody></table></section>''']
    qs = "".join(f'<div class="q" id="q{i + 1}"><b>Q{i + 1}.</b> {E(q)}</div>' for i, (q, *_r) in enumerate(Q))
    out.append(f'<section class="sec" id="prob"><h2>Probability and brain teasers<a class="pat" href="#pans">Answers</a><a class="back" href="#top">↑ Index</a></h2><div class="cols">{qs}</div></section>')
    ans = "".join(f'<tr><td><a href="#q{i + 1}">Q{i + 1}</a></td><td class="a">{E(a)}</td><td>{E(w)}</td><td class="c">{"exact + simulation" if sim else "exact"}</td></tr>' for i, (q, a, w, ex, sim) in enumerate(Q))
    out.append(f'<section class="sec" id="pans"><h2>Answers with working<a class="back" href="#prob">↑ Questions</a><a class="back" href="#top">↑ Index</a></h2><table class="key"><thead><tr><th>Q</th><th>Answer</th><th>Working</th><th>Checked by</th></tr></thead><tbody>{ans}</tbody></table><p class="meta">Checks: <code>generated/src/elite_prob.py</code> recomputes every answer exactly (fractions, enumeration or closed form) and runs seeded Monte Carlo simulations for 27 of them.</p></section>')
    if True:
        out.append(f'<section class="sec" id="cpp"><h2>About the C++ exercises<a class="back" href="#top">↑ Index</a></h2><ul><li>All eight compile with <code>-Wall -Wextra</code> and pass their checks under AddressSanitizer and UndefinedBehaviorSanitizer; the two multithreaded ones (SPSC queue, false sharing) also pass ThreadSanitizer.</li><li><code>bench.h</code> runs each version several times and reports the best nanoseconds per operation. Timings depend on the machine: the numbers shown came from one cloud container, so measure on your own laptop and compare the ratios, not the absolute values.</li><li>Correctness is asserted; speed is only printed. A faster version that gives a different answer fails.</li></ul><pre>{E((EL / "bench.h").read_text())}</pre></section>')
    for i, (s, t, why, ask) in enumerate(EX):
        tm = "".join(f"<tr><td>{E(l.rsplit(' ', 2)[0].strip())}</td><td class=v>{E(' '.join(l.rsplit(' ', 2)[1:]))}</td></tr>" for l in TM.get(s, []))
        out.append(f'''<section class="sec" id="{s}"><h2><span class="num">{i + 1:02d}</span>{E(t)}<a class="back" href="#top">↑ Index</a></h2><p>{E(why)}</p>
<div class="two"><div><h3>Measured here (-O2, one cloud container)</h3><table class="tm"><tbody>{tm}</tbody></table></div><div><h3>Think about</h3><p>{E(ask)}</p></div></div>
<h3>Code (<code>generated/elite/{s}.cpp</code>)</h3><pre>{E((EL / f"{s}.cpp").read_text())}</pre></section>''')
    return "".join(out)
CSS = """@page { size: A4; margin: 11mm 12mm 13mm; } @page :first { margin: 0; }
* { box-sizing: border-box; } html { -webkit-print-color-adjust: exact; print-color-adjust: exact; } body { margin: 0; font: 400 8.6pt/1.42 Inter, sans-serif; color: #1e293b; }
a { color: #c2410c; text-decoration: none; } .cover { padding: 15mm 15mm; break-after: page; } .eb { font: 600 8pt "JetBrains Mono"; letter-spacing: .14em; color: #c2410c; margin: 0 0 3mm; } code { font: 600 7.6pt "JetBrains Mono"; }
h1 { font: 700 32pt/1.02 "Space Grotesk"; margin: 0 0 4mm; color: #0f172a; } h1 span { color: #c2410c; font-size: 18pt; } .lead { font-size: 9.8pt; color: #475569; } .how { background: #fff7ed; border-left: 3px solid #c2410c; padding: 2mm 3mm; }
table { border-collapse: collapse; width: 100%; } .ix td { padding: 1.3mm 2mm; border-bottom: 1px solid #e2e8f0; font-size: 9.5pt; white-space: pre; } .ix td a { color: #0f172a; font-weight: 600; } .ix .pg { text-align: right; } .ix .pg a { color: #c2410c; font-family: "JetBrains Mono"; }
.sec { break-before: page; } h2 { font: 700 15pt "Space Grotesk"; color: #0f172a; border-bottom: 3px solid #c2410c; padding-bottom: 1.5mm; margin: 0 0 2.5mm; display: flex; align-items: baseline; gap: 2.5mm; }
.num { font: 600 9pt "JetBrains Mono"; color: #c2410c; } .pat { margin-left: auto; font: 600 7.5pt "JetBrains Mono"; } .back { font: 600 7.5pt "JetBrains Mono"; border: 1px solid #fdba74; background: #fff7ed; border-radius: 99px; padding: 0 7px; } h2 > .back:first-of-type { margin-left: auto; } h2 .pat + .back { margin-left: 0; }
h3 { font: 700 9.8pt "Space Grotesk"; color: #1d4ed8; margin: 2.5mm 0 1mm; } .cols { column-count: 2; column-gap: 7mm; } .q { break-inside: avoid; margin-bottom: 2.2mm; } .q b { color: #c2410c; }
th { font: 600 7pt "JetBrains Mono"; text-transform: uppercase; color: #64748b; background: #f1f5f9; padding: 1.2mm 2mm; text-align: left; } .key td { border-bottom: 1px solid #eef2f7; padding: .9mm 2mm; vertical-align: top; font-size: 7.9pt; } .key .a { font-weight: 700; color: #166534; width: 32mm; } .key .c { color: #64748b; width: 24mm; font-size: 7.2pt; }
.two { display: grid; grid-template-columns: 1.2fr 1fr; gap: 6mm; } .tm td { border-bottom: 1px solid #eef2f7; padding: .8mm 2mm; } .tm .v { text-align: right; font: 600 8pt "JetBrains Mono"; color: #166534; }
pre { font: 400 6.8pt/1.35 "JetBrains Mono"; background: #f8fafc; border: 1px solid #e2e8f0; border-left: 3px solid #1d4ed8; padding: 2mm 2.5mm; white-space: pre-wrap; margin: 0; font-variant-ligatures: none; } ul { padding-left: 5mm; } .meta { color: #64748b; font-size: 8pt; }"""
js = SRC / "r.js"
def render(pages, name):
    (SRC / "el.html").write_text(f'<!doctype html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700&family=Inter:wght@400;600;700&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet"><style>{CSS}</style></head><body><div id="top"></div>{body(pages)}</body></html>')
    js.write_text("const { chromium } = require('playwright'); (async () => { const b = await chromium.launch(); const p = await b.newPage(); await p.goto('file://' + __dirname + '/el.html', { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready); await p.pdf({ path: __dirname + '/" + name + "', format: 'A4', printBackground: true, preferCSSPageSize: true }); await b.close(); })();")
    subprocess.run(["node", str(js)], check=True)
    r = PdfReader(str(SRC / name)); return {k.lstrip("/"): r.get_destination_page_number(v) + 1 for k, v in r.named_destinations.items()}, len(r.pages)
KEYS = ["prob", "pans", "cpp"] + [s for s, *_ in EX]
d1, n1 = render(None, "p1.pdf"); d2, n2 = render(d1, "p2.pdf"); assert n1 == n2 and all(d1[k] == d2[k] for k in KEYS)
w = PdfWriter(clone_from=PdfReader(str(SRC / "p2.pdf"))); w.add_outline_item("Index", 0, fit=Fit.fit()); w.add_outline_item("Probability questions", d2["prob"] - 1, fit=Fit.fit()); w.add_outline_item("Answers", d2["pans"] - 1, fit=Fit.fit())
par = w.add_outline_item("C++ exercises", d2["cpp"] - 1, fit=Fit.fit())
for s, t, *_ in EX: w.add_outline_item(t, d2[s] - 1, parent=par, fit=Fit.fit())
NP = len(w.pages)
for i, pg in enumerate(w.pages):
    if i == 0: continue
    buf = io.BytesIO(); c = canvas.Canvas(buf, pagesize=(float(pg.mediabox.width), float(pg.mediabox.height))); c.setFont("Helvetica", 7.5); c.setFillGray(.55)
    c.drawRightString(float(pg.mediabox.width) - 26, 14, f"{i + 1} / {NP}"); c.save(); buf.seek(0); pg.merge_page(PdfReader(buf).pages[0]); pg.compress_content_streams(level=9)
w.add_metadata({"/Title": "Elite track pack"}); w.write(str(OUT / "elite-track-pack.pdf"))
for f in ("p1.pdf", "p2.pdf", "r.js", "el.html"): (SRC / f).unlink()
print(NP, "pages", d2)
