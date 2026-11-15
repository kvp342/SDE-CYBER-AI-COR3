"""Company files II: six more companies, same format as sources/kb/t_companies.py, with sources found by web search on 15 Nov 2026.
Everything about a process is what candidates report; it changes yearly. Run from the repo root: python3 generated/src/company2.py"""
import html, io, pathlib, subprocess
from pypdf import PdfReader, PdfWriter
from pypdf.generic import Fit
from reportlab.pdfgen import canvas
ROOT = pathlib.Path(__file__).resolve().parents[2]; OUT = ROOT / "generated"; SRC = OUT / "src"
E = lambda s: html.escape(str(s), quote=True)
KB = "https://claude.ai/artifact/McuS723LTAb16Q6SpdUsAT#"
NOTE = "Based on a small number of anonymous, self-reported candidate posts (mostly 2025). Processes change every year and differ between on-campus and off-campus: read 3 to 5 recent posts for your exact role before the interview."
CO = [
 dict(id="co-uber", title="Uber (SDE intern and SDE-1)", lvl=3,
  why="A high-bar product company with engineering teams in Bengaluru and Hyderabad. Reports describe a hard online assessment, so speed on medium-hard problems decides who gets interviews.",
  process=["Online assessment: reports describe 3 problems; one India report calls all three LeetCode-hard, another says the problems were framed as real-world Uber scenarios.",
           "Interviews: DSA rounds, plus design (LLD for SDE-1 in one report, high-level design in another) and a resume and behavioural discussion.",
           "Reports from 2025 disagree on difficulty for new-grad roles; many posts are for interns or SDE-2, which may overstate the fresher bar."],
  prep=["The Hard pass and timed contests are what matter for the OA", "LLD pack: rate limiter and parking lot are close to the kind of design asked", "Run OA sets 5 to 8 and Mocks 3, 4 and 6"],
  pit=["Solving one OA problem perfectly and leaving the rest blank", "Over-engineering the LLD before the core works"],
  ask=["A graph or DP problem with a real-world story", "Design a component such as a rate limiter or a ride-matching queue"],
  sources=[("Jointaro: Uber SDE intern India, June 2025", "https://www.jointaro.com/interviews/companies/uber/experiences/software-development-engineer-sde-intern-india-june-1-2025-declined-offer-positive-17a27aca"),
           ("Jointaro: Uber software developer India, July 2025", "https://www.jointaro.com/interviews/companies/uber/experiences/software-developer-india-july-1-2025-no-offer-neutral-49db9c91"),
           ("Glassdoor: Uber SDE-1 review", "https://www.glassdoor.co.in/Interview/Uber-Interview-E575263-RVW99627683.htm"), ("PrepInsta: Uber SDE-1 interview experience", "https://prepinsta.com/?p=1621210")],
  rel=["dp", "bfs", "lld"]),
 dict(id="co-salesforce", title="Salesforce (AMTS)", lvl=2,
  why="Hires freshers as Associate Member of Technical Staff (AMTS), often through campus and pool drives in India. Reports describe a supportive, DSA-focused process.",
  process=["Online assessment: a HackerRank coding test in a 2025 pool-campus report; one review describes 3 medium-hard problems on graphs, greedy and DP.",
           "Interviews: the same pool-campus report describes 2 virtual technical rounds on DSA, then an on-site hiring-manager round. Asteroid Collision and a sliding-window problem appear in reports.",
           "Candidates describe interviewers who guide you when you are stuck: think aloud."],
  prep=["Graphs, greedy and DP from the Hard pass", "OA set 1 contains Asteroid Collision; redo it", "Prepare project stories for the hiring-manager round (Mock 8)"],
  pit=["Staying silent when stuck: the interviewers are reported to help if you explain your thinking"],
  ask=["Asteroid Collision", "A sliding-window or graph medium", "Walk me through a project you built"],
  sources=[("LeetCode: Salesforce AMTS, India pool campus hiring", "https://leetcode.com/discuss/post/8514030/salesforce-amts-interview-experience-ind-ijyg/"),
           ("Jointaro: Salesforce AMTS India, July 2025", "https://www.jointaro.com/interviews/companies/salesforce/experiences/amts-software-engineer-india-july-24-2025-declined-offer-positive-3237c147"),
           ("Let's Code: Salesforce AMTS interview experience", "https://lets-code.co.in/interview-experience/salesforce-associate-member-of-technical-staff-(amts)/68f4c145677cbb233117e35d/"),
           ("Glassdoor: Salesforce interview review", "https://www.glassdoor.co.in/Interview/Salesforce-Interview-E11159-RVW99280293.htm")],
  rel=["greedy", "dp", "stack-queue"]),
 dict(id="co-adobe", title="Adobe (MTS-1)", lvl=2,
  why="Hires freshers as Member of Technical Staff (MTS-1), with large teams in Noida and Bengaluru. Reports stress writing complete code for classic algorithms, plus Core CS.",
  process=["2025 Noida reports: an HR screen, then several technical rounds (one report says four); questions included implementing KMP and Kadane's algorithm in full, the upper bound of an element in a sorted array, and generating all permutations.",
           "Older India reports: 2 data-structure rounds that also covered OOP and OS, then a hiring-manager round and an HR round.",
           "Some campus drives used an online test with aptitude as well as coding; one candidate said aptitude accuracy separated candidates."],
  prep=["String algorithms (KMP) and Kadane: write them from memory", "Aptitude pack for campus tests", "Core CS one-pagers (OOP, OS) before the technical rounds"],
  pit=["Knowing an algorithm's idea but not being able to code it fully", "Skipping aptitude practice"],
  ask=["Implement KMP", "Maximum subarray (Kadane)", "Upper bound in a sorted array; all permutations"],
  sources=[("Glassdoor: Adobe MTS-1 interview questions", "https://static.glassdoor.at/Interview/Adobe-MTS-1-Interview-Questions-EI_IE1090.0,5_KO6,11.htm"),
           ("GeeksforGeeks: Adobe MTS-1 (off-campus)", "https://www.geeksforgeeks.org/adobe-interview-experience-for-mts-1-off-campus/"),
           ("GeeksforGeeks: Adobe MTS-1 interview experience", "https://www.geeksforgeeks.org/adobe-interview-experience-for-mts-1-2/")],
  rel=["string-algos", "dp", "binary-search"]),
 dict(id="co-walmart", title="Walmart Global Tech India (Software Engineer)", lvl=2,
  why="Recruits freshers on campus in India; campus posts list the fresher role as SDE-2 (Software Engineer II). Few 2025 fresher reports exist, so read new posts before your drive.",
  process=["Campus drives in older reports: an online coding test (HackerEarth in one), then about 3 interview rounds.",
           "Rounds mix DSA (two LeetCode mediums in one report) with computer-science fundamentals: OOP, OS, SQL and networks; some include schema or system design.",
           "2025 reviews found are mostly for experienced hires; treat the fresher details as indicative."],
  prep=["Two mediums in 45 minutes: OA sets and DSA mocks", "Core CS one-pagers and the SQL pack for the fundamentals round", "System design one-pager for a light design question"],
  pit=["Neglecting SQL and networks because the OA is DSA"],
  ask=["Two medium DSA problems", "Design a schema for orders", "OOP, OS and SQL questions"],
  sources=[("LeetCode: Walmart Global Tech India SDE-2 (fresher) on-campus questions", "https://leetcode.com/discuss/post/2559079/walmart-global-tech-india-sde2fresher-oncampus-interview-questions"),
           ("Glassdoor: Walmart Global Tech interview review", "https://www.glassdoor.co.in/Interview/Walmart-Global-Tech-Interview-E3293060-RVW90950596.htm"),
           ("GeeksforGeeks: Walmart SDE-2 on-campus 2021", "https://www.geeksforgeeks.org/walmart-interview-experience-for-sde-2-on-campus-2021-virtual/amp/")],
  rel=["acid", "oop", "hld"]),
 dict(id="co-phonepe", title="PhonePe (SDE-1)", lvl=3,
  why="Fintech in Bengaluru known for its machine-coding round. Clean, extensible, tested code matters as much as getting it working.",
  process=["Machine coding: reports describe 60 to 90 minutes to build a working application (for example a customer-issue resolution system), with modular structure, validations, exception handling and sometimes concurrency.",
           "A follow-up review of your code: interviewers ask why you made each design choice and how it would scale or extend.",
           "DSA rounds also appear (a word-search-in-a-grid problem in one 2025 report)."],
  prep=["LLD pack: write each design again in 90 minutes without looking", "Backend starter: practise layering, validation and tests", "Run Mock 6 twice; practise explaining trade-offs aloud"],
  pit=["Code in one big class with no separation", "No input validation or error handling", "Not being able to justify a design decision"],
  ask=["Build an issue-tracking or booking system in 90 minutes", "Why this class structure? How would you add a new feature?", "Word search in a grid"],
  sources=[("LeetCode: My PhonePe SDE-1 interview experience", "https://leetcode.com/discuss/post/6437867/"), ("LeetCode: PhonePe machine coding round, SDE", "https://leetcode.com/discuss/interview-experience/6980677"),
           ("Jointaro: PhonePe software engineer Bengaluru, Sept 2025", "https://www.jointaro.com/interviews/companies/phonepe/experiences/software-engineer-bengaluru-karnataka-september-1-2025-no-offer-neutral-f435d5c3"),
           ("Glassdoor: PhonePe interview review", "https://www.glassdoor.co.in/Interview/PhonePe-Interview-E2289138-RVW99430224.htm")],
  rel=["lld", "solid", "oop"]),
 dict(id="co-zscaler", title="Zscaler (software engineer, security company)", lvl=2,
  why="A cloud-security company with large engineering teams in India; a natural target for your security profile. Reports describe a selective process with strong C/C++ and fundamentals.",
  process=["Campus: an online coding round first (a Bengaluru C/C++ developer offer report), then technical interviews.",
           "Reports mention DSA, OOP, DBMS and C++ questions; one write-up describes an online assessment, a group discussion and two interviews.",
           "Pass rates in aggregated reports are low, but samples are small (3 to 9 reports)."],
  prep=["C++ depth: the STL card, the 30 bugs and the LLD code", "OS and networks one-pagers: a networking company asks about TCP, TLS and proxies", "TenantWall and the security lab notebook give you security stories"],
  pit=["Weak C++ details (memory, pointers, virtual functions)", "No security examples on the resume"],
  ask=["A medium DSA problem in C++", "Explain how TLS works", "Questions on OOP and DBMS"],
  sources=[("LeetCode: Zscaler internship + FTE, C/C++ developer, on-campus Bengaluru", "https://leetcode.com/discuss/post/4706480/Zscaler-or-Internship-%2B-FTE-or-Software-Developer-CC%2B%2B-or-On-Campus-or-Bangalore-Offer-Accepted/"),
           ("Jointaro: Zscaler SDE India, Oct 2025", "https://www.jointaro.com/interviews/companies/zscaler/experiences/software-development-engineer-sde-india-october-4-2025-accepted-offer-positive-69c24042"),
           ("PracHub: Zscaler software engineer, OA, group discussion and two interviews", "https://prachub.com/interview-experiences/zscaler-software-engineer-interview-online-assessment-group-discussion-and-two-interviews-b6142643e1"),
           ("Glassdoor: Zscaler interview review", "https://www.glassdoor.co.in/Interview/Zscaler-Interview-E359434-RVW69325822.htm")],
  rel=["tcp-udp", "http-tls", "oop"]),
]
def body(pages):
    pg = lambda k: str(pages.get(k, "000")) if pages else "000"
    rows = "".join(f'<tr><td><a href="#{c["id"]}">{E(c["title"])}</a><div class="f">{E(c["why"])}</div></td><td class="pg"><a href="#{c["id"]}">{pg(c["id"])}</a></td></tr>' for c in CO)
    out = [f'''<section class="cover"><p class="eb">COMPANIES · FILES II</p><h1>Six more<br><span>company files</span></h1>
<p class="lead">Uber, Salesforce, Adobe, Walmart Global Tech, PhonePe and Zscaler, in the same format as the ten files in the Knowledge Base: what candidates report about the process, how your plan prepares you, common mistakes, likely questions and the sources. Palo Alto Networks was also considered, but no India new-grad reports turned up, so it is left out rather than guessed.</p>
<p class="how"><b>Read this first.</b> {E(NOTE)} See the <a href="{KB}companies-howto">company files guide</a> for how to use these the week before an interview.</p>
<table class="ix"><tbody>{rows}</tbody></table></section>''']
    for c in CO:
        li = lambda xs: "".join(f"<li>{E(x)}</li>" for x in xs)
        out.append(f'''<section class="sec" id="{c["id"]}"><h2>{E(c["title"])}<a class="back" href="#top">↑ Index</a></h2><p class="why">{E(c["why"])}</p>
<h3>What candidates report</h3><ul>{li(c["process"])}</ul><h3>How your plan prepares you</h3><ul>{li(c["prep"])}</ul>
<div class="two"><div><h3>Common mistakes</h3><ul>{li(c["pit"])}</ul></div><div><h3>Questions to expect</h3><ul>{li(c["ask"])}</ul></div></div>
<h3>Sources</h3><ul class="src">{"".join(f"<li><a href={chr(34)}{u}{chr(34)}>{E(t)}</a></li>" for t, u in c["sources"])}</ul>
<p class="meta">Related Knowledge Base pages: {", ".join(f'<a href="{KB}{r}">{r}</a>' for r in c["rel"])}.</p></section>''')
    return "".join(out)
