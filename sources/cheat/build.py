import html
E=html.escape
def code(title,src): return f'<figure class="code"><figcaption>{E(title)}</figcaption><pre>{E(src.strip(chr(10)))}</pre></figure>'
def table(head,rows,cls=""): return '<div class="tw"><table class="'+cls+'"><thead><tr>'+"".join(f"<th>{E(x)}</th>" for x in head)+'</tr></thead><tbody>'+"".join("<tr>"+"".join(f"<td>{c}</td>" for c in r)+"</tr>" for r in rows)+'</tbody></table></div>'
c=lambda s:f"<code>{E(s)}</code>"
S=[]
def sec(id,label,title,body): S.append(f'<section class="sec" id="{id}"><header><p class="label">{E(label)}</p><h2>{E(title)}</h2></header>{body}</section>')

sec("rules","Read before every session","The rules",
 '<div class="cols">'
 '<div><h3>The problem loop</h3><ol class="num"><li><b>Restate</b> the input, output and constraints. One example by hand. (3 min)</li><li><b>Brute force</b> and its Big-O. (5 min)</li><li><b>Optimise:</b> sort? hash? two pointers? binary search the answer? repeated work? a graph? (10 to 20 min)</li><li><b>Code</b> it in one go. (10 to 15 min)</li><li><b>Test</b> the sample and two edge cases. (5 min)</li><li><b>Log</b> the pattern, the time, S/H/F and the mistake. (1 min)</li></ol></div>'
 '<div><h3>When stuck</h3><ul class="plain"><li>30 minutes alone, then a hint only</li><li>60 minutes, then the solution: close it and code from memory</li><li>Re-solve at 1, 3, 7 and 21 days</li><li>Mark it S (solved), H (hint) or F (failed)</li></ul><h3>Never zero</h3><ul class="plain"><li>Minimum day: revision, 2 Striver, 1 LeetCode, 20 min of flashcards</li><li>Short on time, cut: the Elite HFT track (if open), the CP habit, the AI-security project, then cyber. Never DSA or revision.</li></ul></div>'
 '<div><h3>Edge cases to try</h3><ul class="plain"><li>Empty input, one element, two elements</li><li>All equal, already sorted, reverse sorted</li><li>Negative numbers and zero</li><li>The largest n and the largest values (overflow)</li><li>Duplicates; the target missing</li><li>Trees: empty, one node, a straight line</li><li>Graphs: disconnected, a self-loop, a cycle</li></ul></div></div>')

sec("complexity","Constraints name the algorithm","Complexity",
 '<div class="cols two">'+
 table(["n up to","Aim for","Typical technique"],[["10 to 12","O(n!)","Permutations, backtracking"],["20 to 25","O(2ⁿ)","Bitmask, subsets, meet in the middle"],["100","O(n³) or O(n⁴)","Floyd-Warshall, interval DP"],["1,000 to 5,000","O(n²)","2D DP, nested loops"],["10⁵","O(n log n)","Sorting, heap, binary search, segment tree"],["10⁶ to 10⁷","O(n)","Two pointers, hashing, prefix sums, sieve"],["10⁹ to 10¹⁸","O(log n) or O(√n)","Binary search, maths, fast power"]],"num")+
 '<div><ul class="plain"><li>About <b>10⁸ simple operations per second</b></li><li>'+c("int")+' holds about ±2.1×10⁹. Anything bigger: '+c("long long")+' (about ±9.2×10¹⁸)</li><li>Overflow happens in the expression: write '+c("1LL * a * b")+'</li><li>Mid without overflow: '+c("lo + (hi - lo) / 2")+'</li><li>Modulo: '+c("((a % M) + M) % M")+' for negatives; '+c("M = 1e9 + 7")+'</li><li>Recursion deeper than about 10⁵ risks a stack overflow</li><li>'+c("sort")+' is O(n log n); '+c("map")+' and '+c("set")+' are O(log n) per operation; '+c("unordered_map")+' is O(1) on average</li><li>A loop that halves or doubles runs log n times; '+c("i*i <= n")+' runs √n times</li></ul></div></div>')

