"""Placement Field Guide: a print-designed HTML rendered to PDF with Playwright."""
import html, pathlib
E = lambda s: html.escape(s, quote=True)
OUT = pathlib.Path(__file__).parent

LV = {  # level: (name, colour, tag)
    0: ("Foundation", "#16a34a", "L0"),
    1: ("Core", "#0891b2", "L1"),
    2: ("Interview-ready", "#2563eb", "L2"),
    3: ("Advanced", "#7c3aed", "L3"),
    4: ("Elite", "#c2410c", "L4"),
}
def chip(l): n, c, t = LV[l]; return f'<span class="chip" style="--k:{c}">{t} · {n}</span>'
def a(url, text=None): return f'<a href="{E(url)}">{E(text or url)}</a>'

pages = []
def page(cls, body): pages.append(f'<section class="pg {cls}">{body}</section>')

def head(no, eyebrow, title, sub="", col="#c2410c"):
    return (f'<header class="sh" style="--k:{col}"><span class="no">{no}</span><div><p class="eb">{E(eyebrow)}</p>'
            f'<h1>{E(title)}</h1>' + (f'<p class="sub">{E(sub)}</p>' if sub else "") + '</div></header>')

def ladder(rows):
    """rows: (level, title, what, resources, done-when)"""
    out = ['<div class="ladder">']
    for l, t, what, res, done in rows:
        n, c, tag = LV[l]
        out.append(f'<div class="rung" style="--k:{c}"><div class="rt"><b>{tag}</b><span>{E(n)}</span></div>'
                   f'<div class="rb"><h3>{E(t)}</h3><p>{what}</p><p class="res"><b>Use:</b> {res}</p>'
                   f'<p class="dw"><b>Done when:</b> {E(done)}</p></div></div>')
    out.append('</div>')
    return "".join(out)

def table(head_, rows, cls=""):
    h = "".join(f"<th>{x}</th>" for x in head_)
    b = "".join("<tr>" + "".join(f"<td>{x}</td>" for x in r) + "</tr>" for r in rows)
    return f'<table class="{cls}"><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table>'

# ---------------------------------------------------------------- cover
page("cover", f'''
<div class="cv-grid">{''.join(f'<i style="--k:{LV[l][1]};--h:{30+l*14}%"></i>' for l in range(5))}</div>
<p class="cv-eb">FIELD GUIDE · NOV 2026 → JUN 2028</p>
<h1 class="cv-t">Tier-3 to<br><span>Top Offer</span></h1>
<p class="cv-s">The placement field guide for a B.Tech CSE (Cybersecurity) student: DSA, Core CS, system design, security, AWS and AI, sorted into five difficulty levels, with a complete efficiency system (day modes, a 7-step problem routine, revision schedule, AI prompts, OA tactics), an off-campus hiring machine, and 16 real stories from students who did it from tier-3 colleges.</p>
<div class="cv-lv">{''.join(chip(l) for l in range(5))}</div>
<div class="cv-ft"><div><b>Built from</b><span>your Playbook, Roadmap and Cheat Sheet, plus public interview experiences, free courses and hiring pages</span></div>
<div><b>Tap any topic</b><span>Underlined names open an in-depth page in the <a href="https://claude.ai/artifact/McuS723LTAb16Q6SpdUsAT">Placement Knowledge Base</a>: concept, why it matters for you, code, mistakes, interview questions, practice</span></div>
<div><b>Track</b><span>Intensive: Striver core done by 30 Jan 2027 · AWS SAA by April · sprint 31 May–31 Jul · placements Aug–Dec 2027</span></div></div>
''')

# ---------------------------------------------------------------- 00 how to use
page("", head("00", "START HERE", "How this guide works", "Every topic is a ladder. Find your rung, climb one at a time, and stop climbing where the target job stops asking.") + f'''
<div class="lvgrid">
{''.join(f'<div class="lvc" style="--k:{LV[l][1]}"><b>{LV[l][2]}</b><h3>{LV[l][0]}</h3><p>{d}</p></div>' for l, d in [
 (0, "You can't do it yet. Learn the syntax, the idea, the vocabulary. Goal: no blank page."),
 (1, "You can do it with notes. Standard problems, standard questions. Service-company OA level."),
 (2, "You can do it cold, timed, out loud. Product-company interview level (Amazon, Razorpay, Atlassian)."),
 (3, "You can do the twist. Hards, contests, design trade-offs. Google, Microsoft, D. E. Shaw level."),
 (4, "You do what few freshers do. CP rating 1900+, CVEs, open source, HFT puzzles. The outlier offers."),
])}
</div>
<h2>Which level each target needs</h2>
{table(["Target", "DSA", "Core CS", "Design", "Security", "Cloud/AI"], [
 ["Mass recruiters (TCS Digital, Infosys SP, Accenture)", chip(1), chip(1), "—", "—", "—"],
 ["Product mid-tier (Razorpay, Zomato, Agoda, Myntra)", chip(2), chip(2), chip(1)+" LLD", "—", chip(1)],
 ["Big Tech (Amazon, Microsoft, Google, Atlassian)", chip(3), chip(2), chip(2), "—", chip(1)],
 ["Security roles (AppSec, cloud security, SOC+)", chip(2), chip(2), chip(1), chip(3), chip(2)+" AWS"],
 ["Elite: HFT / quant dev (only through the 31 Mar gate)", chip(4), chip(3), chip(2), "—", "maths "+chip(3)],
], "lvt")}
<aside class="call" style="--k:#2563eb"><b>Every name is a door</b><p>Topic names with a dotted underline link to their own page in the <a href="https://claude.ai/artifact/McuS723LTAb16Q6SpdUsAT">Placement Knowledge Base</a>: the concept in depth, why it matters for your plan, key points, code, common mistakes, interview questions to tick off, practice problems and free resources. 147 pages, including 43 worked solutions (all tested) and model answers for Core CS and security.</p></aside>
<aside class="call" style="--k:#c2410c"><b>The one rule</b><p>Depth on one ladder beats breadth on five. Your main ladder is DSA to {chip(3)}. Core CS to {chip(2)}. Security to {chip(3)} because it's your degree and your edge. Everything else stops at {chip(1)}–{chip(2)} unless a specific job needs more.</p></aside>
''')

