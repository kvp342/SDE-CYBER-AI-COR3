"""The older 18-step Striver A2Z sheet, rebuilt from a public scrape, as a clickable PDF."""
import json, html, subprocess, pathlib, io
from collections import Counter, OrderedDict
from pypdf import PdfReader, PdfWriter
from pypdf.generic import Fit
from reportlab.pdfgen import canvas
A = pathlib.Path(__file__).parent
d = json.load(open(A / "g2.json"))
E = lambda s: html.escape(str(s), quote=True)
STEPS = [(1, "Learn the basics", ["Things to Know in C++/Java/Python or any language", "Build-up Logical Thinking", "Patterns", "Learn STL/Java-Collections or similar thing in your language", "Know Basic Maths", "Learn Basic Recursion", "Learn Basic Hashing"]),
 (2, "Learn important sorting techniques", ["Sorting-I", "Sorting-II"]), (3, "Solve problems on arrays", ["Easy", "Medium", "Hard"]),
 (4, "Binary search", ["BS on 1D Arrays", "BS on Answers", "BS on 2D Arrays"]), (5, "Strings (basic and medium)", ["Basic and Easy String Problems", "Medium String Problems"]),
 (6, "Linked list", ["Learn 1D LinkedList", "Learn Doubly LinkedList", "Medium Problems of LL", "Medium Problems of DLL", "Hard Problems of LL"]),
 (7, "Recursion", ["Get a Strong Hold", "Subsequences Pattern", "Trying out all Combos / Hard"]),
 (8, "Bit manipulation", ["Learn Bit Manipulation", "Interview Problems", "Advanced Maths"]),
 (9, "Stack and queues", ["Learning", "Prefix, Infix, PostFix Conversion Problems", "Monotonic Stack/Queue Problems [VVV. Imp]", "Implementation Problems"]),
 (10, "Sliding window and two pointer", ["Medium Problems", "Hard Problems"]), (11, "Heaps", ["Learning", "Medium Problems", "Hard Problems"]),
 (12, "Greedy algorithms", ["Easy Problems", "Medium/Hard"]), (13, "Binary trees", ["Traversals", "Medium Problems", "Hard Problems"]),
 (14, "Binary search trees", ["Concepts", "Practice Problems"]),
 (15, "Graphs", ["Learning", "Problems on BFS/DFS", "Topo Sort and Problems", "Shortest Path Algorithms and Problems", "MinimumSpanningTree/Disjoint Set and Problems", "Other Algorithms"]),
 (16, "Dynamic programming", ["Introduction to DP", "1D DP", "2D/3D DP and DP on Grids", "DP on Subsequences", "DP on Strings", "DP on Stocks", "DP on LIS", "MCM DP | Partition DP", "DP on Squares"]),
 (17, "Tries", ["Theory", "Problems"]), (18, "Strings (advanced)", ["Hard Problems"])]
# shared category names: at position k, items appear in step order among the steps still active at k
ACTIVE = {"Learning": lambda k: [9, 11, 15] if k <= 4 else [9, 15] if k <= 6 else [9],
          "Medium Problems": lambda k: [10, 11, 13] if k <= 7 else [10, 13] if k == 8 else [13],
          "Hard Problems": lambda k: [10, 11, 13, 18] if k <= 4 else [11, 13, 18] if k <= 6 else [13, 18] if k <= 9 else [13]}
step_of = {}
for c, f in ACTIVE.items():
    byk = OrderedDict()
    for i, x in enumerate(d):
        if x["category"] == c: byk.setdefault(x["order"], []).append(i)
    for k, idx in byk.items():
        st = f(k); assert len(st) == len(idx), (c, k, len(st), len(idx))
        for s, i in zip(st, idx): step_of[i] = s
lec = {}
for n, _, lectures in STEPS:
    for L in lectures: lec.setdefault(L, []).append(n)
for i, x in enumerate(d):
    if i not in step_of:
        ss = lec[x["category"]]; assert len(ss) == 1, x["category"]; step_of[i] = ss[0]
