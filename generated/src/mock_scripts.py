"""Mock interview scripts for practising with a friend: 2 DSA, 1 Core CS, 1 LLD, 1 security, 1 HR. Each has timed phases, what the
interviewer says, hints to give in order, and a scoring rubric. Problems come from material already tested in the kit (asserted).
Run from the repo root: python3 generated/src/mock_scripts.py"""
import html, io, pathlib, subprocess, sys
from pypdf import PdfReader, PdfWriter
from pypdf.generic import Fit
from reportlab.pdfgen import canvas
ROOT = pathlib.Path(__file__).resolve().parents[2]; OUT = ROOT / "generated"; SRC = OUT / "src"
sys.path.insert(0, str(SRC)); from t_probs2 import P as PROBS2
E = lambda s: html.escape(str(s), quote=True); KB = "https://claude.ai/artifact/McuS723LTAb16Q6SpdUsAT#"
IDS = {p["id"] for p in PROBS2}
RUBRIC_DSA = [("Problem understanding", "Restated the problem, asked about input size, edge cases and output format before coding"), ("Approach", "Gave a brute force, then a better idea, with complexity, before coding"),
              ("Code", "Correct, readable, sensible names; no long silences"), ("Testing", "Walked through an example and edge cases without being asked; found own bugs"),
              ("Communication", "Thought aloud; took hints well; explained trade-offs")]
