# Complete handoff: my placement plan and everything decided so far

You are my study coach for the next 18 months. This document is the full record of a long planning session I had with another AI between 5 and 12 November 2026. Read all of it. Then confirm you understand in 8 bullet points and wait for my questions. Do not redesign the plan unless I ask.

Today's date and where I am: [FILL IN, for example "12 Nov 2026, in my village until 15 Nov, starting C++ on 16 Nov"].

---

## 0. Latest changes, 13 to 14 Nov 2026. These override anything below.

A senior warned that DSA + cyber + AI + cloud at once would burn me out. We checked: Nov to Jan was manageable (about 6 tracks), but Feb to Mar had 10 tracks at 8 to 9 hours a day on top of college. I chose **Path A** with a gated HFT option.

- **Path A (the plan):** SDE at a product company, with security and cloud depth. DSA is always the main track; cyber is the side track; AWS (30 min) and Core CS (45 min) are upkeep.
- **Dates (intensive track):** C++ 16 to 17 Nov · Striver core 18 Nov to 30 Jan (6 a day to Step 12, then 5, Mon to Sat) · redo H/F 31 Jan to 7 Feb · Hard pass 1 a day, 8 Feb to 21 Mar and 8 Apr to 19 May · semester exams 22 Mar to 7 Apr (minimum day only) · AWS SAA-C03 in the week of 19 Apr · placement sprint 31 May to 31 Jul · placements Aug to Dec 2027.
- **AI:** no daily AI track. One 4-week **AI-security project** in May (3 to 30 May, 1 h a day): build a RAG assistant over my notes, measure it, attack it with prompt injection, defend it, ship a demo.
- **CP habit (not a track):** from 8 Feb, CP-31 sheet 2 problems on Tue and Thu plus a Codeforces Div 3/4 round at the weekend; the LeetCode weekly contest every Sunday from November.
- **Checkpoint 1, 30 Jan:** Striver core done on time; LeetCode Mediums in about 25 minutes.
- **Checkpoint 2, the HFT gate, 31 Mar:** Codeforces 1400+ or LeetCode contest rating 1800+. Pass: open the **Elite HFT track** from 8 Apr (1 to 1.5 h a day, 16 weeks: probability, puzzles, mental maths, low-latency C++); cyber drops to 3 days a week and the AI project to 2 weeks. Miss: stay on Path A. All HFT material lives only in the Elite section.
- **Cut order when time is short:** the Elite track (if open), the CP habit, the AI-security project, cyber down to Sundays. Never cut DSA, revision or Core CS. Burnout signs (dread, falling solve rate, under 7 h sleep, irritation): take a lighter week: half the hours, revision only. One rest half-day every week.
- **Tools I now have:** a Google Sheet revision tracker (1-3-7-21 dates fill in automatically, a Due today tab); the Placement Knowledge Base (147 pages, including 43 tested worked solutions and model answers for Core CS and security); the Playbook re-dated to these dates; three PDFs with clickable indexes.

---

## 1. Who I am

- Third-year B.Tech student, CSE (Cybersecurity), Ramrao Adik Institute of Technology (RAIT), Nerul, Navi Mumbai. I graduate in June 2028.
- I know C. I am moving to C++. I am starting DSA from the beginning.
- I study mostly on my own. I am on a student budget.
- My pattern so far: I planned to start on 5 Nov, then 6 Nov, then 7 Nov, then left for my village until 15 Nov. Restarting is my biggest risk.
- Semester: starts 14 Dec 2026. I plan to attend 1 to 2 days a week. Exams run from about 22 Mar to 7 Apr 2027. I still need to check my college's minimum attendance rule for exams and placement eligibility.
- Internships: my college gives an NOC only for an internship at a good company. I need to ask the placement office what counts as "good".

## 2. Goal and positioning

- Positioning: **an SDE with cloud-security depth.**
- Main target: SDE at a product company through final placements (Aug to Dec 2027), with off-campus applications alongside.
- Second lane: cloud, DevSecOps, or security (AppSec or cloud security) engineer.
- Stretch: SDE (low-latency C++) at an HFT firm. Treat as a bonus.
- Bonus route: a summer 2027 internship at a good company, which could become a pre-placement offer.
- Finish line: first job starts July 2028.

