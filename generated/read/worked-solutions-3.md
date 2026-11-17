WORKED SOLUTIONS · PART III

# 40 more tested solutions

Forty more frequently asked LeetCode problems, none of them in Part I (the 43 solutions in the Knowledge Base), Part II (40 more) or the 48 OA practice problems. Each page gives the pattern, the key idea, the steps, a C++17 solution, the test it passed, the complexity, the traps and the follow-up questions interviewers ask. Levels: L1 1, L2 38, L3 1.

**How to use.** Read the title, try the problem on LeetCode for 25 minutes (L1 15, L3 40), then open the page. If you needed the solution, log it in your revision tracker and redo it in 3, 7 and 21 days. Every solution here was compiled with `g++ -std=c++17 -Wall -fsanitize=address,undefined` and passed the test shown.

## Index (grouped by pattern)

| \#  | Problem                                                             | Pattern          | Level |
|-----|---------------------------------------------------------------------|------------------|-------|
| 1   | [Valid Sudoku](#01-valid-sudoku)                                             | Hashing          | L2    |
| 2   | [K Closest Points to Origin](#02-k-closest-points-to-origin)                              | Heap             | L2    |
| 3   | [4Sum](#03-4sum)                                                    | Two pointers     | L2    |
| 4   | [Fruit Into Baskets](#04-fruit-into-baskets)                                      | Sliding window   | L2    |
| 5   | [Max Consecutive Ones III](#05-max-consecutive-ones-iii)                                | Sliding window   | L2    |
| 6   | [Find Minimum in Rotated Sorted Array](#06-find-minimum-in-rotated-sorted-array)                    | Binary search    | L2    |
| 7   | [Find First and Last Position of Element in Sorted Array](#07-find-first-and-last-position-of-element-in-sorted-array) | Binary search    | L2    |
| 8   | [Capacity To Ship Packages Within D Days](#08-capacity-to-ship-packages-within-d-days)                 | Binary search    | L2    |
| 9   | [Time Based Key-Value Store](#09-time-based-key-value-store)                              | Binary search    | L2    |
| 10  | [Min Stack](#10-min-stack)                                               | Stack            | L2    |
| 11  | [Basic Calculator II](#11-basic-calculator-ii)                                     | Stack            | L2    |
| 12  | [Next Greater Element II](#12-next-greater-element-ii)                                 | Monotonic stack  | L2    |
| 13  | [Remove K Digits](#13-remove-k-digits)                                         | Monotonic stack  | L2    |
| 14  | [Palindrome Linked List](#14-palindrome-linked-list)                                 | Linked list      | L1    |
| 15  | [Add Two Numbers](#15-add-two-numbers)                                        | Linked list      | L2    |
| 16  | [Reorder List](#16-reorder-list)                                           | Linked list      | L2    |
| 17  | [Sort List](#17-sort-list)                                              | Linked list      | L2    |
| 18  | [Path Sum III](#18-path-sum-iii)                                           | Trees            | L2    |
| 19  | [Flatten Binary Tree to Linked List](#19-flatten-binary-tree-to-linked-list)                     | Trees            | L2    |
| 20  | [Lowest Common Ancestor of a Binary Search Tree](#20-lowest-common-ancestor-of-a-binary-search-tree)         | BST              | L2    |
| 21  | [Delete Node in a BST](#21-delete-node-in-a-bst)                                   | BST              | L2    |
| 22  | [Binary Tree Zigzag Level Order Traversal](#22-binary-tree-zigzag-level-order-traversal)               | BFS              | L2    |
| 23  | [All Nodes Distance K in Binary Tree](#23-all-nodes-distance-k-in-binary-tree)                    | BFS              | L2    |
| 24  | [Open the Lock](#24-open-the-lock)                                          | BFS              | L2    |
| 25  | [Shortest Path in Binary Matrix](#25-shortest-path-in-binary-matrix)                         | BFS              | L2    |
| 26  | [Is Graph Bipartite?](#26-is-graph-bipartite)                                    | BFS              | L2    |
| 27  | [Find Eventual Safe States](#27-find-eventual-safe-states)                              | Topological sort | L2    |
| 28  | [Path With Minimum Effort](#28-path-with-minimum-effort)                               | Shortest paths   | L2    |
| 29  | [Min Cost to Connect All Points](#29-min-cost-to-connect-all-points)                         | MST              | L2    |
| 30  | [Number of Operations to Make Network Connected](#30-number-of-operations-to-make-network-connected)         | Union-Find       | L2    |
| 31  | [Combination Sum II](#31-combination-sum-ii)                                     | Backtracking     | L2    |
| 32  | [Palindrome Partitioning](#32-palindrome-partitioning)                                | Backtracking     | L2    |
| 33  | [Sudoku Solver](#33-sudoku-solver)                                          | Backtracking     | L3    |
| 34  | [Partition Labels](#34-partition-labels)                                       | Greedy           | L2    |
| 35  | [Interval List Intersections](#35-interval-list-intersections)                            | Intervals        | L2    |
| 36  | [House Robber II](#36-house-robber-ii)                                        | DP               | L2    |
| 37  | [Target Sum](#37-target-sum)                                             | DP               | L2    |
| 38  | [Maximal Square](#38-maximal-square)                                         | DP               | L2    |
| 39  | [Best Time to Buy and Sell Stock with Cooldown](#39-best-time-to-buy-and-sell-stock-with-cooldown)          | DP               | L2    |
| 40  | [Interleaving String](#40-interleaving-string)                                    | String DP        | L2    |

Problem statements are on LeetCode (each page links to it). Pattern pages link to the online Knowledge Base. Explanations and code are original.

## 01. Valid Sudoku

L2 [Hashing](knowledge-base/dsa.md#hashing-and-frequency-maps) · [LeetCode ↗](https://leetcode.com/problems/valid-sudoku/) · A quick check of 2D indexing and sets.

### Key idea

Each filled digit must be unique in its row, its column and its 3×3 box. Box index = (r / 3) \* 3 + c / 3. Keep a seen-flag per (row, digit), (column, digit) and (box, digit).

### Steps

1.  Skip '.' cells
2.  Compute d = ch - '1' and the box index
3.  If any of the three flags is set, return false; otherwise set all three

### C++17 solution

``` cpp
class Solution {
public:
    bool isValidSudoku(vector<vector<char>>& b) {
        bool row[9][9] = {}, col[9][9] = {}, box[9][9] = {};
        for (int r = 0; r < 9; r++)
            for (int c = 0; c < 9; c++) {
                if (b[r][c] == '.') continue;
                int d = b[r][c] - '1', k = (r / 3) * 3 + c / 3;
                if (row[r][d] || col[c][d] || box[k][d]) return false;
                row[r][d] = col[c][d] = box[k][d] = true;
            }
        return true;
    }
};
```

### Test it passed

``` cpp
vector<string> s{"53..7....","6..195...",".98....6.","8...6...3","4..8.3..1","7...2...6",".6....28.","...419..5","....8..79"};
vector<vector<char>> b; for (auto& x : s) b.push_back(vector<char>(x.begin(), x.end()));
assert(Solution().isValidSudoku(b)); b[0][0] = '8'; assert(!Solution().isValidSudoku(b));
```

### Complexity

O(81) = O(1) time and space

### Traps

- Wrong box formula (r / 3 + c / 3 collides)
- Checking that the board is solvable: the problem only asks about filled cells

### Follow-ups

- Solve the board (see Sudoku Solver).
- Use one 9-bit mask per row, column and box instead of bool arrays.

## 02. K Closest Points to Origin

L2 [Heap](knowledge-base/dsa.md#heaps-and-priority-queues) · [LeetCode ↗](https://leetcode.com/problems/k-closest-points-to-origin/) · Top-k with a heap.

### Key idea

Keep a max-heap of size k keyed by squared distance. When it grows past k, pop the farthest. What remains are the k closest.

### Steps

1.  Use x\*x + y\*y (no square root needed)
2.  Push each point; pop when size \> k
3.  Empty the heap into the answer

### C++17 solution

``` cpp
class Solution {
public:
    vector<vector<int>> kClosest(vector<vector<int>>& pts, int k) {
        priority_queue<pair<long long, int>> pq;           // (distance², index), largest on top
        for (int i = 0; i < (int)pts.size(); i++) {
            long long d = 1LL * pts[i][0] * pts[i][0] + 1LL * pts[i][1] * pts[i][1];
            pq.push({d, i});
            if ((int)pq.size() > k) pq.pop();
        }
        vector<vector<int>> r;
        while (!pq.empty()) { r.push_back(pts[pq.top().second]); pq.pop(); }
        return r;
    }
};
```

### Test it passed

``` cpp
vector<vector<int>> p{{3,3},{5,-1},{-2,4}}; auto r = Solution().kClosest(p, 2); sort(r.begin(), r.end());
assert((r == vector<vector<int>>{{-2,4},{3,3}}));
```

### Complexity

O(n log k) time, O(k) space

### Traps

- Using a min-heap of all n points (O(n log n), fine but not what they want)
- int overflow in x\*x + y\*y for large coordinates

### Follow-ups

- O(n) average with quickselect (nth_element).
- Points arrive as a stream: the size-k heap still works.

## 03. 4Sum

L2 [Two pointers](knowledge-base/dsa.md#two-pointers) · [LeetCode ↗](https://leetcode.com/problems/4sum/) · Extends 3Sum; tests duplicate handling.

### Key idea

Sort. Fix two indices i \< j with duplicate skipping, then run two pointers on the rest for target − a\[i\] − a\[j\]. Use long long sums: values reach 1e9.

### Steps

1.  Sort
2.  Loop i, skip equal neighbours; loop j \> i, skip equal neighbours
3.  Two pointers l, r; on a match record it and skip duplicates on both sides

### C++17 solution

``` cpp
class Solution {
public:
    vector<vector<int>> fourSum(vector<int>& a, int target) {
        sort(a.begin(), a.end()); int n = a.size(); vector<vector<int>> r;
        for (int i = 0; i < n; i++) {
            if (i && a[i] == a[i - 1]) continue;
            for (int j = i + 1; j < n; j++) {
                if (j > i + 1 && a[j] == a[j - 1]) continue;
                int l = j + 1, h = n - 1;
                while (l < h) {
                    long long s = (long long)a[i] + a[j] + a[l] + a[h];
                    if (s < target) l++;
                    else if (s > target) h--;
                    else {
                        r.push_back({a[i], a[j], a[l], a[h]});
                        while (l < h && a[l] == a[l + 1]) l++;
                        while (l < h && a[h] == a[h - 1]) h--;
                        l++; h--;
                    }
                }
            }
        }
        return r;
    }
};
```

### Test it passed

``` cpp
vector<int> a{1,0,-1,0,-2,2}; auto r = Solution().fourSum(a, 0);
assert((r == vector<vector<int>>{{-2,-1,1,2},{-2,0,0,2},{-1,0,0,1}}));
vector<int> b{2,2,2,2,2}; assert(Solution().fourSum(b, 8).size() == 1);
vector<int> c{1000000000,1000000000,1000000000,1000000000}; assert(Solution().fourSum(c, -294967296).empty());
```

### Complexity

O(n³) time, O(1) extra space

### Traps

- int overflow of the four-number sum
- Skipping duplicates of j with j \> 0 instead of j \> i + 1

### Follow-ups

- Generalise to kSum with recursion down to the 2-pointer base case.

## 04. Fruit Into Baskets

L2 [Sliding window](knowledge-base/dsa.md#sliding-window) · [LeetCode ↗](https://leetcode.com/problems/fruit-into-baskets/) · Longest window with at most 2 distinct values.

### Key idea

Grow the right end; keep counts in a map. While the map has more than 2 keys, shrink from the left. The answer is the largest window seen.

### Steps

1.  cnt\[f\[r\]\]++
2.  While cnt.size() \> 2: decrement cnt\[f\[l\]\], erase at 0, l++
3.  best = max(best, r - l + 1)

### C++17 solution

``` cpp
class Solution {
public:
    int totalFruit(vector<int>& f) {
        unordered_map<int, int> cnt; int l = 0, best = 0;
        for (int r = 0; r < (int)f.size(); r++) {
            cnt[f[r]]++;
            while (cnt.size() > 2) { if (--cnt[f[l]] == 0) cnt.erase(f[l]); l++; }
            best = max(best, r - l + 1);
        }
        return best;
    }
};
```

### Test it passed

``` cpp
vector<int> a{1,2,1}, b{0,1,2,2}, c{1,2,3,2,2}, d{3,3,3,1,2,1,1,2,3,3,4};
assert(Solution().totalFruit(a) == 3 && Solution().totalFruit(b) == 3 && Solution().totalFruit(c) == 4 && Solution().totalFruit(d) == 5);
```

### Complexity

O(n) time, O(1) space (map holds at most 3 keys)

### Traps

- Forgetting to erase keys at count 0, so size() never drops

### Follow-ups

- At most k distinct values: same code with k instead of 2.

## 05. Max Consecutive Ones III

L2 [Sliding window](knowledge-base/dsa.md#sliding-window) · [LeetCode ↗](https://leetcode.com/problems/max-consecutive-ones-iii/) · Longest window with at most k zeros.

### Key idea

A window is valid if it holds at most k zeros (flip them). Expand right; when zeros exceed k, move left past a zero.

### Steps

1.  zeros += (a\[r\] == 0)
2.  While zeros \> k: zeros -= (a\[l\] == 0), l++
3.  best = max(best, r - l + 1)

### C++17 solution

``` cpp
class Solution {
public:
    int longestOnes(vector<int>& a, int k) {
        int l = 0, zeros = 0, best = 0;
        for (int r = 0; r < (int)a.size(); r++) {
            zeros += a[r] == 0;
            while (zeros > k) zeros -= a[l++] == 0;
            best = max(best, r - l + 1);
        }
        return best;
    }
};
```

### Test it passed

``` cpp
vector<int> a{1,1,1,0,0,0,1,1,1,1,0}, b{0,0,1,1,0,0,1,1,1,0,1,1,0,0,0,1,1,1,1};
assert(Solution().longestOnes(a, 2) == 6 && Solution().longestOnes(b, 3) == 10);
```

### Complexity

O(n) time, O(1) space

### Traps

- Trying to actually flip values in the array

### Follow-ups

- Longest Repeating Character Replacement uses the same idea with 'window − max frequency ≤ k'.

## 06. Find Minimum in Rotated Sorted Array

L2 [Binary search](knowledge-base/dsa.md#binary-search) · [LeetCode ↗](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/) · Binary search on a property, not a value.

### Key idea

Compare the middle with the right end. If a\[m\] \> a\[r\], the minimum is to the right of m; otherwise it is at m or to its left.

### Steps

1.  l = 0, r = n - 1; while l \< r
2.  m = l + (r - l) / 2
3.  a\[m\] \> a\[r\] ? l = m + 1 : r = m
4.  Return a\[l\]

### C++17 solution

``` cpp
class Solution {
public:
    int findMin(vector<int>& a) {
        int l = 0, r = a.size() - 1;
        while (l < r) {
            int m = l + (r - l) / 2;
            if (a[m] > a[r]) l = m + 1; else r = m;
        }
        return a[l];
    }
};
```

### Test it passed

``` cpp
vector<int> a{3,4,5,1,2}, b{4,5,6,7,0,1,2}, c{11,13,15,17}, d{2,1};
assert(Solution().findMin(a) == 1 && Solution().findMin(b) == 0 && Solution().findMin(c) == 11 && Solution().findMin(d) == 1);
```

### Complexity

O(log n) time, O(1) space

### Traps

- Comparing with a\[l\] instead of a\[r\] (fails when the array is not rotated)
- Using r = m - 1, which can skip the minimum

### Follow-ups

- With duplicates (II): when a\[m\] == a\[r\], do r-- (worst case O(n)).

## 07. Find First and Last Position of Element in Sorted Array

L2 [Binary search](knowledge-base/dsa.md#binary-search) · [LeetCode ↗](https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/) · lower_bound and upper_bound.

### Key idea

The first position is the first index with a\[i\] ≥ t (lower bound). The last is one before the first index with a\[i\] \> t (upper bound). If the lower bound is not t, return \[-1, -1\].

### Steps

1.  lo = lower_bound(t)
2.  If lo == n or a\[lo\] != t: return {-1,-1}
3.  hi = upper_bound(t) - 1

### C++17 solution

``` cpp
class Solution {
    int bound(vector<int>& a, int t, bool upper) {          // first i with a[i] >= t (or > t if upper)
        int l = 0, r = a.size();
        while (l < r) {
            int m = l + (r - l) / 2;
            if (a[m] < t || (upper && a[m] == t)) l = m + 1; else r = m;
        }
        return l;
    }
public:
    vector<int> searchRange(vector<int>& a, int t) {
        int lo = bound(a, t, false);
        if (lo == (int)a.size() || a[lo] != t) return {-1, -1};
        return {lo, bound(a, t, true) - 1};
    }
};
```

### Test it passed

``` cpp
vector<int> a{5,7,7,8,8,10}, e{};
assert((Solution().searchRange(a, 8) == vector<int>{3,4}) && (Solution().searchRange(a, 6) == vector<int>{-1,-1}) && (Solution().searchRange(e, 0) == vector<int>{-1,-1}));
```

### Complexity

O(log n) time, O(1) space

### Traps

- Finding one match then scanning outwards (O(n) on all-equal arrays)

### Follow-ups

- Count occurrences of t: upper − lower.
- In C++ you can use std::lower_bound / std::upper_bound directly.

## 08. Capacity To Ship Packages Within D Days

L2 [Binary search](knowledge-base/dsa.md#binary-search) · [LeetCode ↗](https://leetcode.com/problems/capacity-to-ship-packages-within-d-days/) · Binary search on the answer.

### Key idea

If capacity c works, every larger c works. So binary search c between max(w) and sum(w); check feasibility greedily by filling each day until the next package does not fit.

### Steps

1.  lo = max weight, hi = total weight
2.  days(c): count days by greedy filling
3.  If days(c) ≤ D: hi = c else lo = c + 1

### C++17 solution

``` cpp
class Solution {
public:
    int shipWithinDays(vector<int>& w, int D) {
        int lo = *max_element(w.begin(), w.end()), hi = accumulate(w.begin(), w.end(), 0);
        while (lo < hi) {
            int c = lo + (hi - lo) / 2, days = 1, load = 0;
            for (int x : w) { if (load + x > c) { days++; load = 0; } load += x; }
            if (days <= D) hi = c; else lo = c + 1;
        }
        return lo;
    }
};
```

### Test it passed

``` cpp
vector<int> a{1,2,3,4,5,6,7,8,9,10}, b{3,2,2,4,1,4}, c{1,2,3,1,1};
assert(Solution().shipWithinDays(a, 5) == 15 && Solution().shipWithinDays(b, 3) == 6 && Solution().shipWithinDays(c, 4) == 3);
```

### Complexity

O(n log(sum)) time, O(1) space

### Traps

- Starting lo at 1 (a package heavier than c can never ship)

### Follow-ups

- Same shape: Koko Eating Bananas, Split Array Largest Sum, Minimum Days to Make Bouquets.

## 09. Time Based Key-Value Store

L2 [Binary search](knowledge-base/dsa.md#binary-search) · [LeetCode ↗](https://leetcode.com/problems/time-based-key-value-store/) · Design question with binary search inside.

### Key idea

Timestamps for each key arrive in increasing order, so append (time, value) to a vector per key. get(key, t) is the last entry with time ≤ t: upper_bound on t, then step back one.

### Steps

1.  set: m\[key\].push_back({t, v})
2.  get: it = upper_bound by time; if it is begin, return ""
3.  Return prev(it)-\>second

### C++17 solution

``` cpp
class TimeMap {
    unordered_map<string, vector<pair<int, string>>> m;
public:
    void set(string k, string v, int t) { m[k].push_back({t, v}); }
    string get(string k, int t) {
        auto f = m.find(k); if (f == m.end()) return "";
        auto& v = f->second;
        auto it = upper_bound(v.begin(), v.end(), t, [](int x, const pair<int, string>& p) { return x < p.first; });
        return it == v.begin() ? "" : prev(it)->second;
    }
};
```

### Test it passed

``` text
TimeMap tm; tm.set("foo", "bar", 1); assert(tm.get("foo", 1) == "bar" && tm.get("foo", 3) == "bar");
tm.set("foo", "bar2", 4); assert(tm.get("foo", 4) == "bar2" && tm.get("foo", 5) == "bar2" && tm.get("foo", 0) == "" && tm.get("x", 1) == "");
```

### Complexity

set O(1), get O(log n)

### Traps

- Using m\[k\] in get (inserts empty keys)
- lower_bound returns the first time ≥ t, not the last ≤ t

### Follow-ups

- What if timestamps are not increasing? Use map\<int,string\> per key and upper_bound.

## 10. Min Stack

L2 [Stack](knowledge-base/dsa.md#stacks-and-queues) · [LeetCode ↗](https://leetcode.com/problems/min-stack/) · Design: O(1) getMin.

### Key idea

Store, with every pushed value, the minimum of the stack at that point. Then top, pop and getMin are all O(1).

### Steps

1.  push(x): s.push({x, min(x, current min)})
2.  pop: s.pop()
3.  getMin: s.top().second

### C++17 solution

``` cpp
class MinStack {
    stack<pair<int, int>> s;                      // (value, min so far)
public:
    void push(int x) { s.push({x, s.empty() ? x : min(x, s.top().second)}); }
    void pop() { s.pop(); }
    int top() { return s.top().first; }
    int getMin() { return s.top().second; }
};
```

### Test it passed

``` text
MinStack m; m.push(-2); m.push(0); m.push(-3); assert(m.getMin() == -3); m.pop(); assert(m.top() == 0 && m.getMin() == -2);
```

### Complexity

O(1) per operation, O(n) space

### Traps

- Keeping one global min variable (wrong after popping the min)

### Follow-ups

- Use O(1) extra space by storing differences from the min (watch overflow).
- Max stack with popMax (needs a balanced tree or lazy deletion).

## 11. Basic Calculator II

L2 [Stack](knowledge-base/dsa.md#stacks-and-queues) · [LeetCode ↗](https://leetcode.com/problems/basic-calculator-ii/) · Expression parsing without parentheses.

### Key idea

Read numbers left to right, remembering the operator before each. For + and − push ±num; for \* and / apply it to the top of the stack at once (higher precedence). The answer is the sum of the stack.

### Steps

1.  Build num digit by digit
2.  At an operator or the end: apply the previous operator, then remember this one and reset num
3.  Sum the stack

### C++17 solution

``` cpp
class Solution {
public:
    int calculate(string s) {
        vector<long long> st; long long num = 0; char op = '+';
        for (size_t i = 0; i <= s.size(); i++) {
            char c = i < s.size() ? s[i] : '+';
            if (isdigit(c)) { num = num * 10 + (c - '0'); continue; }
            if (c == ' ') continue;
            if (op == '+') st.push_back(num);
            else if (op == '-') st.push_back(-num);
            else if (op == '*') st.back() *= num;
            else st.back() /= num;                // C++ division truncates toward zero, as required
            op = c; num = 0;
        }
        return accumulate(st.begin(), st.end(), 0LL);
    }
};
```

### Test it passed

``` text
assert(Solution().calculate("3+2*2") == 7 && Solution().calculate(" 3/2 ") == 1 && Solution().calculate(" 3+5 / 2 ") == 5 && Solution().calculate("14-3/2") == 13);
```

### Complexity

O(n) time, O(n) space (O(1) possible)

### Traps

- Treating spaces as operators
- Forgetting the last number (the sentinel at the end handles it)

### Follow-ups

- Add parentheses (Basic Calculator I/III): recurse or push the state on '('.
- Do it in O(1) space by keeping only the last term.

## 12. Next Greater Element II

L2 [Monotonic stack](knowledge-base/dsa.md#monotonic-stack) · [LeetCode ↗](https://leetcode.com/problems/next-greater-element-ii/) · Circular array trick.

### Key idea

Walk the array twice (i from 0 to 2n − 1, index i % n) with a stack of indices whose answer is unknown. While the current value beats the value on top, that index's answer is the current value.

### Steps

1.  ans filled with -1
2.  For i in 0..2n-1: x = a\[i % n\]; pop while a\[top\] \< x, set ans\[top\] = x
3.  Push i only in the first pass

### C++17 solution

``` cpp
class Solution {
public:
    vector<int> nextGreaterElements(vector<int>& a) {
        int n = a.size(); vector<int> ans(n, -1); stack<int> st;
        for (int i = 0; i < 2 * n; i++) {
            int x = a[i % n];
            while (!st.empty() && a[st.top()] < x) { ans[st.top()] = x; st.pop(); }
            if (i < n) st.push(i);
        }
        return ans;
    }
};
```

### Test it passed

``` cpp
vector<int> a{1,2,1}, b{1,2,3,4,3};
assert((Solution().nextGreaterElements(a) == vector<int>{2,-1,2}) && (Solution().nextGreaterElements(b) == vector<int>{2,3,4,-1,4}));
```

### Complexity

O(n) time, O(n) space

### Traps

- Using ≤ in the pop condition (equal values are not greater)

### Follow-ups

- Daily Temperatures is the same idea returning distances.

## 13. Remove K Digits

L2 [Monotonic stack](knowledge-base/dsa.md#monotonic-stack) · [LeetCode ↗](https://leetcode.com/problems/remove-k-digits/) · Greedy with an increasing stack.

### Key idea

To make the number smallest, a digit should be removed when the next digit is smaller. Keep an increasing stack: pop while k \> 0 and the top is bigger than the current digit. Remove leftover k from the end, strip leading zeros.

### Steps

1.  For each digit: pop while k and top \> d (k--); push d
2.  Pop k more from the end
3.  Strip leading zeros; empty means "0"

### C++17 solution

``` cpp
class Solution {
public:
    string removeKdigits(string num, int k) {
        string st;
        for (char d : num) {
            while (k && !st.empty() && st.back() > d) { st.pop_back(); k--; }
            st.push_back(d);
        }
        st.resize(st.size() - min<size_t>(k, st.size()));
        size_t i = 0; while (i < st.size() && st[i] == '0') i++;
        st = st.substr(i);
        return st.empty() ? "0" : st;
    }
};
```

### Test it passed

``` text
assert(Solution().removeKdigits("1432219", 3) == "1219" && Solution().removeKdigits("10200", 1) == "200" && Solution().removeKdigits("10", 2) == "0" && Solution().removeKdigits("112", 1) == "11");
```

### Complexity

O(n) time, O(n) space

### Traps

- Forgetting the leftover k for an increasing string
- Returning an empty string instead of "0"

### Follow-ups

- Largest number by removing k digits: reverse the comparison.

## 14. Palindrome Linked List

L1 [Linked list](knowledge-base/dsa.md#linked-lists) · [LeetCode ↗](https://leetcode.com/problems/palindrome-linked-list/) · Middle + reverse.

### Key idea

Find the middle, reverse the second half, then compare the first half with the reversed half node by node.

### Steps

1.  Slow/fast to the middle
2.  Reverse from slow
3.  Compare until the reversed half ends

### C++17 solution

``` cpp
class Solution {
public:
    bool isPalindrome(ListNode* h) {
        ListNode *s = h, *f = h;
        while (f && f->next) { s = s->next; f = f->next->next; }
        ListNode* prev = nullptr;
        while (s) { ListNode* n = s->next; s->next = prev; prev = s; s = n; }
        for (ListNode* a = h; prev; a = a->next, prev = prev->next) if (a->val != prev->val) return false;
        return true;
    }
};
```

### Test it passed

``` text
assert(Solution().isPalindrome(mk({1,2,2,1})) && !Solution().isPalindrome(mk({1,2})) && Solution().isPalindrome(mk({1,2,3,2,1})) && Solution().isPalindrome(mk({1})));
```

### Complexity

O(n) time, O(1) space

### Traps

- The list is left modified: mention restoring it if the interviewer cares

### Follow-ups

- Restore the list after checking (reverse the second half again).

## 15. Add Two Numbers

L2 [Linked list](knowledge-base/dsa.md#linked-lists) · [LeetCode ↗](https://leetcode.com/problems/add-two-numbers/) · Digit-by-digit addition with a carry.

### Key idea

Digits are stored in reverse, so add node by node from the head with a carry, appending to a dummy list. Continue while either list or the carry remains.

### Steps

1.  Dummy head, tail pointer, carry = 0
2.  sum = carry + (l1 ? l1-\>val : 0) + (l2 ? l2-\>val : 0)
3.  Append sum % 10; carry = sum / 10

### C++17 solution

``` cpp
class Solution {
public:
    ListNode* addTwoNumbers(ListNode* a, ListNode* b) {
        ListNode d(0); ListNode* t = &d; int carry = 0;
        while (a || b || carry) {
            int s = carry + (a ? a->val : 0) + (b ? b->val : 0);
            t->next = new ListNode(s % 10); t = t->next; carry = s / 10;
            if (a) a = a->next;
            if (b) b = b->next;
        }
        return d.next;
    }
};
```

### Test it passed

``` cpp
assert((tov(Solution().addTwoNumbers(mk({2,4,3}), mk({5,6,4}))) == vector<int>{7,0,8}));
assert((tov(Solution().addTwoNumbers(mk({9,9,9,9}), mk({9,9}))) == vector<int>{8,9,0,0,1}));
```

### Complexity

O(max(m, n)) time, O(1) extra space besides the output

### Traps

- Dropping the final carry

### Follow-ups

- Digits in forward order (II): use two stacks or reverse both lists first.

## 16. Reorder List

L2 [Linked list](knowledge-base/dsa.md#linked-lists) · [LeetCode ↗](https://leetcode.com/problems/reorder-list/) · Combines three basic list moves.

### Key idea

L0 → Ln → L1 → Ln−1 …: find the middle (slow/fast), reverse the second half, then merge the two halves alternately.

### Steps

1.  Slow/fast to the middle; cut after slow
2.  Reverse the second half
3.  Weave: a-\>next = b, b-\>next = old a-\>next

### C++17 solution

``` cpp
class Solution {
public:
    void reorderList(ListNode* h) {
        if (!h || !h->next) return;
        ListNode *s = h, *f = h;
        while (f->next && f->next->next) { s = s->next; f = f->next->next; }
        ListNode *prev = nullptr, *cur = s->next; s->next = nullptr;
        while (cur) { ListNode* n = cur->next; cur->next = prev; prev = cur; cur = n; }
        for (ListNode *a = h, *b = prev; b; ) {
            ListNode *an = a->next, *bn = b->next;
            a->next = b; b->next = an; a = an; b = bn;
        }
    }
};
```

### Test it passed

``` cpp
ListNode* a = mk({1,2,3,4}); Solution().reorderList(a); assert((tov(a) == vector<int>{1,4,2,3}));
ListNode* b = mk({1,2,3,4,5}); Solution().reorderList(b); assert((tov(b) == vector<int>{1,5,2,4,3}));
```

### Complexity

O(n) time, O(1) space

### Traps

- Not cutting the first half (creates a cycle)

### Follow-ups

- Could you do it with a deque? (Yes, O(n) extra space.)

## 17. Sort List

L2 [Linked list](knowledge-base/dsa.md#linked-lists) · [LeetCode ↗](https://leetcode.com/problems/sort-list/) · Merge sort on a list.

### Key idea

Merge sort fits lists: split at the middle with slow/fast pointers, sort each half, merge two sorted lists. No random access needed.

### Steps

1.  Base case: 0 or 1 node
2.  Split with slow/fast (fast starts at head-\>next so two nodes split)
3.  Merge the sorted halves with a dummy head

### C++17 solution

``` cpp
class Solution {
    ListNode* merge(ListNode* a, ListNode* b) {
        ListNode d(0); ListNode* t = &d;
        while (a && b) { if (a->val <= b->val) { t->next = a; a = a->next; } else { t->next = b; b = b->next; } t = t->next; }
        t->next = a ? a : b; return d.next;
    }
public:
    ListNode* sortList(ListNode* h) {
        if (!h || !h->next) return h;
        ListNode *s = h, *f = h->next;
        while (f && f->next) { s = s->next; f = f->next->next; }
        ListNode* r = s->next; s->next = nullptr;
        return merge(sortList(h), sortList(r));
    }
};
```

### Test it passed

``` cpp
assert((tov(Solution().sortList(mk({4,2,1,3}))) == vector<int>{1,2,3,4}) && (tov(Solution().sortList(mk({-1,5,3,4,0}))) == vector<int>{-1,0,3,4,5}) && tov(Solution().sortList(nullptr)).empty());
```

### Complexity

O(n log n) time, O(log n) stack space

### Traps

- Starting fast at head for two nodes: the split never shrinks (infinite recursion)

### Follow-ups

- O(1) space: bottom-up merge sort with sizes 1, 2, 4, …

## 18. Path Sum III

L2 [Trees](knowledge-base/dsa.md#binary-trees) · [LeetCode ↗](https://leetcode.com/problems/path-sum-iii/) · Prefix sums on a root-to-node path.

### Key idea

Count downward paths summing to t. Along the current root-to-node path, keep counts of prefix sums. At a node with running sum s, paths ending here = count\[s − t\]. Add s before going down, remove it when coming back.

### Steps

1.  cnt\[0\] = 1
2.  dfs(node, s): s += val; ans += cnt\[s - t\]; cnt\[s\]++; recurse; cnt\[s\]--
3.  Use long long sums

### C++17 solution

``` cpp
class Solution {
    unordered_map<long long, int> cnt; int ans = 0, t = 0;
    void dfs(TreeNode* n, long long s) {
        if (!n) return;
        s += n->val;
        auto it = cnt.find(s - t); if (it != cnt.end()) ans += it->second;
        cnt[s]++; dfs(n->left, s); dfs(n->right, s); cnt[s]--;
    }
public:
    int pathSum(TreeNode* root, int target) { t = target; cnt[0] = 1; dfs(root, 0); return ans; }
};
```

### Test it passed

``` text
assert(Solution().pathSum(tree({"10","5","-3","3","2","null","11","3","-2","null","1"}), 8) == 3);
assert(Solution().pathSum(tree({"5","4","8","11","null","13","4","7","2","null","null","5","1"}), 22) == 3);
```

### Complexity

O(n) time, O(h) space for the path (map entries)

### Traps

- Forgetting to undo cnt\[s\]++ (sibling subtrees then share prefixes)
- int overflow

### Follow-ups

- Path Sum II: return the paths from root to leaf with sum t (backtracking).

## 19. Flatten Binary Tree to Linked List

L2 [Trees](knowledge-base/dsa.md#binary-trees) · [LeetCode ↗](https://leetcode.com/problems/flatten-binary-tree-to-linked-list/) · In-place pointer rewiring.

### Key idea

Morris-style: at each node with a left child, find the rightmost node of the left subtree, attach the current right subtree there, move the left subtree to the right, clear left. Move right.

### Steps

1.  cur = root; while cur
2.  If cur-\>left: p = rightmost of cur-\>left; p-\>right = cur-\>right; cur-\>right = cur-\>left; cur-\>left = null
3.  cur = cur-\>right

### C++17 solution

``` cpp
class Solution {
public:
    void flatten(TreeNode* root) {
        for (TreeNode* cur = root; cur; cur = cur->right)
            if (cur->left) {
                TreeNode* p = cur->left;
                while (p->right) p = p->right;
                p->right = cur->right; cur->right = cur->left; cur->left = nullptr;
            }
    }
};
```

### Test it passed

``` cpp
TreeNode* r = tree({"1","2","5","3","4","null","6"}); Solution().flatten(r); vector<int> v;
for (TreeNode* c = r; c; c = c->right) { assert(!c->left); v.push_back(c->val); } assert((v == vector<int>{1,2,3,4,5,6}));
```

### Complexity

O(n) time, O(1) space

### Traps

- Leaving left pointers set

### Follow-ups

- Recursive version with a 'prev' pointer in reverse preorder (right, left, root).

## 20. Lowest Common Ancestor of a Binary Search Tree

L2 [BST](knowledge-base/dsa.md#binary-search-trees) · [LeetCode ↗](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/) · Use the BST order.

### Key idea

If both values are smaller than the node, the LCA is on the left; if both larger, on the right; otherwise this node splits them and is the LCA.

### Steps

1.  Loop from the root
2.  Both \< val: go left; both \> val: go right
3.  Else return the node

### C++17 solution

``` cpp
class Solution {
public:
    TreeNode* lowestCommonAncestor(TreeNode* r, TreeNode* p, TreeNode* q) {
        while (r) {
            if (p->val < r->val && q->val < r->val) r = r->left;
            else if (p->val > r->val && q->val > r->val) r = r->right;
            else return r;
        }
        return nullptr;
    }
};
```

### Test it passed

``` text
TreeNode* r = tree({"6","2","8","0","4","7","9","null","null","3","5"});
TreeNode *two = r->left, *eight = r->right, *four = r->left->right;
assert(Solution().lowestCommonAncestor(r, two, eight) == r && Solution().lowestCommonAncestor(r, two, four) == two);
```

### Complexity

O(h) time, O(1) space

### Traps

- Using the general binary-tree LCA (works but ignores the BST property)

### Follow-ups

- What if p or q may be missing from the tree? Check existence first.

## 21. Delete Node in a BST

L2 [BST](knowledge-base/dsa.md#binary-search-trees) · [LeetCode ↗](https://leetcode.com/problems/delete-node-in-a-bst/) · The three deletion cases.

### Key idea

Find the node. No left child: return right. No right child: return left. Two children: copy the smallest value of the right subtree into the node, then delete that value from the right subtree.

### Steps

1.  Recurse left or right by comparing keys
2.  Handle the 0/1-child cases by returning the other child
3.  Two children: successor = leftmost of right

### C++17 solution

``` cpp
class Solution {
public:
    TreeNode* deleteNode(TreeNode* r, int key) {
        if (!r) return nullptr;
        if (key < r->val) r->left = deleteNode(r->left, key);
        else if (key > r->val) r->right = deleteNode(r->right, key);
        else {
            if (!r->left) return r->right;          // the test harness does not free nodes, so no delete here
            if (!r->right) return r->left;
            TreeNode* s = r->right; while (s->left) s = s->left;
            r->val = s->val; r->right = deleteNode(r->right, s->val);
        }
        return r;
    }
};
```

### Test it passed

``` cpp
auto inorder = [](TreeNode* t) { vector<int> v; function<void(TreeNode*)> go = [&](TreeNode* x) { if (!x) return; go(x->left); v.push_back(x->val); go(x->right); }; go(t); return v; };
TreeNode* r = Solution().deleteNode(tree({"5","3","6","2","4","null","7"}), 3); assert((inorder(r) == vector<int>{2,4,5,6,7}));
r = Solution().deleteNode(r, 5); assert((inorder(r) == vector<int>{2,4,6,7})); assert((inorder(Solution().deleteNode(r, 0)) == vector<int>{2,4,6,7}));
```

### Complexity

O(h) time, O(h) stack

### Traps

- Losing a subtree in the two-children case

### Follow-ups

- Insert into a BST; check the tree stays balanced (AVL / red-black discussion).

## 22. Binary Tree Zigzag Level Order Traversal

L2 [BFS](knowledge-base/dsa.md#bfs-and-graph-basics) · [LeetCode ↗](https://leetcode.com/problems/binary-tree-zigzag-level-order-traversal/) · Level order with a twist.

### Key idea

Normal BFS level by level; reverse every second level (or fill each level's vector from the back).

### Steps

1.  Queue with root
2.  For each level: pop size nodes, write val at index i or size-1-i
3.  Flip the direction flag

### C++17 solution

``` cpp
class Solution {
public:
    vector<vector<int>> zigzagLevelOrder(TreeNode* root) {
        vector<vector<int>> r; if (!root) return r;
        queue<TreeNode*> q; q.push(root); bool ltr = true;
        while (!q.empty()) {
            int n = q.size(); vector<int> lv(n);
            for (int i = 0; i < n; i++) {
                TreeNode* x = q.front(); q.pop();
                lv[ltr ? i : n - 1 - i] = x->val;
                if (x->left) q.push(x->left);
                if (x->right) q.push(x->right);
            }
            r.push_back(lv); ltr = !ltr;
        }
        return r;
    }
};
```

### Test it passed

``` cpp
assert((Solution().zigzagLevelOrder(tree({"3","9","20","null","null","15","7"})) == vector<vector<int>>{{3},{20,9},{15,7}}));
```

### Complexity

O(n) time, O(n) space

### Traps

- Changing the order children are pushed instead of the write order (breaks lower levels)

### Follow-ups

- Vertical order traversal (sort by column, then row, then value).

## 23. All Nodes Distance K in Binary Tree

L2 [BFS](knowledge-base/dsa.md#bfs-and-graph-basics) · [LeetCode ↗](https://leetcode.com/problems/all-nodes-distance-k-in-binary-tree/) · Turn the tree into a graph.

### Key idea

Record each node's parent with a DFS. Then BFS from the target over three neighbours (left, right, parent) for k steps; the nodes in the queue are the answer.

### Steps

1.  DFS to fill parent\[\]
2.  BFS from target with a visited set, k levels
3.  Return the values in the last level

### C++17 solution

``` cpp
class Solution {
    unordered_map<TreeNode*, TreeNode*> par;
    void link(TreeNode* n, TreeNode* p) { if (!n) return; par[n] = p; link(n->left, n); link(n->right, n); }
public:
    vector<int> distanceK(TreeNode* root, TreeNode* target, int k) {
        link(root, nullptr);
        queue<TreeNode*> q; q.push(target); unordered_set<TreeNode*> seen{target};
        for (int d = 0; d < k && !q.empty(); d++)
            for (int n = q.size(); n--; ) {
                TreeNode* x = q.front(); q.pop();
                for (TreeNode* y : {x->left, x->right, par[x]})
                    if (y && seen.insert(y).second) q.push(y);
            }
        vector<int> r; while (!q.empty()) { r.push_back(q.front()->val); q.pop(); }
        return r;
    }
};
```

### Test it passed

``` cpp
TreeNode* r = tree({"3","5","1","6","2","0","8","null","null","7","4"});
auto v = Solution().distanceK(r, r->left, 2); sort(v.begin(), v.end()); assert((v == vector<int>{1,4,7}));
```

### Complexity

O(n) time, O(n) space

### Traps

- Revisiting the node you came from (use a visited set)

### Follow-ups

- Do it without the parent map: return distances up the recursion.

## 24. Open the Lock

L2 [BFS](knowledge-base/dsa.md#bfs-and-graph-basics) · [LeetCode ↗](https://leetcode.com/problems/open-the-lock/) · Shortest path in an implicit graph.

### Key idea

States are the 10,000 four-digit strings; each has 8 neighbours (turn one wheel up or down). BFS from "0000" avoiding deadends; the level when the target appears is the answer.

### Steps

1.  Put deadends in a visited set; if "0000" is dead return -1
2.  BFS by levels
3.  For each wheel, try ±1 mod 10

### C++17 solution

``` cpp
class Solution {
public:
    int openLock(vector<string>& dead, string target) {
        unordered_set<string> seen(dead.begin(), dead.end());
        if (seen.count("0000")) return -1;
        queue<string> q; q.push("0000"); seen.insert("0000");
        for (int steps = 0; !q.empty(); steps++)
            for (int n = q.size(); n--; ) {
                string s = q.front(); q.pop();
                if (s == target) return steps;
                for (int i = 0; i < 4; i++)
                    for (int d : {1, 9}) {
                        string t = s; t[i] = (t[i] - '0' + d) % 10 + '0';
                        if (seen.insert(t).second) q.push(t);
                    }
            }
        return -1;
    }
};
```

### Test it passed

``` cpp
vector<string> a{"0201","0101","0102","1212","2002"}, b{"8888"}, c{"8887","8889","8878","8898","8788","8988","7888","9888"};
assert(Solution().openLock(a, "0202") == 6 && Solution().openLock(b, "0009") == 1 && Solution().openLock(c, "8888") == -1);
```

### Complexity

O(10⁴ · 8) time and space

### Traps

- Wheel arithmetic for 0 → 9 (use + 9 mod 10)

### Follow-ups

- Bidirectional BFS roughly halves the explored states.

## 25. Shortest Path in Binary Matrix

L2 [BFS](knowledge-base/dsa.md#bfs-and-graph-basics) · [LeetCode ↗](https://leetcode.com/problems/shortest-path-in-binary-matrix/) · Grid BFS with 8 directions.

### Key idea

BFS from the top-left over 0-cells in 8 directions, counting cells on the path. Mark cells as visited when pushed. Blocked start or end means -1.

### Steps

1.  If g\[0\]\[0\] or g\[n-1\]\[n-1\] is 1: return -1
2.  dist starts at 1
3.  Pop, check if it is the end, push 8 neighbours

### C++17 solution

``` cpp
class Solution {
public:
    int shortestPathBinaryMatrix(vector<vector<int>>& g) {
        int n = g.size(); if (g[0][0] || g[n - 1][n - 1]) return -1;
        queue<array<int, 3>> q; q.push({0, 0, 1}); g[0][0] = 1;
        while (!q.empty()) {
            auto [r, c, d] = q.front(); q.pop();
            if (r == n - 1 && c == n - 1) return d;
            for (int dr = -1; dr <= 1; dr++)
                for (int dc = -1; dc <= 1; dc++) {
                    int nr = r + dr, nc = c + dc;
                    if (nr >= 0 && nc >= 0 && nr < n && nc < n && !g[nr][nc]) { g[nr][nc] = 1; q.push({nr, nc, d + 1}); }
                }
        }
        return -1;
    }
};
```

### Test it passed

``` cpp
vector<vector<int>> a{{0,1},{1,0}}, b{{0,0,0},{1,1,0},{1,1,0}}, c{{1,0,0},{1,1,0},{1,1,0}}, d{{0}};
assert(Solution().shortestPathBinaryMatrix(a) == 2 && Solution().shortestPathBinaryMatrix(b) == 4 && Solution().shortestPathBinaryMatrix(c) == -1 && Solution().shortestPathBinaryMatrix(d) == 1);
```

### Complexity

O(n²) time and space

### Traps

- Marking visited when popped (cells get pushed many times)

### Follow-ups

- Weighted cells: Dijkstra. A\* with Chebyshev distance as the heuristic.

## 26. Is Graph Bipartite?

L2 [BFS](knowledge-base/dsa.md#bfs-and-graph-basics) · [LeetCode ↗](https://leetcode.com/problems/is-graph-bipartite/) · Two-colouring.

### Key idea

Colour each uncoloured node 0 and BFS; every neighbour must get the opposite colour. A neighbour with the same colour means an odd cycle: not bipartite. Start from every node (the graph may be disconnected).

### Steps

1.  color\[\] = -1
2.  For each uncoloured node: BFS
3.  Same colour on an edge → false

### C++17 solution

``` cpp
class Solution {
public:
    bool isBipartite(vector<vector<int>>& g) {
        int n = g.size(); vector<int> col(n, -1);
        for (int s = 0; s < n; s++) {
            if (col[s] != -1) continue;
            queue<int> q; q.push(s); col[s] = 0;
            while (!q.empty()) {
                int u = q.front(); q.pop();
                for (int v : g[u]) {
                    if (col[v] == -1) { col[v] = col[u] ^ 1; q.push(v); }
                    else if (col[v] == col[u]) return false;
                }
            }
        }
        return true;
    }
};
```

### Test it passed

``` cpp
vector<vector<int>> a{{1,2,3},{0,2},{0,1,3},{0,2}}, b{{1,3},{0,2},{1,3},{0,2}}, c{{},{2},{1}};
assert(!Solution().isBipartite(a) && Solution().isBipartite(b) && Solution().isBipartite(c));
```

### Complexity

O(V + E) time, O(V) space

### Traps

- Starting only from node 0 (misses other components)

### Follow-ups

- Possible Bipartition (dislikes list): build the graph, same check.
- Union-Find version: union all neighbours of u; u must not join them.

## 27. Find Eventual Safe States

L2 [Topological sort](knowledge-base/dsa.md#topological-sort) · [LeetCode ↗](https://leetcode.com/problems/find-eventual-safe-states/) · Kahn's algorithm on the reversed graph.

### Key idea

A node is safe if every path leads to a terminal node. Reverse the edges and run Kahn's algorithm from the terminal nodes (out-degree 0): everything removed is safe; nodes on or leading into cycles never reach 0.

### Steps

1.  outdeg\[u\] = g\[u\].size(); rev\[v\].push_back(u)
2.  Queue all nodes with outdeg 0
3.  Pop u, mark safe, for p in rev\[u\]: if --outdeg\[p\] == 0 push

### C++17 solution

``` cpp
class Solution {
public:
    vector<int> eventualSafeNodes(vector<vector<int>>& g) {
        int n = g.size(); vector<vector<int>> rev(n); vector<int> out(n); queue<int> q; vector<bool> safe(n);
        for (int u = 0; u < n; u++) { out[u] = g[u].size(); for (int v : g[u]) rev[v].push_back(u); if (!out[u]) q.push(u); }
        while (!q.empty()) {
            int u = q.front(); q.pop(); safe[u] = true;
            for (int p : rev[u]) if (--out[p] == 0) q.push(p);
        }
        vector<int> r; for (int u = 0; u < n; u++) if (safe[u]) r.push_back(u);
        return r;
    }
};
```

### Test it passed

``` cpp
vector<vector<int>> a{{1,2},{2,3},{5},{0},{5},{},{}}, b{{1,2,3,4},{1,2},{3,4},{0,4},{}};
assert((Solution().eventualSafeNodes(a) == vector<int>{2,4,5,6}) && (Solution().eventualSafeNodes(b) == vector<int>{4}));
```

### Complexity

O(V + E) time and space

### Traps

- Using in-degree on the original graph (answers a different question)

### Follow-ups

- DFS with three colours (white, grey on stack, black safe) gives the same answer.

## 28. Path With Minimum Effort

L2 [Shortest paths](knowledge-base/dsa.md#dijkstra-and-shortest-paths) · [LeetCode ↗](https://leetcode.com/problems/path-with-minimum-effort/) · Dijkstra with a max instead of a sum.

### Key idea

The cost of a path is its largest height step. Dijkstra still works: the cost to reach a neighbour is max(cost so far, \|height difference\|), and it never decreases along a path.

### Steps

1.  dist all INF, dist\[0\]\[0\] = 0, min-heap of (dist, r, c)
2.  Pop; skip stale entries; stop at the bottom-right
3.  Relax 4 neighbours with max()

### C++17 solution

``` cpp
class Solution {
public:
    int minimumEffortPath(vector<vector<int>>& h) {
        int R = h.size(), C = h[0].size(); vector<vector<int>> dist(R, vector<int>(C, INT_MAX));
        priority_queue<array<int, 3>, vector<array<int, 3>>, greater<>> pq; pq.push({0, 0, 0}); dist[0][0] = 0;
        int dr[] = {1, -1, 0, 0}, dc[] = {0, 0, 1, -1};
        while (!pq.empty()) {
            auto [d, r, c] = pq.top(); pq.pop();
            if (d > dist[r][c]) continue;
            if (r == R - 1 && c == C - 1) return d;
            for (int k = 0; k < 4; k++) {
                int nr = r + dr[k], nc = c + dc[k];
                if (nr < 0 || nc < 0 || nr >= R || nc >= C) continue;
                int nd = max(d, abs(h[nr][nc] - h[r][c]));
                if (nd < dist[nr][nc]) { dist[nr][nc] = nd; pq.push({nd, nr, nc}); }
            }
        }
        return 0;
    }
};
```

### Test it passed

``` cpp
vector<vector<int>> a{{1,2,2},{3,8,2},{5,3,5}}, b{{1,2,3},{3,8,4},{5,3,5}}, c{{1,2,1,1,1},{1,2,1,2,1},{1,2,1,2,1},{1,2,1,2,1},{1,1,1,2,1}};
assert(Solution().minimumEffortPath(a) == 2 && Solution().minimumEffortPath(b) == 1 && Solution().minimumEffortPath(c) == 0);
```

### Complexity

O(RC log(RC)) time, O(RC) space

### Traps

- Summing the differences instead of taking the max

### Follow-ups

- Alternative: binary search the effort + BFS, or Kruskal with Union-Find until start and end connect.

## 29. Min Cost to Connect All Points

L2 [MST](knowledge-base/dsa.md#disjoint-set-union-union-find) · [LeetCode ↗](https://leetcode.com/problems/min-cost-to-connect-all-points/) · Minimum spanning tree (Prim).

### Key idea

Connect all points with minimum total Manhattan distance = an MST of the complete graph. Prim's O(n²) version is simplest for a dense graph: keep each point's cheapest edge to the tree, add the cheapest point, update.

### Steps

1.  minEdge\[i\] = INF, minEdge\[0\] = 0
2.  n times: pick the unused point with the smallest minEdge, add it
3.  Update every unused point's minEdge with its distance to the new point

### C++17 solution

``` cpp
class Solution {
public:
    int minCostConnectPoints(vector<vector<int>>& p) {
        int n = p.size(), total = 0; vector<int> best(n, INT_MAX); vector<bool> in(n); best[0] = 0;
        for (int it = 0; it < n; it++) {
            int u = -1;
            for (int i = 0; i < n; i++) if (!in[i] && (u == -1 || best[i] < best[u])) u = i;
            in[u] = true; total += best[u];
            for (int v = 0; v < n; v++)
                if (!in[v]) best[v] = min(best[v], abs(p[u][0] - p[v][0]) + abs(p[u][1] - p[v][1]));
        }
        return total;
    }
};
```

### Test it passed

``` cpp
vector<vector<int>> a{{0,0},{2,2},{3,10},{5,2},{7,0}}, b{{3,12},{-2,5},{-4,1}}, c{{0,0}};
assert(Solution().minCostConnectPoints(a) == 20 && Solution().minCostConnectPoints(b) == 18 && Solution().minCostConnectPoints(c) == 0);
```

### Complexity

O(n²) time, O(n) space

### Traps

- Kruskal on all n² edges works but sorts ~n²/2 edges (slower for n = 1000)

### Follow-ups

- Explain Kruskal with Union-Find and when it beats Prim (sparse graphs).

## 30. Number of Operations to Make Network Connected

L2 [Union-Find](knowledge-base/dsa.md#disjoint-set-union-union-find) · [LeetCode ↗](https://leetcode.com/problems/number-of-operations-to-make-network-connected/) · Count components.

### Key idea

With fewer than n − 1 cables it is impossible. Otherwise, every redundant cable can be moved, and you need components − 1 moves. Count components with Union-Find.

### Steps

1.  If edges \< n - 1: return -1
2.  Union every cable; components = n − successful unions
3.  Return components − 1

### C++17 solution

``` cpp
class Solution {
    vector<int> par;
    int find(int x) { return par[x] == x ? x : par[x] = find(par[x]); }
public:
    int makeConnected(int n, vector<vector<int>>& cables) {
        if ((int)cables.size() < n - 1) return -1;
        par.resize(n); iota(par.begin(), par.end(), 0); int comps = n;
        for (auto& c : cables) { int a = find(c[0]), b = find(c[1]); if (a != b) { par[a] = b; comps--; } }
        return comps - 1;
    }
};
```

### Test it passed

``` cpp
vector<vector<int>> a{{0,1},{0,2},{1,2}}, b{{0,1},{0,2},{0,3},{1,2},{1,3}}, c{{0,1},{0,2},{0,3},{1,2}};
assert(Solution().makeConnected(4, a) == 1 && Solution().makeConnected(6, b) == 2 && Solution().makeConnected(6, c) == -1);
```

### Complexity

O((n + E) α(n)) time, O(n) space

### Traps

- Counting redundant cables instead of components (only the count check needs them)

### Follow-ups

- Add union by rank and explain why α(n) is effectively constant.

## 31. Combination Sum II

L2 [Backtracking](knowledge-base/dsa.md#recursion-and-backtracking) · [LeetCode ↗](https://leetcode.com/problems/combination-sum-ii/) · Duplicates in the input.

### Key idea

Sort. At each depth, try each candidate once per value: skip a\[i\] if i \> start and a\[i\] == a\[i−1\]. Each number is used at most once, so recurse with i + 1. Stop early when a\[i\] exceeds the remaining target.

### Steps

1.  Sort
2.  dfs(start, rem): if rem == 0 record
3.  for i ≥ start: skip same-value siblings; break if a\[i\] \> rem; recurse i + 1

### C++17 solution

``` cpp
class Solution {
    vector<vector<int>> r; vector<int> cur;
    void dfs(vector<int>& a, int s, int rem) {
        if (!rem) { r.push_back(cur); return; }
        for (int i = s; i < (int)a.size() && a[i] <= rem; i++) {
            if (i > s && a[i] == a[i - 1]) continue;
            cur.push_back(a[i]); dfs(a, i + 1, rem - a[i]); cur.pop_back();
        }
    }
public:
    vector<vector<int>> combinationSum2(vector<int>& a, int t) { sort(a.begin(), a.end()); dfs(a, 0, t); return r; }
};
```

### Test it passed

``` cpp
vector<int> a{10,1,2,7,6,1,5}, b{2,5,2,1,2};
assert((Solution().combinationSum2(a, 8) == vector<vector<int>>{{1,1,6},{1,2,5},{1,7},{2,6}}));
assert((Solution().combinationSum2(b, 5) == vector<vector<int>>{{1,2,2},{5}}));
```

### Complexity

O(2ⁿ) worst case time, O(n) depth

### Traps

- Skipping with i \> 0 instead of i \> start (loses \[1,1,6\])

### Follow-ups

- Combination Sum III (k numbers from 1–9).

## 32. Palindrome Partitioning

L2 [Backtracking](knowledge-base/dsa.md#recursion-and-backtracking) · [LeetCode ↗](https://leetcode.com/problems/palindrome-partitioning/) · Cut points with a palindrome check.

### Key idea

From position s, try every end e where s\[s..e\] is a palindrome, take it, and recurse from e + 1. A precomputed table pal\[i\]\[j\] makes each check O(1).

### Steps

1.  pal\[i\]\[j\] = s\[i\]==s\[j\] && (j - i \< 2 \|\| pal\[i+1\]\[j-1\]) (fill i from the end)
2.  dfs(start): at the end record the path
3.  Try each palindromic piece

### C++17 solution

``` cpp
class Solution {
    vector<vector<string>> r; vector<string> cur; vector<vector<bool>> pal;
    void dfs(const string& s, int st) {
        if (st == (int)s.size()) { r.push_back(cur); return; }
        for (int e = st; e < (int)s.size(); e++)
            if (pal[st][e]) { cur.push_back(s.substr(st, e - st + 1)); dfs(s, e + 1); cur.pop_back(); }
    }
public:
    vector<vector<string>> partition(string s) {
        int n = s.size(); pal.assign(n, vector<bool>(n));
        for (int i = n - 1; i >= 0; i--) for (int j = i; j < n; j++) pal[i][j] = s[i] == s[j] && (j - i < 2 || pal[i + 1][j - 1]);
        dfs(s, 0); return r;
    }
};
```

### Test it passed

``` cpp
assert((Solution().partition("aab") == vector<vector<string>>{{"a","a","b"},{"aa","b"}}) && (Solution().partition("a") == vector<vector<string>>{{"a"}}));
assert(Solution().partition("aaaa").size() == 8);
```

### Complexity

O(n · 2ⁿ) time, O(n²) table

### Traps

- Filling the table with i ascending (pal\[i+1\]\[j-1\] not ready yet)

### Follow-ups

- Palindrome Partitioning II: minimum cuts with DP in O(n²).

## 33. Sudoku Solver

L3 [Backtracking](knowledge-base/dsa.md#recursion-and-backtracking) · [LeetCode ↗](https://leetcode.com/problems/sudoku-solver/) · Constraint backtracking with bitmasks.

### Key idea

Keep a 9-bit mask of used digits per row, column and box. Go through empty cells in order; for each, try digits not in any of the three masks, set, recurse, unset on failure.

### Steps

1.  Build masks and the list of empty cells
2.  solve(k): if k == empties.size() return true
3.  For each free digit: set bits, write, recurse; undo

### C++17 solution

``` cpp
class Solution {
    int row[9] = {}, col[9] = {}, box[9] = {}; vector<pair<int, int>> e;
    bool solve(vector<vector<char>>& b, size_t k) {
        if (k == e.size()) return true;
        auto [r, c] = e[k]; int bx = r / 3 * 3 + c / 3, used = row[r] | col[c] | box[bx];
        for (int d = 0; d < 9; d++) {
            if (used >> d & 1) continue;
            row[r] ^= 1 << d; col[c] ^= 1 << d; box[bx] ^= 1 << d; b[r][c] = '1' + d;
            if (solve(b, k + 1)) return true;
            row[r] ^= 1 << d; col[c] ^= 1 << d; box[bx] ^= 1 << d;
        }
        b[r][c] = '.'; return false;
    }
public:
    void solveSudoku(vector<vector<char>>& b) {
        for (int r = 0; r < 9; r++) for (int c = 0; c < 9; c++) {
            if (b[r][c] == '.') { e.push_back({r, c}); continue; }
            int d = b[r][c] - '1'; row[r] |= 1 << d; col[c] |= 1 << d; box[r / 3 * 3 + c / 3] |= 1 << d;
        }
        solve(b, 0);
    }
};
```

### Test it passed

``` cpp
vector<string> s{"53..7....","6..195...",".98....6.","8...6...3","4..8.3..1","7...2...6",".6....28.","...419..5","....8..79"};
vector<vector<char>> b; for (auto& x : s) b.push_back(vector<char>(x.begin(), x.end())); Solution().solveSudoku(b);
vector<string> want{"534678912","672195348","198342567","859761423","426853791","713924856","961537284","287419635","345286179"};
for (int r = 0; r < 9; r++) assert(string(b[r].begin(), b[r].end()) == want[r]);
```

### Complexity

Exponential worst case, fast in practice; O(81) space

### Traps

- Forgetting to reset the cell to '.' when backtracking past it

### Follow-ups

- Speed-up: always fill the empty cell with the fewest options next (MRV heuristic).

## 34. Partition Labels

L2 [Greedy](knowledge-base/dsa.md#greedy-algorithms) · [LeetCode ↗](https://leetcode.com/problems/partition-labels/) · Last occurrence trick.

### Key idea

Record the last index of each letter. Scan, extending the current part's end to the last index of every letter seen. When i reaches that end, close the part.

### Steps

1.  last\[c\] for each letter
2.  end = max(end, last\[s\[i\]\])
3.  If i == end: record i - start + 1, start = i + 1

### C++17 solution

``` cpp
class Solution {
public:
    vector<int> partitionLabels(string s) {
        int last[26] = {}; for (int i = 0; i < (int)s.size(); i++) last[s[i] - 'a'] = i;
        vector<int> r; int st = 0, end = 0;
        for (int i = 0; i < (int)s.size(); i++) {
            end = max(end, last[s[i] - 'a']);
            if (i == end) { r.push_back(i - st + 1); st = i + 1; }
        }
        return r;
    }
};
```

### Test it passed

``` cpp
assert((Solution().partitionLabels("ababcbacadefegdehijhklij") == vector<int>{9,7,8}) && (Solution().partitionLabels("eccbbbbdec") == vector<int>{10}));
```

### Complexity

O(n) time, O(1) space

### Traps

- Closing a part before checking every letter inside it

### Follow-ups

- This is Merge Intervals in disguise: each letter is the interval \[first, last\].

## 35. Interval List Intersections

L2 [Intervals](knowledge-base/dsa.md#interval-problems) · [LeetCode ↗](https://leetcode.com/problems/interval-list-intersections/) · Two pointers on sorted intervals.

### Key idea

Both lists are sorted and disjoint. The overlap of A\[i\] and B\[j\] is \[max starts, min ends\] if that is non-empty. Then drop whichever interval ends first.

### Steps

1.  lo = max(a0, b0), hi = min(a1, b1)
2.  If lo ≤ hi record
3.  Advance the pointer whose interval ends first

### C++17 solution

``` cpp
class Solution {
public:
    vector<vector<int>> intervalIntersection(vector<vector<int>>& A, vector<vector<int>>& B) {
        vector<vector<int>> r; size_t i = 0, j = 0;
        while (i < A.size() && j < B.size()) {
            int lo = max(A[i][0], B[j][0]), hi = min(A[i][1], B[j][1]);
            if (lo <= hi) r.push_back({lo, hi});
            (A[i][1] < B[j][1]) ? i++ : j++;
        }
        return r;
    }
};
```

### Test it passed

``` cpp
vector<vector<int>> A{{0,2},{5,10},{13,23},{24,25}}, B{{1,5},{8,12},{15,24},{25,26}}, C{}, D{{1,7}};
assert((Solution().intervalIntersection(A, B) == vector<vector<int>>{{1,2},{5,5},{8,10},{15,23},{24,24},{25,25}}));
assert(Solution().intervalIntersection(C, D).empty());
```

### Complexity

O(m + n) time, O(1) extra space

### Traps

- Advancing both pointers after a match

### Follow-ups

- Meeting scheduler: first common slot of at least d minutes (same loop, check hi − lo ≥ d).

## 36. House Robber II

L2 [DP](knowledge-base/dsa.md#dynamic-programming) · [LeetCode ↗](https://leetcode.com/problems/house-robber-ii/) · Circular version of House Robber.

### Key idea

The first and last houses are adjacent, so you cannot take both. Answer = max(rob houses 0..n−2, rob houses 1..n−1), each a plain House Robber in O(1) space.

### Steps

1.  n == 1: return a\[0\]
2.  line(l, r): prev2, prev1 rolling max
3.  Return max(line(0, n-2), line(1, n-1))

### C++17 solution

``` cpp
class Solution {
    int line(vector<int>& a, int l, int r) {
        int p2 = 0, p1 = 0;
        for (int i = l; i <= r; i++) { int cur = max(p1, p2 + a[i]); p2 = p1; p1 = cur; }
        return p1;
    }
public:
    int rob(vector<int>& a) {
        int n = a.size(); if (n == 1) return a[0];
        return max(line(a, 0, n - 2), line(a, 1, n - 1));
    }
};
```

### Test it passed

``` cpp
vector<int> a{2,3,2}, b{1,2,3,1}, c{1,2,3}, d{5};
assert(Solution().rob(a) == 3 && Solution().rob(b) == 4 && Solution().rob(c) == 3 && Solution().rob(d) == 5);
```

### Complexity

O(n) time, O(1) space

### Traps

- Forgetting n == 1 (both ranges become empty)

### Follow-ups

- House Robber III: houses on a binary tree (return (take, skip) per node).

## 37. Target Sum

L2 [DP](knowledge-base/dsa.md#dynamic-programming) · [LeetCode ↗](https://leetcode.com/problems/target-sum/) · Reduces to subset-sum counting.

### Key idea

Split the numbers into a plus set P and a minus set N: P − N = t and P + N = S, so P = (S + t) / 2. Count subsets with that sum using a 1D knapsack (iterate sums downwards).

### Steps

1.  If \|t\| \> S or (S + t) odd: return 0
2.  goal = (S + t) / 2; dp\[0\] = 1
3.  For each x: for s from goal down to x: dp\[s\] += dp\[s - x\]

### C++17 solution

``` cpp
class Solution {
public:
    int findTargetSumWays(vector<int>& a, int t) {
        int S = accumulate(a.begin(), a.end(), 0);
        if (abs(t) > S || (S + t) % 2) return 0;
        int goal = (S + t) / 2; vector<int> dp(goal + 1); dp[0] = 1;
        for (int x : a) for (int s = goal; s >= x; s--) dp[s] += dp[s - x];
        return dp[goal];
    }
};
```

### Test it passed

``` cpp
vector<int> a{1,1,1,1,1}, b{1}, c{0,0,0,0,0,0,0,0,1}, d{100};
assert(Solution().findTargetSumWays(a, 3) == 5 && Solution().findTargetSumWays(b, 1) == 1 && Solution().findTargetSumWays(c, 1) == 256 && Solution().findTargetSumWays(d, -200) == 0);
```

### Complexity

O(n · goal) time, O(goal) space

### Traps

- Iterating sums upwards (uses an item twice)
- Missing the \|t\| \> S check (negative index)

### Follow-ups

- Explain why zeros double the count (each 0 can be + or −).

## 38. Maximal Square

L2 [DP](knowledge-base/dsa.md#dynamic-programming) · [LeetCode ↗](https://leetcode.com/problems/maximal-square/) · Grid DP with a min of three.

### Key idea

dp\[i\]\[j\] = side of the largest all-1 square with bottom-right corner (i, j) = 1 + min(top, left, top-left) when the cell is '1'. Track the maximum side and return its square.

### Steps

1.  dp sized (R+1) × (C+1) to avoid edge checks
2.  If m\[i\]\[j\] == '1': dp = 1 + min of three neighbours
3.  Return best²

### C++17 solution

``` cpp
class Solution {
public:
    int maximalSquare(vector<vector<char>>& m) {
        int R = m.size(), C = m[0].size(), best = 0; vector<vector<int>> dp(R + 1, vector<int>(C + 1));
        for (int i = 1; i <= R; i++)
            for (int j = 1; j <= C; j++)
                if (m[i - 1][j - 1] == '1') {
                    dp[i][j] = 1 + min({dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]});
                    best = max(best, dp[i][j]);
                }
        return best * best;
    }
};
```

### Test it passed

``` cpp
vector<string> s{"10100","10111","11111","10010"}; vector<vector<char>> m; for (auto& x : s) m.push_back(vector<char>(x.begin(), x.end()));
vector<vector<char>> z{{'0','1'},{'1','0'}}, o{{'0'}};
assert(Solution().maximalSquare(m) == 4 && Solution().maximalSquare(z) == 1 && Solution().maximalSquare(o) == 0);
```

### Complexity

O(RC) time, O(RC) space (O(C) with one row)

### Traps

- Returning the side instead of the area

### Follow-ups

- Maximal Rectangle: histogram + stack per row.
- Count all square submatrices: sum every dp value.

## 39. Best Time to Buy and Sell Stock with Cooldown

L2 [DP](knowledge-base/dsa.md#dynamic-programming) · [LeetCode ↗](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-cooldown/) · State machine DP.

### Key idea

Three states at the end of each day: hold (own a share), sold (sold today), rest (no share, free to buy). hold = max(hold, rest − p); sold = hold + p; rest = max(rest, sold). Cooldown is enforced because you can only buy from rest.

### Steps

1.  hold = -INF, sold = 0, rest = 0
2.  Update all three from the previous day's values
3.  Answer max(sold, rest)

### C++17 solution

``` cpp
class Solution {
public:
    int maxProfit(vector<int>& p) {
        int hold = INT_MIN / 2, sold = 0, rest = 0;
        for (int x : p) {
            int h = max(hold, rest - x), s = hold + x, r = max(rest, sold);
            hold = h; sold = s; rest = r;
        }
        return max(sold, rest);
    }
};
```

### Test it passed

``` cpp
vector<int> a{1,2,3,0,2}, b{1}, c{2,1};
assert(Solution().maxProfit(a) == 3 && Solution().maxProfit(b) == 0 && Solution().maxProfit(c) == 0);
```

### Complexity

O(n) time, O(1) space

### Traps

- Updating in place so today's sold uses today's hold

### Follow-ups

- With a transaction fee; at most k transactions (Stock IV).

## 40. Interleaving String

L2 [String DP](knowledge-base/dsa.md#string-dp-lcs-and-edit-distance) · [LeetCode ↗](https://leetcode.com/problems/interleaving-string/) · 2D DP over two prefixes.

### Key idea

dp\[i\]\[j\] = can the first i chars of s1 and the first j chars of s2 form the first i + j chars of s3? It is true if the last char came from s1 (dp\[i−1\]\[j\] and s1\[i−1\] == s3\[i+j−1\]) or from s2 (similarly).

### Steps

1.  If lengths do not add up: false
2.  dp\[0\]\[0\] = true
3.  Fill row by row; return dp\[m\]\[n\]

### C++17 solution

``` cpp
class Solution {
public:
    bool isInterleave(string a, string b, string c) {
        int m = a.size(), n = b.size(); if (m + n != (int)c.size()) return false;
        vector<vector<bool>> dp(m + 1, vector<bool>(n + 1)); dp[0][0] = true;
        for (int i = 0; i <= m; i++)
            for (int j = 0; j <= n; j++) {
                if (i && dp[i - 1][j] && a[i - 1] == c[i + j - 1]) dp[i][j] = true;
                if (j && dp[i][j - 1] && b[j - 1] == c[i + j - 1]) dp[i][j] = true;
            }
        return dp[m][n];
    }
};
```

### Test it passed

``` text
assert(Solution().isInterleave("aabcc", "dbbca", "aadbbcbcac") && !Solution().isInterleave("aabcc", "dbbca", "aadbbbaccc") && Solution().isInterleave("", "", ""));
```

### Complexity

O(mn) time, O(mn) space (O(n) with one row)

### Traps

- Greedy matching from s1 first (fails when both strings offer the same char)

### Follow-ups

- Reduce to O(n) space with a single row.