CSS = """@page { size: A4; margin: 12mm 13mm 14mm; } @page :first { margin: 0; }
* { box-sizing: border-box; } html { -webkit-print-color-adjust: exact; print-color-adjust: exact; } body { margin: 0; font: 400 9.2pt/1.5 Inter, sans-serif; color: #1e293b; }
a { color: #c2410c; text-decoration: none; } .cover { padding: 16mm 15mm; break-after: page; } .eb { font: 600 8pt "JetBrains Mono"; letter-spacing: .14em; color: #c2410c; margin: 0 0 3mm; }
h1 { font: 700 34pt/1.02 "Space Grotesk"; margin: 0 0 4mm; color: #0f172a; } h1 span { color: #c2410c; } .lead { font-size: 10pt; color: #475569; } .how { background: #fff7ed; border-left: 3px solid #c2410c; padding: 2mm 3mm; }
table { border-collapse: collapse; width: 100%; } .ix td { padding: 2mm; border-bottom: 1px solid #e2e8f0; vertical-align: top; } .ix td a { color: #0f172a; font-weight: 600; font-size: 10pt; } .ix .f { font-size: 8pt; color: #64748b; } .ix .pg { text-align: right; } .ix .pg a { color: #c2410c; font-family: "JetBrains Mono"; }
.sec { break-before: page; } h2 { font: 700 16pt "Space Grotesk"; color: #0f172a; border-bottom: 3px solid #c2410c; padding-bottom: 1.5mm; margin: 0 0 2.5mm; display: flex; align-items: baseline; } .back { margin-left: auto; font: 600 7.5pt "JetBrains Mono"; border: 1px solid #fdba74; background: #fff7ed; border-radius: 99px; padding: 0 7px; }
.why { font-size: 10pt; color: #334155; } h3 { font: 700 10.5pt "Space Grotesk"; color: #1d4ed8; margin: 4mm 0 1.2mm; } ul { padding-left: 5mm; margin: 0; } li { margin-bottom: 1.3mm; } .two { display: grid; grid-template-columns: 1fr 1fr; gap: 6mm; }
.src li { font-size: 8.4pt; } .meta { color: #64748b; font-size: 8.4pt; margin-top: 3mm; }"""
js = SRC / "r.js"
def render(pages, name):
    (SRC / "co.html").write_text(f'<!doctype html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700&family=Inter:wght@400;600&family=JetBrains+Mono:wght@600&display=swap" rel="stylesheet"><style>{CSS}</style></head><body><div id="top"></div>{body(pages)}</body></html>')
    js.write_text("const { chromium } = require('playwright'); (async () => { const b = await chromium.launch(); const p = await b.newPage(); await p.goto('file://' + __dirname + '/co.html', { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready); await p.pdf({ path: __dirname + '/" + name + "', format: 'A4', printBackground: true, preferCSSPageSize: true }); await b.close(); })();")
    subprocess.run(["node", str(js)], check=True)
    r = PdfReader(str(SRC / name)); return {k.lstrip("/"): r.get_destination_page_number(v) + 1 for k, v in r.named_destinations.items()}, len(r.pages)
