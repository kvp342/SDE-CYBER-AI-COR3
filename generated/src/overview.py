"""The whole kit on one A4 page: timeline, daily routine, the 7 DSA phases (same structure as the external 6-month roadmap)
mapped to your dates and files, system design / LLD / machine coding, the other tracks, checkpoints. Every file link is
checked to exist and the page count is asserted to be 1. Run from the repo root: python3 generated/src/overview.py"""
import html, pathlib, subprocess
from pypdf import PdfReader, PdfWriter
ROOT = pathlib.Path(__file__).resolve().parents[2]; OUT = ROOT / "generated"; SRC = OUT / "src"
GH = "https://github.com/kvp342/intrusion-detection-and-prevention/blob/ccr-ca7232a7-t7lq94/"
E = html.escape; USED = []
def K(path, label):
    USED.append(path); return f'<a href="{GH}{path}">{E(label)}</a>'
TIMELINE = [("17 Nov", "C++ refresh"), ("18 Nov – 30 Jan", "Striver A2Z core, 5–6/day"), ("Feb – May", "Hard pass + Codeforces 1400 by 31 Mar"), ("Feb – Mar", "Internship applications, GSoC/LFX"),
            ("21 Mar", "TenantWall paper"), ("22 Mar – 7 Apr", "Exams: Anki only"), ("wk of 19 Apr", "AWS SAA-C03"), ("May", "Internship or AI-security project"), ("31 May – 31 Jul", "Placement sprint"), ("Aug – Dec", "Placements")]
