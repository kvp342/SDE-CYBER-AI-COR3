INTERVIEWS · PRACTICE WITH A FRIEND

# Mock interview scripts

Six scripts a friend can run without being an expert: what to say, how long each part takes, which hints to give and in what order, and a rubric to score you. Swap roles afterwards: interviewing someone else teaches you what interviewers notice.

**Rules.** Camera on, timer visible, no notes. The interviewer writes down every hint given and the time stamps. Score right after, then talk for 10 minutes: one thing to keep, one thing to fix. Repeat a script after two weeks with different problems from the same pattern.

|                                           |        |
|-------------------------------------------|--------|
| [DSA mock 1: stacks and strings](#dsa-mock-1-stacks-and-strings-45-minutes) | 45 min |
| [DSA mock 2: graphs](#dsa-mock-2-graphs-45-minutes)             | 45 min |
| [Core CS mock](#core-cs-mock-30-minutes)                  | 30 min |
| [LLD mock: rate limiter](#lld-mock-rate-limiter-45-minutes)        | 45 min |
| [Security mock](#security-mock-30-minutes)                 | 30 min |
| [HR and behavioural mock](#hr-and-behavioural-mock-30-minutes)       | 30 min |

### Scoring

Each rubric line is scored 1 (weak) to 4 (strong). 17–20: ready; 13–16: close, fix the lowest line; 12 or below: repeat the related practice before the next mock. Each hint used costs nothing in the score but note it: hints you needed show what to revise.

## DSA mock 1: stacks and strings 45 minutes

Interviewer: share a blank editor (no autocomplete) or paper. Candidate codes in C++. Reference answers: [Decode String](https://leetcode.com/problems/decode-string/) (Worked Solutions II), [Sliding Window Maximum](https://leetcode.com/problems/sliding-window-maximum/) (Worked Solutions II).

### Script

|        |                                   |                                                                                                                                                                                                                |
|--------|-----------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 2 min  | Intro                             | "Tell me briefly about yourself and the language you'll use."                                                                                                                                                  |
| 18 min | Problem 1: Decode String          | Say: "Given an encoded string like 3\[a2\[c\]\], return its decoded form: accaccacc. Numbers before brackets repeat the bracketed part." Expected: a stack of (string so far, repeat count), O(output length). |
| 18 min | Problem 2: Sliding Window Maximum | Say: "Given an array and k, return the maximum of every window of size k." Expected: monotonic deque of indices, O(n). Accept an O(n log k) heap first, then ask for O(n).                                     |
| 5 min  | Follow-ups                        | Ask: "Why is the deque solution O(n) even with a while loop inside?" and "What if counts can have several digits in Decode String?"                                                                            |
| 2 min  | Candidate's questions             | Let them ask one question; answer briefly.                                                                                                                                                                     |

### Hints, in order

- Problem 1: "What do you need to remember when you see '\['?" → "What if you pushed the current string and the number?"
- Problem 2: "Which elements can never be the maximum again?" → "Keep indices in a structure where values decrease."
- If stuck for 4 minutes, give the next hint; note each hint given.

### Rubric

|                       |                                                                                          |               |
|-----------------------|------------------------------------------------------------------------------------------|---------------|
| Problem understanding | Restated the problem, asked about input size, edge cases and output format before coding | 1 · 2 · 3 · 4 |
| Approach              | Gave a brute force, then a better idea, with complexity, before coding                   | 1 · 2 · 3 · 4 |
| Code                  | Correct, readable, sensible names; no long silences                                      | 1 · 2 · 3 · 4 |
| Testing               | Walked through an example and edge cases without being asked; found own bugs             | 1 · 2 · 3 · 4 |
| Communication         | Thought aloud; took hints well; explained trade-offs                                     | 1 · 2 · 3 · 4 |
| Total                 |                                                                                          | \_\_\_\_ / 20 |

Notes and time stamps:

## DSA mock 2: graphs 45 minutes

Same setup. Draw small graphs on paper if needed. Reference answers: [Course Schedule II](https://leetcode.com/problems/course-schedule-ii/) (Worked Solutions II), [Cheapest Flights Within K Stops](https://leetcode.com/problems/cheapest-flights-within-k-stops/) (Worked Solutions II).

### Script

|        |                                            |                                                                                                                                                                                                                                        |
|--------|--------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 2 min  | Intro                                      | Warm-up: "What's a graph problem you solved recently?"                                                                                                                                                                                 |
| 20 min | Problem 1: Course Schedule II              | Say: "n courses, prerequisite pairs \[a, b\] meaning b before a. Return an order to take all courses, or empty if impossible." Expected: Kahn's algorithm (BFS on in-degree 0), detect a cycle when fewer than n are output, O(V + E). |
| 18 min | Problem 2: Cheapest Flights Within K Stops | Say: "Given flights with prices, find the cheapest price from src to dst with at most k stops, or −1." Expected: Bellman–Ford for k + 1 rounds using a copy of the previous round, or Dijkstra on (cost, node, stops).                 |
| 3 min  | Follow-ups                                 | Ask: "Why does plain Dijkstra fail here?" and "How would you detect the cycle with DFS instead?"                                                                                                                                       |
| 2 min  | Candidate's questions                      |                                                                                                                                                                                                                                        |

### Hints, in order

- Problem 1: "Which courses can you take first?" → "What happens to other courses when you finish one?"
- Problem 2: "What does 'at most k stops' limit?" → "Can you relax edges only k + 1 times?" → "Why must each round read the previous round's costs?"

### Rubric

|                       |                                                                                          |               |
|-----------------------|------------------------------------------------------------------------------------------|---------------|
| Problem understanding | Restated the problem, asked about input size, edge cases and output format before coding | 1 · 2 · 3 · 4 |
| Approach              | Gave a brute force, then a better idea, with complexity, before coding                   | 1 · 2 · 3 · 4 |
| Code                  | Correct, readable, sensible names; no long silences                                      | 1 · 2 · 3 · 4 |
| Testing               | Walked through an example and edge cases without being asked; found own bugs             | 1 · 2 · 3 · 4 |
| Communication         | Thought aloud; took hints well; explained trade-offs                                     | 1 · 2 · 3 · 4 |
| Total                 |                                                                                          | \_\_\_\_ / 20 |

Notes and time stamps:

## Core CS mock 30 minutes

Interviewer reads the questions; candidate answers aloud, with a whiteboard for diagrams. Use the Core CS one-pagers to check answers. Reference answers: [Operating systems: model answers](knowledge-base/q-a.md#operating-systems-model-answers) (Knowledge Base), [DBMS and SQL: model answers](knowledge-base/q-a.md#dbms-and-sql-model-answers) (Knowledge Base), [Computer networks: model answers](knowledge-base/q-a.md#computer-networks-model-answers) (Knowledge Base), [OOP: the four pillars](knowledge-base/core-cs.md#oop-the-four-pillars) (Knowledge Base).

### Script

|       |                   |                                                                                                                                                   |
|-------|-------------------|---------------------------------------------------------------------------------------------------------------------------------------------------|
| 8 min | Operating systems | Ask: process vs thread; the four deadlock conditions and one way to prevent each; what happens on a page fault.                                   |
| 8 min | DBMS and SQL      | Ask: ACID with a bank-transfer example; dirty read vs phantom read and which isolation level stops each; write SQL for the second-highest salary. |
| 8 min | Networks          | Ask: what happens when you type a URL (from DNS to rendering); TCP vs UDP with examples; how TLS uses both asymmetric and symmetric encryption.   |
| 6 min | OOP               | Ask: how virtual functions work (vtable); why a base class needs a virtual destructor; one SOLID principle with an example from their project.    |

### Hints, in order

- Give a hint only after 1 minute of silence, and only one per question: for example "think about what each transaction sees".

### Rubric

|           |                                                                    |               |
|-----------|--------------------------------------------------------------------|---------------|
| Accuracy  | Facts correct; no confident wrong statements                       | 1 · 2 · 3 · 4 |
| Depth     | Went one level below the definition (an example, a why)            | 1 · 2 · 3 · 4 |
| Structure | Answers organised: definition → example → trade-off                | 1 · 2 · 3 · 4 |
| Honesty   | Said 'I'm not sure, but I think…' instead of bluffing              | 1 · 2 · 3 · 4 |
| Diagrams  | Used a quick sketch where it helps (process states, TCP handshake) | 1 · 2 · 3 · 4 |
| Total     |                                                                    | \_\_\_\_ / 20 |

Notes and time stamps:

## LLD mock: rate limiter 45 minutes

Candidate designs and codes a per-client rate limiter in C++. Compare afterwards with lld/rate_limiter.cpp in the kit. Reference answers: [Low-level design (LLD)](knowledge-base/design.md#low-level-design-lld) (Knowledge Base).

### Script

|        |              |                                                                                                                                                                                                           |
|--------|--------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 7 min  | Requirements | Say: "Design a rate limiter for an API: each client may make at most N requests per window." Let the candidate ask: burst allowed? exact or approximate? one server or many? What to return when limited? |
| 10 min | Design       | Expect: an interface allow(client), at least two algorithms (token bucket, sliding window), per-client state in a hash map, injectable clock for tests.                                                   |
| 20 min | Code         | Expect working code for one algorithm, thread-safe (mutex), plus a short test with a fake clock.                                                                                                          |
| 8 min  | Extensions   | Ask: "How would this work across 10 servers?" (Redis with atomic operations or a gateway) and "What HTTP response do you send?" (429 with Retry-After).                                                   |

### Hints, in order

- "How will you test time-based behaviour without sleeping?" → injected clock.
- "What happens if two threads call allow at once?"

### Rubric

|              |                                                  |               |
|--------------|--------------------------------------------------|---------------|
| Requirements | Asked the questions that change the design       | 1 · 2 · 3 · 4 |
| Abstractions | Clean interface; algorithms swappable (Strategy) | 1 · 2 · 3 · 4 |
| Correctness  | Window and refill maths right; no data races     | 1 · 2 · 3 · 4 |
| Testability  | Clock injected; a real test written              | 1 · 2 · 3 · 4 |
| Trade-offs   | Compared algorithms: memory, accuracy, bursts    | 1 · 2 · 3 · 4 |
| Total        |                                                  | \_\_\_\_ / 20 |

Notes and time stamps:

## Security mock 30 minutes

For security or security-aware SDE roles. Interviewer uses the lab map's interview questions and the TenantWall helpers. Reference answers: [OWASP Top 10](knowledge-base/security.md#owasp-top-10) (Knowledge Base), [TenantWall (your research project)](knowledge-base/cloud.md#tenantwall-your-research-project) (Knowledge Base), [ABAC: attribute-based access control](knowledge-base/cloud.md#abac-attribute-based-access-control) (Knowledge Base).

### Script

|        |                       |                                                                                                                                                                                                                        |
|--------|-----------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 8 min  | Project deep dive     | Ask: "Explain TenantWall. How does ABAC stop tenant A reading tenant B's data? How did you prove it? What does the alarm catch, and how fast?"                                                                         |
| 10 min | Web security          | Ask three: SQL injection prevention; stored vs reflected XSS; CSRF and SameSite cookies; SSRF in the cloud; IDOR.                                                                                                      |
| 7 min  | Scenario              | Say: "A login endpoint is being brute-forced. What do you do in the next hour, and what do you change long-term?" Expect: rate limiting, lockouts or CAPTCHA, alerting, MFA, checking logs for success after failures. |
| 5 min  | Candidate's questions |                                                                                                                                                                                                                        |

### Hints, in order

- For the scenario: "What would you look for in the logs?"

### Rubric

|                  |                                                               |               |
|------------------|---------------------------------------------------------------|---------------|
| Project depth    | Explains design, tests and limits of TenantWall clearly       | 1 · 2 · 3 · 4 |
| Fundamentals     | Correct causes and fixes for web vulnerabilities              | 1 · 2 · 3 · 4 |
| Defence in depth | Proposes layers, not one fix                                  | 1 · 2 · 3 · 4 |
| Ethics           | Mentions permission and responsible disclosure where relevant | 1 · 2 · 3 · 4 |
| Clarity          | Explains to a non-specialist when asked                       | 1 · 2 · 3 · 4 |
| Total            |                                                               | \_\_\_\_ / 20 |

Notes and time stamps:

## HR and behavioural mock 30 minutes

Use the interview story bank. Interviewer asks; candidate answers in STAR form, about 2 minutes each. Reference answers: [Behavioural interviews and STAR stories](knowledge-base/career.md#behavioural-interviews-and-star-stories) (Knowledge Base).

### Script

|        |                       |                                                                                                                                                                                                                                             |
|--------|-----------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 5 min  | Opening               | "Tell me about yourself." "Why this company?"                                                                                                                                                                                               |
| 18 min | Behavioural           | Pick four: a project you are proud of; a time you failed; a disagreement; learning something fast; going beyond the task; helping someone. After each, ask one follow-up: "What would you do differently?" or "What did you personally do?" |
| 5 min  | HR                    | "Strengths and a weakness?" "Where do you see yourself in five years?" "Are you open to relocating?"                                                                                                                                        |
| 2 min  | Candidate's questions |                                                                                                                                                                                                                                             |

### Hints, in order

- If an answer drifts into 'we', ask: "What was your part?"

### Rubric

|            |                                                 |               |
|------------|-------------------------------------------------|---------------|
| Structure  | Clear STAR; result stated                       | 1 · 2 · 3 · 4 |
| Ownership  | Uses 'I' for own actions; credits others fairly | 1 · 2 · 3 · 4 |
| Evidence   | Concrete details and numbers                    | 1 · 2 · 3 · 4 |
| Reflection | Real learning, not a disguised strength         | 1 · 2 · 3 · 4 |
| Length     | About 2 minutes; stops when done                | 1 · 2 · 3 · 4 |
| Total      |                                                 | \_\_\_\_ / 20 |

Notes and time stamps:
