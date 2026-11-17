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
 dict(id="dsa3", title="DSA mock 3: DP on strings", minutes=45, ref=["p2-word-break", "p2-decode-ways"],
  setup="Shared editor without autocomplete, or paper. Candidate codes in C++.",
  phases=[(2, "Intro", "\"Which DP problem did you find hardest so far, and why?\""),
          (18, "Problem 1: Word Break", "Say: \"Given a string and a dictionary, can the string be split into dictionary words?\" Expected: dp[i] = prefix of length i can be split; check every j < i; a hash set for the dictionary."),
          (18, "Problem 2: Decode Ways", "Say: \"A message of digits encodes letters A=1 … Z=26. Count the ways to decode it.\" Expected: dp over prefixes; one-digit step if not '0', two-digit step if 10–26."),
          (5, "Follow-ups", "Ask: \"Return all sentences for Word Break (II): what changes and what is the worst case?\" and \"Make Decode Ways O(1) space.\""),
          (2, "Candidate's questions", "")],
  hints=["Problem 1: \"What does it mean for a prefix to be breakable?\" → \"If dp[j] is true, what must hold for dp[i]?\"", "Problem 2: \"What does a '0' do?\" → \"How is this like climbing stairs?\""], rubric=RUBRIC_DSA),
 dict(id="dsa4", title="DSA mock 4: trees and grids", minutes=45, ref=["p2-build-tree", "p2-pacific-atlantic"],
  setup="Same setup. Let the candidate draw the tree and the grid.",
  phases=[(2, "Intro", "Warm-up: \"Preorder, inorder, postorder: which one gives sorted order in a BST?\""),
          (20, "Problem 1: Build tree from preorder and inorder", "Say: \"Rebuild a binary tree from its preorder and inorder traversals (values are unique).\" Expected: first preorder value is the root; its inorder index splits left and right; a hash map gives O(n)."),
          (18, "Problem 2: Pacific Atlantic Water Flow", "Say: \"Water flows to equal or lower neighbours. Which cells can reach both oceans?\" Expected: search backwards from each ocean's border (uphill), intersect the two reachable sets."),
          (3, "Follow-ups", "Ask: \"Why search from the oceans instead of from every cell?\" and \"Build from inorder and postorder instead.\""),
          (2, "Candidate's questions", "")],
  hints=["Problem 1: \"Where is the root in preorder?\" → \"How do you find it in inorder quickly?\"", "Problem 2: \"Is it easier to ask where water can come from?\""], rubric=RUBRIC_DSA),
 dict(id="osnet", title="OS and networks deep dive", minutes=30, ref=["qa-os", "qa-cn", "virtual-memory", "tcp-udp"],
  setup="One topic is followed down three levels of 'why'. Check answers against the Core CS one-pagers.",
  phases=[(10, "Memory", "Ask: what happens on a page fault, step by step; why a TLB helps; what thrashing is and how to fix it. Then: \"Why does a fork() not copy all memory immediately?\" (copy-on-write)."),
          (10, "Concurrency", "Ask: process vs thread; a race condition example; mutex vs semaphore; the four deadlock conditions and how to break one."),
          (10, "Networks", "Ask: what happens when you type a URL; TCP handshake and why three steps; how TLS combines asymmetric and symmetric crypto; what a /26 subnet gives you.")],
  hints=["Only after a minute of silence: \"Start from what the CPU sees.\" or \"Think about what each side knows after each message.\""],
  rubric=[("Accuracy", "No confident wrong statements"), ("Depth", "Could go three levels of 'why'"), ("Clarity", "Simple language, a quick sketch where useful"), ("Connections", "Linked theory to real systems (Linux, browsers)"), ("Honesty", "Said when unsure")]),
 dict(id="sd", title="System design (fresher level)", minutes=40, ref=["hld", "caching", "load-balancing"],
  setup="Use the URL shortener or notification service from the system design case studies as the reference answer.",
  phases=[(6, "Requirements", "Say: \"Design a URL shortener.\" Let the candidate ask about scale, custom aliases, expiry and analytics."),
          (6, "Estimates", "Expect requests per second for reads and writes, and storage for five years, with stated assumptions."),
          (14, "High-level design", "Expect API, data model, ID generation, cache, database choice and a diagram."),
          (10, "Deep dive", "Pick one: ID generation without collisions, or handling a hot link, or counting clicks without slowing redirects."),
          (4, "Wrap-up", "Ask: \"What breaks first at 10× traffic?\"")],
  hints=["\"What is the read to write ratio?\"", "\"Where would you put a cache, and what would you store?\""],
  rubric=[("Requirements", "Asked before designing"), ("Estimates", "Numbers with assumptions"), ("Design", "Clear components and data flow"), ("Trade-offs", "Explained choices (301 vs 302, counter vs hash)"), ("Communication", "Drew and narrated")]),
 dict(id="twgrill", title="TenantWall project grilling", minutes=30, ref=["tenantwall", "abac", "cloudtrail"],
  setup="The interviewer reads the TenantWall helpers and paper outline beforehand and keeps asking 'how do you know?'.",
  phases=[(5, "Pitch", "\"Explain TenantWall in two minutes to someone who has not heard of ABAC.\""),
          (10, "Design", "Ask: why ABAC and not one role per tenant; what stops a tenant changing its own tag; why the explicit deny is separate; what DescribeInstances exposes."),
          (10, "Evidence", "Ask: how many isolation tests, what each showed, the alert delay and how you measured it, what it costs per month."),
          (5, "Limits", "Ask: what would break at 1,000 tenants; what you would do differently; what you learned.")],
  hints=["If vague: \"Show me the exact condition in the policy.\""],
  rubric=[("Clarity", "Two-minute pitch a non-expert understands"), ("Depth", "Policy-level detail without notes"), ("Evidence", "Real numbers from real tests"), ("Limits", "Names weaknesses honestly"), ("Ownership", "Clear about own contribution versus the professor's")]),
 dict(id="secscen", title="Security scenario round", minutes=30, ref=["owasp", "sqli", "xss"],
  setup="For security-aware SDE roles. The interviewer plays an engineer on call; use the lab map and lab notebook as references.",
  phases=[(10, "Incident", "Say: \"Our login API shows 5,000 failed logins a minute from many IPs, and two accounts later logged in successfully. Walk me through the next hour.\" Expect: contain (rate limits, lock affected accounts), investigate logs, notify, then fix (MFA, credential-stuffing defences)."),
          (12, "Code review", "Show a short handler that builds SQL from a query parameter and echoes a name into HTML. Ask the candidate to find the issues (SQL injection, XSS, missing ownership check) and fix them."),
          (8, "Design", "Ask: \"How would you store passwords and sessions for this app?\" and \"What would you log, and what must you never log?\"")],
  hints=["\"Which accounts are at risk right now?\"", "\"Where does user input reach a query or a page?\""],
  rubric=[("Prioritisation", "Contained before investigating"), ("Accuracy", "Correct causes and fixes"), ("Depth", "Layers of defence, not one fix"), ("Communication", "Clear steps under pressure"), ("Ethics", "Mentions disclosure and user notification")]),
]
for s in SCRIPTS:
    assert sum(m for m, *_ in s["phases"]) == s["minutes"], (s["id"], sum(m for m, *_ in s["phases"]))
    assert len(s["rubric"]) == 5