sec("cpp","What you need from C++","C++ and the STL",
 code("Starter",'''
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;

int main() {
    ios::sync_with_stdio(false); cin.tin(nullptr);
    int n; cin >> n;
    vector<int> a(n);
    for (int &x : a) cin >> x;
    cout << accumulate(a.begin(), a.end(), 0LL) << "\\n";
}
'''.replace("cin.tin","cin.tie"))+
 '<div class="cols two">'+
 table(["Container","Use it for","Key calls"],[
  [c("vector<T>"),"Dynamic array",c("push_back pop_back back size [i]")],
  [c("string"),"Text",c("size substr(i,len) find += ")],
  [c("pair<A,B>"),"Two values",c(".first .second")],
  [c("stack<T>"),"Last in, first out",c("push pop top empty")],
  [c("queue<T>"),"First in, first out (BFS)",c("push pop front empty")],
  [c("deque<T>"),"Both ends",c("push_front push_back pop_front pop_back")],
  [c("priority_queue<T>"),"Max-heap",c("push pop top")],
  [c("set<T>"),"Sorted unique",c("insert erase count lower_bound")],
  [c("map<K,V>"),"Sorted key to value",c("m[k] count find erase")],
  [c("unordered_map<K,V>"),"Hash map, O(1) average",c("m[k] count find")],
 ])+
 '<div>'+code("Idioms",'''
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
''')+'<ul class="plain"><li>'+c("top()")+' or '+c("pop()")+' on an empty container is undefined: check '+c("empty()")+' first</li><li>'+c("v.size()")+' is unsigned: '+c("v.size() - 1")+' underflows when empty</li><li>Pass big things by reference: '+c("const vector<int> &v")+'</li><li>After '+c("cin >> n")+', call '+c("cin.ignore()")+' before '+c("getline")+'</li></ul></div></div>')

sec("patterns","The trigger tells you the technique","Pattern triggers",
 table(["If the problem says…","Think","Why"],[
  ["Sorted array, find a target or a boundary","Binary search","Halve the search space each step"],
  ["\"Minimum of the maximum\", \"smallest value such that…\"","Binary search on the answer","The answer is monotonic: check(x) flips once"],
  ["Pair or triplet with a sum, in a sorted array","Two pointers","Move the end that helps"],
  ["Longest or shortest subarray or substring with a condition","Sliding window","Grow right, shrink left while invalid"],
  ["Subarray sum equals K, count of subarrays","Prefix sum + hash map","sum(l..r) = pre[r] − pre[l−1]"],
  ["Next greater or smaller element, histogram areas","Monotonic stack","Each element is pushed and popped once"],
  ["Top K, Kth largest, merge K sorted","Heap","Keep only K items"],
  ["Seen before? count? group by?","Hash map or set","O(1) lookups"],
  ["All subsets, permutations, combinations","Backtracking","Choose, explore, un-choose"],
  ["Shortest path, unweighted","BFS","Level by level"],
  ["Shortest path, weights ≥ 0","Dijkstra","Greedy on the closest node"],
  ["Negative edges; all pairs","Bellman-Ford; Floyd-Warshall","Relax edges repeatedly"],
  ["Connected groups, \"same component\", merging","DFS or Union-Find (DSU)","Near O(1) per union"],
  ["Order with prerequisites","Topological sort","Kahn's algorithm with in-degrees"],
  ["Count ways, min or max cost, \"can you reach\"","Dynamic programming","Overlapping subproblems"],
  ["Choices now affect later, local best works","Greedy (sort first)","Prove it with an exchange argument"],
  ["Prefix lookups, autocomplete, max XOR","Trie","One node per character or bit"],
  ["Appears once, toggle, subsets up to 20","Bit manipulation","XOR cancels pairs; masks enumerate subsets"],
  ["Linked list: middle, cycle","Slow and fast pointers","Fast moves two, slow moves one"],
  ["Tree: any \"path\" or \"height\" question","DFS returning a value up","Combine the left and right answers"],
  ["Intervals: merge, overlap, rooms","Sort by start or end","Then sweep once"],
 ]))

