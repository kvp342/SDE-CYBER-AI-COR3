"""Final plan: one short document that ties the whole kit together, from Nov 2026 to placements.
Run from the repo root: python3 generated/src/final_plan.py"""
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

# ------------------------------------------------------------------ 1
sec("rules", "Read this first: the seven rules", UL([
 "<b>One plan, one tracker.</b> The plan is the Playbook (" + K("playbook.html") + "). Log every problem and topic in your revision tracker. If it is not logged, it did not happen.",
 "<b>Depth over count.</b> Seniors' advice converges on about 250–300 well-chosen problems with patterns understood, not 1,000 rushed ones." + S("https://sirjohnnymai.com/blog/visa-intern-sde-2026/", "Visa SDE intern guide 2026 (blog): ~300 well-chosen problems beat 1,000") + S("https://leetcode.com/discuss/post/8297681/", "LeetCode Discuss: Surviving a Tier 3 college, off-campus strategy") + " Your plan already covers this through Striver A2Z plus the 123 worked solutions in this kit.",
 "<b>Stuck rule.</b> Think for 25 minutes (15 for easy, 40 for hard). Then read the solution, close it, write it yourself, and schedule redos at 1, 3, 7 and 21 days.",
 "<b>Be ready before you ask.</b> A referral only gets you the interview; you still have to pass it." + S("https://www.teamblind.com/post/internship-referrals-m4srdvdu", "Blind thread: internship referrals (be LeetCode-ready first)") + " Ask for referrals once you can solve most mediums in 30 minutes.",
 "<b>Apply early.</b> Internship applications often open 6–8 months before the start date." + S("https://thenewviews.com/sde-internships/", "15+ Top SDE Internships 2026 (apply 6–8 months early)") + " Section 4 lists the windows.",
 "<b>Proof beats claims.</b> Two deployed projects, a GitHub with tests and CI, and write-ups of your security labs. Your resume should point to things a recruiter can open.",
 "<b>Weekly review, every Sunday.</b> 30 minutes: what slipped, what to cut, next week's three priorities (" + K("generated/weekly-planner.pdf") + ")."]) +
 '<p class="note">This plan is short on purpose. Each line points to the file in the kit that has the detail. Dates for outside programmes come from the sources listed at the end; always confirm on the official page before applying.</p>')