for pid in SCRIPTS[0]["ref"] + SCRIPTS[1]["ref"]: assert pid in IDS, pid   # DSA problems exist (and were compiled and tested) in Worked Solutions II
def body(pages):
    pg = lambda k: str(pages.get(k, "000")) if pages else "000"
    rows = "".join(f'<tr><td><a href="#{s["id"]}">{E(s["title"])}</a></td><td class=c>{s["minutes"]} min</td><td class="pg"><a href="#{s["id"]}">{pg(s["id"])}</a></td></tr>' for s in SCRIPTS)
    out = [f'''<section class="cover"><p class="eb">INTERVIEWS · PRACTICE WITH A FRIEND · II</p><h1>Mock interview<br><span>scripts II</span></h1>
<p class="lead">Six more scripts (DP on strings, trees and grids, OS and networks, system design, a TenantWall grilling and a security scenario) a friend can run without being an expert: what to say, how long each part takes, which hints to give and in what order, and a rubric to score you. Swap roles afterwards: interviewing someone else teaches you what interviewers notice.</p>
<p class="how"><b>Rules.</b> Camera on, timer visible, no notes. The interviewer writes down every hint given and the time stamps. Score right after, then talk for 10 minutes: one thing to keep, one thing to fix. Repeat a script after two weeks with different problems from the same pattern.</p>
<table class="ix"><tbody>{rows}</tbody></table>
<h3>Scoring</h3><p>Each rubric line is scored 1 (weak) to 4 (strong). 17–20: ready; 13–16: close, fix the lowest line; 12 or below: repeat the related practice before the next mock. Each hint used costs nothing in the score but note it: hints you needed show what to revise.</p></section>''']
    for s in SCRIPTS:
        ph = "".join(f"<tr><td class=t>{m} min</td><td class=k>{E(n)}</td><td>{E(d)}</td></tr>" for m, n, d in s["phases"])
        rb = "".join(f"<tr><td class=k>{E(a)}</td><td>{E(b)}</td><td class=sc>1 · 2 · 3 · 4</td></tr>" for a, b in s["rubric"])
        KBT = __import__('json').loads((OUT / 'kb2' / 'aliases.json').read_text())
        LC = {q["id"]: (q["title"], q["prac"][0][1]) for q in PROBS2}
        refs = ", ".join(f'<a href="{LC[r][1]}">{E(LC[r][0])}</a> (Worked Solutions II)' if r in LC else f'<a href="{KB}{r}">{E(KBT[r][0])}</a> (Knowledge Base)' for r in s["ref"])
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
    (SRC / "ms2.html").write_text(f'<!doctype html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700&family=Inter:wght@400;600;700&family=JetBrains+Mono:wght@600&display=swap" rel="stylesheet"><style>{CSS}</style></head><body><div id="top"></div>{body(pages)}</body></html>')
    js.write_text("const { chromium } = require('playwright'); (async () => { const b = await chromium.launch(); const p = await b.newPage(); await p.goto('file://' + __dirname + '/ms2.html', { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready); await p.pdf({ path: __dirname + '/" + name + "', format: 'A4', printBackground: true, preferCSSPageSize: true }); await b.close(); })();")
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
w.add_metadata({"/Title": "Mock interview scripts II"}); w.write(str(OUT / "mock-interview-scripts-2.pdf"))
for f in ("p1.pdf", "p2.pdf", "r.js", "ms2.html"): (SRC / f).unlink()
print(NP, "pages", d2)
