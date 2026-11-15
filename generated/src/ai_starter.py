"""Guide PDF for generated/ai-security-starter. Runs the offline tests and suites and prints their real numbers.
Run from the repo root: python3 generated/src/ai_starter.py"""
import html, subprocess, pathlib, io, sys, json
from pypdf import PdfReader, PdfWriter
from pypdf.generic import Fit
from reportlab.pdfgen import canvas
ROOT = pathlib.Path(__file__).resolve().parents[2]; OUT = ROOT / "generated"; SRC = OUT / "src"; P = OUT / "ai-security-starter"
sys.path[:0] = [str(P), str(P / "eval"), str(P / "attacks")]
import run_eval, run_attacks
E = lambda s: html.escape(str(s), quote=True)
KB = "https://claude.ai/artifact/McuS723LTAb16Q6SpdUsAT#"
t = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests"], cwd=P, capture_output=True, text=True)
assert t.returncode == 0, t.stderr
TESTLINE = t.stderr.strip().splitlines()[-3] + " · " + t.stderr.strip().splitlines()[-1]
EV = {d: run_eval.run("stub", d, verbose=False) for d in (False, True)}
AT = run_attacks.run("stub", verbose=False)
CASES = json.loads((P / "attacks" / "cases.json").read_text())
LAYERS = [("1. Input scan", "defence.scan_input", "Blocks questions containing override phrases (ignore, disregard or forget previous instructions; you are now; system override) or requests to reveal hidden instructions, after removing zero-width characters.", "Direct injection"),
          ("2. Document sanitising", "defence.sanitise_chunk", "Drops HTML comments and replaces instruction-like sentences in retrieved chunks with a marker before the model sees them.", "Indirect injection"),
          ("3. Prompt separation", "defence.build_prompt", "Puts documents inside <document> tags and tells the model that document text is data, never instructions.", "Both (model-dependent)"),
          ("4. Output checks", "defence.check_output", "Blocks answers containing the canary token or secret patterns (AWS access keys, private keys) and removes links outside an allowlist.", "Leaks and exfiltration")]
SRCS = [("OWASP Top 10 for LLM Applications: LLM01 Prompt Injection", "https://genai.owasp.org/llmrisk/llm01-prompt-injection/"),
        ("Greshake et al., 'Not what you've signed up for' (indirect prompt injection), arXiv 2302.12173", "https://arxiv.org/abs/2302.12173"),
        ("Simon Willison's prompt injection series", "https://simonwillison.net/series/prompt-injection/"),
        ("Anthropic Python SDK", "https://github.com/anthropics/anthropic-sdk-python")]