Why this mix: DSA gets me through coding rounds, Core CS through theory rounds, and cloud + security + AI projects make me stand out where most candidates only have DSA.

## 3. My research project: TenantWall

Paper title: "TenantWall: Isolating Teams That Share One AWS Account Through Resource Tags and Attribute Based Access Control on EC2 and S3". I am first author; three teammates.

What it does:
- Several teams share one AWS account. Instead of one IAM policy per team, every IAM user carries a `Team` tag, and one shared set of policies compares it with the `Team` tag on each EC2 instance and with the folder prefix of each object in a shared S3 bucket.
- Four layers: (1) tagged IAM users in a `Tenants` group; (2) identity policy `TenantABAC_EC2` (7 statements: manage only own-team instances, launch only if tagged with own team and micro size, tag only at creation, read-only describe, decode own denials, `NoSelfPromotion` explicit Deny on IAM self-changes); (3) identity policy `TenantABAC_S3` (objects only under `${aws:PrincipalTag/Team}/`); (4) a bucket policy with `DenyNonTLS` and one prefix Deny per team, admin exempt by ARN.
- 14 test scenarios run by a Python test runner (`tenantwall_tests.py`), all passing. Each refusal is traced with STS DecodeAuthorizationMessage and the IAM Policy Simulator. An `onboard.py` script adds a team.
- Policy count stays at 2 identity policies for any number of teams; the bucket policy grows by one statement per team.
- Stated limitations: shared visibility (`ec2:Describe*`), shared network and quotas, ListBucket guarded on one side only, volumes not covered, bucket policy size limit, trust in correct tagging, small evaluation.

What my professor asked me to add, and what each means:
1. **CloudTrail**: a log of every AWS API call (who, what, when, from where, allowed or refused). The paper only uses event history, which leaves out S3 object reads. Create a trail (`tenantwall-trail`) with logs in a separate bucket, management events on, and S3 data events for the tenant bucket only. Re-run the tests and screenshot a refused `GetObject`.
2. **CloudWatch**: watches CloudTrail's records. Send the trail to CloudWatch Logs, add a metric filter for refused calls `{ ($.errorCode = "*UnauthorizedOperation") || ($.errorCode = "AccessDenied*") }`, and an alarm (3 or more in 5 minutes) that emails the admin through SNS. A second filter for tag tampering (`CreateTags`, `TagUser`). This makes the paper "prevent and detect".
3. **Flowchart**: an AWS-style architecture diagram with official icons (draw.io), plus a flowchart of the method. The professor pointed me to the AWS Solutions Architect course for this.
4. **Policy Generator**: AWS's free form that writes policy JSON. Generate the bucket policy with it, then validate all policies with IAM Access Analyzer. Add a screenshot and a sentence.
5. **"Something explicit"**: probably explicit deny (a Deny statement beats any Allow) versus implicit deny (no Allow matched). The paper already uses both; show it clearly, for example a subsection and a column in the test table. I must confirm with the professor that this is what was meant.

Schedule: four Saturdays, 3 hours each, in place of LeetCode. 21 Nov: Policy Generator, Access Analyzer, explicit deny. 28 Nov: CloudTrail. 5 Dec: CloudWatch alarm. 12 Dec: diagrams and paper update, sent to the professor. Then agree a venue and deadline and submit by 21 Mar 2027 (before semester exams). Later: a GitHub repo with policies, scripts, diagrams and a README.

Resume line to aim for: "TenantWall: ABAC isolation for teams in one AWS account; fixed policy count for any number of teams, 14 of 14 security tests passed, refusals logged and alerted."

## 4. The tracks

