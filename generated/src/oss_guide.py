"""Open-source and GSoC starter guide. Run from the repo root: bash generated/oss/git_workflow_check.sh && python3 generated/src/oss_guide.py"""
import html, io, pathlib, re, subprocess
from pypdf import PdfReader, PdfWriter
from pypdf.generic import Fit
from reportlab.pdfgen import canvas
ROOT = pathlib.Path(__file__).resolve().parents[2]; OUT = ROOT / "generated"; SRC = OUT / "src"
GH = "https://github.com/kvp342/intrusion-detection-and-prevention/blob/ccr-ca7232a7-t7lq94/"
TREE = "https://github.com/kvp342/intrusion-detection-and-prevention/tree/ccr-ca7232a7-t7lq94/"
E = html.escape
USED = set()
def K(path, label=None):
    """Link to a kit file; every path is checked to exist before the PDF is built."""
    USED.add(path)
    url = (TREE + path.rstrip("/")) if path.endswith("/") else GH + path
    return f'<a class="kit" href="{url}">{E(label or path.replace("generated/", ""))}</a>'
def L(url, label): return f'<a href="{url}">{E(label)}</a>'
SOURCES = []
def S(url, label):
    """Cite an outside source: numbered in the Sources section."""
    if (url, label) not in SOURCES: SOURCES.append((url, label))
    n = SOURCES.index((url, label)) + 1
    return f'<sup><a href="#src">[{n}]</a></sup>'
def T(head, rows, cls=""):
    return f'<table class="{cls}"><thead><tr>{"".join(f"<th>{h}</th>" for h in head)}</tr></thead><tbody>' + "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows) + "</tbody></table>"
def UL(items): return "<ul>" + "".join(f"<li>{x}</li>" for x in items) + "</ul>"

SEC = []
def sec(id, title, body): SEC.append((id, title, body))
FAQ = ("https://developers.google.com/open-source/gsoc/faq", "Google Summer of Code FAQ (official)")
TL = ("https://developers.google.com/open-source/gsoc/timeline", "Google Summer of Code timeline (official)")
BLOG = ("https://opensource.googleblog.com/2026/02/introducing-the-185-organizations-for-gsoc-2026.html", "Google Open Source Blog: the 185 organisations for GSoC 2026")
LFE = ("https://docs.linuxfoundation.org/lfx/mentorship/mentee-guide/am-i-eligible", "LFX Mentorship: am I eligible? (official)")
LFA = ("https://docs.linuxfoundation.org/lfx/mentorship/mentee-guide/how-to-apply", "LFX Mentorship: how to apply (official)")
LFT = ("https://docs.linuxfoundation.org/lfx/mentorship/mentorship-program-timelines", "LFX Mentorship programme timelines (official)")
GHS = ("https://docs.github.com/en/search-github/searching-on-github/searching-issues-and-pull-requests", "GitHub Docs: searching issues and pull requests")
GHF = ("https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/syncing-a-fork", "GitHub Docs: syncing a fork")
C = lambda src: S(*src)

sec("why", "Why open source, and which programme", UL([
 "<b>What it gives you:</b> reviewed code in a real codebase, a public record recruiters can open, and mentors who can vouch for you. It also fits March 2027, when on-campus internship options are thin.",
 "<b>Google Summer of Code (GSoC):</b> paid, mentored work on an open-source project over a flexible 8 to 22 weeks. You must be at least 18 and a beginner to open source (regular contributors to a project do not count as beginners). Projects are small (about 90 hours), medium (about 175) or large (about 350). Payment depends on passing evaluations, not on your code being merged." + C(FAQ),
 "<b>LFX Mentorship (Linux Foundation):</b> paid terms of about three months on Linux Foundation projects, including CNCF cloud projects. You must be 18 by the start date and meet each project's prerequisites. You can apply to at most three projects per term, and applications open about four weeks before a term (the spring term runs 1 March to 31 May)." + C(LFE) + C(LFA) + C(LFT),
 "<b>Plain contributions:</b> no deadline and no stipend, but every merged pull request counts on your resume and makes a GSoC or LFX application much stronger.",
 "<b>Your fit:</b> C++ and Python, security, and cloud. Look at organisations tagged with security, networking, cloud or C++ on the GSoC organisations page, and at CNCF projects on LFX."]) +
 T(["", "GSoC (2026 cycle, for reference)", "LFX spring term"], [
  ["Organisations announced", "19 Feb 2026 (185 organisations)" + C(BLOG), "Projects listed on LFX from early January"],
  ["Talk to mentors", "19 Feb – 15 Mar 2026" + C(TL), "During the about four-week application window"],
  ["Applications", "16 – 31 Mar 2026, 18:00 UTC" + C(TL), "About four weeks before 1 March" + C(LFT)],
  ["Results", "30 Apr 2026" + C(TL), "Before the term starts"],
  ["Work", "Coding from 25 May 2026" + C(TL), "1 Mar – 31 May"]]) + '<p class="note">GSoC 2027 dates were not published when this was written (17 Nov 2026). Expect a similar pattern, and check the official timeline page from January; Google notes that the timeline can shift a little each year.</p>')