# ------------------------------------------------------------------ 2
sec("phases", "The plan on one page", T(["When", "Phase", "Goal", "Open"], [
 ["16–17 Nov 2026", "C++ refresh", "STL fluency, no compile errors", K("generated/patterns-stl-card.pdf")],
 ["18 Nov 2026", "TenantWall finish + show", "Run the 14 tests yourself, screenshots, Policy Generator, diagrams; evening C++/STL skim", K("generated/tenantwall-explained.pdf")],
 ["19 Nov 2026", "Cloud course day", "About 10 h: plan weeks 0–4 (setup, IAM, compute, networking, S3); 1 h DSA", K("generated/cloud-architect-2h-plan.pdf")],
 ["20 Nov 2026 – 25 Feb 2027", "Cloud course, 1 h a day", "Each plan week takes two calendar weeks (dates in the cloud plan)", K("generated/cloud-architect-2h-plan.pdf")],
 ["Saturdays, 21 Nov – 30 Jan", "Cyber, 2 h", "One security lab or a PortSwigger Web Security Academy topic", K("generated/security-labs-workbook.pdf")],
 ["From 1 Feb 2027", "Cyber, 1–1.5 h a day", "Labs, SOC log analyser project, TenantWall paper; read OWASP Top 10 for LLM apps, one item a week", K("generated/soc-log-analysis-project.pdf")],
 ["20 Nov 2026 – 30 Jan 2027", "Striver A2Z core", "Classic 18-step sheet on " + L("https://codolio.com/question-tracker/sheet/strivers-a2z-dsa-sheet", "Codolio") + " (tick each problem; link LeetCode and Codeforces), 5–6 problems a day + 1–2 LeetCode problems on the same topic; LeetCode contests from December", K("Striver-A2Z-DSA-Sheet-Classic.pdf") + ", " + K("generated/worked-solutions-2.pdf")],
 ["Daily, from 20 Nov", "Core CS + flashcards", "1 hour Core CS, 15–20 min Anki", K("generated/core-cs-one-pagers.pdf") + ", " + K("generated/anki/", "anki decks")],
 ["8 Feb – 19 May 2027", "Hard pass + Codeforces", "Hard problems, OA sets, Codeforces 1400 by 31 Mar", K("generated/worked-solutions-3.pdf") + ", " + K("generated/oa-simulation-packs.pdf") + ", " + K("generated/codeforces-ladder.pdf")],
 ["Feb – Mar 2027", "Internship applications", "Resume final, profiles live, apply and ask for referrals", K("generated/resume-kit.pdf") + ", " + K("generated/profile-kit.pdf")],
 ["By 21 Mar 2027", "TenantWall paper", "Submit the research paper", K("generated/tenantwall-paper-outline.pdf")],
 ["22 Mar – 7 Apr 2027", "Exams", "Pause new material; Anki only", K("generated/anki-decks-guide.pdf")],
 ["31 Mar 2027", "Checkpoint", "Elite (HFT) track only if the gate is passed", K("generated/elite-track-pack.pdf")],
 ["March 2027, or week of 19 Apr", "AWS SAA-C03 exam", "Book for early March (before college exams) once two practice sets score 80%+; otherwise the week of 19 April", K("generated/aws-saa-c03-study-pack.pdf")],
 ["May 2027", "AI-security project (or internship)", "A deployed, tested project; if you land a summer internship, it replaces this", K("generated/ai-security-starter-guide.pdf")],
 ["31 May – 31 Jul 2027", "Placement sprint", "Mocks, company files, LLD and system design, OA sets", K("generated/mock-interview-scripts.pdf") + ", " + K("generated/company-files-2.pdf")],
 ["Aug – Dec 2027", "Placements", "OAs and interviews; 6-month internship and full-time offers", K("generated/interview-day-kit.pdf")],
]))

# ------------------------------------------------------------------ 3
sec("months", "Month by month: what to do and what to finish", T(["Month", "Do", "Finish by month end"], [
 ["Nov 2026", "A2Z steps 1–3 (about). Set up the tracker and Anki. Apply to the Science Academies research fellowship (SRFP) if research interests you: closes 30 Nov 2026." + S("https://www.ias.ac.in/public/Resources/News/SRFP2027_Announcement.pdf", "Indian Academy of Sciences: SRFP 2027 announcement"), "Arrays, hashing, sorting, binary search basics"],
 ["Dec 2026", "A2Z steps 4–9 (binary search, strings, linked list, recursion). Resume v1 from the resume kit.", "Resume v1; about 200+ problems logged (5–6 a day since 20 Nov)"],
 ["Jan 2027", "A2Z steps 10–18 (stack, heap, greedy, trees, graphs, DP). Pick open-source orgs for GSoC or LFX and make 2–3 small contributions (see the open-source guide).", "A2Z core done (30 Jan); GitHub profile clean"],
 ["Feb 2027", "Hard pass begins. Codeforces ladder. OA sets 1–4 on Saturdays. Write the TenantWall paper. Watch for GSoC orgs (mid-Feb) and IIT summer research calls." + S("https://developers.google.com/open-source/gsoc/timeline", "Google Summer of Code timeline (official)") + S("https://nm7.si/blog/research-internships-at-iits-for-ug-students", "Research internships at IITs for UG students (dates roundup)"), "Applications sent; 2 mocks done"],
 ["Mar 2027", "Internship season. Apply daily (Section 8). GSoC proposal in the contributor window (2026's was 16–31 Mar). Codeforces 1400 gate on 31 Mar. Paper by 21 Mar.", "Paper submitted; gate result known"],
 ["Apr 2027", "Exams until 7 Apr, then AWS final revision; exam in the week of 19 Apr. Keep applying.", "AWS SAA-C03 passed"],
 ["May 2027", "Internship, or the AI-security project. Keep 1 hour of DSA a day either way.", "Project deployed with tests, or internship started"],
 ["Jun–Jul 2027", "Placement sprint: 2 mocks a week, LLD, system design, company files, OA sets 9–16. Watch for Flipkart GRiD and other hiring challenges (2026 registration closed in July)." + S("https://www.talentd.in/articles/flipkart-grid-8-0-internships-sde-roles", "Flipkart GRiD guide: internships and SDE roles"), "Resume v3; 10+ mocks scored"],
 ["Aug–Dec 2027", "Placements. Apply to big-tech new-grad and 6-month intern roles as they open. OA sets 17–24 every Saturday from 17 Jul to 4 Sep. Use the interview day kit every time.", "Offer"],
 ["Jan–Jun 2028", "6-month internship or final semester. Convert the internship into a pre-placement offer (PPO).", "PPO or full-time role"],
]))

