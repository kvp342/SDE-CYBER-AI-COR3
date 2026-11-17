ONLINE ASSESSMENT · SIMULATION PACKS II

# 8 more timed OAs sets 9–16 · 90 minutes each

Eight practice online assessments in the shape most fresher coding rounds use: three problems, one timer, no help. 24 new LeetCode problems, none repeated from the first OA pack or from the 83 worked solutions. Each set has a question page (open it when the timer starts) and a solution page (open it only after you have scored yourself).

## Index

| \#  | Set                                                                                        | Suggested date  | Mix       | Max |     |
|-----|--------------------------------------------------------------------------------------------|-----------------|-----------|-----|-----|
| 9   | [Arrays in place](#set-9-arrays-in-place)Bit tricks, backtracking, cyclic placement                       | Sat 6 Mar 2027  | E · M · H | 600 |     |
| 10  | [Strings and intervals](#set-10-strings-and-intervals)Two pointers, interval merging, stack                     | Sat 1 May 2027  | E · M · H | 600 |     |
| 11  | [Windows and histograms](#set-11-windows-and-histograms)XOR, sliding window, monotonic stack                     | Sat 15 May 2027 | E · M · H | 600 |     |
| 12  | [Grids and BFS](#set-12-grids-and-bfs)Hashing, flood fill from the border, BFS on indices               | Sat 29 May 2027 | E · M · H | 600 |     |
| 13  | [Search and counting DP](#set-13-search-and-counting-dp)Binary search, combination DP, string DP                 | Sat 5 Jun 2027  | M · M · H | 700 |     |
| 14  | [Design and counting](#set-14-design-and-counting)Arithmetic, monotonic stack class, Fenwick tree             | Sat 19 Jun 2027 | E · M · H | 600 |     |
| 15  | [Union-find and merge sort](#set-15-union-find-and-merge-sort)DSU, interval DP on strings, counting with merge sort | Sat 26 Jun 2027 | M · M · H | 700 |     |
| 16  | [Final mixed](#set-16-final-mixed)Backtracking, tree centres, interval DP                             | Sat 10 Jul 2027 | M · M · H | 700 |     |
| ·   | [How to run a set, and the scoring guide](#how-to-run-a-set)                                         |                 |           |     |     |

Dates continue the first pack: set 9 in early March before the exam break, 10–12 in May, 13–16 in the placement sprint. Take each on its date, alternating with the first pack. Move a date if a test or the AWS exam (week of 19 Apr) clashes. Problem statements are on LeetCode; the one-line summaries, sketches and code here are original. Every reference solution was compiled with `g++ -std=c++17 -Wall -fsanitize=address,undefined` and passed its tests.

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

Maximum points per set: set 9: 600, set 10: 600, set 11: 600, set 12: 600, set 13: 700, set 14: 600, set 15: 700, set 16: 700. Because the maximum differs, score yourself as a percentage of the set's maximum:

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

## SET 9. Arrays in place

90 minutes · maximum 600 points · suggested date Sat 6 Mar 2027. Topics are hidden on purpose: working out the pattern is part of the test.

Problem 1[Missing Number ↗](https://leetcode.com/problems/missing-number/)Easy10 min · 100 pts

An array holds n distinct numbers from 0 to n; find the one missing.

https://leetcode.com/problems/missing-number/

Your score: \_\_\_\_\_\_ / 100    Time used: \_\_\_\_\_\_ min    Wrong submissions: \_\_\_\_\_\_

Problem 2[Generate Parentheses ↗](https://leetcode.com/problems/generate-parentheses/)Medium30 min · 200 pts

List every valid string of n pairs of parentheses.

https://leetcode.com/problems/generate-parentheses/

Your score: \_\_\_\_\_\_ / 200    Time used: \_\_\_\_\_\_ min    Wrong submissions: \_\_\_\_\_\_

Problem 3[First Missing Positive ↗](https://leetcode.com/problems/first-missing-positive/)Hard50 min · 300 pts

Find the smallest positive integer not in an unsorted array, in O(n) time and O(1) extra space.

https://leetcode.com/problems/first-missing-positive/

Your score: \_\_\_\_\_\_ / 300    Time used: \_\_\_\_\_\_ min    Wrong submissions: \_\_\_\_\_\_

Total: \_\_\_\_\_\_ / 600 = \_\_\_\_\_\_ %    [Solutions for this set →](#set-9-solutions)

## SET 9. Solutions

Focus: Bit tricks, backtracking, cyclic placement. Read the sketch first, then rewrite the code yourself from memory.

### 1. [Missing Number](https://leetcode.com/problems/missing-number/) Easy [Bit manipulation](knowledge-base/dsa.md#bit-manipulation)

1.  XOR every index 0..n with every value: equal pairs cancel, leaving the missing number. (Or n(n+1)/2 minus the sum.)

**Complexity:** O(n) time, O(1) space   **Edge cases:** Missing 0 or missing n

``` cpp
int missingNumber(vector<int>& a) { int x = a.size(); for (int i = 0; i < (int)a.size(); i++) x ^= i ^ a[i]; return x; }
```

### 2. [Generate Parentheses](https://leetcode.com/problems/generate-parentheses/) Medium [Backtracking](knowledge-base/dsa.md#recursion-and-backtracking)

1.  Build left to right: add '(' while fewer than n are open; add ')' while closes are fewer than opens.

**Complexity:** O(Catalan(n) · n)   **Edge cases:** n = 1

``` cpp
void gen(int n, int open, int close, string& cur, vector<string>& out) {
    if ((int)cur.size() == 2 * n) { out.push_back(cur); return; }
    if (open < n) { cur.push_back('('); gen(n, open + 1, close, cur, out); cur.pop_back(); }
    if (close < open) { cur.push_back(')'); gen(n, open, close + 1, cur, out); cur.pop_back(); }
}
vector<string> generateParenthesis(int n) { vector<string> out; string cur; gen(n, 0, 0, cur, out); return out; }
```

### 3. [First Missing Positive](https://leetcode.com/problems/first-missing-positive/) Hard [Hashing](knowledge-base/dsa.md#hashing-and-frequency-maps)

1.  The answer is in 1..n+1. Put each value v in 1..n at index v−1 by swapping until it is there or a duplicate blocks it.
2.  The first index i with a\[i\] ≠ i+1 gives i+1; if none, n+1.

**Complexity:** O(n) time, O(1) space   **Edge cases:** Duplicates (avoid infinite swaps); All negative

``` cpp
int firstMissingPositive(vector<int>& a) {
    int n = a.size();
    for (int i = 0; i < n; i++) while (a[i] > 0 && a[i] <= n && a[a[i] - 1] != a[i]) swap(a[i], a[a[i] - 1]);
    for (int i = 0; i < n; i++) if (a[i] != i + 1) return i + 1;
    return n + 1;
}
```

## SET 10. Strings and intervals

90 minutes · maximum 600 points · suggested date Sat 1 May 2027. Topics are hidden on purpose: working out the pattern is part of the test.

Problem 1[Valid Palindrome ↗](https://leetcode.com/problems/valid-palindrome/)Easy10 min · 100 pts

Is a string a palindrome when only letters and digits count and case is ignored?

https://leetcode.com/problems/valid-palindrome/

Your score: \_\_\_\_\_\_ / 100    Time used: \_\_\_\_\_\_ min    Wrong submissions: \_\_\_\_\_\_

Problem 2[Insert Interval ↗](https://leetcode.com/problems/insert-interval/)Medium30 min · 200 pts

Insert a new interval into sorted, non-overlapping intervals and merge where needed.

https://leetcode.com/problems/insert-interval/

Your score: \_\_\_\_\_\_ / 200    Time used: \_\_\_\_\_\_ min    Wrong submissions: \_\_\_\_\_\_

Problem 3[Longest Valid Parentheses ↗](https://leetcode.com/problems/longest-valid-parentheses/)Hard50 min · 300 pts

Length of the longest well-formed parentheses substring.

https://leetcode.com/problems/longest-valid-parentheses/

Your score: \_\_\_\_\_\_ / 300    Time used: \_\_\_\_\_\_ min    Wrong submissions: \_\_\_\_\_\_

Total: \_\_\_\_\_\_ / 600 = \_\_\_\_\_\_ %    [Solutions for this set →](#set-10-solutions)

## SET 10. Solutions

Focus: Two pointers, interval merging, stack. Read the sketch first, then rewrite the code yourself from memory.

### 1. [Valid Palindrome](https://leetcode.com/problems/valid-palindrome/) Easy [Two pointers](knowledge-base/dsa.md#two-pointers)

1.  Two pointers from both ends; skip non-alphanumeric characters; compare lowercase.

**Complexity:** O(n) time, O(1) space   **Edge cases:** Empty or only spaces is a palindrome

``` text
bool isPalindrome(string s) {
    int i = 0, j = (int)s.size() - 1;
    while (i < j) {
        if (!isalnum((unsigned char)s[i])) { i++; continue; }
        if (!isalnum((unsigned char)s[j])) { j--; continue; }
        if (tolower((unsigned char)s[i]) != tolower((unsigned char)s[j])) return false;
        i++; j--;
    }
    return true;
}
```

### 2. [Insert Interval](https://leetcode.com/problems/insert-interval/) Medium [Intervals](knowledge-base/dsa.md#interval-problems)

1.  Copy intervals ending before the new one; merge every interval that overlaps it into one; copy the rest.

**Complexity:** O(n) time   **Edge cases:** New interval before all or after all; Touching endpoints merge

``` cpp
vector<vector<int>> insert(vector<vector<int>>& a, vector<int> nw) {
    vector<vector<int>> r; size_t i = 0;
    while (i < a.size() && a[i][1] < nw[0]) r.push_back(a[i++]);
    while (i < a.size() && a[i][0] <= nw[1]) { nw[0] = min(nw[0], a[i][0]); nw[1] = max(nw[1], a[i][1]); i++; }
    r.push_back(nw);
    while (i < a.size()) r.push_back(a[i++]);
    return r;
}
```

### 3. [Longest Valid Parentheses](https://leetcode.com/problems/longest-valid-parentheses/) Hard [Stack](knowledge-base/dsa.md#stacks-and-queues)

1.  Keep a stack of indices with a base: start with −1. Push the index of each '('. On ')', pop; if the stack is empty, push this index as the new base; else the valid length is i − top.

**Complexity:** O(n) time, O(n) space   **Edge cases:** Empty string; Leading ')'

``` cpp
int longestValidParentheses(string s) {
    vector<int> st{-1}; int best = 0;
    for (int i = 0; i < (int)s.size(); i++) {
        if (s[i] == '(') st.push_back(i);
        else { st.pop_back(); if (st.empty()) st.push_back(i); else best = max(best, i - st.back()); }
    }
    return best;
}
```

## SET 11. Windows and histograms

90 minutes · maximum 600 points · suggested date Sat 15 May 2027. Topics are hidden on purpose: working out the pattern is part of the test.

Problem 1[Single Number ↗](https://leetcode.com/problems/single-number/)Easy10 min · 100 pts

Every number appears twice except one; find it with O(1) extra space.

https://leetcode.com/problems/single-number/

Your score: \_\_\_\_\_\_ / 100    Time used: \_\_\_\_\_\_ min    Wrong submissions: \_\_\_\_\_\_

Problem 2[Subarray Product Less Than K ↗](https://leetcode.com/problems/subarray-product-less-than-k/)Medium30 min · 200 pts

Count contiguous subarrays of positive numbers whose product is less than k.

https://leetcode.com/problems/subarray-product-less-than-k/

Your score: \_\_\_\_\_\_ / 200    Time used: \_\_\_\_\_\_ min    Wrong submissions: \_\_\_\_\_\_

Problem 3[Maximal Rectangle ↗](https://leetcode.com/problems/maximal-rectangle/)Hard50 min · 300 pts

Largest rectangle of 1s in a binary matrix.

https://leetcode.com/problems/maximal-rectangle/

Your score: \_\_\_\_\_\_ / 300    Time used: \_\_\_\_\_\_ min    Wrong submissions: \_\_\_\_\_\_

Total: \_\_\_\_\_\_ / 600 = \_\_\_\_\_\_ %    [Solutions for this set →](#set-11-solutions)

## SET 11. Solutions

Focus: XOR, sliding window, monotonic stack. Read the sketch first, then rewrite the code yourself from memory.

### 1. [Single Number](https://leetcode.com/problems/single-number/) Easy [Bit manipulation](knowledge-base/dsa.md#bit-manipulation)

1.  XOR all numbers: pairs cancel to 0.

**Complexity:** O(n) time, O(1) space   **Edge cases:** Single element array

``` cpp
int singleNumber(vector<int>& a) { int x = 0; for (int v : a) x ^= v; return x; }
```

### 2. [Subarray Product Less Than K](https://leetcode.com/problems/subarray-product-less-than-k/) Medium [Sliding window](knowledge-base/dsa.md#sliding-window)

1.  Grow a window to the right, multiplying; while the product is at least k, divide out from the left. Every window ending at r adds r − l + 1 subarrays.

**Complexity:** O(n) time, O(1) space   **Edge cases:** k ≤ 1 means no subarray qualifies

``` cpp
int numSubarrayProductLessThanK(vector<int>& a, int k) {
    if (k <= 1) return 0;
    long long prod = 1; int l = 0, cnt = 0;
    for (int r = 0; r < (int)a.size(); r++) { prod *= a[r]; while (prod >= k) prod /= a[l++]; cnt += r - l + 1; }
    return cnt;
}
```

### 3. [Maximal Rectangle](https://leetcode.com/problems/maximal-rectangle/) Hard [Monotonic stack](knowledge-base/dsa.md#monotonic-stack)

1.  For each row, build column heights of consecutive 1s ending there.
2.  Each row is then 'largest rectangle in a histogram': a stack of increasing heights; pop and measure when a lower bar arrives.

**Complexity:** O(rows · cols) time, O(cols) space   **Edge cases:** Empty matrix; All zeros

``` cpp
int largestRect(const vector<int>& h) {
    vector<int> st; int best = 0, n = h.size();
    for (int i = 0; i <= n; i++) {
        int cur = i == n ? 0 : h[i];
        while (!st.empty() && h[st.back()] >= cur) { int ht = h[st.back()]; st.pop_back(); int w = st.empty() ? i : i - st.back() - 1; best = max(best, ht * w); }
        st.push_back(i);
    }
    return best;
}
int maximalRectangle(vector<vector<char>>& m) {
    if (m.empty()) return 0;
    vector<int> h(m[0].size(), 0); int best = 0;
    for (auto& row : m) { for (size_t j = 0; j < row.size(); j++) h[j] = row[j] == '1' ? h[j] + 1 : 0; best = max(best, largestRect(h)); }
    return best;
}
```

## SET 12. Grids and BFS

90 minutes · maximum 600 points · suggested date Sat 29 May 2027. Topics are hidden on purpose: working out the pattern is part of the test.

Problem 1[Contains Duplicate ↗](https://leetcode.com/problems/contains-duplicate/)Easy10 min · 100 pts

Does any value appear at least twice?

https://leetcode.com/problems/contains-duplicate/

Your score: \_\_\_\_\_\_ / 100    Time used: \_\_\_\_\_\_ min    Wrong submissions: \_\_\_\_\_\_

Problem 2[Surrounded Regions ↗](https://leetcode.com/problems/surrounded-regions/)Medium35 min · 200 pts

Flip every region of 'O' not connected to the border into 'X'.

https://leetcode.com/problems/surrounded-regions/

Your score: \_\_\_\_\_\_ / 200    Time used: \_\_\_\_\_\_ min    Wrong submissions: \_\_\_\_\_\_

Problem 3[Jump Game IV ↗](https://leetcode.com/problems/jump-game-iv/)Hard45 min · 300 pts

From index i you may move to i−1, i+1 or any j with a\[j\] == a\[i\]. Minimum jumps from the first to the last index.

https://leetcode.com/problems/jump-game-iv/

Your score: \_\_\_\_\_\_ / 300    Time used: \_\_\_\_\_\_ min    Wrong submissions: \_\_\_\_\_\_

Total: \_\_\_\_\_\_ / 600 = \_\_\_\_\_\_ %    [Solutions for this set →](#set-12-solutions)

## SET 12. Solutions

Focus: Hashing, flood fill from the border, BFS on indices. Read the sketch first, then rewrite the code yourself from memory.

### 1. [Contains Duplicate](https://leetcode.com/problems/contains-duplicate/) Easy [Hashing](knowledge-base/dsa.md#hashing-and-frequency-maps)

1.  Insert into a hash set; a failed insert means a duplicate.

**Complexity:** O(n) time and space   **Edge cases:** Empty array

``` cpp
bool containsDuplicate(vector<int>& a) { unordered_set<int> s; for (int v : a) if (!s.insert(v).second) return true; return false; }
```

### 2. [Surrounded Regions](https://leetcode.com/problems/surrounded-regions/) Medium [DFS](knowledge-base/dsa.md#dfs-components-and-cycles)

1.  Regions touching the border survive. DFS from every border 'O' and mark it safe.
2.  Then flip remaining 'O' to 'X' and safe marks back to 'O'.

**Complexity:** O(rows · cols)   **Edge cases:** Single row or column; No 'O' at all

``` cpp
void mark(vector<vector<char>>& b, int r, int c) {
    if (r < 0 || c < 0 || r >= (int)b.size() || c >= (int)b[0].size() || b[r][c] != 'O') return;
    b[r][c] = 'S'; mark(b, r + 1, c); mark(b, r - 1, c); mark(b, r, c + 1); mark(b, r, c - 1);
}
void solve(vector<vector<char>>& b) {
    int m = b.size(), n = b[0].size();
    for (int i = 0; i < m; i++) { mark(b, i, 0); mark(b, i, n - 1); }
    for (int j = 0; j < n; j++) { mark(b, 0, j); mark(b, m - 1, j); }
    for (auto& row : b) for (char& ch : row) ch = ch == 'S' ? 'O' : 'X';
}
```

### 3. [Jump Game IV](https://leetcode.com/problems/jump-game-iv/) Hard [BFS](knowledge-base/dsa.md#bfs-and-graph-basics)

1.  BFS over indices. Group indices by value; when you first use a value's group, enqueue all of them and then clear the group so it is never scanned again (this keeps BFS linear).

**Complexity:** O(n) time and space   **Edge cases:** Single element: 0; Long runs of equal values (clear the group)

``` cpp
int minJumps(vector<int>& a) {
    int n = a.size(); if (n == 1) return 0;
    unordered_map<int, vector<int>> g; for (int i = 0; i < n; i++) g[a[i]].push_back(i);
    vector<int> dist(n, -1); queue<int> q; q.push(0); dist[0] = 0;
    while (!q.empty()) {
        int i = q.front(); q.pop();
        if (i == n - 1) return dist[i];
        auto& same = g[a[i]];
        same.push_back(i - 1); same.push_back(i + 1);
        for (int j : same) if (j >= 0 && j < n && dist[j] < 0) { dist[j] = dist[i] + 1; q.push(j); }
        same.clear();
    }
    return -1;
}
```

## SET 13. Search and counting DP

90 minutes · maximum 700 points · suggested date Sat 5 Jun 2027. Topics are hidden on purpose: working out the pattern is part of the test.

Problem 1[Find Peak Element ↗](https://leetcode.com/problems/find-peak-element/)Medium20 min · 200 pts

Return the index of any element greater than its neighbours, in O(log n).

https://leetcode.com/problems/find-peak-element/

Your score: \_\_\_\_\_\_ / 200    Time used: \_\_\_\_\_\_ min    Wrong submissions: \_\_\_\_\_\_

Problem 2[Coin Change II ↗](https://leetcode.com/problems/coin-change-ii/)Medium30 min · 200 pts

Count the combinations of coins that make an amount (order does not matter).

https://leetcode.com/problems/coin-change-ii/

Your score: \_\_\_\_\_\_ / 200    Time used: \_\_\_\_\_\_ min    Wrong submissions: \_\_\_\_\_\_

Problem 3[Distinct Subsequences ↗](https://leetcode.com/problems/distinct-subsequences/)Hard40 min · 300 pts

Count the subsequences of s that equal t.

https://leetcode.com/problems/distinct-subsequences/

Your score: \_\_\_\_\_\_ / 300    Time used: \_\_\_\_\_\_ min    Wrong submissions: \_\_\_\_\_\_

Total: \_\_\_\_\_\_ / 700 = \_\_\_\_\_\_ %    [Solutions for this set →](#set-13-solutions)

## SET 13. Solutions

Focus: Binary search, combination DP, string DP. Read the sketch first, then rewrite the code yourself from memory.

### 1. [Find Peak Element](https://leetcode.com/problems/find-peak-element/) Medium [Binary search](knowledge-base/dsa.md#binary-search)

1.  If a\[mid\] \< a\[mid+1\], a peak lies to the right; otherwise at mid or to the left.

**Complexity:** O(log n) time   **Edge cases:** Array of one element; Strictly increasing array

``` cpp
int findPeakElement(vector<int>& a) { int lo = 0, hi = a.size() - 1; while (lo < hi) { int m = (lo + hi) / 2; if (a[m] < a[m + 1]) lo = m + 1; else hi = m; } return lo; }
```

### 2. [Coin Change II](https://leetcode.com/problems/coin-change-ii/) Medium [DP](knowledge-base/dsa.md#dynamic-programming)

1.  dp\[x\] = ways to make x. Loop coins on the outside and amounts inside, so each combination is counted once: dp\[x\] += dp\[x − coin\].

**Complexity:** O(coins · amount)   **Edge cases:** Amount 0 has one way; Loop order swapped counts permutations instead

``` cpp
int change(int amount, vector<int>& coins) {
    vector<unsigned long long> dp(amount + 1, 0); dp[0] = 1;
    for (int c : coins) for (int x = c; x <= amount; x++) dp[x] += dp[x - c];
    return (int)dp[amount];
}
```

### 3. [Distinct Subsequences](https://leetcode.com/problems/distinct-subsequences/) Hard [DP](knowledge-base/dsa.md#string-dp-lcs-and-edit-distance)

1.  dp\[j\] = ways to form the first j characters of t. For each character of s, go j from right to left: if s\[i\] == t\[j−1\], dp\[j\] += dp\[j−1\].

**Complexity:** O(\|s\| · \|t\|) time, O(\|t\|) space   **Edge cases:** t longer than s gives 0; Iterate j backwards so each s character is used once

``` cpp
int numDistinct(string s, string t) {
    vector<unsigned long long> dp(t.size() + 1, 0); dp[0] = 1;
    for (char ch : s) for (int j = t.size(); j >= 1; j--) if (ch == t[j - 1]) dp[j] += dp[j - 1];
    return (int)dp[t.size()];
}
```

## SET 14. Design and counting

90 minutes · maximum 600 points · suggested date Sat 19 Jun 2027. Topics are hidden on purpose: working out the pattern is part of the test.

Problem 1[Plus One ↗](https://leetcode.com/problems/plus-one/)Easy10 min · 100 pts

Add one to a number stored as an array of digits.

https://leetcode.com/problems/plus-one/

Your score: \_\_\_\_\_\_ / 100    Time used: \_\_\_\_\_\_ min    Wrong submissions: \_\_\_\_\_\_

Problem 2[Online Stock Span ↗](https://leetcode.com/problems/online-stock-span/)Medium30 min · 200 pts

Design a class: for each new price, return how many consecutive days (including today) had a price at most today's.

https://leetcode.com/problems/online-stock-span/

Your score: \_\_\_\_\_\_ / 200    Time used: \_\_\_\_\_\_ min    Wrong submissions: \_\_\_\_\_\_

Problem 3[Count of Smaller Numbers After Self ↗](https://leetcode.com/problems/count-of-smaller-numbers-after-self/)Hard50 min · 300 pts

For each element, count the smaller elements to its right.

https://leetcode.com/problems/count-of-smaller-numbers-after-self/

Your score: \_\_\_\_\_\_ / 300    Time used: \_\_\_\_\_\_ min    Wrong submissions: \_\_\_\_\_\_

Total: \_\_\_\_\_\_ / 600 = \_\_\_\_\_\_ %    [Solutions for this set →](#set-14-solutions)

## SET 14. Solutions

Focus: Arithmetic, monotonic stack class, Fenwick tree. Read the sketch first, then rewrite the code yourself from memory.

### 1. [Plus One](https://leetcode.com/problems/plus-one/) Easy [Two pointers](knowledge-base/dsa.md#two-pointers)

1.  From the last digit: if it is below 9, add one and stop; else set it to 0 and carry. If every digit carried, put a 1 in front.

**Complexity:** O(n)   **Edge cases:** All nines

``` cpp
vector<int> plusOne(vector<int> d) { for (int i = d.size() - 1; i >= 0; i--) { if (d[i] < 9) { d[i]++; return d; } d[i] = 0; } d.insert(d.begin(), 1); return d; }
```

### 2. [Online Stock Span](https://leetcode.com/problems/online-stock-span/) Medium [Monotonic stack](knowledge-base/dsa.md#monotonic-stack)

1.  Keep a stack of (price, span) with decreasing prices. Pop every entry with price ≤ today and add its span to today's.

**Complexity:** Amortised O(1) per call   **Edge cases:** Equal prices are popped too

``` cpp
class StockSpanner {
    vector<pair<int, int>> st;
public:
    int next(int price) { int span = 1; while (!st.empty() && st.back().first <= price) { span += st.back().second; st.pop_back(); } st.push_back({price, span}); return span; }
};
```

### 3. [Count of Smaller Numbers After Self](https://leetcode.com/problems/count-of-smaller-numbers-after-self/) Hard [Binary search](knowledge-base/dsa.md#binary-search)

1.  Compress values to ranks. Walk from the right with a Fenwick (binary indexed) tree: the answer for a\[i\] is the count of ranks below its own; then add its rank.

**Complexity:** O(n log n) time, O(n) space   **Edge cases:** Equal values do not count as smaller; Negative numbers (compress first)

``` cpp
vector<int> countSmaller(vector<int>& a) {
    vector<int> v(a); sort(v.begin(), v.end()); v.erase(unique(v.begin(), v.end()), v.end());
    int m = v.size(); vector<int> bit(m + 1, 0), res(a.size());
    for (int i = (int)a.size() - 1; i >= 0; i--) {
        int r = lower_bound(v.begin(), v.end(), a[i]) - v.begin();   // 0-based rank; count ranks < r
        int c = 0; for (int x = r; x > 0; x -= x & -x) c += bit[x];
        res[i] = c;
        for (int x = r + 1; x <= m; x += x & -x) bit[x]++;
    }
    return res;
}
```

## SET 15. Union-find and merge sort

90 minutes · maximum 700 points · suggested date Sat 26 Jun 2027. Topics are hidden on purpose: working out the pattern is part of the test.

Problem 1[Redundant Connection ↗](https://leetcode.com/problems/redundant-connection/)Medium25 min · 200 pts

A tree plus one extra edge is given; return the edge that, removed, leaves a tree (the last such edge in the input).

https://leetcode.com/problems/redundant-connection/

Your score: \_\_\_\_\_\_ / 200    Time used: \_\_\_\_\_\_ min    Wrong submissions: \_\_\_\_\_\_

Problem 2[Longest Palindromic Subsequence ↗](https://leetcode.com/problems/longest-palindromic-subsequence/)Medium30 min · 200 pts

Length of the longest subsequence that reads the same both ways.

https://leetcode.com/problems/longest-palindromic-subsequence/

Your score: \_\_\_\_\_\_ / 200    Time used: \_\_\_\_\_\_ min    Wrong submissions: \_\_\_\_\_\_

Problem 3[Reverse Pairs ↗](https://leetcode.com/problems/reverse-pairs/)Hard35 min · 300 pts

Count pairs i \< j with a\[i\] \> 2·a\[j\].

https://leetcode.com/problems/reverse-pairs/

Your score: \_\_\_\_\_\_ / 300    Time used: \_\_\_\_\_\_ min    Wrong submissions: \_\_\_\_\_\_

Total: \_\_\_\_\_\_ / 700 = \_\_\_\_\_\_ %    [Solutions for this set →](#set-15-solutions)

## SET 15. Solutions

Focus: DSU, interval DP on strings, counting with merge sort. Read the sketch first, then rewrite the code yourself from memory.

### 1. [Redundant Connection](https://leetcode.com/problems/redundant-connection/) Medium [Union-find](knowledge-base/dsa.md#disjoint-set-union-union-find)

1.  Union-find over the edges in order: the first edge whose ends are already connected closes the cycle.

**Complexity:** O(n α(n))   **Edge cases:** Return the last cycle edge in input order (the first one that fails)

``` cpp
vector<int> findRedundantConnection(vector<vector<int>>& e) {
    vector<int> p(e.size() + 1); iota(p.begin(), p.end(), 0);
    function<int(int)> f = [&](int x) { return p[x] == x ? x : p[x] = f(p[x]); };
    for (auto& ed : e) { int a = f(ed[0]), b = f(ed[1]); if (a == b) return ed; p[a] = b; }
    return {};
}
```

### 2. [Longest Palindromic Subsequence](https://leetcode.com/problems/longest-palindromic-subsequence/) Medium [DP](knowledge-base/dsa.md#string-dp-lcs-and-edit-distance)

1.  dp\[i\]\[j\] for s\[i..j\]: equal ends give dp\[i+1\]\[j−1\] + 2; otherwise max(dp\[i+1\]\[j\], dp\[i\]\[j−1\]). Fill i from the end.

**Complexity:** O(n²) time and space   **Edge cases:** Single character is 1

``` cpp
int longestPalindromeSubseq(string s) {
    int n = s.size(); vector<vector<int>> dp(n, vector<int>(n, 0));
    for (int i = n - 1; i >= 0; i--) { dp[i][i] = 1; for (int j = i + 1; j < n; j++) dp[i][j] = s[i] == s[j] ? dp[i + 1][j - 1] + 2 : max(dp[i + 1][j], dp[i][j - 1]); }
    return dp[0][n - 1];
}
```

### 3. [Reverse Pairs](https://leetcode.com/problems/reverse-pairs/) Hard [Divide and conquer](knowledge-base/dsa.md#time-and-space-complexity)

1.  Merge sort. Before merging two sorted halves, count for each left element how many right elements r satisfy left \> 2·r with one moving pointer; then merge.

**Complexity:** O(n log n)   **Edge cases:** Use 64-bit for 2·a\[j\]; Negative numbers

``` cpp
long long sortCount(vector<int>& a, int lo, int hi) {
    if (hi - lo <= 1) return 0;
    int mid = (lo + hi) / 2; long long c = sortCount(a, lo, mid) + sortCount(a, mid, hi);
    for (int i = lo, j = mid; i < mid; i++) { while (j < hi && (long long)a[i] > 2LL * a[j]) j++; c += j - mid; }
    inplace_merge(a.begin() + lo, a.begin() + mid, a.begin() + hi);
    return c;
}
int reversePairs(vector<int>& a) { return (int)sortCount(a, 0, a.size()); }
```

## SET 16. Final mixed

90 minutes · maximum 700 points · suggested date Sat 10 Jul 2027. Topics are hidden on purpose: working out the pattern is part of the test.

Problem 1[Letter Combinations of a Phone Number ↗](https://leetcode.com/problems/letter-combinations-of-a-phone-number/)Medium20 min · 200 pts

Return all letter strings a phone keypad digit string could spell.

https://leetcode.com/problems/letter-combinations-of-a-phone-number/

Your score: \_\_\_\_\_\_ / 200    Time used: \_\_\_\_\_\_ min    Wrong submissions: \_\_\_\_\_\_

Problem 2[Minimum Height Trees ↗](https://leetcode.com/problems/minimum-height-trees/)Medium30 min · 200 pts

Return every root that gives a tree of minimum height.

https://leetcode.com/problems/minimum-height-trees/

Your score: \_\_\_\_\_\_ / 200    Time used: \_\_\_\_\_\_ min    Wrong submissions: \_\_\_\_\_\_

Problem 3[Minimum Cost to Cut a Stick ↗](https://leetcode.com/problems/minimum-cost-to-cut-a-stick/)Hard40 min · 300 pts

Cuts at given positions on a stick of length n; each cut costs the current piece's length. Minimise the total.

https://leetcode.com/problems/minimum-cost-to-cut-a-stick/

Your score: \_\_\_\_\_\_ / 300    Time used: \_\_\_\_\_\_ min    Wrong submissions: \_\_\_\_\_\_

Total: \_\_\_\_\_\_ / 700 = \_\_\_\_\_\_ %    [Solutions for this set →](#set-16-solutions)

## SET 16. Solutions

Focus: Backtracking, tree centres, interval DP. Read the sketch first, then rewrite the code yourself from memory.

### 1. [Letter Combinations of a Phone Number](https://leetcode.com/problems/letter-combinations-of-a-phone-number/) Medium [Backtracking](knowledge-base/dsa.md#recursion-and-backtracking)

1.  Backtrack over digits, appending each letter of the current digit's key.

**Complexity:** O(4^n · n)   **Edge cases:** Empty input returns an empty list, not \[""\]

``` cpp
vector<string> letterCombinations(string d) {
    if (d.empty()) return {};
    static const string key[] = {"", "", "abc", "def", "ghi", "jkl", "mno", "pqrs", "tuv", "wxyz"};
    vector<string> out; string cur;
    function<void(int)> go = [&](int i) { if (i == (int)d.size()) { out.push_back(cur); return; } for (char ch : key[d[i] - '0']) { cur.push_back(ch); go(i + 1); cur.pop_back(); } };
    go(0); return out;
}
```

### 2. [Minimum Height Trees](https://leetcode.com/problems/minimum-height-trees/) Medium [Topological sort](knowledge-base/dsa.md#topological-sort)

1.  Peel leaves layer by layer (like Kahn's algorithm on degrees). The last one or two nodes left are the centres.

**Complexity:** O(n)   **Edge cases:** n = 1 returns \[0\]

``` cpp
vector<int> findMinHeightTrees(int n, vector<vector<int>>& e) {
    if (n == 1) return {0};
    vector<vector<int>> g(n); vector<int> deg(n, 0);
    for (auto& x : e) { g[x[0]].push_back(x[1]); g[x[1]].push_back(x[0]); deg[x[0]]++; deg[x[1]]++; }
    vector<int> leaves; for (int i = 0; i < n; i++) if (deg[i] == 1) leaves.push_back(i);
    int left = n;
    while (left > 2) {
        left -= leaves.size(); vector<int> nxt;
        for (int u : leaves) for (int v : g[u]) if (--deg[v] == 1) nxt.push_back(v);
        leaves = nxt;
    }
    sort(leaves.begin(), leaves.end()); return leaves;
}
```

### 3. [Minimum Cost to Cut a Stick](https://leetcode.com/problems/minimum-cost-to-cut-a-stick/) Hard [DP](knowledge-base/dsa.md#dynamic-programming)

1.  Sort cuts and add 0 and n as ends. dp\[i\]\[j\] = minimum cost to make every cut strictly between ends i and j = min over k of dp\[i\]\[k\] + dp\[k\]\[j\] + (c\[j\] − c\[i\]).

**Complexity:** O(m³) for m cuts   **Edge cases:** Interval DP like Burst Balloons: choose the first cut in the range

``` cpp
int minCost(int n, vector<int> cuts) {
    cuts.push_back(0); cuts.push_back(n); sort(cuts.begin(), cuts.end());
    int m = cuts.size(); vector<vector<int>> dp(m, vector<int>(m, 0));
    for (int len = 2; len < m; len++) for (int i = 0; i + len < m; i++) {
        int j = i + len; dp[i][j] = INT_MAX;
        for (int k = i + 1; k < j; k++) dp[i][j] = min(dp[i][j], dp[i][k] + dp[k][j] + cuts[j] - cuts[i]);
    }
    return dp[0][m - 1];
}
```