# ---------------------------------------------------------------- 01 timeline
TL = [
 ("16 Nov – 13 Dec 2026", "Full force", "C++ in 2 days, then Striver sheet 5–6/day in order, LeetCode daily, 1 Core CS subject, cyber 1 h, AWS 30 min", "#16a34a"),
 ("14 Dec – 30 Jan 2027", "Sheet core done", "College 1–2 days/week. Finish Striver core by 30 Jan: checkpoint 1. TenantWall build: CloudTrail, metric filter, alarm, SNS", "#0891b2"),
 ("8 Feb – 21 Mar 2027", "Hard pass 1 + paper", "Hard problems part 1, cyber 1 h (your side track), system design, CP habit (Tue/Thu + a weekend round), TenantWall paper by 21 Mar. No AI yet.", "#2563eb"),
 ("22 Mar – 7 Apr 2027", "Semester exams", "Exams first. DSA drops to 1 revision problem/day. 31 Mar: checkpoint 2, the HFT gate (a 5-minute look at your ratings).", "#64748b"),
 ("8 Apr – 30 May 2027", "Hard pass 2 + AWS", "SAA-C03 exam week of 19 Apr. Hard part 2, LLD, binary-exploitation taster, AI-security project in May (1 h/day). Elite HFT track only if you passed the gate.", "#7c3aed"),
 ("31 May – 31 Jul 2027", "Placement sprint", "2 mocks/week, company-tagged LeetCode, OA simulations, resume v5, 25 applications/week off-campus", "#c2410c"),
 ("Aug – Dec 2027", "Placements", "On-campus drives + off-campus machine running in parallel. Keep 3 problems/day.", "#be123c"),
 ("Jan – Jun 2028", "Convert / upgrade", "Internship-to-PPO or keep interviewing for a better offer until graduation", "#a16207"),
]
page("", head("01", "THE ROUTE", "Nov 2026 → Jun 2028 on one page", "The intensive track you chose, with the semester and exams built in.") +
 '<div class="tl">' + "".join(f'<div class="tli" style="--k:{c}"><span class="d">{E(d)}</span><h3>{E(t)}</h3><p>{E(x)}</p></div>' for d, t, x, c in TL) + '</div>' + f'''
<h2>Internship windows you can still hit</h2>
{table(["Window", "What opens", "Action now"], [
 ["Nov 2026 – Feb 2027", "Off-campus summer 2027 intern roles still open at startups and mid-tier product cos; Unstop competitions (Flipkart GRiD, Myntra HackerRamp, etc. run yearly)", "Apply weekly from mid-Dec once 150+ problems are done"],
 ["Feb – Apr 2027", "GSoC contributor applications (usually Mar–Apr); LFX Mentorship spring cohort", "Pick 1 org in Jan, make 3 merged PRs before applying"],
 ["Jun – Sep 2027", "Big Tech new-grad + 6-month intern roles for the 2028 batch", "Have resume, 2 projects, 400 problems ready by 31 May"],
 ["Year-round", "Bug bounty programmes, CTFs (KPMG, CyberSecurity events), open-source issues", "One CTF a month from Feb"],
])}
<aside class="call" style="--k:#0891b2"><b>NOC note</b><p>Your college gives no NOC by default, but you said a good company internship changes that. Have the offer letter first, then ask. Remote internships and 6-month Jan–Jun 2028 roles avoid most attendance clashes.</p></aside>
''')

# ---------------------------------------------------------------- 02 efficiency
page("", head("02", "LEARN FASTER", "The efficiency system", "Twelve methods with evidence behind them. Use all of them every week; they cost minutes and save months.", "#16a34a") +
 '<div class="eff">' + "".join(f'<div class="ef"><span>{i:02d}</span><h3>{E(t)}</h3><p>{d}</p></div>' for i, (t, d) in enumerate([
 ("Retrieval first", "Close the video and solve or explain from memory before checking. Testing yourself beats rereading for long-term memory (Roediger &amp; Karpicke, 2006)."),
 ("Spaced revision 1-3-7-21", "Re-solve each problem you got wrong after 1, 3, 7 and 21 days. Keep the list in a sheet; it's your most valuable file."),
 ("The 20-40 rule", "Stuck 20 min on Easy/Medium (40 on Hard)? Read only the hint or the approach line, then code it yourself. Never copy code."),
 ("Pattern, not problem", "After each solve, write one line: 'trigger → pattern'. E.g. 'sorted + pair sum → two pointers'. 300 problems become ~25 patterns."),
 ("Interleave", "Mix topics in revision days (a graph, a DP, a string). Blocked practice feels faster; interleaved practice sticks better."),
 ("Speak while you code", "Solve 1 problem a day out loud as if in an interview. It's a separate skill and the one tier-3 candidates practise least."),
 ("Error log", "Every wrong submission: the bug in one line (off-by-one, overflow, missed empty case). Read the log before each contest."),
 ("Upsolve", "After every contest, solve the next unsolved problem with the editorial. That one problem teaches more than the whole contest."),
 ("Feynman for Core CS", "Explain deadlock, normalisation or TCP handshake on a blank page in 5 lines. Can't? That's your revision list."),
 ("50/10 deep blocks", "50 min phone-in-another-room, 10 min break. 6 blocks/day is a full-force day. Track blocks, not hours."),
 ("Sleep 7+ h", "Memory consolidates during sleep; all-nighters before contests cost more than they give."),
 ("Weekly review (Sun, 30 min)", "What did I solve, what did I fail, what moves next week? Adjust the plan instead of abandoning it."),
 ], 1)) + '</div>' + f'''
<h2>A full-force day (16 Nov → 13 Dec)</h2>
{table(["Block", "Time", "Work"], [
 ["1–2", "09:30–11:30", "Striver sheet: 3 new problems in order (C++)"],
 ["3", "11:45–12:35", "LeetCode: 1 daily + 1 revision from the 1-3-7-21 list"],
 ["4", "14:00–14:50", "Core CS: one subtopic, Feynman page, 10 MCQs"],
 ["5", "15:00–15:50", "Striver: 2–3 more problems"],
 ["6", "17:00–18:00", "Cyber: one PortSwigger / TryHackMe lab, timed"],
 ["7", "18:15–18:45", "AWS 30 min (this week's module)"],
 ["8", "21:00–21:30", "Speak-aloud problem + error log + tomorrow's 3 problems picked"],
])}
''')