T=[("Binary search",'''
int lo = 0, hi = n - 1, ans = -1;
while (lo <= hi) {
    int mid = lo + (hi - lo) / 2;
    if (a[mid] >= x) { ans = mid; hi = mid - 1; }   // first index >= x
    else lo = mid + 1;
}
'''),("Binary search on the answer",'''
ll lo = MIN_ANS, hi = MAX_ANS, ans = hi;
while (lo <= hi) {
    ll mid = lo + (hi - lo) / 2;
    if (ok(mid)) { ans = mid; hi = mid - 1; }   // smallest value that works
    else lo = mid + 1;
}
'''),("Two pointers (sorted array)",'''
int i = 0, j = n - 1;
while (i < j) {
    int s = a[i] + a[j];
    if (s == target) { /* found */ i++; j--; }
    else if (s < target) i++;
    else j--;
}
'''),("Sliding window (longest valid)",'''
int best = 0;
for (int l = 0, r = 0; r < n; r++) {
    add(a[r]);
    while (!valid()) remove(a[l++]);
    best = max(best, r - l + 1);
}
'''),("Prefix sum; subarrays with sum K",'''
vector<ll> pre(n + 1, 0);
for (int i = 0; i < n; i++) pre[i + 1] = pre[i] + a[i];
// sum of a[l..r] = pre[r + 1] - pre[l]

unordered_map<ll, int> seen; seen[0] = 1;
ll sum = 0, ways = 0;
for (int x : a) { sum += x; ways += seen[sum - k]; seen[sum]++; }
'''),("Monotonic stack (next greater)",'''
vector<int> nge(n, -1); stack<int> st;       // st holds indices
for (int i = 0; i < n; i++) {
    while (!st.empty() && a[st.top()] < a[i]) { nge[st.top()] = a[i]; st.pop(); }
    st.push(i);
}
'''),("Backtracking (subsets)",'''
void go(int i, vector<int> &cur) {
    if (i == n) { out.push_back(cur); return; }
    cur.push_back(a[i]); go(i + 1, cur);     // choose
    cur.pop_back();      go(i + 1, cur);     // un-choose
}
'''),("BFS (shortest path, unweighted)",'''
vector<int> dist(n, -1); queue<int> q;
dist[s] = 0; q.push(s);
while (!q.empty()) {
    int u = q.front(); q.pop();
    for (int v : adj[u]) if (dist[v] == -1) { dist[v] = dist[u] + 1; q.push(v); }
}
'''),("DFS; grid neighbours",'''
void dfs(int u) {
    vis[u] = true;
    for (int v : adj[u]) if (!vis[v]) dfs(v);
}
int dr[] = {-1, 1, 0, 0}, dc[] = {0, 0, -1, 1};
// nr = r + dr[k], nc = c + dc[k]; check 0 <= nr < R and 0 <= nc < C
'''),("Topological sort (Kahn)",'''
vector<int> indeg(n), order; queue<int> q;
for (int u = 0; u < n; u++) for (int v : adj[u]) indeg[v]++;
for (int u = 0; u < n; u++) if (!indeg[u]) q.push(u);
while (!q.empty()) {
    int u = q.front(); q.pop(); order.push_back(u);
    for (int v : adj[u]) if (--indeg[v] == 0) q.push(v);
}
// order.size() < n  means there is a cycle
'''),("Dijkstra",'''
vector<ll> d(n, LLONG_MAX);
priority_queue<pair<ll,int>, vector<pair<ll,int>>, greater<>> pq;
d[s] = 0; pq.push({0, s});
while (!pq.empty()) {
    auto [du, u] = pq.top(); pq.pop();
    if (du > d[u]) continue;
    for (auto [v, w] : adj[u])
        if (du + w < d[v]) { d[v] = du + w; pq.push({d[v], v}); }
}
'''),("Union-Find (DSU)",'''
vector<int> p(n), sz(n, 1);
iota(p.begin(), p.end(), 0);
int find(int x) { return p[x] == x ? x : p[x] = find(p[x]); }
bool unite(int a, int b) {
    a = find(a); b = find(b);
    if (a == b) return false;
    if (sz[a] < sz[b]) swap(a, b);
    p[b] = a; sz[a] += sz[b]; return true;
}
'''),("DP: 0/1 knapsack, LIS, LCS",'''
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
'''),("Linked list: reverse; slow and fast",'''
Node *prev = nullptr, *cur = head;
while (cur) { Node *nx = cur->next; cur->next = prev; prev = cur; cur = nx; }
head = prev;

Node *slow = head, *fast = head;             // middle, or cycle check
while (fast && fast->next) { slow = slow->next; fast = fast->next->next;
                             if (slow == fast) { /* cycle */ break; } }
'''),("Tree: height, level order",'''
int height(Node *r) { return r ? 1 + max(height(r->left), height(r->right)) : 0; }

queue<Node*> q; if (root) q.push(root);
while (!q.empty()) {
    int k = q.size();                         // one level
    while (k--) { Node *u = q.front(); q.pop();
                  if (u->left) q.push(u->left); if (u->right) q.push(u->right); }
}
'''),("Bits and maths",'''
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
''')]
sec("templates","Type these until they are automatic","Templates",'<div class="codes">'+"".join(code(t,s) for t,s in T)+'</div>')

