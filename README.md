# Placement Prep

**Read everything directly on GitHub:** [generated/read/](generated/read/) has every guide, pack, plan, the knowledge base and both A2Z sheets as plain Markdown (no HTML, no PDF viewer needed). Start with [Your final plan](generated/read/final-plan.md).

My placement kit (B.Tech CSE Cybersecurity, class of 2028). **Plan: Path A**, an SDE profile with security and cloud depth, plus an Elite HFT track that opens only if I pass the 31 March 2027 checkpoint.

## Open

| File | What it is |
|---|---|
| `index.html` | Home screen linking everything below |
| `playbook.html` | Daily tracker: Today's problems, ticks, XP, five themes, every lesson. Installable, works offline |
| `roadmap.html` | Nov 2026 → Jun 2028: timeline, week-by-week and day-by-day plan, milestones, checkpoints, Elite section |
| `knowledge-base.html` | 167 pages: concepts, 43 tested worked solutions, Core CS and security model answers, 8 mock interviews, 10 company files |
| `cheat-sheet.html` | One-page rules, complexity, STL, patterns, templates, DP, Core CS, SQL, security, AWS |
| `Placement-Prep-Complete.pdf` | Guide + cheat sheet + roadmap in one PDF, with a start page, clickable index and bookmarks |
| `Placement-Knowledge-Base.pdf` | The Knowledge Base as a PDF, works offline |
| `DSA-Placement-Playbook.pdf` | The Playbook (Café theme) as a PDF |
| `Tier3-to-Top-Offer-Placement-Guide.pdf` | The guide on its own |
| `Striver-A2Z-DSA-Sheet-Classic.pdf` | The older 18-step A2Z sheet (474 items) the plan is built on, with an appendix of items missing from the new version |
| `Striver-A2Z-DSA-Sheet-2026.pdf` | The current takeuforward A2Z sheet (20 sections, 453 problems), clickable |
| `GEMINI-HANDOFF.md` | Full context to paste into another AI assistant |
| `sources/` | Scripts that build all of the above |
| `generated/roadmapsh-checklists.pdf` | roadmap.sh maps (Backend, Cyber Security, AWS, CS, System Design, DevOps) as checklists, mapped to the kit with gaps marked |
| `generated/final-plan.pdf` | Final plan: the plan, seven rules, month-by-month actions to placements, opportunity windows (SRFP, GSoC, LFX, IIT research, hiring challenges), daily system, checkpoints, filtered resources seniors used, internship hunt playbook, and a 'when X, open Y' map of the kit; 19 cited sources |
| `generated/worked-solutions-2.pdf` | Worked Solutions II: 40 more most-asked LeetCode problems (not in the Knowledge Base set), each with idea, steps, tested C++17 code, traps and follow-ups; clickable index by pattern |
| `generated/worked-solutions-3.pdf` | Worked Solutions III: 40 more most-asked LeetCode problems (none in Parts I/II or the OA packs), each with idea, steps, tested C++17 code, traps and follow-ups; clickable index by pattern |
| `generated/worked-solutions-4.pdf` | Worked Solutions IV: 25 hard (L3) problems for product-company final rounds (wildcard matching, KMP, skyline, bitmask BFS, interval DP, merge-sort counting, trie search and more), none in Parts I–III or the OA packs; tested C++17 with -Wall -Wextra under ASan/UBSan |
| `generated/oa-simulation-packs.pdf` | 8 timed online-assessment sets (3 LeetCode problems, 90 minutes each, 24 problems with no repeats), dated to the plan, with a scoring guide, a record table and a solution page per set (sketch, edge cases, tested C++17) |
| `generated/core-cs-mcq-bank.pdf` | 150 OA-style MCQs (30 each on OS, DBMS, CN, OOP, C++ output) with answer keys on separate pages and a reason per answer; C++ outputs, SQL, subnet and page-fault answers machine-checked |
| `generated/core-cs-mcq-bank-2.pdf` | 150 more OA-style MCQs (30 each on OS, DBMS, CN, OOP, C++ output), none repeated from bank I, more numericals (SRTF, Round Robin, optimal paging, disk scheduling, closures, subnetting, delays) and design patterns; answer keys with reasons; 90 automated checks (every C++ output compiled and run) |
| `generated/sql-pack.pdf` | 40 interview SQL questions (basics, joins, aggregation, subqueries, window functions, indexing) on one sample database, each with the query, its real output and an explanation |
| `generated/sql-pack.sql` | The sample database and all 40 queries in one file: load it into SQLite or any SQL playground to practise |
| `generated/sql-pack-2.pdf` | SQL pack II: 30 harder questions (gaps and islands, sessions, running balances, medians, retention, funnels, recursive trees and calendars, pivots, mutual follows, overlapping bookings, dedup, keyset pagination) on one product-analytics database; every query's full output checked against an independent Python answer |
| `generated/sql-pack-2.sql` | The pack II database and all 30 queries as one script (sqlite3 practice2.db < sql-pack-2.sql) |
| `generated/aws-saa-c03-study-pack.pdf` | AWS SAA-C03 final revision: notes for the four domains, a service-for-need table, 60 original scenario questions with explained answers, and a day-by-day plan for 5–18 Apr 2027 |
| `generated/aws-lab-workbook.pdf` | AWS hands-on lab workbook: 10 labs for SAA-C03 (budget and MFA, IAM roles, S3 versioning, VPC, EC2 with IMDSv2, ALB with Auto Scaling, private RDS, Lambda with an HTTP API, CloudTrail root-login alarm, KMS) plus a teardown checklist; console steps, CLI commands checked against the AWS service models and the CLI's parser, cost notes and cleanup for each |
| `generated/tenantwall-helpers.pdf` | TenantWall: architecture diagram, method flowchart, IAM and bucket policies explained, alerting setup, isolation test plan and a checklist for the paper's audit and alerting section |
| `generated/tenantwall/` | The TenantWall files themselves: diagrams (SVG and PNG), policy JSON, CloudTrail and alarm setup script, and an offline policy check script |
| `generated/ai-security-starter-guide.pdf` | Guide to the AI-security project starter: how it works, the four defence layers, how to run it, offline results per attack, and a 4-week May plan |
| `generated/ai-security-starter/` | The starter itself: a RAG assistant over security notes, 20 evaluation questions, 12 prompt-injection attacks, defence module, 8 offline tests; one flag switches to Claude |
| `generated/backend-starter/` | Study-tracker REST API (FastAPI, SQLite, JWT login, rate limiting) with 10 security-focused tests, an architecture diagram and a security checklist in its README |
| `generated/lld-pack.pdf` | Six LLD designs (parking lot, library, Splitwise, elevator, rate limiter, LRU cache): requirements, class diagrams, decisions, follow-ups and full C++17 code |
| `generated/lld/` | The six C++17 programs; each runs a demo that checks its own behaviour |
| `generated/core-cs-one-pagers.pdf` | One A4 revision page each for OS, DBMS, CN, OOP, SQL and System Design: 10 definitions, a diagram and the 10 most-asked questions |
| `generated/patterns-stl-card.pdf` | One-page pattern decision tree (problem signal → pattern → Knowledge Base page), a C++ STL card with complexities, and 30 common C++ contest bugs with fixes |
| `generated/stl_check.cpp` | Compiles and runs every STL call on the card (proof the card is correct) |
| `generated/aptitude-pack.pdf` | 150 aptitude questions (60 quant, 50 logical, 40 verbal) with timing guidance and worked answers on separate pages; every computable answer checked in Python |
| `generated/aptitude-pack-2.pdf` | 90 more aptitude questions: 40 quant on new topics, 30 logical (incl. syllogisms, seating, cubes) and a new data-interpretation section (4 sets × 5); none repeated from pack I; every one of the 90 answers recomputed in Python |
| `generated/anki/*.csv` | 1,031 flashcards in 7 Anki decks (all 123 worked solutions, Core CS, patterns and C++ bugs, complexity, security, AWS, aptitude), built from material already checked in the kit |
| `generated/anki-decks-guide.pdf` | One page: importing the decks into AnkiDroid, AnkiMobile or Anki desktop, and a daily routine |
| `generated/security-lab-notebook.pdf` | CTF and PortSwigger write-up templates with worked examples, a STRIDE threat model of TenantWall, a lab command sheet, and web security by vulnerability class (linked to the free PortSwigger topics) |
| `generated/security-labs-workbook.pdf` | 6 hands-on security labs on your own machine (permissions and SUID, nmap on localhost, HTTP vs HTTPS packet capture, hashing and cracking test hashes, find and fix SQL injection and XSS in a Flask app, brute-force detection rule); legal note first; every command run and its output captured |
| `generated/security-labs/` | Code for the labs: vulnerable and fixed Flask apps, brute-force detector, cracking lab, CLI lab script, 7 pytest tests |
| `generated/soc-log-analysis-project.pdf` | logsentry, a SOC portfolio project: a standard-library Python tool that detects SSH brute force, success-after-failures (likely compromise), web scanning, scanner user agents and SQLi/XSS/traversal in real log formats, JSON alerts mapped to MITRE ATT&CK; 11 tests incl. false-positive and evasion cases; guide with limits and resume line |
| `generated/soc-log-analyzer/` | The logsentry code, sample logs and tests (python3 -m unittest test_logsentry) |
| `generated/weekly-planner.pdf` | 28 printable week pages (16 Nov 2026 – 30 May 2027): phase and goal, fixed dates (OA sets, TenantWall deadline, exams, AWS exam), daily tick boxes and a weekly review |
| `generated/weekly-revision-tests.pdf` | 34 Sunday self-tests (22 Nov 2026 – 25 Jul 2027, none in the exam break), 30 minutes each: 3 pattern questions from that week's A2Z topics (then mixed), 4 Core CS MCQs on a five-week rotation, 1 AWS and 1 security question; answers on the next page; nothing repeats; all drawn from checked kit material |
| `generated/company-files-2.pdf` | Six more company files (Uber, Salesforce AMTS, Adobe MTS-1, Walmart Global Tech, PhonePe, Zscaler): reported process, how the plan prepares you, mistakes, likely questions, sources |
| `generated/resume-kit.pdf` | One-page ATS-safe resume template (placeholders only), bullet formula with weak-to-strong examples for TenantWall, the AI-security and backend projects, where each number comes from, and a 12-point review checklist |
| `generated/resume/` | The template as Markdown and HTML, to paste into Google Docs or Word |
| `generated/interview-story-bank.pdf` | Six STAR story templates (prompts, no invented stories) mapped to Amazon's 16 Leadership Principles and Google's hiring attributes, a coverage matrix, a fill-in worksheet and 25 HR questions with answer outlines |
| `generated/profile-kit.pdf` | LinkedIn checklist, three headline options and an About template, GitHub pinning and project README guide, a profile README template, and a 4-week posting plan |
| `generated/profile/` | The LinkedIn text and the GitHub profile README as files to copy |
| `generated/docker-ci-guide.pdf` | One page: the Dockerfiles and GitHub Actions workflows added to both starters, explained line by line, with run commands |
| `generated/network-programming-project.pdf` | C++ network programming project: a poll()-based multi-client chat server and a minimal HTTP/1.1 server (code in generated/netproj/), 11 tests over real localhost sockets under ASan/UBSan, plus a guide to each syscall, TCP framing, HTTP basics, and the interview questions it prepares you for |
| `generated/netproj/` | chat_server.cpp, http_server.cpp and test_net.py (python3 test_net.py) |
| `generated/open-source-gsoc-guide.pdf` | Open source from first PR to GSoC/LFX: which programme fits (official rules: age, beginner status, project sizes, evaluations), a week-by-week plan from December to the March window, finding first issues, the fork–branch–rebase PR workflow (tested end to end), PR and message templates, proposal outline; 8 official sources |
| `generated/oss/` | git_workflow_check.sh: runs the guide's whole git workflow against local test repositories |
| `generated/system-design-case-studies.pdf` | Five designs (URL shortener, chat, news feed, notifications, file sync): requirements, computed estimates, API, data model, diagram, design and trade-offs |
| `generated/sysdesign/` | The five diagrams as SVG and PNG |
| `generated/elite-track-pack.pdf` | Elite (HFT) checkpoint pack: 40 probability questions with worked answers (all checked exactly, 27 also by simulation) and 8 low-latency C++ exercises with measured timings |
| `generated/elite/` | The 8 C++ exercises, the timing harness and a sample of measured timings |
| `generated/knowledge-base-v2.html` | The Knowledge Base with 213 pages: the original 167 plus the 40 Worked Solutions II problems and the 6 new company files, all searchable and linked. Open it in a browser |
| `generated/kb2/` | Sources for v2 (a copy of `sources/kb` plus the two new modules); rebuild with `python3 generated/src/kb2_build.py` |
| `generated/cyber-security-interview-bank.pdf` | 97 security interview questions with model answers in 8 sections (fundamentals, network, web, cryptography, identity and cloud, incident response and SOC, Linux/Windows/AD, scenarios); computable facts checked by script; official sources per section |
| `generated/owasp-portswigger-lab-map.pdf` | OWASP Top 10:2025 mapped to free PortSwigger Academy topics (tick boxes), what changed since 2021, a 10-week lab order and 10 web-security interview questions with answers |
| `generated/mock-interview-scripts.pdf` | Six mock interview scripts for practising with a friend (2 DSA, Core CS, LLD, security, HR): timed phases, what to say, hints in order, 5-line rubric |
| `generated/mock-interview-scripts-2.pdf` | Six more mock scripts (DP on strings, trees and grids, OS and networks deep dive, fresher system design, TenantWall grilling, security scenario round); DSA problems only from tested Worked Solutions II |
| `generated/linux-git-debugging-sheet.pdf` | Two pages of daily commands (files and text, processes, Git everyday and safe undo, C++ debugging with sanitizers, gdb, valgrind, strace), every one run and checked |
| `generated/codeforces-ladder.pdf` | Codeforces ladder 800 → 1600: 10 topics × 5 rating bands (links to the official filtered problem set), a 6-week plan to the 31 March gate, and how rating moves |
| `generated/interview-day-kit.pdf` | OA-day and interview-day checklists, what to say when stuck, four email templates (referral, thank-you, follow-up, more time) and how to compare offers, with a worked example |
| `generated/applications-outreach-kit.pdf` | Applications tracker (CSV with follow-up-date and funnel formulas, checked on example rows) plus five new outreach templates (LinkedIn note, recruiter email, alumnus advice, professor research email, status check; placeholders only) and a weekly 10-applications/5-messages routine |
| `generated/outreach/` | applications-tracker.csv (import into Google Sheets) and outreach-templates.md |
| `generated/interview-day/` | The email templates (Markdown) and an offer comparison sheet (CSV with formulas, opens in Google Sheets) |
| `generated/tenantwall-paper-outline.pdf` | TenantWall paper: what to write in each section, figures and tables, a 7-week writing plan to 21 March, submission checklist and references |
| `generated/tenantwall/paper/` | IEEE-format LaTeX skeleton (main.tex with prompts, refs.bib, compiled main.pdf); upload to Overleaf to write |
| `generated/oa-simulation-packs-2.pdf` | 8 more timed OA sets (9–16), 24 new problems not in the first pack or the worked solutions, dated Mar–Jul 2027, with scoring guide and tested solutions |
| `generated/oa-simulation-packs-3.pdf` | 8 more timed OA sets (17–24) for placement season, Saturdays 17 Jul – 4 Sep 2027, each with a company-style theme; 24 new problems not in OA packs I–II or Worked Solutions I–III; scoring guide, question and solution pages, tested C++17 |
| `generated/company-files-3.pdf` | Six more company files (Oracle, Cisco, Swiggy, Zomato/Eternal, CRED, CrowdStrike): reported process, preparation from the kit, mistakes, likely questions, sources |
| `generated/index-of-everything.pdf` | Every file in the repository with what it is, when to use it and a link that opens it on GitHub |
| `agent/` | Instructions, backlog and log for the scheduled agent |
| `generated/` | Documents the agent builds |

Revision tracker (Google Sheet, private to me): Log, Due today, Mocks, Stats and Settings tabs.

## Key dates

Striver core done 30 Jan 2027 (checkpoint 1) · semester exams 22 Mar – 7 Apr · HFT gate 31 Mar (Codeforces 1400+ or LeetCode contest 1800+) · AWS SAA-C03 week of 19 Apr · AI-security project May · placement sprint 31 May – 31 Jul · placements Aug – Dec 2027.

## Run it

Open `index.html` in a browser. Progress in the offline pages is stored in that browser; back it up from the Playbook, Part 09. To install on a phone, host the folder (for example GitHub Pages: Settings → Pages → this branch, root) and use "Add to Home screen".