exec(open(OUT / "process.py").read())
# ---------------------------------------------------------------- 03 DSA ladder
page("", head("03", "MAIN LADDER", "DSA from L0 to L4", "The ladder that decides most offers. Climb it in order; don't skip L2 to chase L4.", "#2563eb") + ladder([
 (0, "C++ and STL in 2 days", "vector, string, pair, map, unordered_map, set, priority_queue, stack, queue, deque; sort with lambdas; iterators; <code>auto</code>; fast I/O. Big-O of every operation.",
  a("https://takeuforward.org/c/c-stl-tutorial-most-asked-stl-functions-in-c/", "takeuforward STL") + ", your Cheat Sheet §3, " + a("https://www.learncpp.com", "learncpp.com") + " (chapters you need)", "you can write any STL container op without searching"),
 (1, "Striver A2Z: steps 1–9", "Basics, sorting, arrays, binary search, strings, linked list, recursion, bit manipulation, stack/queue. Easy + Medium in sheet order, 5–6 a day.",
  a("https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/", "Striver A2Z sheet") + ", LeetCode daily", "you solve 80% of step problems within 25 min without hints"),
 (2, "Striver steps 10–18 + patterns", "Sliding window, two pointers, heaps, greedy, binary trees, BST, graphs (BFS/DFS, Dijkstra, topo sort, DSU), DP 1D/2D/subsequence/LIS/strings, tries.",
  "Striver sheet, " + a("https://neetcode.io/practice", "NeetCode 150") + " as a cross-check, LeetCode company tags", "LC Medium in ≤25 min, out loud, with complexity — 70% of the time"),
 (3, "Hard problems + contests", "Hards from the sheet in 2 passes; monotonic stack, interval DP, bitmask DP, DP on trees, segment tree / BIT, string hashing, KMP/Z. Weekly LC contest + Codeforces Div 2.",
  a("https://cses.fi/problemset/", "CSES") + ", " + "CP31 sheet" + ", " + a("https://codeforces.com", "Codeforces") + ", " + a("https://cp-algorithms.com", "cp-algorithms"), "LC contest rating 1800+ or CF 1400+; LC Hard in 45 min half the time"),
 (4, "Competitive edge", "CF Div 1/2 D–E, advanced graphs (flows, SCC, bridges), heavy-light, centroid, matrix exponentiation, probability DP, game theory. ICPC-style team practice.",
  "CSES advanced sections, " + a("https://usaco.guide", "USACO Guide") + " gold/platinum, CF gym, AtCoder ABC/ARC", "CF 1900+ / LC Knight-Guardian; only for the Elite HFT track or top-tier Google"),
]) + f'''
<h2>Problem counts that are enough</h2>
{table(["By", "Total solved", "Mix", "Signal"], [
 ["30 Jan 2027", "≈ 300", "Striver core E/M", chip(1)+"→"+chip(2)],
 ["30 May 2027", "≈ 450", "+ 120 Hards/tagged", chip(2)+"→"+chip(3)],
 ["31 Jul 2027", "≈ 550", "+ company-tagged, mocks", chip(3)],
])}
''')

# ---------------------------------------------------------------- 04 patterns
PAT = [
 ("Sorted array, find pair/triple", "Two pointers", 1), ("Longest/shortest subarray with condition", "Sliding window", 1),
 ("Min/max answer that is monotone", "Binary search on answer", 2), ("Next greater / smaller", "Monotonic stack", 2),
 ("k largest / streaming median", "Heap(s)", 2), ("Subarray sum = k", "Prefix sum + hashmap", 1),
 ("All subsets / permutations", "Backtracking", 1), ("Shortest path, unweighted", "BFS", 1),
 ("Shortest path, weighted ≥0", "Dijkstra", 2), ("Dependencies / order", "Topological sort", 2),
 ("Connected groups, merging", "DSU", 2), ("Count ways / min cost over choices", "DP", 2),
 ("Two strings compare", "2D DP (LCS/edit)", 2), ("Prefix matching many words", "Trie", 2),
 ("Range query + update", "Segment tree / BIT", 3), ("Intervals overlap", "Sort + sweep", 2),
 ("n ≤ 20, choose subsets", "Bitmask DP", 3), ("Tree answer per node", "DFS + DP on trees", 3),
 ("Max XOR pair", "Bit trie", 3), ("Pattern in text, O(n)", "KMP / Z / hashing", 3),
]
page("", head("04", "PATTERN TRIGGERS", "Read the problem, name the pattern", "20 triggers that cover most interview problems. Cover the right column and quiz yourself.", "#2563eb") +
 table(["If the problem says…", "Reach for", "Level"], [[E(t), f"<b>{E(p)}</b>", chip(l)] for t, p, l in PAT], "pt") + f'''
<h2>Constraint → complexity</h2>
{table(["n up to", "10", "20", "500", "5 000", "10⁶", "10⁹+"], [["Aim for", "O(n!)", "O(2ⁿ)", "O(n³)", "O(n²)", "O(n log n)", "O(log n) / O(1)"]], "cx")}
<aside class="call" style="--k:#2563eb"><b>The interview loop (UMPIRE)</b><p><b>U</b>nderstand (repeat it, ask about constraints and edge cases) · <b>M</b>atch a pattern · <b>P</b>lan in words, state complexity · <b>I</b>mplement cleanly · <b>R</b>eview with a dry run · <b>E</b>valuate trade-offs and a better approach. Talk the whole time.</p></aside>
''')