sec("dp","Dynamic programming in five questions","DP recipe",
 '<div class="cols two"><ol class="num"><li><b>State:</b> what changes between subproblems? (index, capacity, last choice)</li><li><b>Meaning:</b> say dp[i] in one sentence</li><li><b>Transition:</b> the choices at this state</li><li><b>Base case:</b> the smallest inputs</li><li><b>Order and answer:</b> which way to fill, and where the answer sits</li></ol>'+
 table(["Family","State","Examples"],[["1D","dp[i]","Climbing stairs, house robber"],["Grid","dp[r][c]","Unique paths, minimum path sum"],["Subsequence","dp[i][sum]","Subset sum, knapsack, coin change"],["Two strings","dp[i][j]","LCS, edit distance"],["LIS","dp[i] ending at i","LIS, longest chain"],["Stocks","dp[day][holding][k]","Buy and sell variants"],["Intervals","dp[l][r]","Matrix chain, burst balloons"]])+'</div>')

sec("cs","One-line answers, then go deeper","Core CS",
 '<div class="cols two"><div><h3>OOP</h3><ul class="plain"><li><b>Encapsulation:</b> data and methods together, internals hidden</li><li><b>Abstraction:</b> show what it does, hide how</li><li><b>Inheritance:</b> a class reuses and extends another</li><li><b>Polymorphism:</b> one interface, many forms. Compile-time: overloading. Run-time: virtual functions through the vtable.</li><li>A <b>virtual destructor</b> is needed when deleting through a base pointer</li><li><b>Shallow copy</b> copies pointers; <b>deep copy</b> copies what they point to</li><li><b>SOLID:</b> single responsibility, open/closed, Liskov, interface segregation, dependency inversion</li></ul>'
 '<h3>Operating systems</h3><ul class="plain"><li><b>Process</b> has its own memory; <b>threads</b> share it</li><li><b>Context switch:</b> save one state, load another</li><li><b>Scheduling:</b> FCFS, SJF, round robin, priority</li><li><b>Deadlock</b> needs all four: mutual exclusion, hold and wait, no preemption, circular wait</li><li><b>Mutex</b> has one owner; a <b>semaphore</b> is a counter</li><li><b>Paging</b> maps virtual pages to frames; a page fault loads from disk; thrashing is constant faulting</li><li><b>Virtual memory</b> lets processes use more than physical RAM</li></ul></div>'
 '<div><h3>DBMS</h3><ul class="plain"><li><b>ACID:</b> atomicity, consistency, isolation, durability</li><li><b>Normal forms:</b> 1NF atomic values; 2NF no partial dependency; 3NF no transitive dependency; BCNF every determinant is a key</li><li><b>Keys:</b> primary, candidate, foreign, composite</li><li><b>Index:</b> a B+ tree that speeds reads and slows writes</li><li><b>Isolation levels:</b> read uncommitted, read committed, repeatable read, serializable</li><li><b>Joins:</b> inner, left, right, full, cross, self</li></ul>'
 '<h3>Networks</h3><ul class="plain"><li><b>OSI:</b> physical, data link, network, transport, session, presentation, application</li><li><b>TCP:</b> reliable, ordered, 3-way handshake (SYN, SYN-ACK, ACK). <b>UDP:</b> no guarantees, faster</li><li><b>Typing a URL:</b> DNS lookup, TCP handshake, TLS handshake, HTTP request, response, render</li><li><b>HTTP codes:</b> 2xx ok, 3xx redirect, 4xx your fault, 5xx server fault</li><li><b>Subnetting:</b> /24 has 256 addresses, 254 hosts</li><li><b>NAT</b> maps private to public addresses; <b>DHCP</b> hands out addresses; <b>ARP</b> maps IP to MAC</li></ul></div></div>')