def body(pages):
    pg = lambda k: str(pages.get(k, "000")) if pages else "000"
    ix = [("What it is and how it works", "how"), ("Defence layers", "layers"), ("Run it", "run"), ("Offline results", "results"), ("May project plan", "plan"), ("Sources", "srcs")]
    rows = "".join(f'<tr><td><a href="#{a}">{x}</a></td><td class="pg"><a href="#{a}">{pg(a)}</a></td></tr>' for x, a in ix)
    out = [f'''<section class="cover"><p class="eb">AI SECURITY · PROJECT STARTER</p><h1>secrag<br><span>RAG assistant with prompt-injection defences</span></h1>
<p class="lead">A working starting point for the May AI-security project: a small assistant that answers from your security notes, 20 evaluation questions, 12 prompt-injection attacks (6 direct, 6 indirect), and four defence layers you can switch on and measure. Everything runs offline; one flag switches to Claude.</p>
<p class="how"><b>Where.</b> <code>generated/ai-security-starter/</code> in the repository. Tests: {E(TESTLINE)}. Standard library only, except the optional <code>anthropic</code> SDK.</p>
<table class="ix"><tbody>{rows}</tbody></table></section>''']
    out.append(f'''<section class="sec" id="how"><h2>What it is and how it works<a class="back" href="#top">↑ Index</a></h2>
<pre class="flow">question
   │
   ├─[1 input scan]──── blocked? → "I can't help with that request."
   ▼
retrieve top 3 chunks from notes/ (TF-IDF cosine)
   │
   ├─[2 sanitise chunks]  remove HTML comments and instruction-like sentences
   ▼
build prompt ─[3 separation]  &lt;document&gt; tags + "documents are data" rule + canary token
   ▼
model (StubLLM offline, or Claude)
   ▼
[4 output checks]  canary or secret → block · unknown links → remove
   ▼
answer + sources + reasons</pre>
<ul><li><b>Retrieval</b> (<code>secrag/store.py</code>): each <code>##</code> section of a note is one chunk; TF-IDF vectors and cosine similarity pick the top 3. No embeddings service needed; swapping in real embeddings is a good week-3 extension.</li>
<li><b>Models</b> (<code>secrag/llm.py</code>): <code>StubLLM</code> is deliberately naive, like an unprotected model: it obeys instructions found anywhere in its input, which lets the attack suite run offline. <code>AnthropicLLM</code> calls Claude through the official SDK, reads credentials from the environment, defaults to <code>claude-opus-5-5</code> (change with <code>SECRAG_MODEL</code>), and enables the server-side refusal fallback.</li>
<li><b>Measures</b>: retrieval hit@3, answer match (an expected phrase appears), false blocks on normal questions, and attack success rate per attack.</li></ul>
<p class="meta">See also the <a href="{KB}owasp">OWASP</a> and <a href="{KB}threat-modelling">threat modelling</a> Knowledge Base pages.</p></section>''')
    out.append(f'<section class="sec" id="layers"><h2>Defence layers<a class="back" href="#top">↑ Index</a></h2><table class="t"><thead><tr><th>Layer</th><th>Code</th><th>What it does</th><th>Against</th></tr></thead><tbody>{"".join(f"<tr><td><b>{E(a)}</b></td><td><code>{E(b)}</code></td><td>{E(c)}</td><td>{E(d)}</td></tr>" for a, b, c, d in LAYERS)}</tbody></table><p class="meta">No layer is complete. Pattern filters miss paraphrases and other languages; prompt separation depends on the model; output checks only catch what you know to look for. The project\'s value is measuring each layer, not claiming the problem is solved.</p></section>')
    out.append('''<section class="sec" id="run"><h2>Run it<a class="back" href="#top">↑ Index</a></h2><pre>cd generated/ai-security-starter
python3 -m unittest discover -s tests -v     # offline, no key
python3 eval/run_eval.py --defended
python3 attacks/run_attacks.py

# with Claude (small cost per run; set a spending limit first)
pip install -r requirements.txt
export ANTHROPIC_API_KEY=...                 # or: ant auth login. Never commit keys.
python3 eval/run_eval.py --llm anthropic --defended
python3 attacks/run_attacks.py --llm anthropic</pre><p class="meta">The scripts print one line per question or attack with the answer and the reasons a defence fired, then the totals.</p></section>''')
    ar = "".join(f'<tr><td>{c["id"]}</td><td>{c["type"]}</td><td>{E(c["question"].replace(chr(0x200b), "[zero-width]"))}</td><td class="{"bad" if AT["baseline"][c["id"]] else "good"}">{"succeeded" if AT["baseline"][c["id"]] else "stopped"}</td><td class="{"bad" if AT["defended"][c["id"]] else "good"}">{"succeeded" if AT["defended"][c["id"]] else "stopped"}</td></tr>' for c in CASES)
    sb, sd = sum(AT["baseline"].values()), sum(AT["defended"].values())
    out.append(f'''<section class="sec" id="results"><h2>Offline results<a class="back" href="#top">↑ Index</a></h2>
<table class="kv"><thead><tr><th>Measure</th><th>Baseline</th><th>Defended</th></tr></thead><tbody>
<tr><td>Attack success rate</td><td>{sb}/12</td><td>{sd}/12</td></tr><tr><td>Retrieval hit@3</td><td>{EV[False]["hit"]}/20</td><td>{EV[True]["hit"]}/20</td></tr>
<tr><td>Normal questions blocked</td><td>{EV[False]["blocked"]}/20</td><td>{EV[True]["blocked"]}/20</td></tr><tr><td>Answer match (extractive stub)</td><td>{EV[False]["match"]}/20</td><td>{EV[True]["match"]}/20</td></tr></tbody></table>
<h3>Per attack</h3><table class="t"><thead><tr><th>ID</th><th>Type</th><th>Question asked</th><th>Baseline</th><th>Defended</th></tr></thead><tbody>{ar}</tbody></table>
<p class="meta"><b>How to read this.</b> The stub obeys injections by design and the filters use similar patterns, so these numbers only prove the pipeline works end to end. Run the same suites with Claude and with new held-out attacks to get results worth reporting. The lower defended answer match comes from the stub reading tagged documents differently, not from the defences removing content; check this with a real model.</p></section>''')
    out.append('''<section class="sec" id="plan"><h2>May project plan<a class="back" href="#top">↑ Index</a></h2><table class="t"><thead><tr><th>Week</th><th>Do</th><th>Output</th></tr></thead><tbody>
<tr><td>1</td><td>Run both suites with Claude. Add 10 notes from your own study material and 10 matching questions.</td><td>Baseline table with a real model</td></tr>
<tr><td>2</td><td>Write 20 held-out attacks the filters have never seen: paraphrases, Hindi or Telugu, base64, markdown links, role-play. Measure each layer alone and all together.</td><td>Ablation table: attack success rate and false blocks per layer</td></tr>
<tr><td>3</td><td>Add one stronger defence, for example a second, cheaper model call that labels each retrieved chunk as data or instructions. Measure again, with cost and latency.</td><td>Before/after table with cost per question</td></tr>
<tr><td>4</td><td>Write a 4-page report (problem, threat model, method, results, limits). Clean the README, add the tables, record a 2-minute demo.</td><td>GitHub repository and report</td></tr></tbody></table>
<h3>What to say in interviews</h3><ul><li>The problem: an assistant that reads untrusted documents can be steered by text inside them.</li><li>The method: a fixed evaluation set and attack suite, with defences switched on one at a time.</li><li>The result: attack success rate and false-block rate per layer, with a real model, and what still got through.</li></ul></section>''')
    out.append(f'<section class="sec" id="srcs"><h2>Sources<a class="back" href="#top">↑ Index</a></h2><ul>{"".join(f"<li><a href={chr(34)}{u}{chr(34)}>{E(x)}</a><span class=u>{E(u)}</span></li>" for x, u in SRCS)}</ul><p class="meta">The notes, attacks and code are original. The attack styles follow the public categories in the sources above.</p></section>')
    return "".join(out)
