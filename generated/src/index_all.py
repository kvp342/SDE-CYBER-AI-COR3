"""Index of everything: one PDF linking every file in the repository with what it is and when to use it.
Links point to the files on GitHub (the working branch), which open on a phone; a PDF's relative file links do not.
Regenerate it last, after everything else. Run from the repo root: python3 generated/src/index_all.py"""
import html, io, pathlib, re, subprocess
from collections import defaultdict
from pypdf import PdfReader, PdfWriter
from pypdf.generic import Fit
from reportlab.pdfgen import canvas
ROOT = pathlib.Path(__file__).resolve().parents[2]; OUT = ROOT / "generated"; SRC = OUT / "src"
E = lambda s: html.escape(str(s), quote=True)
GH = "https://github.com/kvp342/intrusion-detection-and-prevention/blob/ccr-ca7232a7-t7lq94/"
TREE = "https://github.com/kvp342/intrusion-detection-and-prevention/tree/ccr-ca7232a7-t7lq94/"
SELF = "generated/index-of-everything.pdf"
readme = (ROOT / "README.md").read_text()
DESC = dict(re.findall(r"^\| `([^`]+)` \| (.+?) \|\s*$", readme, re.M))
DESC["README.md"] = "What this repository is, with a table of every main file"
DESC[SELF] = "This index: every file in the repository, what it is and when to use it"
FILES = sorted(set(subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True).stdout.split()) | {SELF})
GROUPS = [
 ("start", "Start here", "Open these first; they link to most of the rest.", ["generated/final-plan.pdf", "index.html", "playbook.html", "roadmap.html", "generated/knowledge-base-v2.html", "generated/kb2/", "knowledge-base.html", "cheat-sheet.html", "README.md", "GEMINI-HANDOFF.md", "generated/", SELF]),
 ("pdf", "Main PDFs", "For offline reading and printing.", ["Placement-Prep-Complete.pdf", "DSA-Placement-Playbook.pdf", "Placement-Knowledge-Base.pdf", "Tier3-to-Top-Offer-Placement-Guide.pdf", "Striver-A2Z-DSA-Sheet-Classic.pdf", "Striver-A2Z-DSA-Sheet-2026.pdf"]),
 ("dsa", "DSA, OAs and the Elite track", "Daily from 18 Nov; OA sets on their dates (13 Feb to 3 Jul); the Elite pack only if the 31 Mar gate is passed.",
  ["generated/worked-solutions-2.pdf", "generated/worked-solutions-3.pdf", "generated/oa-simulation-packs.pdf", "generated/oa-simulation-packs-2.pdf", "generated/oa-simulation-packs-3.pdf", "generated/patterns-stl-card.pdf", "generated/stl_check.cpp", "generated/aptitude-pack.pdf", "generated/elite-track-pack.pdf", "generated/elite/", "generated/codeforces-ladder.pdf"]),
 ("cs", "Core CS, SQL and design", "1 hour a day of Core CS; one-pagers the night before any interview; LLD and system design in the placement sprint.",
  ["generated/core-cs-one-pagers.pdf", "generated/core-cs-mcq-bank.pdf", "generated/sql-pack.pdf", "generated/sql-pack.sql", "generated/sql-pack-2.pdf", "generated/sql-pack-2.sql", "generated/lld-pack.pdf", "generated/lld/", "generated/system-design-case-studies.pdf", "generated/sysdesign/"]),
 ("sec", "Cloud, security and research", "AWS 30 minutes a day, final revision 5 to 18 Apr; TenantWall before 21 Mar; labs in the cyber track.",
  ["generated/aws-saa-c03-study-pack.pdf", "generated/aws-lab-workbook.pdf", "generated/tenantwall-helpers.pdf", "generated/tenantwall-paper-outline.pdf", "generated/tenantwall/paper/", "generated/tenantwall/", "generated/security-lab-notebook.pdf", "generated/owasp-portswigger-lab-map.pdf", "generated/cyber-security-interview-bank.pdf", "generated/roadmapsh-checklists.pdf"]),
 ("proj", "Projects", "Backend project when the plan schedules it; AI-security project in May.",
  ["generated/backend-starter/", "generated/ai-security-starter/", "generated/ai-security-starter-guide.pdf", "generated/docker-ci-guide.pdf"]),
 ("jobs", "Interviews and applications", "From the placement sprint (31 May); resume and profiles a month earlier.",
  ["generated/resume-kit.pdf", "generated/resume/", "generated/interview-story-bank.pdf", "generated/profile-kit.pdf", "generated/profile/", "generated/company-files-2.pdf", "generated/company-files-3.pdf", "generated/mock-interview-scripts.pdf", "generated/mock-interview-scripts-2.pdf", "generated/interview-day-kit.pdf", "generated/interview-day/"]),
 ("rev", "Revision and planning", "Every day (flashcards) and every Sunday (planner and weekly review).",
  ["generated/anki/*.csv", "generated/anki-decks-guide.pdf", "generated/weekly-planner.pdf", "generated/weekly-revision-tests.pdf", "generated/linux-git-debugging-sheet.pdf"]),
]
listed = {p for *_, ps in GROUPS for p in ps}
missing_desc = [p for p in listed if p not in DESC]
assert not missing_desc, missing_desc
undescribed = [k for k in DESC if k.startswith("generated/") and k not in listed]
assert not undescribed, f"README rows not placed in a group: {undescribed}"
def url(p):
    if p.endswith("/"): return TREE + p.rstrip("/")
    if "*" in p: return TREE + p.split("*")[0].rstrip("/")
    return GH + p