sec("plan", "Week by week: December to the deadline", T(["When", "Do", "Done when"], [
 ["Dec 2026, weeks 1–2", "Learn the workflow (Section 4) on your own repository. Read the GSoC FAQ and the LFX mentee guide end to end.", "You can fork, branch, open a PR and rebase without notes"],
 ["Dec 2026, weeks 3–4", "Shortlist 5 projects: language you know, active in the last month, clear contributing guide, friendly replies to newcomers. Build each one locally.", "All 5 build and their tests run on your machine"],
 ["Jan 2027", "Pick 2 projects. Fix 2–3 small issues (docs, tests, small bugs). Join their chat or mailing list and read old discussions before asking.", "At least one merged PR"],
 ["Early Feb 2027", "Read last year's GSoC project ideas for your 2 projects. Make one larger contribution in the area you want to propose.", "A PR that touches real code in that area"],
 ["Mid-Feb 2027", "When organisations are announced, check yours are in. Read their 2027 ideas list the same day.", "One idea chosen, mentor identified"],
 ["Late Feb – mid-Mar 2027", "Discuss the idea with the mentor in public channels. Draft the proposal (Section 6) and ask for one round of feedback.", "Mentor has seen your draft"],
 ["Contributor window (late Mar)", "Submit early, not on the last day. Keep contributing while proposals are reviewed.", "Submitted with time to spare"],
 ["If not selected", "Keep contributing anyway: LFX has three terms a year, and merged PRs stay on your resume.", "—"]]) +
 '<p class="note">Fit it around the plan: about 4 hours a week in December and January, taken from project time rather than DSA. The exam break (22 Mar – 7 Apr) overlaps the end of the GSoC window, so submit before it starts.</p>')

sec("find", "Finding a project and a first issue", UL([
 "<b>Signs of a healthy project:</b> commits in the last few weeks, issues answered within days, a CONTRIBUTING file, tests you can run, and maintainers who are polite to beginners.",
 "<b>Search GitHub for beginner issues:</b> <code>is:issue is:open label:\"good first issue\" language:C++</code> (or Python), optionally with <code>no:assignee</code> and <code>comments:&lt;3</code> to find untouched ones." + C(GHS),
 "<b>Good first contributions:</b> fix a broken doc example, add a missing test, improve an error message, reproduce a bug report and add the exact steps.",
 "<b>Before you start:</b> comment on the issue (\"I'd like to work on this; my plan is …\") and wait for a yes on anything bigger than a typo. Never open a PR for an issue someone else is working on.",
 "<b>Avoid:</b> drive-by PRs that only reformat code, mass typo PRs across many repos, and AI-generated changes you cannot explain line by line. Maintainers notice, and it can get you banned from a programme."]))

sec("git", "The pull-request workflow (tested)", "<p>Every command below was run end to end against local test repositories by <code>generated/oss/git_workflow_check.sh</code>, including a maintainer pushing a change while your PR was open." + C(GHF) + "</p><pre>" + E("""# once: fork on GitHub (button), then
git clone https://github.com/YOU/project.git && cd project
git remote add upstream https://github.com/OWNER/project.git
git remote -v                                 # origin = your fork, upstream = the project

# for every change: a new branch
git switch -c fix-typo-in-readme
# ... edit, build, run the project's tests ...
git add app.txt && git commit -m "Fix typo in app.txt"
git push -u origin fix-typo-in-readme         # then open the PR on GitHub

# the project moved on while you waited: update your branch
git fetch upstream
git rebase upstream/main                      # replay your commit on top of theirs
git push --force-with-lease origin fix-typo-in-readme   # safe force: refuses if someone else pushed

# keep your fork's main equal to the project's
git switch main && git merge --ff-only upstream/main && git push origin main""") + "</pre>" + UL([
 "One branch per PR; never work on main.", "Small PRs get reviewed; 1,000-line PRs wait.", "Run the project's tests and formatter before pushing; CI failures waste a reviewer's time.",
 "Use <code>--force-with-lease</code>, never plain <code>--force</code>, on a branch others may have seen."]))

