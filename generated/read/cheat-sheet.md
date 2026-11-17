Prep Cheat Sheet

[Cheat sheet](#the-rules)

[Rules](#the-rules)[Complexity](#complexity)[C++](#c-and-the-stl)[Patterns](#pattern-triggers)[Templates](#templates)[DP](#dp-recipe)[Core CS](#core-cs)[SQL](#sql)[Security](#security)[AWS](#aws)[Interviews](#interviews)[Knowledge ↗](knowledge-base/README.md)

Placement prep · one page

# Prep cheat sheet

The rules, the triggers and the templates. Read the first section before every session, and the whole page before every test.

Read before every session

## The rules

### The problem loop

1.  **Restate** the input, output and constraints. One example by hand. (3 min)
2.  **Brute force** and its Big-O. (5 min)
3.  **Optimise:** sort? hash? two pointers? binary search the answer? repeated work? a graph? (10 to 20 min)
4.  **Code** it in one go. (10 to 15 min)
5.  **Test** the sample and two edge cases. (5 min)
6.  **Log** the pattern, the time, S/H/F and the mistake. (1 min)

### When stuck

- 30 minutes alone, then a hint only
- 60 minutes, then the solution: close it and code from memory
- Re-solve at 1, 3, 7 and 21 days
- Mark it S (solved), H (hint) or F (failed)

### Never zero

- Minimum day: revision, 2 Striver, 1 LeetCode, 20 min of flashcards
- Short on time, cut: the Elite HFT track (if open), the CP habit, the AI-security project, then cyber. Never DSA or revision.

### Edge cases to try

- Empty input, one element, two elements
- All equal, already sorted, reverse sorted
- Negative numbers and zero
- The largest n and the largest values (overflow)
- Duplicates; the target missing
- Trees: empty, one node, a straight line
- Graphs: disconnected, a self-loop, a cycle

Constraints name the algorithm

## Complexity

| n up to        | Aim for           | Typical technique                          |
|----------------|-------------------|--------------------------------------------|
| 10 to 12       | O(n!)             | Permutations, backtracking                 |
| 20 to 25       | O(2ⁿ)             | Bitmask, subsets, meet in the middle       |
| 100            | O(n³) or O(n⁴)    | Floyd-Warshall, interval DP                |
| 1,000 to 5,000 | O(n²)             | 2D DP, nested loops                        |
| 10⁵            | O(n log n)        | Sorting, heap, binary search, segment tree |
| 10⁶ to 10⁷     | O(n)              | Two pointers, hashing, prefix sums, sieve  |
| 10⁹ to 10¹⁸    | O(log n) or O(√n) | Binary search, maths, fast power           |

- About **10⁸ simple operations per second**
- `int` holds about ±2.1×10⁹. Anything bigger: `long long` (about ±9.2×10¹⁸)
- Overflow happens in the expression: write `1LL * a * b`
- Mid without overflow: `lo + (hi - lo) / 2`
- Modulo: `((a % M) + M) % M` for negatives; `M = 1e9 + 7`
- Recursion deeper than about 10⁵ risks a stack overflow
- `sort` is O(n log n); `map` and `set` are O(log n) per operation; `unordered_map` is O(1) on average
- A loop that halves or doubles runs log n times; `i*i <= n` runs √n times

What you need from C++

## C++ and the STL

``` cpp
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;

int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n; cin >> n;
    vector<int> a(n);
    for (int &x : a) cin >> x;
    cout << accumulate(a.begin(), a.end(), 0LL) << "\n";
}
```

Starter

| Container            | Use it for                | Key calls                                 |
|----------------------|---------------------------|-------------------------------------------|
| `vector<T>`          | Dynamic array             | `push_back pop_back back size [i]`        |
| `string`             | Text                      | `size substr(i,len) find += `             |
| `pair<A,B>`          | Two values                | `.first .second`                          |
| `stack<T>`           | Last in, first out        | `push pop top empty`                      |
| `queue<T>`           | First in, first out (BFS) | `push pop front empty`                    |
| `deque<T>`           | Both ends                 | `push_front push_back pop_front pop_back` |
| `priority_queue<T>`  | Max-heap                  | `push pop top`                            |
| `set<T>`             | Sorted unique             | `insert erase count lower_bound`          |
| `map<K,V>`           | Sorted key to value       | `m[k] count find erase`                   |
| `unordered_map<K,V>` | Hash map, O(1) average    | `m[k] count find`                         |

``` cpp
sort(a.begin(), a.end());                       // ascending
sort(a.begin(), a.end(), greater<int>());       // descending
sort(v.begin(), v.end(), [](auto &x, auto &y){  // custom
    return x.second > y.second; });
reverse(a.begin(), a.end());
a.erase(unique(a.begin(), a.end()), a.end());   // after sort: dedupe
int i = lower_bound(a.begin(), a.end(), x) - a.begin(); // first >= x
int j = upper_bound(a.begin(), a.end(), x) - a.begin(); // first >  x
priority_queue<int, vector<int>, greater<int>> minh;    // min-heap
for (auto &[k, v] : m) { }                      // iterate a map
if (m.count(k)) { }       // check without inserting (m[k] inserts!)
__builtin_popcount(x);    // set bits (use ...ll for long long)
string t = to_string(42); int v = stoi("42");
```

Idioms

- `top()` or `pop()` on an empty container is undefined: check `empty()` first
- `v.size()` is unsigned: `v.size() - 1` underflows when empty
- Pass big things by reference: `const vector<int> &v`
- After `cin >> n`, call `cin.ignore()` before `getline`

The trigger tells you the technique

## Pattern triggers

| If the problem says…                                       | Think                        | Why                                          |
|------------------------------------------------------------|------------------------------|----------------------------------------------|
| Sorted array, find a target or a boundary                  | Binary search                | Halve the search space each step             |
| "Minimum of the maximum", "smallest value such that…"      | Binary search on the answer  | The answer is monotonic: check(x) flips once |
| Pair or triplet with a sum, in a sorted array              | Two pointers                 | Move the end that helps                      |
| Longest or shortest subarray or substring with a condition | Sliding window               | Grow right, shrink left while invalid        |
| Subarray sum equals K, count of subarrays                  | Prefix sum + hash map        | sum(l..r) = pre\[r\] − pre\[l−1\]            |
| Next greater or smaller element, histogram areas           | Monotonic stack              | Each element is pushed and popped once       |
| Top K, Kth largest, merge K sorted                         | Heap                         | Keep only K items                            |
| Seen before? count? group by?                              | Hash map or set              | O(1) lookups                                 |
| All subsets, permutations, combinations                    | Backtracking                 | Choose, explore, un-choose                   |
| Shortest path, unweighted                                  | BFS                          | Level by level                               |
| Shortest path, weights ≥ 0                                 | Dijkstra                     | Greedy on the closest node                   |
| Negative edges; all pairs                                  | Bellman-Ford; Floyd-Warshall | Relax edges repeatedly                       |
| Connected groups, "same component", merging                | DFS or Union-Find (DSU)      | Near O(1) per union                          |
| Order with prerequisites                                   | Topological sort             | Kahn's algorithm with in-degrees             |
| Count ways, min or max cost, "can you reach"               | Dynamic programming          | Overlapping subproblems                      |
| Choices now affect later, local best works                 | Greedy (sort first)          | Prove it with an exchange argument           |
| Prefix lookups, autocomplete, max XOR                      | Trie                         | One node per character or bit                |
| Appears once, toggle, subsets up to 20                     | Bit manipulation             | XOR cancels pairs; masks enumerate subsets   |
| Linked list: middle, cycle                                 | Slow and fast pointers       | Fast moves two, slow moves one               |
| Tree: any "path" or "height" question                      | DFS returning a value up     | Combine the left and right answers           |
| Intervals: merge, overlap, rooms                           | Sort by start or end         | Then sweep once                              |

Type these until they are automatic

## Templates

``` text
int lo = 0, hi = n - 1, ans = -1;
while (lo <= hi) {
    int mid = lo + (hi - lo) / 2;
    if (a[mid] >= x) { ans = mid; hi = mid - 1; }   // first index >= x
    else lo = mid + 1;
}
```

Binary search

``` text
ll lo = MIN_ANS, hi = MAX_ANS, ans = hi;
while (lo <= hi) {
    ll mid = lo + (hi - lo) / 2;
    if (ok(mid)) { ans = mid; hi = mid - 1; }   // smallest value that works
    else lo = mid + 1;
}
```

Binary search on the answer

``` text
int i = 0, j = n - 1;
while (i < j) {
    int s = a[i] + a[j];
    if (s == target) { /* found */ i++; j--; }
    else if (s < target) i++;
    else j--;
}
```

Two pointers (sorted array)

``` text
int best = 0;
for (int l = 0, r = 0; r < n; r++) {
    add(a[r]);
    while (!valid()) remove(a[l++]);
    best = max(best, r - l + 1);
}
```

Sliding window (longest valid)

``` cpp
vector<ll> pre(n + 1, 0);
for (int i = 0; i < n; i++) pre[i + 1] = pre[i] + a[i];
// sum of a[l..r] = pre[r + 1] - pre[l]

unordered_map<ll, int> seen; seen[0] = 1;
ll sum = 0, ways = 0;
for (int x : a) { sum += x; ways += seen[sum - k]; seen[sum]++; }
```

Prefix sum; subarrays with sum K

``` cpp
vector<int> nge(n, -1); stack<int> st;       // st holds indices
for (int i = 0; i < n; i++) {
    while (!st.empty() && a[st.top()] < a[i]) { nge[st.top()] = a[i]; st.pop(); }
    st.push(i);
}
```

Monotonic stack (next greater)

``` cpp
void go(int i, vector<int> &cur) {
    if (i == n) { out.push_back(cur); return; }
    cur.push_back(a[i]); go(i + 1, cur);     // choose
    cur.pop_back();      go(i + 1, cur);     // un-choose
}
```

Backtracking (subsets)

``` cpp
vector<int> dist(n, -1); queue<int> q;
dist[s] = 0; q.push(s);
while (!q.empty()) {
    int u = q.front(); q.pop();
    for (int v : adj[u]) if (dist[v] == -1) { dist[v] = dist[u] + 1; q.push(v); }
}
```

BFS (shortest path, unweighted)

``` text
void dfs(int u) {
    vis[u] = true;
    for (int v : adj[u]) if (!vis[v]) dfs(v);
}
int dr[] = {-1, 1, 0, 0}, dc[] = {0, 0, -1, 1};
// nr = r + dr[k], nc = c + dc[k]; check 0 <= nr < R and 0 <= nc < C
```

DFS; grid neighbours

``` cpp
vector<int> indeg(n), order; queue<int> q;
for (int u = 0; u < n; u++) for (int v : adj[u]) indeg[v]++;
for (int u = 0; u < n; u++) if (!indeg[u]) q.push(u);
while (!q.empty()) {
    int u = q.front(); q.pop(); order.push_back(u);
    for (int v : adj[u]) if (--indeg[v] == 0) q.push(v);
}
// order.size() < n  means there is a cycle
```

Topological sort (Kahn)

``` cpp
vector<ll> d(n, LLONG_MAX);
priority_queue<pair<ll,int>, vector<pair<ll,int>>, greater<>> pq;
d[s] = 0; pq.push({0, s});
while (!pq.empty()) {
    auto [du, u] = pq.top(); pq.pop();
    if (du > d[u]) continue;
    for (auto [v, w] : adj[u])
        if (du + w < d[v]) { d[v] = du + w; pq.push({d[v], v}); }
}
```

Dijkstra

``` cpp
vector<int> p(n), sz(n, 1);
iota(p.begin(), p.end(), 0);
int find(int x) { return p[x] == x ? x : p[x] = find(p[x]); }
bool unite(int a, int b) {
    a = find(a); b = find(b);
    if (a == b) return false;
    if (sz[a] < sz[b]) swap(a, b);
    p[b] = a; sz[a] += sz[b]; return true;
}
```

Union-Find (DSU)

``` cpp
// knapsack: best value with capacity W
vector<int> dp(W + 1, 0);
for (int i = 0; i < n; i++)
    for (int c = W; c >= wt[i]; c--) dp[c] = max(dp[c], dp[c - wt[i]] + val[i]);

// LIS in O(n log n)
vector<int> t;
for (int x : a) { auto it = lower_bound(t.begin(), t.end(), x);
                  if (it == t.end()) t.push_back(x); else *it = x; }

// LCS of s and r
vector<vector<int>> L(n + 1, vector<int>(m + 1, 0));
for (int i = 1; i <= n; i++) for (int j = 1; j <= m; j++)
    L[i][j] = s[i-1] == r[j-1] ? L[i-1][j-1] + 1 : max(L[i-1][j], L[i][j-1]);
```

DP: 0/1 knapsack, LIS, LCS

``` text
Node *prev = nullptr, *cur = head;
while (cur) { Node *nx = cur->next; cur->next = prev; prev = cur; cur = nx; }
head = prev;

Node *slow = head, *fast = head;             // middle, or cycle check
while (fast && fast->next) { slow = slow->next; fast = fast->next->next;
                             if (slow == fast) { /* cycle */ break; } }
```

Linked list: reverse; slow and fast

``` text
int height(Node *r) { return r ? 1 + max(height(r->left), height(r->right)) : 0; }

queue<Node*> q; if (root) q.push(root);
while (!q.empty()) {
    int k = q.size();                         // one level
    while (k--) { Node *u = q.front(); q.pop();
                  if (u->left) q.push(u->left); if (u->right) q.push(u->right); }
}
```

Tree: height, level order

``` cpp
x & 1            // odd?            x & (x - 1)     // drop the lowest set bit
x & -x           // lowest set bit  x >> i & 1      // i-th bit
x | (1 << i)     // set bit i       x & ~(1 << i)   // clear bit i
for (int mask = 0; mask < (1 << n); mask++) { }     // all subsets

ll power(ll a, ll b, ll M) { ll r = 1; a %= M;
    while (b) { if (b & 1) r = r * a % M; a = a * a % M; b >>= 1; } return r; }
// gcd(a, b) = __gcd(a, b);  lcm = a / gcd * b
vector<bool> prime(n + 1, true); prime[0] = prime[1] = false;   // sieve
for (int i = 2; (ll)i * i <= n; i++) if (prime[i])
    for (int j = i * i; j <= n; j += i) prime[j] = false;
```

Bits and maths

Dynamic programming in five questions

## DP recipe

1.  **State:** what changes between subproblems? (index, capacity, last choice)
2.  **Meaning:** say dp\[i\] in one sentence
3.  **Transition:** the choices at this state
4.  **Base case:** the smallest inputs
5.  **Order and answer:** which way to fill, and where the answer sits

| Family      | State                     | Examples                          |
|-------------|---------------------------|-----------------------------------|
| 1D          | dp\[i\]                   | Climbing stairs, house robber     |
| Grid        | dp\[r\]\[c\]              | Unique paths, minimum path sum    |
| Subsequence | dp\[i\]\[sum\]            | Subset sum, knapsack, coin change |
| Two strings | dp\[i\]\[j\]              | LCS, edit distance                |
| LIS         | dp\[i\] ending at i       | LIS, longest chain                |
| Stocks      | dp\[day\]\[holding\]\[k\] | Buy and sell variants             |
| Intervals   | dp\[l\]\[r\]              | Matrix chain, burst balloons      |

One-line answers, then go deeper

## Core CS

### OOP

- **Encapsulation:** data and methods together, internals hidden
- **Abstraction:** show what it does, hide how
- **Inheritance:** a class reuses and extends another
- **Polymorphism:** one interface, many forms. Compile-time: overloading. Run-time: virtual functions through the vtable.
- A **virtual destructor** is needed when deleting through a base pointer
- **Shallow copy** copies pointers; **deep copy** copies what they point to
- **SOLID:** single responsibility, open/closed, Liskov, interface segregation, dependency inversion

### Operating systems

- **Process** has its own memory; **threads** share it
- **Context switch:** save one state, load another
- **Scheduling:** FCFS, SJF, round robin, priority
- **Deadlock** needs all four: mutual exclusion, hold and wait, no preemption, circular wait
- **Mutex** has one owner; a **semaphore** is a counter
- **Paging** maps virtual pages to frames; a page fault loads from disk; thrashing is constant faulting
- **Virtual memory** lets processes use more than physical RAM

### DBMS

- **ACID:** atomicity, consistency, isolation, durability
- **Normal forms:** 1NF atomic values; 2NF no partial dependency; 3NF no transitive dependency; BCNF every determinant is a key
- **Keys:** primary, candidate, foreign, composite
- **Index:** a B+ tree that speeds reads and slows writes
- **Isolation levels:** read uncommitted, read committed, repeatable read, serializable
- **Joins:** inner, left, right, full, cross, self

### Networks

- **OSI:** physical, data link, network, transport, session, presentation, application
- **TCP:** reliable, ordered, 3-way handshake (SYN, SYN-ACK, ACK). **UDP:** no guarantees, faster
- **Typing a URL:** DNS lookup, TCP handshake, TLS handshake, HTTP request, response, render
- **HTTP codes:** 2xx ok, 3xx redirect, 4xx your fault, 5xx server fault
- **Subnetting:** /24 has 256 addresses, 254 hosts
- **NAT** maps private to public addresses; **DHCP** hands out addresses; **ARP** maps IP to MAC

Write the clauses in this order

## SQL

``` sql
SELECT dept, COUNT(*) AS n, AVG(salary) AS avg_sal
FROM employees e
JOIN departments d ON d.id = e.dept_id
WHERE e.active = 1            -- filters rows
GROUP BY dept
HAVING COUNT(*) > 5           -- filters groups
ORDER BY avg_sal DESC
LIMIT 10;
-- runs as: FROM, JOIN, WHERE, GROUP BY, HAVING, SELECT, ORDER BY, LIMIT
```

Shape of a query

``` sql
-- second highest salary
SELECT MAX(salary) FROM employees
WHERE salary < (SELECT MAX(salary) FROM employees);

-- top earner in each department
SELECT * FROM (
  SELECT e.*, DENSE_RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS r
  FROM employees e) t
WHERE r = 1;

-- duplicates
SELECT email, COUNT(*) FROM users GROUP BY email HAVING COUNT(*) > 1;

-- running total
SELECT day, SUM(amount) OVER (ORDER BY day) AS running FROM sales;

-- a CTE
WITH big AS (SELECT * FROM orders WHERE total > 1000)
SELECT customer_id, COUNT(*) FROM big GROUP BY customer_id;
```

The interview favourites

Labs only: platforms built for it and machines you own

## Security

``` bash
ls -la; pwd; cd; cat; less; head; tail -f
grep -rn "text" .        find / -name "*.conf" 2>/dev/null
chmod 640 file           chown user:group file
ps aux; top; kill -9 PID
ss -tulpn                # listening ports
sudo -l                  # what may I run as root?
find / -perm -4000 2>/dev/null   # SUID files
curl -I https://site     # response headers
```

Linux

``` bash
nmap -sV -sC -p- target        # versions, default scripts, all ports
nmap -sn 192.168.1.0/24        # which hosts are up
tcpdump -i eth0 port 80
# Wireshark filters
http; dns; tcp.port == 443; ip.addr == 10.0.0.5
tcp.flags.syn == 1 && tcp.flags.ack == 0
```

Recon and capture

| Port      | Service      |
|-----------|--------------|
| 20, 21    | FTP          |
| 22        | SSH          |
| 23        | Telnet       |
| 25        | SMTP         |
| 53        | DNS          |
| 80 / 443  | HTTP / HTTPS |
| 110 / 143 | POP3 / IMAP  |
| 3306      | MySQL        |
| 3389      | RDP          |
| 5432      | PostgreSQL   |

### OWASP Top 10 (2021)

1.  Broken access control (IDOR)
2.  Cryptographic failures
3.  Injection (SQL, command, XSS)
4.  Insecure design
5.  Security misconfiguration
6.  Vulnerable and outdated components
7.  Identification and authentication failures
8.  Software and data integrity failures
9.  Logging and monitoring failures
10. Server-side request forgery (SSRF)

- **Fix injection** with parameterised queries, never string building
- **Fix XSS** with output encoding and a content security policy
- **Hash passwords** with bcrypt or Argon2 and a salt; hashing is one-way, encryption is not
- **STRIDE:** spoofing, tampering, repudiation, information disclosure, denial of service, elevation of privilege

For the SAA exam and for TenantWall

## AWS

| Service            | What it is                                            |
|--------------------|-------------------------------------------------------|
| IAM                | Users, groups, roles, policies. Who can do what.      |
| EC2 / EBS          | Virtual servers / their disks                         |
| S3                 | Object storage in buckets                             |
| VPC                | Your private network: subnets, route tables, gateways |
| RDS / DynamoDB     | Managed SQL / NoSQL key-value                         |
| ELB + Auto Scaling | Spread load / add and remove servers                  |
| Route 53           | DNS                                                   |
| CloudFront         | CDN at edge locations                                 |
| Lambda             | Run code without servers                              |
| SQS / SNS          | Queue / publish and subscribe                         |
| CloudTrail         | Who called which API, when                            |
| CloudWatch         | Metrics, logs, alarms                                 |
| KMS                | Encryption keys                                       |
| CloudFormation     | Infrastructure as code                                |

### IAM, the part TenantWall lives on

- **Evaluation order:** an explicit Deny wins; otherwise an Allow is needed; otherwise implicit deny
- **Identity policy** attaches to a user, group or role; **resource policy** attaches to the thing (a bucket)
- **ABAC:** compare `aws:PrincipalTag/Team` with `aws:ResourceTag/Team`
- **Least privilege:** grant only what is needed
- **Role:** temporary credentials, no long-lived keys

### Remember for the exam

- **Security group:** stateful, allow rules only, on the instance. **NACL:** stateless, allow and deny, on the subnet.
- **Public subnet** routes to an internet gateway; **private** reaches out through a NAT gateway
- **Multi-AZ** is for availability; **read replicas** are for read scaling
- **S3 classes:** Standard, Infrequent Access, Glacier, by how often you read
- **Shared responsibility:** AWS secures the cloud; you secure what you put in it

The night before and in the room

## Interviews

### In a coding round

1.  Repeat the problem; ask for constraints and an example
2.  Say the brute force and its complexity
3.  Improve it out loud; get a nod before coding
4.  Code cleanly, naming things by meaning
5.  Walk one example through the code
6.  State time and space; mention edge cases

### Project walk-through, 3 minutes

1.  The problem, in one sentence
2.  What you built and your part in it
3.  One hard decision and why you made it
4.  How you tested it, with a number
5.  What you would change next

TenantWall: 2 identity policies for any number of teams; 14 of 14 tests; refusals logged and alerted.

### Five stories to have ready

- A hard bug you fixed
- A disagreement in a team
- A deadline you nearly missed
- A failure and what changed after
- Something you taught yourself

Tell each as situation, task, action, result. End every interview with one real question.

Templates are C++17. Type them yourself until they are automatic; do not paste them.13 Nov 2026