SCRIPTS = [
 dict(id="dsa1", title="DSA mock 1: stacks and strings", minutes=45, ref=["p2-decode-string", "p2-sliding-window-max"],
  setup="Interviewer: share a blank editor (no autocomplete) or paper. Candidate codes in C++.",
  phases=[(2, "Intro", "\"Tell me briefly about yourself and the language you'll use.\""),
          (18, "Problem 1: Decode String", "Say: \"Given an encoded string like 3[a2[c]], return its decoded form: accaccacc. Numbers before brackets repeat the bracketed part.\" Expected: a stack of (string so far, repeat count), O(output length)."),
          (18, "Problem 2: Sliding Window Maximum", "Say: \"Given an array and k, return the maximum of every window of size k.\" Expected: monotonic deque of indices, O(n). Accept an O(n log k) heap first, then ask for O(n)."),
          (5, "Follow-ups", "Ask: \"Why is the deque solution O(n) even with a while loop inside?\" and \"What if counts can have several digits in Decode String?\""),
          (2, "Candidate's questions", "Let them ask one question; answer briefly.")],
  hints=["Problem 1: \"What do you need to remember when you see '['?\" → \"What if you pushed the current string and the number?\"",
         "Problem 2: \"Which elements can never be the maximum again?\" → \"Keep indices in a structure where values decrease.\"",
         "If stuck for 4 minutes, give the next hint; note each hint given."], rubric=RUBRIC_DSA),
 dict(id="dsa2", title="DSA mock 2: graphs", minutes=45, ref=["p2-course-schedule-ii", "p2-cheapest-flights"],
  setup="Same setup. Draw small graphs on paper if needed.",
  phases=[(2, "Intro", "Warm-up: \"What's a graph problem you solved recently?\""),
          (20, "Problem 1: Course Schedule II", "Say: \"n courses, prerequisite pairs [a, b] meaning b before a. Return an order to take all courses, or empty if impossible.\" Expected: Kahn's algorithm (BFS on in-degree 0), detect a cycle when fewer than n are output, O(V + E)."),
          (18, "Problem 2: Cheapest Flights Within K Stops", "Say: \"Given flights with prices, find the cheapest price from src to dst with at most k stops, or −1.\" Expected: Bellman–Ford for k + 1 rounds using a copy of the previous round, or Dijkstra on (cost, node, stops)."),
          (3, "Follow-ups", "Ask: \"Why does plain Dijkstra fail here?\" and \"How would you detect the cycle with DFS instead?\""),
          (2, "Candidate's questions", "")],
  hints=["Problem 1: \"Which courses can you take first?\" → \"What happens to other courses when you finish one?\"",
         "Problem 2: \"What does 'at most k stops' limit?\" → \"Can you relax edges only k + 1 times?\" → \"Why must each round read the previous round's costs?\""], rubric=RUBRIC_DSA),
 dict(id="core", title="Core CS mock", minutes=30, ref=["qa-os", "qa-dbms", "qa-cn", "oop"],
  setup="Interviewer reads the questions; candidate answers aloud, with a whiteboard for diagrams. Use the Core CS one-pagers to check answers.",
  phases=[(8, "Operating systems", "Ask: process vs thread; the four deadlock conditions and one way to prevent each; what happens on a page fault."),
          (8, "DBMS and SQL", "Ask: ACID with a bank-transfer example; dirty read vs phantom read and which isolation level stops each; write SQL for the second-highest salary."),
          (8, "Networks", "Ask: what happens when you type a URL (from DNS to rendering); TCP vs UDP with examples; how TLS uses both asymmetric and symmetric encryption."),
          (6, "OOP", "Ask: how virtual functions work (vtable); why a base class needs a virtual destructor; one SOLID principle with an example from their project.")],
  hints=["Give a hint only after 1 minute of silence, and only one per question: for example \"think about what each transaction sees\"."],
  rubric=[("Accuracy", "Facts correct; no confident wrong statements"), ("Depth", "Went one level below the definition (an example, a why)"), ("Structure", "Answers organised: definition → example → trade-off"),
          ("Honesty", "Said 'I'm not sure, but I think…' instead of bluffing"), ("Diagrams", "Used a quick sketch where it helps (process states, TCP handshake)")]),
 dict(id="lld", title="LLD mock: rate limiter", minutes=45, ref=["lld"],
  setup="Candidate designs and codes a per-client rate limiter in C++. Compare afterwards with lld/rate_limiter.cpp in the kit.",
  phases=[(7, "Requirements", "Say: \"Design a rate limiter for an API: each client may make at most N requests per window.\" Let the candidate ask: burst allowed? exact or approximate? one server or many? What to return when limited?"),
          (10, "Design", "Expect: an interface allow(client), at least two algorithms (token bucket, sliding window), per-client state in a hash map, injectable clock for tests."),
          (20, "Code", "Expect working code for one algorithm, thread-safe (mutex), plus a short test with a fake clock."),
          (8, "Extensions", "Ask: \"How would this work across 10 servers?\" (Redis with atomic operations or a gateway) and \"What HTTP response do you send?\" (429 with Retry-After).")],
  hints=["\"How will you test time-based behaviour without sleeping?\" → injected clock.", "\"What happens if two threads call allow at once?\""],
  rubric=[("Requirements", "Asked the questions that change the design"), ("Abstractions", "Clean interface; algorithms swappable (Strategy)"), ("Correctness", "Window and refill maths right; no data races"),
          ("Testability", "Clock injected; a real test written"), ("Trade-offs", "Compared algorithms: memory, accuracy, bursts")]),
 dict(id="sec", title="Security mock", minutes=30, ref=["owasp", "tenantwall", "abac"],
  setup="For security or security-aware SDE roles. Interviewer uses the lab map's interview questions and the TenantWall helpers.",
  phases=[(8, "Project deep dive", "Ask: \"Explain TenantWall. How does ABAC stop tenant A reading tenant B's data? How did you prove it? What does the alarm catch, and how fast?\""),
          (10, "Web security", "Ask three: SQL injection prevention; stored vs reflected XSS; CSRF and SameSite cookies; SSRF in the cloud; IDOR."),
          (7, "Scenario", "Say: \"A login endpoint is being brute-forced. What do you do in the next hour, and what do you change long-term?\" Expect: rate limiting, lockouts or CAPTCHA, alerting, MFA, checking logs for success after failures."),
          (5, "Candidate's questions", "")],
  hints=["For the scenario: \"What would you look for in the logs?\""],
  rubric=[("Project depth", "Explains design, tests and limits of TenantWall clearly"), ("Fundamentals", "Correct causes and fixes for web vulnerabilities"), ("Defence in depth", "Proposes layers, not one fix"),
          ("Ethics", "Mentions permission and responsible disclosure where relevant"), ("Clarity", "Explains to a non-specialist when asked")]),
 dict(id="hr", title="HR and behavioural mock", minutes=30, ref=["star"],
  setup="Use the interview story bank. Interviewer asks; candidate answers in STAR form, about 2 minutes each.",
  phases=[(5, "Opening", "\"Tell me about yourself.\" \"Why this company?\""),
          (18, "Behavioural", "Pick four: a project you are proud of; a time you failed; a disagreement; learning something fast; going beyond the task; helping someone. After each, ask one follow-up: \"What would you do differently?\" or \"What did you personally do?\""),
          (5, "HR", "\"Strengths and a weakness?\" \"Where do you see yourself in five years?\" \"Are you open to relocating?\""),
          (2, "Candidate's questions", "")],
  hints=["If an answer drifts into 'we', ask: \"What was your part?\""],
  rubric=[("Structure", "Clear STAR; result stated"), ("Ownership", "Uses 'I' for own actions; credits others fairly"), ("Evidence", "Concrete details and numbers"),
          ("Reflection", "Real learning, not a disguised strength"), ("Length", "About 2 minutes; stops when done")]),
]
for s in SCRIPTS:
    assert sum(m for m, *_ in s["phases"]) == s["minutes"], (s["id"], sum(m for m, *_ in s["phases"]))
    assert len(s["rubric"]) == 5
