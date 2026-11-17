# Mocks

[All categories](README.md) · 9 topics

## Topics

- [How to run a mock interview](#how-to-run-a-mock-interview)
- [Mock 1: arrays and hashing](#mock-1-arrays-and-hashing)
- [Mock 2: sliding window and binary search](#mock-2-sliding-window-and-binary-search)
- [Mock 3: trees and graphs](#mock-3-trees-and-graphs)
- [Mock 4: dynamic programming](#mock-4-dynamic-programming)
- [Mock 5: Core CS viva](#mock-5-core-cs-viva)
- [Mock 6: low-level design (parking lot)](#mock-6-low-level-design-parking-lot)
- [Mock 7: system design (URL shortener)](#mock-7-system-design-url-shortener)
- [Mock 8: behavioural and project deep dive](#mock-8-behavioural-and-project-deep-dive)

## How to run a mock interview

*Level 2: Interview-ready*

From 31 May you do two mocks a week. This kit lets a classmate interview you properly even if they have never done it: a script, hints to give, answer keys and a score sheet.

**Key idea**

Two people, two roles. The interviewer reads the mock page (including the hidden answers); the candidate sees only the problem. Swap roles next time: interviewing others teaches you what interviewers notice.

Timing for a 45-minute DSA mock: 2 minutes of introductions, 35 minutes on problems, 8 minutes of feedback. The interviewer stays quiet unless the candidate is stuck for 3 or more minutes, then gives the next hint on the ladder, never the solution.

After each mock, both write three lines: what went well, what broke, one fix. Enter the scores in the tracker's Mocks tab. Repeat any mock you scored under 3 in an area after two weeks.

Schedule: 8 mocks in this kit, each run twice (once in June, once in July) gives the 16 mocks the plan asks for. Do Mock 5 (Core CS viva) and Mock 8 (behavioural) before every real interview week too.


**Points**

- Score each area 1 to 4: 1 = could not, 2 = with heavy hints, 3 = with a nudge, 4 = independently and clearly
- Problem solving: clarified, found an approach, improved it
- Code: correct, clean names, handles edge cases
- Communication: thought aloud, explained before coding, took hints well
- Testing: dry run, edge cases, complexity stated
- A pass is 3+ in every area. Log the scores in the tracker's Mocks tab

**Traps**

- Mocking only with friends who go easy
- Not recording what broke
- Doing the same problem twice in a week (you are testing memory, not skill)

**Practise**

- [Pramp (free peer mocks)](https://www.pramp.com)

**Related:** [The interview loop (UMPIRE)](career.md#the-interview-loop-umpire) · [Speaking while you code](method.md#speaking-while-you-code) · [Behavioural interviews and STAR stories](career.md#behavioural-interviews-and-star-stories)

[Back to the topic list](#topics)

## Mock 1: arrays and hashing

*Level 2: Interview-ready*

Warm-up level for the first mock. Tests whether you clarify, give a brute force, then improve.

**Key idea**

Format: 45 minutes, two problems. Problem 1 is a warm-up (aim for 12 minutes), problem 2 is the main one (aim for 23 minutes).

Problem 1: Majority Element. Given an array of n integers, return the element that appears more than n/2 times (it always exists).

Problem 2: Set Matrix Zeroes. Given an m × n matrix, if an element is 0, set its entire row and column to 0, in place.


**Points**

- Score each area 1 to 4: 1 = could not, 2 = with heavy hints, 3 = with a nudge, 4 = independently and clearly
- Problem solving: clarified, found an approach, improved it
- Code: correct, clean names, handles edge cases
- Communication: thought aloud, explained before coding, took hints well
- Testing: dry run, edge cases, complexity stated
- A pass is 3+ in every area. Log the scores in the tracker's Mocks tab

**Questions and model answers**

**Q. Problem 1: hints and answer key**

Hint 1: Could you do it with a hash map? (Yes, O(n) space.) Hint 2: Sorting puts the majority at index n/2; what does that cost? Hint 3: Pair each majority element with a different element and cancel them; what survives? Answer: Boyer–Moore voting. Keep a candidate and a count; if count is 0, take the current element as candidate; add 1 if equal, else subtract 1. O(n) time, O(1) space. Follow-up: elements appearing more than n/3 times (keep two candidates, then verify).

**Q. Problem 2: hints and answer key**

Hint 1: Why can't you zero cells as you scan? (New zeros would spread.) Hint 2: Record which rows and columns to clear first: O(m + n) space. Hint 3: Can the first row and first column store those marks? Answer: use row 0 and column 0 as marker arrays, with two booleans for whether row 0 and column 0 themselves contain a zero; mark, then clear from the bottom-right, then clear row 0 and column 0 last. O(mn) time, O(1) extra space.


**Traps**

- Interviewer gives the answer instead of a hint
- Candidate codes in silence
- Skipping the dry run because time is short

**Practise**

- [Majority Element](https://leetcode.com/problems/majority-element/)
- [Set Matrix Zeroes](https://leetcode.com/problems/set-matrix-zeroes/)

**Related:** [Hashing and frequency maps](dsa.md#hashing-and-frequency-maps) · [How to run a mock interview](#how-to-run-a-mock-interview)

[Back to the topic list](#topics)

## Mock 2: sliding window and binary search

*Level 2: Interview-ready*

The two patterns that appear most in online assessments.

**Key idea**

Format: 45 minutes, two Medium problems, about 18 minutes each, with time for questions.

Problem 1: Longest Repeating Character Replacement. Given a string of uppercase letters and an integer k, you may change at most k characters. Return the length of the longest substring of one repeated letter you can get.

Problem 2: Find Minimum in Rotated Sorted Array. A sorted array of distinct numbers was rotated. Find the minimum in O(log n).


**Points**

- Score each area 1 to 4: 1 = could not, 2 = with heavy hints, 3 = with a nudge, 4 = independently and clearly
- Problem solving: clarified, found an approach, improved it
- Code: correct, clean names, handles edge cases
- Communication: thought aloud, explained before coding, took hints well
- Testing: dry run, edge cases, complexity stated
- A pass is 3+ in every area. Log the scores in the tracker's Mocks tab

**Questions and model answers**

**Q. Problem 1: hints and answer key**

Hint 1: For a fixed window, how many changes does it need? (length − count of its most frequent letter.) Hint 2: Expand right; when the window needs more than k changes, shrink from the left. Hint 3: Does maxFreq ever need to decrease? (No: a smaller maxFreq can't produce a longer answer.) Answer: sliding window with a 26-count array and the best frequency seen; valid while (r − l + 1) − maxFreq ≤ k. O(n) time, O(1) space.

**Q. Problem 2: hints and answer key**

Hint 1: Compare a\[mid\] with which end? Hint 2: If a\[mid\] \> a\[hi\], where must the minimum be? Hint 3: Use lo \< hi and hi = mid (not mid − 1) on the other branch. Answer: while lo \< hi: mid = lo + (hi − lo)/2; if a\[mid\] \> a\[hi\] lo = mid + 1 else hi = mid; return a\[lo\]. O(log n). Follow-up: with duplicates, when a\[mid\] == a\[hi\] do hi−− (worst case O(n)).


**Traps**

- Interviewer gives the answer instead of a hint
- Candidate codes in silence
- Skipping the dry run because time is short

**Practise**

- [Longest Repeating Character Replacement](https://leetcode.com/problems/longest-repeating-character-replacement/)
- [Find Minimum in Rotated Sorted Array](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/)

**Related:** [Sliding window](dsa.md#sliding-window) · [Binary search](dsa.md#binary-search)

[Back to the topic list](#topics)

## Mock 3: trees and graphs

*Level 2: Interview-ready*

Trees and graphs are the largest topic in product-company loops.

**Key idea**

Format: 45 minutes, two Medium problems.

Problem 1: Binary Tree Right Side View. Return the values you would see looking at the tree from the right, top to bottom.

Problem 2: Clone Graph. Given a reference to a node in a connected undirected graph, return a deep copy of the graph.


**Points**

- Score each area 1 to 4: 1 = could not, 2 = with heavy hints, 3 = with a nudge, 4 = independently and clearly
- Problem solving: clarified, found an approach, improved it
- Code: correct, clean names, handles edge cases
- Communication: thought aloud, explained before coding, took hints well
- Testing: dry run, edge cases, complexity stated
- A pass is 3+ in every area. Log the scores in the tracker's Mocks tab

**Questions and model answers**

**Q. Problem 1: hints and answer key**

Hint 1: What do all the visible nodes have in common? (Last node on each level.) Hint 2: Which traversal gives you levels? Hint 3: Could DFS do it if it visits right before left and tracks depth? Answer: BFS level order, record the last node of each level; or DFS right-first, record a node when depth == result size. O(n) time.

**Q. Problem 2: hints and answer key**

Hint 1: What goes wrong if you copy neighbours naively? (Cycles: infinite recursion, duplicate copies.) Hint 2: Remember which original nodes already have a copy. Hint 3: A hash map from original to copy, filled as you traverse. Answer: DFS or BFS with unordered\_map\<Node\*, Node\*\>; create a copy on first visit, then connect copied neighbours. O(V + E) time and space. Follow-up: what if the graph is disconnected? (Start a traversal from every node.)


**Traps**

- Interviewer gives the answer instead of a hint
- Candidate codes in silence
- Skipping the dry run because time is short

**Practise**

- [Binary Tree Right Side View](https://leetcode.com/problems/binary-tree-right-side-view/)
- [Clone Graph](https://leetcode.com/problems/clone-graph/)

**Related:** [Binary trees](dsa.md#binary-trees) · [BFS and graph basics](dsa.md#bfs-and-graph-basics) · [DFS, components and cycles](dsa.md#dfs-components-and-cycles)

[Back to the topic list](#topics)

## Mock 4: dynamic programming

*Level 3: Advanced*

Product companies ask at least one DP; this mock checks you can define states out loud.

**Key idea**

Format: 45 minutes. Problem 1 is a warm-up DP (10 minutes), problem 2 is the main one (25 minutes).

Problem 1: Unique Paths. A robot in an m × n grid moves only right or down. How many paths from top-left to bottom-right?

Problem 2: Word Break. Given a string s and a dictionary of words, can s be split into a sequence of dictionary words?


**Points**

- Score each area 1 to 4: 1 = could not, 2 = with heavy hints, 3 = with a nudge, 4 = independently and clearly
- Problem solving: clarified, found an approach, improved it
- Code: correct, clean names, handles edge cases
- Communication: thought aloud, explained before coding, took hints well
- Testing: dry run, edge cases, complexity stated
- A pass is 3+ in every area. Log the scores in the tracker's Mocks tab

**Questions and model answers**

**Q. Problem 1: hints and answer key**

Hint 1: How can you arrive at a cell? Hint 2: Write dp\[i\]\[j\] from its neighbours. Hint 3: Do you need the whole table? Answer: dp\[i\]\[j\] = dp\[i−1\]\[j\] + dp\[i\]\[j−1\], first row and column are 1; one row of size n is enough. O(mn) time, O(n) space. Bonus: the answer is C(m+n−2, m−1).

**Q. Problem 2: hints and answer key**

Hint 1: Try a recursive split: is the first word in the dictionary, and can the rest be split? Hint 2: Which subproblems repeat? (Suffixes or prefixes.) Hint 3: Define dp\[i\] = can s\[0..i) be split. Answer: dp\[0\] = true; dp\[i\] = true if some j \< i has dp\[j\] and s\[j..i) in a hash set of words. O(n² ) checks (limit j to the longest word length). Follow-up: return all sentences (Word Break II: backtracking with memo).


**Traps**

- Jumping to a table before stating the state in words
- Wrong base case (dp\[0\])
- Not stating complexity

**Practise**

- [Unique Paths](https://leetcode.com/problems/unique-paths/)
- [Word Break](https://leetcode.com/problems/word-break/)

**Related:** [Dynamic programming](dsa.md#dynamic-programming) · [Recursion and backtracking](dsa.md#recursion-and-backtracking)

[Back to the topic list](#topics)

## Mock 5: Core CS viva

*Level 2: Interview-ready*

Many rounds spend 15 to 30 minutes on OS, DBMS, networks and OOP. This is a rapid-fire viva.

**Key idea**

Format: 30 minutes. The interviewer asks 8 of the questions below, about 3 minutes each, and pushes once with a follow-up ("why?", "give an example", "what breaks?").

The answers are in the Q&A pages of this Knowledge Base; below, each card lists only what a strong answer must include, so the interviewer can judge quickly.


**Points**

- Score each area 1 to 4: 1 = could not, 2 = with heavy hints, 3 = with a nudge, 4 = independently and clearly
- Problem solving: clarified, found an approach, improved it
- Code: correct, clean names, handles edge cases
- Communication: thought aloud, explained before coding, took hints well
- Testing: dry run, edge cases, complexity stated
- A pass is 3+ in every area. Log the scores in the tracker's Mocks tab

**Questions and model answers**

**Q. Process vs thread**

Must include: own address space vs shared; each thread has its own stack and registers; why threads are cheaper (no new address space, no TLB flush); the risk (shared-data bugs).

**Q. Deadlock: conditions and prevention**

All four conditions named; a concrete prevention (fixed lock order); mention of avoidance (Banker's) or detection.

**Q. Virtual memory and page faults**

Per-process address space, page tables, TLB; why (isolation, bigger than RAM, sharing); what happens on a fault; thrashing.

**Q. ACID and isolation levels**

Each letter with an example (bank transfer); dirty, non-repeatable and phantom reads; which level stops which.

**Q. Indexes and B+ trees**

Why a scan is slow; shallow wide tree, few page reads; range queries via linked leaves; the cost on writes.

**Q. Normalise this table**

Give Student(roll, name, dept, dept\_head). Must spot the transitive dependency and split into Student and Dept (3NF).

**Q. What happens when you type a URL**

DNS resolution chain, TCP handshake, TLS, HTTP request through load balancer/CDN, response, rendering. Bonus: caching at each step.

**Q. TCP vs UDP; why a 3-way handshake**

Reliability features of TCP; UDP use cases; why two messages are not enough (both sides must confirm sequence numbers).

**Q. Virtual functions and the vtable**

vtable per class, vptr per object, one indirection; why base destructors must be virtual.

**Q. SQL: second-highest salary per department**

DENSE\_RANK() OVER (PARTITION BY dept ORDER BY salary DESC) = 2, and why DENSE\_RANK over RANK for ties.


**Traps**

- Answers that are definitions with no example
- Panicking at a follow-up instead of reasoning aloud

**Related:** [Operating systems: model answers](q-a.md#operating-systems-model-answers) · [DBMS and SQL: model answers](q-a.md#dbms-and-sql-model-answers) · [Computer networks: model answers](q-a.md#computer-networks-model-answers) · [OOP and C++: model answers](q-a.md#oop-and-c-model-answers)

[Back to the topic list](#topics)

## Mock 6: low-level design (parking lot)

*Level 2: Interview-ready*

Flipkart, Swiggy, Razorpay and others run an LLD or machine-coding round; the parking lot is the classic.

**Key idea**

Format: 45 minutes. Prompt: "Design a parking lot system." The candidate should spend the first 5 minutes asking questions, then draw classes, then code the core in C++.

The interviewer answers questions with these requirements: multiple floors; spot sizes small, medium, large; vehicles bike, car, truck; tickets with entry time; payment by hours at a per-size rate; show free spots per floor.


**Points**

- Score each area 1 to 4: 1 = could not, 2 = with heavy hints, 3 = with a nudge, 4 = independently and clearly
- Problem solving: clarified, found an approach, improved it
- Code: correct, clean names, handles edge cases
- Communication: thought aloud, explained before coding, took hints well
- Testing: dry run, edge cases, complexity stated
- A pass is 3+ in every area. Log the scores in the tracker's Mocks tab

**Questions and model answers**

**Q. Classes a good design has**

ParkingLot (floors), Floor (spots, free counts), Spot (id, size, occupied), Vehicle with a type, Ticket (id, vehicle, spot, entry time), a PricingStrategy interface (per-size hourly rates), an EntryGate/ExitGate or ParkingService that assigns spots and closes tickets. Enums for sizes and vehicle types.

**Q. Follow-up questions to ask**

1) Add electric-vehicle spots with charging. Does the design extend without editing old classes? (open/closed) 2) Two cars arrive at the same moment at two gates: how do you avoid giving both the same spot? (lock per floor or atomic claim) 3) Change pricing on weekends: where does that live? (strategy) 4) How would you find the nearest free spot quickly? (per-size min-heaps or free lists per floor)

**Q. Red flags**

One giant class; no enums; pricing hard-coded inside the ticket; ignoring concurrency when asked; coding before agreeing on requirements.


**Traps**

- Interviewer gives the answer instead of a hint
- Candidate codes in silence
- Skipping the dry run because time is short

**Practise**

- [awesome-low-level-design](https://github.com/ashishps1/awesome-low-level-design)

**Related:** [Low-level design (LLD)](design.md#low-level-design-lld) · [SOLID and design patterns](core-cs.md#solid-and-design-patterns) · [OOP: the four pillars](core-cs.md#oop-the-four-pillars)

[Back to the topic list](#topics)

## Mock 7: system design (URL shortener)

*Level 3: Advanced*

Big Tech asks light HLD of freshers; your AWS prep makes this your strong round.

**Key idea**

Format: 45 minutes. Prompt: "Design a URL shortener like bit.ly." Expect: requirements, numbers, API, data model, diagram, one deep dive, trade-offs.

Numbers to give if asked: 100 million new links a month, 10:1 read to write, links kept 5 years.


**Points**

- Score each area 1 to 4: 1 = could not, 2 = with heavy hints, 3 = with a nudge, 4 = independently and clearly
- Problem solving: clarified, found an approach, improved it
- Code: correct, clean names, handles edge cases
- Communication: thought aloud, explained before coding, took hints well
- Testing: dry run, edge cases, complexity stated
- A pass is 3+ in every area. Log the scores in the tracker's Mocks tab

**Questions and model answers**

**Q. What a strong answer covers**

Back-of-envelope: about 40 writes/s and 400 reads/s; 6 billion links over 5 years; a 7-character base62 key gives 3.5 trillion combinations. API: POST /shorten, GET /{key} → 301/302 redirect. Data: key → long URL, created\_at, owner. Key generation: counter + base62, or a pre-generated key service; avoid hash collisions. Storage: a key-value store or sharded SQL by key. Read path: cache (Redis) in front, CDN for hot links. Extras: rate limiting, analytics via a queue, expiry.

**Q. Deep-dive questions**

1) How do two servers avoid issuing the same key? (ranges from a key service, or a central counter with batches) 2) A link goes viral: what fails first and how do you protect it? (cache, CDN) 3) 301 vs 302: which do you use and why? (302 if you want analytics) 4) How would you stop people shortening malicious URLs? (allow-list checks, Safe Browsing-style lookups, rate limits)

**Q. Red flags**

No numbers; jumping to microservices; hashing without handling collisions; no cache for a read-heavy system.


**Traps**

- Interviewer gives the answer instead of a hint
- Candidate codes in silence
- Skipping the dry run because time is short

**Practise**

- [System Design Primer](https://github.com/donnemartin/system-design-primer)

**Related:** [High-level system design (HLD)](design.md#high-level-system-design-hld) · [Caching and CDNs](design.md#caching-and-cdns) · [Load balancing, replication and sharding](design.md#load-balancing-replication-and-sharding)

[Back to the topic list](#topics)

## Mock 8: behavioural and project deep dive

*Level 2: Interview-ready*

Amazon's bar raiser and every HR round. Your TenantWall story should be your strongest answer.

**Key idea**

Format: 40 minutes. 20 minutes of behavioural questions (STAR), 20 minutes of the interviewer drilling into one project.

The interviewer pushes on every answer with "What exactly did you do?", "What was the result, in numbers?" and "What would you change?".


**Points**

- Score each area 1 to 4: 1 = could not, 2 = with heavy hints, 3 = with a nudge, 4 = independently and clearly
- Problem solving: clarified, found an approach, improved it
- Code: correct, clean names, handles edge cases
- Communication: thought aloud, explained before coding, took hints well
- Testing: dry run, edge cases, complexity stated
- A pass is 3+ in every area. Log the scores in the tracker's Mocks tab

**Questions and model answers**

**Q. Behavioural prompts**

1) Tell me about yourself (60 seconds). 2) A time you failed. 3) A conflict in a team. 4) Something you learned fast. 5) A time you went beyond what was asked. 6) Why this company? Listen for: Situation in one line, most time on Actions in 'I' not 'we', a Result with a number, a lesson.

**Q. Project deep dive: TenantWall**

Ask: What problem does it solve? Why ABAC instead of a role per tenant? Show me the policy condition. How did you prove tenant A cannot read tenant B's data? What does the CloudWatch alarm catch, and how fast? What breaks at 1,000 tenants? What would an attacker try first? Listen for: a clear diagram in words, real test evidence, honest limits.

**Q. Project deep dive: AI-security project**

Ask: How does retrieval work? How did you measure answer quality? Which prompt-injection attack worked best, and why? What defence stopped it, and what does it still miss? Listen for: numbers from the eval set and an honest list of remaining gaps.


**Traps**

- Talking about the team instead of your own actions
- No numbers
- Defensive answers to 'what would you change?'

**Related:** [Behavioural interviews and STAR stories](career.md#behavioural-interviews-and-star-stories) · [TenantWall (your research project)](cloud.md#tenantwall-your-research-project) · [Projects that get shortlisted](career.md#projects-that-get-shortlisted)

[Back to the topic list](#topics)
