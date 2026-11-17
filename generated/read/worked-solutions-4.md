WORKED SOLUTIONS · PART IV · HARD

# 25 hard problems tested solutions

Twenty-five hard (L3) LeetCode problems of the kind product companies use in final rounds, none of them in Parts I to III or the 72 OA practice problems (195 problems checked by script). Each page gives the pattern, the key idea, the steps, a C++17 solution, the test it passed, the complexity, the traps and the follow-up questions interviewers ask. Levels: L1 0, L2 0, L3 25.

**How to use.** Read the title, try the problem on LeetCode for 40 minutes, then open the page. If you needed the solution, log it in your revision tracker and redo it in 3, 7 and 21 days. Every solution here was compiled with `g++ -std=c++17 -Wall -Wextra -fsanitize=address,undefined` and passed the test shown.

## Index (grouped by pattern)

| \#  | Problem                                               | Pattern                     | Level |
|-----|-------------------------------------------------------|-----------------------------|-------|
| 1   | [Wildcard Matching](#01-wildcard-matching)                          | String DP                   | L3    |
| 2   | [Shortest Palindrome](#02-shortest-palindrome)                       | String algorithms           | L3    |
| 3   | [Substring with Concatenation of All Words](#03-substring-with-concatenation-of-all-words) | Sliding window              | L3    |
| 4   | [Word Break II](#04-word-break-ii)                             | Backtracking                | L3    |
| 5   | [Integer to English Words](#05-integer-to-english-words)                  | Simulation                  | L3    |
| 6   | [Basic Calculator](#06-basic-calculator)                          | Stack                       | L3    |
| 7   | [Max Points on a Line](#07-max-points-on-a-line)                      | Geometry and hashing        | L3    |
| 8   | [The Skyline Problem](#08-the-skyline-problem)                       | Heap                        | L3    |
| 9   | [Minimum Cost to Hire K Workers](#09-minimum-cost-to-hire-k-workers)            | Heap                        | L3    |
| 10  | [Course Schedule III](#10-course-schedule-iii)                       | Greedy                      | L3    |
| 11  | [Word Search II](#11-word-search-ii)                            | Trie + backtracking         | L3    |
| 12  | [Remove Invalid Parentheses](#12-remove-invalid-parentheses)                | BFS                         | L3    |
| 13  | [Bus Routes](#13-bus-routes)                                | BFS                         | L3    |
| 14  | [Shortest Path Visiting All Nodes](#14-shortest-path-visiting-all-nodes)         | Bitmask BFS                 | L3    |
| 15  | [Making A Large Island](#15-making-a-large-island)                    | Union-Find                  | L3    |
| 16  | [Count of Range Sum](#16-count-of-range-sum)                       | Divide and conquer          | L3    |
| 17  | [Find K-th Smallest Pair Distance](#17-find-k-th-smallest-pair-distance)         | Binary search on the answer | L3    |
| 18  | [Dungeon Game](#18-dungeon-game)                             | Grid DP                     | L3    |
| 19  | [Cherry Pickup II](#19-cherry-pickup-ii)                         | Grid DP                     | L3    |
| 20  | [Best Time to Buy and Sell Stock III](#20-best-time-to-buy-and-sell-stock-iii)      | Stock DP                    | L3    |
| 21  | [Best Time to Buy and Sell Stock IV](#21-best-time-to-buy-and-sell-stock-iv)       | Stock DP                    | L3    |
| 22  | [Frog Jump](#22-frog-jump)                                | DP                          | L3    |
| 23  | [Russian Doll Envelopes](#23-russian-doll-envelopes)                   | LIS                         | L3    |
| 24  | [Strange Printer](#24-strange-printer)                          | Interval DP                 | L3    |
| 25  | [Number of Digit One](#25-number-of-digit-one)                      | Digit DP                    | L3    |

Problem statements are on LeetCode (each page links to it). Pattern pages link to the online Knowledge Base. Explanations and code are original.

## 01. Wildcard Matching

L3 [String DP](knowledge-base/dsa.md#string-dp-lcs-and-edit-distance) · [LeetCode ↗](https://leetcode.com/problems/wildcard-matching/) · Classic 2D DP; '\*' is the tricky case.

### Key idea

dp\[i\]\[j\] = s\[0..i) matches p\[0..j). '?' or an equal letter consumes one of each. '\*' either matches nothing (dp\[i\]\[j−1\]) or one more character of s (dp\[i−1\]\[j\]).

### Steps

1.  dp\[0\]\[0\] = true; dp\[0\]\[j\] = dp\[0\]\[j−1\] while p\[j−1\] is '\*'
2.  Fill row by row with the three cases
3.  Answer dp\[n\]\[m\]

### C++17 solution

``` cpp
class Solution {
public:
    bool isMatch(string s, string p) {
        int n = s.size(), m = p.size(); vector<vector<char>> dp(n + 1, vector<char>(m + 1, 0)); dp[0][0] = 1;
        for (int j = 1; j <= m; j++) dp[0][j] = p[j - 1] == '*' && dp[0][j - 1];
        for (int i = 1; i <= n; i++)
            for (int j = 1; j <= m; j++) {
                if (p[j - 1] == '*') dp[i][j] = dp[i][j - 1] || dp[i - 1][j];
                else dp[i][j] = (p[j - 1] == '?' || p[j - 1] == s[i - 1]) && dp[i - 1][j - 1];
            }
        return dp[n][m];
    }
};
```

### Test it passed

``` text
Solution S; assert(!S.isMatch("aa", "a") && S.isMatch("aa", "*") && !S.isMatch("cb", "?a") && S.isMatch("adceb", "*a*b") && !S.isMatch("acdcb", "a*c?b") && S.isMatch("", "***"));
```

### Complexity

O(nm) time, O(nm) space (O(m) with one row)

### Traps

- Forgetting the leading-stars row (pattern '\*\*\*' matches an empty string)

### Follow-ups

- Greedy two-pointer solution with backtracking to the last '\*' runs in O(nm) worst case but O(1) space.
- Compare with Regular Expression Matching, where '\*' repeats the previous character.

## 02. Shortest Palindrome

L3 [String algorithms](knowledge-base/dsa.md#string-algorithms-kmp-z-hashing) · [LeetCode ↗](https://leetcode.com/problems/shortest-palindrome/) · KMP prefix function in disguise.

### Key idea

Add the fewest characters in front: find the longest prefix of s that is a palindrome. Build t = s + '#' + reverse(s); the KMP prefix function at the end of t is that length. Prepend the reverse of the rest.

### Steps

1.  t = s + '#' + rev
2.  Compute the prefix (failure) function of t
3.  k = pi.back(); return reverse(s.substr(k)) + s

### C++17 solution

``` cpp
class Solution {
public:
    string shortestPalindrome(string s) {
        string r(s.rbegin(), s.rend()), t = s + "#" + r; vector<int> pi(t.size(), 0);
        for (size_t i = 1; i < t.size(); i++) {
            int k = pi[i - 1];
            while (k > 0 && t[i] != t[k]) k = pi[k - 1];
            if (t[i] == t[k]) k++;
            pi[i] = k;
        }
        return r.substr(0, s.size() - pi.back()) + s;
    }
};
```

### Test it passed

``` text
Solution S; assert(S.shortestPalindrome("aacecaaa") == "aaacecaaa" && S.shortestPalindrome("abcd") == "dcbabcd" && S.shortestPalindrome("") == "" && S.shortestPalindrome("aba") == "aba");
```

### Complexity

O(n) time and space

### Traps

- Without the '#', the match can run past the middle

### Follow-ups

- Brute force checks each prefix for being a palindrome in O(n²).
- Explain the prefix function in one sentence.

## 03. Substring with Concatenation of All Words

L3 [Sliding window](knowledge-base/dsa.md#sliding-window) · [LeetCode ↗](https://leetcode.com/problems/substring-with-concatenation-of-all-words/) · Counting window over equal-length words.

### Key idea

All words have the same length L. For each start offset 0..L−1, slide a window word by word, keeping counts; shrink from the left when a word is over-used; record the start when the window holds exactly all words.

### Steps

1.  need = counts of words
2.  For off in 0..L−1: left = off, seen = {}, cnt = 0
3.  Take the next word; if unknown reset; else add and shrink while over-used; if cnt == k record left

### C++17 solution

``` cpp
class Solution {
public:
    vector<int> findSubstring(string s, vector<string>& words) {
        vector<int> r; if (words.empty()) return r;
        int L = words[0].size(), k = words.size(), n = s.size(); unordered_map<string, int> need;
        for (auto& w : words) need[w]++;
        for (int off = 0; off < L; off++) {
            unordered_map<string, int> seen; int left = off, cnt = 0;
            for (int j = off; j + L <= n; j += L) {
                string w = s.substr(j, L);
                if (!need.count(w)) { seen.clear(); cnt = 0; left = j + L; continue; }
                seen[w]++; cnt++;
                while (seen[w] > need[w]) { seen[s.substr(left, L)]--; cnt--; left += L; }
                if (cnt == k) { r.push_back(left); seen[s.substr(left, L)]--; cnt--; left += L; }
            }
        }
        sort(r.begin(), r.end()); return r;
    }
};
```

### Test it passed

``` cpp
Solution S; vector<string> a{"foo","bar"}, b{"word","good","best","word"}, c{"bar","foo","the"};
assert((S.findSubstring("barfoothefoobarman", a) == vector<int>{0,9}) && S.findSubstring("wordgoodgoodgoodbestword", b).empty());
assert((S.findSubstring("barfoofoobarthefoobarman", c) == vector<int>{6,9,12}));
```

### Complexity

O(n · L) time, O(k) space

### Traps

- Duplicate words in the list (use counts, not a set)
- Resetting the window on an unknown word

### Follow-ups

- Simpler O(n · k · L): check every start independently.

## 04. Word Break II

L3 [Backtracking](knowledge-base/dsa.md#recursion-and-backtracking) · [LeetCode ↗](https://leetcode.com/problems/word-break-ii/) · Word Break with all answers: memoise by start index.

### Key idea

From position i, try every dictionary word that matches s at i and recurse on the rest; cache the list of sentences for each i so each suffix is solved once.

### Steps

1.  memo\[i\] = all sentences for s\[i..\]
2.  Base: i == n gives one empty sentence
3.  Join word + ' ' + rest

### C++17 solution

``` cpp
class Solution {
    unordered_map<int, vector<string>> memo; unordered_set<string> dict; string s;
    vector<string> go(int i) {
        if (i == (int)s.size()) return {""};
        auto it = memo.find(i); if (it != memo.end()) return it->second;
        vector<string> out;
        for (int j = i + 1; j <= (int)s.size(); j++) {
            string w = s.substr(i, j - i);
            if (!dict.count(w)) continue;
            for (auto& rest : go(j)) out.push_back(rest.empty() ? w : w + " " + rest);
        }
        return memo[i] = out;
    }
public:
    vector<string> wordBreak(string str, vector<string>& words) {
        s = str; dict = unordered_set<string>(words.begin(), words.end()); memo.clear();
        auto r = go(0); sort(r.begin(), r.end()); return r;
    }
};
```

### Test it passed

``` cpp
Solution S; vector<string> a{"cat","cats","and","sand","dog"}, b{"apple","pen","applepen","pine","pineapple"};
assert((S.wordBreak("catsanddog", a) == vector<string>{"cat sand dog","cats and dog"}));
assert((S.wordBreak("pineapplepenapple", b) == vector<string>{"pine apple pen apple","pine applepen apple","pineapple pen apple"}) && S.wordBreak("catsandog", a).empty());
```

### Complexity

Exponential output in the worst case; memo avoids recomputing suffixes

### Traps

- Inputs like 'aaaa…b' with words a, aa, aaa: first check Word Break I to fail fast

### Follow-ups

- Return only the count of sentences (a 1D DP).

## 05. Integer to English Words

L3 [Simulation](knowledge-base/dsa.md#string-algorithms-kmp-z-hashing) · [LeetCode ↗](https://leetcode.com/problems/integer-to-english-words/) · Careful case handling under time pressure.

### Key idea

Split into groups of three digits (units, thousand, million, billion). Each group under 1000 is spoken the same way: hundreds, then tens (with 10–19 special), then ones.

### Steps

1.  Tables for 1–19 and tens
2.  helper(n \< 1000)
3.  Walk groups from billions down; skip zero groups; 0 is 'Zero'

### C++17 solution

``` cpp
class Solution {
    vector<string> lo{"", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen"};
    vector<string> tens{"", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"};
    string three(int n) {
        string r;
        if (n >= 100) { r = lo[n / 100] + " Hundred"; n %= 100; }
        if (n >= 20) { r += (r.empty() ? "" : " ") + tens[n / 10]; n %= 10; }
        if (n > 0) r += (r.empty() ? "" : " ") + lo[n];
        return r;
    }
public:
    string numberToWords(int num) {
        if (num == 0) return "Zero";
        vector<pair<int, string>> g{{1000000000, "Billion"}, {1000000, "Million"}, {1000, "Thousand"}, {1, ""}}; string r;
        for (auto& [v, name] : g)
            if (num >= v) { string part = three(num / v) + (name.empty() ? "" : " " + name); r += (r.empty() ? "" : " ") + part; num %= v; }
        return r;
    }
};
```

### Test it passed

``` text
Solution S; assert(S.numberToWords(123) == "One Hundred Twenty Three" && S.numberToWords(12345) == "Twelve Thousand Three Hundred Forty Five");
assert(S.numberToWords(1234567) == "One Million Two Hundred Thirty Four Thousand Five Hundred Sixty Seven" && S.numberToWords(0) == "Zero" && S.numberToWords(1000010) == "One Million Ten");
```

### Complexity

O(1) (at most 10 digits)

### Traps

- Extra spaces around empty parts
- Numbers like 1,000,010 with zero groups in the middle

### Follow-ups

- Indian numbering (lakh, crore) instead: groups of 3 then 2 digits.

## 06. Basic Calculator

L3 [Stack](knowledge-base/dsa.md#stacks-and-queues) · [LeetCode ↗](https://leetcode.com/problems/basic-calculator/) · Parentheses with + and − only.

### Key idea

Keep a running result and a sign. On '(' push the current result and sign and start fresh; on ')' pop and combine: result = saved + savedSign × result.

### Steps

1.  Parse numbers digit by digit
2.  '+'/'−' add the pending number with the sign, set the new sign
3.  '(' push (result, sign); ')' finish the number, then combine with the popped pair

### C++17 solution

``` cpp
class Solution {
public:
    int calculate(string s) {
        long long res = 0, num = 0; int sign = 1; stack<pair<long long, int>> st;
        for (char c : s) {
            if (isdigit(c)) num = num * 10 + (c - '0');
            else if (c == '+' || c == '-') { res += sign * num; num = 0; sign = c == '+' ? 1 : -1; }
            else if (c == '(') { st.push({res, sign}); res = 0; sign = 1; }
            else if (c == ')') { res += sign * num; num = 0; auto [r, sg] = st.top(); st.pop(); res = r + sg * res; }
        }
        return (int)(res + sign * num);
    }
};
```

### Test it passed

``` text
Solution S; assert(S.calculate("1 + 1") == 2 && S.calculate(" 2-1 + 2 ") == 3 && S.calculate("(1+(4+5+2)-3)+(6+8)") == 23 && S.calculate("-(2+3)") == -5 && S.calculate("1-(-2)") == 3);
```

### Complexity

O(n) time, O(n) stack

### Traps

- Unary minus at the start or after '('
- Forgetting the last number after the loop

### Follow-ups

- Add \* and / (Basic Calculator III): recursion per parenthesis level.

## 07. Max Points on a Line

L3 [Geometry and hashing](knowledge-base/dsa.md#hashing-and-frequency-maps) · [LeetCode ↗](https://leetcode.com/problems/max-points-on-a-line/) · Exact slopes, not doubles.

### Key idea

For each point, count the other points by normalised direction (dx, dy) divided by their gcd with a fixed sign. The biggest count + 1 is the best line through that point.

### Steps

1.  For i: map\<pair\<int,int\>, int\>
2.  dx, dy; g = gcd; normalise sign so dx \> 0, or dx == 0 and dy \> 0
3.  best = max(best, count + 1)

### C++17 solution

``` cpp
class Solution {
public:
    int maxPoints(vector<vector<int>>& p) {
        int n = p.size(), best = min(n, 1);
        for (int i = 0; i < n; i++) {
            map<pair<int, int>, int> cnt;
            for (int j = i + 1; j < n; j++) {
                int dx = p[j][0] - p[i][0], dy = p[j][1] - p[i][1], g = gcd(dx, dy);
                dx /= g; dy /= g;
                if (dx < 0 || (dx == 0 && dy < 0)) { dx = -dx; dy = -dy; }
                best = max(best, ++cnt[{dx, dy}] + 1);
            }
        }
        return best;
    }
};
```

### Test it passed

``` cpp
vector<vector<int>> a{{1,1},{2,2},{3,3}}, b{{1,1},{3,2},{5,3},{4,1},{2,3},{1,4}}, c{{0,0}}; Solution S; assert(S.maxPoints(a) == 3 && S.maxPoints(b) == 4 && S.maxPoints(c) == 1);
```

### Complexity

O(n² log n) time, O(n) space

### Traps

- Floating-point slopes (precision errors)
- Vertical lines (dx = 0)

### Follow-ups

- Duplicate points: count them separately and add to every line.

## 08. The Skyline Problem

L3 [Heap](knowledge-base/dsa.md#heaps-and-priority-queues) · [LeetCode ↗](https://leetcode.com/problems/the-skyline-problem/) · Sweep line with a multiset of heights.

### Key idea

Make events: a start (x, −h) and an end (x, +h); sort so starts come before ends and taller starts first. Keep a multiset of active heights (with 0). When the maximum changes, emit a key point.

### Steps

1.  Events sorted
2.  Start: insert h; end: erase one h
3.  If max height changed, push (x, max)

### C++17 solution

``` cpp
class Solution {
public:
    vector<vector<int>> getSkyline(vector<vector<int>>& b) {
        vector<pair<int, int>> ev;
        for (auto& x : b) { ev.push_back({x[0], -x[2]}); ev.push_back({x[1], x[2]}); }
        sort(ev.begin(), ev.end());
        multiset<int> h{0}; int prev = 0; vector<vector<int>> r;
        for (auto [x, y] : ev) {
            if (y < 0) h.insert(-y); else h.erase(h.find(y));
            int cur = *h.rbegin();
            if (cur != prev) { r.push_back({x, cur}); prev = cur; }
        }
        return r;
    }
};
```

### Test it passed

``` cpp
vector<vector<int>> a{{2,9,10},{3,7,15},{5,12,12},{15,20,10},{19,24,8}}, b{{0,2,3},{2,5,3}}; Solution S;
assert((S.getSkyline(a) == vector<vector<int>>{{2,10},{3,15},{7,12},{12,0},{15,10},{20,8},{24,0}}) && (S.getSkyline(b) == vector<vector<int>>{{0,3},{5,0}}));
```

### Complexity

O(n log n) time, O(n) space

### Traps

- erase(value) removes every copy; erase one with find
- Two buildings touching at the same height must not create a dip

### Follow-ups

- Divide and conquer merge, like merge sort.

## 09. Minimum Cost to Hire K Workers

L3 [Heap](knowledge-base/dsa.md#heaps-and-priority-queues) · [LeetCode ↗](https://leetcode.com/problems/minimum-cost-to-hire-k-workers/) · Sort by ratio, keep smallest qualities.

### Key idea

In a group everyone is paid at the highest wage/quality ratio in it. Sort by ratio; for each worker as the captain (highest ratio so far), pay ratio × (sum of the k smallest qualities seen). Keep those with a max-heap.

### Steps

1.  Sort by wage/quality
2.  Push quality, sum += q; if size \> k pop the largest
3.  When size == k: best = min(best, sum × ratio)

### C++17 solution

``` cpp
class Solution {
public:
    double mincostToHireWorkers(vector<int>& q, vector<int>& w, int k) {
        int n = q.size(); vector<pair<double, int>> v;
        for (int i = 0; i < n; i++) v.push_back({(double)w[i] / q[i], q[i]});
        sort(v.begin(), v.end());
        priority_queue<int> pq; long long sum = 0; double best = 1e18;
        for (auto [r, qq] : v) {
            pq.push(qq); sum += qq;
            if ((int)pq.size() > k) { sum -= pq.top(); pq.pop(); }
            if ((int)pq.size() == k) best = min(best, sum * r);
        }
        return best;
    }
};
```

### Test it passed

``` cpp
vector<int> q1{10,20,5}, w1{70,50,30}, q2{3,1,10,10,1}, w2{4,8,2,2,7}; Solution S;
assert(fabs(S.mincostToHireWorkers(q1, w1, 2) - 105.0) < 1e-6 && fabs(S.mincostToHireWorkers(q2, w2, 3) - 30.666666667) < 1e-6);
```

### Complexity

O(n log n) time, O(n) space

### Traps

- Integer division for the ratio

### Follow-ups

- Why the captain must be the highest ratio in the group.

## 10. Course Schedule III

L3 [Greedy](knowledge-base/dsa.md#greedy-algorithms) · [LeetCode ↗](https://leetcode.com/problems/course-schedule-iii/) · Exchange argument with a max-heap.

### Key idea

Take courses in order of deadline. Add each one; if the total time passes its deadline, drop the longest course taken so far (it frees the most time and keeps the count).

### Steps

1.  Sort by deadline
2.  Push duration; time += d
3.  If time \> deadline: time −= top; pop

### C++17 solution

``` cpp
class Solution {
public:
    int scheduleCourse(vector<vector<int>>& c) {
        sort(c.begin(), c.end(), [](const vector<int>& a, const vector<int>& b) { return a[1] < b[1]; });
        priority_queue<int> pq; int t = 0;
        for (auto& x : c) { pq.push(x[0]); t += x[0]; if (t > x[1]) { t -= pq.top(); pq.pop(); } }
        return pq.size();
    }
};
```

### Test it passed

``` cpp
vector<vector<int>> a{{100,200},{200,1300},{1000,1250},{2000,3200}}, b{{1,2}}, c{{3,2},{4,3}}; Solution S; assert(S.scheduleCourse(a) == 3 && S.scheduleCourse(b) == 1 && S.scheduleCourse(c) == 0);
```

### Complexity

O(n log n) time, O(n) space

### Traps

- Sorting by duration instead of deadline

### Follow-ups

- Prove the swap: replacing a longer course by a shorter one never hurts later choices.

## 11. Word Search II

L3 [Trie + backtracking](knowledge-base/dsa.md#tries) · [LeetCode ↗](https://leetcode.com/problems/word-search-ii/) · Search all words at once with a trie.

### Key idea

Insert every word into a trie. DFS from each cell, walking the trie as you move; when a node ends a word, record it and clear the marker so it is reported once.

### Steps

1.  Build the trie with a word pointer at terminal nodes
2.  DFS(r, c, node): mark the cell, try 4 neighbours, unmark
3.  Prune: stop when the trie has no child for the letter

### C++17 solution

``` cpp
class Solution {
    struct Node { Node* nx[26] = {}; string* word = nullptr; };
    vector<Node> pool; vector<string> out;
    void dfs(vector<vector<char>>& b, int r, int c, Node* n) {
        char ch = b[r][c]; if (ch == '#' || !n->nx[ch - 'a']) return;
        n = n->nx[ch - 'a'];
        if (n->word) { out.push_back(*n->word); n->word = nullptr; }
        b[r][c] = '#';
        int dr[] = {1, -1, 0, 0}, dc[] = {0, 0, 1, -1};
        for (int k = 0; k < 4; k++) { int nr = r + dr[k], nc = c + dc[k]; if (nr >= 0 && nc >= 0 && nr < (int)b.size() && nc < (int)b[0].size()) dfs(b, nr, nc, n); }
        b[r][c] = ch;
    }
public:
    vector<string> findWords(vector<vector<char>>& b, vector<string>& words) {
        size_t total = 1; for (auto& w : words) total += w.size();
        pool.assign(total, Node()); size_t used = 1; Node* root = &pool[0];
        for (auto& w : words) { Node* n = root; for (char ch : w) { if (!n->nx[ch - 'a']) n->nx[ch - 'a'] = &pool[used++]; n = n->nx[ch - 'a']; } n->word = &w; }
        out.clear();
        for (int r = 0; r < (int)b.size(); r++) for (int c = 0; c < (int)b[0].size(); c++) dfs(b, r, c, root);
        sort(out.begin(), out.end()); return out;
    }
};
```

### Test it passed

``` cpp
vector<vector<char>> b{{'o','a','a','n'},{'e','t','a','e'},{'i','h','k','r'},{'i','f','l','v'}}, c{{'a','b'},{'c','d'}};
vector<string> w{"oath","pea","eat","rain"}, w2{"abcb"}; Solution S;
assert((S.findWords(b, w) == vector<string>{"eat","oath"}) && S.findWords(c, w2).empty());
```

### Complexity

O(cells · 4 · 3^(L−1)) worst case; the trie shares prefixes

### Traps

- Reporting a word twice (clear the marker)
- Reusing a cell in one word (mark it while on the path)

### Follow-ups

- Prune trie nodes whose subtree has no words left.

## 12. Remove Invalid Parentheses

L3 [BFS](knowledge-base/dsa.md#bfs-and-graph-basics) · [LeetCode ↗](https://leetcode.com/problems/remove-invalid-parentheses/) · BFS by number of removals.

### Key idea

Level k of a BFS holds strings with k characters removed. The first level that contains valid strings gives all answers with the minimum removals; stop there.

### Steps

1.  Queue with s, visited set
2.  If any string in the level is valid, collect all valid ones and stop
3.  Otherwise remove each '(' or ')' once to form the next level

### C++17 solution

``` cpp
class Solution {
    bool valid(const string& s) { int b = 0; for (char c : s) { if (c == '(') b++; else if (c == ')' && --b < 0) return false; } return b == 0; }
public:
    vector<string> removeInvalidParentheses(string s) {
        vector<string> level{s}; unordered_set<string> seen{s};
        while (true) {
            vector<string> ok;
            for (auto& t : level) if (valid(t)) ok.push_back(t);
            if (!ok.empty()) { sort(ok.begin(), ok.end()); return ok; }
            vector<string> next;
            for (auto& t : level)
                for (size_t i = 0; i < t.size(); i++)
                    if (t[i] == '(' || t[i] == ')') { string u = t.substr(0, i) + t.substr(i + 1); if (seen.insert(u).second) next.push_back(u); }
            level = next;
        }
    }
};
```

### Test it passed

``` cpp
Solution S; assert((S.removeInvalidParentheses("()())()") == vector<string>{"(())()","()()()"}) && (S.removeInvalidParentheses("(a)())()") == vector<string>{"(a())()","(a)()()"}) && (S.removeInvalidParentheses(")(") == vector<string>{""}));
```

### Complexity

Exponential in the worst case; the visited set prunes duplicates

### Traps

- Continuing past the first valid level (gives non-minimal answers)

### Follow-ups

- DFS with counts of extra '(' and ')' to remove is faster in practice.

## 13. Bus Routes

L3 [BFS](knowledge-base/dsa.md#bfs-and-graph-basics) · [LeetCode ↗](https://leetcode.com/problems/bus-routes/) · BFS over buses, not stops.

### Key idea

Map each stop to the buses that serve it. BFS where one level is one more bus: from the current stops, take every unused bus and add all its stops.

### Steps

1.  If source == target: 0
2.  stop → buses map
3.  Level by level; mark buses and stops used

### C++17 solution

``` cpp
class Solution {
public:
    int numBusesToDestination(vector<vector<int>>& routes, int s, int t) {
        if (s == t) return 0;
        unordered_map<int, vector<int>> at; for (int i = 0; i < (int)routes.size(); i++) for (int x : routes[i]) at[x].push_back(i);
        vector<bool> usedBus(routes.size()); unordered_set<int> seen{s}; queue<int> q; q.push(s);
        for (int buses = 1; !q.empty(); buses++)
            for (int n = q.size(); n--; ) {
                int stop = q.front(); q.pop();
                for (int b : at[stop]) {
                    if (usedBus[b]) continue;
                    usedBus[b] = true;
                    for (int x : routes[b]) { if (x == t) return buses; if (seen.insert(x).second) q.push(x); }
                }
            }
        return -1;
    }
};
```

### Test it passed

``` cpp
vector<vector<int>> a{{1,2,7},{3,6,7}}, b{{7,12},{4,5,15},{6},{15,19},{9,12,13}}; Solution S;
assert(S.numBusesToDestination(a, 1, 6) == 2 && S.numBusesToDestination(b, 15, 12) == -1 && S.numBusesToDestination(a, 3, 3) == 0);
```

### Complexity

O(total stops) time and space

### Traps

- BFS over stops with every pair edge (quadratic in route length)

### Follow-ups

- Return the actual sequence of buses.

## 14. Shortest Path Visiting All Nodes

L3 [Bitmask BFS](knowledge-base/dsa.md#bitmask-dp) · [LeetCode ↗](https://leetcode.com/problems/shortest-path-visiting-all-nodes/) · BFS over (node, visited set).

### Key idea

State = (node, mask of visited nodes). Start from every node at once with its own bit set. BFS; the first state whose mask is full gives the answer.

### Steps

1.  Queue all (i, 1 \<\< i)
2.  seen\[mask\]\[node\]
3.  Expand to neighbours with mask \| 1 \<\< nb

### C++17 solution

``` cpp
class Solution {
public:
    int shortestPathLength(vector<vector<int>>& g) {
        int n = g.size(), full = (1 << n) - 1; vector<vector<bool>> seen(1 << n, vector<bool>(n));
        queue<pair<int, int>> q; for (int i = 0; i < n; i++) { q.push({i, 1 << i}); seen[1 << i][i] = true; }
        for (int d = 0; !q.empty(); d++)
            for (int k = q.size(); k--; ) {
                auto [u, m] = q.front(); q.pop();
                if (m == full) return d;
                for (int v : g[u]) { int nm = m | 1 << v; if (!seen[nm][v]) { seen[nm][v] = true; q.push({v, nm}); } }
            }
        return -1;
    }
};
```

### Test it passed

``` cpp
vector<vector<int>> a{{1,2,3},{0},{0},{0}}, b{{1},{0,2,4},{1,3,4},{2},{1,2}}, c{{}}; Solution S; assert(S.shortestPathLength(a) == 4 && S.shortestPathLength(b) == 4 && S.shortestPathLength(c) == 0);
```

### Complexity

O(2ⁿ · n²) time, O(2ⁿ · n) space

### Traps

- Starting from node 0 only (the best start may be elsewhere)

### Follow-ups

- Relation to the travelling salesman DP (Held–Karp).

## 15. Making A Large Island

L3 [Union-Find](knowledge-base/dsa.md#disjoint-set-union-union-find) · [LeetCode ↗](https://leetcode.com/problems/making-a-large-island/) · Label islands, then try each water cell.

### Key idea

Label each island with an id and record its size. For each 0, add 1 + the sizes of the distinct islands around it. If there is no 0, the answer is the whole grid.

### Steps

1.  DFS/BFS labelling with ids from 2
2.  size\[id\]
3.  For each 0: set of neighbour ids, sum sizes + 1

### C++17 solution

``` cpp
class Solution {
public:
    int largestIsland(vector<vector<int>>& g) {
        int n = g.size(), id = 2, best = 0; vector<int> sz(2, 0);
        int dr[] = {1, -1, 0, 0}, dc[] = {0, 0, 1, -1};
        for (int r = 0; r < n; r++) for (int c = 0; c < n; c++) if (g[r][c] == 1) {
            int cnt = 0; vector<pair<int, int>> st{{r, c}}; g[r][c] = id;
            while (!st.empty()) {
                auto [x, y] = st.back(); st.pop_back(); cnt++;
                for (int k = 0; k < 4; k++) { int a = x + dr[k], b = y + dc[k]; if (a >= 0 && b >= 0 && a < n && b < n && g[a][b] == 1) { g[a][b] = id; st.push_back({a, b}); } }
            }
            sz.push_back(cnt); best = max(best, cnt); id++;
        }
        for (int r = 0; r < n; r++) for (int c = 0; c < n; c++) if (g[r][c] == 0) {
            set<int> ids; for (int k = 0; k < 4; k++) { int a = r + dr[k], b = c + dc[k]; if (a >= 0 && b >= 0 && a < n && b < n && g[a][b] > 1) ids.insert(g[a][b]); }
            int s = 1; for (int x : ids) s += sz[x]; best = max(best, s);
        }
        return best;
    }
};
```

### Test it passed

``` cpp
vector<vector<int>> a{{1,0},{0,1}}, b{{1,1},{1,0}}, c{{1,1},{1,1}}, d{{0,0},{0,0}}; Solution S; assert(S.largestIsland(a) == 3 && S.largestIsland(b) == 4 && S.largestIsland(c) == 4 && S.largestIsland(d) == 1);
```

### Complexity

O(n²) time and space

### Traps

- Counting the same island twice when it touches the cell on two sides (use a set)

### Follow-ups

- Union-Find gives the same result without labels.

## 16. Count of Range Sum

L3 [Divide and conquer](knowledge-base/dsa.md#recursion-and-backtracking) · [LeetCode ↗](https://leetcode.com/problems/count-of-range-sum/) · Merge sort on prefix sums.

### Key idea

Count pairs i \< j of prefix sums with lower ≤ P\[j\] − P\[i\] ≤ upper. In merge sort, both halves are sorted, so for each left element two moving pointers find the valid range in the right half.

### Steps

1.  P\[0\] = 0, P\[i+1\] = P\[i\] + a\[i\] (long long)
2.  sort(lo, hi): recurse, then count with two pointers, then merge
3.  Answer the total count

### C++17 solution

``` cpp
class Solution {
    long long lo_, hi_;
    long long go(vector<long long>& p, int l, int r) {            // [l, r)
        if (r - l <= 1) return 0;
        int m = (l + r) / 2; long long cnt = go(p, l, m) + go(p, m, r);
        int a = m, b = m;
        for (int i = l; i < m; i++) {
            while (a < r && p[a] - p[i] < lo_) a++;
            while (b < r && p[b] - p[i] <= hi_) b++;
            cnt += b - a;
        }
        inplace_merge(p.begin() + l, p.begin() + m, p.begin() + r);
        return cnt;
    }
public:
    int countRangeSum(vector<int>& a, int lower, int upper) {
        lo_ = lower; hi_ = upper; vector<long long> p(a.size() + 1, 0);
        for (size_t i = 0; i < a.size(); i++) p[i + 1] = p[i] + a[i];
        return (int)go(p, 0, p.size());
    }
};
```

### Test it passed

``` cpp
vector<int> a{-2,5,-1}, b{0}, c{2147483647,-2147483648,-1,0}; Solution S; assert(S.countRangeSum(a, -2, 2) == 3 && S.countRangeSum(b, 0, 0) == 1 && S.countRangeSum(c, -1, 0) == 4);
```

### Complexity

O(n log n) time, O(n) space

### Traps

- int overflow in prefix sums (the third test)

### Follow-ups

- A Fenwick tree over compressed prefix sums also works.

## 17. Find K-th Smallest Pair Distance

L3 [Binary search on the answer](knowledge-base/dsa.md#binary-search) · [LeetCode ↗](https://leetcode.com/problems/find-k-th-smallest-pair-distance/) · Count pairs ≤ d with two pointers.

### Key idea

Sort. Binary search the distance d; for a given d, count pairs with difference ≤ d using a sliding left pointer. The smallest d with count ≥ k is the answer.

### Steps

1.  Sort
2.  lo = 0, hi = max − min
3.  count(d): for r, move l while a\[r\] − a\[l\] \> d; add r − l

### C++17 solution

``` cpp
class Solution {
public:
    int smallestDistancePair(vector<int>& a, int k) {
        sort(a.begin(), a.end()); int lo = 0, hi = a.back() - a[0];
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2; long long cnt = 0;
            for (int l = 0, r = 0; r < (int)a.size(); r++) { while (a[r] - a[l] > mid) l++; cnt += r - l; }
            if (cnt >= k) hi = mid; else lo = mid + 1;
        }
        return lo;
    }
};
```

### Test it passed

``` cpp
vector<int> a{1,3,1}, b{1,1,1}, c{1,6,1}, d{62,100,4}; Solution S; assert(S.smallestDistancePair(a, 1) == 0 && S.smallestDistancePair(b, 2) == 0 && S.smallestDistancePair(c, 3) == 5 && S.smallestDistancePair(d, 2) == 58);
```

### Complexity

O(n log n + n log W) time, O(1) extra space

### Traps

- Counting with int (n² pairs can overflow)

### Follow-ups

- K-th smallest element in a sorted matrix uses the same idea.

## 18. Dungeon Game

L3 [Grid DP](knowledge-base/dsa.md#dynamic-programming) · [LeetCode ↗](https://leetcode.com/problems/dungeon-game/) · DP that must run backwards.

### Key idea

need\[i\]\[j\] = minimum health when entering cell (i, j) to survive to the end. From the bottom-right: need = max(1, min(need right, need down) − dungeon\[i\]\[j\]).

### Steps

1.  Pad with INT_MAX borders; need\[n\]\[m−1\] = need\[n−1\]\[m\] = 1
2.  Fill from bottom-right to top-left
3.  Answer need\[0\]\[0\]

### C++17 solution

``` cpp
class Solution {
public:
    int calculateMinimumHP(vector<vector<int>>& d) {
        int n = d.size(), m = d[0].size(); vector<vector<int>> need(n + 1, vector<int>(m + 1, INT_MAX));
        need[n][m - 1] = need[n - 1][m] = 1;
        for (int i = n - 1; i >= 0; i--)
            for (int j = m - 1; j >= 0; j--)
                need[i][j] = max(1, min(need[i + 1][j], need[i][j + 1]) - d[i][j]);
        return need[0][0];
    }
};
```

### Test it passed

``` cpp
vector<vector<int>> a{{-2,-3,3},{-5,-10,1},{10,30,-5}}, b{{0}}, c{{100}}; Solution S; assert(S.calculateMinimumHP(a) == 7 && S.calculateMinimumHP(b) == 1 && S.calculateMinimumHP(c) == 1);
```

### Complexity

O(nm) time and space

### Traps

- Going top-left to bottom-right (needs two quantities, does not work)
- Health must stay at least 1

### Follow-ups

- Why does a forward DP fail? (A path's best end health and minimum need conflict.)

## 19. Cherry Pickup II

L3 [Grid DP](knowledge-base/dsa.md#dynamic-programming) · [LeetCode ↗](https://leetcode.com/problems/cherry-pickup-ii/) · Two walkers at once.

### Key idea

Both robots move down one row each step, so the state is (row, col1, col2). dp = cherries collected from this row down; count a shared cell once; try the 9 move pairs.

### Steps

1.  dp over rows from the bottom
2.  cur\[c1\]\[c2\] = grid\[r\]\[c1\] + (c1 != c2 ? grid\[r\]\[c2\] : 0) + best of 9 next pairs
3.  Answer dp\[0\]\[0\]\[m−1\]

### C++17 solution

``` cpp
class Solution {
public:
    int cherryPickup(vector<vector<int>>& g) {
        int n = g.size(), m = g[0].size(); vector<vector<int>> nxt(m, vector<int>(m, 0)), cur(m, vector<int>(m, 0));
        for (int r = n - 1; r >= 0; r--) {
            for (int a = 0; a < m; a++)
                for (int b = 0; b < m; b++) {
                    int best = 0;
                    if (r + 1 < n)
                        for (int da = -1; da <= 1; da++) for (int db = -1; db <= 1; db++) {
                            int x = a + da, y = b + db;
                            if (x >= 0 && y >= 0 && x < m && y < m) best = max(best, nxt[x][y]);
                        }
                    cur[a][b] = g[r][a] + (a != b ? g[r][b] : 0) + best;
                }
            swap(cur, nxt);
        }
        return nxt[0][m - 1];
    }
};
```

### Test it passed

``` cpp
vector<vector<int>> a{{3,1,1},{2,5,1},{1,5,5},{2,1,1}}, b{{1,0,0,0,0,0,1},{2,0,0,0,0,3,0},{2,0,9,0,0,0,0},{0,3,0,5,4,0,0},{1,0,2,3,0,0,6}};
Solution S; assert(S.cherryPickup(a) == 24 && S.cherryPickup(b) == 28);
```

### Complexity

O(n · m² · 9) time, O(m²) space

### Traps

- Counting a cell twice when both robots stand on it

### Follow-ups

- Cherry Pickup I: one walker goes there and back (model as two walkers moving together).

## 20. Best Time to Buy and Sell Stock III

L3 [Stock DP](knowledge-base/dsa.md#dynamic-programming) · [LeetCode ↗](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iii/) · State machine with two transactions.

### Key idea

Track four states: after first buy, first sell, second buy, second sell. Each day update them in order; the second buy uses the profit from the first sell.

### Steps

1.  b1 = max(b1, −p); s1 = max(s1, b1 + p)
2.  b2 = max(b2, s1 − p); s2 = max(s2, b2 + p)
3.  Answer s2

### C++17 solution

``` cpp
class Solution {
public:
    int maxProfit(vector<int>& p) {
        int b1 = INT_MIN, s1 = 0, b2 = INT_MIN, s2 = 0;
        for (int x : p) { b1 = max(b1, -x); s1 = max(s1, b1 + x); b2 = max(b2, s1 - x); s2 = max(s2, b2 + x); }
        return s2;
    }
};
```

### Test it passed

``` cpp
vector<int> a{3,3,5,0,0,3,1,4}, b{1,2,3,4,5}, c{7,6,4,3,1}; Solution S; assert(S.maxProfit(a) == 6 && S.maxProfit(b) == 4 && S.maxProfit(c) == 0);
```

### Complexity

O(n) time, O(1) space

### Traps

- Updating with yesterday's values is not needed here: same-day buy and sell adds nothing

### Follow-ups

- At most k transactions: Stock IV.
- Prefix best and suffix best arrays give another O(n) solution.

## 21. Best Time to Buy and Sell Stock IV

L3 [Stock DP](knowledge-base/dsa.md#dynamic-programming) · [LeetCode ↗](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iv/) · Generalise the state machine to k.

### Key idea

buy\[j\], sell\[j\] for the j-th transaction, j = 1..k. If k ≥ n/2, the limit does not bind: sum every positive day-to-day rise.

### Steps

1.  If 2k ≥ n: greedy sum of rises
2.  Else for each price, for j = 1..k: buy\[j\] = max(buy\[j\], sell\[j−1\] − p); sell\[j\] = max(sell\[j\], buy\[j\] + p)
3.  Answer sell\[k\]

### C++17 solution

``` cpp
class Solution {
public:
    int maxProfit(int k, vector<int>& p) {
        int n = p.size();
        if (2 * k >= n) { int s = 0; for (int i = 1; i < n; i++) s += max(0, p[i] - p[i - 1]); return s; }
        vector<int> buy(k + 1, INT_MIN), sell(k + 1, 0);
        for (int x : p)
            for (int j = 1; j <= k; j++) { buy[j] = max(buy[j], sell[j - 1] - x); sell[j] = max(sell[j], buy[j] + x); }
        return sell[k];
    }
};
```

### Test it passed

``` cpp
vector<int> a{2,4,1}, b{3,2,6,5,0,3}, c{1,2,4,2,5,7,2,4,9,0}; Solution S; assert(S.maxProfit(2, a) == 2 && S.maxProfit(2, b) == 7 && S.maxProfit(4, c) == 15 && S.maxProfit(2, c) == 13);
```

### Complexity

O(nk) time, O(k) space

### Traps

- Huge k without the greedy shortcut (time and memory)

### Follow-ups

- With a cooldown or a fee: change the transitions.

## 22. Frog Jump

L3 [DP](knowledge-base/dsa.md#dynamic-programming) · [LeetCode ↗](https://leetcode.com/problems/frog-jump/) · DP over (stone, last jump).

### Key idea

For each stone keep the set of jump sizes that can land on it. From a stone reached with jump k, try k − 1, k, k + 1 (positive) to stones that exist.

### Steps

1.  map\<stone, set\<jump\>\>; stones\[0\] gets {0}
2.  For each stone in order, for each k in its set, for d in k−1..k+1 with d \> 0: add d to stone + d if it exists
3.  Answer: last stone's set not empty

### C++17 solution

``` cpp
class Solution {
public:
    bool canCross(vector<int>& stones) {
        unordered_map<int, unordered_set<int>> can; for (int s : stones) can[s];
        can[stones[0]].insert(0);
        for (int s : stones)
            for (int k : can[s])
                for (int d = k - 1; d <= k + 1; d++)
                    if (d > 0 && can.count(s + d)) can[s + d].insert(d);
        return !can[stones.back()].empty();
    }
};
```

### Test it passed

``` cpp
vector<int> a{0,1,3,5,6,8,12,17}, b{0,1,2,3,4,8,9,11}, c{0,2}; Solution S; assert(S.canCross(a) && !S.canCross(b) && !S.canCross(c));
```

### Complexity

O(n²) time and space

### Traps

- Modifying a set while iterating it (only later stones are changed, so it is safe here)
- The first jump must be exactly 1

### Follow-ups

- Return the minimum number of jumps.

## 23. Russian Doll Envelopes

L3 [LIS](knowledge-base/dsa.md#dynamic-programming) · [LeetCode ↗](https://leetcode.com/problems/russian-doll-envelopes/) · 2D LIS with a sorting trick.

### Key idea

Sort by width ascending and, for equal widths, height descending. Then the answer is the longest strictly increasing subsequence of heights (the descending tie-break stops two equal widths from nesting).

### Steps

1.  Sort with the tie-break
2.  Patience LIS: lower_bound into tails
3.  Answer tails.size()

### C++17 solution

``` cpp
class Solution {
public:
    int maxEnvelopes(vector<vector<int>>& e) {
        sort(e.begin(), e.end(), [](const vector<int>& a, const vector<int>& b) { return a[0] != b[0] ? a[0] < b[0] : a[1] > b[1]; });
        vector<int> tails;
        for (auto& x : e) { auto it = lower_bound(tails.begin(), tails.end(), x[1]); if (it == tails.end()) tails.push_back(x[1]); else *it = x[1]; }
        return tails.size();
    }
};
```

### Test it passed

``` cpp
vector<vector<int>> a{{5,4},{6,4},{6,7},{2,3}}, b{{1,1},{1,1},{1,1}}, c{{4,5},{4,6},{6,7},{2,3},{1,1}}; Solution S; assert(S.maxEnvelopes(a) == 3 && S.maxEnvelopes(b) == 1 && S.maxEnvelopes(c) == 4);
```

### Complexity

O(n log n) time, O(n) space

### Traps

- Ascending heights for equal widths (lets equal widths nest)

### Follow-ups

- Boxes in 3D: sort and an O(n²) DP.

## 24. Strange Printer

L3 [Interval DP](knowledge-base/dsa.md#dynamic-programming) · [LeetCode ↗](https://leetcode.com/problems/strange-printer/) · Interval DP with a merge on equal ends.

### Key idea

dp\[i\]\[j\] = turns to print s\[i..j\]. Start with dp\[i+1\]\[j\] + 1 (print s\[i\] alone); for every k in (i, j\] with s\[k\] == s\[i\], print them in one stroke: dp\[i+1\]\[k−1\] + dp\[k\]\[j\].

### Steps

1.  Length 1 costs 1
2.  Fill by increasing length
3.  Answer dp\[0\]\[n−1\]

### C++17 solution

``` cpp
class Solution {
public:
    int strangePrinter(string s) {
        int n = s.size(); vector<vector<int>> dp(n + 1, vector<int>(n + 1, 0));
        for (int i = n - 1; i >= 0; i--)
            for (int j = i; j < n; j++) {
                dp[i][j] = 1 + (i + 1 <= j ? dp[i + 1][j] : 0);
                for (int k = i + 1; k <= j; k++)
                    if (s[k] == s[i]) dp[i][j] = min(dp[i][j], (i + 1 <= k - 1 ? dp[i + 1][k - 1] : 0) + dp[k][j]);
            }
        return dp[0][n - 1];
    }
};
```

### Test it passed

``` text
Solution S; assert(S.strangePrinter("aaabbb") == 2 && S.strangePrinter("aba") == 2 && S.strangePrinter("abcabc") == 5 && S.strangePrinter("a") == 1);
```

### Complexity

O(n³) time, O(n²) space

### Traps

- Off-by-one on empty inner intervals

### Follow-ups

- Removing consecutive duplicates first shrinks n without changing the answer.

## 25. Number of Digit One

L3 [Digit DP](knowledge-base/dsa.md#dynamic-programming) · [LeetCode ↗](https://leetcode.com/problems/number-of-digit-one/) · Count by position.

### Key idea

Count how often 1 appears at each decimal position. For position value p, split n into high = n / (10p), cur = (n / p) % 10, low = n % p: ones = high·p + (cur \> 1 ? p : cur == 1 ? low + 1 : 0).

### Steps

1.  Loop p = 1, 10, 100, … while p ≤ n
2.  Add the formula for each position
3.  Use long long for p

### C++17 solution

``` cpp
class Solution {
public:
    int countDigitOne(int n) {
        long long total = 0;
        for (long long p = 1; p <= n; p *= 10) {
            long long high = n / (p * 10), cur = (n / p) % 10, low = n % p;
            total += high * p + (cur > 1 ? p : cur == 1 ? low + 1 : 0);
        }
        return (int)total;
    }
};
```

### Test it passed

``` text
Solution S; int brute = 0; for (int i = 1; i <= 2024; i++) for (int x = i; x; x /= 10) brute += x % 10 == 1;
assert(S.countDigitOne(13) == 6 && S.countDigitOne(0) == 0 && S.countDigitOne(100) == 21 && S.countDigitOne(2024) == brute);
```

### Complexity

O(log n) time, O(1) space

### Traps

- Overflow of p near INT_MAX (use long long)

### Follow-ups

- Count any digit d (careful with 0 and leading zeros).
