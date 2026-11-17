ONLINE ASSESSMENT · SIMULATION PACKS III

# 8 more timed OAs sets 17–24 · 90 minutes each

Eight more practice online assessments for the placement season itself: three problems, one timer, no help. Each set has a company-style theme (strings, graphs, DP, heaps, hashing, trees, matrices, mixed). 24 new LeetCode problems, none repeated from OA packs I and II or Worked Solutions I to III (171 problems, checked by script). Each set has a question page (open it when the timer starts) and a solution page (open it only after you have scored yourself).

## Index

| \#  | Set                                                                          | Suggested date  | Mix       | Max |     |
|-----|------------------------------------------------------------------------------|-----------------|-----------|-----|-----|
| 17  | [Strings and arrays](#set-17-strings-and-arrays)Service-company style: careful string handling  | Sat 17 Jul 2027 | E · M · H | 600 |     |
| 18  | [Graphs](#set-18-graphs)Product-company style: degrees, reachability, bridges      | Sat 24 Jul 2027 | E · M · H | 600 |     |
| 19  | [Dynamic programming](#set-19-dynamic-programming)DP-heavy rounds: 1D, chains, palindromes      | Sat 31 Jul 2027 | E · M · H | 600 |     |
| 20  | [Heaps and greedy](#set-20-heaps-and-greedy)Priority queues and exchange arguments           | Sat 7 Aug 2027  | E · M · H | 600 |     |
| 21  | [Hashing and prefix sums](#set-21-hashing-and-prefix-sums)Maps, remainders and 'at most k' counting | Sat 14 Aug 2027 | E · M · H | 600 |     |
| 22  | [Trees](#set-22-trees)Recursion on trees, level indices, greedy from the leaves   | Sat 21 Aug 2027 | E · M · H | 600 |     |
| 23  | [Matrices](#set-23-matrices)Grid recursion, staircase search, heap from the border   | Sat 28 Aug 2027 | E · M · H | 600 |     |
| 24  | [Final mixed](#set-24-final-mixed)One of each: two pointers, grid DFS, two multisets    | Sat 4 Sep 2027  | E · M · H | 600 |     |
| ·   | [How to run a set, and the scoring guide](#how-to-run-a-set)                           |                 |           |     |     |

Dates run every Saturday from 17 July to 4 September 2027, as placement OAs start. If a real OA falls on a Saturday, take the set on Sunday instead. Problem statements are on LeetCode; the one-line summaries, sketches and code here are original. Every reference solution was compiled with `g++ -std=c++17 -Wall -Wextra -fsanitize=address,undefined` and passed its tests.

## How to run a set

### Before

- Pick a 90-minute slot with no interruptions. Phone on silent, notes closed, no AI tools, no searching. Use C++ in the LeetCode editor (or a plain editor without autocomplete, closer to HackerRank and similar platforms).
- Read the [OA tactics page](knowledge-base/career.md#online-assessments-oas) once beforehand.

### During

- Start the timer, then open the question page. Spend the first 5 minutes reading all three problems and decide the order: usually easiest first.
- The minutes next to each problem are a budget. When a budget runs out, submit what you have and move on; come back at the end if time is left.
- If you cannot find the optimal idea, write a correct brute force: in real OAs it often passes part of the hidden tests.
- Test on the given examples and one edge case you write yourself before every submit.

### Scoring guide

| Problem | Full marks | Partial marks                                                                                                                                |
|---------|------------|----------------------------------------------------------------------------------------------------------------------------------------------|
| Easy    | 100        | If a submission fails, LeetCode shows how many test cases passed. Score = full marks × passed / total, rounded down. No submission scores 0. |
| Medium  | 200        |                                                                                                                                              |
| Hard    | 300        |                                                                                                                                              |

Maximum points per set: set 17: 600, set 18: 600, set 19: 600, set 20: 600, set 21: 600, set 22: 600, set 23: 600, set 24: 600. Because the maximum differs, score yourself as a percentage of the set's maximum:

|             |                                                                                                                |
|-------------|----------------------------------------------------------------------------------------------------------------|
| 80% or more | Strong. Keep the next set on its date.                                                                         |
| 50–79%      | On track. Redo every problem you did not fully solve within 3 days, without looking.                           |
| Below 50%   | Repeat the set in 2 weeks after revising the patterns on its solution page (each links to the Knowledge Base). |

These bands are a personal benchmark for tracking progress, not a company's cut-off. Real cut-offs vary by company and by batch.

### After

- Write the score, the time each problem took and the number of wrong submissions in your revision tracker. Add every problem you did not fully solve to its Log so it comes back for revision.
- Then read the solution page: compare your idea with the sketch, not just the code.

### Record

| Set |
|-----|
| 1   |
| 2   |
| 3   |
| 4   |
| 5   |
| 6   |
| 7   |
| 8   |

## SET 17. Strings and arrays

90 minutes · maximum 600 points · suggested date Sat 17 Jul 2027. Topics are hidden on purpose: working out the pattern is part of the test.

Problem 1[Longest Common Prefix ↗](https://leetcode.com/problems/longest-common-prefix/)Easy15 min · 100 pts

Return the longest prefix shared by every string in a list.

https://leetcode.com/problems/longest-common-prefix/

Your score: \_\_\_\_\_\_ / 100    Time used: \_\_\_\_\_\_ min    Wrong submissions: \_\_\_\_\_\_

Problem 2[String Compression ↗](https://leetcode.com/problems/string-compression/)Medium30 min · 200 pts

Compress runs of repeated characters in place ("aabbccc" → a2b2c3) and return the new length.

https://leetcode.com/problems/string-compression/

Your score: \_\_\_\_\_\_ / 200    Time used: \_\_\_\_\_\_ min    Wrong submissions: \_\_\_\_\_\_

Problem 3[Text Justification ↗](https://leetcode.com/problems/text-justification/)Hard45 min · 300 pts

Lay words out in lines of exactly W characters, spreading spaces evenly (extra spaces go left); the last line is left-aligned.

https://leetcode.com/problems/text-justification/

Your score: \_\_\_\_\_\_ / 300    Time used: \_\_\_\_\_\_ min    Wrong submissions: \_\_\_\_\_\_

Total: \_\_\_\_\_\_ / 600 = \_\_\_\_\_\_ %    [Solutions for this set →](#set-17-solutions)

## SET 17. Solutions

Focus: Service-company style: careful string handling. Read the sketch first, then rewrite the code yourself from memory.

### 1. [Longest Common Prefix](https://leetcode.com/problems/longest-common-prefix/) Easy [Strings](knowledge-base/dsa.md#time-and-space-complexity)

1.  Start with the first string as the prefix; for each other string, shrink the prefix to the part that matches.

**Complexity:** O(total characters) time, O(1) extra space   **Edge cases:** An empty result; One string only

``` cpp
string longestCommonPrefix(vector<string>& s) {
    string p = s[0];
    for (auto& w : s) { size_t i = 0; while (i < p.size() && i < w.size() && p[i] == w[i]) i++; p.resize(i); }
    return p;
}
```

### 2. [String Compression](https://leetcode.com/problems/string-compression/) Medium [Two pointers](knowledge-base/dsa.md#two-pointers)

1.  Read pointer finds the end of each run; write pointer writes the character, then the run length's digits if it is more than 1.

**Complexity:** O(n) time, O(1) space   **Edge cases:** Run lengths of 10 or more (several digits); Single characters get no count

``` cpp
int compress(vector<char>& c) {
    int w = 0, n = c.size();
    for (int i = 0; i < n; ) {
        int j = i; while (j < n && c[j] == c[i]) j++;
        c[w++] = c[i];
        if (j - i > 1) for (char d : to_string(j - i)) c[w++] = d;
        i = j;
    }
    return w;
}
```

### 3. [Text Justification](https://leetcode.com/problems/text-justification/) Hard [Simulation](knowledge-base/dsa.md#time-and-space-complexity)

1.  Greedily take as many words as fit (word lengths + one space between each).
2.  Last line or a single word: join with single spaces and pad right.
3.  Otherwise spaces = (W − letters) / gaps, and the first (W − letters) % gaps gaps get one more.

**Complexity:** O(total characters) time   **Edge cases:** A line with one word; The last line is never fully justified

``` cpp
vector<string> fullJustify(vector<string>& w, int W) {
    vector<string> r; int n = w.size();
    for (int i = 0; i < n; ) {
        int j = i, len = 0;
        while (j < n && len + (int)w[j].size() + (j - i) <= W) len += w[j++].size();
        string line = w[i]; int gaps = j - i - 1;
        if (j == n || gaps == 0) {
            for (int k = i + 1; k < j; k++) line += " " + w[k];
            line += string(W - line.size(), ' ');
        } else {
            int sp = (W - len) / gaps, extra = (W - len) % gaps;
            for (int k = i + 1; k < j; k++) line += string(sp + (k - i <= extra ? 1 : 0), ' ') + w[k];
        }
        r.push_back(line); i = j;
    }
    return r;
}
```

## SET 18. Graphs

90 minutes · maximum 600 points · suggested date Sat 24 Jul 2027. Topics are hidden on purpose: working out the pattern is part of the test.

Problem 1[Find the Town Judge ↗](https://leetcode.com/problems/find-the-town-judge/)Easy15 min · 100 pts

The judge trusts nobody and is trusted by everyone else; find them or return -1.

https://leetcode.com/problems/find-the-town-judge/

Your score: \_\_\_\_\_\_ / 100    Time used: \_\_\_\_\_\_ min    Wrong submissions: \_\_\_\_\_\_

Problem 2[Keys and Rooms ↗](https://leetcode.com/problems/keys-and-rooms/)Medium25 min · 200 pts

Room 0 is open; each room holds keys to other rooms. Can you enter every room?

https://leetcode.com/problems/keys-and-rooms/

Your score: \_\_\_\_\_\_ / 200    Time used: \_\_\_\_\_\_ min    Wrong submissions: \_\_\_\_\_\_

Problem 3[Critical Connections in a Network ↗](https://leetcode.com/problems/critical-connections-in-a-network/)Hard50 min · 300 pts

Return every connection whose removal disconnects the network (the bridges).

https://leetcode.com/problems/critical-connections-in-a-network/

Your score: \_\_\_\_\_\_ / 300    Time used: \_\_\_\_\_\_ min    Wrong submissions: \_\_\_\_\_\_

Total: \_\_\_\_\_\_ / 600 = \_\_\_\_\_\_ %    [Solutions for this set →](#set-18-solutions)

## SET 18. Solutions

Focus: Product-company style: degrees, reachability, bridges. Read the sketch first, then rewrite the code yourself from memory.

### 1. [Find the Town Judge](https://leetcode.com/problems/find-the-town-judge/) Easy [Graph degrees](knowledge-base/dsa.md#bfs-and-graph-basics)

1.  Score = in-degree − out-degree; the judge is the only person with score n − 1.

**Complexity:** O(n + edges) time, O(n) space   **Edge cases:** n = 1 with no trust pairs (the single person is the judge)

``` cpp
int findJudge(int n, vector<vector<int>>& t) {
    vector<int> d(n + 1);
    for (auto& e : t) { d[e[0]]--; d[e[1]]++; }
    for (int i = 1; i <= n; i++) if (d[i] == n - 1) return i;
    return -1;
}
```

### 2. [Keys and Rooms](https://leetcode.com/problems/keys-and-rooms/) Medium [DFS](knowledge-base/dsa.md#dfs-components-and-cycles)

1.  Graph reachability from node 0: DFS with a stack and a visited array, count visited rooms.

**Complexity:** O(rooms + keys) time, O(rooms) space   **Edge cases:** Keys to rooms already visited

``` cpp
bool canVisitAllRooms(vector<vector<int>>& rooms) {
    vector<bool> seen(rooms.size()); vector<int> st{0}; seen[0] = true; int cnt = 1;
    while (!st.empty()) {
        int u = st.back(); st.pop_back();
        for (int v : rooms[u]) if (!seen[v]) { seen[v] = true; cnt++; st.push_back(v); }
    }
    return cnt == (int)rooms.size();
}
```

### 3. [Critical Connections in a Network](https://leetcode.com/problems/critical-connections-in-a-network/) Hard [Bridges (Tarjan)](knowledge-base/dsa.md#dfs-components-and-cycles)

1.  DFS assigning discovery times tin\[u\]; low\[u\] = smallest tin reachable from u's subtree using one back edge.
2.  Edge (u, v) to a child v is a bridge when low\[v\] \> tin\[u\].

**Complexity:** O(V + E) time, O(V + E) space   **Edge cases:** Skip the edge back to the parent; Disconnected graphs: start DFS from every unvisited node

``` cpp
vector<vector<int>> criticalConnections(int n, vector<vector<int>>& con) {
    vector<vector<int>> g(n); for (auto& e : con) { g[e[0]].push_back(e[1]); g[e[1]].push_back(e[0]); }
    vector<int> tin(n, -1), low(n); int timer = 0; vector<vector<int>> r;
    function<void(int, int)> dfs = [&](int u, int p) {
        tin[u] = low[u] = timer++;
        for (int v : g[u]) {
            if (v == p) continue;
            if (tin[v] != -1) low[u] = min(low[u], tin[v]);
            else { dfs(v, u); low[u] = min(low[u], low[v]); if (low[v] > tin[u]) r.push_back({u, v}); }
        }
    };
    for (int i = 0; i < n; i++) if (tin[i] == -1) dfs(i, -1);
    return r;
}
```

## SET 19. Dynamic programming

90 minutes · maximum 600 points · suggested date Sat 31 Jul 2027. Topics are hidden on purpose: working out the pattern is part of the test.

Problem 1[Min Cost Climbing Stairs ↗](https://leetcode.com/problems/min-cost-climbing-stairs/)Easy10 min · 100 pts

Pay cost\[i\] to step on stair i, then climb 1 or 2; start at 0 or 1. Minimum cost to reach the top.

https://leetcode.com/problems/min-cost-climbing-stairs/

Your score: \_\_\_\_\_\_ / 100    Time used: \_\_\_\_\_\_ min    Wrong submissions: \_\_\_\_\_\_

Problem 2[Longest String Chain ↗](https://leetcode.com/problems/longest-string-chain/)Medium30 min · 200 pts

A word is a predecessor of another if inserting one letter makes it. Find the longest chain.

https://leetcode.com/problems/longest-string-chain/

Your score: \_\_\_\_\_\_ / 200    Time used: \_\_\_\_\_\_ min    Wrong submissions: \_\_\_\_\_\_

Problem 3[Minimum Insertion Steps to Make a String Palindrome ↗](https://leetcode.com/problems/minimum-insertion-steps-to-make-a-string-palindrome/)Hard50 min · 300 pts

Fewest characters to insert anywhere so the string becomes a palindrome.

https://leetcode.com/problems/minimum-insertion-steps-to-make-a-string-palindrome/

Your score: \_\_\_\_\_\_ / 300    Time used: \_\_\_\_\_\_ min    Wrong submissions: \_\_\_\_\_\_

Total: \_\_\_\_\_\_ / 600 = \_\_\_\_\_\_ %    [Solutions for this set →](#set-19-solutions)

## SET 19. Solutions

Focus: DP-heavy rounds: 1D, chains, palindromes. Read the sketch first, then rewrite the code yourself from memory.

### 1. [Min Cost Climbing Stairs](https://leetcode.com/problems/min-cost-climbing-stairs/) Easy [1D DP](knowledge-base/dsa.md#dynamic-programming)

1.  dp\[i\] = min(dp\[i−1\] + cost\[i−1\], dp\[i−2\] + cost\[i−2\]); keep only two values.

**Complexity:** O(n) time, O(1) space   **Edge cases:** The top is one past the last stair

``` cpp
int minCostClimbingStairs(vector<int>& c) {
    int a = 0, b = 0;
    for (int i = 2; i <= (int)c.size(); i++) { int x = min(b + c[i - 1], a + c[i - 2]); a = b; b = x; }
    return b;
}
```

### 2. [Longest String Chain](https://leetcode.com/problems/longest-string-chain/) Medium [DP on sorted order](knowledge-base/dsa.md#dynamic-programming)

1.  Sort words by length. dp\[word\] = 1 + max dp\[word with one letter removed\] over all removals found so far.

**Complexity:** O(n · L²) time, O(n · L) space   **Edge cases:** Several words of the same length; Chains that skip a length do not count

``` cpp
int longestStrChain(vector<string>& w) {
    sort(w.begin(), w.end(), [](const string& a, const string& b) { return a.size() < b.size(); });
    unordered_map<string, int> dp; int best = 0;
    for (auto& s : w) {
        int cur = 1;
        for (size_t i = 0; i < s.size(); i++) {
            auto it = dp.find(s.substr(0, i) + s.substr(i + 1));
            if (it != dp.end()) cur = max(cur, it->second + 1);
        }
        dp[s] = cur; best = max(best, cur);
    }
    return best;
}
```

### 3. [Minimum Insertion Steps to Make a String Palindrome](https://leetcode.com/problems/minimum-insertion-steps-to-make-a-string-palindrome/) Hard [String DP](knowledge-base/dsa.md#string-dp-lcs-and-edit-distance)

1.  Characters already in the longest palindromic subsequence can stay; every other one needs a partner inserted.
2.  Answer = n − LPS(s), and LPS(s) = LCS(s, reverse(s)).

**Complexity:** O(n²) time, O(n²) space (O(n) with two rows)   **Edge cases:** Already a palindrome (answer 0)

``` cpp
int minInsertions(string s) {
    int n = s.size(); string t(s.rbegin(), s.rend()); vector<vector<int>> dp(n + 1, vector<int>(n + 1));
    for (int i = 1; i <= n; i++)
        for (int j = 1; j <= n; j++)
            dp[i][j] = s[i - 1] == t[j - 1] ? dp[i - 1][j - 1] + 1 : max(dp[i - 1][j], dp[i][j - 1]);
    return n - dp[n][n];
}
```

## SET 20. Heaps and greedy

90 minutes · maximum 600 points · suggested date Sat 7 Aug 2027. Topics are hidden on purpose: working out the pattern is part of the test.

Problem 1[Last Stone Weight ↗](https://leetcode.com/problems/last-stone-weight/)Easy10 min · 100 pts

Repeatedly smash the two heaviest stones; return the weight of the last stone (or 0).

https://leetcode.com/problems/last-stone-weight/

Your score: \_\_\_\_\_\_ / 100    Time used: \_\_\_\_\_\_ min    Wrong submissions: \_\_\_\_\_\_

Problem 2[Hand of Straights ↗](https://leetcode.com/problems/hand-of-straights/)Medium30 min · 200 pts

Can the cards be split into groups of k consecutive values?

https://leetcode.com/problems/hand-of-straights/

Your score: \_\_\_\_\_\_ / 200    Time used: \_\_\_\_\_\_ min    Wrong submissions: \_\_\_\_\_\_

Problem 3[IPO ↗](https://leetcode.com/problems/ipo/)Hard50 min · 300 pts

Start with capital w; do at most k projects, each needing capital\[i\] and adding profit\[i\]. Maximise final capital.

https://leetcode.com/problems/ipo/

Your score: \_\_\_\_\_\_ / 300    Time used: \_\_\_\_\_\_ min    Wrong submissions: \_\_\_\_\_\_

Total: \_\_\_\_\_\_ / 600 = \_\_\_\_\_\_ %    [Solutions for this set →](#set-20-solutions)

## SET 20. Solutions

Focus: Priority queues and exchange arguments. Read the sketch first, then rewrite the code yourself from memory.

### 1. [Last Stone Weight](https://leetcode.com/problems/last-stone-weight/) Easy [Heap](knowledge-base/dsa.md#heaps-and-priority-queues)

1.  Max-heap: pop two, push the difference if non-zero.

**Complexity:** O(n log n) time, O(n) space   **Edge cases:** All stones destroyed (return 0)

``` cpp
int lastStoneWeight(vector<int>& s) {
    priority_queue<int> pq(s.begin(), s.end());
    while (pq.size() > 1) { int a = pq.top(); pq.pop(); int b = pq.top(); pq.pop(); if (a != b) pq.push(a - b); }
    return pq.empty() ? 0 : pq.top();
}
```

### 2. [Hand of Straights](https://leetcode.com/problems/hand-of-straights/) Medium [Greedy with an ordered map](knowledge-base/dsa.md#greedy-algorithms)

1.  The smallest remaining card must start a group. Walk an ordered count map; for each value with count f, take f from each of the next k values.

**Complexity:** O(n log n) time, O(n) space   **Edge cases:** n not divisible by k; Duplicates

``` cpp
bool isNStraightHand(vector<int>& h, int k) {
    if (h.size() % k) return false;
    map<int, int> c; for (int x : h) c[x]++;
    for (auto it = c.begin(); it != c.end(); ++it) {
        int f = it->second; if (!f) continue;
        for (int d = 0; d < k; d++) {
            auto jt = c.find(it->first + d);
            if (jt == c.end() || jt->second < f) return false;
            jt->second -= f;
        }
    }
    return true;
}
```

### 3. [IPO](https://leetcode.com/problems/ipo/) Hard [Two heaps / greedy](knowledge-base/dsa.md#heaps-and-priority-queues)

1.  Sort projects by required capital. Each round, push every affordable project's profit into a max-heap and take the best one.

**Complexity:** O(n log n) time, O(n) space   **Edge cases:** No affordable project left: stop early

``` cpp
int findMaximizedCapital(int k, int w, vector<int>& p, vector<int>& c) {
    int n = p.size(); vector<pair<int, int>> v; for (int i = 0; i < n; i++) v.push_back({c[i], p[i]});
    sort(v.begin(), v.end());
    priority_queue<int> pq; int i = 0;
    while (k--) {
        while (i < n && v[i].first <= w) pq.push(v[i++].second);
        if (pq.empty()) break;
        w += pq.top(); pq.pop();
    }
    return w;
}
```

## SET 21. Hashing and prefix sums

90 minutes · maximum 600 points · suggested date Sat 14 Aug 2027. Topics are hidden on purpose: working out the pattern is part of the test.

Problem 1[Isomorphic Strings ↗](https://leetcode.com/problems/isomorphic-strings/)Easy10 min · 100 pts

Can the characters of s be replaced one-to-one to get t?

https://leetcode.com/problems/isomorphic-strings/

Your score: \_\_\_\_\_\_ / 100    Time used: \_\_\_\_\_\_ min    Wrong submissions: \_\_\_\_\_\_

Problem 2[Continuous Subarray Sum ↗](https://leetcode.com/problems/continuous-subarray-sum/)Medium30 min · 200 pts

Is there a subarray of length at least 2 whose sum is a multiple of k?

https://leetcode.com/problems/continuous-subarray-sum/

Your score: \_\_\_\_\_\_ / 200    Time used: \_\_\_\_\_\_ min    Wrong submissions: \_\_\_\_\_\_

Problem 3[Subarrays with K Different Integers ↗](https://leetcode.com/problems/subarrays-with-k-different-integers/)Hard50 min · 300 pts

Count subarrays with exactly k distinct values.

https://leetcode.com/problems/subarrays-with-k-different-integers/

Your score: \_\_\_\_\_\_ / 300    Time used: \_\_\_\_\_\_ min    Wrong submissions: \_\_\_\_\_\_

Total: \_\_\_\_\_\_ / 600 = \_\_\_\_\_\_ %    [Solutions for this set →](#set-21-solutions)

## SET 21. Solutions

Focus: Maps, remainders and 'at most k' counting. Read the sketch first, then rewrite the code yourself from memory.

### 1. [Isomorphic Strings](https://leetcode.com/problems/isomorphic-strings/) Easy [Hashing](knowledge-base/dsa.md#hashing-and-frequency-maps)

1.  Remember the last position each character was seen in s and in t; they must always match.

**Complexity:** O(n) time, O(1) space   **Edge cases:** Two characters mapping to the same one ('badc' → 'baba' is false)

``` text
bool isIsomorphic(string s, string t) {
    int a[256] = {}, b[256] = {};
    for (size_t i = 0; i < s.size(); i++) {
        unsigned char x = s[i], y = t[i];
        if (a[x] != b[y]) return false;
        a[x] = b[y] = i + 1;
    }
    return true;
}
```

### 2. [Continuous Subarray Sum](https://leetcode.com/problems/continuous-subarray-sum/) Medium [Prefix sums mod k](knowledge-base/dsa.md#prefix-sums)

1.  Two prefix sums with the same remainder mod k bound a subarray divisible by k. Store the first index of each remainder (remainder 0 at index −1).

**Complexity:** O(n) time, O(min(n, k)) space   **Edge cases:** Length must be at least 2; Zeros: \[0, 0\] is divisible by any k

``` cpp
bool checkSubarraySum(vector<int>& a, int k) {
    unordered_map<int, int> first{{0, -1}}; int s = 0;
    for (int i = 0; i < (int)a.size(); i++) {
        s = (s + a[i]) % k;
        auto it = first.find(s);
        if (it == first.end()) first[s] = i;
        else if (i - it->second >= 2) return true;
    }
    return false;
}
```

### 3. [Subarrays with K Different Integers](https://leetcode.com/problems/subarrays-with-k-different-integers/) Hard [Sliding window (at most k)](knowledge-base/dsa.md#sliding-window)

1.  exactly(k) = atMost(k) − atMost(k − 1). atMost uses a sliding window: for each right end, all windows ending there with left ≥ l are valid (r − l + 1 of them).

**Complexity:** O(n) time, O(n) space   **Edge cases:** The answer can exceed int for large n in variants: use long long inside

``` cpp
long long atMost(vector<int>& a, int k) {
    unordered_map<int, int> c; int l = 0; long long res = 0;
    for (int i = 0; i < (int)a.size(); i++) {
        if (c[a[i]]++ == 0) k--;
        while (k < 0) { if (--c[a[l]] == 0) k++; l++; }
        res += i - l + 1;
    }
    return res;
}
int subarraysWithKDistinct(vector<int>& a, int k) { return atMost(a, k) - atMost(a, k - 1); }
```

## SET 22. Trees

90 minutes · maximum 600 points · suggested date Sat 21 Aug 2027. Topics are hidden on purpose: working out the pattern is part of the test.

Problem 1[Symmetric Tree ↗](https://leetcode.com/problems/symmetric-tree/)Easy10 min · 100 pts

Is the tree a mirror of itself?

https://leetcode.com/problems/symmetric-tree/

Your score: \_\_\_\_\_\_ / 100    Time used: \_\_\_\_\_\_ min    Wrong submissions: \_\_\_\_\_\_

Problem 2[Maximum Width of Binary Tree ↗](https://leetcode.com/problems/maximum-width-of-binary-tree/)Medium30 min · 200 pts

Width of a level = distance between its leftmost and rightmost nodes, counting the gaps. Return the maximum.

https://leetcode.com/problems/maximum-width-of-binary-tree/

Your score: \_\_\_\_\_\_ / 200    Time used: \_\_\_\_\_\_ min    Wrong submissions: \_\_\_\_\_\_

Problem 3[Binary Tree Cameras ↗](https://leetcode.com/problems/binary-tree-cameras/)Hard50 min · 300 pts

A camera covers its node, parent and children. Minimum cameras to cover every node.

https://leetcode.com/problems/binary-tree-cameras/

Your score: \_\_\_\_\_\_ / 300    Time used: \_\_\_\_\_\_ min    Wrong submissions: \_\_\_\_\_\_

Total: \_\_\_\_\_\_ / 600 = \_\_\_\_\_\_ %    [Solutions for this set →](#set-22-solutions)

## SET 22. Solutions

Focus: Recursion on trees, level indices, greedy from the leaves. Read the sketch first, then rewrite the code yourself from memory.

### 1. [Symmetric Tree](https://leetcode.com/problems/symmetric-tree/) Easy [Tree recursion](knowledge-base/dsa.md#binary-trees)

1.  Compare left and right subtrees as mirrors: values equal, outer pair mirrors, inner pair mirrors.

**Complexity:** O(n) time, O(h) stack   **Edge cases:** Empty tree is symmetric

``` text
bool mirror(TreeNode* a, TreeNode* b) {
    if (!a || !b) return a == b;
    return a->val == b->val && mirror(a->left, b->right) && mirror(a->right, b->left);
}
bool isSymmetric(TreeNode* r) { return !r || mirror(r->left, r->right); }
```

### 2. [Maximum Width of Binary Tree](https://leetcode.com/problems/maximum-width-of-binary-tree/) Medium [BFS with indices](knowledge-base/dsa.md#bfs-and-graph-basics)

1.  Number nodes like a heap (children 2i and 2i + 1). Subtract each level's first index so numbers stay small; width = last − first + 1.

**Complexity:** O(n) time, O(n) space   **Edge cases:** Index overflow on deep skewed trees (normalise per level, use unsigned 64-bit)

``` text
int widthOfBinaryTree(TreeNode* root) {
    if (!root) return 0;
    unsigned long long best = 0; queue<pair<TreeNode*, unsigned long long>> q; q.push({root, 0});
    while (!q.empty()) {
        int n = q.size(); unsigned long long base = q.front().second, first = 0, last = 0;
        for (int i = 0; i < n; i++) {
            auto [x, id] = q.front(); q.pop(); id -= base;
            if (i == 0) first = id;
            last = id;
            if (x->left) q.push({x->left, 2 * id});
            if (x->right) q.push({x->right, 2 * id + 1});
        }
        best = max(best, last - first + 1);
    }
    return (int)best;
}
```

### 3. [Binary Tree Cameras](https://leetcode.com/problems/binary-tree-cameras/) Hard [Greedy DFS (tree states)](knowledge-base/dsa.md#binary-trees)

1.  Post-order states: 0 = not covered, 1 = has a camera, 2 = covered without one. Null counts as covered.
2.  If a child is uncovered, put a camera here; else if a child has a camera, this node is covered; else it is uncovered and its parent will handle it.
3.  Add one camera if the root ends uncovered.

**Complexity:** O(n) time, O(h) stack   **Edge cases:** The root left uncovered; Order of evaluation: run the DFS before reading the counter

``` text
int cams;
int go(TreeNode* n) {
    if (!n) return 2;
    int l = go(n->left), r = go(n->right);
    if (l == 0 || r == 0) { cams++; return 1; }
    return (l == 1 || r == 1) ? 2 : 0;
}
int minCameraCover(TreeNode* root) { cams = 0; int s = go(root); return cams + (s == 0); }
```

## SET 23. Matrices

90 minutes · maximum 600 points · suggested date Sat 28 Aug 2027. Topics are hidden on purpose: working out the pattern is part of the test.

Problem 1[Flood Fill ↗](https://leetcode.com/problems/flood-fill/)Easy10 min · 100 pts

Recolour the connected region of the starting pixel's colour.

https://leetcode.com/problems/flood-fill/

Your score: \_\_\_\_\_\_ / 100    Time used: \_\_\_\_\_\_ min    Wrong submissions: \_\_\_\_\_\_

Problem 2[Search a 2D Matrix II ↗](https://leetcode.com/problems/search-a-2d-matrix-ii/)Medium25 min · 200 pts

Rows and columns are each sorted ascending. Is the target present?

https://leetcode.com/problems/search-a-2d-matrix-ii/

Your score: \_\_\_\_\_\_ / 200    Time used: \_\_\_\_\_\_ min    Wrong submissions: \_\_\_\_\_\_

Problem 3[Trapping Rain Water II ↗](https://leetcode.com/problems/trapping-rain-water-ii/)Hard55 min · 300 pts

A height map on a grid: how much rain water stays trapped?

https://leetcode.com/problems/trapping-rain-water-ii/

Your score: \_\_\_\_\_\_ / 300    Time used: \_\_\_\_\_\_ min    Wrong submissions: \_\_\_\_\_\_

Total: \_\_\_\_\_\_ / 600 = \_\_\_\_\_\_ %    [Solutions for this set →](#set-23-solutions)

## SET 23. Solutions

Focus: Grid recursion, staircase search, heap from the border. Read the sketch first, then rewrite the code yourself from memory.

### 1. [Flood Fill](https://leetcode.com/problems/flood-fill/) Easy [DFS on a grid](knowledge-base/dsa.md#dfs-components-and-cycles)

1.  DFS from the start, painting cells of the original colour. If the new colour equals the old one, return at once (otherwise infinite recursion).

**Complexity:** O(R · C) time and stack   **Edge cases:** New colour equal to the old colour

``` cpp
void paint(vector<vector<int>>& g, int r, int c, int from, int to) {
    if (r < 0 || c < 0 || r >= (int)g.size() || c >= (int)g[0].size() || g[r][c] != from) return;
    g[r][c] = to;
    paint(g, r + 1, c, from, to); paint(g, r - 1, c, from, to); paint(g, r, c + 1, from, to); paint(g, r, c - 1, from, to);
}
vector<vector<int>> floodFill(vector<vector<int>>& g, int sr, int sc, int color) {
    if (g[sr][sc] != color) paint(g, sr, sc, g[sr][sc], color);
    return g;
}
```

### 2. [Search a 2D Matrix II](https://leetcode.com/problems/search-a-2d-matrix-ii/) Medium [Staircase search](knowledge-base/dsa.md#binary-search)

1.  Start at the top-right corner: if it is too big move left, if too small move down. Each step removes a row or a column.

**Complexity:** O(R + C) time, O(1) space   **Edge cases:** Binary search per row works too but is O(R log C)

``` cpp
bool searchMatrix(vector<vector<int>>& m, int t) {
    int r = 0, c = m[0].size() - 1;
    while (r < (int)m.size() && c >= 0) {
        if (m[r][c] == t) return true;
        if (m[r][c] > t) c--; else r++;
    }
    return false;
}
```

### 3. [Trapping Rain Water II](https://leetcode.com/problems/trapping-rain-water-ii/) Hard [Min-heap from the border](knowledge-base/dsa.md#heaps-and-priority-queues)

1.  Water level is set by the lowest wall around. Push all border cells into a min-heap. Pop the lowest; for each unseen neighbour, it holds max(0, level − height) water; push it with level max(level, height).

**Complexity:** O(RC log(RC)) time, O(RC) space   **Edge cases:** Grids smaller than 3 × 3 trap nothing

``` cpp
int trapRainWater(vector<vector<int>>& h) {
    int R = h.size(), C = h[0].size(); if (R < 3 || C < 3) return 0;
    priority_queue<array<int, 3>, vector<array<int, 3>>, greater<>> pq; vector<vector<bool>> seen(R, vector<bool>(C));
    for (int r = 0; r < R; r++) for (int c = 0; c < C; c++)
        if (r == 0 || c == 0 || r == R - 1 || c == C - 1) { pq.push({h[r][c], r, c}); seen[r][c] = true; }
    int water = 0, dr[] = {1, -1, 0, 0}, dc[] = {0, 0, 1, -1};
    while (!pq.empty()) {
        auto [ht, r, c] = pq.top(); pq.pop();
        for (int k = 0; k < 4; k++) {
            int nr = r + dr[k], nc = c + dc[k];
            if (nr < 0 || nc < 0 || nr >= R || nc >= C || seen[nr][nc]) continue;
            seen[nr][nc] = true; water += max(0, ht - h[nr][nc]); pq.push({max(ht, h[nr][nc]), nr, nc});
        }
    }
    return water;
}
```

## SET 24. Final mixed

90 minutes · maximum 600 points · suggested date Sat 4 Sep 2027. Topics are hidden on purpose: working out the pattern is part of the test.

Problem 1[Valid Palindrome II ↗](https://leetcode.com/problems/valid-palindrome-ii/)Easy15 min · 100 pts

Can the string become a palindrome by deleting at most one character?

https://leetcode.com/problems/valid-palindrome-ii/

Your score: \_\_\_\_\_\_ / 100    Time used: \_\_\_\_\_\_ min    Wrong submissions: \_\_\_\_\_\_

Problem 2[Max Area of Island ↗](https://leetcode.com/problems/max-area-of-island/)Medium25 min · 200 pts

Largest 4-connected group of 1s in a grid.

https://leetcode.com/problems/max-area-of-island/

Your score: \_\_\_\_\_\_ / 200    Time used: \_\_\_\_\_\_ min    Wrong submissions: \_\_\_\_\_\_

Problem 3[Sliding Window Median ↗](https://leetcode.com/problems/sliding-window-median/)Hard50 min · 300 pts

Median of every window of size k.

https://leetcode.com/problems/sliding-window-median/

Your score: \_\_\_\_\_\_ / 300    Time used: \_\_\_\_\_\_ min    Wrong submissions: \_\_\_\_\_\_

Total: \_\_\_\_\_\_ / 600 = \_\_\_\_\_\_ %    [Solutions for this set →](#set-24-solutions)

## SET 24. Solutions

Focus: One of each: two pointers, grid DFS, two multisets. Read the sketch first, then rewrite the code yourself from memory.

### 1. [Valid Palindrome II](https://leetcode.com/problems/valid-palindrome-ii/) Easy [Two pointers](knowledge-base/dsa.md#two-pointers)

1.  Move pointers inwards; at the first mismatch, try skipping the left or the right character and check the rest.

**Complexity:** O(n) time, O(1) space   **Edge cases:** Only one deletion allowed: do not recurse again

``` text
bool isPal(const string& s, int i, int j) { while (i < j) if (s[i++] != s[j--]) return false; return true; }
bool validPalindrome(string s) {
    int i = 0, j = s.size() - 1;
    while (i < j) { if (s[i] != s[j]) return isPal(s, i + 1, j) || isPal(s, i, j - 1); i++; j--; }
    return true;
}
```

### 2. [Max Area of Island](https://leetcode.com/problems/max-area-of-island/) Medium [DFS on a grid](knowledge-base/dsa.md#dfs-components-and-cycles)

1.  DFS from each land cell, sinking cells (set to 0) as they are counted so each is counted once.

**Complexity:** O(R · C) time, O(R · C) stack in the worst case   **Edge cases:** All water (answer 0)

``` cpp
int area(vector<vector<int>>& g, int r, int c) {
    if (r < 0 || c < 0 || r >= (int)g.size() || c >= (int)g[0].size() || !g[r][c]) return 0;
    g[r][c] = 0;
    return 1 + area(g, r + 1, c) + area(g, r - 1, c) + area(g, r, c + 1) + area(g, r, c - 1);
}
int maxAreaOfIsland(vector<vector<int>>& g) {
    int best = 0;
    for (int r = 0; r < (int)g.size(); r++) for (int c = 0; c < (int)g[0].size(); c++) best = max(best, area(g, r, c));
    return best;
}
```

### 3. [Sliding Window Median](https://leetcode.com/problems/sliding-window-median/) Hard [Two multisets](knowledge-base/dsa.md#heaps-and-priority-queues)

1.  Keep the smaller half in lo and the larger in hi (lo has the extra element when k is odd).
2.  Insert into the right half, remove the element leaving the window from whichever half holds it, then rebalance.

**Complexity:** O(n log k) time, O(k) space   **Edge cases:** Overflow when averaging two large ints (convert to double first); Duplicates: erase one copy with find, not the value

``` cpp
vector<double> medianSlidingWindow(vector<int>& a, int k) {
    multiset<int> lo, hi; vector<double> r;
    auto balance = [&]() {
        while (lo.size() > hi.size() + 1) { hi.insert(*prev(lo.end())); lo.erase(prev(lo.end())); }
        while (hi.size() > lo.size()) { lo.insert(*hi.begin()); hi.erase(hi.begin()); }
    };
    for (int i = 0; i < (int)a.size(); i++) {
        if (lo.empty() || a[i] <= *prev(lo.end())) lo.insert(a[i]); else hi.insert(a[i]);
        if (i >= k) { int out = a[i - k]; if (out <= *prev(lo.end())) lo.erase(lo.find(out)); else hi.erase(hi.find(out)); }
        balance();
        if (i >= k - 1) r.push_back(k % 2 ? (double)*prev(lo.end()) : ((double)*prev(lo.end()) + (double)*hi.begin()) / 2.0);
    }
    return r;
}
```
