"""Striver's A2Z DSA Sheet (current takeuforward version) as a clickable PDF: index with page numbers, checkboxes, links."""
import json, html, subprocess, pathlib, io, sys
from collections import Counter
from pypdf import PdfReader, PdfWriter
from pypdf.generic import Fit
from reportlab.pdfgen import canvas
A = pathlib.Path(__file__).parent
o = json.load(open(A / "syllabus.json")); F = o["fields"]; R = o["rows"]
rec = lambda i: dict(zip(F[R[i][0]], R[i][1:]))
E = lambda s: html.escape(str(s), quote=True)
BASE = "https://takeuforward.org"
LV = {"basic": ("Basic", "#15803d"), "core": ("Core", "#1d4ed8"), "pro": ("Pro", "#c2410c")}

sections = []
for si, root in enumerate(o["roots"]):
    sec = rec(root); subs = []; loose = []
    for c in sec["children"]:
        r = rec(c)
        if r["type"] == "category": subs.append((r["label"].strip(), [rec(x) for x in r["children"]]))
        else: loose.append(r)
    if loose: subs.insert(0, ("", loose))
    sections.append((si + 1, sec["label"].strip(), subs))

def links(it):
    out = []
    if it.get("type") == "contest": return '<span class="muted">Timed contest on the site</span>'
    if it.get("layoutType") == "practice": out.append(f'<a href="{BASE}/practice/dsa/{E(it["slug"])}">Practice</a>')
    if it.get("leetcode_link"): out.append(f'<a href="{E(it["leetcode_link"])}">LeetCode</a>')
    if it.get("yt_video"): out.append(f'<a href="{E(it["yt_video"])}">Video</a>')
    if it.get("free_blog_link"):
        b = it["free_blog_link"]; out.append(f'<a href="{E(b if b.startswith("http") else BASE + b)}">Article</a>')
    return " · ".join(out) or '<span class="muted">On the sheet page</span>'

tot = Counter(); per = []
for n, label, subs in sections:
    c = Counter()
    for _, items in subs:
        for it in items:
            if it.get("type") == "contest": c["contest"] += 1
            elif it.get("layoutType") == "learning": c["lesson"] += 1
            else: c["practice"] += 1; c[it.get("difficulty") or "none"] += 1
            if it.get("isPremium"): c["plus"] += 1
    per.append(c); tot.update(c)

