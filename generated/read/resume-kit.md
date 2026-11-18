PLACEMENTS · RESUME KIT

# Resume kit one page, ATS-safe, honest numbers

A one-page template with placeholders (fill it in Google Docs or Word from `generated/resume/resume-template.md` or `.html`), a formula for strong bullets with examples for TenantWall, the AI-security project and the backend project, and a checklist to run before every application.

**The rule.** Every number on your resume must be real and you must be able to explain how you measured it. The examples use \[brackets\] where your measured value goes.

|                                             |
|---------------------------------------------|
| [One-page template (placeholders)](#your-name) |
| [Writing bullets](#writing-bullets)                  |
| [Review checklist](#review-checklist)                |

# YOUR NAME

City, India · your.email@example.com · +91 XXXXX XXXXX · linkedin.com/in/your-handle · github.com/your-handle

## Education

**B.Tech, Computer Science and Engineering (Cyber Security)**2024 – 2028

Your College, City

- CGPA: X.XX / 10 (only if 7.5 or above; otherwise leave it out)
- Relevant courses: Data Structures, Operating Systems, DBMS, Computer Networks, Cryptography

## Projects

**TenantWall: tenant isolation on AWS with ABAC**Dec 2026 – Mar 2027

Research project with Prof. \[Name\] · github.com/your-handle/tenantwall

- Designed attribute-based access control for a shared S3 bucket and EC2 fleet so each tenant reaches only its own resources, using tag-matched IAM policies and explicit denies; validated with IAM Access Analyzer (0 findings)
- Verified isolation with 14 scenarios on real AWS (10 refusals, each classified as explicit or implicit deny) and built CloudTrail → CloudWatch → SNS alerting that emailed on refused calls within 3 minutes
- Paper \[submitted to / accepted at\] \[venue\], \[month year\]

**Secure RAG assistant with prompt-injection defences**May 2027

Python, Claude API · github.com/your-handle/secrag

- Built a retrieval-augmented assistant over security notes with four defence layers (input scanning, document sanitising, prompt separation, output checks)
- Cut attack success rate from \[A\]% to \[B\]% on \[N\] held-out prompt-injection attacks while blocking \[C\]% of \[M\] normal questions, measured with an evaluation harness

**Study tracker REST API**Jan 2027

Python, FastAPI, SQLite, JWT · github.com/your-handle/study-tracker

- Built a REST API with JWT login, scrypt password hashing, per-user authorisation on every query and login rate limiting
- Wrote \[N\] tests covering forged and expired tokens, cross-user access and SQL injection; ran them in GitHub Actions on every push

## Skills

Languages: C++ (STL), Python, SQL, Bash

Cloud and security: AWS (IAM, S3, EC2, CloudTrail, CloudWatch), OWASP Top 10, Burp Suite, Linux

Tools: Git, Docker, FastAPI, Linux

## Achievements

- AWS Certified Solutions Architect – Associate (SAA-C03), \[month year\]
- Solved \[N\]+ DSA problems (LeetCode: \[handle\]); Codeforces rating \[R\] (\[handle\])
- \[CTF or hackathon result, with rank and number of teams\]

## Writing bullets

### Formula

|              |                                                                |
|--------------|----------------------------------------------------------------|
| Action verb  | Built, designed, reduced, automated, tested, led               |
| What you did | the technical work, in plain words                             |
| How          | the tools or method that matter for the job                    |
| Result       | a measured number, or a concrete outcome if you cannot measure |

### Weak → strong

| Weak                                  | Strong                                                                                                                                                       |
|---------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Worked on AWS security for a project. | Designed attribute-based access control for a shared S3 bucket so each tenant reaches only its own data, using tag-matched IAM policies and explicit denies. |
| Made a chatbot using AI.              | Built a retrieval-augmented assistant with four prompt-injection defences and cut attack success rate from \[A\]% to \[B\]% on \[N\] held-out attacks.       |
| Created a backend app with login.     | Built a FastAPI service with JWT login, per-user authorisation and rate limiting, covered by \[N\] security tests run in CI on every push.                   |
| Good at DSA.                          | Solved \[N\]+ problems on LeetCode and Codeforces; rated \[R\] on Codeforces.                                                                                |

### Where your numbers come from

|                     |                                                                                                                                                         |
|---------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------|
| TenantWall          | number of isolation tests and how many were denied (the test plan in the TenantWall helpers); alert delay measured over several trials                  |
| AI-security project | attack success rate before and after defences, false-block rate and answer quality, from the starter's run_attacks.py and run_eval.py with a real model |
| Backend project     | number of tests; requests per second and p95 latency if you load-test it (one of the README's extension ideas)                                          |
| DSA and contests    | problems solved and contest rating, from your profiles on the day you apply                                                                             |

Order projects by relevance to the role: for SDE roles put the backend project or TenantWall first; for security roles, TenantWall and the AI-security project. See the [resume](knowledge-base/career.md#the-one-page-resume) Knowledge Base page.

## Review checklist

|     |                                                                                                                                           |
|-----|-------------------------------------------------------------------------------------------------------------------------------------------|
| ☐   | One page. Single column, no tables, text boxes, icons, photos or skill bars: resume filters (ATS) read text top to bottom.                |
| ☐   | File: PDF exported from Google Docs, Word or LaTeX, named Firstname-Lastname-Resume.pdf. Check that you can select and copy all the text. |
| ☐   | Standard headings: Education, Experience (if any), Projects, Skills, Achievements.                                                        |
| ☐   | Every bullet starts with an action verb and has a result; no 'responsible for' or 'worked on'.                                            |
| ☐   | Every number is real and you can explain how you measured it. Leave a bullet without a number rather than invent one.                     |
| ☐   | Every skill listed appears in a project or you can answer three questions on it.                                                          |
| ☐   | GitHub links work, repositories have a README with results, and no keys or secrets are committed.                                         |
| ☐   | Match the job post: reorder skills and projects so the most relevant come first; use the post's exact words where true.                   |
| ☐   | Consistent dates, tense (past for finished work) and punctuation; no spelling mistakes (read it aloud once).                              |
| ☐   | No personal details beyond city, email, phone and links (no photo, date of birth or address).                                             |
| ☐   | Ask a senior or a mentor to read it for 30 seconds and tell you what they remember; that is what a recruiter sees.                        |
| ☐   | Keep a master version with everything, and a tailored copy per company.                                                                   |