CSS = """@page { size: A4; margin: 12mm 12mm 14mm; } @page :first { margin: 0; }
* { box-sizing: border-box; } html { -webkit-print-color-adjust: exact; print-color-adjust: exact; } body { margin: 0; font: 400 9pt/1.45 Inter, sans-serif; color: #1e293b; }
a { color: #c2410c; text-decoration: none; } .cover { padding: 16mm 15mm; break-after: page; } code { font: 600 7.8pt "JetBrains Mono"; }
.eb { font: 600 8pt "JetBrains Mono"; letter-spacing: .14em; color: #c2410c; margin: 0 0 3mm; } h1 { font: 700 34pt/1.02 "Space Grotesk"; margin: 0 0 4mm; color: #0f172a; } h1 span { color: #c2410c; font-size: 17pt; }
.lead { font-size: 10pt; color: #475569; } .how { background: #fff7ed; border-left: 3px solid #c2410c; padding: 2mm 3mm; } table { border-collapse: collapse; width: 100%; }
th { font: 600 7pt "JetBrains Mono"; text-transform: uppercase; color: #64748b; background: #f1f5f9; padding: 1.3mm 2mm; text-align: left; }
.ix td { padding: 2mm; border-bottom: 1px solid #e2e8f0; font-size: 10pt; } .ix td a { color: #0f172a; font-weight: 600; } .ix .pg { text-align: right; } .ix .pg a { color: #c2410c; font-family: "JetBrains Mono"; }
.sec { break-before: page; } h2 { font: 700 15pt "Space Grotesk"; color: #0f172a; border-bottom: 3px solid #c2410c; padding-bottom: 1.5mm; margin: 0 0 3mm; display: flex; align-items: baseline; }
.back { margin-left: auto; font: 600 7.5pt "JetBrains Mono"; border: 1px solid #fdba74; background: #fff7ed; border-radius: 99px; padding: 0 7px; } h3 { font: 700 10.5pt "Space Grotesk"; color: #1d4ed8; margin: 4mm 0 1.5mm; }
.meta { color: #475569; font-size: 8.5pt; } pre { font: 400 7.8pt/1.45 "JetBrains Mono"; background: #f8fafc; border: 1px solid #e2e8f0; border-left: 3px solid #1d4ed8; padding: 2.5mm 3mm; white-space: pre-wrap; }
pre { font-variant-ligatures: none; font-feature-settings: "liga" 0, "calt" 0; } ul { padding-left: 5mm; } li { margin-bottom: 1.5mm; }
.t td, .kv td { border-bottom: 1px solid #e2e8f0; padding: 1.6mm 2mm; vertical-align: top; } .kv td:first-child { font-weight: 600; } .good { color: #166534; font-weight: 600; } .bad { color: #b42318; font-weight: 600; }
.u { display: block; font: 400 7pt "JetBrains Mono"; color: #94a3b8; }"""
js = SRC / "r.js"
def render(pages, name):
    (SRC / "ai.html").write_text(f'<!doctype html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700&family=Inter:wght@400;600&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet"><style>{CSS}</style></head><body><div id="top"></div>{body(pages)}</body></html>')
    js.write_text("const { chromium } = require('playwright'); (async () => { const b = await chromium.launch(); const p = await b.newPage(); await p.goto('file://' + __dirname + '/ai.html', { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready); await p.pdf({ path: __dirname + '/" + name + "', format: 'A4', printBackground: true, preferCSSPageSize: true }); await b.close(); })();")
    subprocess.run(["node", str(js)], check=True)
    r = PdfReader(str(SRC / name)); return {k.lstrip("/"): r.get_destination_page_number(v) + 1 for k, v in r.named_destinations.items()}, len(r.pages)