def kind(p):
    parts = p.split("/")
    if p == SELF: return "this index"
    if parts[0] == "sources": return f"source for the {parts[1]} build" if len(parts) > 2 else "source"
    if parts[0] == "agent": return "agent instructions, backlog or log"
    if parts[:2] == ["generated", "src"]: return "build or check script"
    if parts[:2] == ["generated", "kb2"]: return "Knowledge Base v2 source"
    if len(parts) > 2 and parts[0] == "generated": return f"part of generated/{parts[1]}/"
    ext = p.rsplit(".", 1)[-1]
    return {"pdf": "PDF", "html": "web page", "md": "document", "js": "app script", "webmanifest": "app manifest", "png": "app icon", "csv": "flashcard deck", "cpp": "C++ source", "sql": "SQL file"}.get(ext, "file")
def body(pages):
    pg = lambda k: str(pages.get(k, "000")) if pages else "000"
    rows = "".join(f'<tr><td><a href="#{g}">{E(t)}</a></td><td class="pg"><a href="#{g}">{pg(g)}</a></td></tr>' for g, t, *_ in GROUPS) + f'<tr><td><a href="#all">Appendix: all {len(FILES)} files</a></td><td class="pg"><a href="#all">{pg("all")}</a></td></tr>'
    out = [f'''<section class="cover"><p class="eb">PLACEMENT KIT · INDEX</p><h1>Index of<br><span>everything</span></h1>
<p class="lead">Every file in the repository: what it is, when to use it, and a link that opens it on GitHub (phone or laptop). The main items are grouped by when you need them; the appendix lists every file, including build scripts and sources.</p>
<p class="how"><b>Fastest start.</b> Open <code>index.html</code> (the home screen) or the Playbook for today's work; open the Knowledge Base v2 to look anything up; use this index when you need a specific file. Links open the working branch <code>ccr-ca7232a7-t7lq94</code>; if you merge it, links still work while the branch exists.</p>
<table class="ix"><tbody>{rows}</tbody></table></section>''']
    for g, t, when, ps in GROUPS:
        r = "".join(f'<tr><td class="p"><a href="{url(p)}">{E(p)}</a></td><td>{E(DESC[p])}</td></tr>' for p in ps)
        out.append(f'<section class="grp" id="{g}"><h2>{E(t)}<a class="back" href="#top">↑ Index</a></h2><p class="when"><b>When:</b> {E(when)}</p><table class="t"><tbody>{r}</tbody></table></section>')
    by = defaultdict(list)
    for f in FILES: by[f.split("/")[0] if "/" not in f[len(f.split("/")[0]) + 1:] or f.count("/") < 2 else "/".join(f.split("/")[:2])].append(f)
    app = "".join(f'<tr><td class="p"><a href="{GH + f}">{E(f)}</a></td><td class="k">{E(DESC.get(f, kind(f)))}</td></tr>' for f in FILES)
    out.append(f'<section class="sec" id="all"><h2>Appendix: all {len(FILES)} files<a class="back" href="#top">↑ Index</a></h2><table class="t small"><tbody>{app}</tbody></table></section>')
    return "".join(out)