# ------------------------------------------------------------------ 4
sec("windows", "Opportunity windows (confirm each on the official page)", T(["Programme", "Usual window", "Why it matters", "Status (17 Nov 2026)"], [
 ["Science Academies SRFP (IASc, INSA, NASI)", "Sep – 30 Nov", "Funded 2-month research stay in 2027", "Open until 30 Nov 2026" + S("https://www.ias.ac.in/public/Resources/News/SRFP2027_Announcement.pdf", "Indian Academy of Sciences: SRFP 2027 announcement")],
 ["Google Summer of Code", "Orgs announced mid-Feb; contributor applications in March", "Paid open-source work, strong on a resume", "2027 dates not out yet" + S("https://developers.google.com/open-source/gsoc/timeline", "Google Summer of Code timeline (official)")],
 ["LFX Mentorship (Linux Foundation)", "Spring term runs 1 Mar – 31 May; mentee applications for about 4 weeks before", "Paid mentorship on CNCF and other projects", "Watch LFX from January" + S("https://docs.linuxfoundation.org/lfx/mentorship/mentorship-program-timelines", "LFX Mentorship programme timelines (official)")],
 ["IIT summer research (SURGE, SFP, SURE, SRIP)", "Feb – Mar", "Research experience, letters of recommendation", "2027 calls not out yet" + S("https://nm7.si/blog/research-internships-at-iits-for-ug-students", "Research internships at IITs for UG students (dates roundup)")],
 ["Off-campus summer internships", "Big tech often opens mid-year for the next summer; others year-round", "The main route if your campus has few drives", "Example: Salesforce Summer 2027 SWE intern was open in India" + S("https://www.sightsinplus.com/news/internship/salesforce-summer-2027-software-engineer-internship-applications-open-in-india/", "Salesforce Summer 2027 SWE internship, India")],
 ["Hiring challenges (Flipkart GRiD, Amazon HackOn, TCS CodeVita)", "Usually mid-year", "Interview shortlists and PPO routes", "Next cycles not announced" + S("https://www.talentd.in/articles/flipkart-grid-8-0-internships-sde-roles", "Flipkart GRiD guide: internships and SDE roles") + S("https://velonx.in/blog/top-company-hackathons-for-students-in-india-in-2026", "Top company hackathons for students in India 2026")],
 ["CERT-In work-based learning", "Periodic", "Government cyber security experience", "Check wblp.in and cert-in.org.in" + S("https://en.wikipedia.org/wiki/Indian_Computer_Emergency_Response_Team", "CERT-In (overview)")],
]) + '<p class="note">Note: Google STEP is aimed at first- and second-year students, so it is unlikely to fit your year; check its page if unsure. Dates above are from the 2026 cycle unless marked; they shift a little every year.</p>')