PHASES = [
 ("1 Foundations", "Complexity, arrays, strings, hashing, prefix sums, Kadane", "Nov (A2Z 1–3)", [("generated/patterns-stl-card.pdf", "STL card"), ("generated/worked-solutions-2.pdf", "WS II")]),
 ("2 Core patterns", "Two pointers, sliding window, binary search (incl. on the answer)", "Dec (A2Z 4–5, 10)", [("generated/worked-solutions-3.pdf", "WS III")]),
 ("3 Data structures", "Linked lists, stacks/queues, monotonic stack, trees, BST, heaps", "Dec – Jan (A2Z 6, 9, 11, 13–14)", [("generated/worked-solutions-3.pdf", "WS III"), ("generated/gap-fill-pack.pdf", "Invert tree")]),
 ("4 Graphs", "BFS/DFS, topo sort, Dijkstra, DSU, MST, bitmask BFS", "Late Jan (A2Z 15)", [("generated/worked-solutions-2.pdf", "WS II"), ("generated/worked-solutions-4.pdf", "WS IV")]),
 ("5 Backtracking", "Subsets, permutations, N-Queens, Sudoku, word search", "Dec (A2Z 7)", [("generated/worked-solutions-3.pdf", "WS III")]),
 ("6 Dynamic programming", "1D, 2D, strings, knapsack, intervals, trees, stocks, digit DP", "Feb (A2Z 16) + hard pass", [("generated/worked-solutions-4.pdf", "WS IV (hard)")]),
 ("7 Advanced", "Tries, bits, segment tree, Fenwick, sieve, modular maths", "Feb (A2Z 8, 17) + hard pass", [("generated/gap-fill-pack.pdf", "Gap-fill"), ("generated/codeforces-ladder.pdf", "CF ladder")]),
]
TRACKS = [
 ("System design basics", "Scaling, SQL vs NoSQL, caching, queues, CDN, CAP, APIs, rate limiting, consistent hashing", [("generated/core-cs-one-pagers.pdf", "One-pagers")]),
 ("HLD", "URL shortener, chat, feed, notifications, file sync; API gateway, ride matching, checkout, autocomplete, video; Instagram", [("generated/system-design-case-studies.pdf", "SD I"), ("generated/system-design-case-studies-2.pdf", "SD II"), ("generated/gap-fill-pack.pdf", "Instagram")]),
 ("LLD", "Parking lot, library, elevator, Splitwise, rate limiter, LRU; tic-tac-toe, vending, booking, logger, TTL store, snake & ladder; ATM", [("generated/lld-pack.pdf", "LLD I"), ("generated/lld-pack-2.pdf", "LLD II"), ("generated/gap-fill-pack.pdf", "ATM")]),
 ("Machine coding", "Food ordering, pluggable-eviction cache, inventory (plus every LLD above as 60–90 min practice)", [("generated/gap-fill-pack.pdf", "Gap-fill")]),
 ("Core CS, SQL", "OS, DBMS, CN, OOP: 1 h/day; 300 MCQs; 70 SQL questions", [("generated/core-cs-mcq-bank.pdf", "MCQ I"), ("generated/core-cs-mcq-bank-2.pdf", "MCQ II"), ("generated/sql-pack.pdf", "SQL I"), ("generated/sql-pack-2.pdf", "SQL II")]),
 ("OAs, aptitude", "24 timed OA sets on Saturdays (13 Feb – 4 Sep); 240 aptitude questions", [("generated/oa-simulation-packs.pdf", "OA I"), ("generated/oa-simulation-packs-2.pdf", "OA II"), ("generated/oa-simulation-packs-3.pdf", "OA III"), ("generated/aptitude-pack-2.pdf", "Aptitude II")]),
 ("Security, cloud", "AWS 30 min/day; labs on weekends; TenantWall paper", [("generated/aws-lab-workbook.pdf", "AWS labs"), ("generated/security-labs-workbook.pdf", "Sec labs"), ("generated/cyber-security-interview-bank.pdf", "Sec Q&A")]),
 ("Projects", "Backend, AI-security, C++ networking, SOC log analyser", [("generated/network-programming-project.pdf", "Networking"), ("generated/soc-log-analysis-project.pdf", "logsentry")]),
 ("Applying", "Resume, profiles, 10 applications + 5 messages a week, open source", [("generated/resume-kit.pdf", "Resume"), ("generated/applications-outreach-kit.pdf", "Tracker"), ("generated/open-source-gsoc-guide.pdf", "GSoC")]),
 ("Interviews", "Mocks from March (2/week from 31 May), company files, stories, interview day", [("generated/mock-interview-scripts.pdf", "Mocks I"), ("generated/mock-interview-scripts-2.pdf", "Mocks II"), ("generated/company-files-3.pdf", "Companies"), ("generated/interview-day-kit.pdf", "Day kit")]),
]
CHECK = [("31 Dec", "200+ problems; resume v1"), ("30 Jan", "A2Z core done"), ("31 Mar", "CF 1400; paper submitted; applications out"), ("30 Apr", "AWS passed; WS II–IV done"), ("31 Jul", "Mocks 17+/20; 2 deployed projects")]
FIRST5 = [("generated/final-plan.pdf", "Final plan"), ("playbook.html", "Playbook (daily)"), ("Striver-A2Z-DSA-Sheet-Classic.pdf", "A2Z sheet"), ("generated/anki-decks-guide.pdf", "Anki decks"), ("generated/weekly-revision-tests.pdf", "Sunday tests")]
links = lambda xs: " · ".join(K(p, l) for p, l in xs)
CSS = """@page { size: A4; margin: 8mm 9mm; } * { box-sizing: border-box; } html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { margin: 0; font: 400 7.9pt/1.38 Inter, sans-serif; color: #1e293b; } a { color: #1d4ed8; text-decoration: none; font-weight: 600; }
h1 { font: 700 15pt "Space Grotesk"; margin: 0; color: #0f172a; } h1 span { color: #c2410c; } .sub { color: #475569; margin: .5mm 0 1.5mm; }
h2 { font: 700 8.6pt "Space Grotesk"; color: #c2410c; margin: 2mm 0 .8mm; text-transform: uppercase; letter-spacing: .04em; }
table { border-collapse: collapse; width: 100%; } td, th { border-bottom: 1px solid #e2e8f0; padding: .55mm 1.2mm; vertical-align: top; text-align: left; }
th { font: 600 6.2pt "JetBrains Mono"; color: #64748b; background: #f1f5f9; text-transform: uppercase; } td.k { font-weight: 700; white-space: nowrap; color: #0f172a; }
.tl { display: flex; gap: .8mm; flex-wrap: wrap; } .tl div { flex: 1 1 17%; background: #f8fafc; border-left: 2.5px solid #1d4ed8; padding: .6mm 1.2mm; } .tl b { display: block; font: 600 6.6pt "JetBrains Mono"; color: #1d4ed8; }
.day { background: #fff7ed; border-left: 3px solid #c2410c; padding: 1mm 2mm; margin-top: 1.2mm; } .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 3mm; }
.foot { margin-top: 1.5mm; color: #475569; font-size: 6.6pt; }"""
HTML = f'''<h1>The whole kit <span>on one page</span></h1><p class="sub">Your plan from 17 Nov 2026 to placements, in the same seven-phase DSA structure as the external 6-month roadmap, with your dates and the file to open for each part. Every one of that roadmap's 95 named problems is covered: 79 as tested worked solutions, 15 in your A2Z sheet, 1 in the gap-fill pack.</p>
<h2>Timeline</h2><div class="tl">{"".join(f"<div><b>{E(d)}</b>{E(t)}</div>" for d, t in TIMELINE)}</div>
<div class="day"><b>Every day:</b> Anki 15–20 min · DSA 3–4 h (5–6 new A2Z problems + redos on days 1, 3, 7, 21) · Core CS 1 h · AWS 30 min · log in the tracker. <b>Saturday:</b> OA set (from Feb). <b>Sunday:</b> 30-min revision test + weekly review. <b>Stuck rule:</b> 25 min (15 easy, 40 hard), then read, close, rewrite.</div>
<h2>DSA in seven phases</h2><table><thead><tr><th>Phase</th><th>Topics</th><th>When</th><th>Worked solutions to use</th></tr></thead><tbody>{"".join(f'<tr><td class="k">{E(p)}</td><td>{E(t)}</td><td>{E(w)}</td><td>{links(f)}</td></tr>' for p, t, w, f in PHASES)}</tbody></table>
<h2>Everything else</h2><table><thead><tr><th>Track</th><th>What</th><th>Open</th></tr></thead><tbody>{"".join(f'<tr><td class="k">{E(t)}</td><td>{E(w)}</td><td>{links(f)}</td></tr>' for t, w, f in TRACKS)}</tbody></table>
<div class="grid"><div><h2>Checkpoints</h2><table><tbody>{"".join(f'<tr><td class="k">{E(d)}</td><td>{E(t)}</td></tr>' for d, t in CHECK)}</tbody></table></div>
<div><h2>Open these five first</h2><table><tbody>{"".join(f"<tr><td>{K(p, l)}</td></tr>" for p, l in FIRST5)}</tbody></table></div></div>
<p class="foot">Everything else: {K("generated/index-of-everything.pdf", "index of everything")} · readable on GitHub: {K("generated/read/README.md", "generated/read/")} · deadline now: SRFP research fellowship closes 30 Nov 2026.</p>'''
for p in USED: assert (ROOT / p).exists(), p
(SRC / "overview.html").write_text(f'<!doctype html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700&family=Inter:wght@400;600;700&family=JetBrains+Mono:wght@600&display=swap" rel="stylesheet"><style>{CSS}</style></head><body>{HTML}</body></html>')
js = SRC / "rov.js"; js.write_text("const { chromium } = require('playwright'); (async () => { const b = await chromium.launch(); const p = await b.newPage(); await p.goto('file://' + __dirname + '/overview.html', { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready); await p.pdf({ path: __dirname + '/ov.pdf', format: 'A4', printBackground: true, preferCSSPageSize: true }); await b.close(); })();")
subprocess.run(["node", str(js)], check=True)
r = PdfReader(str(SRC / "ov.pdf")); assert len(r.pages) == 1, f"must be one page, got {len(r.pages)}"
w = PdfWriter(clone_from=r); w.add_metadata({"/Title": "The whole kit on one page"}); w.write(str(OUT / "one-page-overview.pdf"))
for f in ("ov.pdf", "rov.js", "overview.html"): (SRC / f).unlink()
print("1 page;", len(set(USED)), "file links checked")