for pid in SCRIPTS[0]["ref"] + SCRIPTS[1]["ref"]: assert pid in IDS, pid   # DSA problems exist (and were compiled and tested) in Worked Solutions II
assert (OUT / "lld" / "rate_limiter.cpp").exists()
def body(pages):
    pg = lambda k: str(pages.get(k, "000")) if pages else "000"
    rows = "".join(f'<tr><td><a href="#{s["id"]}">{E(s["title"])}</a></td><td class=c>{s["minutes"]} min</td><td class="pg"><a href="#{s["id"]}">{pg(s["id"])}</a></td></tr>' for s in SCRIPTS)
    out = [f'''<section class="cover"><p class="eb">INTERVIEWS · PRACTICE WITH A FRIEND</p><h1>Mock interview<br><span>scripts</span></h1>
<p class="lead">Six scripts a friend can run without being an expert: what to say, how long each part takes, which hints to give and in what order, and a rubric to score you. Swap roles afterwards: interviewing someone else teaches you what interviewers notice.</p>
<p class="how"><b>Rules.</b> Camera on, timer visible, no notes. The interviewer writes down every hint given and the time stamps. Score right after, then talk for 10 minutes: one thing to keep, one thing to fix. Repeat a script after two weeks with different problems from the same pattern.</p>
<table class="ix"><tbody>{rows}</tbody></table>
<h3>Scoring</h3><p>Each rubric line is scored 1 (weak) to 4 (strong). 17–20: ready; 13–16: close, fix the lowest line; 12 or below: repeat the related practice before the next mock. Each hint used costs nothing in the score but note it: hints you needed show what to revise.</p></section>''']
    for s in SCRIPTS:
        ph = "".join(f"<tr><td class=t>{m} min</td><td class=k>{E(n)}</td><td>{E(d)}</td></tr>" for m, n, d in s["phases"])
        rb = "".join(f"<tr><td class=k>{E(a)}</td><td>{E(b)}</td><td class=sc>1 · 2 · 3 · 4</td></tr>" for a, b in s["rubric"])
        LC = {q["id"]: (q["title"], q["prac"][0][1]) for q in PROBS2}
        refs = ", ".join(f'<a href="{LC[r][1]}">{E(LC[r][0])}</a> (Worked Solutions II)' if r in LC else f'<a href="{KB}{r}">{r}</a>' for r in s["ref"])
        out.append(f'''<section class="sec" id="{s["id"]}"><h2>{E(s["title"])} <span class=m>{s["minutes"]} minutes</span><a class="back" href="#top">↑ Index</a></h2><p class="meta">{E(s["setup"])} Reference answers: {refs}.</p>
<h3>Script</h3><table class="ph"><tbody>{ph}</tbody></table><h3>Hints, in order</h3><ul>{"".join(f"<li>{E(h)}</li>" for h in s["hints"])}</ul>
<h3>Rubric</h3><table class="rb"><tbody>{rb}<tr><td class=k>Total</td><td></td><td class=sc>____ / 20</td></tr></tbody></table><p class="meta">Notes and time stamps:</p><div class="notes"></div></section>''')
    return "".join(out)
