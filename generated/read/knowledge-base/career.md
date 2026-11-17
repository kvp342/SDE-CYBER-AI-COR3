# Career

[All categories](README.md) · 12 topics

## Topics

- [The interview loop (UMPIRE)](#the-interview-loop-umpire)
- [Online assessments (OAs)](#online-assessments-oas)
- [Mock interviews](#mock-interviews)
- [Behavioural interviews and STAR stories](#behavioural-interviews-and-star-stories)
- [The one-page resume](#the-one-page-resume)
- [Projects that get shortlisted](#projects-that-get-shortlisted)
- [Referrals and LinkedIn outreach](#referrals-and-linkedin-outreach)
- [Cold emailing startups](#cold-emailing-startups)
- [The application pipeline](#the-application-pipeline)
- [Preparing for a specific company](#preparing-for-a-specific-company)
- [Offers, CTC and negotiation](#offers-ctc-and-negotiation)
- [Open source and GSoC](#open-source-and-gsoc)

## The interview loop (UMPIRE)

*Level 1: Core*

A fixed routine for every DSA interview so nerves don't decide your structure.

**Key idea**

Understand: restate the problem, ask about input size, ranges, duplicates, empty input; agree on 2 examples. Match: name the pattern. Plan: describe the approach in words and give its complexity; get a nod. Implement: clean code, good names. Review: dry-run an example and an edge case. Evaluate: complexity, trade-offs, what you'd improve.

Always say the brute force first. It shows you can solve it, gives you a fallback and often reveals the optimisation.


**Points**

- Spend ~5 min understanding, ~5 planning, ~20 coding, ~5 testing in a 45-min round
- If stuck, think aloud about what you know; interviewers give hints to people who talk

**Traps**

- Coding before the interviewer agrees with the approach

**Learn more**

- [CodePath UMPIRE guide](https://guides.codepath.org/compsci/UMPIRE-Interview-Strategy)

**Related:** [Speaking while you code](method.md#speaking-while-you-code) · [Patterns, not problems](method.md#patterns-not-problems) · [Mock interviews](#mock-interviews)

[Back to the topic list](#topics)

## Online assessments (OAs)

*Level 1: Core*

The first filter for almost every off-campus role. Many strong candidates fail here from poor tactics, not poor skill.

**Key idea**

Typical format: 2–3 DSA problems in 60–90 minutes on HackerRank, HackerEarth, CodeSignal or Mettl, sometimes with MCQs on CS fundamentals and aptitude.

Tactics: read all problems in the first 2 minutes; solve in order of confidence; submit a brute force for partial test cases if the optimal idea isn't coming; check overflow (long long), empty and max-size inputs; stop optimising in the last 10 minutes.

Practise in the same environment: do timed sets on HackerRank, not only LeetCode, because I/O handling differs (you often write main() and read input yourself).


**Points**

- Keep your C++ template ready to paste
- Proctoring: webcam, no tab switching
- Simulate a full 90-minute OA weekly from June

**Traps**

- Spending 60 minutes on problem 1
- Forgetting to read input in the given format

**Learn more**

- [HackerRank interview prep kit](https://www.hackerrank.com/interview/interview-preparation-kit)

**Related:** [Competitive programming and contests](dsa.md#competitive-programming-and-contests) · [The error log](method.md#the-error-log) · [Time and space complexity](dsa.md#time-and-space-complexity)

[Back to the topic list](#topics)

## Mock interviews

*Level 2: Interview-ready*

Interviewing is a separate skill from solving. Mocks are where you find out what breaks under pressure.

**Key idea**

From 31 May, two mocks a week: one peer DSA mock and one Core CS / design mock. Rotate roles: being the interviewer teaches you what they look for.

Free options: Pramp (peer matching), friends from college or Discord groups, the AI mock-interviewer prompt. Record yourself when practising alone.

After each mock, write three things: what went well, what broke, one fix for next time.


**Points**

- Score yourself 1–5 on problem solving, code, communication
- Do mocks at the same time of day as real interviews

**Traps**

- Only doing mocks with friends who go easy on you

**Learn more**

- [Pramp](https://www.pramp.com)
- [interviewing.io (free practice when available)](https://interviewing.io)

**Related:** [The interview loop (UMPIRE)](#the-interview-loop-umpire) · [Speaking while you code](method.md#speaking-while-you-code) · [Behavioural interviews and STAR stories](#behavioural-interviews-and-star-stories)

[Back to the topic list](#topics)

## Behavioural interviews and STAR stories

*Level 1: Core*

Amazon's bar raiser and every HR round use behavioural questions. Six good stories cover almost all of them.

**Key idea**

STAR: Situation (one line of context), Task (your responsibility), Action (what you did — most of the answer, in 'I' not 'we'), Result (outcome with a number, plus what you learned).

Prepare six stories that each fit several questions: a hard technical problem (TenantWall IAM), a failure, a conflict, learning something fast (C++/AWS), going beyond the task (a security finding), helping or leading someone.

For Amazon, map each story to Leadership Principles: Ownership, Dive Deep, Learn and Be Curious, Bias for Action, Deliver Results, Customer Obsession.


**Points**

- Keep each story to ~2 minutes
- Have a 60-second 'tell me about yourself'
- Real numbers beat adjectives

**Traps**

- Talking about the team instead of your actions
- No result or lesson

**Interviewers ask**

- Tell me about a time you failed.
- Tell me about a conflict with a teammate.
- Why this company?

**Learn more**

- [Amazon Leadership Principles](https://www.amazon.jobs/content/en/our-workplace/leadership-principles)

**Related:** [Mock interviews](#mock-interviews) · [TenantWall (your research project)](cloud.md#tenantwall-your-research-project)

[Back to the topic list](#topics)

## The one-page resume

*Level 1: Core*

Off-campus, the resume is read for 6–10 seconds. It decides whether any of your work gets seen.

**Key idea**

One page, single column, no photos, tables or graphics (ATS parsers break on them), exported as PDF named Firstname\_Lastname\_SDE.pdf.

Order for you: contact links (LinkedIn, GitHub, LeetCode/Codeforces) → education (CGPA if ≥ 7.5) → experience → projects (TenantWall first) → achievements (ratings, CTF ranks, AWS SAA, paper) → skills.

Bullet formula: action verb + what you built + technology + measurable result. 'Built X using Y, which achieved Z.'

Keep a 2-page private master resume with every bullet; cut 3 one-page versions (SDE, Security/AppSec, Cloud) and tailor each application in 5 minutes.


**Points**

- Numbers in every project bullet
- Link a live demo or video
- Have two seniors review it

**Traps**

- Listing every technology you've touched
- Tutorial projects (to-do app, weather app)

**Learn more**

- [Overleaf resume templates (Jake's resume)](https://www.overleaf.com/latex/templates/jakes-resume/syzfjbzwjncs)

**Related:** [Projects that get shortlisted](#projects-that-get-shortlisted) · [Referrals and LinkedIn outreach](#referrals-and-linkedin-outreach)

[Back to the topic list](#topics)

## Projects that get shortlisted

*Level 2: Interview-ready*

Two strong projects with numbers beat six tutorials, and give you the stories for interviews.

**Key idea**

Every project needs: a live link or demo video, a README with an architecture diagram, at least one number (latency, requests/s, users, bugs found), and a 'what I'd do next' line.

For your profile: TenantWall (cloud security research), a rate-limited URL shortener on AWS with load-test numbers (backend + design), a log-based intrusion detector (security + data), a secure RAG assistant with prompt-injection tests (AI + AppSec), and 3+ merged open-source PRs.

Threat-model each project and fix one issue; it becomes a unique interview story.


**Points**

- Pin them on GitHub with clean READMEs
- Write tests for core logic
- Never commit secrets (.env in .gitignore)

**Traps**

- Unfinished projects with no README

**Interviewers ask**

- Walk me through your project's architecture.
- What was the hardest bug?
- How would it scale?

**Learn more**

- [roadmap.sh project ideas](https://roadmap.sh/projects)

**Related:** [TenantWall (your research project)](cloud.md#tenantwall-your-research-project) · [The one-page resume](#the-one-page-resume) · [Threat modelling (STRIDE)](security.md#threat-modelling-stride)

[Back to the topic list](#topics)

## Referrals and LinkedIn outreach

*Level 1: Core*

The strongest off-campus channel: the Eternal (Zomato) story in this guide came through a referral.

**Key idea**

Find employees or alumni at the target company on LinkedIn (search 'company + RAIT' first, then any engineer). Send a short, specific note with the job ID and your resume link. Ask for a referral, not 'a job'.

Make it easy to say yes: one-line intro, two proofs (problems solved, project), the exact role and job ID, a resume link. Thank them either way and follow up once after 5–7 days.

Build the network before you need it: comment thoughtfully on engineers' posts, share your project write-ups.


**Points**

- 10 referral messages a week
- Alumni reply far more often than strangers
- Track every message in your sheet

```text
Hi [Name], I'm a 3rd-year CSE (Cybersecurity) student; I've solved 450+ DSA problems and built [project in one line].
I'm applying for [Role, Job ID] at [Company]. Would you be open to referring me?
Resume: [link]. Thank you!
```

**Traps**

- 'Hi, any openings?' messages with no context
- Messaging the same person repeatedly

**Related:** [The application pipeline](#the-application-pipeline) · [The one-page resume](#the-one-page-resume) · [Cold emailing startups](#cold-emailing-startups)

[Back to the topic list](#topics)

## Cold emailing startups

*Level 2: Interview-ready*

Startups hire interns without formal drives. A specific email to a founder can skip the whole funnel.

**Key idea**

Target funded Indian startups (Inc42, Entrackr funding news, YC India companies). Email the founder or CTO directly.

Five lines: you use or studied their product; who you are; one relevant thing you built (with a number); one specific observation (a bug, a missing security header, a feature idea); the ask (internship for N months, 15-minute call). Attach or link resume and GitHub.

Send 5 a week, personalised. A security observation done responsibly (no exploitation) is a strong opener for a cyber student.


**Points**

- Subject line: role + your hook
- Follow up once after a week

**Traps**

- Mass-mailing the same template
- Testing their systems without permission

**Learn more**

- [Inc42 funding news](https://inc42.com/buzz/funding-galore-indian-startup-funding-this-week/)
- [Y Combinator companies (India filter)](https://www.ycombinator.com/companies)

**Related:** [Referrals and LinkedIn outreach](#referrals-and-linkedin-outreach) · [The application pipeline](#the-application-pipeline)

[Back to the topic list](#topics)

## The application pipeline

*Level 1: Core*

Off-campus hiring is a numbers game. A batched system makes 50 good applications a month take 90 minutes a week.

**Key idea**

Collect: saved job alerts on LinkedIn and Naukri, 40 bookmarked careers pages checked Monday and Thursday, Unstop and HackerEarth for hiring contests.

Apply in two 45-minute batches (Mon, Thu): tailor the resume in 5 minutes, apply within 48 hours of posting, send the referral message for each job.

Track everything in one sheet: company, role, date, channel, contact, status, next action. Follow up once after 5–7 days. Expect a 2–5% reply rate; volume plus quality produces interviews.


**Points**

- Apply even before you feel ready (≈150 problems + 1 project)
- Hiring contests skip resume filters
- Re-use 'why this company' answers

**Traps**

- Applying only on campus
- No tracker, so no follow-ups

**Learn more**

- [Unstop](https://unstop.com)
- [LinkedIn Jobs](https://www.linkedin.com/jobs/)

**Related:** [Referrals and LinkedIn outreach](#referrals-and-linkedin-outreach) · [Cold emailing startups](#cold-emailing-startups) · [The one-page resume](#the-one-page-resume)

[Back to the topic list](#topics)

## Preparing for a specific company

*Level 2: Interview-ready*

Once you have an interview, one focused week beats general practice.

**Key idea**

1) Read 5–10 recent interview experiences for that company and role on LeetCode Discuss and GeeksforGeeks; note round types and repeated questions. 2) Solve its most frequent recent LeetCode-tagged problems (top 30). 3) Map its values to your STAR stories. 4) Use the product: find one improvement and one security thought to mention.

Ask the recruiter about the round structure; they usually tell you.


**Points**

- LeetCode company tags need Premium; free alternatives are Discuss posts and GitHub lists of company questions
- Glassdoor interview section

**Traps**

- Only solving tagged problems without fundamentals

**Learn more**

- [LeetCode Discuss: interview experiences](https://leetcode.com/discuss/interview-experience)
- [GfG interview experiences](https://www.geeksforgeeks.org/interview-experiences/)

**Related:** [Behavioural interviews and STAR stories](#behavioural-interviews-and-star-stories) · [Mock interviews](#mock-interviews)

[Back to the topic list](#topics)

## Offers, CTC and negotiation

*Level 2: Interview-ready*

Freshers often lose money or sign bad bonds by not knowing what to ask.

**Key idea**

CTC (cost to company) includes fixed salary, variable/bonus, joining bonus, stock (RSUs vesting over years), benefits. In-hand monthly pay is fixed salary minus tax and PF, divided by 12. Ask for the breakdown in writing.

Check the service agreement or bond clause, notice period, location and relocation support before signing.

Negotiation: research ranges on levels.fyi and Glassdoor; avoid naming a number first; if you have a competing written offer, mention it politely. Mass-recruiter fresher offers are rarely negotiable; product companies sometimes adjust joining bonus.


**Points**

- RSUs: 4-year vesting is common, often with a 1-year cliff
- PPO = pre-placement offer from an internship

**Traps**

- Comparing CTCs without separating fixed and variable

**Interviewers ask**

- What are your salary expectations?

**Learn more**

- [levels.fyi](https://www.levels.fyi)
- [Glassdoor India](https://www.glassdoor.co.in)

**Related:** [The application pipeline](#the-application-pipeline)

[Back to the topic list](#topics)

## Open source and GSoC

*Level 3: Advanced*

A brand that removes the college question (see the tier-3 MCA student's GSoC story), and real code review experience.

**Key idea**

Pick one organisation whose tech you use (C++, Python, security tools). Set up the project locally, read the contribution guide, start with 'good first issue' labels, and join their chat.

Aim for 3+ merged PRs before applying to programmes. GSoC contributor applications usually open in March–April (check the timeline each year); LFX Mentorship runs several cohorts a year; MLH Fellowship is another route.

Your proposal should show you already understand the codebase: link your merged PRs and give a week-by-week plan.


**Points**

- Quality of PRs \> quantity
- Maintainers often refer good contributors for jobs

**Traps**

- Typo-fix PRs to many repos
- Starting a month before the deadline

**Learn more**

- [Google Summer of Code](https://summerofcode.withgoogle.com)
- [LFX Mentorship](https://mentorship.lfx.linuxfoundation.org)
- [MLH Fellowship](https://fellowship.mlh.io)

**Related:** [Projects that get shortlisted](#projects-that-get-shortlisted)

[Back to the topic list](#topics)