if __name__ == "__main__":
    d1, n1 = render(None, "p1.pdf"); d2, n2 = render(d1, "p2.pdf"); assert n1 == n2 and all(d1[c["id"]] == d2[c["id"]] for c in CO)
    w = PdfWriter(clone_from=PdfReader(str(SRC / "p2.pdf"))); w.add_outline_item("Index", 0, fit=Fit.fit())
    for c in CO: w.add_outline_item(c["title"], d2[c["id"]] - 1, fit=Fit.fit())
    NP = len(w.pages)
    for i, pg in enumerate(w.pages):
        if i == 0: continue
        buf = io.BytesIO(); cv = canvas.Canvas(buf, pagesize=(float(pg.mediabox.width), float(pg.mediabox.height))); cv.setFont("Helvetica", 7.5); cv.setFillGray(.55)
        cv.drawRightString(float(pg.mediabox.width) - 26, 14, f"{i + 1} / {NP}"); cv.save(); buf.seek(0); pg.merge_page(PdfReader(buf).pages[0]); pg.compress_content_streams(level=9)
    w.add_metadata({"/Title": "Company files II"}); w.write(str(OUT / "company-files-2.pdf"))
    for f in ("p1.pdf", "p2.pdf", "r.js", "co.html"): (SRC / f).unlink()
    print(NP, "pages", d2)
