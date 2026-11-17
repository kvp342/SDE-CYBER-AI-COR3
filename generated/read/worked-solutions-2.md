WORKED SOLUTIONS · PART II

# 40 more tested solutions

Forty frequently asked LeetCode problems that are not in Part I (the 43 solutions in the Knowledge Base). Each page gives the pattern, the key idea, the steps, a C++17 solution, the test it passed, the complexity, the traps and the follow-up questions interviewers ask. Levels: L1 4, L2 31, L3 5.

**How to use.** Read the title, try the problem on LeetCode for 25 minutes (L1 15, L3 40), then open the page. If you needed the solution, log it in your revision tracker and redo it in 3, 7 and 21 days. Every solution here was compiled with `g++ -std=c++17 -Wall -fsanitize=address,undefined` and passed the test shown.

## Index (grouped by pattern)

| \#  | Problem                                                      | Pattern          | Level |
|-----|--------------------------------------------------------------|------------------|-------|
| 1   | [Rotate Image](#01-rotate-image)                                      | Matrix           | L2    |
| 2   | [Spiral Matrix](#02-spiral-matrix)                                    | Matrix           | L2    |
| 3   | [Set Matrix Zeroes](#03-set-matrix-zeroes)                                | Matrix           | L2    |
| 4   | [Merge Sorted Array](#04-merge-sorted-array)                               | Two pointers     | L1    |
| 5   | [Next Permutation](#05-next-permutation)                                 | Two pointers     | L2    |
| 6   | [Sort Colors (Dutch national flag)](#06-sort-colors-dutch-national-flag)                | Two pointers     | L2    |
| 7   | [Longest Palindromic Substring](#07-longest-palindromic-substring)                    | Two pointers     | L2    |
| 8   | [Palindromic Substrings](#08-palindromic-substrings)                           | Two pointers     | L2    |
| 9   | [Minimum Size Subarray Sum](#09-minimum-size-subarray-sum)                        | Sliding window   | L2    |
| 10  | [Permutation in String](#10-permutation-in-string)                            | Sliding window   | L2    |
| 11  | [Sliding Window Maximum](#11-sliding-window-maximum)                           | Monotonic deque  | L3    |
| 12  | [Search a 2D Matrix](#12-search-a-2d-matrix)                               | Binary search    | L2    |
| 13  | [Majority Element (Boyer–Moore)](#13-majority-element-boyermoore)                   | Hashing          | L1    |
| 14  | [Decode String](#14-decode-string)                                   | Stack            | L2    |
| 15  | [Find the Duplicate Number](#15-find-the-duplicate-number)                       | Linked list      | L2    |
| 16  | [Copy List with Random Pointer](#16-copy-list-with-random-pointer)                   | Linked list      | L2    |
| 17  | [Remove Nth Node From End of List](#17-remove-nth-node-from-end-of-list)                | Linked list      | L2    |
| 18  | [Reverse Nodes in k-Group](#18-reverse-nodes-in-k-group)                        | Linked list      | L3    |
| 19  | [Diameter of Binary Tree](#19-diameter-of-binary-tree)                         | Trees            | L1    |
| 20  | [Construct Binary Tree from Preorder and Inorder](#20-construct-binary-tree-from-preorder-and-inorder) | Trees            | L2    |
| 21  | [Serialize and Deserialize Binary Tree](#21-serialize-and-deserialize-binary-tree)           | Trees            | L3    |
| 22  | [Kth Smallest Element in a BST](#22-kth-smallest-element-in-a-bst)                   | BST              | L2    |
| 23  | [Binary Tree Right Side View](#23-binary-tree-right-side-view)                     | BFS              | L2    |
| 24  | [Clone Graph](#24-clone-graph)                                     | BFS              | L2    |
| 25  | [Pacific Atlantic Water Flow](#25-pacific-atlantic-water-flow)                     | DFS              | L2    |
| 26  | [Course Schedule II](#26-course-schedule-ii)                              | Topological sort | L2    |
| 27  | [Cheapest Flights Within K Stops](#27-cheapest-flights-within-k-stops)                 | Shortest paths   | L2    |
| 28  | [Word Search](#28-word-search)                                     | Backtracking     | L2    |
| 29  | [Combination Sum](#29-combination-sum)                                 | Backtracking     | L2    |
| 30  | [Permutations II](#30-permutations-ii)                                 | Backtracking     | L2    |
| 31  | [N-Queens](#31-n-queens)                                        | Backtracking     | L3    |
| 32  | [Jump Game II](#32-jump-game-ii)                                    | Greedy           | L2    |
| 33  | [Gas Station](#33-gas-station)                                     | Greedy           | L2    |
| 34  | [Non-overlapping Intervals](#34-non-overlapping-intervals)                       | Intervals        | L2    |
| 35  | [Decode Ways](#35-decode-ways)                                     | DP               | L2    |
| 36  | [Unique Paths](#36-unique-paths)                                    | DP               | L2    |
| 37  | [Word Break](#37-word-break)                                      | DP               | L2    |
| 38  | [Longest Increasing Path in a Matrix](#38-longest-increasing-path-in-a-matrix)             | DP               | L3    |
| 39  | [Maximum Product Subarray](#39-maximum-product-subarray)                        | Kadane           | L2    |
| 40  | [Counting Bits](#40-counting-bits)                                   | Bit manipulation | L1    |

Problem statements are on LeetCode (each page links to it). Pattern pages link to the online Knowledge Base. Explanations and code are original.

## 01. Rotate Image

L2 [Matrix](knowledge-base/dsa.md#time-and-space-complexity) · [LeetCode ↗](https://leetcode.com/problems/rotate-image/) · A common in-place matrix warm-up.

### Key idea

Rotating 90° clockwise in place = transpose (swap a\[i\]\[j\] with a\[j\]\[i\]) then reverse each row.

### Steps

1.  Transpose: for i \< j swap
2.  Reverse every row

### C++17 solution

``` cpp
class Solution {
public:
    void rotate(vector<vector<int>>& a) {
        int n = a.size();
        for (int i = 0; i < n; i++) for (int j = i + 1; j < n; j++) swap(a[i][j], a[j][i]);
        for (auto& row : a) reverse(row.begin(), row.end());
    }
};
```

### Test it passed

``` cpp
vector<vector<int>> a{{1,2,3},{4,5,6},{7,8,9}}; Solution().rotate(a); assert((a == vector<vector<int>>{{7,4,1},{8,5,2},{9,6,3}}));
```

### Complexity

O(n²) time, O(1) space

### Traps

- Swapping every (i, j) pair twice by looping j from 0

### Follow-ups

- Rotate anticlockwise (reverse rows first, or transpose then reverse columns).

## 02. Spiral Matrix

L2 [Matrix](knowledge-base/dsa.md#time-and-space-complexity) · [LeetCode ↗](https://leetcode.com/problems/spiral-matrix/) · Tests careful boundary handling.

### Key idea

Keep four boundaries (top, bottom, left, right). Walk right along top, down the right side, left along bottom, up the left side, shrinking each boundary after use; check the boundaries before the last two walks.

### Steps

1.  Loop while top ≤ bottom and left ≤ right
2.  Guard the bottom and left walks with top ≤ bottom and left ≤ right

### C++17 solution

``` cpp
class Solution {
public:
    vector<int> spiralOrder(vector<vector<int>>& m) {
        vector<int> r; int t = 0, b = m.size() - 1, l = 0, rt = m[0].size() - 1;
        while (t <= b && l <= rt) {
            for (int j = l; j <= rt; j++) r.push_back(m[t][j]);
            t++;
            for (int i = t; i <= b; i++) r.push_back(m[i][rt]);
            rt--;
            if (t <= b) { for (int j = rt; j >= l; j--) r.push_back(m[b][j]); b--; }
            if (l <= rt) { for (int i = b; i >= t; i--) r.push_back(m[i][l]); l++; }
        }
        return r;
    }
};
```

### Test it passed

``` cpp
vector<vector<int>> a{{1,2,3},{4,5,6},{7,8,9}}; assert((Solution().spiralOrder(a) == vector<int>{1,2,3,6,9,8,7,4,5}));
vector<vector<int>> b{{1,2,3,4},{5,6,7,8},{9,10,11,12}}; assert((Solution().spiralOrder(b) == vector<int>{1,2,3,4,8,12,11,10,9,5,6,7}));
vector<vector<int>> c{{1},{2},{3}}; assert((Solution().spiralOrder(c) == vector<int>{1,2,3}));
```

### Complexity

O(mn) time, O(1) extra

### Traps

- Missing the guards, so a single row or column is printed twice

### Follow-ups

- Generate an n × n spiral matrix (Spiral Matrix II).

## 03. Set Matrix Zeroes

L2 [Matrix](knowledge-base/dsa.md#time-and-space-complexity) · [LeetCode ↗](https://leetcode.com/problems/set-matrix-zeroes/) · The O(1)-space follow-up is the real question.

### Key idea

Use the first row and first column as markers for which rows and columns to clear, and two flags for whether row 0 and column 0 themselves need clearing. Clear the inner cells first, row 0 and column 0 last.

### Steps

1.  Record zero in row 0 / col 0 flags
2.  Mark a\[i\]\[0\] = a\[0\]\[j\] = 0 for inner zeros
3.  Clear inner cells from marks, then row 0 and col 0

### C++17 solution

``` cpp
class Solution {
public:
    void setZeroes(vector<vector<int>>& a) {
        int m = a.size(), n = a[0].size(); bool r0 = false, c0 = false;
        for (int j = 0; j < n; j++) if (!a[0][j]) r0 = true;
        for (int i = 0; i < m; i++) if (!a[i][0]) c0 = true;
        for (int i = 1; i < m; i++) for (int j = 1; j < n; j++) if (!a[i][j]) a[i][0] = a[0][j] = 0;
        for (int i = 1; i < m; i++) for (int j = 1; j < n; j++) if (!a[i][0] || !a[0][j]) a[i][j] = 0;
        if (r0) for (int j = 0; j < n; j++) a[0][j] = 0;
        if (c0) for (int i = 0; i < m; i++) a[i][0] = 0;
    }
};
```

### Test it passed

``` cpp
vector<vector<int>> a{{1,1,1},{1,0,1},{1,1,1}}; Solution().setZeroes(a); assert((a == vector<vector<int>>{{1,0,1},{0,0,0},{1,0,1}}));
vector<vector<int>> b{{0,1,2,0},{3,4,5,2},{1,3,1,5}}; Solution().setZeroes(b); assert((b == vector<vector<int>>{{0,0,0,0},{0,4,5,0},{0,3,1,0}}));
```

### Complexity

O(mn) time, O(1) extra

### Traps

- Clearing row 0 before reading its marks

### Follow-ups

- Why not just mark cells with -1? (values can be any integer)

## 04. Merge Sorted Array

L1 [Two pointers](knowledge-base/dsa.md#two-pointers) · [LeetCode ↗](https://leetcode.com/problems/merge-sorted-array/) · Easy, but merging from the back is the trick.

### Key idea

Fill a from the end: compare the largest remaining of each array and place it at the back. No element of a is overwritten before it is read.

### Steps

1.  i = m−1, j = n−1, k = m+n−1
2.  while j ≥ 0: take the larger of a\[i\], b\[j\]

### C++17 solution

``` cpp
class Solution {
public:
    void merge(vector<int>& a, int m, vector<int>& b, int n) {
        int i = m - 1, j = n - 1, k = m + n - 1;
        while (j >= 0) a[k--] = (i >= 0 && a[i] > b[j]) ? a[i--] : b[j--];
    }
};
```

### Test it passed

``` cpp
vector<int> a{1,2,3,0,0,0}, b{2,5,6}; Solution().merge(a,3,b,3); assert((a == vector<int>{1,2,2,3,5,6}));
vector<int> c{0}, d{1}; Solution().merge(c,0,d,1); assert((c == vector<int>{1}));
```

### Complexity

O(m + n) time, O(1) space

### Traps

- Merging from the front and overwriting a

### Follow-ups

- Merge without extra space when both arrays are full (gap method).

## 05. Next Permutation

L2 [Two pointers](knowledge-base/dsa.md#two-pointers) · [LeetCode ↗](https://leetcode.com/problems/next-permutation/) · A classic in-place array question.

### Key idea

From the right, find the first i with a\[i\] \< a\[i+1\] (the pivot). If none, reverse the whole array. Otherwise swap a\[i\] with the rightmost element greater than it, then reverse the suffix after i (it was descending).

### Steps

1.  Find pivot i
2.  Find j \> i from the right with a\[j\] \> a\[i\]; swap
3.  Reverse a\[i+1..\]

### C++17 solution

``` cpp
class Solution {
public:
    void nextPermutation(vector<int>& a) {
        int n = a.size(), i = n - 2;
        while (i >= 0 && a[i] >= a[i + 1]) i--;
        if (i >= 0) { int j = n - 1; while (a[j] <= a[i]) j--; swap(a[i], a[j]); }
        reverse(a.begin() + i + 1, a.end());
    }
};
```

### Test it passed

``` cpp
vector<int> a{1,2,3}; Solution().nextPermutation(a); assert((a == vector<int>{1,3,2}));
vector<int> b{3,2,1}; Solution().nextPermutation(b); assert((b == vector<int>{1,2,3}));
vector<int> c{1,1,5}; Solution().nextPermutation(c); assert((c == vector<int>{1,5,1}));
vector<int> d{1,3,2}; Solution().nextPermutation(d); assert((d == vector<int>{2,1,3}));
```

### Complexity

O(n) time, O(1) space

### Traps

- Using \> instead of \>= with duplicates

### Follow-ups

- What does std::next_permutation return?

## 06. Sort Colors (Dutch national flag)

L2 [Two pointers](knowledge-base/dsa.md#two-pointers) · [LeetCode ↗](https://leetcode.com/problems/sort-colors/) · Three-pointer partitioning; asked often as a one-pass follow-up.

### Key idea

Keep low (next place for 0), mid (current), high (next place for 2). A 0 swaps to low and both advance; a 1 just advances mid; a 2 swaps to high and only high moves back, because the swapped-in value is unchecked.

### Steps

1.  low = mid = 0, high = n−1
2.  while mid ≤ high: by a\[mid\] swap and move

### C++17 solution

``` cpp
class Solution {
public:
    void sortColors(vector<int>& a) {
        int lo = 0, mid = 0, hi = (int)a.size() - 1;
        while (mid <= hi) {
            if (a[mid] == 0) swap(a[lo++], a[mid++]);
            else if (a[mid] == 1) mid++;
            else swap(a[mid], a[hi--]);
        }
    }
};
```

### Test it passed

``` cpp
vector<int> a{2,0,2,1,1,0}; Solution().sortColors(a); assert((a == vector<int>{0,0,1,1,2,2}));
vector<int> b{2,0,1}; Solution().sortColors(b); assert((b == vector<int>{0,1,2}));
```

### Complexity

O(n) time, O(1) space

### Traps

- Advancing mid after swapping with high

### Follow-ups

- Counting sort works too: why is one pass better?

## 07. Longest Palindromic Substring

L2 [Two pointers](knowledge-base/dsa.md#two-pointers) · [LeetCode ↗](https://leetcode.com/problems/longest-palindromic-substring/) · Asked everywhere; expand-around-centre beats the DP table in memory.

### Key idea

Every palindrome has a centre: a character (odd length) or a gap between two (even). Expand outwards from each of the 2n−1 centres while the ends match; keep the longest.

### Steps

1.  for each i: expand(i, i) and expand(i, i+1)
2.  Track best start and length

### C++17 solution

``` cpp
class Solution {
public:
    string longestPalindrome(string s) {
        int st = 0, len = 0, n = s.size();
        auto grow = [&](int l, int r) { while (l >= 0 && r < n && s[l] == s[r]) { l--; r++; } if (r - l - 1 > len) { len = r - l - 1; st = l + 1; } };
        for (int i = 0; i < n; i++) { grow(i, i); grow(i, i + 1); }
        return s.substr(st, len);
    }
};
```

### Test it passed

``` text
string r = Solution().longestPalindrome("babad"); assert(r == "bab" || r == "aba"); assert(Solution().longestPalindrome("cbbd") == "bb"); assert(Solution().longestPalindrome("a") == "a");
```

### Complexity

O(n²) time, O(1) space

### Traps

- Forgetting even-length centres

### Follow-ups

- Manacher's algorithm gives O(n): explain the idea.

## 08. Palindromic Substrings

L2 [Two pointers](knowledge-base/dsa.md#two-pointers) · [LeetCode ↗](https://leetcode.com/problems/palindromic-substrings/) · Same centres as the previous problem, counting instead of keeping the best.

### Key idea

Expand from all 2n−1 centres; every successful expansion step is one more palindromic substring.

### Steps

1.  count += expansions from (i, i) and (i, i+1)

### C++17 solution

``` cpp
class Solution {
public:
    int countSubstrings(string s) {
        int n = s.size(), c = 0;
        for (int ctr = 0; ctr < 2 * n - 1; ctr++) {
            int l = ctr / 2, r = l + ctr % 2;
            while (l >= 0 && r < n && s[l] == s[r]) { c++; l--; r++; }
        }
        return c;
    }
};
```

### Test it passed

``` text
assert(Solution().countSubstrings("abc") == 3); assert(Solution().countSubstrings("aaa") == 6);
```

### Complexity

O(n²) time, O(1) space

### Traps

- Double-counting by expanding the same centre twice

### Follow-ups

- Palindrome Partitioning II (minimum cuts).

## 09. Minimum Size Subarray Sum

L2 [Sliding window](knowledge-base/dsa.md#sliding-window) · [LeetCode ↗](https://leetcode.com/problems/minimum-size-subarray-sum/) · The 'shortest window' version of sliding window.

### Key idea

All numbers are positive, so the window sum grows when you expand and shrinks when you move left. Expand right; while the sum is at least target, record the length and shrink from the left.

### Steps

1.  sum += a\[r\]
2.  while sum ≥ target: best = min(best, r−l+1); sum −= a\[l++\]

### C++17 solution

``` cpp
class Solution {
public:
    int minSubArrayLen(int target, vector<int>& a) {
        int best = INT_MAX, l = 0; long long sum = 0;
        for (int r = 0; r < (int)a.size(); r++) {
            sum += a[r];
            while (sum >= target) { best = min(best, r - l + 1); sum -= a[l++]; }
        }
        return best == INT_MAX ? 0 : best;
    }
};
```

### Test it passed

``` cpp
vector<int> a{2,3,1,2,4,3}; assert(Solution().minSubArrayLen(7,a) == 2); vector<int> b{1,4,4}; assert(Solution().minSubArrayLen(4,b) == 1); vector<int> c{1,1,1,1}; assert(Solution().minSubArrayLen(11,c) == 0);
```

### Complexity

O(n) time, O(1) space

### Traps

- Using it with negative numbers (then you need prefix sums + a deque)

### Follow-ups

- Shortest subarray with sum at least K with negatives (LeetCode 862).

## 10. Permutation in String

L2 [Sliding window](knowledge-base/dsa.md#sliding-window) · [LeetCode ↗](https://leetcode.com/problems/permutation-in-string/) · Fixed-size window with character counts.

### Key idea

A permutation of s1 is a window of length \|s1\| in s2 with the same letter counts. Slide a fixed window and compare two 26-count arrays (or track how many letters match).

### Steps

1.  Count s1
2.  Slide window of size \|s1\| over s2, updating counts
3.  Return true when counts are equal

### C++17 solution

``` cpp
class Solution {
public:
    bool checkInclusion(string s1, string s2) {
        if (s1.size() > s2.size()) return false;
        array<int, 26> a{}, b{};
        for (char c : s1) a[c - 'a']++;
        for (int i = 0; i < (int)s2.size(); i++) {
            b[s2[i] - 'a']++;
            if (i >= (int)s1.size()) b[s2[i - s1.size()] - 'a']--;
            if (a == b) return true;
        }
        return false;
    }
};
```

### Test it passed

``` text
assert(Solution().checkInclusion("ab","eidbaooo")); assert(!Solution().checkInclusion("ab","eidboaoo")); assert(!Solution().checkInclusion("abc","ab"));
```

### Complexity

O(26·n) time, O(1) space

### Traps

- Off-by-one when removing the left character

### Follow-ups

- Find All Anagrams in a String (return every start index).

## 11. Sliding Window Maximum

L3 [Monotonic deque](knowledge-base/dsa.md#monotonic-stack) · [LeetCode ↗](https://leetcode.com/problems/sliding-window-maximum/) · Hard favourite; the monotonic deque is the pattern to learn.

### Key idea

Keep indices in a deque whose values decrease from front to back. Drop the front when it leaves the window; before pushing i, pop smaller values from the back (they can never be a maximum again). The front is the window's maximum.

### Steps

1.  pop front if out of window
2.  pop back while a\[back\] ≤ a\[i\]; push i
3.  record a\[front\] once i ≥ k−1

### C++17 solution

``` cpp
class Solution {
public:
    vector<int> maxSlidingWindow(vector<int>& a, int k) {
        deque<int> dq; vector<int> r;
        for (int i = 0; i < (int)a.size(); i++) {
            if (!dq.empty() && dq.front() <= i - k) dq.pop_front();
            while (!dq.empty() && a[dq.back()] <= a[i]) dq.pop_back();
            dq.push_back(i);
            if (i >= k - 1) r.push_back(a[dq.front()]);
        }
        return r;
    }
};
```

### Test it passed

``` cpp
vector<int> a{1,3,-1,-3,5,3,6,7}; assert((Solution().maxSlidingWindow(a,3) == vector<int>{3,3,5,5,6,7})); vector<int> b{1}; assert((Solution().maxSlidingWindow(b,1) == vector<int>{1}));
```

### Complexity

O(n) time, O(k) space

### Traps

- Storing values instead of indices (cannot tell when they leave)

### Follow-ups

- Why is it O(n) with the inner while loop?

## 12. Search a 2D Matrix

L2 [Binary search](knowledge-base/dsa.md#binary-search) · [LeetCode ↗](https://leetcode.com/problems/search-a-2d-matrix/) · Binary search over a matrix treated as one sorted array.

### Key idea

Rows are sorted and each row starts after the previous ends, so index k maps to cell (k / n, k % n). Binary search k over 0..mn−1.

### Steps

1.  lo = 0, hi = mn − 1
2.  v = a\[mid / n\]\[mid % n\]

### C++17 solution

``` cpp
class Solution {
public:
    bool searchMatrix(vector<vector<int>>& a, int t) {
        int m = a.size(), n = a[0].size(), lo = 0, hi = m * n - 1;
        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2, v = a[mid / n][mid % n];
            if (v == t) return true;
            if (v < t) lo = mid + 1; else hi = mid - 1;
        }
        return false;
    }
};
```

### Test it passed

``` cpp
vector<vector<int>> a{{1,3,5,7},{10,11,16,20},{23,30,34,60}}; assert(Solution().searchMatrix(a,3)); assert(!Solution().searchMatrix(a,13)); assert(Solution().searchMatrix(a,60));
```

### Complexity

O(log mn) time

### Traps

- Using m instead of n in the index mapping

### Follow-ups

- Search a 2D Matrix II (rows and columns sorted separately): start at the top-right corner.

## 13. Majority Element (Boyer–Moore)

L1 [Hashing](knowledge-base/dsa.md#hashing-and-frequency-maps) · [LeetCode ↗](https://leetcode.com/problems/majority-element/) · Short, but the O(1)-space voting idea is what interviewers look for.

### Key idea

Pair each majority element with a different element and cancel; the majority survives. Keep a candidate and a count: on count 0 take the current element, add 1 if equal, else subtract 1.

### Steps

1.  cand, cnt = 0
2.  for x: if cnt == 0 cand = x; cnt += (x == cand) ? 1 : −1

### C++17 solution

``` cpp
class Solution {
public:
    int majorityElement(vector<int>& a) {
        int cand = 0, cnt = 0;
        for (int x : a) { if (cnt == 0) cand = x; cnt += (x == cand) ? 1 : -1; }
        return cand;
    }
};
```

### Test it passed

``` cpp
vector<int> a{3,2,3}; assert(Solution().majorityElement(a) == 3); vector<int> b{2,2,1,1,1,2,2}; assert(Solution().majorityElement(b) == 2);
```

### Complexity

O(n) time, O(1) space

### Traps

- Forgetting to verify when a majority is not guaranteed

### Follow-ups

- Majority Element II: all elements appearing more than n/3 times (two candidates, then verify).

## 14. Decode String

L2 [Stack](knowledge-base/dsa.md#stacks-and-queues) · [LeetCode ↗](https://leetcode.com/problems/decode-string/) · Nested brackets: a stack of (string so far, repeat count).

### Key idea

On '\[' push the current string and number, then start fresh. On '\]' pop and append the current string count times to the popped string. Digits build the number; letters extend the current string.

### Steps

1.  digit → k = k·10 + d
2.  '\[' → push (cur, k); reset
3.  '\]' → (prev, k) = pop; cur = prev + cur × k

### C++17 solution

``` cpp
class Solution {
public:
    string decodeString(string s) {
        vector<pair<string, int>> st; string cur; int k = 0;
        for (char ch : s) {
            if (isdigit(ch)) k = k * 10 + (ch - '0');
            else if (ch == '[') { st.push_back({cur, k}); cur.clear(); k = 0; }
            else if (ch == ']') { auto [prev, n] = st.back(); st.pop_back(); string t; while (n--) t += cur; cur = prev + t; }
            else cur += ch;
        }
        return cur;
    }
};
```

### Test it passed

``` text
assert(Solution().decodeString("3[a]2[bc]") == "aaabcbc"); assert(Solution().decodeString("3[a2[c]]") == "accaccacc"); assert(Solution().decodeString("2[abc]3[cd]ef") == "abcabccdcdcdef"); assert(Solution().decodeString("10[a]") == "aaaaaaaaaa");
```

### Complexity

O(output length) time

### Traps

- Reading only single-digit counts

### Follow-ups

- Recursive-descent version; Basic Calculator.

## 15. Find the Duplicate Number

L2 [Linked list](knowledge-base/dsa.md#linked-lists) · [LeetCode ↗](https://leetcode.com/problems/find-the-duplicate-number/) · Floyd's cycle detection on an array; a favourite 'no extra space' twist.

### Key idea

Values are in 1..n with n+1 slots, so treat i → a\[i\] as a linked list. The duplicate is where two pointers point to the same node: the entrance of the cycle. Find it with slow/fast pointers, then restart one from the start.

### Steps

1.  slow = a\[slow\], fast = a\[a\[fast\]\] until they meet
2.  slow = a\[0\]... walk both one step until equal

### C++17 solution

``` cpp
class Solution {
public:
    int findDuplicate(vector<int>& a) {
        int s = a[0], f = a[0];
        do { s = a[s]; f = a[a[f]]; } while (s != f);
        s = a[0];
        while (s != f) { s = a[s]; f = a[f]; }
        return s;
    }
};
```

### Test it passed

``` cpp
vector<int> a{1,3,4,2,2}; assert(Solution().findDuplicate(a) == 2); vector<int> b{3,1,3,4,2}; assert(Solution().findDuplicate(b) == 3); vector<int> c{3,3,3,3,3}; assert(Solution().findDuplicate(c) == 3);
```

### Complexity

O(n) time, O(1) space, array unmodified

### Traps

- Sorting or marking (modifies the array, which the problem forbids)

### Follow-ups

- Prove why the meeting point leads to the cycle entrance.

## 16. Copy List with Random Pointer

L2 [Linked list](knowledge-base/dsa.md#linked-lists) · [LeetCode ↗](https://leetcode.com/problems/copy-list-with-random-pointer/) · Deep copy; the O(1)-space weaving trick is the follow-up.

### Key idea

Weave a copy after every node (A → A' → B → B'). Then A'.random = A.random-\>next. Finally unweave the two lists.

### Steps

1.  insert copies
2.  set random of copies
3.  split lists

### C++17 solution

``` cpp
struct Node { int val; Node* next = nullptr; Node* random = nullptr; Node(int v) : val(v) {} };
class Solution {
public:
    Node* copyRandomList(Node* h) {
        for (Node* p = h; p; p = p->next->next) { Node* c = new Node(p->val); c->next = p->next; p->next = c; }
        for (Node* p = h; p; p = p->next->next) if (p->random) p->next->random = p->random->next;
        Node dummy(0); Node* t = &dummy;
        for (Node* p = h; p; p = p->next) { t->next = p->next; t = t->next; p->next = t->next; }
        return dummy.next;
    }
};
```

### Test it passed

``` text
Node *a = new Node(7), *b = new Node(13), *c = new Node(11); a->next = b; b->next = c; b->random = a; c->random = c;
Node* r = Solution().copyRandomList(a); assert(r != a && r->val == 7 && r->next->val == 13 && r->next->random == r && r->next->next->random == r->next->next && !r->random);
assert(a->next == b && b->next == c && !c->next); assert(Solution().copyRandomList(nullptr) == nullptr);
```

### Complexity

O(n) time, O(1) extra

### Traps

- Not restoring the original list

### Follow-ups

- Hash-map version: simpler, O(n) extra space.

## 17. Remove Nth Node From End of List

L2 [Linked list](knowledge-base/dsa.md#linked-lists) · [LeetCode ↗](https://leetcode.com/problems/remove-nth-node-from-end-of-list/) · Two pointers with a gap of n.

### Key idea

Move a fast pointer n steps ahead of a slow one (both starting at a dummy). Move both until fast reaches the last node; slow-\>next is the node to remove.

### Steps

1.  dummy → head
2.  fast moves n steps
3.  move both until fast-\>next is null; slow-\>next = slow-\>next-\>next

### C++17 solution

``` cpp
class Solution {
public:
    ListNode* removeNthFromEnd(ListNode* head, int n) {
        ListNode dummy(0, head); ListNode *f = &dummy, *s = &dummy;
        for (int i = 0; i < n; i++) f = f->next;
        while (f->next) { f = f->next; s = s->next; }
        s->next = s->next->next; return dummy.next;
    }
};
```

### Test it passed

``` cpp
assert((tov(Solution().removeNthFromEnd(mk({1,2,3,4,5}),2)) == vector<int>{1,2,3,5})); assert(tov(Solution().removeNthFromEnd(mk({1}),1)).empty()); assert((tov(Solution().removeNthFromEnd(mk({1,2}),2)) == vector<int>{2}));
```

### Complexity

O(n) time, O(1) space, one pass

### Traps

- No dummy node, so removing the head breaks

### Follow-ups

- Delete the middle node of a linked list.

## 18. Reverse Nodes in k-Group

L3 [Linked list](knowledge-base/dsa.md#linked-lists) · [LeetCode ↗](https://leetcode.com/problems/reverse-nodes-in-k-group/) · Hard pointer manipulation with a dummy node.

### Key idea

Use a dummy head. For each group: check k nodes exist; reverse them by moving each next node to the front of the group; then advance prev to the group's new tail.

### Steps

1.  count k nodes ahead; stop if fewer
2.  k−1 times: move cur-\>next to after prev
3.  prev = cur (old first node, now last)

### C++17 solution

``` cpp
class Solution {
public:
    ListNode* reverseKGroup(ListNode* head, int k) {
        ListNode dummy(0, head); ListNode* prev = &dummy;
        while (true) {
            ListNode* t = prev; for (int i = 0; i < k && t; i++) t = t->next;
            if (!t) break;
            ListNode* cur = prev->next;
            for (int i = 1; i < k; i++) { ListNode* nx = cur->next; cur->next = nx->next; nx->next = prev->next; prev->next = nx; }
            prev = cur;
        }
        return dummy.next;
    }
};
```

### Test it passed

``` cpp
assert((tov(Solution().reverseKGroup(mk({1,2,3,4,5}),2)) == vector<int>{2,1,4,3,5})); assert((tov(Solution().reverseKGroup(mk({1,2,3,4,5}),3)) == vector<int>{3,2,1,4,5})); assert((tov(Solution().reverseKGroup(mk({1,2}),1)) == vector<int>{1,2}));
```

### Complexity

O(n) time, O(1) space

### Traps

- Reversing a final group that has fewer than k nodes

### Follow-ups

- Reverse Linked List II (reverse between positions m and n).

## 19. Diameter of Binary Tree

L1 [Trees](knowledge-base/dsa.md#binary-trees) · [LeetCode ↗](https://leetcode.com/problems/diameter-of-binary-tree/) · Height recursion that updates a global answer.

### Key idea

The longest path through a node = height(left) + height(right). Compute heights bottom-up and keep the best sum.

### Steps

1.  h(node) = 1 + max(h(l), h(r))
2.  best = max(best, h(l) + h(r))

### C++17 solution

``` cpp
class Solution {
    int best = 0;
    int h(TreeNode* r) { if (!r) return 0; int a = h(r->left), b = h(r->right); best = max(best, a + b); return 1 + max(a, b); }
public:
    int diameterOfBinaryTree(TreeNode* root) { h(root); return best; }
};
```

### Test it passed

``` text
assert(Solution().diameterOfBinaryTree(tree({"1","2","3","4","5"})) == 3); assert(Solution().diameterOfBinaryTree(tree({"1","2"})) == 1);
```

### Complexity

O(n) time, O(h) space

### Traps

- Assuming the path passes through the root

### Follow-ups

- Binary Tree Maximum Path Sum (same shape with values).

## 20. Construct Binary Tree from Preorder and Inorder

L2 [Trees](knowledge-base/dsa.md#binary-trees) · [LeetCode ↗](https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/) · Tests understanding of traversals.

### Key idea

The first preorder value is the root. Its position in inorder splits left and right subtrees. Use a hash map from value to inorder index so each split is O(1).

### Steps

1.  map value → inorder index
2.  build(lo, hi): root = pre\[p++\]; left = build(lo, idx−1); right = build(idx+1, hi)

### C++17 solution

``` cpp
class Solution {
    unordered_map<int, int> pos; int p = 0;
    TreeNode* build(vector<int>& pre, int lo, int hi) {
        if (lo > hi) return nullptr;
        TreeNode* r = new TreeNode(pre[p++]); int m = pos[r->val];
        r->left = build(pre, lo, m - 1); r->right = build(pre, m + 1, hi); return r;
    }
public:
    TreeNode* buildTree(vector<int>& pre, vector<int>& in) { for (int i = 0; i < (int)in.size(); i++) pos[in[i]] = i; return build(pre, 0, in.size() - 1); }
};
```

### Test it passed

``` cpp
vector<int> pre{3,9,20,15,7}, in{9,3,15,20,7}; TreeNode* r = Solution().buildTree(pre,in);
assert(r->val == 3 && r->left->val == 9 && r->right->val == 20 && r->right->left->val == 15 && r->right->right->val == 7 && !r->left->left);
```

### Complexity

O(n) time, O(n) space

### Traps

- Building the left subtree after the right (preorder order matters)

### Follow-ups

- From inorder and postorder: build right first.

## 21. Serialize and Deserialize Binary Tree

L3 [Trees](knowledge-base/dsa.md#binary-trees) · [LeetCode ↗](https://leetcode.com/problems/serialize-and-deserialize-binary-tree/) · A Hard question that mixes traversal and design.

### Key idea

Preorder with a marker for null ('#') describes the tree uniquely. Serialize recursively; deserialize by reading tokens in the same order.

### Steps

1.  ser: val, then left, then right; '#' for null
2.  de: read token; '#' → null; else node, left = de(), right = de()

### C++17 solution

``` cpp
class Codec {
    void ser(TreeNode* r, string& s) { if (!r) { s += "# "; return; } s += to_string(r->val) + " "; ser(r->left, s); ser(r->right, s); }
    TreeNode* de(istringstream& in) { string t; in >> t; if (t == "#") return nullptr; TreeNode* r = new TreeNode(stoi(t)); r->left = de(in); r->right = de(in); return r; }
public:
    string serialize(TreeNode* root) { string s; ser(root, s); return s; }
    TreeNode* deserialize(string data) { istringstream in(data); return de(in); }
};
```

### Test it passed

``` text
Codec c; TreeNode* r = tree({"1","2","3","null","null","4","5"}); string s = c.serialize(r); assert(s == "1 2 # # 3 4 # # 5 # # ");
assert(c.serialize(c.deserialize(s)) == s); assert(c.deserialize(c.serialize(nullptr)) == nullptr); assert(c.serialize(tree({"-7"})) == "-7 # # ");
```

### Complexity

O(n) time and space

### Traps

- Leaving out null markers (preorder alone is ambiguous)

### Follow-ups

- Serialize a BST more compactly (no null markers needed).

## 22. Kth Smallest Element in a BST

L2 [BST](knowledge-base/dsa.md#binary-search-trees) · [LeetCode ↗](https://leetcode.com/problems/kth-smallest-element-in-a-bst/) · Inorder traversal of a BST is sorted.

### Key idea

An inorder walk visits a BST in ascending order. Walk iteratively with a stack and stop at the k-th node.

### Steps

1.  push left spine
2.  pop, k−−, if k == 0 return
3.  go right

### C++17 solution

``` cpp
class Solution {
public:
    int kthSmallest(TreeNode* root, int k) {
        stack<TreeNode*> st; TreeNode* cur = root;
        while (cur || !st.empty()) {
            while (cur) { st.push(cur); cur = cur->left; }
            cur = st.top(); st.pop();
            if (--k == 0) return cur->val;
            cur = cur->right;
        }
        return -1;
    }
};
```

### Test it passed

``` text
assert(Solution().kthSmallest(tree({"3","1","4","null","2"}),1) == 1); assert(Solution().kthSmallest(tree({"5","3","6","2","4","null","null","1"}),3) == 3);
```

### Complexity

O(h + k) time, O(h) space

### Traps

- Collecting the whole inorder list (O(n) memory)

### Follow-ups

- If the tree changes often: store subtree sizes in each node.

## 23. Binary Tree Right Side View

L2 [BFS](knowledge-base/dsa.md#bfs-and-graph-basics) · [LeetCode ↗](https://leetcode.com/problems/binary-tree-right-side-view/) · A level-order variant.

### Key idea

Do a level-order traversal and record the last node of every level.

### Steps

1.  queue; for each level of size s, the s-th popped node is visible

### C++17 solution

``` cpp
class Solution {
public:
    vector<int> rightSideView(TreeNode* root) {
        vector<int> r; if (!root) return r; queue<TreeNode*> q; q.push(root);
        while (!q.empty()) {
            int s = q.size();
            for (int i = 0; i < s; i++) { TreeNode* n = q.front(); q.pop(); if (i == s - 1) r.push_back(n->val); if (n->left) q.push(n->left); if (n->right) q.push(n->right); }
        }
        return r;
    }
};
```

### Test it passed

``` cpp
assert((Solution().rightSideView(tree({"1","2","3","null","5","null","4"})) == vector<int>{1,3,4})); assert((Solution().rightSideView(tree({"1","2"})) == vector<int>{1,2})); assert(Solution().rightSideView(nullptr).empty());
```

### Complexity

O(n) time, O(width) space

### Traps

- Only following right children (misses a deeper left node)

### Follow-ups

- DFS version: visit right first, record when depth == result size.

## 24. Clone Graph

L2 [BFS](knowledge-base/dsa.md#bfs-and-graph-basics) · [LeetCode ↗](https://leetcode.com/problems/clone-graph/) · Deep copy with a visited map.

### Key idea

Map each original node to its copy. BFS from the start; on seeing a neighbour without a copy, create it and enqueue it; always link the copies.

### Steps

1.  copy\[start\] = new node
2.  for each popped u, for v in u's neighbours: create copy if missing, link copy\[u\] → copy\[v\]

### C++17 solution

``` cpp
struct Node { int val; vector<Node*> neighbors; Node(int v) : val(v) {} };
class Solution {
public:
    Node* cloneGraph(Node* s) {
        if (!s) return nullptr;
        unordered_map<Node*, Node*> cp; cp[s] = new Node(s->val); queue<Node*> q; q.push(s);
        while (!q.empty()) {
            Node* u = q.front(); q.pop();
            for (Node* v : u->neighbors) { if (!cp.count(v)) { cp[v] = new Node(v->val); q.push(v); } cp[u]->neighbors.push_back(cp[v]); }
        }
        return cp[s];
    }
};
```

### Test it passed

``` cpp
vector<Node*> n; for (int i = 1; i <= 4; i++) n.push_back(new Node(i));
n[0]->neighbors = {n[1], n[3]}; n[1]->neighbors = {n[0], n[2]}; n[2]->neighbors = {n[1], n[3]}; n[3]->neighbors = {n[0], n[2]};
Node* c = Solution().cloneGraph(n[0]); assert(c != n[0] && c->val == 1 && c->neighbors.size() == 2 && c->neighbors[0]->val == 2 && c->neighbors[1]->val == 4);
assert(c->neighbors[0]->neighbors[0] == c && c->neighbors[0] != n[1]); assert(Solution().cloneGraph(nullptr) == nullptr);
```

### Complexity

O(V + E) time and space

### Traps

- Creating a second copy of a node already seen (no map)

### Follow-ups

- Copy List with Random Pointer uses the same map idea.

## 25. Pacific Atlantic Water Flow

L2 [DFS](knowledge-base/dsa.md#dfs-components-and-cycles) · [LeetCode ↗](https://leetcode.com/problems/pacific-atlantic-water-flow/) · Reverse the direction: flow uphill from the oceans.

### Key idea

Instead of checking every cell, start from each ocean's border and move to neighbours that are at least as high. Cells reached from both oceans are the answer.

### Steps

1.  DFS from top row + left column → pac
2.  DFS from bottom row + right column → atl
3.  answer = cells in both

### C++17 solution

``` cpp
class Solution {
    int m, n;
    void dfs(vector<vector<int>>& h, vector<vector<bool>>& v, int r, int c) {
        v[r][c] = true; int d[] = {1, 0, -1, 0, 1};
        for (int k = 0; k < 4; k++) { int a = r + d[k], b = c + d[k + 1]; if (a >= 0 && b >= 0 && a < m && b < n && !v[a][b] && h[a][b] >= h[r][c]) dfs(h, v, a, b); }
    }
public:
    vector<vector<int>> pacificAtlantic(vector<vector<int>>& h) {
        m = h.size(); n = h[0].size(); vector<vector<bool>> p(m, vector<bool>(n)), a(m, vector<bool>(n));
        for (int i = 0; i < m; i++) { dfs(h, p, i, 0); dfs(h, a, i, n - 1); }
        for (int j = 0; j < n; j++) { dfs(h, p, 0, j); dfs(h, a, m - 1, j); }
        vector<vector<int>> r;
        for (int i = 0; i < m; i++) for (int j = 0; j < n; j++) if (p[i][j] && a[i][j]) r.push_back({i, j});
        return r;
    }
};
```

### Test it passed

``` cpp
vector<vector<int>> h{{1,2,2,3,5},{3,2,3,4,4},{2,4,5,3,1},{6,7,1,4,5},{5,1,1,2,4}};
assert((Solution().pacificAtlantic(h) == vector<vector<int>>{{0,4},{1,3},{1,4},{2,2},{3,0},{3,1},{4,0}}));
```

### Complexity

O(mn) time and space

### Traps

- Running a search from every cell (O((mn)²))

### Follow-ups

- Same trick: Surrounded Regions, Number of Enclaves.

## 26. Course Schedule II

L2 [Topological sort](knowledge-base/dsa.md#topological-sort) · [LeetCode ↗](https://leetcode.com/problems/course-schedule-ii/) · Return the actual order (Kahn's algorithm).

### Key idea

Kahn's algorithm: push all courses with in-degree 0; pop one, add it to the order and lower its neighbours' in-degree. If the order has fewer than n courses, there is a cycle.

### Steps

1.  edge b → a for \[a, b\]
2.  queue of in-degree 0
3.  order.size() \< n → return {}

### C++17 solution

``` cpp
class Solution {
public:
    vector<int> findOrder(int n, vector<vector<int>>& pre) {
        vector<vector<int>> g(n); vector<int> in(n), ord;
        for (auto& e : pre) { g[e[1]].push_back(e[0]); in[e[0]]++; }
        queue<int> q; for (int i = 0; i < n; i++) if (!in[i]) q.push(i);
        while (!q.empty()) { int u = q.front(); q.pop(); ord.push_back(u); for (int v : g[u]) if (--in[v] == 0) q.push(v); }
        return (int)ord.size() == n ? ord : vector<int>{};
    }
};
```

### Test it passed

``` cpp
vector<vector<int>> p{{1,0},{2,0},{3,1},{3,2}}; auto o = Solution().findOrder(4,p); assert(o.size() == 4 && o[0] == 0 && o[3] == 3);
vector<vector<int>> cyc{{1,0},{0,1}}; assert(Solution().findOrder(2,cyc).empty()); vector<vector<int>> none; assert(Solution().findOrder(1,none).size() == 1);
```

### Complexity

O(V + E) time and space

### Traps

- Reversing the edge direction

### Follow-ups

- Alien Dictionary (build the graph from word order).

## 27. Cheapest Flights Within K Stops

L2 [Shortest paths](knowledge-base/dsa.md#dijkstra-and-shortest-paths) · [LeetCode ↗](https://leetcode.com/problems/cheapest-flights-within-k-stops/) · Shortest path with a limit on edges: Bellman–Ford for k+1 rounds.

### Key idea

Run Bellman–Ford for k+1 rounds (k stops = k+1 flights). Relax from a copy of the previous round's costs so one round uses only one more flight.

### Steps

1.  dist\[src\] = 0
2.  repeat k+1 times: nd = dist; for each flight relax nd\[v\] from dist\[u\]; dist = nd

### C++17 solution

``` cpp
class Solution {
public:
    int findCheapestPrice(int n, vector<vector<int>>& f, int src, int dst, int k) {
        const int INF = 1e9; vector<int> d(n, INF); d[src] = 0;
        for (int i = 0; i <= k; i++) {
            vector<int> nd = d;
            for (auto& e : f) if (d[e[0]] != INF && d[e[0]] + e[2] < nd[e[1]]) nd[e[1]] = d[e[0]] + e[2];
            d = nd;
        }
        return d[dst] == INF ? -1 : d[dst];
    }
};
```

### Test it passed

``` cpp
vector<vector<int>> f{{0,1,100},{1,2,100},{2,0,100},{1,3,600},{2,3,200}}; assert(Solution().findCheapestPrice(4,f,0,3,1) == 700);
vector<vector<int>> g{{0,1,100},{1,2,100},{0,2,500}}; assert(Solution().findCheapestPrice(3,g,0,2,1) == 200); assert(Solution().findCheapestPrice(3,g,0,2,0) == 500);
```

### Complexity

O(k · E) time, O(n) space

### Traps

- Relaxing in place (one round can chain several flights)
- Plain Dijkstra ignores the stop limit

### Follow-ups

- Dijkstra with (cost, node, stops) states: when is it faster?

## 28. Word Search

L2 [Backtracking](knowledge-base/dsa.md#recursion-and-backtracking) · [LeetCode ↗](https://leetcode.com/problems/word-search/) · Grid backtracking; tests marking and unmarking visited cells.

### Key idea

Start a DFS from every cell that matches the first letter. Mark the cell as used, recurse into 4 neighbours for the next letter, and unmark on the way back.

### Steps

1.  dfs(r, c, i): bounds and letter check
2.  mark, try 4 directions, unmark

### C++17 solution

``` cpp
class Solution {
    bool dfs(vector<vector<char>>& g, const string& w, int r, int c, int i) {
        if (i == (int)w.size()) return true;
        if (r < 0 || c < 0 || r >= (int)g.size() || c >= (int)g[0].size() || g[r][c] != w[i]) return false;
        char t = g[r][c]; g[r][c] = '#';
        bool ok = dfs(g, w, r + 1, c, i + 1) || dfs(g, w, r - 1, c, i + 1) || dfs(g, w, r, c + 1, i + 1) || dfs(g, w, r, c - 1, i + 1);
        g[r][c] = t; return ok;
    }
public:
    bool exist(vector<vector<char>>& g, string w) {
        for (int r = 0; r < (int)g.size(); r++) for (int c = 0; c < (int)g[0].size(); c++) if (dfs(g, w, r, c, 0)) return true;
        return false;
    }
};
```

### Test it passed

``` cpp
vector<vector<char>> g{{'A','B','C','E'},{'S','F','C','S'},{'A','D','E','E'}}; assert(Solution().exist(g,"ABCCED")); assert(Solution().exist(g,"SEE")); assert(!Solution().exist(g,"ABCB"));
```

### Complexity

O(mn · 3^L) time, O(L) recursion

### Traps

- Forgetting to unmark, so later paths cannot reuse the cell

### Follow-ups

- Word Search II: many words at once (trie + DFS).

## 29. Combination Sum

L2 [Backtracking](knowledge-base/dsa.md#recursion-and-backtracking) · [LeetCode ↗](https://leetcode.com/problems/combination-sum/) · The standard 'choose with repetition' backtracking.

### Key idea

Each candidate can be used many times. Recurse with the remaining target, starting from the current index (not i+1) so the same number can repeat, and only moving forward so combinations aren't repeated in different orders.

### Steps

1.  go(start, remaining)
2.  for i ≥ start with c\[i\] ≤ remaining: pick, go(i, remaining − c\[i\]), unpick

### C++17 solution

``` cpp
class Solution {
    vector<vector<int>> res; vector<int> cur;
    void go(vector<int>& c, int s, int rem) {
        if (rem == 0) { res.push_back(cur); return; }
        for (int i = s; i < (int)c.size() && c[i] <= rem; i++) { cur.push_back(c[i]); go(c, i, rem - c[i]); cur.pop_back(); }
    }
public:
    vector<vector<int>> combinationSum(vector<int>& c, int t) { sort(c.begin(), c.end()); go(c, 0, t); return res; }
};
```

### Test it passed

``` cpp
vector<int> a{2,3,6,7}; auto r = Solution().combinationSum(a,7); assert((r == vector<vector<int>>{{2,2,3},{7}}));
vector<int> b{2,3,5}; assert(Solution().combinationSum(b,8).size() == 3);
```

### Complexity

Exponential in the target; recursion depth ≤ target / min

### Traps

- Starting the loop at 0 (duplicate combinations in different orders)

### Follow-ups

- Combination Sum II: each number once, with duplicates in the input.

## 30. Permutations II

L2 [Backtracking](knowledge-base/dsa.md#recursion-and-backtracking) · [LeetCode ↗](https://leetcode.com/problems/permutations-ii/) · Permutations with duplicate values: the skip rule is the test.

### Key idea

Sort, then build permutations with a used\[\] array. Skip a value if it equals the previous value and the previous copy is not currently used: that order was already generated.

### Steps

1.  sort
2.  skip i if used\[i\] or (i \> 0 and a\[i\] == a\[i−1\] and !used\[i−1\])

### C++17 solution

``` cpp
class Solution {
    vector<vector<int>> res; vector<int> cur; vector<bool> used;
    void go(vector<int>& a) {
        if (cur.size() == a.size()) { res.push_back(cur); return; }
        for (int i = 0; i < (int)a.size(); i++) {
            if (used[i] || (i > 0 && a[i] == a[i - 1] && !used[i - 1])) continue;
            used[i] = true; cur.push_back(a[i]); go(a); cur.pop_back(); used[i] = false;
        }
    }
public:
    vector<vector<int>> permuteUnique(vector<int>& a) { sort(a.begin(), a.end()); used.assign(a.size(), false); go(a); return res; }
};
```

### Test it passed

``` cpp
vector<int> a{1,1,2}; assert((Solution().permuteUnique(a) == vector<vector<int>>{{1,1,2},{1,2,1},{2,1,1}})); vector<int> b{1,2,3}; assert(Solution().permuteUnique(b).size() == 6);
```

### Complexity

O(n · n!) time, O(n) space

### Traps

- Using a set of results to dedupe (works, but slow and noticed)

### Follow-ups

- Why does the !used\[i−1\] condition work?

## 31. N-Queens

L3 [Backtracking](knowledge-base/dsa.md#recursion-and-backtracking) · [LeetCode ↗](https://leetcode.com/problems/n-queens/) · The classic Hard backtracking problem.

### Key idea

Place one queen per row. A column c is safe in row r if no queen uses column c, diagonal r−c, or anti-diagonal r+c. Track those three in boolean arrays for O(1) checks.

### Steps

1.  go(row): if row == n record the board
2.  for each col safe: place, mark three arrays, recurse, unmark

### C++17 solution

``` cpp
class Solution {
    vector<vector<string>> res; vector<string> b; vector<bool> col, d1, d2; int n;
    void go(int r) {
        if (r == n) { res.push_back(b); return; }
        for (int c = 0; c < n; c++) {
            if (col[c] || d1[r - c + n - 1] || d2[r + c]) continue;
            col[c] = d1[r - c + n - 1] = d2[r + c] = true; b[r][c] = 'Q';
            go(r + 1);
            col[c] = d1[r - c + n - 1] = d2[r + c] = false; b[r][c] = '.';
        }
    }
public:
    vector<vector<string>> solveNQueens(int N) { n = N; b.assign(n, string(n, '.')); col.assign(n, false); d1.assign(2 * n, false); d2.assign(2 * n, false); go(0); return res; }
};
```

### Test it passed

``` text
assert(Solution().solveNQueens(4).size() == 2); assert(Solution().solveNQueens(1).size() == 1); assert(Solution().solveNQueens(8).size() == 92);
```

### Complexity

O(n!) time, O(n) space

### Traps

- Wrong diagonal index (r − c can be negative: offset by n − 1)

### Follow-ups

- Count only (N-Queens II); do it with bitmasks.

## 32. Jump Game II

L2 [Greedy](knowledge-base/dsa.md#greedy-algorithms) · [LeetCode ↗](https://leetcode.com/problems/jump-game-ii/) · BFS by levels, done greedily in O(n).

### Key idea

Think of jumps as BFS levels. Within the current level (up to \`end\`), track the farthest index reachable. When you reach \`end\`, take one jump and set end = farthest.

### Steps

1.  far = max(far, i + a\[i\])
2.  if i == end: jumps++, end = far

### C++17 solution

``` cpp
class Solution {
public:
    int jump(vector<int>& a) {
        int jumps = 0, end = 0, far = 0;
        for (int i = 0; i + 1 < (int)a.size(); i++) { far = max(far, i + a[i]); if (i == end) { jumps++; end = far; } }
        return jumps;
    }
};
```

### Test it passed

``` cpp
vector<int> a{2,3,1,1,4}; assert(Solution().jump(a) == 2); vector<int> b{2,3,0,1,4}; assert(Solution().jump(b) == 2); vector<int> c{0}; assert(Solution().jump(c) == 0);
```

### Complexity

O(n) time, O(1) space

### Traps

- Looping to the last index (adds an extra jump)

### Follow-ups

- Jump Game III / IV (BFS on indices).

## 33. Gas Station

L2 [Greedy](knowledge-base/dsa.md#greedy-algorithms) · [LeetCode ↗](https://leetcode.com/problems/gas-station/) · A greedy proof question.

### Key idea

If total gas \< total cost, no answer. Otherwise run once: whenever the tank goes negative at i, no start between the old start and i works, so restart at i+1.

### Steps

1.  total += g − c; tank += g − c
2.  if tank \< 0: start = i + 1, tank = 0

### C++17 solution

``` cpp
class Solution {
public:
    int canCompleteCircuit(vector<int>& g, vector<int>& c) {
        int total = 0, tank = 0, start = 0;
        for (int i = 0; i < (int)g.size(); i++) { total += g[i] - c[i]; tank += g[i] - c[i]; if (tank < 0) { start = i + 1; tank = 0; } }
        return total < 0 ? -1 : start;
    }
};
```

### Test it passed

``` cpp
vector<int> g{1,2,3,4,5}, c{3,4,5,1,2}; assert(Solution().canCompleteCircuit(g,c) == 3); vector<int> g2{2,3,4}, c2{3,4,3}; assert(Solution().canCompleteCircuit(g2,c2) == -1);
```

### Complexity

O(n) time, O(1) space

### Traps

- Trying every start (O(n²))

### Follow-ups

- Prove why skipping to i+1 is safe.

## 34. Non-overlapping Intervals

L2 [Intervals](knowledge-base/dsa.md#interval-problems) · [LeetCode ↗](https://leetcode.com/problems/non-overlapping-intervals/) · Interval scheduling: keep the earliest-ending ones.

### Key idea

To keep the most intervals, sort by end and greedily keep an interval when it starts at or after the last kept end. Removals = n − kept.

### Steps

1.  sort by end
2.  keep if start ≥ lastEnd

### C++17 solution

``` cpp
class Solution {
public:
    int eraseOverlapIntervals(vector<vector<int>>& a) {
        sort(a.begin(), a.end(), [](auto& x, auto& y) { return x[1] < y[1]; });
        int kept = 0; long long end = LLONG_MIN;
        for (auto& v : a) if (v[0] >= end) { kept++; end = v[1]; }
        return a.size() - kept;
    }
};
```

### Test it passed

``` cpp
vector<vector<int>> a{{1,2},{2,3},{3,4},{1,3}}; assert(Solution().eraseOverlapIntervals(a) == 1); vector<vector<int>> b{{1,2},{1,2},{1,2}}; assert(Solution().eraseOverlapIntervals(b) == 2);
vector<vector<int>> c{{1,2},{2,3}}; assert(Solution().eraseOverlapIntervals(c) == 0);
```

### Complexity

O(n log n) time, O(1) extra

### Traps

- Sorting by start and keeping the first

### Follow-ups

- Minimum Number of Arrows to Burst Balloons; Meeting Rooms II (count overlap with a min-heap).

## 35. Decode Ways

L2 [DP](knowledge-base/dsa.md#dynamic-programming) · [LeetCode ↗](https://leetcode.com/problems/decode-ways/) · A 1-D DP with tricky zeros.

### Key idea

dp\[i\] = ways to decode the first i characters. The last char alone works if it isn't '0' (add dp\[i−1\]); the last two work if they form 10..26 (add dp\[i−2\]).

### Steps

1.  dp\[0\] = 1
2.  single digit 1..9 → += dp\[i−1\]
3.  two digits 10..26 → += dp\[i−2\]

### C++17 solution

``` cpp
class Solution {
public:
    int numDecodings(string s) {
        int n = s.size(); vector<int> dp(n + 1, 0); dp[0] = 1;
        for (int i = 1; i <= n; i++) {
            if (s[i - 1] != '0') dp[i] += dp[i - 1];
            if (i >= 2) { int v = (s[i - 2] - '0') * 10 + (s[i - 1] - '0'); if (v >= 10 && v <= 26) dp[i] += dp[i - 2]; }
        }
        return dp[n];
    }
};
```

### Test it passed

``` text
assert(Solution().numDecodings("12") == 2); assert(Solution().numDecodings("226") == 3); assert(Solution().numDecodings("06") == 0); assert(Solution().numDecodings("10") == 1);
```

### Complexity

O(n) time, O(n) space (O(1) with two variables)

### Traps

- Treating '06' as valid

### Follow-ups

- Decode Ways II with '\*' wildcards.

## 36. Unique Paths

L2 [DP](knowledge-base/dsa.md#dynamic-programming) · [LeetCode ↗](https://leetcode.com/problems/unique-paths/) · The first grid DP; often followed by obstacles.

### Key idea

You reach a cell only from above or from the left, so dp\[i\]\[j\] = dp\[i−1\]\[j\] + dp\[i\]\[j−1\]. One row is enough: dp\[j\] += dp\[j−1\].

### Steps

1.  dp = row of 1s
2.  for each next row: dp\[j\] += dp\[j−1\]

### C++17 solution

``` cpp
class Solution {
public:
    int uniquePaths(int m, int n) {
        vector<long long> dp(n, 1);
        for (int i = 1; i < m; i++) for (int j = 1; j < n; j++) dp[j] += dp[j - 1];
        return dp[n - 1];
    }
};
```

### Test it passed

``` text
assert(Solution().uniquePaths(3,7) == 28); assert(Solution().uniquePaths(3,2) == 3); assert(Solution().uniquePaths(1,1) == 1);
```

### Complexity

O(mn) time, O(n) space

### Traps

- Using int for big grids

### Follow-ups

- With obstacles (Unique Paths II).
- Closed form: C(m+n−2, m−1).

## 37. Word Break

L2 [DP](knowledge-base/dsa.md#dynamic-programming) · [LeetCode ↗](https://leetcode.com/problems/word-break/) · The standard 'can the prefix be built' DP.

### Key idea

dp\[i\] is true if s\[0..i) can be split into dictionary words. dp\[i\] is true if some j \< i has dp\[j\] true and s\[j..i) in the dictionary.

### Steps

1.  dp\[0\] = true; put words in a hash set
2.  for i, for j \< i: if dp\[j\] and s.substr(j, i−j) in set → dp\[i\] = true

### C++17 solution

``` cpp
class Solution {
public:
    bool wordBreak(string s, vector<string>& words) {
        unordered_set<string> d(words.begin(), words.end()); int n = s.size();
        vector<bool> dp(n + 1, false); dp[0] = true;
        for (int i = 1; i <= n; i++) for (int j = 0; j < i && !dp[i]; j++) if (dp[j] && d.count(s.substr(j, i - j))) dp[i] = true;
        return dp[n];
    }
};
```

### Test it passed

``` cpp
vector<string> a{"leet","code"}; assert(Solution().wordBreak("leetcode",a)); vector<string> b{"apple","pen"}; assert(Solution().wordBreak("applepenapple",b));
vector<string> c{"cats","dog","sand","and","cat"}; assert(!Solution().wordBreak("catsandog",c));
```

### Complexity

O(n² · L) time, O(n) space

### Traps

- Greedy longest-match (fails on 'catsandog'-style inputs)

### Follow-ups

- Word Break II: return all sentences (DP + backtracking with memo).

## 38. Longest Increasing Path in a Matrix

L3 [DP](knowledge-base/dsa.md#dynamic-programming) · [LeetCode ↗](https://leetcode.com/problems/longest-increasing-path-in-a-matrix/) · DFS with memo on a DAG.

### Key idea

Strictly increasing moves can never cycle, so the grid is a DAG. memo\[r\]\[c\] = 1 + max over larger neighbours of memo of that neighbour. Each cell is computed once.

### Steps

1.  dfs(r, c) returns memo if set
2.  try 4 neighbours with a larger value
3.  answer = max over all cells

### C++17 solution

``` cpp
class Solution {
    vector<vector<int>> memo; int m, n;
    int dfs(vector<vector<int>>& a, int r, int c) {
        if (memo[r][c]) return memo[r][c];
        int best = 1, d[] = {1, 0, -1, 0, 1};
        for (int k = 0; k < 4; k++) { int x = r + d[k], y = c + d[k + 1]; if (x >= 0 && y >= 0 && x < m && y < n && a[x][y] > a[r][c]) best = max(best, 1 + dfs(a, x, y)); }
        return memo[r][c] = best;
    }
public:
    int longestIncreasingPath(vector<vector<int>>& a) {
        m = a.size(); n = a[0].size(); memo.assign(m, vector<int>(n, 0)); int r = 0;
        for (int i = 0; i < m; i++) for (int j = 0; j < n; j++) r = max(r, dfs(a, i, j));
        return r;
    }
};
```

### Test it passed

``` cpp
vector<vector<int>> a{{9,9,4},{6,6,8},{2,1,1}}; assert(Solution().longestIncreasingPath(a) == 4); vector<vector<int>> b{{3,4,5},{3,2,6},{2,2,1}}; assert(Solution().longestIncreasingPath(b) == 4); vector<vector<int>> c{{1}}; assert(Solution().longestIncreasingPath(c) == 1);
```

### Complexity

O(mn) time and space

### Traps

- DFS without memo (exponential)
- Using a visited array (unneeded: no cycles)

### Follow-ups

- Topological-sort (peel by out-degree) version.

## 39. Maximum Product Subarray

L2 [Kadane](knowledge-base/dsa.md#dynamic-programming) · [LeetCode ↗](https://leetcode.com/problems/maximum-product-subarray/) · Kadane's twist: a negative number swaps max and min.

### Key idea

Track both the largest and smallest product ending here. A negative number turns the smallest into the largest, so swap them before multiplying.

### Steps

1.  if x \< 0 swap(hi, lo)
2.  hi = max(x, hi·x), lo = min(x, lo·x), best = max(best, hi)

### C++17 solution

``` cpp
class Solution {
public:
    int maxProduct(vector<int>& a) {
        int hi = a[0], lo = a[0], best = a[0];
        for (int i = 1; i < (int)a.size(); i++) {
            int x = a[i]; if (x < 0) swap(hi, lo);
            hi = max(x, hi * x); lo = min(x, lo * x); best = max(best, hi);
        }
        return best;
    }
};
```

### Test it passed

``` cpp
vector<int> a{2,3,-2,4}; assert(Solution().maxProduct(a) == 6); vector<int> b{-2,0,-1}; assert(Solution().maxProduct(b) == 0); vector<int> c{-2,3,-4}; assert(Solution().maxProduct(c) == 24);
```

### Complexity

O(n) time, O(1) space

### Traps

- Tracking only the maximum

### Follow-ups

- Why does a zero reset both values automatically?

## 40. Counting Bits

L1 [Bit manipulation](knowledge-base/dsa.md#bit-manipulation) · [LeetCode ↗](https://leetcode.com/problems/counting-bits/) · DP on bits.

### Key idea

i has the same set bits as i \>\> 1, plus its lowest bit. So bits\[i\] = bits\[i \>\> 1\] + (i & 1).

### Steps

1.  r\[0\] = 0
2.  r\[i\] = r\[i \>\> 1\] + (i & 1)

### C++17 solution

``` cpp
class Solution {
public:
    vector<int> countBits(int n) { vector<int> r(n + 1, 0); for (int i = 1; i <= n; i++) r[i] = r[i >> 1] + (i & 1); return r; }
};
```

### Test it passed

``` cpp
assert((Solution().countBits(2) == vector<int>{0,1,1})); assert((Solution().countBits(5) == vector<int>{0,1,1,2,1,2}));
```

### Complexity

O(n) time

### Traps

- Calling popcount per number (fine, but not the DP they want)

### Follow-ups

- Another recurrence: r\[i\] = r\[i & (i − 1)\] + 1.