sec("sql","Write the clauses in this order","SQL",
 '<div class="cols two">'+code("Shape of a query",'''
SELECT dept, COUNT(*) AS n, AVG(salary) AS avg_sal
FROM employees e
JOIN departments d ON d.id = e.dept_id
WHERE e.active = 1            -- filters rows
GROUP BY dept
HAVING COUNT(*) > 5           -- filters groups
ORDER BY avg_sal DESC
LIMIT 10;
-- runs as: FROM, JOIN, WHERE, GROUP BY, HAVING, SELECT, ORDER BY, LIMIT
''')+code("The interview favourites",'''
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
''')+'</div>')

sec("security","Labs only: platforms built for it and machines you own","Security",
 '<div class="cols two"><div>'+code("Linux",'''
ls -la; pwd; cd; cat; less; head; tail -f
grep -rn "text" .        find / -name "*.conf" 2>/dev/null
chmod 640 file           chown user:group file
ps aux; top; kill -9 PID
ss -tulpn                # listening ports
sudo -l                  # what may I run as root?
find / -perm -4000 2>/dev/null   # SUID files
curl -I https://site     # response headers
''')+code("Recon and capture",'''
nmap -sV -sC -p- target        # versions, default scripts, all ports
nmap -sn 192.168.1.0/24        # which hosts are up
tcpdump -i eth0 port 80
# Wireshark filters
http; dns; tcp.port == 443; ip.addr == 10.0.0.5
tcp.flags.syn == 1 && tcp.flags.ack == 0
''')+'</div><div>'+
 table(["Port","Service"],[["20, 21","FTP"],["22","SSH"],["23","Telnet"],["25","SMTP"],["53","DNS"],["80 / 443","HTTP / HTTPS"],["110 / 143","POP3 / IMAP"],["3306","MySQL"],["3389","RDP"],["5432","PostgreSQL"]],"num")+
 '<h3>OWASP Top 10 (2021)</h3><ol class="num tight"><li>Broken access control (IDOR)</li><li>Cryptographic failures</li><li>Injection (SQL, command, XSS)</li><li>Insecure design</li><li>Security misconfiguration</li><li>Vulnerable and outdated components</li><li>Identification and authentication failures</li><li>Software and data integrity failures</li><li>Logging and monitoring failures</li><li>Server-side request forgery (SSRF)</li></ol>'
 '<ul class="plain"><li><b>Fix injection</b> with parameterised queries, never string building</li><li><b>Fix XSS</b> with output encoding and a content security policy</li><li><b>Hash passwords</b> with bcrypt or Argon2 and a salt; hashing is one-way, encryption is not</li><li><b>STRIDE:</b> spoofing, tampering, repudiation, information disclosure, denial of service, elevation of privilege</li></ul></div></div>')

