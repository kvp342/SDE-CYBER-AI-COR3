OPEN SOURCE · GSOC AND LFX

# Open source from first PR to GSoC

A practical route from zero to a merged pull request and a GSoC or LFX application by March 2027: which programme fits, a week-by-week plan from December, how to find a first issue, the exact git workflow (tested), how to write PRs and talk to maintainers, and how to write the proposal. Programme rules and dates come from the official pages listed at the end.

| Section                                                 |
|---------------------------------------------------------|
| [1. Why open source, and which programme](#01-why-open-source-and-which-programme)      |
| [2. Week by week: December to the deadline](#02-week-by-week-december-to-the-deadline)    |
| [3. Finding a project and a first issue](#03-finding-a-project-and-a-first-issue)       |
| [4. The pull-request workflow (tested)](#04-the-pull-request-workflow-tested)        |
| [5. Writing the PR and talking to maintainers](#05-writing-the-pr-and-talking-to-maintainers) |
| [6. The proposal](#06-the-proposal)                              |
| [7. Mistakes to avoid](#07-mistakes-to-avoid)                         |
| [8. Where this fits in the kit](#08-where-this-fits-in-the-kit)               |
| [Sources (8)](#-sources)                                 |

Start this week: Section 4 on a repository of your own. By the end of December, have five projects shortlisted and building on your machine.

## 01. Why open source, and which programme

- **What it gives you:** reviewed code in a real codebase, a public record recruiters can open, and mentors who can vouch for you. It also fits March 2027, when on-campus internship options are thin.
- **Google Summer of Code (GSoC):** paid, mentored work on an open-source project over a flexible 8 to 22 weeks. You must be at least 18 and a beginner to open source (regular contributors to a project do not count as beginners). Projects are small (about 90 hours), medium (about 175) or large (about 350). Payment depends on passing evaluations, not on your code being merged.^([\[1\]](#-sources))
- **LFX Mentorship (Linux Foundation):** paid terms of about three months on Linux Foundation projects, including CNCF cloud projects. You must be 18 by the start date and meet each project's prerequisites. You can apply to at most three projects per term, and applications open about four weeks before a term (the spring term runs 1 March to 31 May).^([\[2\]](#-sources)[\[3\]](#-sources)[\[4\]](#-sources))
- **Plain contributions:** no deadline and no stipend, but every merged pull request counts on your resume and makes a GSoC or LFX application much stronger.
- **Your fit:** C++ and Python, security, and cloud. Look at organisations tagged with security, networking, cloud or C++ on the GSoC organisations page, and at CNCF projects on LFX.

|                         | GSoC (2026 cycle, for reference)                    | LFX spring term                                     |
|-------------------------|-----------------------------------------------------|-----------------------------------------------------|
| Organisations announced | 19 Feb 2026 (185 organisations)^([\[5\]](#-sources)) | Projects listed on LFX from early January           |
| Talk to mentors         | 19 Feb – 15 Mar 2026^([\[6\]](#-sources))            | During the about four-week application window       |
| Applications            | 16 – 31 Mar 2026, 18:00 UTC^([\[6\]](#-sources))     | About four weeks before 1 March^([\[4\]](#-sources)) |
| Results                 | 30 Apr 2026^([\[6\]](#-sources))                     | Before the term starts                              |
| Work                    | Coding from 25 May 2026^([\[6\]](#-sources))         | 1 Mar – 31 May                                      |

GSoC 2027 dates were not published when this was written (17 Nov 2026). Expect a similar pattern, and check the official timeline page from January; Google notes that the timeline can shift a little each year.

## 02. Week by week: December to the deadline

| When                          | Do                                                                                                                                                  | Done when                                                |
|-------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------|
| Dec 2026, weeks 1–2           | Learn the workflow (Section 4) on your own repository. Read the GSoC FAQ and the LFX mentee guide end to end.                                       | You can fork, branch, open a PR and rebase without notes |
| Dec 2026, weeks 3–4           | Shortlist 5 projects: language you know, active in the last month, clear contributing guide, friendly replies to newcomers. Build each one locally. | All 5 build and their tests run on your machine          |
| Jan 2027                      | Pick 2 projects. Fix 2–3 small issues (docs, tests, small bugs). Join their chat or mailing list and read old discussions before asking.            | At least one merged PR                                   |
| Early Feb 2027                | Read last year's GSoC project ideas for your 2 projects. Make one larger contribution in the area you want to propose.                              | A PR that touches real code in that area                 |
| Mid-Feb 2027                  | When organisations are announced, check yours are in. Read their 2027 ideas list the same day.                                                      | One idea chosen, mentor identified                       |
| Late Feb – mid-Mar 2027       | Discuss the idea with the mentor in public channels. Draft the proposal (Section 6) and ask for one round of feedback.                              | Mentor has seen your draft                               |
| Contributor window (late Mar) | Submit early, not on the last day. Keep contributing while proposals are reviewed.                                                                  | Submitted with time to spare                             |
| If not selected               | Keep contributing anyway: LFX has three terms a year, and merged PRs stay on your resume.                                                           | —                                                        |

Fit it around the plan: about 4 hours a week in December and January, taken from project time rather than DSA. The exam break (22 Mar – 7 Apr) overlaps the end of the GSoC window, so submit before it starts.

## 03. Finding a project and a first issue

- **Signs of a healthy project:** commits in the last few weeks, issues answered within days, a CONTRIBUTING file, tests you can run, and maintainers who are polite to beginners.
- **Search GitHub for beginner issues:** `is:issue is:open label:"good first issue" language:C++` (or Python), optionally with `no:assignee` and `comments:<3` to find untouched ones.^([\[7\]](#-sources))
- **Good first contributions:** fix a broken doc example, add a missing test, improve an error message, reproduce a bug report and add the exact steps.
- **Before you start:** comment on the issue ("I'd like to work on this; my plan is …") and wait for a yes on anything bigger than a typo. Never open a PR for an issue someone else is working on.
- **Avoid:** drive-by PRs that only reformat code, mass typo PRs across many repos, and AI-generated changes you cannot explain line by line. Maintainers notice, and it can get you banned from a programme.

## 04. The pull-request workflow (tested)

Every command below was run end to end against local test repositories by `generated/oss/git_workflow_check.sh`, including a maintainer pushing a change while your PR was open.^([\[8\]](#-sources))

``` bash
# once: fork on GitHub (button), then
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
git switch main && git merge --ff-only upstream/main && git push origin main
```

- One branch per PR; never work on main.
- Small PRs get reviewed; 1,000-line PRs wait.
- Run the project's tests and formatter before pushing; CI failures waste a reviewer's time.
- Use `--force-with-lease`, never plain `--force`, on a branch others may have seen.

## 05. Writing the PR and talking to maintainers

### A PR description that gets reviewed

``` text
Fix crash when config file is empty (#1234)

What: parse_config() returned a null pointer for an empty file and the caller
dereferenced it. It now returns an empty Config and logs a warning.
Why: reported in #1234; reproducible with `touch empty.cfg && app --config empty.cfg`.
Tests: added test_empty_config; all existing tests pass locally (ctest).
Notes: happy to rename the warning or move it if you prefer.
```

### Messages

- **Asking for an issue:** "Hi, I'd like to work on this. I reproduced it on main (steps below). My plan is to … Does that sound right?"
- **Stuck:** say what you tried and what happened, with the exact error. Ask in the public channel, not by private message, so others benefit.
- **Review comments:** thank, fix, reply "Done in \<commit\>" under each comment. Do not argue style; follow the project's.
- **Silence:** wait a week, then one polite ping. Maintainers are often volunteers.

## 06. The proposal

| Section             | What to write                                                                                                                       |
|---------------------|-------------------------------------------------------------------------------------------------------------------------------------|
| Title and summary   | One sentence on what you will build and why the project needs it.                                                                   |
| About you           | Year, skills, time zone, hours a week available, and links to your merged PRs in this project (the strongest part).                 |
| Problem             | What is missing or broken today, with links to issues or discussions.                                                               |
| Design              | How you will do it: components, files you will touch, alternatives you considered and why you rejected them. A small diagram helps. |
| Timeline            | Week by week until the end, with a deliverable for each evaluation. Include a buffer week and your exam dates.                      |
| Testing and docs    | How you will test it and what documentation you will write.                                                                         |
| After the programme | How you will keep maintaining it.                                                                                                   |

- Base it on the organisation's ideas list and on what the mentor said; do not invent an unrelated project.
- Be honest about time. GSoC sizes are about 90, 175 or 350 hours; pick the size you can really deliver.^([\[1\]](#-sources))
- Ask the mentor to review a draft at least a week before the deadline.

## 07. Mistakes to avoid

- Applying to many organisations with the same generic proposal.
- Starting in March: by then serious applicants have weeks of contributions.
- Opening many tiny PRs just to show a count.
- Asking 'how do I start?' without reading the contributing guide.
- Promising more hours than you have (exams, placements).
- Disappearing after selection: failing an evaluation ends the stipend.

## 08. Where this fits in the kit

| Need                                 | Open                                                                                                                                                           |
|--------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| The overall plan and dates           | [final-plan.pdf](final-plan.md)                               |
| Git commands and debugging           | [linux-git-debugging-sheet.pdf](linux-git-debugging-sheet.md) |
| Docker and CI (most projects use CI) | [docker-ci-guide.pdf](docker-ci-guide.md)                     |
| Putting PRs on your resume           | [resume-kit.pdf](resume-kit.md)                               |
| GitHub profile                       | [profile-kit.pdf](profile-kit.md)                             |
| The tested workflow script           | [oss/git_workflow_check.sh](https://github.com/kvp342/intrusion-detection-and-prevention/blob/ccr-ca7232a7-t7lq94/generated/oss/git_workflow_check.sh)         |

## ··. Sources

Checked on 17 Nov 2026. Blogs and forum posts are single opinions; official pages win when they disagree. Numbers marked as rules of thumb are not company requirements.

1.  [Google Summer of Code FAQ (official)](https://developers.google.com/open-source/gsoc/faq)  
    https://developers.google.com/open-source/gsoc/faq
2.  [LFX Mentorship: am I eligible? (official)](https://docs.linuxfoundation.org/lfx/mentorship/mentee-guide/am-i-eligible)  
    https://docs.linuxfoundation.org/lfx/mentorship/mentee-guide/am-i-eligible
3.  [LFX Mentorship: how to apply (official)](https://docs.linuxfoundation.org/lfx/mentorship/mentee-guide/how-to-apply)  
    https://docs.linuxfoundation.org/lfx/mentorship/mentee-guide/how-to-apply
4.  [LFX Mentorship programme timelines (official)](https://docs.linuxfoundation.org/lfx/mentorship/mentorship-program-timelines)  
    https://docs.linuxfoundation.org/lfx/mentorship/mentorship-program-timelines
5.  [Google Open Source Blog: the 185 organisations for GSoC 2026](https://opensource.googleblog.com/2026/02/introducing-the-185-organizations-for-gsoc-2026.html)  
    https://opensource.googleblog.com/2026/02/introducing-the-185-organizations-for-gsoc-2026.html
6.  [Google Summer of Code timeline (official)](https://developers.google.com/open-source/gsoc/timeline)  
    https://developers.google.com/open-source/gsoc/timeline
7.  [GitHub Docs: searching issues and pull requests](https://docs.github.com/en/search-github/searching-on-github/searching-issues-and-pull-requests)  
    https://docs.github.com/en/search-github/searching-on-github/searching-issues-and-pull-requests
8.  [GitHub Docs: syncing a fork](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/syncing-a-fork)  
    https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/syncing-a-fork