sec("pr", "Writing the PR and talking to maintainers", "<h3>A PR description that gets reviewed</h3><pre>" + E("""Fix crash when config file is empty (#1234)

What: parse_config() returned a null pointer for an empty file and the caller
dereferenced it. It now returns an empty Config and logs a warning.
Why: reported in #1234; reproducible with `touch empty.cfg && app --config empty.cfg`.
Tests: added test_empty_config; all existing tests pass locally (ctest).
Notes: happy to rename the warning or move it if you prefer.""") + "</pre><h3>Messages</h3>" + UL([
 "<b>Asking for an issue:</b> \"Hi, I'd like to work on this. I reproduced it on main (steps below). My plan is to … Does that sound right?\"",
 "<b>Stuck:</b> say what you tried and what happened, with the exact error. Ask in the public channel, not by private message, so others benefit.",
 "<b>Review comments:</b> thank, fix, reply \"Done in &lt;commit&gt;\" under each comment. Do not argue style; follow the project's.",
 "<b>Silence:</b> wait a week, then one polite ping. Maintainers are often volunteers."]))

sec("proposal", "The proposal", T(["Section", "What to write"], [
 ["Title and summary", "One sentence on what you will build and why the project needs it."],
 ["About you", "Year, skills, time zone, hours a week available, and links to your merged PRs in this project (the strongest part)."],
 ["Problem", "What is missing or broken today, with links to issues or discussions."],
 ["Design", "How you will do it: components, files you will touch, alternatives you considered and why you rejected them. A small diagram helps."],
 ["Timeline", "Week by week until the end, with a deliverable for each evaluation. Include a buffer week and your exam dates."],
 ["Testing and docs", "How you will test it and what documentation you will write."],
 ["After the programme", "How you will keep maintaining it."]]) + UL([
 "Base it on the organisation's ideas list and on what the mentor said; do not invent an unrelated project.",
 "Be honest about time. GSoC sizes are about 90, 175 or 350 hours; pick the size you can really deliver." + C(FAQ),
 "Ask the mentor to review a draft at least a week before the deadline."]))

sec("mistakes", "Mistakes to avoid", UL([
 "Applying to many organisations with the same generic proposal.", "Starting in March: by then serious applicants have weeks of contributions.",
 "Opening many tiny PRs just to show a count.", "Asking 'how do I start?' without reading the contributing guide.",
 "Promising more hours than you have (exams, placements).", "Disappearing after selection: failing an evaluation ends the stipend."]))

sec("kit", "Where this fits in the kit", T(["Need", "Open"], [
 ["The overall plan and dates", K("generated/final-plan.pdf")], ["Git commands and debugging", K("generated/linux-git-debugging-sheet.pdf")],
 ["Docker and CI (most projects use CI)", K("generated/docker-ci-guide.pdf")], ["Putting PRs on your resume", K("generated/resume-kit.pdf")],
 ["GitHub profile", K("generated/profile-kit.pdf")], ["The tested workflow script", K("generated/oss/git_workflow_check.sh")]]))