def body(pages):
    pg = lambda k: str(pages.get(k, "000")) if pages is not None else "000"
    rows = "".join(f'<tr><td class="n">{n:02d}</td><td><a href="#s{n}">{E(label)}</a></td><td class="c">{per[i]["practice"]}</td><td class="c">{per[i]["basic"]}</td><td class="c">{per[i]["core"]}</td><td class="c">{per[i]["pro"]}</td><td class="c">{per[i]["lesson"]}</td><td class="c">{per[i]["plus"]}</td><td class="pg"><a href="#s{n}">{pg(f"s{n}")}</a></td></tr>'
                   for i, (n, label, subs) in enumerate(sections))
    out = [f'''<section class="cover"><p class="eb">TAKEUFORWARD · CURRENT VERSION · FETCHED 15 NOV 2026</p><h1>Striver's A2Z<br><span>DSA Sheet</span></h1>
<p class="lead">The sheet as takeuforward.org serves it today: {len(sections)} sections, {tot["practice"]} practice problems, {tot["lesson"]} lessons and {tot["contest"]} contests. Every problem links to its practice page, and to LeetCode, the video and the article where the site lists them. Tick the boxes on paper or in a PDF app that supports annotations.</p>
<div class="key"><span class="lv" style="--k:#15803d">Basic</span><span class="lv" style="--k:#1d4ed8">Core</span><span class="lv" style="--k:#c2410c">Pro</span><span class="plus">Plus</span><span class="muted">Basic, Core and Pro are the site's own levels. "Plus" marks items the site flags as premium (needs takeUforward Plus).</span></div>
<h2>Index</h2><table class="ix"><thead><tr><th>#</th><th>Section</th><th>Problems</th><th>Basic</th><th>Core</th><th>Pro</th><th>Lessons</th><th>Plus</th><th>Page</th></tr></thead><tbody>{rows}
<tr class="tot"><td></td><td>Total</td><td class="c">{tot["practice"]}</td><td class="c">{tot["basic"]}</td><td class="c">{tot["core"]}</td><td class="c">{tot["pro"]}</td><td class="c">{tot["lesson"]}</td><td class="c">{tot["plus"]}</td><td></td></tr></tbody></table>
<p class="note"><b>How this fits your plan.</b> Your Playbook and Roadmap dates were built on the older 18-step version of the sheet. This version covers the same core topics but is reorganised: a new Beginner Problems section, Sliding Window / 2 Pointer as its own section, Heaps and Maths as separate sections, and some problems renamed or moved. Solve in this sheet's order if you prefer it; keep the plan's daily pace (5 to 6 a day).</p>
<p class="src">Source: <a href="{BASE}/prep-hub/strivers-a2z-dsa-sheet">takeuforward.org/prep-hub/strivers-a2z-dsa-sheet</a>. The site may change after this date.</p></section>''']
    k = 0
    for n, label, subs in sections:
        out.append(f'<section class="sec" id="s{n}"><h2><span class="sn">{n:02d}</span>{E(label)} <a class="back" href="#top">↑ Index</a></h2><p class="sub">{per[n-1]["practice"]} problems · {per[n-1]["lesson"]} lessons{" · " + str(per[n-1]["contest"]) + " contest" if per[n-1]["contest"] else ""}</p>')
        for sl, items in subs:
            if sl: out.append(f'<h3>{E(sl)}</h3>')
            out.append('<table class="it"><tbody>')
            for it in items:
                k += 1
                kind = it.get("type")
                lvl = LV.get(it.get("difficulty"))
                tag = (f'<span class="lv" style="--k:{lvl[1]}">{lvl[0]}</span>' if lvl else
                       ('<span class="lv" style="--k:#64748b">Lesson</span>' if it.get("layoutType") == "learning" else '<span class="lv" style="--k:#7c3aed">Contest</span>' if kind == "contest" else ""))
                plus = '<span class="plus">Plus</span>' if it.get("isPremium") else ""
                out.append(f'<tr><td class="box">☐</td><td class="k">{k}</td><td class="t">{E(it["label"])} {plus}</td><td class="l">{tag}</td><td class="a">{links(it)}</td><td class="d">{E(it.get("duration") or "")}</td></tr>')
            out.append('</tbody></table>')
        out.append('</section>')
    return "".join(out)

CSS = """@page { size: A4; margin: 12mm 12mm 14mm; } @page :first { margin: 0; }
* { box-sizing: border-box; } html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { margin: 0; font: 400 8.6pt/1.4 Inter, sans-serif; color: #1e293b; }
a { color: #c2410c; text-decoration: none; }
.cover { padding: 16mm 15mm 10mm; break-after: page; }
.eb { font: 600 8pt "JetBrains Mono"; letter-spacing: .14em; color: #c2410c; margin: 0 0 3mm; }
h1 { font: 700 34pt/1 "Space Grotesk"; margin: 0 0 4mm; color: #0f172a; } h1 span { color: #c2410c; }
.lead { font-size: 10pt; color: #475569; max-width: 165mm; margin: 0 0 4mm; }
.key { display: flex; flex-wrap: wrap; gap: 6px; align-items: center; margin-bottom: 4mm; font-size: 8pt; }
h2 { font: 700 13pt "Space Grotesk"; color: #0f172a; margin: 3mm 0 2mm; }
.lv { display: inline-block; font: 600 7pt "JetBrains Mono"; color: var(--k); border: 1px solid color-mix(in srgb, var(--k) 45%, #fff); background: color-mix(in srgb, var(--k) 10%, #fff); border-radius: 99px; padding: 0 6px; white-space: nowrap; }
.plus { display: inline-block; font: 600 6.6pt "JetBrains Mono"; color: #a16207; background: #fef3c7; border-radius: 4px; padding: 0 4px; }
.muted { color: #64748b; }
table { width: 100%; border-collapse: collapse; }
.ix th { font: 600 7pt "JetBrains Mono"; text-transform: uppercase; color: #64748b; background: #f1f5f9; padding: 1.3mm 2mm; text-align: left; }
.ix td { padding: 1.1mm 2mm; border-bottom: 1px solid #e2e8f0; font-size: 8.6pt; } .ix td a { color: #0f172a; }
.ix .c { text-align: center; font-family: "JetBrains Mono"; } .ix .n { font: 600 8pt "JetBrains Mono"; color: #94a3b8; }
.ix .pg { text-align: right; font: 600 8pt "JetBrains Mono"; } .ix .pg a { color: #c2410c; } .ix .tot td { font-weight: 700; border-top: 2px solid #cbd5e1; }
.note { margin-top: 4mm; padding: 2.5mm 3.5mm; border-left: 4px solid #2563eb; background: #eff6ff; border-radius: 0 6px 6px 0; font-size: 8.6pt; }
.src { font-size: 7.6pt; color: #64748b; margin-top: 3mm; }
.sec { break-before: page; } .sec:first-of-type { break-before: auto; }
.sec h2 { font-size: 16pt; border-bottom: 3px solid #c2410c; padding-bottom: 1.5mm; margin-top: 0; display: flex; align-items: baseline; gap: 3mm; }
.sec h2 .sn { color: #c2410c; font-family: "JetBrains Mono"; }
.back { margin-left: auto; font: 600 7.5pt "JetBrains Mono"; border: 1px solid #fdba74; background: #fff7ed; border-radius: 99px; padding: 0 7px; }
.sub { color: #64748b; margin: 0 0 2mm; font-size: 8.2pt; }
h3 { font: 700 10pt "Space Grotesk"; color: #1d4ed8; margin: 3mm 0 1mm; break-after: avoid; }
.it tr { break-inside: avoid; } .it td { padding: 1mm 1.5mm; border-bottom: 1px solid #eef2f7; vertical-align: top; }
.it .box { width: 5mm; font-size: 10pt; color: #94a3b8; } .it .k { width: 8mm; font: 500 7.4pt "JetBrains Mono"; color: #94a3b8; }
.it .t { font-weight: 600; color: #0f172a; } .it .l { width: 17mm; } .it .a { width: 62mm; font-size: 7.8pt; } .it .d { width: 16mm; white-space: nowrap; font: 500 7pt "JetBrains Mono"; color: #94a3b8; text-align: right; }"""