# ------------------------------------------------------------------ 5
sec("daily", "The daily and weekly system", T(["Block", "Time", "What", "Open"], [
 ["Warm-up", "15–20 min", "Anki reviews (all decks)", K("generated/anki-decks-guide.pdf")],
 ["DSA", "3–4 h", "5–6 new problems in sheet order, plus the day's redos (1-3-7-21)", K("generated/patterns-stl-card.pdf")],
 ["Core CS", "1 h", "One topic: read the one-pager, answer 10 MCQs, explain it aloud", K("generated/core-cs-mcq-bank.pdf")],
 ["Track work", "1 h cloud (to 25 Feb); from Feb also 1–1.5 h cyber", "Cloud course 1 h a day (" + K("generated/cloud-architect-2h-plan.pdf", "plan") + "); Saturday 2 h cyber until A2Z is done, then cyber daily; AI-security project in May", K("generated/security-lab-notebook.pdf")],
 ["Log", "10 min", "Tracker, plus one Anki card for every problem you got wrong", K("generated/weekly-planner.pdf")],
]) + "<h3>Every week</h3>" + UL([
 "<b>Saturday:</b> one OA set under exam conditions (90 minutes), from the date the set lists. Score it the same day.",
 "<b>Sunday:</b> the week's 30-minute self-test (" + K("generated/weekly-revision-tests.pdf") + "), then weekly review (30 min), redo the week's failed problems, plan next week.",
 "<b>From Feb:</b> one Codeforces contest a week. <b>From Mar:</b> one mock interview a week; two a week from 31 May.",
 "<b>Rest:</b> one half-day off a week. Burnout costs more days than it saves (a senior's warning in your own plan)."]))

# ------------------------------------------------------------------ 6
sec("targets", "Checkpoints: numbers to hit", T(["By", "DSA", "Other", "If behind"], [
 ["31 Dec 2026", "200+ problems logged", "Resume v1; Anki daily streak", "Cut new problems to 4/day; keep redos"],
 ["30 Jan 2027", "A2Z core sheet done", "GitHub clean, 1 project live", "Skip optional A2Z problems; do the must-do list"],
 ["31 Mar 2027", "Codeforces 1400; 80% of OA sets 1–4 solved in time", "Paper submitted; applications out", "Elite track stays closed; focus on SDE"],
 ["30 Apr 2027", "Worked Solutions II and III done", "AWS SAA-C03 passed", "Move AWS out by 4 weeks, not DSA"],
 ["31 Jul 2027", "All 123 kit solutions redone without help; mocks at 17+/20", "2 deployed projects; resume v3", "Extra mocks with the scripts; fix the lowest rubric line"],
]) + '<p class="note">These are rules of thumb from seniors and guides, not company requirements. Common figures: 250+ problems and 2 deployed projects before the application push; 50+ TryHackMe rooms for security roles.' + S("https://leetcode.com/discuss/post/8297681/", "LeetCode Discuss: Surviving a Tier 3 college, off-campus strategy") + S("https://tutorsbot.com/blog/cyber-security-internship-2026-india-guide", "Cyber security internship 2026 India guide (portfolio figures)") + '</p>')