data = {n: OrderedDict((L, []) for L in lectures) for n, _, lectures in STEPS}
for i, x in sorted(enumerate(d), key=lambda t: t[1]["order"]): data[step_of[i]][x["category"]].append(x)
total = Counter(x["difficulty"] for x in d)
per = {n: Counter(x["difficulty"] for L in data[n].values() for x in L) for n, _, _ in STEPS}
COL = {"Easy": "#15803d", "Medium": "#1d4ed8", "Hard": "#c2410c"}
import re as _re
_o = json.load(open(A.parent / "a2z" / "syllabus.json")); _F = _o["fields"]
_new = [dict(zip(_F[r[0]], r[1:])) for r in _o["rows"]]
_norm = lambda t: _re.sub(r"[^a-z0-9]", "", t.lower())
NEWP = {_norm(x["label"]): x["slug"] for x in _new if x.get("type") == "item" and x.get("layoutType") == "practice"}
NEWLC = {x["leetcode_link"].rstrip("/"): x["slug"] for x in _new if x.get("leetcode_link")}
MATCH = Counter()
def links(x):
    out = []
    slug = NEWP.get(_norm(x["name"])) or (NEWLC.get(x["leetcode"].rstrip("/")) if x.get("leetcode") else None)
    if slug: out.append(f'<a href="https://takeuforward.org/practice/dsa/{E(slug)}">Practice</a>'); MATCH["yes"] += 1
    else: MATCH["no"] += 1
    if x.get("leetcode"): out.append(f'<a href="{E(x["leetcode"])}">LeetCode</a>')
    if x.get("youtube"): out.append(f'<a href="{E(x["youtube"])}">Video</a>')
    return " · ".join(out) or '<span class="muted">Removed from the new site</span>'
def name_link(x):
    slug = NEWP.get(_norm(x["name"])) or (NEWLC.get(x["leetcode"].rstrip("/")) if x.get("leetcode") else None)
    u = f"https://takeuforward.org/practice/dsa/{slug}" if slug else (x.get("leetcode") or x.get("youtube"))
    return f'<a class="nm" href="{E(u)}">{E(x["name"])}</a>' if u else E(x["name"])
def gone(x):
    return not (NEWP.get(_norm(x["name"])) or (NEWLC.get(x["leetcode"].rstrip("/")) if x.get("leetcode") else None))
def body(pages):
    pg = lambda k: str(pages.get(k, "000")) if pages else "000"
    rows = "".join(f'<tr><td class="n">{n:02d}</td><td><a href="#s{n}">{E(t)}</a></td><td class="c">{sum(per[n].values())}</td><td class="c">{per[n]["Easy"]}</td><td class="c">{per[n]["Medium"]}</td><td class="c">{per[n]["Hard"]}</td><td class="pg"><a href="#s{n}">{pg(f"s{n}")}</a></td></tr>' for n, t, _ in STEPS)
    out = [f'''<section class="cover"><p class="eb">TAKEUFORWARD · THE OLDER 18-STEP VERSION</p><h1>Striver's A2Z<br><span>DSA Sheet (classic)</span></h1>
<p class="lead">The version your plan is built on: 18 steps and {len(d)} items ({total["Easy"]} Easy, {total["Medium"]} Medium, {total["Hard"]} Hard), with every lecture in its original order. Each item links to LeetCode and Striver's video, and to its practice page on today's takeuforward site where the problem still exists.</p>
<div class="key"><span class="lv" style="--k:#15803d">Easy</span><span class="lv" style="--k:#1d4ed8">Medium</span><span class="lv" style="--k:#c2410c">Hard</span></div>
<h2>Index</h2><table class="ix"><thead><tr><th>Step</th><th>Topic</th><th>Items</th><th>Easy</th><th>Medium</th><th>Hard</th><th>Page</th></tr></thead><tbody>{rows}
<tr><td class="n">+</td><td><a href="#gone">Appendix: not found in the new sheet</a></td><td class="c" colspan="4"></td><td class="pg"><a href="#gone">{pg("gone")}</a></td></tr><tr class="tot"><td></td><td>Total</td><td class="c">{len(d)}</td><td class="c">{total["Easy"]}</td><td class="c">{total["Medium"]}</td><td class="c">{total["Hard"]}</td><td></td></tr></tbody></table>
<p class="note"><b>How this fits your plan.</b> Your Playbook's day-by-day problems follow these 18 steps in this order (it counts {359} Easy/Medium and 84 Hard; the extra items here are mostly the C++ basics and pattern lessons in Step 1). The old takeuforward article pages have been removed (they return \"page not found\"), so they are not linked; use the video, or the new practice page where there is one.</p>
<p class="src">Source: the old sheet as preserved in a public scrape (github.com/aryanbatras/leetcode-daily-discord, data/a2z.json); step order rebuilt from the sheet's structure. Current version: takeuforward.org/prep-hub/strivers-a2z-dsa-sheet.</p></section>''']
    k = 0
    for n, t, lectures in STEPS:
        out.append(f'<section class="sec" id="s{n}"><h2><span class="sn">STEP {n:02d}</span>{E(t)} <a class="back" href="#top">↑ Index</a></h2><p class="sub">{sum(per[n].values())} items · {per[n]["Easy"]} Easy, {per[n]["Medium"]} Medium, {per[n]["Hard"]} Hard</p>')
        for li, L in enumerate(lectures, 1):
            items = data[n][L]
            if not items: continue
            out.append(f'<h3>Lec {li}: {E(L)}</h3><table class="it"><tbody>')
            for x in items:
                k += 1
                out.append(f'<tr><td class="box">☐</td><td class="k">{k}</td><td class="t">{name_link(x)}</td><td class="l"><span class="lv" style="--k:{COL[x["difficulty"]]}">{x["difficulty"]}</span></td><td class="a">{links(x)}</td></tr>')
            out.append('</tbody></table>')
        out.append('</section>')
    miss = [(n, t, L, x) for n, t, lectures in STEPS for L in lectures for x in data[n][L] if gone(x)]
    out.append(f'<section class="sec" id="gone"><h2><span class="sn">APPENDIX</span>Not found in the new sheet <a class="back" href="#top">↑ Index</a></h2><p class="sub">{len(miss)} items from this classic sheet have no match in the current version by name or LeetCode link. Most were removed; a few may only have been renamed. If you use the new sheet, solve these too.</p><table class="it"><tbody>')
    for n, t, L, x in miss:
        out.append(f'<tr><td class="box">☐</td><td class="k">S{n:02d}</td><td class="t">{name_link(x)}<br><span class="muted">{E(L)}</span></td><td class="l"><span class="lv" style="--k:{COL[x["difficulty"]]}">{x["difficulty"]}</span></td><td class="a">{links(x)}</td></tr>')
    out.append('</tbody></table></section>')
    return "".join(out)
