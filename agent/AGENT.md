# Placement kit agent: standing instructions

You are improving a placement-preparation kit for a B.Tech CSE (Cybersecurity) student, class of 2028, on **Path A** (SDE with security and cloud depth; an Elite HFT track opens only if they pass a checkpoint on 31 Mar 2027). Everything lives in this repository.

## Every run

1. `git fetch origin ccr-ca7232a7-t7lq94 && git checkout ccr-ca7232a7-t7lq94 && git pull`. Work on this branch; after each push, also update `main` to the same commit (fast-forward only). Never push anywhere else, never open pull requests.
2. If today is after 21 Nov 2026, write nothing and stop.
3. Open `agent/BACKLOG.md`. Take the **first** item whose box is `[ ]`. If it was started but left unfinished (see `agent/LOG.md`), finish it instead.
4. Build it completely in one run. Quality bar:
   - Content is accurate. Code in C++17 must compile with `g++ -std=c++17 -Wall` and pass tests you write; say in the log what you tested.
   - Sources: you may use WebSearch and WebFetch for public pages (roadmap.sh, takeuforward, official docs, LeetCode problem pages). Cite each source with a link in the document. Never copy long passages: summarise in your own words. If a site is blocked, use another source or your own knowledge and say so in the log.
   - PDFs: write HTML, render with Playwright (`require('playwright')`, `page.pdf`, A4, `printBackground: true`), fonts Inter / Space Grotesk / JetBrains Mono from Google Fonts. Every PDF needs a clickable index (internal `#id` links), section back-links, real web links, and page numbers. Use flat colours (no blur, shadows or gradients) so phone viewers open it. Keep each PDF under 5 MB.
   - Match the existing style: see `Tier3-to-Top-Offer-Placement-Guide.pdf` and `sources/` for helpers.
   - Plain, direct English. No emoji. No filler.
5. Save outputs in `generated/` (PDFs and HTML) and the build script in `generated/src/`. Add one line per new file to the table in `README.md`. Then run `python3 generated/src/make_markdown.py` so `generated/read/` (the Markdown copy of everything, readable directly on GitHub) includes the new file; add the new builder and its HTML name to `BUILDERS` in that script first.
6. Tick the item in `agent/BACKLOG.md`, append a short entry to `agent/LOG.md` (date, item, files, what you verified, anything left).
7. Commit with a clear message and push: `git push -u origin ccr-ca7232a7-t7lq94`, then keep `main` identical: `git push origin ccr-ca7232a7-t7lq94:main` (the student asked for everything on main; retry up to 4 times on network errors).

## Never

- Put personal details in the repo (no names, email, phone, CGPA, college ID). The repo is public.
- Delete or rewrite existing files outside `generated/` and `agent/`, except adding lines to `README.md`.
- Add anything about TLE Eliminators.
- Spend the run on more than one backlog item if the first is not finished and verified.
- Invent facts, statistics or interview stories. If unsure, leave it out.

## Context you can rely on

- Plan dates: C++ 16–17 Nov 2026; Striver A2Z core 18 Nov – 30 Jan (classic 18-step sheet, 5–6 problems a day); Hard pass 8 Feb – 19 May (paused for exams 22 Mar – 7 Apr); AWS SAA-C03 in the week of 19 Apr; AI-security project in May; placement sprint 31 May – 31 Jul; placements Aug – Dec 2027.
- Existing material: `knowledge-base.html` (167 pages incl. 43 tested solutions, Core CS Q&A, 8 mocks, 10 company files), `roadmap.html`, `playbook.html`, `cheat-sheet.html`, two A2Z sheet PDFs, and the sources in `sources/`.