# ------------------------------------------------------------------ 7
sec("resources", "Resources seniors actually used (filtered)", "<p>Use the first column. Add the second only if you have time. The third wastes time for your goal.</p>" + T(["Area", "Use", "Optional", "Skip"], [
 ["DSA", L("https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2", "Striver A2Z") + " (your plan), LeetCode, the kit's 123 worked solutions" + S("https://aditiiprasad.medium.com/google-swe-intern-2026-interview-experience-off-campus-30809a111142", "Google SWE Intern 2026 interview experience (off campus)"), L("https://neetcode.io/practice", "NeetCode 150") + " for pattern revision; " + L("https://cses.fi/problemset/", "CSES") + " for hard practice", "A second full sheet; 1,000-problem counts"],
 ["Contests", L("https://codeforces.com/", "Codeforces") + " Div 2/3, the kit's ladder", "LeetCode weekly contests", "Grinding ratings past 1600 unless on the Elite track"],
 ["Core CS", "The kit's one-pagers and MCQ bank; " + L("https://pages.cs.wisc.edu/~remzi/OSTEP/", "OSTEP (free OS book)"), L("https://leetcode.com/studyplan/top-sql-50/", "LeetCode SQL 50"), "Full university-length courses before placements"],
 ["Design", "The kit's LLD pack and case studies; " + L("https://github.com/donnemartin/system-design-primer", "System Design Primer"), "Alex Xu's System Design Interview (book)", "Deep distributed-systems theory for intern roles"],
 ["Security", L("https://tryhackme.com/", "TryHackMe") + ", " + L("https://portswigger.net/web-security", "PortSwigger Web Security Academy") + ", " + L("https://overthewire.org/wargames/bandit/", "OverTheWire Bandit") + S("https://github.com/hossainabir1/tryhackme-roadmap-free-vs-premium", "TryHackMe learning path 2026 (free vs premium)"), L("https://www.hackthebox.com/", "Hack The Box") + ", " + L("https://picoctf.org/", "picoCTF") + ", " + L("https://ctftime.org/", "CTFtime"), "Paid bootcamps that promise placement"],
 ["Cloud", "The kit's AWS pack; " + L("https://skillbuilder.aws/", "AWS Skill Builder") + " (free tier)", "One paid SAA-C03 video course", "A second cloud certificate before placements"],
 ["Resume", L("https://www.overleaf.com/latex/templates/jakes-resume-anonymous/cstpnrbkhndn", "Jake's resume (Overleaf)") + ", one page, single column" + S("https://www.overleaf.com/latex/templates/jakes-resume-anonymous/cstpnrbkhndn", "Jake's Resume (Anonymous), Overleaf template"), "The kit's resume kit for bullet wording", "Two-column or graphic templates (ATS parsing problems)"],
]))

# ------------------------------------------------------------------ 8
sec("hunt", "The internship hunt playbook", "<h3>Channels, in order of payoff</h3>" + T(["Channel", "How", "Kit"], [
 ["Campus drives", "Register for every eligible drive; read the company file before each test", K("generated/company-files-3.pdf")],
 ["Referrals", "Find engineers (alumni first) at the company on LinkedIn; one short message with your resume link, a deployed project and your LeetCode or Codeforces handle" + S("https://leetcode.com/discuss/post/8297681/", "LeetCode Discuss: Surviving a Tier 3 college, off-campus strategy"), K("generated/interview-day-kit.pdf", "referral template (interview day kit)")],
 ["Apply first, then ask", "Apply on the careers page, then ask for a referral with the job ID; one off-campus Google intern did exactly this" + S("https://aditiiprasad.medium.com/google-swe-intern-2026-interview-experience-off-campus-30809a111142", "Google SWE Intern 2026 interview experience (off campus)"), K("generated/profile-kit.pdf")],
 ["Job boards and trackers", "LinkedIn jobs, company career pages, Internshala, Wellfound, GitHub trackers for 2027 internships" + S("https://github.com/Jayagna/internship-radar-2027", "Internship radar 2027 (GitHub tracker, India-eligible roles)"), K("generated/resume-kit.pdf")],
 ["Open source and research", "GSoC, LFX, IIT summer research, SRFP (Section 4)", K("generated/tenantwall-paper-outline.pdf")],
 ["Hiring challenges", "GRiD, HackOn, CodeVita: treat them as OA practice that can shortlist you", K("generated/oa-simulation-packs-2.pdf")],
]) + "<h3>The loop, every week from February</h3>" + UL([
 "Keep a sheet: company, role, link, date applied, referral asked (who), status, next action.",
 "Ten tailored applications and five referral messages a week. Tailor the top three resume bullets to the job's keywords.",
 "Follow up once after 7 days. Never send the same message twice to one person.",
 "After every OA or interview, write down every question within an hour and add the hard ones to Anki."]))