# ---------------------------------------------------------------- 05 Core CS
page("", head("05", "CORE CS", "OS, DBMS, CN, OOP, SQL by level", "Interviewers ask the same 40 questions. Know them at L2 and you've covered most rounds.", "#0891b2") + table(
 ["Subject", chip(1) + " know", chip(2) + " explain + example", chip(3) + " depth"], [
 ["<b>OS</b>", "process vs thread, scheduling algos, deadlock conditions", "paging, virtual memory, page faults, mutex vs semaphore, producer-consumer, thrashing", "TLB, copy-on-write, context-switch cost, Linux scheduler (CFS), memory-mapped files"],
 ["<b>DBMS</b>", "keys, ER, normal forms to 3NF, ACID", "BCNF, indexing (B+ tree), transactions and isolation levels, deadlock, joins", "MVCC, write-ahead logging, query plans, sharding vs replication, CAP"],
 ["<b>CN</b>", "OSI vs TCP/IP, TCP vs UDP, IP classes, DNS", "3-way handshake, flow vs congestion control, HTTP/HTTPS + TLS, subnetting, what happens when you type a URL", "TCP congestion algorithms, QUIC/HTTP3, BGP basics, NAT traversal, CDN"],
 ["<b>OOP</b>", "4 pillars with C++ examples", "virtual functions + vtable, overloading vs overriding, abstract vs interface, SOLID", "design patterns (singleton, factory, observer, strategy), RAII, rule of 5"],
 ["<b>SQL</b>", "SELECT, WHERE, GROUP BY, HAVING, JOIN", "subqueries, window functions (RANK, ROW_NUMBER, LAG), Nth highest salary", "query optimisation, indexes in practice, CTE recursion"],
], "cs") + f'''
<p class="res"><b>Use:</b> {a("https://www.geeksforgeeks.org/operating-systems/", "GfG OS")} · Striver/takeuforward Core CS notes · {a("https://www.youtube.com/@GateSmashers", "Gate Smashers")} for weak topics · {a("https://leetcode.com/studyplan/top-sql-50/", "LeetCode SQL 50")} · {a("https://sqlbolt.com", "SQLBolt")}</p>
<h2>The 12 most-asked questions (answer each in 60 seconds)</h2>
<ol class="q2">{''.join(f'<li>{E(q)}</li>' for q in [
 "Process vs thread — and why threads are cheaper", "Four conditions of deadlock and how to prevent one",
 "What is virtual memory and why do we need it?", "Mutex vs semaphore with an example",
 "Explain normalisation up to 3NF using one table", "What are ACID properties? Which isolation level prevents dirty reads?",
 "How does a B+ tree index speed up a query?", "What happens when you type google.com and press Enter?",
 "TCP vs UDP — when would you choose UDP?", "Explain the TCP 3-way handshake and why not 2-way",
 "Runtime polymorphism in C++: how does the vtable work?", "Write SQL for the second-highest salary per department",
])}</ol>
''')

# ---------------------------------------------------------------- 06 design + projects
page("", head("06", "BUILD AND DESIGN", "System design and projects", "Freshers get LLD more than HLD. Projects get you shortlisted; design talk gets you hired.", "#7c3aed") + ladder([
 (1, "LLD basics", "Classes, relationships, SOLID, 4 patterns. Design a parking lot, library system, Splitwise, elevator in C++.", a("https://github.com/ashishps1/awesome-low-level-design", "awesome-low-level-design") + " (free)", "you can design a parking lot with classes in 30 min"),
 (2, "HLD fundamentals", "Load balancer, caching, CDN, DB choice (SQL vs NoSQL), replication, sharding, message queues, rate limiting. Design URL shortener, chat app, news feed.", a("https://github.com/donnemartin/system-design-primer", "system-design-primer") + ", " + a("https://roadmap.sh/system-design", "roadmap.sh") + ", your AWS SAA notes", "you can draw and defend a URL shortener with numbers"),
 (3, "Trade-off depth", "Consistency models, CAP/PACELC, idempotency, distributed IDs, back-pressure, observability.", "Designing Data-Intensive Applications (Kleppmann) chapters 1–9; engineering blogs (Razorpay, Zomato, Uber)", "you can argue two designs and pick one with reasons"),
]) + f'''
<h2>Projects that work for a cyber + SDE profile</h2>
{table(["Project", "Shows", "Level"], [
 ["<b>TenantWall</b>: ABAC multi-tenant isolation on AWS with CloudTrail, metric-filter alarm, SNS, Access Analyzer + paper", "cloud security, IAM depth, research", chip(3)],
 ["Rate-limited URL shortener (C++/Go or Node) with Redis cache, load test numbers, deployed on AWS", "backend + system design", chip(2)],
 ["Log-based intrusion detector: parse auth/nginx logs, flag brute force and scans, dashboard", "security + data handling", chip(2)],
 ["AI-security project (May): a RAG assistant you attack with prompt injection and then defend", "AI + AppSec (rare combo)", chip(3)],
 ["Open-source PRs (3+ merged) in one org", "real code review, collaboration", chip(3)],
])}
<aside class="call" style="--k:#7c3aed"><b>Project rule</b><p>Every project needs: a live link or demo video, a README with an architecture diagram, one number (latency, users, requests/s, bugs found), and a line on what you'd do next. Two great projects beat six tutorials.</p></aside>
''')

# ---------------------------------------------------------------- 07 security
page("", head("07", "YOUR EDGE", "Security ladder", "Your degree is cybersecurity. Most SDE candidates can't talk about it — use that in every interview.", "#be123c") + ladder([
 (0, "Foundations", "Linux command line, networking basics, HTTP, how the web works.", a("https://overthewire.org/wargames/bandit/", "OverTheWire Bandit") + ", " + a("https://tryhackme.com/path/outline/presecurity", "TryHackMe Pre-Security") + " (free rooms)", "Bandit level 20+"),
 (1, "Web security", "OWASP Top 10: SQLi, XSS, CSRF, SSRF, IDOR, auth flaws, access control.", a("https://portswigger.net/web-security", "PortSwigger Web Security Academy") + " (free)", "all Apprentice labs + 30 Practitioner labs"),
 (2, "Practical AppSec + cloud", "Burp Suite workflow, code review for vulns, secure coding in C++, AWS IAM/S3 misconfigurations, threat modelling (STRIDE).", "PortSwigger Practitioner, " + a("https://flaws.cloud", "flaws.cloud") + ", " + a("https://owasp.org/www-project-top-ten/", "OWASP"), "you can explain and fix 5 vulns in code"),
 (3, "Binary + CTFs", "C memory, stack layout, buffer overflow, format strings, ROP basics, GDB/pwndbg, Ghidra reversing. Jeopardy CTFs monthly.", a("https://pwn.college", "pwn.college") + ", " + a("https://picoctf.org", "picoCTF") + ", " + a("https://ctftime.org", "CTFtime"), "top-25% finish in a mid CTF; 3 write-ups on a blog"),
 (4, "Proof in the wild", "Valid bug bounty reports, a CVE, a security tool on GitHub with users, conference/college talk.", a("https://hackerone.com/hacktivity", "HackerOne") + ", " + a("https://bugcrowd.com", "Bugcrowd") + ", vendor disclosure programmes", "one accepted report or CVE"),
]) + '''
<aside class="call" style="--k:#be123c"><b>Use it in SDE interviews</b><p>When asked about any project: "I also threat-modelled it — here's the IDOR I found and fixed." When asked about databases: mention SQL injection and parameterised queries. One security sentence per answer makes you memorable.</p></aside>
''')