def render(pages, out):
    doc = f'''<!doctype html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@600;700&family=Inter:wght@400;600;700&family=JetBrains+Mono:wght@500;600&display=swap" rel="stylesheet"><style>{CSS}</style></head><body><div id="top"></div>{body(pages)}</body></html>'''
    (A / "a2z.html").write_text(doc)
    js = A / "r.js"
    js.write_text("""const { chromium } = require('playwright'); (async () => { const b = await chromium.launch(); const p = await b.newPage();
      await p.goto('file://' + __dirname + '/a2z.html', { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready);
      await p.pdf({ path: __dirname + '/""" + out + """', format: 'A4', printBackground: true, preferCSSPageSize: true }); await b.close(); })();""")
    subprocess.run(["node", str(js)], check=True)
    r = PdfReader(str(A / out))
    return {k.lstrip("/"): r.get_destination_page_number(v) + 1 for k, v in r.named_destinations.items()}, len(r.pages)

d1, n1 = render(None, "pass1.pdf")
d2, n2 = render(d1, "pass2.pdf")
assert n1 == n2 and all(d1[f"s{n}"] == d2[f"s{n}"] for n, _, _ in sections), "pages moved"
w = PdfWriter(clone_from=PdfReader(str(A / "pass2.pdf")))
w.add_outline_item("Index", 0, fit=Fit.fit())
for n, label, _ in sections: w.add_outline_item(f"{n:02d}  {label}", d2[f"s{n}"] - 1, fit=Fit.fit())
N = len(w.pages)
for i, pg in enumerate(w.pages):
    if i == 0: continue
    buf = io.BytesIO(); c = canvas.Canvas(buf, pagesize=(float(pg.mediabox.width), float(pg.mediabox.height))); c.setFont("Helvetica", 7.5); c.setFillGray(.55)
    c.drawRightString(float(pg.mediabox.width) - 26, 14, f"{i + 1} / {N}"); c.save(); buf.seek(0); pg.merge_page(PdfReader(buf).pages[0]); pg.compress_content_streams(level=9)
w.compress_identical_objects(remove_duplicates=True, remove_unreferenced=True)
w.add_metadata({"/Title": "Striver's A2Z DSA Sheet (current version, Nov 2026)"})
w.write(str(A / "Striver-A2Z-DSA-Sheet-2026.pdf"))
print(N, "pages;", dict(tot))