# ------------------------------------------------------------------ 9
sec("security", "The security and cloud track (your edge)", UL([
 "<b>Your story:</b> an SDE who understands security and cloud, with TenantWall as proof. Every interview gets the two-minute TenantWall pitch (" + K("generated/mock-interview-scripts-2.pdf", "grilling script") + ").",
 "<b>Labs, in order:</b> Bandit (Linux), TryHackMe beginner and SOC paths, PortSwigger SQL injection and XSS, then Hack The Box. Write up each lab in your notebook; publish clean versions on GitHub." + S("https://github.com/hossainabir1/tryhackme-roadmap-free-vs-premium", "TryHackMe learning path 2026 (free vs premium)") + " (" + K("generated/owasp-portswigger-lab-map.pdf") + ")",
 "<b>A home lab for SOC roles:</b> collect logs from your own virtual machines and practise spotting failed logins, new services and odd processes; list it on the resume." + S("https://www.networkershome.com/how-to-become-a-soc-analyst-india/", "How to become a SOC analyst in India 2026"),
 "<b>Certificates:</b> AWS SAA-C03 is in the plan. Security+ or the Google Cybersecurity Certificate are optional extras; do not take them before placements unless a target role asks." + S("https://tutorsbot.com/blog/cyber-security-internship-2026-india-guide", "Cyber security internship 2026 India guide (portfolio figures)"),
 "<b>Ethics:</b> only test systems you own or platforms that invite it. One unauthorised scan can end a security career before it starts."]))

# ------------------------------------------------------------------ 10
sec("process", "How the hiring process runs, and what to open", T(["Stage", "What happens", "How to win", "Open"], [
 ["Resume screen", "Seconds per resume; ATS keyword match", "One page, numbers in every bullet, links that work", K("generated/resume-kit.pdf")],
 ["Online assessment", "2–3 problems in 60–90 min, sometimes MCQs and aptitude", "Timed practice on Saturdays; read all problems first", K("generated/oa-simulation-packs.pdf") + ", " + K("generated/aptitude-pack.pdf")],
 ["Technical rounds", "1–3 rounds of DSA, sometimes Core CS, LLD or projects", "Talk while you think; state brute force, then improve; test with an example", K("generated/mock-interview-scripts.pdf")],
 ["Core CS / design", "OS, DBMS, CN, OOP, SQL; light design for interns", "Answer in three levels: definition, example, trade-off", K("generated/core-cs-one-pagers.pdf") + ", " + K("generated/lld-pack.pdf")],
 ["HR / behavioural", "Why us, conflicts, failures, projects", "STAR stories prepared in advance; honest numbers", K("generated/interview-story-bank.pdf")],
 ["Offer", "Compare base, bonus, stock, bond, location", "Use the comparison sheet; ask for the offer in writing", K("generated/interview-day/", "interview day files")],
]))

# ------------------------------------------------------------------ 11
sec("mistakes", "Mistakes seniors warn about", UL([
 "<b>Too many resources.</b> One sheet, one tracker. Switching sheets resets your progress.",
 "<b>Watching instead of solving.</b> A video counts only after you code the problem yourself the next day.",
 "<b>No timed practice.</b> Untimed practice does not prepare you for a 90-minute OA.",
 "<b>Asking for referrals too early.</b> Get ready first; you get one first impression per person." + S("https://www.teamblind.com/post/internship-referrals-m4srdvdu", "Blind thread: internship referrals (be LeetCode-ready first)"),
 "<b>Fancy resumes.</b> Graphics and columns break ATS parsing; exaggerated numbers break interviews." + S("https://jobrise.io/blog/one-page-resume-guide-india", "One page resume guide for freshers (India)"),
 "<b>Applying late.</b> Many roles fill early; start in February at the latest.",
 "<b>Skipping Core CS.</b> Many technical rounds include OS, DBMS and networks questions; one hour a day is enough.",
 "<b>Projects with no proof.</b> No deployment, no tests, no README means the project is invisible.",
 "<b>Comparing yourself on LinkedIn.</b> Compare with your own tracker from last month."]))