# ------------------------------------------------------------------ build
for p in USED: assert (ROOT / p.rstrip("/")).exists(), p        # every kit link points at a real file
CSS = """@page { size: A4; margin: 13mm 14mm 15mm; } * { box-sizing: border-box; } html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { margin: 0; font: 400 9.2pt/1.5 Inter, sans-serif; color: #1e293b; } a { color: #1d4ed8; text-decoration: none; } a.kit { font: 600 7.8pt "JetBrains Mono"; color: #0f766e; }
.eb { font: 600 8pt "JetBrains Mono"; letter-spacing: .14em; color: #c2410c; margin: 0 0 2mm; } h1 { font: 700 30pt/1.05 "Space Grotesk"; margin: 0 0 3mm; color: #0f172a; } h1 span { color: #c2410c; }
h2 { font: 700 15pt "Space Grotesk"; color: #0f172a; margin: 0 0 3mm; padding-bottom: 1.5mm; border-bottom: 2px solid #c2410c; display: flex; align-items: baseline; }
h2 .num { color: #c2410c; margin-right: 3mm; } h2 .back { margin-left: auto; font: 600 7.5pt "JetBrains Mono"; color: #64748b; } h3 { font: 700 10.5pt "Space Grotesk"; color: #1d4ed8; margin: 3mm 0 1.5mm; }
section.sec { break-before: page; } table { border-collapse: collapse; width: 100%; margin: 1mm 0 2mm; break-inside: auto; } tr { break-inside: avoid; }
th { font: 600 7pt "JetBrains Mono"; text-transform: uppercase; letter-spacing: .05em; color: #64748b; background: #f1f5f9; padding: 1.3mm 2mm; text-align: left; }
td { border-bottom: 1px solid #e2e8f0; padding: 1.4mm 2mm; vertical-align: top; } table.km td:first-child { width: 45%; } ul { padding-left: 5mm; margin: 1mm 0; } li { margin-bottom: 1.6mm; }
.note { background: #fff7ed; border-left: 3px solid #c2410c; padding: 2mm 3mm; margin: 3mm 0; font-size: 8.6pt; } .lead { font-size: 10.5pt; } sup a { font: 600 6.5pt "JetBrains Mono"; color: #c2410c; }
table.ix td { padding: 1.6mm 2mm; } td.pg { text-align: right; font-family: "JetBrains Mono"; width: 14mm; } ol.src { font-size: 7.8pt; padding-left: 6mm; } ol.src li { margin-bottom: 1mm; word-break: break-all; }"""
def body(pages):
    pg = lambda k: str(pages.get(k, "00")) if pages else "00"
    ix = "".join(f'<tr><td><a href="#{i}">{n + 1}. {E(t)}</a></td><td class="pg"><a href="#{i}">{pg(i)}</a></td></tr>' for n, (i, t, _) in enumerate(SEC))
    ix += f'<tr><td><a href="#src">Sources ({len(SOURCES)})</a></td><td class="pg"><a href="#src">{pg("src")}</a></td></tr>'
    out = [f'''<section><p class="eb">OPEN SOURCE · GSOC AND LFX</p><h1>Open source<br><span>from first PR to GSoC</span></h1>
<p class="lead">A practical route from zero to a merged pull request and a GSoC or LFX application by March 2027: which programme fits, a week-by-week plan from December, how to find a first issue, the exact git workflow (tested), how to write PRs and talk to maintainers, and how to write the proposal. Programme rules and dates come from the official pages listed at the end.</p>
<table class="ix"><thead><tr><th>Section</th><th class="pg">Page</th></tr></thead><tbody>{ix}</tbody></table>
<p class="note">Start this week: Section 4 on a repository of your own. By the end of December, have five projects shortlisted and building on your machine.</p></section>''']
    for n, (i, t, b) in enumerate(SEC):
        out.append(f'<section class="sec" id="{i}"><h2><span class="num">{n + 1:02d}</span>{E(t)}<a class="back" href="#top">↑ Index</a></h2>{b}</section>')
    out.append('<section class="sec" id="src"><h2><span class="num">··</span>Sources<a class="back" href="#top">↑ Index</a></h2><p>Checked on 17 Nov 2026. Blogs and forum posts are single opinions; official pages win when they disagree. Numbers marked as rules of thumb are not company requirements.</p><ol class="src">'
               + "".join(f'<li><a href="{u}">{E(l)}</a><br>{E(u)}</li>' for u, l in SOURCES) + "</ol></section>")
    return "".join(out)
js = SRC / "ro.js"
def render(pages, name):
    (SRC / "oss.html").write_text(f'<!doctype html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700&family=Inter:wght@400;600&family=JetBrains+Mono:wght@600&display=swap" rel="stylesheet"><style>{CSS}</style></head><body><div id="top"></div>{body(pages)}</body></html>')
    js.write_text("const { chromium } = require('playwright'); (async () => { const b = await chromium.launch(); const p = await b.newPage(); await p.goto('file://' + __dirname + '/oss.html', { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready); await p.pdf({ path: __dirname + '/" + name + "', format: 'A4', printBackground: true, preferCSSPageSize: true }); await b.close(); })();")
    subprocess.run(["node", str(js)], check=True)
    r = PdfReader(str(SRC / name)); return {k.lstrip("/"): r.get_destination_page_number(v) + 1 for k, v in r.named_destinations.items()}, len(r.pages)
d1, n1 = render(None, "o1.pdf"); d2, n2 = render(d1, "o2.pdf"); assert n1 == n2 and all(d1[i] == d2[i] for i, _, _ in SEC)
w = PdfWriter(clone_from=PdfReader(str(SRC / "o2.pdf"))); w.add_outline_item("Index", 0, fit=Fit.fit())
for n, (i, t, _) in enumerate(SEC): w.add_outline_item(f"{n + 1}. {t}", d2[i] - 1, fit=Fit.fit())
w.add_outline_item("Sources", d2["src"] - 1, fit=Fit.fit())
NP = len(w.pages)
for k, pg in enumerate(w.pages):
    if k == 0: continue
    buf = io.BytesIO(); cv = canvas.Canvas(buf, pagesize=(float(pg.mediabox.width), float(pg.mediabox.height))); cv.setFont("Helvetica", 7.5); cv.setFillGray(.55)
    cv.drawRightString(float(pg.mediabox.width) - 26, 14, f"{k + 1} / {NP}"); cv.save(); buf.seek(0); pg.merge_page(PdfReader(buf).pages[0]); pg.compress_content_streams(level=9)
w.add_metadata({"/Title": "Open-source and GSoC starter guide"}); w.write(str(OUT / "open-source-gsoc-guide.pdf"))
for f in ("o1.pdf", "o2.pdf", "ro.js", "oss.html"): (SRC / f).unlink()
print(NP, "pages;", len(USED), "kit links;", len(SOURCES), "sources;", d2)