sec("aws","For the SAA exam and for TenantWall","AWS",
 '<div class="cols two">'+table(["Service","What it is"],[["IAM","Users, groups, roles, policies. Who can do what."],["EC2 / EBS","Virtual servers / their disks"],["S3","Object storage in buckets"],["VPC","Your private network: subnets, route tables, gateways"],["RDS / DynamoDB","Managed SQL / NoSQL key-value"],["ELB + Auto Scaling","Spread load / add and remove servers"],["Route 53","DNS"],["CloudFront","CDN at edge locations"],["Lambda","Run code without servers"],["SQS / SNS","Queue / publish and subscribe"],["CloudTrail","Who called which API, when"],["CloudWatch","Metrics, logs, alarms"],["KMS","Encryption keys"],["CloudFormation","Infrastructure as code"]])+
 '<div><h3>IAM, the part TenantWall lives on</h3><ul class="plain"><li><b>Evaluation order:</b> an explicit Deny wins; otherwise an Allow is needed; otherwise implicit deny</li><li><b>Identity policy</b> attaches to a user, group or role; <b>resource policy</b> attaches to the thing (a bucket)</li><li><b>ABAC:</b> compare '+c("aws:PrincipalTag/Team")+' with '+c("aws:ResourceTag/Team")+'</li><li><b>Least privilege:</b> grant only what is needed</li><li><b>Role:</b> temporary credentials, no long-lived keys</li></ul><h3>Remember for the exam</h3><ul class="plain"><li><b>Security group:</b> stateful, allow rules only, on the instance. <b>NACL:</b> stateless, allow and deny, on the subnet.</li><li><b>Public subnet</b> routes to an internet gateway; <b>private</b> reaches out through a NAT gateway</li><li><b>Multi-AZ</b> is for availability; <b>read replicas</b> are for read scaling</li><li><b>S3 classes:</b> Standard, Infrequent Access, Glacier, by how often you read</li><li><b>Shared responsibility:</b> AWS secures the cloud; you secure what you put in it</li></ul></div></div>')

sec("interview","The night before and in the room","Interviews",
 '<div class="cols"><div><h3>In a coding round</h3><ol class="num"><li>Repeat the problem; ask for constraints and an example</li><li>Say the brute force and its complexity</li><li>Improve it out loud; get a nod before coding</li><li>Code cleanly, naming things by meaning</li><li>Walk one example through the code</li><li>State time and space; mention edge cases</li></ol></div>'
 '<div><h3>Project walk-through, 3 minutes</h3><ol class="num"><li>The problem, in one sentence</li><li>What you built and your part in it</li><li>One hard decision and why you made it</li><li>How you tested it, with a number</li><li>What you would change next</li></ol><p class="small muted">TenantWall: 2 identity policies for any number of teams; 14 of 14 tests; refusals logged and alerted.</p></div>'
 '<div><h3>Five stories to have ready</h3><ul class="plain"><li>A hard bug you fixed</li><li>A disagreement in a team</li><li>A deadline you nearly missed</li><li>A failure and what changed after</li><li>Something you taught yourself</li></ul><p class="small muted">Tell each as situation, task, action, result. End every interview with one real question.</p></div></div>')

NAV="".join(f'<a href="#{i}">{t}</a>' for i,t in [("rules","Rules"),("complexity","Complexity"),("cpp","C++"),("patterns","Patterns"),("templates","Templates"),("dp","DP"),("cs","Core CS"),("sql","SQL"),("security","Security"),("aws","AWS"),("interview","Interviews")])
CSS=open('style.css').read()
page=f'''<title>Prep Cheat Sheet</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
{CSS}</style>
<header class="top"><div class="wrap"><a class="name" href="#rules">Cheat sheet</a><nav aria-label="Sections">{NAV}<a href="https://claude.ai/artifact/McuS723LTAb16Q6SpdUsAT" target="_blank" rel="noopener">Knowledge ↗</a></nav></div></header>
<main class="wrap">
<section class="intro"><p class="label">Placement prep · one page</p><h1>Prep cheat sheet</h1><p class="lede">The rules, the triggers and the templates. Read the first section before every session, and the whole page before every test.</p></section>
{"".join(S)}
<footer><span>Templates are C++17. Type them yourself until they are automatic; do not paste them.</span><span class="mono">13 Nov 2026</span></footer>
</main>
'''
open('prep-cheat-sheet.html','w',encoding='utf-8').write(page)
open('preview.html','w',encoding='utf-8').write('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><style>:root{color-scheme:light}body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style></head><body>'+page+'</body></html>')
open('prep-cheat-sheet-offline.html','w',encoding='utf-8').write(open('preview.html',encoding='utf-8').read())
# extract templates for a compile check
src=["#include <bits/stdc++.h>\nusing namespace std;\ntypedef long long ll;\n"]
print(len(page))