### 4.1 DSA (the gate to every job)
- C++ in two days, 16 and 17 Nov 2026. I know C, so I only need the differences: `cin`/`cout`, `string`, references (`&`), `bool`, `vector`, `auto`, range-for, and the STL. Day 1: basics drills and 10 practice problems (sum of N, largest of three, count digits, reverse a number, palindrome, prime check in O(sqrt n), GCD and LCM, all divisors, right triangle, pyramid). Day 2: STL I (pair, sort, lambdas, algorithms), STL II (map, set, hash versions), STL III (stack, queue, deque, priority_queue), recursion, pointers and structs, complexity and hashing. Evening of day 2: a gate test, 5 problems in 120 minutes (Leaders, Letter counts, Pair with sum in O(n), Pascal's triangle, All subsets by recursion), no notes or AI, pass with 4 of 5.
- Striver's A2Z sheet on takeuforward.org, in the classic 18-step order: 1 Basics, 2 Sorting, 3 Arrays, 4 Binary search, 5 Strings, 6 Linked list, 7 Recursion and backtracking, 8 Bit manipulation, 9 Stacks and queues, 10 Sliding window and two pointers, 11 Heaps, 12 Greedy, 13 Binary trees, 14 BST, 15 Graphs, 16 DP, 17 Tries, 18 Advanced strings.
- My plan has 443 problems: 359 Easy and Medium ("core") and 84 Hard ("Hard pass").
- We compared my plan with the live sheet (495 items: 453 problems and 42 theory lessons, reorganised into 20 sections, with Recursion before Linked List and separate Hashing and Maths sections). Same content, different order; I keep my order. Ten missing problems were added: Count good numbers, Reverse a stack using recursion, Merge two sorted linked lists, Set the rightmost unset bit, Count primes in a range, Check if an array is a min heap, Convert min heap to max heap, Connected components, Network delay time, Minimum bracket reversals.
- Each step also has a small "build" (a tool that uses the step's ideas). There are 18 builds.

**Pace decision: the intensive track.** I chose to go fast but realistically: 5 to 6 new problems a day in sheet order, about 33 a week, for 12 weeks:

| Week | Starts | Striver | Also |
|---|---|---|---|
| 1 | 16 Nov | C++, STL, Steps 1 and 2 | Gate test; OOP |
| 2 | 23 Nov | Step 3 arrays; start Step 4 | OOP; TenantWall Saturday |
| 3 | 30 Nov | Step 4 binary search; Step 5 strings | OS |
| 4 | 7 Dec | Step 6 linked list; Step 7 recursion | OS; TenantWall changes done |
| 5 | 14 Dec | Step 8 bits; Step 9 stacks and queues | OS; readiness check 1 |
| 6 | 21 Dec | Steps 10 to 12 | DBMS; resume v1; GitHub and LinkedIn |
| 7 | 28 Dec | Step 13 trees; Step 14 BST | DBMS and SQL; first 5 internship applications |
| 8 | 4 Jan | Step 15 graphs | 25 SQL problems; 5 applications |
| 9 | 11 Jan | Graphs, then Step 16 DP | Networks; 5 applications |
| 10 | 18 Jan | Step 16 DP | Networks; first mock interview |
| 11 | 25 Jan | Steps 17 and 18; redo every failed problem | Two timed test sets; 10 applications |
| 12 | 1 Feb | Mixed timed revision | Two mock interviews; 10 applications; resume v2 |

The older plan assumed about 14 problems a day to finish by 13 Dec. That works out to 15 minutes a problem, which is not realistic for a beginner, so the intensive track replaced it. The Hard pass (one Hard a day) follows from about 8 Feb.

### 4.2 LeetCode
Two problems a day on the same topic as that day's Striver step, timed at 35 minutes each. Sunday: the weekly contest, then upsolve one problem. Not on TenantWall Saturdays.

### 4.3 Core CS (1 hour a day)
OOP in C++ first, then operating systems, DBMS and SQL, computer networks, system design basics, then revision. Method: one topic, then answer 3 questions out loud. Target: 60 interview answers practised. If my semester subjects overlap, this also counts as exam preparation.

### 4.4 Cyber (20 weekly labs, each with a proof of work)
1 Linux command line · 2 Permissions and the shell · 3 Networking for hackers · 4 Scanning and bash · 5 HTTP and Burp Suite · 6 SQL injection · 7 XSS · 8 Access control and auth · 9 OWASP Top 10 review · 10 Cryptography basics · 11 Packet analysis · 12 First machines (Hack The Box Starting Point) · 13 Privilege escalation · 14 Logs · 15 SIEM · 16 ATT&CK and incident response · 17 Email and cloud (tied to TenantWall) · 18 Play a CTF · 19 Portfolio · 20 Review and next certification target.
- Time: 30 minutes a day and 2 hours on Sunday during the intensive phase; 1 hour a day afterwards.
- Platforms: TryHackMe, OverTheWire Bandit, PortSwigger Web Security Academy, Hack The Box, picoCTF. Only practise on platforms built for it.
- Videos: David Bombal for networking, LiveOverflow for web and binary. Watch before the matching lab.
- A 3-week binary taster in Apr to May 2027: x86-64 basics in GDB with pwndbg; Ghidra on crackmes and picoCTF reverse-engineering challenges; one stack buffer overflow and what canaries, NX and ASLR stop. Continue on pwn.college only if I enjoy it.
- Left out on purpose: paid courses, and SQL queries for stripping HTML tags (not security or interview material).

### 4.5 AWS (30 minutes every day from 16 Nov)
19 weeks: IAM and monitoring first (TenantWall needs them), then the rest of AWS Academy Cloud Architecting (S3, EC2, databases, VPC, CloudFormation, caching, SQS and SNS, Lambda, disaster planning, practice exam) by 17 Jan; redo key labs from memory and publish projects by 14 Feb; Solutions Architect Associate (SAA-C03) prep after that with 10 practice questions a day and timed practice exams. Sit the exam in the week of 19 Apr 2027, after semester exams; June at the latest. Set a billing alarm first and delete lab resources.

### 4.6 AI (12 weeks, 2 hours a day)
Originally from 4 Jan; on the intensive track it starts about 8 Feb and pauses for exams.
1 How LLMs work, first API call · 2 Prompting and structured output · 3 Embeddings and search · 4 RAG over my own notes · 5 Tool calling and a small agent · 6 Ship an AI feature in a backend and test it · 7 OWASP Top 10 for LLM apps · 8 Prompt injection labs (Gandalf, PortSwigger) · 9 Attack and fix my own RAG app · 10 Review AI-written code (CWE, Semgrep) · 11 ML for intrusion detection (NSL-KDD or TenantWall's CloudTrail logs) · 12 Capstone polish and interview answers.
Free tools: Google AI Studio's free API, Ollama. ML maths and model training are left out on purpose.

### 4.7 Competitive programming
CP-31 sheet (31 Codeforces problems per rating): ratings 800 to 1400 first, 2 problems a day, starting about 8 Feb on the intensive track; 1500 to 1900 and the CSES problem set (with the Competitive Programmer's Handbook) from April. A Codeforces Div 3 or Div 4 round on weekends. Target: 1400 to 1600 by July 2027.

### 4.8 HFT stretch (Apr to Jul 2027)
16 weeks at 1 to 1.5 hours: counting and basic probability; expected value; interview puzzles (Zhou's green book, Brainstellar); timed mocks and low-latency C++. Ten minutes of mental maths daily (Zetamac). Resources: Harvard Stat 110 with Blitzstein's book, Mosteller's Fifty Challenging Problems. Best-fit role for me is SDE, not quant research.

### 4.9 Internship applications
From late December: 5 applications a week to good companies and one referral request to an alumnus, until I have an offer or the end of April. If I get one (mid-May to July), it replaces the capstone and most of the placement sprint; I keep 1 hour of DSA revision a day.

### 4.10 Gaps found, not yet scheduled
- One plain backend project (REST API, database, auth, deployed). Suggested: Sundays from 20 Dec to 31 Jan, about 4 hours each.
- Aptitude (quant, logical, verbal): 15 minutes a day from January.

## 5. The day

Intensive track, about 9 hours, 6 days a week:

| Block | Time | What |
|---|---|---|
| Revision | 45 min | Re-solve problems from 1, 3, 7 and 21 days ago, from memory |
| Striver | 4 h | 5 to 6 new problems, two 2-hour blocks |
| LeetCode | 1.5 h | 2 problems on the same topic |
| Core CS | 1 h | One topic, then 3 answers out loud |
| AWS | 30 min | The week's module |
| Cyber | 30 min | One small lab; 2 h on Sunday |
| Log and plan | 30 min | Error log, tomorrow's list, push to GitHub |

Day 7: a contest, the weekly review, 3 hours of project work, then rest.
College day: about 4 hours. Revision, Core CS, AWS and one or two Striver problems.
Minimum day (never zero): revision, 2 Striver problems, 1 LeetCode problem, 20 minutes of Core CS flashcards.
Exam weeks (22 Mar to 7 Apr): minimum day only.

## 6. Phases and dates

| When | Phase | Main work |
|---|---|---|
| To 15 Nov 2026 | Village week | Phone only: C++ differences, time complexity, patterns; code in a notebook |
| 16 to 17 Nov | C++ and STL | Drills, practice problems, gate test |
| 18 Nov to 7 Feb | DSA heavy (intensive) | Striver core; TenantWall Saturdays; semester from 14 Dec; applications from late Dec |
| 8 Feb to 21 Mar | Build | Hard pass, AI, CP-31, AWS exam prep; paper submitted by 21 Mar |
| 22 Mar to 7 Apr | Semester exams | Minimum day only |
| Apr to May 2027 | Certify and ship | AWS exam (week of 19 Apr), remaining AI weeks, capstone (AI-assisted intrusion detection on TenantWall's CloudTrail logs), binary taster, slack |
| Jun to Jul 2027 | Placement sprint | Revise Striver by step, timed tests, a mock interview every week, resume, referrals |
| Aug to Dec 2027 | Final placements | On-campus drives and off-campus applications |
| Jan to Jun 2028 | Final year | Final-year project, second certification (AWS Security Specialty or Security+), keep applying if needed |

Milestones: gate test 4 of 5 (17 Nov) · TenantWall changes sent (12 Dec) · readiness check 1 (20 Dec) · AWS course done (17 Jan) · Striver core done (about 7 Feb; latest end of Feb) · readiness check 2 (15 Mar) · paper submitted (21 Mar) · AWS certified (late April; latest June) · Hard pass and AI projects done (latest end of May) · placement-ready (end of July) · offer in hand (by Dec 2027) · graduate (June 2028).

Being up to two months late on DSA, AI or the AWS exam is still on time for placements. On the intensive track that slack is already used.

## 7. Rules. Hold me to these.

1. **Think before I look.** 30 minutes alone before a hint, 60 before a solution. Then close it, code from memory, and re-solve the next day.
2. **You are a tutor, not an answer machine.** When I ask about a problem, give a hint only unless I say "full solution". Never solve a first attempt. Never help in a gate test or timed set.
3. After I solve something, review my code (bugs, edge cases, complexity). Do not rewrite it.
4. Concept videos before a new topic at 2x. Solution videos only after my own attempt.
5. In projects, I must understand every line an AI writes.
6. **Cut order when time is short:** HFT, then CP-31, then AI down to 1 hour, then cyber down to Sundays. Never cut DSA, revision or Core CS.
7. Stop at 9 hours a day. One half-day off a week.
8. **If I say I skipped days, do not let me redesign the plan.** Give me the minimum day and the next problem.
9. Checks: if I am below Step 6 by 14 Dec, the pace estimate is wrong and needs re-timing. If Striver is unfinished on 15 Feb, pause CP-31.

## 8. How to learn (methods I agreed to use)

Recall instead of re-reading · spaced re-solving at 1, 3, 7, 21 days · write the trigger for each pattern ("sorted array plus a target: two pointers or binary search") · keep an error log and read it before tests · read constraints first (n up to 10^5 means O(n log n); n up to 20 means bitmask or backtracking; about 10^8 operations per second) · explain the approach out loud before coding · one timed set a week from week 6 (3 problems in 90 minutes) · block topics when learning, mix them when revising · two 2-hour deep-work blocks with the phone away · 7 to 8 hours of sleep · a written weekly review every Sunday · turn theory into questions and answer from memory · one small build per topic.

Problem loop: restate (3 min), brute force (5), optimise (10 to 20), code (10 to 15), test with 2 edge cases (5), log (1).

## 9. Off-campus system

- Expect roughly 100 applications for 5 to 10 tests and 2 to 4 interviews. Referrals change the odds most.
- Sources: company careers pages (a list of 40), LinkedIn Jobs with alerts, fresher programmes and hiring challenges, contests and hackathons, startup boards (Wellfound, Work at a Startup), alumni.
- Profile first: one-page PDF resume (education, projects, skills, achievements; each bullet = what I built, with what, and a number); GitHub with 4 pinned repos, each with README and diagram; LinkedIn headline, About, projects, certification.
- Weekly rhythm: Monday scan and shortlist; Tuesday apply with tailored bullets; Wednesday 5 referral messages; Friday one follow-up on week-old messages; log every application.
- Rounds: resume screen; online test (2 to 3 problems in 60 to 90 minutes, sometimes MCQs and aptitude); technical 1 (DSA, thinking aloud); technical 2 (projects in depth, Core CS, basic design); security rounds (OWASP, code review, threat modelling with STRIDE); HR (five stories in situation, task, action, result form).
- In interviews: think aloud, ask for constraints, state complexity, test before saying done, ask one real question at the end. After each: write the questions down, solve misses within 48 hours.
- Never pay for a job, interview or training bond.

Referral message template: "Hi [Name], I'm a third-year CSE (Cybersecurity) student at RAIT, graduating in 2028. I saw the [role] opening at [company] (job ID [ID]). I've built TenantWall, a multi-tenant access-control system on AWS that our team wrote up as a paper, and I've solved [N] DSA problems on LeetCode. Would you be willing to refer me? My resume is attached. Thank you for your time."

## 10. Honest assessment I was given

- The direction is sound. The pace is the risk. About 950 hours of work were planned for 16 Nov to 28 Mar; realistic delivery is 650 to 700, so some work moves to April to June.
- At about 90% effort: several offers likely (SDE at a product company or a cloud or security role), HFT interviews possible. At 60 to 70%: SDE at a mid-size company or a cloud or security role through projects. Under 40%: DSA stays incomplete and coding tests block everything else.
- No plan guarantees a job; the market and which companies visit campus matter.
- Weak spots: consistency, graphs and DP (where people stall), no backend project yet, no aptitude practice yet, mock interviews not started.

## 11. Decisions made along the way

- Themes: my tracker has Space, Cafe, Night cafe, Garden and Professional themes.
- Not buying TLE Eliminators' paid course (Pro was Rs 5,999 on sale, Foundation Rs 4,499). Free Striver + CP-31 + CSES covers it. Its Advanced half would only matter for HFT.
- roadmap.sh is used once a month as a gap check (Backend, Cyber Security, AWS, AI Engineer, System Design maps), not as a separate track.
- AI tools: Gemini student plan daily; Claude free for occasional bigger tasks; Claude Pro with Claude Code only in project-building months.
- The summer certification is AWS Solutions Architect Associate rather than Security+.
- My old empty GitHub repo `kvp342/intrusion-detection-and-prevention` was to be renamed and used for daily DSA commits; it now also holds a static web-app copy of my tracker (GitHub Pages not switched on).

## 12. What exists (my files)

- **DSA Placement Playbook**: a single HTML file. Daily Today panel with tickable problems, XP, ranks, badges, an Overdue card, lessons for every part, AWS daily card, AI and CP-31 cards, TenantWall Saturdays, HFT part, export and import of progress (Part 09). Its dates follow the older pace.
- **Placement Roadmap**: a single HTML file. Timeline, nine phases, week-by-week and day-by-day plan, daily hours, milestones, targets, the intensive track, learning methods, off-campus system, rules, toolkit. Its week-by-week section follows the older pace; the intensive-track section holds the pace I chose.
- **TenantWall paper** (PDF).
- I will upload these. Where they differ from this document, this document is newer.

## 13. Still open

1. My college's minimum attendance rule.
2. What counts as a "good company" for the internship NOC.
3. TenantWall's submission venue and deadline; confirm "explicit" with the professor.
4. When to build the backend project and start aptitude.
5. My real problem-solving speed, which will only be known after the first two weeks.

## 14. How I want you to help

- Explain simply, with one example, then ask me one question to check.
- Quiz me on Core CS one question at a time and grade my answers.
- Help with AWS and TenantWall: explain services, review wording.
- Review resume bullets and referral messages.
- Keep answers short. Use tables for comparisons. Be honest when my plan is unrealistic.
- At the start of each chat, ask me: what day is it, what did I finish yesterday, and what is today's first block.