# ------------------------------------------------------------------ 12
KITMAP = [
 ("Planning", [("Daily DSA order", "Striver-A2Z-DSA-Sheet-Classic.pdf"), ("Week plan and Sunday review", "generated/weekly-planner.pdf"), ("Sunday 30-minute self-test", "generated/weekly-revision-tests.pdf"), ("Everything on one page", "generated/one-page-overview.pdf"), ("Find any file", "generated/index-of-everything.pdf"), ("Look up any topic", "generated/knowledge-base-v2.html")]),
 ("DSA and OAs", [("Pattern you cannot recognise", "generated/patterns-stl-card.pdf"), ("Worked problems, set II", "generated/worked-solutions-2.pdf"), ("Worked problems, set III", "generated/worked-solutions-3.pdf"), ("Hard problems for final rounds", "generated/worked-solutions-4.pdf"), ("Saturday OA, sets 1–8", "generated/oa-simulation-packs.pdf"), ("Saturday OA, sets 9–16", "generated/oa-simulation-packs-2.pdf"), ("Saturday OA, sets 17–24 (placement season)", "generated/oa-simulation-packs-3.pdf"), ("Codeforces 1400 gate", "generated/codeforces-ladder.pdf"), ("Aptitude rounds", "generated/aptitude-pack.pdf"), ("More aptitude and data interpretation", "generated/aptitude-pack-2.pdf")]),
 ("Core CS and design", [("Night before a Core CS round", "generated/core-cs-one-pagers.pdf"), ("MCQ rounds", "generated/core-cs-mcq-bank.pdf"), ("More MCQs and numericals", "generated/core-cs-mcq-bank-2.pdf"), ("SQL questions", "generated/sql-pack.pdf"), ("Harder SQL (analytics, recursion)", "generated/sql-pack-2.pdf"), ("LLD round", "generated/lld-pack.pdf"), ("More LLD designs", "generated/lld-pack-2.pdf"), ("ATM, machine coding, segment trees, Instagram", "generated/gap-fill-pack.pdf"), ("System design", "generated/system-design-case-studies.pdf"), ("More system design", "generated/system-design-case-studies-2.pdf"), ("Linux, Git, gdb", "generated/linux-git-debugging-sheet.pdf")]),
 ("Security, cloud, research", [("AWS exam", "generated/aws-saa-c03-study-pack.pdf"), ("AWS hands-on labs", "generated/aws-lab-workbook.pdf"), ("Web security labs", "generated/owasp-portswigger-lab-map.pdf"), ("Lab write-ups", "generated/security-lab-notebook.pdf"), ("Hands-on security labs", "generated/security-labs-workbook.pdf"), ("SOC portfolio project", "generated/soc-log-analysis-project.pdf"), ("Security interview questions", "generated/cyber-security-interview-bank.pdf"), ("TenantWall build", "generated/tenantwall-helpers.pdf"), ("TenantWall paper", "generated/tenantwall-paper-outline.pdf"), ("TenantWall changes in one day", "generated/tenantwall-one-day-runbook.pdf"), ("TenantWall explained", "generated/tenantwall-explained.pdf"), ("Solutions Architect plan", "generated/cloud-architect-2h-plan.pdf"), ("What to do each week", "generated/weekly-schedule.pdf")]),
 ("Projects", [("Backend project", "generated/backend-starter/"), ("AI-security project", "generated/ai-security-starter-guide.pdf"), ("Docker and CI", "generated/docker-ci-guide.pdf"), ("Open source, GSoC and LFX", "generated/open-source-gsoc-guide.pdf"), ("C++ networking project", "generated/network-programming-project.pdf")]),
 ("Applying and interviews", [("Resume", "generated/resume-kit.pdf"), ("LinkedIn and GitHub", "generated/profile-kit.pdf"), ("Behavioural stories", "generated/interview-story-bank.pdf"), ("Before a company's test", "generated/company-files-3.pdf"), ("Practice with a friend", "generated/mock-interview-scripts-2.pdf"), ("OA or interview day", "generated/interview-day-kit.pdf"), ("Tracking applications and outreach", "generated/applications-outreach-kit.pdf"), ("Daily revision", "generated/anki-decks-guide.pdf")]),
]
sec("kitmap", "When you need X, open Y", "".join(f"<h3>{E(g)}</h3>" + T(["When", "Open"], [[E(w), K(p)] for w, p in items], "km") for g, items in KITMAP))

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
    out = [f'''<section><p class="eb">FINAL PLAN · NOV 2026 TO PLACEMENTS</p><h1>Your final plan<br><span>to internships and placements</span></h1>
<p class="lead">Internships from March 2027, placements from August 2027. This is the plan, the rules, the deadlines and the targets on a few pages, filtered from what seniors and guides recommend and tied to the files in this kit. Read Section 1 now, Section 2 every month, and Section 12 whenever you are unsure what to open.</p>
<table class="ix"><thead><tr><th>Section</th><th class="pg">Page</th></tr></thead><tbody>{ix}</tbody></table>
<p class="note">Today's action: if research appeals to you, the Science Academies summer research fellowship (SRFP) closes on 30 November 2026 (Section 4). TenantWall is finished and shown on 18 November, the cloud course starts on 19 November, and Striver A2Z starts on 20 November.</p></section>''']
    for n, (i, t, b) in enumerate(SEC):
        out.append(f'<section class="sec" id="{i}"><h2><span class="num">{n + 1:02d}</span>{E(t)}<a class="back" href="#top">↑ Index</a></h2>{b}</section>')
    out.append('<section class="sec" id="src"><h2><span class="num">··</span>Sources<a class="back" href="#top">↑ Index</a></h2><p>Checked on 17 Nov 2026. Blogs and forum posts are single opinions; official pages win when they disagree. Numbers marked as rules of thumb are not company requirements.</p><ol class="src">'
               + "".join(f'<li><a href="{u}">{E(l)}</a><br>{E(u)}</li>' for u, l in SOURCES) + "</ol></section>")
    return "".join(out)