# ---------------------------------------------------------------- 08 aws, ai, hft
page("", head("08", "MULTIPLIERS", "AWS and the AI-security project", "Each one adds a line to your resume that most tier-3 candidates don't have. HFT has its own Elite page.", "#a16207") + table(
 ["Track", chip(1), chip(2), chip(3)], [
 ["<b>AWS</b> (30 min daily)", "IAM, EC2, S3, VPC basics; billing alarm", "AWS Academy Cloud Architecting done; SAA-C03 passed (Apr 2027)", "TenantWall in production-style; security specialty later"],
 ["<b>AI-security project</b> (May, 1 h a day)", "How LLMs work, embeddings, your first API call", "A RAG assistant over your notes, with a 20-question eval set", "Prompt-injection attacks and defences (OWASP LLM Top 10), a demo video"],
], "cs") + f'''
<p class="res"><b>Use:</b> AWS Academy (via your faculty) · {a("https://www.youtube.com/@freecodecamp", "freeCodeCamp")} SAA course · {a("https://www.deeplearning.ai/short-courses/", "DeepLearning.AI short courses")} · {a("https://genai.owasp.org/llm-top-10/", "OWASP LLM Top 10")} · {a("https://gandalf.lakera.ai", "Gandalf")}</p>
<aside class="call" style="--k:#a16207"><b>Why AI waits until May</b><p>A daily AI track from February would have run beside the Hard pass, cyber, the paper, AWS prep and college: ten tracks at once, the burnout zone. One 4-week project gives you the interview story (build, measure, attack, defend) at a sixth of the hours.</p></aside>
<h2>Resume: one page, ATS-safe</h2>
<div class="two"><div><h3>Order</h3><ol><li>Name, phone, email, LinkedIn, GitHub, LeetCode/CF links</li><li>Education (CGPA if ≥ 7.5)</li><li>Experience / internships</li><li>Projects (2–3, each 2–3 bullets)</li><li>Achievements (ratings, CTF ranks, SAA cert, paper)</li><li>Skills (languages, tools, cloud)</li></ol></div>
<div><h3>Bullet formula</h3><p class="mono">Did X using Y, which resulted in Z (number)</p><p><b>Weak:</b> Made a URL shortener using Node.</p><p><b>Strong:</b> Built a URL shortener serving 1.2k req/s on one t3.micro by adding Redis caching and a token-bucket rate limiter; p95 latency 18 ms.</p><p>Single column, no photos, no tables, PDF, file name <span class="mono">Firstname_Lastname_SDE.pdf</span>.</p></div></div>
''')


# ---------------------------------------------------------------- Elite: HFT (only through the gate)
HFTP = [("W01–W04", "5 Apr – 2 May", "Counting and basic probability", "Permutations, combinations, inclusion–exclusion, Bayes. Blitzstein–Hwang ch. 1–2 + Stat 110. 10 easy Brainstellar puzzles a week.", "40 solved, one-line idea each"),
        ("W05–W08", "3 May – 30 May", "Random variables and expected value", "Linearity of expectation, indicators, binomial/geometric/Poisson, variance. Fair-price games. Mosteller's first 20.", "20 EV problems, no answers peeked"),
        ("W09–W12", "31 May – 27 Jun", "Interview probability and puzzles", "Green-book probability and brain-teasers, Markov chains, gambler's ruin, Brainstellar medium.", "A sheet of 30 patterns"),
        ("W13–W16", "28 Jun – 25 Jul", "Timed practice + low-latency C++", "Timed puzzle sets, Heard on the Street, market-making games; move semantics, cache behaviour, lock-free basics.", "2 timed mocks a week")]
page("", head("L4", "ELITE · OPENS ONLY IF YOU PASS THE 31 MAR CHECKPOINT", "The HFT track", "The only place HFT appears in your plan. Everything else is Path A: SDE with security and cloud depth.", "#c2410c") +
 table(["Checkpoint", "Date", "Pass if", "Then"], [
  ["1", "30 Jan 2027", "Striver core done on time; LeetCode Mediums in about 25 minutes", "Keep the CP habit from 8 Feb. Missed it? Finish Striver first; the gate stays at 31 Mar."],
  ["<b>2, the gate</b>", "31 Mar 2027", "Codeforces 1400+ <b>or</b> LeetCode contest rating 1800+", "<b>Pass:</b> open the track on 8 Apr. <b>Miss:</b> stay on Path A; the contest practice still makes every online test easier."],
 ], "cs") + f'''
<div class="two"><div><h3>What changes if you open it</h3><ul class="tight">
<li><b>Add</b> 1 to 1.5 h a day of the plan below, 8 Apr – 25 Jul</li>
<li><b>CP habit becomes daily:</b> 2 problems a day + a Codeforces Div 2 round a week; aim for 1600+ by July</li>
<li><b>Cyber drops to 3 days a week;</b> keep the binary taster, it pairs with low-latency C++</li>
<li><b>AI-security project shrinks to 2 weeks:</b> build, then attack</li>
<li><b>Never cut</b> the Hard pass, Core CS, the AWS exam, mock interviews</li></ul></div>
<div><h3>Which HFT role fits you</h3>{table(["Role", "Tests", "Fit"], [
  ["SWE, low-latency C++", "Hard coding, C++ depth, OS, networks", chip(3) + " best fit"],
  ["Quant trader", "Probability, mental maths, market-making", chip(4) + " possible"],
  ["Quant researcher", "Deeper probability, statistics, research", chip(4) + " stretch"]], "cs")}</div></div>
<h2>The 16-week plan, 1 to 1.5 h a day</h2>
{table(["Weeks", "Focus", "Inside the hour", "Proof"], [[f"<b>{w}</b><br>{d}", f"<b>{E(f)}</b>", E(i), E(pr)] for w, d, f, i, pr in HFTP], "cs")}
<p class="res"><b>Every day:</b> 10 min of {a("https://arithmetic.zetamac.com", "Zetamac")} (40+, then 50+) · one {a("https://codeforces.com", "Codeforces")} Div 2 round a week, then upsolve.
<b>Learn from:</b> {a("https://projects.iq.harvard.edu/stat110", "Stat 110 + Blitzstein–Hwang (free)")} · {a("https://www.brainstellar.com", "Brainstellar")} · {a("https://cses.fi/problemset/", "CSES")} · Zhou's green book · Mosteller's Fifty Challenging Problems · Heard on the Street.
<b>Knowledge Base:</b> {a("https://claude.ai/artifact/McuS723LTAb16Q6SpdUsAT#probability", "probability")} · {a("https://claude.ai/artifact/McuS723LTAb16Q6SpdUsAT#hft-overview", "HFT roles and the gate")} · {a("https://claude.ai/artifact/McuS723LTAb16Q6SpdUsAT#low-latency-cpp", "low-latency C++")} · {a("https://claude.ai/artifact/McuS723LTAb16Q6SpdUsAT#cp", "contests")}</p>
<aside class="call" style="--k:#c2410c"><b>Be honest with yourself</b><p>HFT firms hire very few freshers, mostly from strong competitive-programming profiles. The gate exists so you spend these hours only when your ratings say it is realistic. Missing it is not a failure: Path A is the plan.</p></aside>
''')