CSS = (A.parent / "a2z" / "make_a2z.py").read_text().split('CSS = """')[1].split('"""')[0]
def render(pages, out):
    (A / "old.html").write_text(f'<!doctype html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@600;700&family=Inter:wght@400;600;700&family=JetBrains+Mono:wght@500;600&display=swap" rel="stylesheet"><style>{CSS}</style></head><body><div id="top"></div>{body(pages)}</body></html>')
    js = A / "r.js"
    js.write_text("const { chromium } = require('playwright'); (async () => { const b = await chromium.launch(); const p = await b.newPage(); await p.goto('file://' + __dirname + '/old.html', { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready); await p.pdf({ path: __dirname + '/" + out + "', format: 'A4', printBackground: true, preferCSSPageSize: true }); await b.close(); })();")
    subprocess.run(["node", str(js)], check=True)
    r = PdfReader(str(A / out)); return {k.lstrip("/"): r.get_destination_page_number(v) + 1 for k, v in r.named_destinations.items()}, len(r.pages)
d1, n1 = render(None, "p1.pdf"); d2, n2 = render(d1, "p2.pdf"); assert n1 == n2 and all(d1[f"s{n}"] == d2[f"s{n}"] for n, _, _ in STEPS) and d1["gone"] == d2["gone"]
w = PdfWriter(clone_from=PdfReader(str(A / "p2.pdf"))); w.add_outline_item("Index", 0, fit=Fit.fit())
for n, t, _ in STEPS: w.add_outline_item(f"Step {n:02d}  {t}", d2[f"s{n}"] - 1, fit=Fit.fit())
w.add_outline_item("Appendix: not in the new sheet", d2["gone"] - 1, fit=Fit.fit())
N = len(w.pages)
for i, pg in enumerate(w.pages):
    if i == 0: continue
    buf = io.BytesIO(); c = canvas.Canvas(buf, pagesize=(float(pg.mediabox.width), float(pg.mediabox.height))); c.setFont("Helvetica", 7.5); c.setFillGray(.55)
    c.drawRightString(float(pg.mediabox.width) - 26, 14, f"{i + 1} / {N}"); c.save(); buf.seek(0); pg.merge_page(PdfReader(buf).pages[0]); pg.compress_content_streams(level=9)
w.compress_identical_objects(remove_duplicates=True, remove_unreferenced=True); w.add_metadata({"/Title": "Striver's A2Z DSA Sheet (classic 18-step version)"})
w.write(str(A / "Striver-A2Z-DSA-Sheet-Classic.pdf"))
print(dict(MATCH)); print(N, "pages;", {n: sum(per[n].values()) for n, _, _ in STEPS})
