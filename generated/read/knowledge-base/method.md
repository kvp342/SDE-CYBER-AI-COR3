# Method

[All categories](README.md) · 14 topics

## Topics

- [Active recall](#active-recall)
- [Spaced repetition (1-3-7-21)](#spaced-repetition-1-3-7-21)
- [The 20–40 minute rule](#the-2040-minute-rule)
- [Patterns, not problems](#patterns-not-problems)
- [Interleaving](#interleaving)
- [Speaking while you code](#speaking-while-you-code)
- [The error log](#the-error-log)
- [Upsolving](#upsolving)
- [Deep-work blocks (50/10)](#deep-work-blocks-5010)
- [Sleep, exercise and energy](#sleep-exercise-and-energy)
- [Weekly review](#weekly-review)
- [Day modes and the never-zero rule](#day-modes-and-the-never-zero-rule)
- [Using AI as a tutor](#using-ai-as-a-tutor)
- [The five difficulty levels](#the-five-difficulty-levels)

## Active recall

*Level 0: Foundation*

The single biggest learning multiplier. It's why the plan says 'solve before watching' and 'explain on a blank page'.

**Key idea**

Retrieving information from memory strengthens it far more than re-reading it (the testing effect, Roediger & Karpicke 2006). Struggling to recall is the point; it feels slower but sticks.

In practice: close the video and solve, write a Core CS answer from memory before checking notes, and use flashcards that ask a question instead of showing a fact.

The Feynman technique: explain the concept in simple words on a blank page as if teaching a junior. Where you get vague is exactly what to re-learn.


**Points**

- Notes in question form ('Why are threads cheaper?')
- Teach a friend or explain aloud
- Use the AI Feynman-checker prompt to find gaps

**Traps**

- Highlighting and re-watching (feels productive, isn't)

**Learn more**

- [Roediger & Karpicke 2006 (PDF)](http://psychnet.wustl.edu/memory/wp-content/uploads/2018/04/Roediger-Karpicke-2006_PPS.pdf)
- [Anki](https://apps.ankiweb.net)

**Related:** [Spaced repetition (1-3-7-21)](#spaced-repetition-1-3-7-21) · [The error log](#the-error-log)

[Back to the topic list](#topics)

## Spaced repetition (1-3-7-21)

*Level 0: Foundation*

Without revision you forget most of a solved problem within weeks. This turns 550 problems into lasting skill.

**Key idea**

Memory fades along a forgetting curve; each review at the right moment resets and flattens it. Spacing reviews out (1, 3, 7, 21 days) gives the most retention per minute.

For DSA: every problem you failed or needed a hint for goes on the list. On its due day, re-solve from a blank file in ≤ 10 minutes. Two clean passes in a row → retire it.

For Core CS facts: Anki does the scheduling automatically, 10 minutes a day.


**Points**

- Revise before new problems each morning
- Keep revision to ~20% of DSA time
- Exam mode = revision only

```text
Google Sheets columns:
Date | Problem | Link | Pattern | Mistake | R1 | R3 | R7 | R21
R1: =A2+1   R3: =A2+3   R7: =A2+7   R21: =A2+21
Filter: any R column <= TODAY() and not ticked
```

**Traps**

- Re-reading old solutions instead of re-solving

**Learn more**

- [Anki manual](https://docs.ankiweb.net)
- [Gwern on spaced repetition](https://gwern.net/spaced-repetition)

**Related:** [Active recall](#active-recall) · [The error log](#the-error-log)

[Back to the topic list](#topics)

## The 20–40 minute rule

*Level 0: Foundation*

Stops you wasting hours stuck, and stops you giving up too early. Both are common.

**Key idea**

Easy/Medium: try for 20 minutes. Hard: 40 minutes. If stuck at the limit, read only the approach or hint (not code), then implement it yourself.

Stuck time is valuable up to a point: you are building the search for a pattern. Beyond it, you're just tired. The hint converts the struggle into learning.

Every problem you needed a hint for goes on the spaced-repetition list.


**Points**

- Use the AI hint-only prompt for graded hints
- Read the editorial only until the key idea

**Traps**

- Copying the full solution
- Spending 3 hours on one problem

**Related:** [Spaced repetition (1-3-7-21)](#spaced-repetition-1-3-7-21) · [The interview loop (UMPIRE)](career.md#the-interview-loop-umpire) · [Using AI as a tutor](#using-ai-as-a-tutor)

[Back to the topic list](#topics)

## Patterns, not problems

*Level 0: Foundation*

300 problems become about 25 reusable patterns, which is how strong candidates solve problems they've never seen.

**Key idea**

After each solve, write one line: trigger → pattern. 'Sorted + pair sum → two pointers.' 'Minimum of the maximum → binary search on the answer.'

Before coding a new problem, scan your trigger list. If nothing fits, run the fallback checklist: can I sort it? hash it? binary search the answer? define states (DP)? model it as a graph?


**Points**

- Keep the trigger list on one page
- Review it before every contest and interview

**Traps**

- Memorising solutions instead of triggers

**Learn more**

- [NeetCode roadmap](https://neetcode.io/roadmap)

**Related:** [Two pointers](dsa.md#two-pointers) · [Sliding window](dsa.md#sliding-window) · [Binary search on the answer](dsa.md#binary-search-on-the-answer) · [Dynamic programming](dsa.md#dynamic-programming)

[Back to the topic list](#topics)

## Interleaving

*Level 0: Foundation*

Interviews don't tell you the topic. Mixed practice trains you to identify the pattern, not just apply it.

**Key idea**

Blocked practice (ten graph problems in a row) feels smooth because you already know the pattern. Interleaved practice (a graph, then a DP, then a string) forces you to choose, which is the real interview skill. Studies show interleaving improves later test performance even though it feels harder.

Use blocked practice when first learning a topic (Striver order), then interleave in revision days, contests and mocks.


**Points**

- Sunday revision: random mix from the 1-3-7-21 list
- LeetCode 'pick one' or company-tagged lists are naturally interleaved

**Traps**

- Interleaving before you know the basics of each topic

**Related:** [Patterns, not problems](#patterns-not-problems) · [Spaced repetition (1-3-7-21)](#spaced-repetition-1-3-7-21)

[Back to the topic list](#topics)

## Speaking while you code

*Level 1: Core*

Interviewers score communication. Silence reads as 'stuck'. Tier-3 candidates practise this least.

**Key idea**

Narrate: restate the problem, ask about constraints, say the brute force and its complexity, explain the better idea before coding, comment while coding ('this map stores value → index'), then dry-run aloud.

Practise one problem a day out loud, ideally recorded. Listen once a week for long silences and filler.


**Points**

- Ask 'Shall I code this approach?' before coding
- Say complexity without being asked

**Traps**

- Coding in silence for 10 minutes then explaining

**Learn more**

- [Pramp (free mock interviews)](https://www.pramp.com)

**Related:** [The interview loop (UMPIRE)](career.md#the-interview-loop-umpire) · [Mock interviews](career.md#mock-interviews)

[Back to the topic list](#topics)

## The error log

*Level 0: Foundation*

Most wrong answers come from the same 10 mistakes. A log makes them visible so you stop repeating them.

**Key idea**

Every wrong submission or failed interview question: one line with the problem, the mistake (off-by-one, int overflow, missed empty input, wrong pattern, misread question) and the fix.

Read the log before every contest, OA and interview. After a month, the top three mistake types become your personal pre-submit checklist.


**Points**

- Tag mistakes by type to count them
- Pre-submit checklist: overflow? empty? n=1? duplicates? negative?

**Traps**

- Logging without ever re-reading

**Related:** [Spaced repetition (1-3-7-21)](#spaced-repetition-1-3-7-21) · [Online assessments (OAs)](career.md#online-assessments-oas)

[Back to the topic list](#topics)

## Upsolving

*Level 1: Core*

The problem just past your level teaches the most; contests only show you where that is.

**Key idea**

After a contest, take the first problem you couldn't solve. Try again for 30 minutes, then read the editorial idea, implement it yourself, and add it to the revision list.

One upsolved problem per contest beats two new contests without upsolving.


**Points**

- Rating grows from upsolving, not from attempts

**Traps**

- Skipping upsolving because the contest went badly

**Learn more**

- [Codeforces editorials](https://codeforces.com)

**Related:** [Competitive programming and contests](dsa.md#competitive-programming-and-contests) · [The 20–40 minute rule](#the-2040-minute-rule)

[Back to the topic list](#topics)

## Deep-work blocks (50/10)

*Level 0: Foundation*

Hours at a desk don't measure progress; focused blocks do. Six blocks is a full-force day.

**Key idea**

Work 50 minutes on one task with the phone in another room and notifications off; take a 10-minute break away from screens. Count blocks, not hours.

Put the hardest work (new DSA) in your sharpest hours, and revision, AWS and admin when tired. Decide each block's task the night before so you start instantly.


**Points**

- Pomofocus timer
- Track blocks per day in your sheet
- 6 blocks = full force; 2 blocks = college day

**Traps**

- Checking the phone 'just once' during a block

**Learn more**

- [Pomofocus](https://pomofocus.io)
- [Cal Newport, Deep Work (book)](https://calnewport.com/deep-work-rules-for-focused-success-in-a-distracted-world/)

**Related:** [Day modes and the never-zero rule](#day-modes-and-the-never-zero-rule) · [Sleep, exercise and energy](#sleep-exercise-and-energy)

[Back to the topic list](#topics)

## Sleep, exercise and energy

*Level 0: Foundation*

Memory consolidation happens during sleep. Cutting sleep to study more is a net loss.

**Key idea**

Sleep 7–8 hours at a fixed time. Sleep after learning consolidates new memories; sleep deprivation hurts attention, problem-solving and recall the next day.

Exercise 20–30 minutes a day (walk, sport, gym) improves focus and mood. One rest half-day a week prevents burnout, which costs weeks.


**Points**

- No all-nighters before contests or interviews
- Caffeine before 2 pm

**Traps**

- Comparing yourself to LinkedIn posts at midnight

**Learn more**

- [Matthew Walker, Why We Sleep (book)](https://www.simonandschuster.com/books/Why-We-Sleep/Matthew-Walker/9781501144325)

**Related:** [Deep-work blocks (50/10)](#deep-work-blocks-5010) · [Day modes and the never-zero rule](#day-modes-and-the-never-zero-rule)

[Back to the topic list](#topics)

## Weekly review

*Level 0: Foundation*

Plans fail quietly. A 30-minute review each Sunday catches drift before it becomes a lost month.

**Key idea**

Every Sunday: count problems, contests and blocks against the week's target; re-solve the week's failed problems; look at what slipped and why; set next week's three priorities.

Monthly (last Sunday, 1 hour): check the milestone checklist, take one timed mock on old topics, cut whatever isn't moving a number.


**Points**

- Move unfinished items, never stack them on top
- Adjust quotas by ±1 problem, not ±5

**Traps**

- Abandoning the plan after one bad week

**Related:** [Day modes and the never-zero rule](#day-modes-and-the-never-zero-rule) · [Spaced repetition (1-3-7-21)](#spaced-repetition-1-3-7-21)

[Back to the topic list](#topics)

## Day modes and the never-zero rule

*Level 0: Foundation*

Your weeks will differ: home, college, exams, bad days. A recipe for each removes the daily decision and keeps the streak.

**Key idea**

Pick one mode each morning: Full force (6–8 blocks), College day (2 problems + AWS + flashcards), Exam mode (1 revision problem), Low energy (1 easy re-solve + read the error log), Sprint (mock + company set + applications).

Never zero: the streak is 'at least one problem touched'. A low-energy day that keeps the streak beats a perfect day followed by four days off.

Behind schedule? Cut in this order: the Elite HFT track (if open), the CP habit, the AI-security project. Never DSA or revision, and never double tomorrow's quota.


**Points**

- Plan tomorrow in 5 minutes tonight
- Exam mode 22 Mar – 7 Apr 2027

**Traps**

- All-or-nothing thinking

**Related:** [Deep-work blocks (50/10)](#deep-work-blocks-5010) · [Weekly review](#weekly-review)

[Back to the topic list](#topics)

## Using AI as a tutor

*Level 0: Foundation*

Claude and Gemini can be a free tutor and interviewer, or a crutch that makes you feel productive while learning nothing. The rules decide which.

**Key idea**

Use AI for: graded hints (one at a time), mock interviews, reviewing your accepted code, checking your Feynman explanations, generating flashcards, and resume critique.

Never paste a problem and ask for the solution before your 20/40-minute timebox. Interviewers spot borrowed understanding in two minutes of follow-ups.

Verify facts it gives you against docs; models can be confidently wrong, especially on exact numbers and APIs.


**Points**

- Ask it to grade you 1–5 with one fix per area
- Use it to explain an editorial line you don't get

```cpp
Hint-only tutor prompt:
I'm solving [problem]. Don't give the solution or code. Give me one hint at a time,
the smallest nudge first. Wait for me to say 'next' before the next hint.
```

**Traps**

- Copying AI code into LeetCode
- Trusting its complexity analysis without checking

**Related:** [The 20–40 minute rule](#the-2040-minute-rule) · [Mock interviews](career.md#mock-interviews)

[Back to the topic list](#topics)

## The five difficulty levels

*Level 0: Foundation*

Tells you where to stop climbing on each topic, so you don't over-invest where your target jobs don't ask.

**Key idea**

L0 Foundation: you can't do it yet; learn syntax, ideas and vocabulary. L1 Core: you can do it with notes (service-company level). L2 Interview-ready: cold, timed, out loud (product companies). L3 Advanced: you can handle the twist: Hards, contests, design trade-offs (Big Tech). L4 Elite: rare proof such as CF 1900+, CVEs, merged open-source work, HFT puzzles.

Your targets: DSA to L3, Core CS to L2, security to L3 (your edge), everything else to L1–L2 unless a specific job needs more.


**Points**

- Climb in order
- Depth on one ladder beats breadth on five

**Traps**

- Starting L4 topics before L2 is solid

**Related:** [Dynamic programming](dsa.md#dynamic-programming) · [OWASP Top 10](security.md#owasp-top-10) · [AWS core services and the SAA-C03 exam](cloud.md#aws-core-services-and-the-saa-c03-exam)

[Back to the topic list](#topics)