CSS = """@page { size: A4; margin: 12mm 13mm 14mm; } @page :first { margin: 0; }
* { box-sizing: border-box; } html { -webkit-print-color-adjust: exact; print-color-adjust: exact; } body { margin: 0; font: 400 9pt/1.45 Inter, sans-serif; color: #1e293b; }
a { color: #c2410c; text-decoration: none; } .cover { padding: 16mm 15mm; break-after: page; } .eb { font: 600 8pt "JetBrains Mono"; letter-spacing: .14em; color: #c2410c; margin: 0 0 3mm; }
h1 { font: 700 34pt/1.02 "Space Grotesk"; margin: 0 0 4mm; color: #0f172a; } h1 span { color: #c2410c; } .lead { font-size: 10pt; color: #475569; } .how { background: #fff7ed; border-left: 3px solid #c2410c; padding: 2mm 3mm; }
table { border-collapse: collapse; width: 100%; } .ix td { padding: 2.2mm 2mm; border-bottom: 1px solid #e2e8f0; font-size: 10.5pt; } .ix td a { color: #0f172a; font-weight: 600; } .ix .c { font-family: "JetBrains Mono"; color: #64748b; } .ix .pg { text-align: right; } .ix .pg a { color: #c2410c; font-family: "JetBrains Mono"; }
.sec { break-before: page; } h2 { font: 700 15pt "Space Grotesk"; color: #0f172a; border-bottom: 3px solid #c2410c; padding-bottom: 1.5mm; margin: 0 0 2mm; display: flex; align-items: baseline; gap: 3mm; } h2 .m { font: 600 8pt "JetBrains Mono"; color: #c2410c; }
.back { margin-left: auto; font: 600 7.5pt "JetBrains Mono"; border: 1px solid #fdba74; background: #fff7ed; border-radius: 99px; padding: 0 7px; } h3 { font: 700 10pt "Space Grotesk"; color: #1d4ed8; margin: 3mm 0 1mm; }
.ph td, .rb td { border-bottom: 1px solid #e2e8f0; padding: 1.6mm 2mm; vertical-align: top; } .t { font: 600 8pt "JetBrains Mono"; color: #c2410c; width: 15mm; } .k { font-weight: 700; width: 40mm; } .sc { width: 30mm; text-align: right; font: 600 8pt "JetBrains Mono"; color: #64748b; }
ul { padding-left: 5mm; margin: 0; } li { margin-bottom: 1mm; } .meta { color: #475569; font-size: 8.4pt; margin: 1mm 0; } .notes { border: 1px dashed #cbd5e1; height: 30mm; border-radius: 4px; }"""
js = SRC / "r.js"
def render(pages, name):
    (SRC / "ms.html").write_text(f'<!doctype html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700&family=Inter:wght@400;600;700&family=JetBrains+Mono:wght@600&display=swap" rel="stylesheet"><style>{CSS}</style></head><body><div id="top"></div>{body(pages)}</body></html>')
    js.write_text("const { chromium } = require('playwright'); (async () => { const b = await chromium.launch(); const p = await b.newPage(); await p.goto('file://' + __dirname + '/ms.html', { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready); await p.pdf({ path: __dirname + '/" + name + "', format: 'A4', printBackground: true, preferCSSPageSize: true }); await b.close(); })();")
    subprocess.run(["node", str(js)], check=True)
    r = PdfReader(str(SRC / name)); return {k.lstrip("/"): r.get_destination_page_number(v) + 1 for k, v in r.named_destinations.items()}, len(r.pages)
d1, n1 = render(None, "p1.pdf"); d2, n2 = render(d1, "p2.pdf"); assert n1 == n2 and all(d1[s["id"]] == d2[s["id"]] for s in SCRIPTS)
assert n2 == len(SCRIPTS) + 1, f"each script should fit on one page: {n2}"
w = PdfWriter(clone_from=PdfReader(str(SRC / "p2.pdf"))); w.add_outline_item("Index", 0, fit=Fit.fit())
for s in SCRIPTS: w.add_outline_item(s["title"], d2[s["id"]] - 1, fit=Fit.fit())
NP = len(w.pages)
for i, pg in enumerate(w.pages):
    if i == 0: continue
    buf = io.BytesIO(); c = canvas.Canvas(buf, pagesize=(float(pg.mediabox.width), float(pg.mediabox.height))); c.setFont("Helvetica", 7.5); c.setFillGray(.55)
    c.drawRightString(float(pg.mediabox.width) - 26, 14, f"{i + 1} / {NP}"); c.save(); buf.seek(0); pg.merge_page(PdfReader(buf).pages[0]); pg.compress_content_streams(level=9)
w.add_metadata({"/Title": "Mock interview scripts"}); w.write(str(OUT / "mock-interview-scripts.pdf"))
for f in ("p1.pdf", "p2.pdf", "r.js", "ms.html"): (SRC / f).unlink()
print(NP, "pages", d2)