# ---------------------------------------------------------------- 09 off-campus machine
page("", head("09", "OFF-CAMPUS", "The hiring machine", "On-campus is a lottery you can't control. Off-campus is a numbers game you can.", "#c2410c") + table(
 ["Channel", "How", "Weekly quota"], [
 ["<b>Referrals</b>", "Find alumni/employees on LinkedIn at target companies; send the referral note below with job ID + resume", "10 messages"],
 ["<b>Careers pages</b>", "Bookmark 40 companies' careers pages; check Mon + Thu. Apply within 48 h of posting", "10 applications"],
 ["<b>Hiring contests</b>", "Unstop, HackerEarth, Naukri Campus, company hackathons (Flipkart GRiD, Myntra HackerRamp, Amazon ML Summer School, JPMC Code for Good)", "every one that opens"],
 ["<b>Cold email</b>", "Startup founders/CTOs (YC India, funded on Inc42/Entrackr) with a 5-line email + one relevant project", "5 emails"],
 ["<b>Open source</b>", "GSoC, LFX Mentorship, MLH Fellowship; maintainers refer contributors", "2 PRs"],
 ["<b>Contest ratings</b>", "Recruiters filter on LC/CF rating; some firms invite top contest rankers", "1–2 contests"],
], "cs") + '''
<div class="two"><div class="tpl"><h3>Referral message (LinkedIn, 300 chars)</h3><p>Hi [Name], I'm a 3rd-year CSE (Cybersecurity) student who has solved 450+ DSA problems and built [project — one line]. I'm applying for [Role, Job ID] at [Company]. Would you be open to referring me? Resume: [link]. Happy to share anything else. Thank you!</p></div>
<div class="tpl"><h3>Cold email to a startup</h3><p><b>Subject:</b> SDE intern — built [X] relevant to [their product]</p><p>Hi [Name], I use/studied [product]. I'm a CSE (Cyber) student; I built [project + number], and I noticed [specific thing — a bug, a security header missing, a feature idea]. I'd love to intern with your team for [months]. Resume + GitHub: [links]. Could we talk for 15 minutes this week?</p></div></div>
<aside class="call" style="--k:#c2410c"><b>Track it</b><p>One sheet: company, role, date, channel, contact, status, next follow-up. Follow up once after 5–7 days. Expect ~2–5% replies; 50 good applications a month is what produces interviews.</p></aside>
''')

# ---------------------------------------------------------------- 10 interviews
page("", head("10", "THE ROOM", "Interviews, rounds and offers", "What each round checks, and how to prepare for it.", "#0f766e") + table(
 ["Round", "What it checks", "Prepare by"], [
 ["Online assessment (60–90 min)", "2–3 DSA problems, sometimes MCQs on CS/aptitude", "Timed LC contests, HackerRank practice, read every line of constraints"],
 ["DSA interview (45–60 min)", "1–2 problems, communication, edge cases, complexity", "Speak-aloud practice, 2 mocks/week from June (Pramp, peers)"],
 ["Core CS / technical", "OS, DBMS, CN, OOP, SQL, your projects in depth", "The 12 questions, Feynman pages, project deep-dive script"],
 ["LLD / HLD (product cos)", "Structuring classes, trade-offs", "6 LLD designs written in C++, 4 HLD diagrams"],
 ["Behavioural / bar raiser", "Ownership, conflict, failure, learning", "6 STAR stories that each fit several questions"],
 ["HR", "Fit, relocation, notice, compensation", "Research the company; know your number"],
], "cs") + f'''
<div class="two"><div><h3>Six STAR stories to prepare</h3><ol><li>A hard technical problem you solved (TenantWall IAM)</li><li>A time you failed and what you changed</li><li>A conflict in a team</li><li>Learning something fast (C++/AWS in weeks)</li><li>Going beyond the task (security finding in a project)</li><li>Leading or helping someone</li></ol></div>
<div><h3>Offer basics</h3><ul><li>CTC ≠ in-hand. Ask for the split: fixed, variable, joining bonus, stocks (vesting).</li><li>Never say a number first if you can avoid it; if pushed, give a range from {a("https://www.levels.fyi", "levels.fyi")} / {a("https://www.glassdoor.co.in", "Glassdoor")}.</li><li>Check the bond/service agreement clause before signing.</li><li>A written offer + another interview in progress is your leverage — be polite and honest.</li></ul></div></div>
<h2>Mock schedule (from 31 May)</h2>
{table(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], [["DSA mock (peer)", "Company-tagged set", "Core CS mock", "LLD design", "OA simulation 90 min", "LC + CF contest", "Review + STAR practice"]], "wk")}
''')