KEYS = ["how", "layers", "run", "results", "plan", "srcs"]
d1, n1 = render(None, "p1.pdf"); d2, n2 = render(d1, "p2.pdf"); assert n1 == n2 and all(d1[k] == d2[k] for k in KEYS)
w = PdfWriter(clone_from=PdfReader(str(SRC / "p2.pdf"))); w.add_outline_item("Index", 0, fit=Fit.fit())
for x, k in [("How it works", "how"), ("Defence layers", "layers"), ("Run it", "run"), ("Results", "results"), ("May plan", "plan"), ("Sources", "srcs")]: w.add_outline_item(x, d2[k] - 1, fit=Fit.fit())
NP = len(w.pages)
for i, pg in enumerate(w.pages):
    if i == 0: continue
    buf = io.BytesIO(); c = canvas.Canvas(buf, pagesize=(float(pg.mediabox.width), float(pg.mediabox.height))); c.setFont("Helvetica", 7.5); c.setFillGray(.55)
    c.drawRightString(float(pg.mediabox.width) - 26, 14, f"{i + 1} / {NP}"); c.save(); buf.seek(0); pg.merge_page(PdfReader(buf).pages[0]); pg.compress_content_streams(level=9)
w.add_metadata({"/Title": "AI-security project starter"}); w.write(str(OUT / "ai-security-starter-guide.pdf"))
for f in ("p1.pdf", "p2.pdf", "r.js", "ai.html"): (SRC / f).unlink()
print(NP, "pages", d2, "attacks", sum(AT["baseline"].values()), sum(AT["defended"].values()))