CSS = """@page { size: A4; margin: 12mm 12mm 14mm; } @page :first { margin: 0; }
* { box-sizing: border-box; } html { -webkit-print-color-adjust: exact; print-color-adjust: exact; } body { margin: 0; font: 400 8.8pt/1.42 Inter, sans-serif; color: #1e293b; }
a { color: #c2410c; text-decoration: none; } .cover { padding: 16mm 15mm; break-after: page; } .eb { font: 600 8pt "JetBrains Mono"; letter-spacing: .14em; color: #c2410c; margin: 0 0 3mm; } code { font: 600 7.8pt "JetBrains Mono"; }
h1 { font: 700 34pt/1.02 "Space Grotesk"; margin: 0 0 4mm; color: #0f172a; } h1 span { color: #c2410c; } .lead { font-size: 10pt; color: #475569; } .how { background: #fff7ed; border-left: 3px solid #c2410c; padding: 2mm 3mm; }
table { border-collapse: collapse; width: 100%; } .ix td { padding: 2.2mm 2mm; border-bottom: 1px solid #e2e8f0; font-size: 10.5pt; } .ix td a { color: #0f172a; font-weight: 600; } .ix .pg { text-align: right; } .ix .pg a { color: #c2410c; font-family: "JetBrains Mono"; }
.grp { break-inside: avoid; margin-bottom: 5mm; } .sec { break-before: page; } h2 { font: 700 13.5pt "Space Grotesk"; color: #0f172a; border-bottom: 3px solid #c2410c; padding-bottom: 1.2mm; margin: 0 0 1.5mm; display: flex; align-items: baseline; }
.back { margin-left: auto; font: 600 7.5pt "JetBrains Mono"; border: 1px solid #fdba74; background: #fff7ed; border-radius: 99px; padding: 0 7px; } .when { color: #475569; margin: 0 0 1.5mm; }
.t td { border-bottom: 1px solid #eef2f7; padding: 1.1mm 2mm; vertical-align: top; } .p { width: 44%; font: 400 7.6pt "JetBrains Mono"; word-break: break-all; } .small td { padding: .5mm 2mm; font-size: 7.6pt; } .k { color: #475569; }"""
js = SRC / "r.js"
def render(pages, name):
    (SRC / "ia.html").write_text(f'<!doctype html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700&family=Inter:wght@400;600&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet"><style>{CSS}</style></head><body><div id="top"></div>{body(pages)}</body></html>')
    js.write_text("const { chromium } = require('playwright'); (async () => { const b = await chromium.launch(); const p = await b.newPage(); await p.goto('file://' + __dirname + '/ia.html', { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready); await p.pdf({ path: __dirname + '/" + name + "', format: 'A4', printBackground: true, preferCSSPageSize: true }); await b.close(); })();")
    subprocess.run(["node", str(js)], check=True)
    r = PdfReader(str(SRC / name)); return {k.lstrip("/"): r.get_destination_page_number(v) + 1 for k, v in r.named_destinations.items()}, len(r.pages)
KEYS = [g for g, *_ in GROUPS] + ["all"]
d1, n1 = render(None, "p1.pdf"); d2, n2 = render(d1, "p2.pdf"); assert n1 == n2 and all(d1[k] == d2[k] for k in KEYS)
w = PdfWriter(clone_from=PdfReader(str(SRC / "p2.pdf"))); w.add_outline_item("Index", 0, fit=Fit.fit())
for g, t, *_ in GROUPS: w.add_outline_item(t, d2[g] - 1, fit=Fit.fit())
w.add_outline_item("All files", d2["all"] - 1, fit=Fit.fit())
NP = len(w.pages)
for i, pg in enumerate(w.pages):
    if i == 0: continue
    buf = io.BytesIO(); c = canvas.Canvas(buf, pagesize=(float(pg.mediabox.width), float(pg.mediabox.height))); c.setFont("Helvetica", 7.5); c.setFillGray(.55)
    c.drawRightString(float(pg.mediabox.width) - 26, 14, f"{i + 1} / {NP}"); c.save(); buf.seek(0); pg.merge_page(PdfReader(buf).pages[0]); pg.compress_content_streams(level=9)
w.add_metadata({"/Title": "Index of everything"}); w.write(str(OUT / "index-of-everything.pdf"))
for f in ("p1.pdf", "p2.pdf", "r.js", "ia.html"): (SRC / f).unlink()
print(NP, "pages;", len(FILES), "files;", len(listed), "main items")