# ---------------------------------------------------------------- 11-12 stories
STORIES = [
 ("Tier-3 → Microsoft, Google and Meta", "Full-time · 2024", "Rejected by Google 3 times and Meta twice before getting selected at both.",
  "Treat rejection as data: log which round failed and fix that round only. Persistence over several cycles is normal, not a sign you're not good enough.",
  "https://leetcode.com/discuss/post/5332550/My-Journey-from-a-Tier-3-College-to-Microsoft-Google-and-Meta:-Lessons-Learned/", "LeetCode Discuss", "Self-reported", 3),
 ("Tier-3 → Razorpay SDE intern", "Internship offer · Aug 2025", "Came through the college T&P cell; the drive had an 8+ CGPA cut-off.",
  "CGPA still opens doors at fintechs. Keep yours above 8 if you can — it's cheaper than any course.",
  "https://leetcode.com/discuss/post/8513477/razorpay-sde-intern-aug-2025-offer-by-an-9rbc/", "LeetCode Discuss", "Self-reported", 2),
 ("Tier-3 → Eternal (Zomato) SDE intern + FTE", "Off-campus · Dec 2025", "Got in through a referral and cleared the intern + full-time process.",
  "Referrals are the strongest off-campus channel. Ten referral messages a week is your quota.",
  "https://leetcode.com/discuss/interview-experience/7407389", "LeetCode Discuss", "Self-reported", 2),
 ("Agoda SDE intern, 6 months, Gurugram", "Offer · May 2026", "A six-month SDE internship offer, documented round by round.",
  "Six-month internships (Jan–Jun of final year) are a real route to a PPO and avoid the summer NOC problem.",
  "https://leetcode.com/discuss/post/8380191/agoda-sde-intern-6-months-gurugram-may-2-9o9b/", "LeetCode Discuss", "Self-reported", 2),
 ("Amazon SDE intern, off-campus", "Selected", "An off-campus Amazon internship: online assessment, then DSA interviews.",
  "Amazon tests DSA + Leadership Principles. Pair every DSA mock with one STAR story.",
  "https://www.geeksforgeeks.org/interview-experiences/amazon-interview-experience-sde-intern-off-campus/", "GeeksforGeeks", "Self-reported", 3),
 ("Myntra RampUp, via Unstop", "Internship · selected", "Entered through an Unstop hiring programme rather than a referral.",
  "Hiring contests on Unstop skip the resume filter. Enter every relevant one.",
  "https://medium.com/@mehakkanyal/myntra-rampup-sde-internship-interview-experience-off-campus-via-unstop-e68307d86771", "Medium", "Self-reported", 2),
 ("INDmoney SDE intern, off-campus", "Selected", "A fintech startup internship with DSA and project rounds.",
  "Startups ask about your projects in depth — have numbers ready.",
  "https://www.geeksforgeeks.org/indmoney-interview-experience-sde-intern-off-campus/", "GeeksforGeeks", "Self-reported", 2),
 ("Scaler SDE intern, off-campus", "Selected", "Ed-tech internship through an off-campus process.",
  "Mid-size companies are reachable earlier — use them as interview practice that might also be an offer.",
  "https://www.geeksforgeeks.org/interview-experiences/scaler-academy-interview-experience-for-sde-intern-off-campus/", "GeeksforGeeks", "Self-reported", 2),
 ("Accolite Digital, Mumbai", "FTE + intern · off-campus · Jan 2022", "An off-campus offer from a Mumbai engineering services company.",
  "Mumbai-based companies are worth a separate list — no relocation question, and local alumni refer more readily.",
  "https://leetcode.com/discuss/interview-experience/1827320/accolite-digital-sde-fteintern-mumbai-jan-2022-accepted-offcampus", "LeetCode Discuss", "Self-reported", 1),
 ("Tier-3 → tier-1 software company", "Full-time", "A personal account of moving from a tier-3 college to a top product company.",
  "Read the whole story for the timeline: the gap between 'started' and 'offer' is usually 12–24 months. You're on that clock now.",
  "https://medium.com/@surajjme/tier-3-college-to-tier-1-software-company-304dae736b23", "Medium", "Self-reported", 2),
 ("Tier-3 MCA → Google Summer of Code 2026", "Open source", "Got into GSoC 2026 as a tier-3 MCA student.",
  "GSoC is a brand that removes the college question. Start contributing in Jan; applications are usually Mar–Apr.",
  "https://dev.to/tarunsinghofficial/how-i-got-into-google-summer-of-code-gsoc-2026-as-a-tier-3-mca-student-4017", "DEV", "Self-reported", 3),
 ("B.Tech → KPMG India cyber (CDIR) intern via CTF", "Security internship", "A KPMG campus CTF was central to moving from final-year B.Tech student to intern on KPMG India's cyber incident response team.",
  "CTF results are a hiring channel for security roles. Play one a month from Feb and write up what you solve.",
  "https://kpmg.com/in/en/insights/2025/10/capture-the-flag-2025-campus-edition.html", "KPMG India", "Company page", 3),
 ("Bug bounties → security engineer", "Security career · 2015", "Anand Prakash started reporting bugs to Facebook and others, which led to a security engineering career.",
  "Accepted bug reports are proof no college name can match. One valid report is worth a line at the top of your resume.",
  "https://yourstory.com/2015/10/techie-tuesdays-anand-prakash", "YourStory", "Interview (older)", 4),
 ("Reported CBSE portal flaws → IIT Kanpur cyber team", "Contract role", "A teenager who reported security flaws in CBSE's marks portal was taken on as an engineer in IIT Kanpur's cybersecurity team (contractual).",
  "Responsible disclosure, written up publicly, can be a résumé on its own.",
  "https://www.siasat.com/teen-who-flagged-cbse-portal-flaws-lands-job-at-iit-kanpur-3486892/amp/", "Siasat", "News report", 4),
 ("Biology graduate → cybersecurity", "Self-taught career", "Anugrah S.R. moved from biology into cybersecurity through self-learning.",
  "If a non-CS graduate can do it, a CSE (Cyber) student with a plan is already ahead.",
  "https://www.cloudsek.com/students-challenge-blogs/from-biology-to-cybersecurity-how-anugrah-s-r-built-a-career-through-self-learning", "CloudSEK", "Company blog", 2),
 ("Two honest rejections: Microsoft and Cisco", "Not selected", "Two tier-3 candidates wrote up interviews they failed.",
  "Read failures as carefully as wins: most write-ups point to communication, edge cases or weak Core CS — all fixable before Aug 2027.",
  "https://medium.com/@adiiiti21/my-microsoft-interview-experience-sde-intern-d2d1499b324e", "Medium + LeetCode", "Self-reported", 3),
]
def story(i, s):
    t, kind, what, lesson, url, src, ver, l = s
    return (f'<article class="st" style="--k:{LV[l][1]}"><div class="sn">{i:02d}</div><div><p class="sk">{E(kind)} · <span class="ver">{E(ver)}</span></p>'
            f'<h3>{E(t)}</h3><p>{E(what)}</p><p class="sl"><b>Copy this:</b> {E(lesson)}</p><p class="ss">{a(url, src)}</p></div></article>')
