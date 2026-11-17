INTERVIEWS · PRACTICE WITH A FRIEND · II

# Mock interview scripts II

Six more scripts (DP on strings, trees and grids, OS and networks, system design, a TenantWall grilling and a security scenario) a friend can run without being an expert: what to say, how long each part takes, which hints to give and in what order, and a rubric to score you. Swap roles afterwards: interviewing someone else teaches you what interviewers notice.

**Rules.** Camera on, timer visible, no notes. The interviewer writes down every hint given and the time stamps. Score right after, then talk for 10 minutes: one thing to keep, one thing to fix. Repeat a script after two weeks with different problems from the same pattern.

|                                           |        |
|-------------------------------------------|--------|
| [DSA mock 3: DP on strings](#dsa-mock-3-dp-on-strings-45-minutes)      | 45 min |
| [DSA mock 4: trees and grids](#dsa-mock-4-trees-and-grids-45-minutes)    | 45 min |
| [OS and networks deep dive](#os-and-networks-deep-dive-30-minutes)     | 30 min |
| [System design (fresher level)](#system-design-fresher-level-40-minutes) | 40 min |
| [TenantWall project grilling](#tenantwall-project-grilling-30-minutes)   | 30 min |
| [Security scenario round](#security-scenario-round-30-minutes)       | 30 min |

### Scoring

Each rubric line is scored 1 (weak) to 4 (strong). 17–20: ready; 13–16: close, fix the lowest line; 12 or below: repeat the related practice before the next mock. Each hint used costs nothing in the score but note it: hints you needed show what to revise.

## DSA mock 3: DP on strings 45 minutes

Shared editor without autocomplete, or paper. Candidate codes in C++. Reference answers: [Word Break](https://leetcode.com/problems/word-break/) (Worked Solutions II), [Decode Ways](https://leetcode.com/problems/decode-ways/) (Worked Solutions II).

### Script

|        |                        |                                                                                                                                                                                                |
|--------|------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 2 min  | Intro                  | "Which DP problem did you find hardest so far, and why?"                                                                                                                                       |
| 18 min | Problem 1: Word Break  | Say: "Given a string and a dictionary, can the string be split into dictionary words?" Expected: dp\[i\] = prefix of length i can be split; check every j \< i; a hash set for the dictionary. |
| 18 min | Problem 2: Decode Ways | Say: "A message of digits encodes letters A=1 … Z=26. Count the ways to decode it." Expected: dp over prefixes; one-digit step if not '0', two-digit step if 10–26.                            |
| 5 min  | Follow-ups             | Ask: "Return all sentences for Word Break (II): what changes and what is the worst case?" and "Make Decode Ways O(1) space."                                                                   |
| 2 min  | Candidate's questions  |                                                                                                                                                                                                |

### Hints, in order

- Problem 1: "What does it mean for a prefix to be breakable?" → "If dp\[j\] is true, what must hold for dp\[i\]?"
- Problem 2: "What does a '0' do?" → "How is this like climbing stairs?"

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

## DSA mock 4: trees and grids 45 minutes

Same setup. Let the candidate draw the tree and the grid. Reference answers: [Construct Binary Tree from Preorder and Inorder](https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/) (Worked Solutions II), [Pacific Atlantic Water Flow](https://leetcode.com/problems/pacific-atlantic-water-flow/) (Worked Solutions II).

### Script

|        |                                                 |                                                                                                                                                                                                        |
|--------|-------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 2 min  | Intro                                           | Warm-up: "Preorder, inorder, postorder: which one gives sorted order in a BST?"                                                                                                                        |
| 20 min | Problem 1: Build tree from preorder and inorder | Say: "Rebuild a binary tree from its preorder and inorder traversals (values are unique)." Expected: first preorder value is the root; its inorder index splits left and right; a hash map gives O(n). |
| 18 min | Problem 2: Pacific Atlantic Water Flow          | Say: "Water flows to equal or lower neighbours. Which cells can reach both oceans?" Expected: search backwards from each ocean's border (uphill), intersect the two reachable sets.                    |
| 3 min  | Follow-ups                                      | Ask: "Why search from the oceans instead of from every cell?" and "Build from inorder and postorder instead."                                                                                          |
| 2 min  | Candidate's questions                           |                                                                                                                                                                                                        |

### Hints, in order

- Problem 1: "Where is the root in preorder?" → "How do you find it in inorder quickly?"
- Problem 2: "Is it easier to ask where water can come from?"

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

## OS and networks deep dive 30 minutes

One topic is followed down three levels of 'why'. Check answers against the Core CS one-pagers. Reference answers: [Operating systems: model answers](knowledge-base/q-a.md#operating-systems-model-answers) (Knowledge Base), [Computer networks: model answers](knowledge-base/q-a.md#computer-networks-model-answers) (Knowledge Base), [Memory management and virtual memory](knowledge-base/core-cs.md#memory-management-and-virtual-memory) (Knowledge Base), [TCP vs UDP and the handshake](knowledge-base/core-cs.md#tcp-vs-udp-and-the-handshake) (Knowledge Base).

### Script

|        |             |                                                                                                                                                                                    |
|--------|-------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 10 min | Memory      | Ask: what happens on a page fault, step by step; why a TLB helps; what thrashing is and how to fix it. Then: "Why does a fork() not copy all memory immediately?" (copy-on-write). |
| 10 min | Concurrency | Ask: process vs thread; a race condition example; mutex vs semaphore; the four deadlock conditions and how to break one.                                                           |
| 10 min | Networks    | Ask: what happens when you type a URL; TCP handshake and why three steps; how TLS combines asymmetric and symmetric crypto; what a /26 subnet gives you.                           |

### Hints, in order

- Only after a minute of silence: "Start from what the CPU sees." or "Think about what each side knows after each message."

### Rubric

|             |                                                 |               |
|-------------|-------------------------------------------------|---------------|
| Accuracy    | No confident wrong statements                   | 1 · 2 · 3 · 4 |
| Depth       | Could go three levels of 'why'                  | 1 · 2 · 3 · 4 |
| Clarity     | Simple language, a quick sketch where useful    | 1 · 2 · 3 · 4 |
| Connections | Linked theory to real systems (Linux, browsers) | 1 · 2 · 3 · 4 |
| Honesty     | Said when unsure                                | 1 · 2 · 3 · 4 |
| Total       |                                                 | \_\_\_\_ / 20 |

Notes and time stamps:

## System design (fresher level) 40 minutes

Use the URL shortener or notification service from the system design case studies as the reference answer. Reference answers: [High-level system design (HLD)](knowledge-base/design.md#high-level-system-design-hld) (Knowledge Base), [Caching and CDNs](knowledge-base/design.md#caching-and-cdns) (Knowledge Base), [Load balancing, replication and sharding](knowledge-base/design.md#load-balancing-replication-and-sharding) (Knowledge Base).

### Script

|        |                   |                                                                                                                   |
|--------|-------------------|-------------------------------------------------------------------------------------------------------------------|
| 6 min  | Requirements      | Say: "Design a URL shortener." Let the candidate ask about scale, custom aliases, expiry and analytics.           |
| 6 min  | Estimates         | Expect requests per second for reads and writes, and storage for five years, with stated assumptions.             |
| 14 min | High-level design | Expect API, data model, ID generation, cache, database choice and a diagram.                                      |
| 10 min | Deep dive         | Pick one: ID generation without collisions, or handling a hot link, or counting clicks without slowing redirects. |
| 4 min  | Wrap-up           | Ask: "What breaks first at 10× traffic?"                                                                          |

### Hints, in order

- "What is the read to write ratio?"
- "Where would you put a cache, and what would you store?"

### Rubric

|               |                                                 |               |
|---------------|-------------------------------------------------|---------------|
| Requirements  | Asked before designing                          | 1 · 2 · 3 · 4 |
| Estimates     | Numbers with assumptions                        | 1 · 2 · 3 · 4 |
| Design        | Clear components and data flow                  | 1 · 2 · 3 · 4 |
| Trade-offs    | Explained choices (301 vs 302, counter vs hash) | 1 · 2 · 3 · 4 |
| Communication | Drew and narrated                               | 1 · 2 · 3 · 4 |
| Total         |                                                 | \_\_\_\_ / 20 |

Notes and time stamps:

## TenantWall project grilling 30 minutes

The interviewer reads the TenantWall helpers and paper outline beforehand and keeps asking 'how do you know?'. Reference answers: [TenantWall (your research project)](knowledge-base/cloud.md#tenantwall-your-research-project) (Knowledge Base), [ABAC: attribute-based access control](knowledge-base/cloud.md#abac-attribute-based-access-control) (Knowledge Base), [CloudTrail and CloudWatch alarms](knowledge-base/cloud.md#cloudtrail-and-cloudwatch-alarms) (Knowledge Base).

### Script

|        |          |                                                                                                                                                         |
|--------|----------|---------------------------------------------------------------------------------------------------------------------------------------------------------|
| 5 min  | Pitch    | "Explain TenantWall in two minutes to someone who has not heard of ABAC."                                                                               |
| 10 min | Design   | Ask: why ABAC and not one role per tenant; what stops a tenant changing its own tag; why the explicit deny is separate; what DescribeInstances exposes. |
| 10 min | Evidence | Ask: how many isolation tests, what each showed, the alert delay and how you measured it, what it costs per month.                                      |
| 5 min  | Limits   | Ask: what would break at 1,000 tenants; what you would do differently; what you learned.                                                                |

### Hints, in order

- If vague: "Show me the exact condition in the policy."

### Rubric

|           |                                                     |               |
|-----------|-----------------------------------------------------|---------------|
| Clarity   | Two-minute pitch a non-expert understands           | 1 · 2 · 3 · 4 |
| Depth     | Policy-level detail without notes                   | 1 · 2 · 3 · 4 |
| Evidence  | Real numbers from real tests                        | 1 · 2 · 3 · 4 |
| Limits    | Names weaknesses honestly                           | 1 · 2 · 3 · 4 |
| Ownership | Clear about own contribution versus the professor's | 1 · 2 · 3 · 4 |
| Total     |                                                     | \_\_\_\_ / 20 |

Notes and time stamps:

## Security scenario round 30 minutes

For security-aware SDE roles. The interviewer plays an engineer on call; use the lab map and lab notebook as references. Reference answers: [OWASP Top 10](knowledge-base/security.md#owasp-top-10) (Knowledge Base), [SQL injection](knowledge-base/security.md#sql-injection) (Knowledge Base), [Cross-site scripting (XSS) and CSRF](knowledge-base/security.md#cross-site-scripting-xss-and-csrf) (Knowledge Base).

### Script

|        |             |                                                                                                                                                                                                                                                                                     |
|--------|-------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 10 min | Incident    | Say: "Our login API shows 5,000 failed logins a minute from many IPs, and two accounts later logged in successfully. Walk me through the next hour." Expect: contain (rate limits, lock affected accounts), investigate logs, notify, then fix (MFA, credential-stuffing defences). |
| 12 min | Code review | Show a short handler that builds SQL from a query parameter and echoes a name into HTML. Ask the candidate to find the issues (SQL injection, XSS, missing ownership check) and fix them.                                                                                           |
| 8 min  | Design      | Ask: "How would you store passwords and sessions for this app?" and "What would you log, and what must you never log?"                                                                                                                                                              |

### Hints, in order

- "Which accounts are at risk right now?"
- "Where does user input reach a query or a page?"

### Rubric

|                |                                           |               |
|----------------|-------------------------------------------|---------------|
| Prioritisation | Contained before investigating            | 1 · 2 · 3 · 4 |
| Accuracy       | Correct causes and fixes                  | 1 · 2 · 3 · 4 |
| Depth          | Layers of defence, not one fix            | 1 · 2 · 3 · 4 |
| Communication  | Clear steps under pressure                | 1 · 2 · 3 · 4 |
| Ethics         | Mentions disclosure and user notification | 1 · 2 · 3 · 4 |
| Total          |                                           | \_\_\_\_ / 20 |

Notes and time stamps:
