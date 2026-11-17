"""Company files III: six more companies, same format as sources/kb/t_companies.py, with sources found by web search on 15 Nov 2026.
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
 dict(id="co-oracle", title="Oracle (software engineer, campus)", lvl=2,
  why="Hires many freshers through campus drives in Hyderabad, Bengaluru and Noida. Reports describe a fundamentals-heavy process at a fresher level.",
  process=["Online assessment: in one Bengaluru report, 2 coding questions plus MCQs on CS fundamentals; a Noida report also mentions MCQs with DSA.",
           "Interviews: a 2025 Hyderabad report describes two technical interviews and an HR round after the online test; others say 3 to 4 rounds in total.",
           "Reported topics: graphs, linked lists, DP, DFS, multithreading, and in-depth questions on your projects; one report adds a little system design."],
  prep=["Core CS MCQ bank and one-pagers for the online test", "OA sets for the 2 coding questions", "Explain one project end to end, including what you would change"],
  pit=["Ignoring the MCQ section", "Not knowing basic multithreading (threads, locks, race conditions)"],
  ask=["A graph or linked-list problem", "Process vs thread; how a mutex works", "Walk me through your project"],
  sources=[("Jointaro: Oracle software engineer Hyderabad, April 2025", "https://www.jointaro.com/interviews/companies/oracle/experiences/software-engineer-hyderabad-april-1-2025-no-offer-positive-81336417/"),
           ("Glassdoor: Oracle campus interview, Hyderabad, Dec 2025", "https://static.glassdoor.com.ar/Interview/Oracle-Interview-E1737-RVW104063014.htm"),
           ("LeetCode: Oracle software engineer campus drive (intern + FTE)", "https://leetcode.com/discuss/post/3871303/oracle-interview-experience-software-engineer-campus-drive-intern-fte-cgbu"),
           ("Glassdoor: Oracle interview review", "https://www.glassdoor.co.in/Interview/Oracle-Interview-E1737-RVW104012964.htm")],
  rel=["qa-os", "bfs", "dp"]),
 dict(id="co-cisco", title="Cisco (software engineer, fresher)", lvl=2,
  why="Networking company with large teams in Bengaluru; a good fit for a cyber-security CSE student because networking questions appear alongside DSA.",
  process=["Online assessment: reports mention coding questions together with networking and computer-fundamentals MCQs.",
           "Interviews: commonly two technical rounds, sometimes a manager round, then HR; some drives merge technical and managerial rounds.",
           "Reported topics: DSA, OOP, OS, DBMS and computer networks (TCP/IP, subnetting, routing)."],
  prep=["Computer Networks one-pager and the CN section of the MCQ bank", "OA sets for coding", "Security lab notebook for networking commands and concepts"],
  pit=["Weak networking basics despite the company's domain", "Thin OOP answers"],
  ask=["Explain the TCP three-way handshake", "Subnet a /26 network", "A medium DSA problem"],
  sources=[("FACE Prep: Cisco hiring process for freshers", "https://faceprep.in/article/cisco-hiring-process-for-freshers-2026/"),
           ("Jointaro: Cisco SDE India, Oct 2025", "https://www.jointaro.com/interviews/companies/cisco/experiences/software-development-engineer-sde-india-october-4-2025-declined-offer-positive-b0d4dea8"),
           ("Jointaro: Cisco software engineer trainee Bengaluru, June 2025", "https://www.jointaro.com/interviews/companies/cisco/experiences/software-engineer-trainee-bengaluru-june-1-2025-accepted-offer-positive-854fc872/"),
           ("Jointaro: Cisco SDE Bengaluru, July 2025", "https://www.jointaro.com/interviews/companies/cisco/experiences/software-development-engineer-sde-bengaluru-july-26-2025-no-offer-neutral-b0b34274")],
  rel=["qa-cn", "tcp-udp", "oop"]),
 dict(id="co-swiggy", title="Swiggy (SDE-1)", lvl=3,
  why="Food and quick-commerce platform in Bengaluru. Reports describe DSA plus a machine-coding or LLD round with high expectations.",
  process=["Early rounds: an online assessment or a DSA round (two problems in one 2025 report).",
           "Machine coding or LLD: reports describe building a small system in a fixed time (45 to 90 minutes) or a demanding LLD discussion; for Android and frontend roles the build is app or UI work.",
           "Later rounds: hiring manager or HR, and for some candidates system design."],
  prep=["LLD pack: rebuild designs in 60–90 minutes", "Backend starter for clean layering and tests", "Mock 6 and the LLD mock script"],
  pit=["Working code with no structure", "No discussion of extensibility or edge cases"],
  ask=["Design and code a small system (for example a library or ordering service)", "Two DSA problems", "Why this class design?"],
  sources=[("LeetCode: Swiggy SDE-1 interview experience", "https://leetcode.com/discuss/post/8362896/swiggy-interview-experience-sde-1-by-sha-5wpc/"),
           ("LeetCode: Swiggy SDE-1, high expectations in the LLD round", "https://leetcode.com/discuss/interview-experience/7278246"),
           ("LeetCode: Swiggy SDE-1 backend, Bangalore, Dec 2025", "https://leetcode.com/discuss/interview-experience/7424272"),
           ("LeetCode: Swiggy SDE-1 (Android), machine coding", "https://leetcode.com/discuss/interview-experience/6783426")],
  rel=["lld", "solid", "oop"]),
 dict(id="co-zomato", title="Zomato / Eternal (SDE-1)", lvl=3,
  why="Zomato's parent is now called Eternal (Gurugram). Reports for 2025 freshers describe a selective process: DSA rounds and a culture-fit round.",
  process=["Usually two technical rounds with one or two DSA problems each, then a managerial or culture-fit round; some reports add an online assessment first.",
           "Reported technical content: DSA (for example minimum swaps to sort), designing an LRU cache, resume deep dives, CS fundamentals.",
           "The culture round focuses on motivation, mindset and why Zomato."],
  prep=["DSA mocks and OA sets", "LRU cache from the LLD pack and Worked Solutions", "Story bank: prepare 'why this company' with specifics"],
  pit=["A generic answer to 'why Zomato?'", "Not knowing the LRU cache cold"],
  ask=["Minimum swaps to sort an array", "Design an LRU cache", "Why do you want to join us?"],
  sources=[("LeetCode: Zomato 2025 grad off-campus SDE-1", "https://leetcode.com/discuss/post/6997937/zomato-2025-grad-offcampus-sde-1-intervi-g3sm/"),
           ("LeetCode: Zomato SDE off-campus 2025", "https://leetcode.com/discuss/post/6493240/zomato-interview-experience-sde-off-campus-2025"),
           ("LeetCode: Zomato (Eternal) SDE, Gurugram, Aug 2025 [offer]", "https://leetcode.com/discuss/interview-experience/7206483"),
           ("Jointaro: Zomato SDE-1 India, May 2025", "https://www.jointaro.com/interviews/companies/zomato/experiences/sde-1-india-may-1-2025-no-offer-positive-91a55560/")],
  rel=["p-lru", "trees", "star"]),
 dict(id="co-cred", title="CRED (backend engineer / SDE-1)", lvl=3,
  why="Fintech in Bengaluru known for a long machine-coding round. Fresher entry is often through internships; reports for fresher full-time roles are few.",
  process=["Machine coding: a timed in-memory build, reported at 2 to 2.5 hours, judged on clean state handling, structure and tests.",
           "Reported tasks include a payment-instrument recommender, metrics over a timestamp range, and an in-memory contact directory.",
           "Other rounds: DSA and backend fundamentals (databases, APIs, concurrency such as optimistic vs pessimistic locking)."],
  prep=["Backend starter: layering, validation and tests", "LLD pack under a 2-hour timer", "DBMS one-pager: transactions, isolation, locking"],
  pit=["No tests in the machine-coding submission", "Global mutable state instead of clear classes"],
  ask=["Build an in-memory service with clear interfaces and tests", "Optimistic vs pessimistic locking", "A sliding or rolling-window calculation"],
  sources=[("LeetCode: CRED SDE-1 interview experience (Dec 2025)", "https://leetcode.com/discuss/interview-experience/7415867"),
           ("TechPrep: CRED interview process", "https://www.techprep.app/blog/cred-interview-process"),
           ("LeetCode: CRED backend engineer, Bengaluru (2021, offer)", "https://leetcode.com/discuss/interview-experience/1627624/cred-backend-engineer-bengaluru-dec-2021-offer"),
           ("Glassdoor: CRED interview review", "https://www.glassdoor.com/Interview/CRED-Interview-E3050300-RVW51242161.htm")],
  rel=["lld", "acid", "sliding-window"]),
 dict(id="co-crowdstrike", title="CrowdStrike (security company, early career)", lvl=3,
  why="Endpoint-security company with teams in Pune and Bengaluru; a strong match for a security profile. Public reports for new-grad roles in India are scarce, so treat this page as a starting point.",
  process=["An April 2025 India report for the sensor team describes an online round of 3 DSA problems, after which only the top few candidates moved to interviews.",
           "Earlier early-career reports mention a HackerRank screen, a recruiter call and a technical discussion.",
           "Most 2025 India reports are for experienced roles and describe a selective process."],
  prep=["OA sets under strict timing (ranking cut-offs)", "C++ depth and OS one-pager: endpoint agents are systems software", "Security lab notebook and TenantWall for security conversations"],
  pit=["Treating a ranked OA like a pass/fail one: every solved problem counts", "No systems knowledge (processes, memory, syscalls)"],
  ask=["Three DSA problems in an online round", "How an operating system isolates processes", "Tell me about a security project"],
  sources=[("Jointaro: CrowdStrike engineering sensor team, India, April 2025", "https://www.jointaro.com/interviews/companies/crowdstrike/experiences/engineering-sensor-team-india-april-1-2025-no-offer-positive-c55ab864"),
           ("Jointaro: CrowdStrike software engineering internship, India, 2023", "https://www.jointaro.com/interviews/companies/crowdstrike/experiences/software-engineerinternship-india-april-1-2023-no-offer-positive-8cb9b6db/"),
           ("Jointaro: CrowdStrike SDET, India, 2024", "https://www.jointaro.com/interviews/companies/crowdstrike/experiences/software-development-engineer-in-test-sdet-india-april-1-2024-no-offer-positive-fbad570a")],
  rel=["process-thread", "binary-exploitation", "oa-tactics"]),
]
def body(pages):
    pg = lambda k: str(pages.get(k, "000")) if pages else "000"
    rows = "".join(f'<tr><td><a href="#{c["id"]}">{E(c["title"])}</a><div class="f">{E(c["why"])}</div></td><td class="pg"><a href="#{c["id"]}">{pg(c["id"])}</a></td></tr>' for c in CO)
    out = [f'''<section class="cover"><p class="eb">COMPANIES · FILES III</p><h1>Company files<br><span>part III</span></h1>
<p class="lead">Oracle, Cisco, Swiggy, Zomato (Eternal), CRED and CrowdStrike, in the same format as the earlier company files: what candidates report about the process, how your plan prepares you, common mistakes, likely questions and the sources. CrowdStrike has few public new-grad reports for India; its page says so.</p>
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
    (SRC / "co3.html").write_text(f'<!doctype html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700&family=Inter:wght@400;600&family=JetBrains+Mono:wght@600&display=swap" rel="stylesheet"><style>{CSS}</style></head><body><div id="top"></div>{body(pages)}</body></html>')
    js.write_text("const { chromium } = require('playwright'); (async () => { const b = await chromium.launch(); const p = await b.newPage(); await p.goto('file://' + __dirname + '/co3.html', { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready); await p.pdf({ path: __dirname + '/" + name + "', format: 'A4', printBackground: true, preferCSSPageSize: true }); await b.close(); })();")
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
    w.add_metadata({"/Title": "Company files III"}); w.write(str(OUT / "company-files-3.pdf"))
    for f in ("p1.pdf", "p2.pdf", "r.js", "co3.html"): (SRC / f).unlink()
    print(NP, "pages", d2)