for half, (lo, hi, sub) in enumerate([(0, 8, "SDE offers and internships, from public interview experiences."), (8, 16, "More routes — including security, open source and the honest failures.")]):
    page("", head("11" if half == 0 else "12", "THEY DID IT FROM TIER-3", "Stories" + (" (part 2)" if half else ""), sub, "#be123c") +
         '<div class="sts">' + "".join(story(i + 1, STORIES[i]) for i in range(lo, hi)) + '</div>' +
         ('''<aside class="call" style="--k:#be123c"><b>What every story has in common</b><p>(1) Hundreds of problems solved before the first offer. (2) One channel that beat the college filter: a referral, a contest, a CTF, open source. (3) At least one rejection first. The college name decided none of them.</p></aside>''' if half == 0 else
          f'''<aside class="call" style="--k:#64748b"><b>How to read these</b><p>Most are self-reported posts; outcomes aren't independently checked. The Cisco rejection is at {a("https://leetcode.com/discuss/interview-experience/4202678", "LeetCode Discuss")}. Aggregator pages that list tier-3 success stories without sources (for example {a("https://jobrise.io/en/blog/tier-3-college-google-hired-stories/", "jobrise.io")}) are left out of the cards. I found no published tier-3 stories for security-engineer full-time offers specifically — the security routes above are CTFs, bug bounties and disclosure.</p></aside>'''))

# ---------------------------------------------------------------- 13 checklists
page("", head("13", "CHECK YOURSELF", "Milestone checklists", "Tick these on paper. If a box is empty at its date, the next month fixes that box first.", "#16a34a") + '<div class="ck">' + "".join(
 f'<div class="cb" style="--k:{c}"><h3>{E(d)}</h3><ul>' + "".join(f"<li>{E(x)}</li>" for x in xs) + '</ul></div>' for d, c, xs in [
 ("13 Dec 2026", "#16a34a", ["C++ STL fluent", "Striver steps 1–6 done (~150 problems)", "OS notes complete", "PortSwigger Apprentice labs done", "AWS weeks 1–4 + billing alarm", "Error log + 1-3-7-21 sheet in use"]),
 ("30 Jan 2027", "#0891b2", ["Striver core done (~300)", "LC contest every week", "DBMS + SQL 50 done", "TenantWall: trail, metric filter, alarm, SNS live", "Checkpoint 1: Mediums in ~25 min", "Resume v1"]),
 ("21–31 Mar 2027", "#2563eb", ["Hard pass 1 done", "TenantWall paper submitted", "CN + OOP notes complete", "1 CTF write-up", "20 off-campus applications sent", "31 Mar gate: CF 1400+ or LC 1800+?"]),
 ("30 May 2027", "#7c3aed", ["~450 problems, 120 Hards", "AWS SAA-C03 passed", "4 LLD + 2 HLD designs", "AI-security project shipped with a demo", "Binary taster: 5 pwn.college levels", "Resume v4 reviewed by 2 seniors"]),
 ("31 Jul 2027", "#c2410c", ["~550 problems, LC 1800+", "16 mocks done", "6 STAR stories rehearsed", "Company-tagged lists for top 15 targets", "100 applications + 40 referral asks", "LinkedIn + GitHub cleaned up"]),
 ("Any week", "#be123c", ["≥ 30 problems solved", "≥ 1 contest", "≥ 3 h Core CS", "≥ 5 h cyber", "≥ 3.5 h AWS", "Sunday review done"]),
]) + '</div>' + '''
<aside class="call" style="--k:#c2410c"><b>Mistakes that cost tier-3 students offers</b><p>Watching solutions instead of solving · 1000 problems with no revision · no speaking practice · projects copied from tutorials · applying only on campus · waiting to "be ready" before applying · ignoring CGPA · quitting after the first rejection.</p></aside>
''')

# ---------------------------------------------------------------- 14 sources
SRC = [
 ("Courses and practice", [
  ("Striver A2Z DSA sheet", "https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/"),
  ("NeetCode practice", "https://neetcode.io/practice"), ("CSES problem set", "https://cses.fi/problemset/"),
  ("cp-algorithms", "https://cp-algorithms.com"),
  ("USACO Guide", "https://usaco.guide"), ("roadmap.sh", "https://roadmap.sh"), ("LeetCode SQL 50", "https://leetcode.com/studyplan/top-sql-50/"),
  ("System Design Primer", "https://github.com/donnemartin/system-design-primer"), ("Awesome LLD", "https://github.com/ashishps1/awesome-low-level-design"),
  ("PortSwigger Academy", "https://portswigger.net/web-security"), ("pwn.college", "https://pwn.college"), ("OverTheWire", "https://overthewire.org/wargames/bandit/"),
  ("picoCTF", "https://picoctf.org"), ("CTFtime", "https://ctftime.org"), ("flaws.cloud", "https://flaws.cloud"),
  ("OWASP LLM Top 10", "https://genai.owasp.org/llm-top-10/"), ("Stat 110", "https://projects.iq.harvard.edu/stat110"),
 ]),
 ("Guides read for this edition", [
  ("Tier-3 roadmap (Substack)", "https://devshreebharatia.substack.com/p/tier-3-college-roadmap-for-software"),
  ("Product companies from tier-3 (Medium)", "https://medium.com/@hardiktaneja_99752/how-to-get-placed-in-product-based-companies-from-a-tier-3-college-f24bb4861b73"),
  ("10 LPA from tier-3 (lets-code)", "https://www.lets-code.co.in/blogs/how-to-get-a-10-lpa-job-as-a-fresher-from-a-tier-3-college/"),
  ("HashedIn SDE-1 experience", "https://leetcode.com/discuss/post/7620735/hashedin-by-deloitte-sde-1-interview-exp-urnm/"),
  ("Off-campus backend internship", "https://leetcode.com/discuss/post/7703521/title-sde-internship-interview-experienc-sbqj/"),
  ("Intuit SDE intern (not selected)", "https://www.geeksforgeeks.org/interview-experiences/intuit-interview-experience-for-sde-internship-off-campus/"),
  ("Cyber jobs in India (talk)", "https://sessionize.com/s/aseem-shrey/getting-a-cybersecurity-job-in-india/41330"),
 ]),
]
page("", head("14", "SOURCES", "Everything linked in this guide", "All free unless noted. Story links are in sections 11–12.", "#64748b") + "".join(
 f'<h2>{E(t)}</h2><ul class="src">' + "".join(f"<li>{a(u, n)}<span>{E(u)}</span></li>" for n, u in xs) + "</ul>" for t, xs in SRC) + '''
<p class="fin">Climb one rung at a time. The college name is a filter for the first round only — everything after it is the work in this guide.</p>
''')

CSS = (OUT / "style.css").read_text()
doc = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Tier-3 to Top Offer</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=Inter:wght@400;600;700&family=JetBrains+Mono:wght@500&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>{"".join(pages)}</body></html>'''
(OUT / "placement-field-guide.html").write_text(doc)
print(len(pages), "pages")
