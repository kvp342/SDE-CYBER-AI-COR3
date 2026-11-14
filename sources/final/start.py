"""'Start here' page for the complete PDF: how to use the three PDFs, a daily routine, and a clickable where-to-find-what table."""
import json, subprocess, pathlib, html
F = pathlib.Path(__file__).parent
E = lambda s: html.escape(s, quote=True)

def find(doc, *keys, lvl=None):
    for e in doc[1]:
        if (lvl is None or e["lvl"] == lvl) and all(k.lower() in e["title"].lower() for k in keys):
            return doc[2][e["id"]]
    raise KeyError(keys)

def idx_page(doc, offset):
    from make import dests
    pre = doc[1][0]["id"].split("-")[0] + "-"
    return dests(doc[0])[0][pre + "pdf-index"] + 1 + offset

def build(g, c, r, START):
    rows = [
        ("Today", "Plan your day", "Playbook PDF → Today, or the Day modes", find(g, "Run your prep like a system")),
        ("Today", "Stuck on a problem", "The 7-step routine and the 20–40 rule", find(g, "One problem, done the efficient way")),
        ("Today", "Which pattern is this?", "20 triggers and the constraint table", find(g, "name the pattern")),
        ("Today", "Copy a C++ template", "Binary search, sliding window, graphs, DSU…", find(c, "Templates")),
        ("Today", "Solve a DP problem", "The 5-step DP recipe", find(c, "DP recipe")),
        ("This week", "This week's plan", "Every week and month of the plan", find(r, "Week by week", lvl=1)),
        ("This week", "Learn faster", "12 methods + AI prompts + 80/20 list", find(g, "The efficiency system")),
        ("This week", "Core CS questions", "OS, DBMS, CN, OOP, SQL by level", find(g, "OS, DBMS")),
        ("This week", "Security ladder", "PortSwigger → pwn.college → bug bounty", find(g, "Security ladder")),
        ("This month", "Am I on track?", "Milestone checklists by date", find(g, "Milestone checklists")),
        ("Applying", "Apply off-campus", "Channels, quotas, referral + cold email templates", find(g, "hiring machine")),
        ("Applying", "Interview coming up", "Rounds, STAR stories, offers, mock schedule", find(g, "Interviews, rounds")),
        ("Stretch", "Am I ready for HFT?", "The 31 Mar gate and the Elite track", find(g, "The HFT track")),
        ("Motivation", "Tier-3 stories", "16 students who did it, with sources", find(g, "Stories")),
    ]
    parts = [("1", "Placement Field Guide", "Levels, efficiency system, every ladder, off-campus machine, stories", idx_page(g, START)),
             ("2", "Prep Cheat Sheet", "Rules, complexity, STL, patterns, templates, DP, Core CS, SQL, security, AWS", idx_page(c, START + g[3])),
             ("3", "Placement Roadmap", "Timeline, phases, week-by-week and day-by-day plan, milestones", idx_page(r, START + g[3] + c[3]))]
    KB = "https://claude.ai/artifact/McuS723LTAb16Q6SpdUsAT"
    html_ = f'''<!doctype html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=Inter:wght@400;600;700&family=JetBrains+Mono:wght@500;600&display=swap" rel="stylesheet">
<style>@page {{ size: A4; margin: 0; }} * {{ box-sizing: border-box; }} html {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
body {{ margin: 0; padding: 13mm 14mm; font: 400 8.8pt/1.45 Inter, sans-serif; color: #1e293b; height: 295mm; overflow: hidden; }}
.eb {{ font: 600 8pt "JetBrains Mono"; letter-spacing: .14em; color: #c2410c; margin: 0 0 2mm; }}
h1 {{ font: 700 30pt/1 "Space Grotesk"; margin: 0 0 2mm; color: #0f172a; }}
.lead {{ font-size: 9.6pt; color: #475569; margin: 0 0 4mm; max-width: 170mm; }}
h2 {{ font: 700 12pt "Space Grotesk"; color: #0f172a; margin: 5mm 0 2mm; }}
.pdfs {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 3mm; }}
.pdfs div {{ border: 1px solid #e2e8f0; border-top: 4px solid var(--k); border-radius: 7px; padding: 3mm; }}
.pdfs b {{ font: 700 10pt "Space Grotesk"; display: block; color: #0f172a; }} .pdfs p {{ margin: 1mm 0 0; color: #475569; font-size: 8.3pt; }}
.pdfs a {{ color: #c2410c; text-decoration: none; }}
.parts {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 3mm; }}
.parts .pt {{ border-radius: 7px; background: #fff7ed; border: 1px solid #fed7aa; padding: 2.5mm 3mm; }}
.pt b {{ font: 700 9.5pt "Space Grotesk"; }} .pt span {{ float: right; font: 600 8pt "JetBrains Mono"; color: #c2410c; }} .pt p {{ margin: 1mm 0 0; font-size: 7.8pt; color: #64748b; }}
ol.day {{ margin: 0; padding-left: 5mm; display: grid; grid-template-columns: 1fr 1fr; column-gap: 8mm; row-gap: 1mm; }}
ol.day li b {{ color: #0f172a; }}
table {{ width: 100%; border-collapse: collapse; font-size: 8.6pt; }}
th {{ text-align: left; font: 600 7pt "JetBrains Mono"; letter-spacing: .08em; text-transform: uppercase; color: #64748b; background: #f1f5f9; padding: 1.4mm 2mm; }}
td {{ padding: 1.1mm 2mm; border-bottom: 1px solid #e2e8f0; }}
td.w {{ font: 600 7pt "JetBrains Mono"; color: #94a3b8; text-transform: uppercase; width: 21mm; }}
td.n {{ font: 600 8.4pt "JetBrains Mono"; color: #c2410c; text-align: right; width: 18mm; white-space: nowrap; }}
td.t b {{ color: #0f172a; }} td.t span {{ color: #64748b; }}
.tip {{ margin-top: 4mm; padding: 2.5mm 3.5mm; border-left: 4px solid #2563eb; background: #eff6ff; border-radius: 0 7px 7px 0; font-size: 8.5pt; }}
</style></head><body>
<p class="eb">START HERE · OPEN THIS PAGE FIRST</p>
<h1>Your placement kit</h1>
<p class="lead">Three PDFs, a revision tracker and one live site. Everything on this page is tappable: rows jump to the right page, underlined topic names anywhere open their in-depth page online, and every section has an <b>↑ Index</b> button to come back. Use the bookmarks panel in your PDF viewer for the full outline.</p>
<h2>Your kit</h2>
<div class="pdfs"><div style="--k:#c2410c"><b>This PDF · Complete</b><p>Guide + Cheat Sheet + Roadmap. Open it to plan, look things up and check progress.</p></div>
<div style="--k:#2563eb"><b>Knowledge Base PDF</b><p>147 pages: concepts, 43 tested solutions, model answers. Online: <a href="{KB}">Knowledge Base</a>.</p></div>
<div style="--k:#16a34a"><b>Playbook PDF</b><p>Café theme: Today and all 13 parts. Tick progress in the online playbook.</p></div>
<div style="--k:#7c3aed"><b>Revision tracker</b><p>Google Sheet: log each problem, revision dates fill in, a Due today tab. <a href="https://docs.google.com/spreadsheets/d/1JhZAMJmKocsnES-4Rhn-gSnhuJA9XoSHccqPZWZwREY/edit">Open it</a>.</p></div></div>
<h2>Inside this PDF</h2>
<div class="parts">{"".join(f'<div class="pt" data-target="{pg}"><b>{n} · {E(t)}</b><span>p. {pg}</span><p>{E(d)}</p></div>' for n, t, d, pg in parts)}</div>
<h2>Every day in five steps</h2>
<ol class="day"><li><b>Pick your day mode</b> (full force, college, exam, low energy, sprint).</li><li><b>Revise first:</b> the tracker's Due today tab (1-3-7-21).</li>
<li><b>New work in 50/10 blocks:</b> Striver in order, then LeetCode, Core CS, cyber, AWS.</li><li><b>Stuck or unsure?</b> Tap the topic name → Knowledge Base page.</li>
<li><b>Night, 5 min:</b> error log + tomorrow's 3 problems. <b>Sunday:</b> weekly review.</li><li><b>Never zero:</b> one problem touched keeps the streak.</li></ol>
<h2>Where to find what</h2>
<table><thead><tr><th>When</th><th>I want to…</th><th style="text-align:right">Page</th></tr></thead><tbody>
{"".join(f'<tr data-target="{pg}"><td class="w">{E(w)}</td><td class="t"><b>{E(t)}</b> · <span>{E(d)}</span></td><td class="n">p. {pg} →</td></tr>' for w, t, d, pg in rows)}
</tbody></table>
<p class="tip"><b>Export your playbook progress on 18 Nov</b> (Logs → Back up progress) before Claude Pro ends on 19 Nov.</p>
</body></html>'''
    (F / "start.html").write_text(html_)
    js = F / "start.js"
    js.write_text('''const { chromium } = require('playwright'); const fs = require('fs');
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 794, height: 1123 } });
  await p.goto('file://' + __dirname + '/start.html', { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready);
  const boxes = await p.evaluate(() => [...document.querySelectorAll('[data-target]')].map(e => { const r = e.getBoundingClientRect(); return [r.left, r.top, r.right, r.bottom, +e.dataset.target]; }));
  fs.writeFileSync(__dirname + '/start-boxes.json', JSON.stringify(boxes));
  await p.pdf({ path: __dirname + '/start.pdf', format: 'A4', printBackground: true, preferCSSPageSize: true }); await b.close(); })();''')
    subprocess.run(["node", str(js)], check=True)
    from pypdf import PdfReader
    rd = PdfReader(str(F / "start.pdf")); assert len(rd.pages) == START, f"start page is {len(rd.pages)} pages"
    H = float(rd.pages[0].mediabox.height); k = 72 / 96
    links = [(0, (l * k, H - b_ * k, rr * k, H - t * k), tgt) for l, t, rr, b_, tgt in json.loads((F / "start-boxes.json").read_text())]
    return F / "start.pdf", links