js = SRC / "rb.js"
def render(pages, name):
    (SRC / "final_plan.html").write_text(f'<!doctype html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700&family=Inter:wght@400;600&family=JetBrains+Mono:wght@600&display=swap" rel="stylesheet"><style>{CSS}</style></head><body><div id="top"></div>{body(pages)}</body></html>')
    js.write_text("const { chromium } = require('playwright'); (async () => { const b = await chromium.launch(); const p = await b.newPage(); await p.goto('file://' + __dirname + '/final_plan.html', { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready); await p.pdf({ path: __dirname + '/" + name + "', format: 'A4', printBackground: true, preferCSSPageSize: true }); await b.close(); })();")
    subprocess.run(["node", str(js)], check=True)
    r = PdfReader(str(SRC / name)); return {k.lstrip("/"): r.get_destination_page_number(v) + 1 for k, v in r.named_destinations.items()}, len(r.pages)
d1, n1 = render(None, "b1.pdf"); d2, n2 = render(d1, "b2.pdf"); assert n1 == n2 and all(d1[i] == d2[i] for i, _, _ in SEC)
w = PdfWriter(clone_from=PdfReader(str(SRC / "b2.pdf"))); w.add_outline_item("Index", 0, fit=Fit.fit())
for n, (i, t, _) in enumerate(SEC): w.add_outline_item(f"{n + 1}. {t}", d2[i] - 1, fit=Fit.fit())
w.add_outline_item("Sources", d2["src"] - 1, fit=Fit.fit())
NP = len(w.pages)
for k, pg in enumerate(w.pages):
    if k == 0: continue
    buf = io.BytesIO(); cv = canvas.Canvas(buf, pagesize=(float(pg.mediabox.width), float(pg.mediabox.height))); cv.setFont("Helvetica", 7.5); cv.setFillGray(.55)
    cv.drawRightString(float(pg.mediabox.width) - 26, 14, f"{k + 1} / {NP}"); cv.save(); buf.seek(0); pg.merge_page(PdfReader(buf).pages[0]); pg.compress_content_streams(level=9)
w.add_metadata({"/Title": "Final plan"}); w.write(str(OUT / "final-plan.pdf"))
for f in ("b1.pdf", "b2.pdf", "rb.js", "final_plan.html"): (SRC / f).unlink()
print(NP, "pages;", len(USED), "kit links;", len(SOURCES), "sources;", d2)
