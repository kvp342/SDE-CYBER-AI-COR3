PLACEMENTS · PROFILE KIT

# Profile kit LinkedIn, GitHub, a 4-week plan

Recruiters and interviewers look at your LinkedIn and GitHub before they talk to you. This kit gives you templates (placeholders only), what to pin and how to describe projects, and a four-week plan to make the profiles active. Copy the text from `generated/profile/linkedin.md` and `generated/profile/github-profile-README.md`.

|                                        |
|----------------------------------------|
| [LinkedIn](#linkedin)                    |
| [GitHub profile and projects](#github-profile-and-projects) |
| [4-week posting plan](#4-week-posting-plan)         |

## LinkedIn

### Checklist

- Photo: clear face, plain background. Banner: optional; a simple one with your focus area is enough.
- Headline: what you are, what you build, one proof point. Stay under 220 characters.
- About: first two lines are shown before 'see more', so put your focus and best project there.
- Featured: add the TenantWall diagram, the paper (when public) and the project repositories.
- Experience and projects: the same bullets as your resume, with links.
- Skills: 10 to 15 real ones; put the five most relevant at the top.
- Open to work: set it to recruiters only if you prefer; list the roles and cities you want.

### Headline options

|                                                                                                                                                  |           |
|--------------------------------------------------------------------------------------------------------------------------------------------------|-----------|
| CSE (Cyber Security) student, class of 2028 \| C++, DSA, AWS \| Building secure cloud and backend systems \| TenantWall: tenant isolation on AWS | 141 / 220 |
| Aspiring SDE \| Cloud security research (AWS IAM, ABAC) \| C++ · Python · FastAPI \| Open to SDE and security internships                        | 118 / 220 |
| B.Tech CSE (Cyber Security) '28 \| Prompt-injection defences for RAG \| Backend APIs \| AWS Solutions Architect – Associate \[after you pass\]   | 137 / 220 |

### About template (989 of 2,600 characters)

``` text
I'm a third-year B.Tech student in Computer Science (Cyber Security) who likes building systems that are correct and hard to break.

What I'm working on:
• TenantWall: research on tenant isolation in AWS using attribute-based access control, with CloudTrail and CloudWatch alerting on denied access. [one result, e.g. N cross-tenant tests, all denied]
• A RAG assistant with layered prompt-injection defences, measured on held-out attacks. [attack success rate before → after]
• A study-tracker REST API (FastAPI, JWT, tests in CI). [link]

Skills: C++ (STL), Python, SQL, AWS (IAM, S3, EC2, CloudTrail), FastAPI, Linux, Git, OWASP Top 10.

I practise DSA daily ([N]+ problems; Codeforces [rating]) and write up CTF and PortSwigger labs on GitHub.

Looking for: software engineering and security internships and new-grad roles from [month year]. Happy to talk about cloud security, backend systems or competitive programming.

GitHub: github.com/your-handle · Email: your.email@example.com
```

## GitHub profile and projects

|                         |                                                                                                                                                         |
|-------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------|
| Pin 4 to 6 repositories | GitHub lets you pin up to six. Pin your best three projects first, then write-ups and a DSA solutions repo.                                             |
| Profile README          | Create a public repository with exactly your username as its name; its README.md appears at the top of your profile.                                    |
| Each project README     | First screen: one sentence on what it does, a screenshot or diagram, how to run it in three commands, results with numbers, and what you would do next. |
| Repository description  | One line under 100 characters with the main technology: 'Tenant isolation on AWS using ABAC IAM policies and CloudTrail alerting'.                      |
| Topics                  | Add 3 to 5 topics (aws, iam, security, fastapi, cpp) so recruiters' searches find the repository.                                                       |
| Hygiene                 | No keys or .env files committed (add a .gitignore first); delete empty or tutorial repositories or make them private; commit regularly in small steps.  |

### Profile README template

``` text
# Hi, I'm [Your Name]

B.Tech CSE (Cyber Security), class of 2028. I build secure backend and cloud systems and practise DSA in C++.

### Projects
| Project | What it is | Stack |
|---|---|---|
| [TenantWall](https://github.com/your-handle/tenantwall) | Tenant isolation on AWS with ABAC, plus alerting on denied access | AWS IAM, S3, EC2, CloudTrail, CloudWatch |
| [secrag](https://github.com/your-handle/secrag) | RAG assistant with layered prompt-injection defences and an attack suite | Python, Claude API |
| [study-tracker](https://github.com/your-handle/study-tracker) | REST API with JWT, per-user authorisation and security tests in CI | FastAPI, SQLite, GitHub Actions |

### Now
- Solving [N]+ DSA problems; Codeforces: [handle]
- Preparing for AWS Solutions Architect – Associate
- Writing up PortSwigger and CTF labs in [security-notes](https://github.com/your-handle/security-notes)

### Contact
[LinkedIn](https://linkedin.com/in/your-handle) · your.email@example.com
```

## 4-week posting plan

Start any time; a good moment is after the first TenantWall results (January) or the AWS exam (April). About 30 minutes a week.

### Week 1: Set up

- [ ] Update photo, headline, About, skills and links (templates on the next pages)
- [ ] Create the GitHub profile README and pin repositories
- [ ] Connect with classmates, seniors and alumni at your target companies (with a one-line note)

### Week 2: Show work

- [ ] Post 1: what TenantWall is and why tenant isolation matters, with the architecture diagram
- [ ] Comment thoughtfully on 3 posts from engineers in your area
- [ ] Push one PortSwigger or CTF write-up to GitHub

### Week 3: Teach something

- [ ] Post 2: one thing you learned (for example how IAM evaluates an explicit deny) in 5 short lines
- [ ] Ask two seniors for 15-minute calls about their teams' hiring
- [ ] Add a README with results to your backend project

### Week 4: Result and ask

- [ ] Post 3: a result (an attack success rate, a contest rating, a passed certification) and what you will do next
- [ ] Message alumni at three target companies for referral advice, with your resume link
- [ ] Review: which posts got responses? Keep the format that worked, one post every two weeks after this

### Rules for posts

- Short: 5 to 10 lines, one idea, one image or diagram.
- Specific: numbers and what you learned, not 'excited to share'.
- Honest: no inflated claims; tag people only if they were involved.
- No confidential details from internships or the professor's unpublished work.
