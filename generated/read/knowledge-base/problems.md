# Problems

[All categories](README.md) · 83 topics

## Topics

- [Two Sum](#two-sum)
- [Best Time to Buy and Sell Stock](#best-time-to-buy-and-sell-stock)
- [Product of Array Except Self](#product-of-array-except-self)
- [Maximum Subarray (Kadane)](#maximum-subarray-kadane)
- [Longest Consecutive Sequence](#longest-consecutive-sequence)
- [Group Anagrams](#group-anagrams)
- [Top K Frequent Elements](#top-k-frequent-elements)
- [3Sum](#3sum)
- [Container With Most Water](#container-with-most-water)
- [Trapping Rain Water](#trapping-rain-water)
- [Longest Substring Without Repeating Characters](#longest-substring-without-repeating-characters)
- [Minimum Window Substring](#minimum-window-substring)
- [Subarray Sum Equals K](#subarray-sum-equals-k)
- [Search in Rotated Sorted Array](#search-in-rotated-sorted-array)
- [Koko Eating Bananas](#koko-eating-bananas)
- [Valid Parentheses](#valid-parentheses)
- [Daily Temperatures](#daily-temperatures)
- [Largest Rectangle in Histogram](#largest-rectangle-in-histogram)
- [Reverse Linked List](#reverse-linked-list)
- [Linked List Cycle II](#linked-list-cycle-ii)
- [Merge K Sorted Lists](#merge-k-sorted-lists)
- [LRU Cache](#lru-cache)
- [Binary Tree Level Order Traversal](#binary-tree-level-order-traversal)
- [Lowest Common Ancestor of a Binary Tree](#lowest-common-ancestor-of-a-binary-tree)
- [Validate Binary Search Tree](#validate-binary-search-tree)
- [Binary Tree Maximum Path Sum](#binary-tree-maximum-path-sum)
- [Number of Islands](#number-of-islands)
- [Course Schedule](#course-schedule)
- [Rotting Oranges](#rotting-oranges)
- [Network Delay Time](#network-delay-time)
- [Number of Provinces](#number-of-provinces)
- [House Robber](#house-robber)
- [Coin Change](#coin-change)
- [Longest Increasing Subsequence](#longest-increasing-subsequence)
- [Longest Common Subsequence](#longest-common-subsequence)
- [Edit Distance](#edit-distance)
- [Partition Equal Subset Sum](#partition-equal-subset-sum)
- [Subsets](#subsets)
- [Merge Intervals](#merge-intervals)
- [Kth Largest Element in an Array](#kth-largest-element-in-an-array)
- [Implement Trie (Prefix Tree)](#implement-trie-prefix-tree)
- [Jump Game](#jump-game)
- [Find Median from Data Stream](#find-median-from-data-stream)
- [Rotate Image](#rotate-image)
- [Spiral Matrix](#spiral-matrix)
- [Set Matrix Zeroes](#set-matrix-zeroes)
- [Next Permutation](#next-permutation)
- [Sort Colors (Dutch national flag)](#sort-colors-dutch-national-flag)
- [Search a 2D Matrix](#search-a-2d-matrix)
- [Majority Element (Boyer–Moore)](#majority-element-boyermoore)
- [Find the Duplicate Number](#find-the-duplicate-number)
- [Merge Sorted Array](#merge-sorted-array)
- [Longest Palindromic Substring](#longest-palindromic-substring)
- [Palindromic Substrings](#palindromic-substrings)
- [Minimum Size Subarray Sum](#minimum-size-subarray-sum)
- [Sliding Window Maximum](#sliding-window-maximum)
- [Permutation in String](#permutation-in-string)
- [Word Search](#word-search)
- [Combination Sum](#combination-sum)
- [Permutations II](#permutations-ii)
- [N-Queens](#n-queens)
- [Decode Ways](#decode-ways)
- [Unique Paths](#unique-paths)
- [Word Break](#word-break)
- [Maximum Product Subarray](#maximum-product-subarray)
- [Jump Game II](#jump-game-ii)
- [Gas Station](#gas-station)
- [Kth Smallest Element in a BST](#kth-smallest-element-in-a-bst)
- [Construct Binary Tree from Preorder and Inorder](#construct-binary-tree-from-preorder-and-inorder)
- [Binary Tree Right Side View](#binary-tree-right-side-view)
- [Serialize and Deserialize Binary Tree](#serialize-and-deserialize-binary-tree)
- [Diameter of Binary Tree](#diameter-of-binary-tree)
- [Pacific Atlantic Water Flow](#pacific-atlantic-water-flow)
- [Course Schedule II](#course-schedule-ii)
- [Clone Graph](#clone-graph)
- [Cheapest Flights Within K Stops](#cheapest-flights-within-k-stops)
- [Reverse Nodes in k-Group](#reverse-nodes-in-k-group)
- [Copy List with Random Pointer](#copy-list-with-random-pointer)
- [Remove Nth Node From End of List](#remove-nth-node-from-end-of-list)
- [Non-overlapping Intervals](#non-overlapping-intervals)
- [Decode String](#decode-string)
- [Counting Bits](#counting-bits)
- [Longest Increasing Path in a Matrix](#longest-increasing-path-in-a-matrix)

## Two Sum

*Level 1: Core*

Pattern: Hashing. The most famous first-round question; asked everywhere as a warm-up.

**Key idea**

Brute force checks every pair: O(n²). Instead, walk once and remember each value's index in a hash map. For each x, the partner you need is target − x; if it's already in the map, you're done.

Check the map before inserting x, so an element is never paired with itself.


**Points**

- For i in 0..n−1: if target − a\[i\] is in the map, return \[map\[target − a\[i\]\], i\]
- Otherwise store a\[i\] → i
- Complexity: O(n) time, O(n) space

```cpp
class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        unordered_map<int, int> pos;                 // value -> index
        for (int i = 0; i < (int)nums.size(); i++) {
            auto it = pos.find(target - nums[i]);
            if (it != pos.end()) return {it->second, i};
            pos[nums[i]] = i;
        }
        return {};
    }
};
```

**Traps**

- Inserting before checking (pairs x with itself)
- Returning values instead of indices

**Interviewers ask**

- What if the array is sorted? (two pointers, O(1) space)
- What if there can be many answers? Return all pairs without duplicates.

**Practise**

- [Solve it on LeetCode: Two Sum](https://leetcode.com/problems/two-sum/)

**Related:** [Hashing and frequency maps](dsa.md#hashing-and-frequency-maps)

[Back to the topic list](#topics)

## Best Time to Buy and Sell Stock

*Level 1: Core*

Pattern: Greedy. Amazon and Microsoft favourite; leads into the stock DP family.

**Key idea**

The best sale on day i uses the cheapest price before day i. Track the running minimum and the best difference.


**Points**

- minPrice = a\[0\]; best = 0
- For each price: best = max(best, price − minPrice); minPrice = min(minPrice, price)
- Complexity: O(n) time, O(1) space

```cpp
class Solution {
public:
    int maxProfit(vector<int>& prices) {
        int lo = INT_MAX, best = 0;
        for (int p : prices) { best = max(best, p - lo); lo = min(lo, p); }
        return best;
    }
};
```

**Traps**

- p − INT\_MAX overflow if the order of the two lines is swapped carelessly (here best is updated first with lo = INT\_MAX, which gives a negative number, safe)

**Interviewers ask**

- Unlimited transactions? (sum every positive difference)
- At most k transactions or with cooldown? (state-machine DP)

**Practise**

- [Solve it on LeetCode: Best Time to Buy and Sell Stock](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/)

**Related:** [Greedy algorithms](dsa.md#greedy-algorithms)

[Back to the topic list](#topics)

## Product of Array Except Self

*Level 2: Interview-ready*

Pattern: Prefix sum. Asked at Amazon, Meta, Microsoft; tests prefix thinking without division.

**Key idea**

answer\[i\] = (product of everything left of i) × (product of everything right of i). Fill left products in one pass, then multiply by a running right product in a second pass.


**Points**

- res\[i\] = product of a\[0..i−1\]
- Walk from the right with r = 1: res\[i\] \*= r; r \*= a\[i\]
- Complexity: O(n) time, O(1) extra space (the output doesn't count)

```cpp
class Solution {
public:
    vector<int> productExceptSelf(vector<int>& nums) {
        int n = nums.size();
        vector<int> res(n, 1);
        for (int i = 1; i < n; i++) res[i] = res[i - 1] * nums[i - 1];
        int r = 1;
        for (int i = n - 1; i >= 0; i--) { res[i] *= r; r *= nums[i]; }
        return res;
    }
};
```

**Traps**

- Using division (breaks with zeros, and it's forbidden)

**Interviewers ask**

- Why is the output array not counted as extra space?

**Practise**

- [Solve it on LeetCode: Product of Array Except Self](https://leetcode.com/problems/product-of-array-except-self/)

**Related:** [Prefix sums](dsa.md#prefix-sums)

[Back to the topic list](#topics)

## Maximum Subarray (Kadane)

*Level 2: Interview-ready*

Pattern: Kadane. Classic; tests whether you see the 1-D DP hidden in it.

**Key idea**

At each index, the best subarray ending here either extends the best one ending at i−1 or starts fresh at i: cur = max(a\[i\], cur + a\[i\]). The answer is the best cur seen.


**Points**

- cur = best = a\[0\]
- For i ≥ 1: cur = max(a\[i\], cur + a\[i\]); best = max(best, cur)
- Complexity: O(n) time, O(1) space

```cpp
class Solution {
public:
    int maxSubArray(vector<int>& nums) {
        int cur = nums[0], best = nums[0];
        for (int i = 1; i < (int)nums.size(); i++) { cur = max(nums[i], cur + nums[i]); best = max(best, cur); }
        return best;
    }
};
```

**Traps**

- Starting best at 0 (wrong when all numbers are negative)

**Interviewers ask**

- Return the start and end indices too.
- Maximum product subarray? (track both max and min)

**Practise**

- [Solve it on LeetCode: Maximum Subarray (Kadane)](https://leetcode.com/problems/maximum-subarray/)

**Related:** [Dynamic programming](dsa.md#dynamic-programming)

[Back to the topic list](#topics)

## Longest Consecutive Sequence

*Level 2: Interview-ready*

Pattern: Hashing. Google and Amazon; the O(n) requirement is the whole point.

**Key idea**

Put all numbers in a hash set. Only start counting from x when x − 1 is not in the set (x is the start of a run), then walk x+1, x+2… Each number is visited at most twice, so the total is O(n).


**Points**

- set s(all)
- For x in s: if x−1 not in s, count the run from x
- Complexity: O(n) average time, O(n) space

```cpp
class Solution {
public:
    int longestConsecutive(vector<int>& nums) {
        unordered_set<int> s(nums.begin(), nums.end());
        int best = 0;
        for (int x : s) {
            if (s.count(x - 1)) continue;          // not the start of a run
            int len = 1;
            while (s.count(x + len)) len++;
            best = max(best, len);
        }
        return best;
    }
};
```

**Traps**

- Starting a walk from every number (O(n²) on a long run)
- Sorting (O(n log n), not what's asked)

**Interviewers ask**

- Why is it O(n) even with the inner while loop?

**Practise**

- [Solve it on LeetCode: Longest Consecutive Sequence](https://leetcode.com/problems/longest-consecutive-sequence/)

**Related:** [Hashing and frequency maps](dsa.md#hashing-and-frequency-maps)

[Back to the topic list](#topics)

## Group Anagrams

*Level 2: Interview-ready*

Pattern: Hashing. Common at Amazon, Uber and service-company OAs.

**Key idea**

Anagrams share a canonical key. Use the sorted word (O(k log k)) or a 26-letter count string (O(k)) as the hash-map key, and append each word to its group.


**Points**

- key = sorted(word)
- groups\[key\].push\_back(word)
- Complexity: O(n·k log k) time, O(n·k) space

```cpp
class Solution {
public:
    vector<vector<string>> groupAnagrams(vector<string>& strs) {
        unordered_map<string, vector<string>> g;
        for (auto& s : strs) { string k = s; sort(k.begin(), k.end()); g[k].push_back(s); }
        vector<vector<string>> res;
        for (auto& [k, v] : g) res.push_back(v);
        return res;
    }
};
```

**Traps**

- Using a count array as the key without separators ("1","11" collisions)

**Interviewers ask**

- Make the key O(k) instead of O(k log k).

**Practise**

- [Solve it on LeetCode: Group Anagrams](https://leetcode.com/problems/group-anagrams/)

**Related:** [Hashing and frequency maps](dsa.md#hashing-and-frequency-maps)

[Back to the topic list](#topics)

## Top K Frequent Elements

*Level 2: Interview-ready*

Pattern: Heap. Amazon's most-asked heap problem.

**Key idea**

Count frequencies with a hash map, then keep a min-heap of size k keyed by frequency; anything smaller than the heap's top can't be in the answer. Bucket sort by frequency gives O(n).


**Points**

- Count
- Push (freq, value) into a min-heap; pop when size \> k
- Heap contents are the answer
- Complexity: O(n log k) time, O(n) space

```cpp
class Solution {
public:
    vector<int> topKFrequent(vector<int>& nums, int k) {
        unordered_map<int, int> f;
        for (int x : nums) f[x]++;
        priority_queue<pair<int,int>, vector<pair<int,int>>, greater<>> pq;   // (freq, value), min on top
        for (auto& [v, c] : f) { pq.push({c, v}); if ((int)pq.size() > k) pq.pop(); }
        vector<int> res;
        while (!pq.empty()) { res.push_back(pq.top().second); pq.pop(); }
        return res;
    }
};
```

**Traps**

- Using a max-heap of all n elements (O(n log n))

**Interviewers ask**

- Do it in O(n) with buckets.
- What if the data is a stream?

**Practise**

- [Solve it on LeetCode: Top K Frequent Elements](https://leetcode.com/problems/top-k-frequent-elements/)

**Related:** [Heaps and priority queues](dsa.md#heaps-and-priority-queues)

[Back to the topic list](#topics)

## 3Sum

*Level 2: Interview-ready*

Pattern: Two pointers. Top-10 at Meta, Amazon, Microsoft; tests duplicate handling.

**Key idea**

Sort. Fix a\[i\] and find pairs in a\[i+1..n−1\] summing to −a\[i\] with two pointers. Skip equal values of a\[i\], and skip equal values after finding a triple, so no duplicate triples appear.


**Points**

- Sort
- For each i (skip a\[i\] == a\[i−1\]): l = i+1, r = n−1
- Move l or r by the sum's sign; on a hit, record and skip duplicates on both sides
- Complexity: O(n²) time, O(1) extra space (besides sorting)

```cpp
class Solution {
public:
    vector<vector<int>> threeSum(vector<int>& a) {
        sort(a.begin(), a.end());
        vector<vector<int>> res; int n = a.size();
        for (int i = 0; i < n - 2; i++) {
            if (i && a[i] == a[i - 1]) continue;
            int l = i + 1, r = n - 1;
            while (l < r) {
                int s = a[i] + a[l] + a[r];
                if (s < 0) l++;
                else if (s > 0) r--;
                else {
                    res.push_back({a[i], a[l], a[r]});
                    while (l < r && a[l] == a[l + 1]) l++;
                    while (l < r && a[r] == a[r - 1]) r--;
                    l++; r--;
                }
            }
        }
        return res;
    }
};
```

**Traps**

- Not skipping duplicates
- Using a set of triples to dedupe (slow, and interviewers notice)

**Interviewers ask**

- 4Sum?
- 3Sum closest?

**Practise**

- [Solve it on LeetCode: 3Sum](https://leetcode.com/problems/3sum/)

**Related:** [Two pointers](dsa.md#two-pointers)

[Back to the topic list](#topics)

## Container With Most Water

*Level 2: Interview-ready*

Pattern: Two pointers. Asked at Google and Amazon; the proof is the interview.

**Key idea**

Start with the widest container. The height is limited by the shorter line, so moving the taller line inward can never help: the width shrinks and the height can't exceed the shorter line. Always move the shorter one.


**Points**

- l = 0, r = n−1
- area = (r − l) × min(h\[l\], h\[r\])
- Move the shorter side inward
- Complexity: O(n) time, O(1) space

```cpp
class Solution {
public:
    int maxArea(vector<int>& h) {
        int l = 0, r = h.size() - 1, best = 0;
        while (l < r) {
            best = max(best, (r - l) * min(h[l], h[r]));
            if (h[l] < h[r]) l++; else r--;
        }
        return best;
    }
};
```

**Traps**

- Moving the taller side

**Interviewers ask**

- Prove that moving the shorter side never skips the best answer.

**Practise**

- [Solve it on LeetCode: Container With Most Water](https://leetcode.com/problems/container-with-most-water/)

**Related:** [Two pointers](dsa.md#two-pointers)

[Back to the topic list](#topics)

## Trapping Rain Water

*Level 3: Advanced*

Pattern: Two pointers. The most famous Hard; Google, Amazon, Goldman Sachs.

**Key idea**

Water above bar i = min(maxLeft, maxRight) − h\[i\]. With two pointers, whichever side has the smaller running maximum is the bottleneck, so that side's water is already known: process it and move inward.


**Points**

- l, r at ends; lmax = rmax = 0
- If h\[l\] \< h\[r\]: lmax = max(lmax, h\[l\]); water += lmax − h\[l\]; l++
- Else the same on the right
- Complexity: O(n) time, O(1) space

```cpp
class Solution {
public:
    int trap(vector<int>& h) {
        int l = 0, r = (int)h.size() - 1, lmax = 0, rmax = 0, w = 0;
        while (l < r) {
            if (h[l] < h[r]) { lmax = max(lmax, h[l]); w += lmax - h[l]; l++; }
            else { rmax = max(rmax, h[r]); w += rmax - h[r]; r--; }
        }
        return w;
    }
};
```

**Traps**

- Off-by-one with prefix arrays
- Forgetting the empty-array case

**Interviewers ask**

- Solve it with prefix/suffix maximum arrays first, then optimise.
- Solve it with a monotonic stack.
- Trapping Rain Water II (2-D, heap + BFS)

**Practise**

- [Solve it on LeetCode: Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/)

**Related:** [Two pointers](dsa.md#two-pointers)

[Back to the topic list](#topics)

## Longest Substring Without Repeating Characters

*Level 2: Interview-ready*

Pattern: Sliding window. Top-5 most asked overall.

**Key idea**

Keep a window with no repeats. Remember the last index of each character; when s\[r\] was seen inside the window, jump l to one past that index.


**Points**

- last\[c\] = −1 for all c; l = 0
- For each r: if last\[s\[r\]\] ≥ l, l = last\[s\[r\]\] + 1
- last\[s\[r\]\] = r; best = max(best, r − l + 1)
- Complexity: O(n) time, O(alphabet) space

```cpp
class Solution {
public:
    int lengthOfLongestSubstring(string s) {
        vector<int> last(256, -1);
        int best = 0;
        for (int l = 0, r = 0; r < (int)s.size(); r++) {
            unsigned char c = s[r];
            if (last[c] >= l) l = last[c] + 1;
            last[c] = r;
            best = max(best, r - l + 1);
        }
        return best;
    }
};
```

**Traps**

- Moving l backwards when the old index is outside the window (the ≥ l check prevents it)

**Interviewers ask**

- At most k distinct characters?
- Return the substring itself.

**Practise**

- [Solve it on LeetCode: Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/)

**Related:** [Sliding window](dsa.md#sliding-window)

[Back to the topic list](#topics)

## Minimum Window Substring

*Level 3: Advanced*

Pattern: Sliding window. Hard sliding-window favourite at Meta, LinkedIn, Uber.

**Key idea**

Count what t needs. Expand r; when the window covers all of t (need count reaches 0), shrink l as far as possible while still covering, recording the smallest window.


**Points**

- need\[c\] from t; missing = \|t\|
- Expand r: if need\[s\[r\]\] \> 0, missing−−; need\[s\[r\]\]−−
- While missing == 0: record; need\[s\[l\]\]++; if it becomes \> 0, missing++; l++
- Complexity: O(\|s\| + \|t\|) time, O(alphabet) space

```cpp
class Solution {
public:
    string minWindow(string s, string t) {
        vector<int> need(128, 0);
        for (char c : t) need[c]++;
        int missing = t.size(), start = 0, len = INT_MAX;
        for (int l = 0, r = 0; r < (int)s.size(); r++) {
            if (need[s[r]]-- > 0) missing--;
            while (missing == 0) {
                if (r - l + 1 < len) { len = r - l + 1; start = l; }
                if (++need[s[l++]] > 0) missing++;
            }
        }
        return len == INT_MAX ? "" : s.substr(start, len);
    }
};
```

**Traps**

- Forgetting duplicate letters in t
- Recording the window after shrinking past validity

**Interviewers ask**

- Why does each character enter and leave at most once?

**Practise**

- [Solve it on LeetCode: Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/)

**Related:** [Sliding window](dsa.md#sliding-window)

[Back to the topic list](#topics)

## Subarray Sum Equals K

*Level 2: Interview-ready*

Pattern: Prefix sum. Common at Meta, Google; the trap is trying a sliding window.

**Key idea**

Negative numbers break sliding windows. A subarray (j, i\] sums to k exactly when prefix\[i\] − prefix\[j\] = k. Keep counts of every prefix seen; at each i add count\[prefix − k\].


**Points**

- count\[0\] = 1; s = 0
- For x: s += x; ans += count\[s − k\]; count\[s\]++
- Complexity: O(n) time, O(n) space

```cpp
class Solution {
public:
    int subarraySum(vector<int>& nums, int k) {
        unordered_map<long long, int> cnt{{0, 1}};
        long long s = 0; int ans = 0;
        for (int x : nums) { s += x; auto it = cnt.find(s - k); if (it != cnt.end()) ans += it->second; cnt[s]++; }
        return ans;
    }
};
```

**Traps**

- Missing cnt\[0\] = 1
- Using a sliding window

**Interviewers ask**

- Longest subarray with sum k?
- Count subarrays divisible by k?

**Practise**

- [Solve it on LeetCode: Subarray Sum Equals K](https://leetcode.com/problems/subarray-sum-equals-k/)

**Related:** [Prefix sums](dsa.md#prefix-sums)

[Back to the topic list](#topics)

## Search in Rotated Sorted Array

*Level 2: Interview-ready*

Pattern: Binary search. Microsoft, Amazon, LinkedIn staple.

**Key idea**

At any mid, one half \[lo, mid\] or \[mid, hi\] is sorted. Check whether the target lies in the sorted half's range; if so search there, otherwise search the other half.


**Points**

- If a\[lo\] ≤ a\[mid\]: left half sorted; go left if a\[lo\] ≤ target \< a\[mid\]
- Else right half sorted; go right if a\[mid\] \< target ≤ a\[hi\]
- Complexity: O(log n) time, O(1) space

```cpp
class Solution {
public:
    int search(vector<int>& a, int target) {
        int lo = 0, hi = a.size() - 1;
        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2;
            if (a[mid] == target) return mid;
            if (a[lo] <= a[mid]) {
                if (a[lo] <= target && target < a[mid]) hi = mid - 1; else lo = mid + 1;
            } else {
                if (a[mid] < target && target <= a[hi]) lo = mid + 1; else hi = mid - 1;
            }
        }
        return -1;
    }
};
```

**Traps**

- Using \< instead of ≤ in a\[lo\] ≤ a\[mid\] (fails on two elements)

**Interviewers ask**

- With duplicates? (worst case O(n): shrink lo/hi when a\[lo\] == a\[mid\] == a\[hi\])
- Find the rotation point / minimum.

**Practise**

- [Solve it on LeetCode: Search in Rotated Sorted Array](https://leetcode.com/problems/search-in-rotated-sorted-array/)

**Related:** [Binary search](dsa.md#binary-search)

[Back to the topic list](#topics)

## Koko Eating Bananas

*Level 2: Interview-ready*

Pattern: Binary search on the answer. The textbook binary-search-on-answer problem.

**Key idea**

If Koko can finish at speed k, she can at any faster speed: feasibility is monotone. Binary search k in \[1, max pile\]; check(k) sums ceil(pile / k) hours.


**Points**

- lo = 1, hi = max(piles)
- check(k): Σ ⌈p/k⌉ ≤ h
- Find the smallest k where check is true
- Complexity: O(n log max) time, O(1) space

```cpp
class Solution {
public:
    int minEatingSpeed(vector<int>& piles, int h) {
        int lo = 1, hi = *max_element(piles.begin(), piles.end()), ans = hi;
        while (lo <= hi) {
            int k = lo + (hi - lo) / 2;
            long long hours = 0;
            for (int p : piles) hours += (p + k - 1) / k;
            if (hours <= h) { ans = k; hi = k - 1; } else lo = k + 1;
        }
        return ans;
    }
};
```

**Traps**

- int overflow in the hours sum
- Starting lo at 0 (division by zero)

**Interviewers ask**

- Capacity to ship packages in D days.
- Split array largest sum.

**Practise**

- [Solve it on LeetCode: Koko Eating Bananas](https://leetcode.com/problems/koko-eating-bananas/)

**Related:** [Binary search on the answer](dsa.md#binary-search-on-the-answer)

[Back to the topic list](#topics)

## Valid Parentheses

*Level 1: Core*

Pattern: Stack. The standard stack opener in first rounds.

**Key idea**

Push opening brackets. On a closing bracket the stack top must be its matching opener; pop it. At the end the stack must be empty.


**Points**

- Map ) → (, \] → \[, } → {
- Mismatch or empty stack on a closer → false
- Complexity: O(n) time, O(n) space

```cpp
class Solution {
public:
    bool isValid(string s) {
        string st;
        for (char c : s) {
            if (c == '(' || c == '[' || c == '{') st.push_back(c);
            else {
                char want = c == ')' ? '(' : c == ']' ? '[' : '{';
                if (st.empty() || st.back() != want) return false;
                st.pop_back();
            }
        }
        return st.empty();
    }
};
```

**Traps**

- Forgetting the final empty check
- Popping an empty stack

**Interviewers ask**

- Minimum additions to make it valid?
- Longest valid parentheses (Hard)

**Practise**

- [Solve it on LeetCode: Valid Parentheses](https://leetcode.com/problems/valid-parentheses/)

**Related:** [Stacks and queues](dsa.md#stacks-and-queues)

[Back to the topic list](#topics)

## Daily Temperatures

*Level 2: Interview-ready*

Pattern: Monotonic stack. The cleanest next-greater-element problem.

**Key idea**

Keep a stack of indices with decreasing temperatures. When a warmer day arrives, every colder day on the stack has found its answer: pop and record the distance.


**Points**

- For i: while stack top is colder than t\[i\], res\[top\] = i − top, pop
- Push i
- Complexity: O(n) time (each index pushed and popped once), O(n) space

```cpp
class Solution {
public:
    vector<int> dailyTemperatures(vector<int>& t) {
        vector<int> res(t.size(), 0), st;
        for (int i = 0; i < (int)t.size(); i++) {
            while (!st.empty() && t[st.back()] < t[i]) { res[st.back()] = i - st.back(); st.pop_back(); }
            st.push_back(i);
        }
        return res;
    }
};
```

**Traps**

- Storing temperatures instead of indices

**Interviewers ask**

- Next greater element in a circular array.

**Practise**

- [Solve it on LeetCode: Daily Temperatures](https://leetcode.com/problems/daily-temperatures/)

**Related:** [Monotonic stack](dsa.md#monotonic-stack)

[Back to the topic list](#topics)

## Largest Rectangle in Histogram

*Level 3: Advanced*

Pattern: Monotonic stack. Hard-round favourite at Google and Amazon; base for Maximal Rectangle.

**Key idea**

For each bar, the widest rectangle of its height spans between its previous smaller and next smaller bars. An increasing stack finds both: when a bar is popped, the current index is its next smaller and the new stack top is its previous smaller.


**Points**

- Append a 0-height sentinel
- Pop while h\[top\] ≥ h\[i\]: width = i − (new top) − 1
- Area = h\[popped\] × width
- Complexity: O(n) time, O(n) space

```cpp
class Solution {
public:
    int largestRectangleArea(vector<int>& h) {
        h.push_back(0);
        vector<int> st; int best = 0;
        for (int i = 0; i < (int)h.size(); i++) {
            while (!st.empty() && h[st.back()] >= h[i]) {
                int height = h[st.back()]; st.pop_back();
                int left = st.empty() ? -1 : st.back();
                best = max(best, height * (i - left - 1));
            }
            st.push_back(i);
        }
        h.pop_back();
        return best;
    }
};
```

**Traps**

- Forgetting the sentinel, so bars left on the stack are never measured

**Interviewers ask**

- Maximal rectangle of 1s in a matrix (apply this per row).

**Practise**

- [Solve it on LeetCode: Largest Rectangle in Histogram](https://leetcode.com/problems/largest-rectangle-in-histogram/)

**Related:** [Monotonic stack](dsa.md#monotonic-stack)

[Back to the topic list](#topics)

## Reverse Linked List

*Level 1: Core*

Pattern: Linked list. Asked in almost every first round; often followed by the recursive version.

**Key idea**

Walk the list re-pointing each node's next to the previous node. Save next before overwriting it.


**Points**

- prev = null, cur = head
- nx = cur.next; cur.next = prev; prev = cur; cur = nx
- Return prev
- Complexity: O(n) time, O(1) space

```cpp
class Solution {
public:
    ListNode* reverseList(ListNode* head) {
        ListNode* prev = nullptr;
        while (head) { ListNode* nx = head->next; head->next = prev; prev = head; head = nx; }
        return prev;
    }
};
```

**Traps**

- Losing the rest of the list

**Interviewers ask**

- Reverse recursively.
- Reverse nodes between positions m and n.
- Reverse in groups of k (Hard).

**Practise**

- [Solve it on LeetCode: Reverse Linked List](https://leetcode.com/problems/reverse-linked-list/)

**Related:** [Linked lists](dsa.md#linked-lists)

[Back to the topic list](#topics)

## Linked List Cycle II

*Level 2: Interview-ready*

Pattern: Linked list. Floyd's algorithm; the proof is a common follow-up.

**Key idea**

Slow moves 1, fast moves 2; if they meet there's a cycle. Then move one pointer to head and step both by 1: they meet at the cycle start, because head-to-start distance equals meeting-point-to-start distance (mod cycle length).


**Points**

- Detect: slow/fast meet
- Reset one to head; step both by 1 until equal
- Complexity: O(n) time, O(1) space

```cpp
class Solution {
public:
    ListNode* detectCycle(ListNode* head) {
        ListNode *s = head, *f = head;
        while (f && f->next) {
            s = s->next; f = f->next->next;
            if (s == f) { s = head; while (s != f) { s = s->next; f = f->next; } return s; }
        }
        return nullptr;
    }
};
```

**Traps**

- Checking f-\>next-\>next without checking f-\>next

**Interviewers ask**

- Prove why the second phase meets at the start.
- Find the cycle length.

**Practise**

- [Solve it on LeetCode: Linked List Cycle II](https://leetcode.com/problems/linked-list-cycle-ii/)

**Related:** [Linked lists](dsa.md#linked-lists)

[Back to the topic list](#topics)

## Merge K Sorted Lists

*Level 3: Advanced*

Pattern: Heap. Amazon, Google, Meta Hard; tests heap use with pointers.

**Key idea**

Push each list's head into a min-heap keyed by value. Pop the smallest, append it, push its next. Every node goes through the heap once.


**Points**

- Min-heap of (val, node)
- Pop, append, push node-\>next
- Complexity: O(N log k) time, O(k) space

```cpp
class Solution {
public:
    ListNode* mergeKLists(vector<ListNode*>& lists) {
        auto cmp = [](ListNode* a, ListNode* b) { return a->val > b->val; };
        priority_queue<ListNode*, vector<ListNode*>, decltype(cmp)> pq(cmp);
        for (auto l : lists) if (l) pq.push(l);
        ListNode dummy(0); ListNode* t = &dummy;
        while (!pq.empty()) { auto n = pq.top(); pq.pop(); t->next = n; t = n; if (n->next) pq.push(n->next); }
        return dummy.next;
    }
};
```

**Traps**

- Pushing null heads

**Interviewers ask**

- Divide and conquer: merge pairs (same complexity, no heap).
- What if lists are huge files on disk? (external merge)

**Practise**

- [Solve it on LeetCode: Merge K Sorted Lists](https://leetcode.com/problems/merge-k-sorted-lists/)

**Related:** [Heaps and priority queues](dsa.md#heaps-and-priority-queues)

[Back to the topic list](#topics)

## LRU Cache

*Level 2: Interview-ready*

Pattern: Linked list. One of the most-asked design questions for freshers at Amazon, Microsoft, Swiggy.

**Key idea**

Need O(1) get and put with recency order. A hash map gives O(1) lookup of a node; a doubly linked list gives O(1) move-to-front and remove-from-back. std::list + splice does both.


**Points**

- map key → list iterator
- get: splice the node to the front
- put: update or insert at front; if over capacity, erase the back and its map entry
- Complexity: O(1) per operation, O(capacity) space

```cpp
class LRUCache {
    int cap;
    list<pair<int,int>> dq;                                  // front = most recent
    unordered_map<int, list<pair<int,int>>::iterator> pos;
public:
    LRUCache(int capacity) : cap(capacity) {}
    int get(int key) {
        auto it = pos.find(key);
        if (it == pos.end()) return -1;
        dq.splice(dq.begin(), dq, it->second);
        return it->second->second;
    }
    void put(int key, int value) {
        auto it = pos.find(key);
        if (it != pos.end()) { it->second->second = value; dq.splice(dq.begin(), dq, it->second); return; }
        dq.emplace_front(key, value); pos[key] = dq.begin();
        if ((int)dq.size() > cap) { pos.erase(dq.back().first); dq.pop_back(); }
    }
};
```

**Traps**

- Forgetting to move on update
- Erasing from the map after popping (dangling)

**Interviewers ask**

- Make it thread-safe.
- LFU cache (Hard).
- How does Redis approximate LRU?

**Practise**

- [Solve it on LeetCode: LRU Cache](https://leetcode.com/problems/lru-cache/)

**Related:** [Linked lists](dsa.md#linked-lists)

[Back to the topic list](#topics)

## Binary Tree Level Order Traversal

*Level 2: Interview-ready*

Pattern: BFS. Base for zigzag, right view, and many tree BFS questions.

**Key idea**

BFS with a queue; process exactly the current queue size each round to keep levels separate.


**Points**

- q = \[root\]
- While q: sz = q.size(); pop sz nodes into one level, pushing children
- Complexity: O(n) time, O(width) space

```cpp
class Solution {
public:
    vector<vector<int>> levelOrder(TreeNode* root) {
        vector<vector<int>> res; if (!root) return res;
        queue<TreeNode*> q; q.push(root);
        while (!q.empty()) {
            int sz = q.size(); res.emplace_back();
            while (sz--) { auto n = q.front(); q.pop(); res.back().push_back(n->val);
                if (n->left) q.push(n->left); if (n->right) q.push(n->right); }
        }
        return res;
    }
};
```

**Traps**

- Reading q.size() inside the loop condition (it changes)

**Interviewers ask**

- Zigzag order.
- Right side view.
- Average of each level.

**Practise**

- [Solve it on LeetCode: Binary Tree Level Order Traversal](https://leetcode.com/problems/binary-tree-level-order-traversal/)

**Related:** [BFS and graph basics](dsa.md#bfs-and-graph-basics)

[Back to the topic list](#topics)

## Lowest Common Ancestor of a Binary Tree

*Level 2: Interview-ready*

Pattern: Trees. Asked at Meta, Amazon, Microsoft; short code, tricky reasoning.

**Key idea**

Recurse: return the node if it's p or q. If the left and right subtrees each return non-null, this node is the LCA; otherwise pass up whichever side is non-null.


**Points**

- Base: null, p or q → return it
- L = lca(left), R = lca(right)
- Both non-null → root; else the non-null one
- Complexity: O(n) time, O(h) space

```cpp
class Solution {
public:
    TreeNode* lowestCommonAncestor(TreeNode* root, TreeNode* p, TreeNode* q) {
        if (!root || root == p || root == q) return root;
        TreeNode* L = lowestCommonAncestor(root->left, p, q);
        TreeNode* R = lowestCommonAncestor(root->right, p, q);
        return L && R ? root : (L ? L : R);
    }
};
```

**Traps**

- Assuming it's a BST (that version walks by value)

**Interviewers ask**

- LCA in a BST.
- What if p or q may not exist in the tree?

**Practise**

- [Solve it on LeetCode: Lowest Common Ancestor of a Binary Tree](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/)

**Related:** [Binary trees](dsa.md#binary-trees)

[Back to the topic list](#topics)

## Validate Binary Search Tree

*Level 2: Interview-ready*

Pattern: BST. Tests whether you know the BST property is global, not parent-child.

**Key idea**

Every node must lie strictly between bounds inherited from its ancestors. Pass (lo, hi) down: left child gets (lo, val), right child gets (val, hi). Use long long or pointers for the bounds.


**Points**

- valid(node, lo, hi): lo \< val \< hi
- Recurse left with hi = val, right with lo = val
- Complexity: O(n) time, O(h) space

```cpp
class Solution {
    bool ok(TreeNode* n, long long lo, long long hi) {
        if (!n) return true;
        if (n->val <= lo || n->val >= hi) return false;
        return ok(n->left, lo, n->val) && ok(n->right, n->val, hi);
    }
public:
    bool isValidBST(TreeNode* root) { return ok(root, LLONG_MIN, LLONG_MAX); }
};
```

**Traps**

- Only comparing a node with its children
- int bounds failing for INT\_MIN/INT\_MAX values

**Interviewers ask**

- Do it with an inorder traversal (must be strictly increasing).
- Recover a BST with two swapped nodes.

**Practise**

- [Solve it on LeetCode: Validate Binary Search Tree](https://leetcode.com/problems/validate-binary-search-tree/)

**Related:** [Binary search trees](dsa.md#binary-search-trees)

[Back to the topic list](#topics)

## Binary Tree Maximum Path Sum

*Level 3: Advanced*

Pattern: Trees. Google and Meta Hard; the 'return one thing, record another' pattern.

**Key idea**

A path can bend at one node. For each node, the best path through it is val + best downward gain from left + from right (ignoring negative gains). But only one side can be returned to the parent.


**Points**

- gain(n) = n.val + max(0, gain(left), gain(right))… returning only one side
- best = max(best, val + max(0,L) + max(0,R))
- Complexity: O(n) time, O(h) space

```cpp
class Solution {
    int best = INT_MIN;
    int gain(TreeNode* n) {
        if (!n) return 0;
        int L = max(0, gain(n->left)), R = max(0, gain(n->right));
        best = max(best, n->val + L + R);
        return n->val + max(L, R);
    }
public:
    int maxPathSum(TreeNode* root) { gain(root); return best; }
};
```

**Traps**

- Returning L + R to the parent (that's not a path)
- Initialising best to 0 (fails on all-negative trees)

**Interviewers ask**

- Diameter of a binary tree (same pattern with edge counts).

**Practise**

- [Solve it on LeetCode: Binary Tree Maximum Path Sum](https://leetcode.com/problems/binary-tree-maximum-path-sum/)

**Related:** [Binary trees](dsa.md#binary-trees)

[Back to the topic list](#topics)

## Number of Islands

*Level 2: Interview-ready*

Pattern: DFS. Most-asked graph problem; grid as an implicit graph.

**Key idea**

Scan the grid; each unvisited '1' starts a new island. Flood-fill it (DFS or BFS) and mark visited so it isn't counted again.


**Points**

- For each cell == '1': count++, flood fill
- Fill: mark '0', recurse into 4 neighbours inside bounds
- Complexity: O(rows × cols) time and space (recursion)

```cpp
class Solution {
    void fill(vector<vector<char>>& g, int r, int c) {
        if (r < 0 || c < 0 || r >= (int)g.size() || c >= (int)g[0].size() || g[r][c] != '1') return;
        g[r][c] = '0';
        fill(g, r + 1, c); fill(g, r - 1, c); fill(g, r, c + 1); fill(g, r, c - 1);
    }
public:
    int numIslands(vector<vector<char>>& g) {
        int n = 0;
        for (int r = 0; r < (int)g.size(); r++) for (int c = 0; c < (int)g[0].size(); c++) if (g[r][c] == '1') { n++; fill(g, r, c); }
        return n;
    }
};
```

**Traps**

- Deep recursion on big grids (use BFS or an explicit stack)
- Not mentioning that you modify the input

**Interviewers ask**

- Max area of an island.
- Number of distinct islands.
- Do it with DSU.

**Practise**

- [Solve it on LeetCode: Number of Islands](https://leetcode.com/problems/number-of-islands/)

**Related:** [DFS, components and cycles](dsa.md#dfs-components-and-cycles)

[Back to the topic list](#topics)

## Course Schedule

*Level 2: Interview-ready*

Pattern: Topological sort. Amazon and Google; cycle detection in a directed graph.

**Key idea**

Courses are nodes, prerequisites are edges. All courses can be finished exactly when the graph has no cycle. Kahn's algorithm: repeatedly take nodes with in-degree 0; if you process all n, there's no cycle.


**Points**

- Build adjacency and in-degrees
- Queue all in-degree-0 nodes; pop, decrement neighbours
- Return processed == n
- Complexity: O(V + E) time and space

```cpp
class Solution {
public:
    bool canFinish(int n, vector<vector<int>>& pre) {
        vector<vector<int>> adj(n); vector<int> indeg(n, 0);
        for (auto& e : pre) { adj[e[1]].push_back(e[0]); indeg[e[0]]++; }
        queue<int> q; for (int i = 0; i < n; i++) if (!indeg[i]) q.push(i);
        int done = 0;
        while (!q.empty()) { int u = q.front(); q.pop(); done++; for (int v : adj[u]) if (--indeg[v] == 0) q.push(v); }
        return done == n;
    }
};
```

**Traps**

- Reversing the edge direction (harmless here, wrong in Course Schedule II's order)

**Interviewers ask**

- Return a valid order (Course Schedule II).
- Do it with DFS colouring.

**Practise**

- [Solve it on LeetCode: Course Schedule](https://leetcode.com/problems/course-schedule/)

**Related:** [Topological sort](dsa.md#topological-sort)

[Back to the topic list](#topics)

## Rotting Oranges

*Level 2: Interview-ready*

Pattern: BFS. Multi-source BFS; Amazon's favourite grid BFS.

**Key idea**

All rotten oranges start the BFS together. Each BFS level is one minute. At the end, if any fresh orange remains, return −1.


**Points**

- Queue all rotten cells; count fresh
- BFS level by level, rotting neighbours and decrementing fresh
- Answer = levels used, or −1
- Complexity: O(rows × cols) time and space

```cpp
class Solution {
public:
    int orangesRotting(vector<vector<int>>& g) {
        int R = g.size(), C = g[0].size(), fresh = 0, mins = 0;
        queue<pair<int,int>> q;
        for (int r = 0; r < R; r++) for (int c = 0; c < C; c++) { if (g[r][c] == 2) q.push({r, c}); else if (g[r][c] == 1) fresh++; }
        int dr[] = {1,-1,0,0}, dc[] = {0,0,1,-1};
        while (!q.empty() && fresh) {
            for (int sz = q.size(); sz--; ) {
                auto [r, c] = q.front(); q.pop();
                for (int k = 0; k < 4; k++) { int nr = r + dr[k], nc = c + dc[k];
                    if (nr >= 0 && nc >= 0 && nr < R && nc < C && g[nr][nc] == 1) { g[nr][nc] = 2; fresh--; q.push({nr, nc}); } }
            }
            mins++;
        }
        return fresh ? -1 : mins;
    }
};
```

**Traps**

- Counting a minute after the last level (stop when fresh is 0)

**Interviewers ask**

- 01 Matrix (distance to nearest 0).
- Walls and gates.

**Practise**

- [Solve it on LeetCode: Rotting Oranges](https://leetcode.com/problems/rotting-oranges/)

**Related:** [BFS and graph basics](dsa.md#bfs-and-graph-basics)

[Back to the topic list](#topics)

## Network Delay Time

*Level 2: Interview-ready*

Pattern: Dijkstra. The standard Dijkstra question.

**Key idea**

Shortest time for the signal to reach every node = the largest shortest-path distance from k. Run Dijkstra with a min-heap; if any node is unreachable, return −1.


**Points**

- dist\[k\] = 0; heap (d, node)
- Pop; skip stale; relax edges
- Answer = max(dist) or −1
- Complexity: O((V + E) log V) time

```cpp
class Solution {
public:
    int networkDelayTime(vector<vector<int>>& times, int n, int k) {
        vector<vector<pair<int,int>>> adj(n + 1);
        for (auto& t : times) adj[t[0]].push_back({t[1], t[2]});
        vector<int> d(n + 1, INT_MAX); d[k] = 0;
        priority_queue<pair<int,int>, vector<pair<int,int>>, greater<>> pq; pq.push({0, k});
        while (!pq.empty()) {
            auto [du, u] = pq.top(); pq.pop();
            if (du > d[u]) continue;
            for (auto [v, w] : adj[u]) if (du + w < d[v]) { d[v] = du + w; pq.push({d[v], v}); }
        }
        int ans = *max_element(d.begin() + 1, d.end());
        return ans == INT_MAX ? -1 : ans;
    }
};
```

**Traps**

- Not skipping stale heap entries (still correct, slower)
- 1-indexed nodes

**Interviewers ask**

- Cheapest flights within K stops (Bellman-Ford / BFS by stops).
- Path with minimum effort.

**Practise**

- [Solve it on LeetCode: Network Delay Time](https://leetcode.com/problems/network-delay-time/)

**Related:** [Dijkstra and shortest paths](dsa.md#dijkstra-and-shortest-paths)

[Back to the topic list](#topics)

## Number of Provinces

*Level 2: Interview-ready*

Pattern: DSU. Connected components; a clean place to show Union-Find.

**Key idea**

Each city starts alone. For every connected pair, union their sets; each successful union reduces the count of components by one.


**Points**

- parent\[i\] = i; comps = n
- For i \< j with isConnected\[i\]\[j\]: if unite(i, j), comps−−
- Complexity: O(n² α(n)) time, O(n) space

```cpp
class Solution {
    vector<int> p;
    int find(int x) { return p[x] == x ? x : p[x] = find(p[x]); }
public:
    int findCircleNum(vector<vector<int>>& g) {
        int n = g.size(), comps = n; p.resize(n); iota(p.begin(), p.end(), 0);
        for (int i = 0; i < n; i++) for (int j = i + 1; j < n; j++)
            if (g[i][j]) { int a = find(i), b = find(j); if (a != b) { p[a] = b; comps--; } }
        return comps;
    }
};
```

**Traps**

- Comparing raw parents instead of roots

**Interviewers ask**

- Solve it with DFS too.
- Redundant connection.
- Accounts merge.

**Practise**

- [Solve it on LeetCode: Number of Provinces](https://leetcode.com/problems/number-of-provinces/)

**Related:** [Disjoint set union (Union-Find)](dsa.md#disjoint-set-union-union-find)

[Back to the topic list](#topics)

## House Robber

*Level 2: Interview-ready*

Pattern: DP. The first DP most interviewers ask.

**Key idea**

At house i you either rob it (take a\[i\] + best up to i−2) or skip it (best up to i−1). Only the last two values are needed.


**Points**

- dp\[i\] = max(dp\[i−1\], dp\[i−2\] + a\[i\])
- Keep two variables
- Complexity: O(n) time, O(1) space

```cpp
class Solution {
public:
    int rob(vector<int>& a) {
        int prev2 = 0, prev1 = 0;
        for (int x : a) { int cur = max(prev1, prev2 + x); prev2 = prev1; prev1 = cur; }
        return prev1;
    }
};
```

**Traps**

- Greedy 'take every other house'

**Interviewers ask**

- Houses in a circle (House Robber II).
- Houses on a tree (House Robber III).

**Practise**

- [Solve it on LeetCode: House Robber](https://leetcode.com/problems/house-robber/)

**Related:** [Dynamic programming](dsa.md#dynamic-programming)

[Back to the topic list](#topics)

## Coin Change

*Level 2: Interview-ready*

Pattern: Knapsack. Most-asked unbounded-knapsack problem; greedy fails on it.

**Key idea**

dp\[x\] = fewest coins to make x. dp\[x\] = min over coins c ≤ x of dp\[x − c\] + 1. Greedy fails (coins 1, 3, 4 for 6: greedy gives 3, best is 2).


**Points**

- dp\[0\] = 0, others = ∞
- For x in 1..amount, for c: dp\[x\] = min(dp\[x\], dp\[x−c\] + 1)
- Answer dp\[amount\] or −1
- Complexity: O(amount × coins) time, O(amount) space

```cpp
class Solution {
public:
    int coinChange(vector<int>& coins, int amount) {
        vector<int> dp(amount + 1, INT_MAX); dp[0] = 0;
        for (int x = 1; x <= amount; x++)
            for (int c : coins) if (c <= x && dp[x - c] != INT_MAX) dp[x] = min(dp[x], dp[x - c] + 1);
        return dp[amount] == INT_MAX ? -1 : dp[amount];
    }
};
```

**Traps**

- INT\_MAX + 1 overflow
- Using greedy

**Interviewers ask**

- Count the number of ways (Coin Change II: coins in the outer loop).
- Print the coins used.

**Practise**

- [Solve it on LeetCode: Coin Change](https://leetcode.com/problems/coin-change/)

**Related:** [Knapsack and subset DP](dsa.md#knapsack-and-subset-dp)

[Back to the topic list](#topics)

## Longest Increasing Subsequence

*Level 2: Interview-ready*

Pattern: DP. Asked for both the O(n²) DP and the O(n log n) follow-up.

**Key idea**

O(n²): dp\[i\] = 1 + max dp\[j\] for j \< i with a\[j\] \< a\[i\]. O(n log n): keep tails\[len\] = smallest possible tail of an increasing subsequence of length len+1; for each x, replace the first tail ≥ x (lower\_bound) or append.


**Points**

- tails = \[\]
- For x: it = lower\_bound(tails, x); replace or push\_back
- Answer = tails.size()
- Complexity: O(n log n) time, O(n) space

```cpp
class Solution {
public:
    int lengthOfLIS(vector<int>& a) {
        vector<int> tails;
        for (int x : a) {
            auto it = lower_bound(tails.begin(), tails.end(), x);
            if (it == tails.end()) tails.push_back(x); else *it = x;
        }
        return tails.size();
    }
};
```

**Traps**

- Thinking tails is the subsequence itself (it isn't)
- upper\_bound for strictly increasing (use lower\_bound)

**Interviewers ask**

- Print the actual subsequence.
- Russian doll envelopes (Hard).

**Practise**

- [Solve it on LeetCode: Longest Increasing Subsequence](https://leetcode.com/problems/longest-increasing-subsequence/)

**Related:** [Dynamic programming](dsa.md#dynamic-programming)

[Back to the topic list](#topics)

## Longest Common Subsequence

*Level 2: Interview-ready*

Pattern: String DP. The base of all two-string DP.

**Key idea**

dp\[i\]\[j\] = LCS of a\[0..i) and b\[0..j). If a\[i−1\] == b\[j−1\], dp\[i\]\[j\] = dp\[i−1\]\[j−1\] + 1; else max(dp\[i−1\]\[j\], dp\[i\]\[j−1\]).


**Points**

- (n+1) × (m+1) table, row/column 0 are 0
- Fill row by row
- Space-optimise to two rows
- Complexity: O(n × m) time, O(m) space

```cpp
class Solution {
public:
    int longestCommonSubsequence(string a, string b) {
        int n = a.size(), m = b.size();
        vector<int> prev(m + 1, 0), cur(m + 1, 0);
        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= m; j++)
                cur[j] = a[i - 1] == b[j - 1] ? prev[j - 1] + 1 : max(prev[j], cur[j - 1]);
            swap(prev, cur);
        }
        return prev[m];
    }
};
```

**Traps**

- Mixing string index i−1 with dp index i

**Interviewers ask**

- Print the LCS.
- Shortest common supersequence.
- Longest palindromic subsequence.

**Practise**

- [Solve it on LeetCode: Longest Common Subsequence](https://leetcode.com/problems/longest-common-subsequence/)

**Related:** [String DP: LCS and edit distance](dsa.md#string-dp-lcs-and-edit-distance)

[Back to the topic list](#topics)

## Edit Distance

*Level 2: Interview-ready*

Pattern: String DP. Google, Amazon, Microsoft; real-world use in spell checkers and diff.

**Key idea**

dp\[i\]\[j\] = edits to turn a\[0..i) into b\[0..j). Equal last characters cost nothing (diagonal). Otherwise 1 + min(insert dp\[i\]\[j−1\], delete dp\[i−1\]\[j\], replace dp\[i−1\]\[j−1\]). Base: dp\[i\]\[0\] = i, dp\[0\]\[j\] = j.


**Points**

- Fill base row and column
- Apply the transition
- Answer dp\[n\]\[m\]
- Complexity: O(n × m) time and space (O(m) with two rows)

```cpp
class Solution {
public:
    int minDistance(string a, string b) {
        int n = a.size(), m = b.size();
        vector<vector<int>> dp(n + 1, vector<int>(m + 1));
        for (int i = 0; i <= n; i++) dp[i][0] = i;
        for (int j = 0; j <= m; j++) dp[0][j] = j;
        for (int i = 1; i <= n; i++) for (int j = 1; j <= m; j++)
            dp[i][j] = a[i - 1] == b[j - 1] ? dp[i - 1][j - 1] : 1 + min({dp[i][j - 1], dp[i - 1][j], dp[i - 1][j - 1]});
        return dp[n][m];
    }
};
```

**Traps**

- Wrong base cases

**Interviewers ask**

- Reduce to O(min(n, m)) space.
- One edit distance (O(n)).

**Practise**

- [Solve it on LeetCode: Edit Distance](https://leetcode.com/problems/edit-distance/)

**Related:** [String DP: LCS and edit distance](dsa.md#string-dp-lcs-and-edit-distance)

[Back to the topic list](#topics)

## Partition Equal Subset Sum

*Level 2: Interview-ready*

Pattern: Knapsack. 0/1 knapsack in disguise; Amazon and Meta.

**Key idea**

Equal halves exist iff some subset sums to total/2 (total must be even). Boolean 0/1 knapsack over sums, iterating sums downwards so each number is used once.


**Points**

- If total is odd → false
- dp\[0\] = true; for x: for s = T..x: dp\[s\] \|= dp\[s − x\]
- Complexity: O(n × total) time, O(total) space

```cpp
class Solution {
public:
    bool canPartition(vector<int>& a) {
        int total = accumulate(a.begin(), a.end(), 0);
        if (total % 2) return false;
        int T = total / 2; vector<char> dp(T + 1, 0); dp[0] = 1;
        for (int x : a) for (int s = T; s >= x; s--) dp[s] |= dp[s - x];
        return dp[T];
    }
};
```

**Traps**

- Iterating sums upwards (reuses a number)

**Interviewers ask**

- Use a bitset for speed.
- Target sum (count sign assignments).

**Practise**

- [Solve it on LeetCode: Partition Equal Subset Sum](https://leetcode.com/problems/partition-equal-subset-sum/)

**Related:** [Knapsack and subset DP](dsa.md#knapsack-and-subset-dp)

[Back to the topic list](#topics)

## Subsets

*Level 2: Interview-ready*

Pattern: Backtracking. The entry point to backtracking; often followed by Subsets II.

**Key idea**

Each element is either in or out: a binary decision tree with 2ⁿ leaves. Recurse with pick / skip, or iterate: for each element, copy every existing subset and add it.


**Points**

- go(i): if i == n, record
- Pick a\[i\], go(i+1), unpick; go(i+1)
- Complexity: O(n × 2ⁿ) time, O(n) recursion depth

```cpp
class Solution {
    vector<vector<int>> res; vector<int> cur;
    void go(vector<int>& a, int i) {
        if (i == (int)a.size()) { res.push_back(cur); return; }
        cur.push_back(a[i]); go(a, i + 1); cur.pop_back();
        go(a, i + 1);
    }
public:
    vector<vector<int>> subsets(vector<int>& a) { go(a, 0); return res; }
};
```

**Traps**

- Forgetting to pop after the pick branch

**Interviewers ask**

- Subsets II with duplicates (sort, skip equal siblings).
- Do it with bitmasks.

**Practise**

- [Solve it on LeetCode: Subsets](https://leetcode.com/problems/subsets/)

**Related:** [Recursion and backtracking](dsa.md#recursion-and-backtracking)

[Back to the topic list](#topics)

## Merge Intervals

*Level 2: Interview-ready*

Pattern: Intervals. Top-asked at Google, Meta, Bloomberg.

**Key idea**

Sort by start. Walk once: if the current interval starts before the last merged one ends, extend the end; otherwise start a new merged interval.


**Points**

- Sort by start
- If start ≤ last.end: last.end = max(last.end, end); else push
- Complexity: O(n log n) time, O(n) output

```cpp
class Solution {
public:
    vector<vector<int>> merge(vector<vector<int>>& iv) {
        sort(iv.begin(), iv.end());
        vector<vector<int>> res;
        for (auto& x : iv) {
            if (!res.empty() && x[0] <= res.back()[1]) res.back()[1] = max(res.back()[1], x[1]);
            else res.push_back(x);
        }
        return res;
    }
};
```

**Traps**

- Setting end = x.end instead of max (a long interval swallowing a short one)

**Interviewers ask**

- Insert interval.
- Meeting rooms II (minimum rooms).

**Practise**

- [Solve it on LeetCode: Merge Intervals](https://leetcode.com/problems/merge-intervals/)

**Related:** [Interval problems](dsa.md#interval-problems)

[Back to the topic list](#topics)

## Kth Largest Element in an Array

*Level 2: Interview-ready*

Pattern: Heap. Asked with the follow-up 'can you beat O(n log n)?'.

**Key idea**

Keep a min-heap of size k: its top is the k-th largest. Quickselect averages O(n).


**Points**

- Push each x; pop when size \> k
- Return top
- Complexity: O(n log k) time, O(k) space

```cpp
class Solution {
public:
    int findKthLargest(vector<int>& a, int k) {
        priority_queue<int, vector<int>, greater<int>> pq;
        for (int x : a) { pq.push(x); if ((int)pq.size() > k) pq.pop(); }
        return pq.top();
    }
};
```

**Traps**

- Max-heap of everything (O(n log n))

**Interviewers ask**

- Quickselect (average O(n), worst O(n²)).
- nth\_element in C++.

**Practise**

- [Solve it on LeetCode: Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/)

**Related:** [Heaps and priority queues](dsa.md#heaps-and-priority-queues)

[Back to the topic list](#topics)

## Implement Trie (Prefix Tree)

*Level 2: Interview-ready*

Pattern: Trie. Common design-style question; base for autocomplete and Word Search II.

**Key idea**

Each node has 26 children and an end-of-word flag. Insert walks/creates nodes; search walks and checks the flag; startsWith only walks.


**Points**

- insert: create missing children, mark end
- search: walk, return end flag
- startsWith: walk, return true
- Complexity: O(length) per operation, O(total characters × 26) space

```cpp
class Trie {
    struct Node { Node* ch[26] = {}; bool end = false; };
    Node* root = new Node();
    Node* walk(const string& w) { Node* n = root; for (char c : w) { n = n->ch[c - 'a']; if (!n) return nullptr; } return n; }
public:
    void insert(string w) { Node* n = root; for (char c : w) { if (!n->ch[c - 'a']) n->ch[c - 'a'] = new Node(); n = n->ch[c - 'a']; } n->end = true; }
    bool search(string w) { Node* n = walk(w); return n && n->end; }
    bool startsWith(string p) { return walk(p) != nullptr; }
};
```

**Traps**

- Leaking memory (mention a destructor or arena)

**Interviewers ask**

- Word Search II.
- Autocomplete top-3 suggestions.
- Max XOR with a bit trie.

**Practise**

- [Solve it on LeetCode: Implement Trie (Prefix Tree)](https://leetcode.com/problems/implement-trie-prefix-tree/)

**Related:** [Tries](dsa.md#tries)

[Back to the topic list](#topics)

## Jump Game

*Level 2: Interview-ready*

Pattern: Greedy. A short greedy problem that tests whether you'd reach for DP unnecessarily.

**Key idea**

Track the furthest index reachable so far. If you ever stand on an index beyond it, you're stuck.


**Points**

- reach = 0
- For i: if i \> reach → false; reach = max(reach, i + a\[i\])
- Complexity: O(n) time, O(1) space

```cpp
class Solution {
public:
    bool canJump(vector<int>& a) {
        int reach = 0;
        for (int i = 0; i < (int)a.size(); i++) { if (i > reach) return false; reach = max(reach, i + a[i]); }
        return true;
    }
};
```

**Traps**

- O(n²) DP when greedy suffices

**Interviewers ask**

- Minimum number of jumps (Jump Game II, greedy BFS by levels).

**Practise**

- [Solve it on LeetCode: Jump Game](https://leetcode.com/problems/jump-game/)

**Related:** [Greedy algorithms](dsa.md#greedy-algorithms)

[Back to the topic list](#topics)

## Find Median from Data Stream

*Level 3: Advanced*

Pattern: Heap. Classic two-heap design; Google, Amazon, Microsoft.

**Key idea**

Keep the smaller half in a max-heap and the larger half in a min-heap, sizes equal or the max-heap one bigger. The median is the max-heap top, or the average of both tops.


**Points**

- Push to lo (max-heap), move lo's top to hi
- If hi is bigger, move hi's top back to lo
- Median from the tops
- Complexity: O(log n) per add, O(1) median

```cpp
class MedianFinder {
    priority_queue<int> lo;                                   // max-heap: smaller half
    priority_queue<int, vector<int>, greater<int>> hi;        // min-heap: larger half
public:
    void addNum(int x) {
        lo.push(x); hi.push(lo.top()); lo.pop();
        if (hi.size() > lo.size()) { lo.push(hi.top()); hi.pop(); }
    }
    double findMedian() { return lo.size() > hi.size() ? lo.top() : (lo.top() + (double)hi.top()) / 2.0; }
};
```

**Traps**

- Integer division when averaging
- int overflow when adding two big tops (cast first)

**Interviewers ask**

- If all numbers are in 0..100? (counting array)
- Sliding window median.

**Practise**

- [Solve it on LeetCode: Find Median from Data Stream](https://leetcode.com/problems/find-median-from-data-stream/)

**Related:** [Heaps and priority queues](dsa.md#heaps-and-priority-queues)

[Back to the topic list](#topics)

## Rotate Image

*Level 2: Interview-ready*

Pattern: Matrix. A common in-place matrix warm-up.

**Key idea**

Rotating 90° clockwise in place = transpose (swap a\[i\]\[j\] with a\[j\]\[i\]) then reverse each row.


**Points**

- Transpose: for i \< j swap
- Reverse every row
- Complexity: O(n²) time, O(1) space

```cpp
class Solution {
public:
    void rotate(vector<vector<int>>& a) {
        int n = a.size();
        for (int i = 0; i < n; i++) for (int j = i + 1; j < n; j++) swap(a[i][j], a[j][i]);
        for (auto& row : a) reverse(row.begin(), row.end());
    }
};
```

**Traps**

- Swapping every (i, j) pair twice by looping j from 0

**Interviewers ask**

- Rotate anticlockwise (reverse rows first, or transpose then reverse columns).

**Practise**

- [Solve it on LeetCode: Rotate Image](https://leetcode.com/problems/rotate-image/)

**Related:** [Time and space complexity](dsa.md#time-and-space-complexity)

[Back to the topic list](#topics)

## Spiral Matrix

*Level 2: Interview-ready*

Pattern: Matrix. Tests careful boundary handling.

**Key idea**

Keep four boundaries (top, bottom, left, right). Walk right along top, down the right side, left along bottom, up the left side, shrinking each boundary after use; check the boundaries before the last two walks.


**Points**

- Loop while top ≤ bottom and left ≤ right
- Guard the bottom and left walks with top ≤ bottom and left ≤ right
- Complexity: O(mn) time, O(1) extra

```cpp
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

**Traps**

- Missing the guards, so a single row or column is printed twice

**Interviewers ask**

- Generate an n × n spiral matrix (Spiral Matrix II).

**Practise**

- [Solve it on LeetCode: Spiral Matrix](https://leetcode.com/problems/spiral-matrix/)

**Related:** [Time and space complexity](dsa.md#time-and-space-complexity)

[Back to the topic list](#topics)

## Set Matrix Zeroes

*Level 2: Interview-ready*

Pattern: Matrix. The O(1)-space follow-up is the real question.

**Key idea**

Use the first row and first column as markers for which rows and columns to clear, and two flags for whether row 0 and column 0 themselves need clearing. Clear the inner cells first, row 0 and column 0 last.


**Points**

- Record zero in row 0 / col 0 flags
- Mark a\[i\]\[0\] = a\[0\]\[j\] = 0 for inner zeros
- Clear inner cells from marks, then row 0 and col 0
- Complexity: O(mn) time, O(1) extra

```cpp
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

**Traps**

- Clearing row 0 before reading its marks

**Interviewers ask**

- Why not just mark cells with -1? (values can be any integer)

**Practise**

- [Solve it on LeetCode: Set Matrix Zeroes](https://leetcode.com/problems/set-matrix-zeroes/)

**Related:** [Time and space complexity](dsa.md#time-and-space-complexity)

[Back to the topic list](#topics)

## Next Permutation

*Level 2: Interview-ready*

Pattern: Two pointers. A classic in-place array question.

**Key idea**

From the right, find the first i with a\[i\] \< a\[i+1\] (the pivot). If none, reverse the whole array. Otherwise swap a\[i\] with the rightmost element greater than it, then reverse the suffix after i (it was descending).


**Points**

- Find pivot i
- Find j \> i from the right with a\[j\] \> a\[i\]; swap
- Reverse a\[i+1..\]
- Complexity: O(n) time, O(1) space

```cpp
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

**Traps**

- Using \> instead of \>= with duplicates

**Interviewers ask**

- What does std::next\_permutation return?

**Practise**

- [Solve it on LeetCode: Next Permutation](https://leetcode.com/problems/next-permutation/)

**Related:** [Two pointers](dsa.md#two-pointers)

[Back to the topic list](#topics)

## Sort Colors (Dutch national flag)

*Level 2: Interview-ready*

Pattern: Two pointers. Three-pointer partitioning; asked often as a one-pass follow-up.

**Key idea**

Keep low (next place for 0), mid (current), high (next place for 2). A 0 swaps to low and both advance; a 1 just advances mid; a 2 swaps to high and only high moves back, because the swapped-in value is unchecked.


**Points**

- low = mid = 0, high = n−1
- while mid ≤ high: by a\[mid\] swap and move
- Complexity: O(n) time, O(1) space

```cpp
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

**Traps**

- Advancing mid after swapping with high

**Interviewers ask**

- Counting sort works too: why is one pass better?

**Practise**

- [Solve it on LeetCode: Sort Colors (Dutch national flag)](https://leetcode.com/problems/sort-colors/)

**Related:** [Two pointers](dsa.md#two-pointers)

[Back to the topic list](#topics)

## Search a 2D Matrix

*Level 2: Interview-ready*

Pattern: Binary search. Binary search over a matrix treated as one sorted array.

**Key idea**

Rows are sorted and each row starts after the previous ends, so index k maps to cell (k / n, k % n). Binary search k over 0..mn−1.


**Points**

- lo = 0, hi = mn − 1
- v = a\[mid / n\]\[mid % n\]
- Complexity: O(log mn) time

```cpp
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

**Traps**

- Using m instead of n in the index mapping

**Interviewers ask**

- Search a 2D Matrix II (rows and columns sorted separately): start at the top-right corner.

**Practise**

- [Solve it on LeetCode: Search a 2D Matrix](https://leetcode.com/problems/search-a-2d-matrix/)

**Related:** [Binary search](dsa.md#binary-search)

[Back to the topic list](#topics)

## Majority Element (Boyer–Moore)

*Level 1: Core*

Pattern: Hashing. Short, but the O(1)-space voting idea is what interviewers look for.

**Key idea**

Pair each majority element with a different element and cancel; the majority survives. Keep a candidate and a count: on count 0 take the current element, add 1 if equal, else subtract 1.


**Points**

- cand, cnt = 0
- for x: if cnt == 0 cand = x; cnt += (x == cand) ? 1 : −1
- Complexity: O(n) time, O(1) space

```cpp
class Solution {
public:
    int majorityElement(vector<int>& a) {
        int cand = 0, cnt = 0;
        for (int x : a) { if (cnt == 0) cand = x; cnt += (x == cand) ? 1 : -1; }
        return cand;
    }
};
```

**Traps**

- Forgetting to verify when a majority is not guaranteed

**Interviewers ask**

- Majority Element II: all elements appearing more than n/3 times (two candidates, then verify).

**Practise**

- [Solve it on LeetCode: Majority Element (Boyer–Moore)](https://leetcode.com/problems/majority-element/)

**Related:** [Hashing and frequency maps](dsa.md#hashing-and-frequency-maps)

[Back to the topic list](#topics)

## Find the Duplicate Number

*Level 2: Interview-ready*

Pattern: Linked list. Floyd's cycle detection on an array; a favourite 'no extra space' twist.

**Key idea**

Values are in 1..n with n+1 slots, so treat i → a\[i\] as a linked list. The duplicate is where two pointers point to the same node: the entrance of the cycle. Find it with slow/fast pointers, then restart one from the start.


**Points**

- slow = a\[slow\], fast = a\[a\[fast\]\] until they meet
- slow = a\[0\]... walk both one step until equal
- Complexity: O(n) time, O(1) space, array unmodified

```cpp
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

**Traps**

- Sorting or marking (modifies the array, which the problem forbids)

**Interviewers ask**

- Prove why the meeting point leads to the cycle entrance.

**Practise**

- [Solve it on LeetCode: Find the Duplicate Number](https://leetcode.com/problems/find-the-duplicate-number/)

**Related:** [Linked lists](dsa.md#linked-lists)

[Back to the topic list](#topics)

## Merge Sorted Array

*Level 1: Core*

Pattern: Two pointers. Easy, but merging from the back is the trick.

**Key idea**

Fill a from the end: compare the largest remaining of each array and place it at the back. No element of a is overwritten before it is read.


**Points**

- i = m−1, j = n−1, k = m+n−1
- while j ≥ 0: take the larger of a\[i\], b\[j\]
- Complexity: O(m + n) time, O(1) space

```cpp
class Solution {
public:
    void merge(vector<int>& a, int m, vector<int>& b, int n) {
        int i = m - 1, j = n - 1, k = m + n - 1;
        while (j >= 0) a[k--] = (i >= 0 && a[i] > b[j]) ? a[i--] : b[j--];
    }
};
```

**Traps**

- Merging from the front and overwriting a

**Interviewers ask**

- Merge without extra space when both arrays are full (gap method).

**Practise**

- [Solve it on LeetCode: Merge Sorted Array](https://leetcode.com/problems/merge-sorted-array/)

**Related:** [Two pointers](dsa.md#two-pointers)

[Back to the topic list](#topics)

## Longest Palindromic Substring

*Level 2: Interview-ready*

Pattern: Two pointers. Asked everywhere; expand-around-centre beats the DP table in memory.

**Key idea**

Every palindrome has a centre: a character (odd length) or a gap between two (even). Expand outwards from each of the 2n−1 centres while the ends match; keep the longest.


**Points**

- for each i: expand(i, i) and expand(i, i+1)
- Track best start and length
- Complexity: O(n²) time, O(1) space

```cpp
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

**Traps**

- Forgetting even-length centres

**Interviewers ask**

- Manacher's algorithm gives O(n): explain the idea.

**Practise**

- [Solve it on LeetCode: Longest Palindromic Substring](https://leetcode.com/problems/longest-palindromic-substring/)

**Related:** [Two pointers](dsa.md#two-pointers)

[Back to the topic list](#topics)

## Palindromic Substrings

*Level 2: Interview-ready*

Pattern: Two pointers. Same centres as the previous problem, counting instead of keeping the best.

**Key idea**

Expand from all 2n−1 centres; every successful expansion step is one more palindromic substring.


**Points**

- count += expansions from (i, i) and (i, i+1)
- Complexity: O(n²) time, O(1) space

```cpp
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

**Traps**

- Double-counting by expanding the same centre twice

**Interviewers ask**

- Palindrome Partitioning II (minimum cuts).

**Practise**

- [Solve it on LeetCode: Palindromic Substrings](https://leetcode.com/problems/palindromic-substrings/)

**Related:** [Two pointers](dsa.md#two-pointers)

[Back to the topic list](#topics)

## Minimum Size Subarray Sum

*Level 2: Interview-ready*

Pattern: Sliding window. The 'shortest window' version of sliding window.

**Key idea**

All numbers are positive, so the window sum grows when you expand and shrinks when you move left. Expand right; while the sum is at least target, record the length and shrink from the left.


**Points**

- sum += a\[r\]
- while sum ≥ target: best = min(best, r−l+1); sum −= a\[l++\]
- Complexity: O(n) time, O(1) space

```cpp
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

**Traps**

- Using it with negative numbers (then you need prefix sums + a deque)

**Interviewers ask**

- Shortest subarray with sum at least K with negatives (LeetCode 862).

**Practise**

- [Solve it on LeetCode: Minimum Size Subarray Sum](https://leetcode.com/problems/minimum-size-subarray-sum/)

**Related:** [Sliding window](dsa.md#sliding-window)

[Back to the topic list](#topics)

## Sliding Window Maximum

*Level 3: Advanced*

Pattern: Monotonic deque. Hard favourite; the monotonic deque is the pattern to learn.

**Key idea**

Keep indices in a deque whose values decrease from front to back. Drop the front when it leaves the window; before pushing i, pop smaller values from the back (they can never be a maximum again). The front is the window's maximum.


**Points**

- pop front if out of window
- pop back while a\[back\] ≤ a\[i\]; push i
- record a\[front\] once i ≥ k−1
- Complexity: O(n) time, O(k) space

```cpp
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

**Traps**

- Storing values instead of indices (cannot tell when they leave)

**Interviewers ask**

- Why is it O(n) with the inner while loop?

**Practise**

- [Solve it on LeetCode: Sliding Window Maximum](https://leetcode.com/problems/sliding-window-maximum/)

**Related:** [Monotonic stack](dsa.md#monotonic-stack)

[Back to the topic list](#topics)

## Permutation in String

*Level 2: Interview-ready*

Pattern: Sliding window. Fixed-size window with character counts.

**Key idea**

A permutation of s1 is a window of length \|s1\| in s2 with the same letter counts. Slide a fixed window and compare two 26-count arrays (or track how many letters match).


**Points**

- Count s1
- Slide window of size \|s1\| over s2, updating counts
- Return true when counts are equal
- Complexity: O(26·n) time, O(1) space

```cpp
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

**Traps**

- Off-by-one when removing the left character

**Interviewers ask**

- Find All Anagrams in a String (return every start index).

**Practise**

- [Solve it on LeetCode: Permutation in String](https://leetcode.com/problems/permutation-in-string/)

**Related:** [Sliding window](dsa.md#sliding-window)

[Back to the topic list](#topics)

## Word Search

*Level 2: Interview-ready*

Pattern: Backtracking. Grid backtracking; tests marking and unmarking visited cells.

**Key idea**

Start a DFS from every cell that matches the first letter. Mark the cell as used, recurse into 4 neighbours for the next letter, and unmark on the way back.


**Points**

- dfs(r, c, i): bounds and letter check
- mark, try 4 directions, unmark
- Complexity: O(mn · 3^L) time, O(L) recursion

```cpp
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

**Traps**

- Forgetting to unmark, so later paths cannot reuse the cell

**Interviewers ask**

- Word Search II: many words at once (trie + DFS).

**Practise**

- [Solve it on LeetCode: Word Search](https://leetcode.com/problems/word-search/)

**Related:** [Recursion and backtracking](dsa.md#recursion-and-backtracking)

[Back to the topic list](#topics)

## Combination Sum

*Level 2: Interview-ready*

Pattern: Backtracking. The standard 'choose with repetition' backtracking.

**Key idea**

Each candidate can be used many times. Recurse with the remaining target, starting from the current index (not i+1) so the same number can repeat, and only moving forward so combinations aren't repeated in different orders.


**Points**

- go(start, remaining)
- for i ≥ start with c\[i\] ≤ remaining: pick, go(i, remaining − c\[i\]), unpick
- Complexity: Exponential in the target; recursion depth ≤ target / min

```cpp
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

**Traps**

- Starting the loop at 0 (duplicate combinations in different orders)

**Interviewers ask**

- Combination Sum II: each number once, with duplicates in the input.

**Practise**

- [Solve it on LeetCode: Combination Sum](https://leetcode.com/problems/combination-sum/)

**Related:** [Recursion and backtracking](dsa.md#recursion-and-backtracking)

[Back to the topic list](#topics)

## Permutations II

*Level 2: Interview-ready*

Pattern: Backtracking. Permutations with duplicate values: the skip rule is the test.

**Key idea**

Sort, then build permutations with a used\[\] array. Skip a value if it equals the previous value and the previous copy is not currently used: that order was already generated.


**Points**

- sort
- skip i if used\[i\] or (i \> 0 and a\[i\] == a\[i−1\] and !used\[i−1\])
- Complexity: O(n · n!) time, O(n) space

```cpp
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

**Traps**

- Using a set of results to dedupe (works, but slow and noticed)

**Interviewers ask**

- Why does the !used\[i−1\] condition work?

**Practise**

- [Solve it on LeetCode: Permutations II](https://leetcode.com/problems/permutations-ii/)

**Related:** [Recursion and backtracking](dsa.md#recursion-and-backtracking)

[Back to the topic list](#topics)

## N-Queens

*Level 3: Advanced*

Pattern: Backtracking. The classic Hard backtracking problem.

**Key idea**

Place one queen per row. A column c is safe in row r if no queen uses column c, diagonal r−c, or anti-diagonal r+c. Track those three in boolean arrays for O(1) checks.


**Points**

- go(row): if row == n record the board
- for each col safe: place, mark three arrays, recurse, unmark
- Complexity: O(n!) time, O(n) space

```cpp
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

**Traps**

- Wrong diagonal index (r − c can be negative: offset by n − 1)

**Interviewers ask**

- Count only (N-Queens II); do it with bitmasks.

**Practise**

- [Solve it on LeetCode: N-Queens](https://leetcode.com/problems/n-queens/)

**Related:** [Recursion and backtracking](dsa.md#recursion-and-backtracking)

[Back to the topic list](#topics)

## Decode Ways

*Level 2: Interview-ready*

Pattern: DP. A 1-D DP with tricky zeros.

**Key idea**

dp\[i\] = ways to decode the first i characters. The last char alone works if it isn't '0' (add dp\[i−1\]); the last two work if they form 10..26 (add dp\[i−2\]).


**Points**

- dp\[0\] = 1
- single digit 1..9 → += dp\[i−1\]
- two digits 10..26 → += dp\[i−2\]
- Complexity: O(n) time, O(n) space (O(1) with two variables)

```cpp
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

**Traps**

- Treating '06' as valid

**Interviewers ask**

- Decode Ways II with '\*' wildcards.

**Practise**

- [Solve it on LeetCode: Decode Ways](https://leetcode.com/problems/decode-ways/)

**Related:** [Dynamic programming](dsa.md#dynamic-programming)

[Back to the topic list](#topics)

## Unique Paths

*Level 2: Interview-ready*

Pattern: DP. The first grid DP; often followed by obstacles.

**Key idea**

You reach a cell only from above or from the left, so dp\[i\]\[j\] = dp\[i−1\]\[j\] + dp\[i\]\[j−1\]. One row is enough: dp\[j\] += dp\[j−1\].


**Points**

- dp = row of 1s
- for each next row: dp\[j\] += dp\[j−1\]
- Complexity: O(mn) time, O(n) space

```cpp
class Solution {
public:
    int uniquePaths(int m, int n) {
        vector<long long> dp(n, 1);
        for (int i = 1; i < m; i++) for (int j = 1; j < n; j++) dp[j] += dp[j - 1];
        return dp[n - 1];
    }
};
```

**Traps**

- Using int for big grids

**Interviewers ask**

- With obstacles (Unique Paths II).
- Closed form: C(m+n−2, m−1).

**Practise**

- [Solve it on LeetCode: Unique Paths](https://leetcode.com/problems/unique-paths/)

**Related:** [Dynamic programming](dsa.md#dynamic-programming)

[Back to the topic list](#topics)

## Word Break

*Level 2: Interview-ready*

Pattern: DP. The standard 'can the prefix be built' DP.

**Key idea**

dp\[i\] is true if s\[0..i) can be split into dictionary words. dp\[i\] is true if some j \< i has dp\[j\] true and s\[j..i) in the dictionary.


**Points**

- dp\[0\] = true; put words in a hash set
- for i, for j \< i: if dp\[j\] and s.substr(j, i−j) in set → dp\[i\] = true
- Complexity: O(n² · L) time, O(n) space

```cpp
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

**Traps**

- Greedy longest-match (fails on 'catsandog'-style inputs)

**Interviewers ask**

- Word Break II: return all sentences (DP + backtracking with memo).

**Practise**

- [Solve it on LeetCode: Word Break](https://leetcode.com/problems/word-break/)

**Related:** [Dynamic programming](dsa.md#dynamic-programming)

[Back to the topic list](#topics)

## Maximum Product Subarray

*Level 2: Interview-ready*

Pattern: Kadane. Kadane's twist: a negative number swaps max and min.

**Key idea**

Track both the largest and smallest product ending here. A negative number turns the smallest into the largest, so swap them before multiplying.


**Points**

- if x \< 0 swap(hi, lo)
- hi = max(x, hi·x), lo = min(x, lo·x), best = max(best, hi)
- Complexity: O(n) time, O(1) space

```cpp
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

**Traps**

- Tracking only the maximum

**Interviewers ask**

- Why does a zero reset both values automatically?

**Practise**

- [Solve it on LeetCode: Maximum Product Subarray](https://leetcode.com/problems/maximum-product-subarray/)

**Related:** [Dynamic programming](dsa.md#dynamic-programming)

[Back to the topic list](#topics)

## Jump Game II

*Level 2: Interview-ready*

Pattern: Greedy. BFS by levels, done greedily in O(n).

**Key idea**

Think of jumps as BFS levels. Within the current level (up to \`end\`), track the farthest index reachable. When you reach \`end\`, take one jump and set end = farthest.


**Points**

- far = max(far, i + a\[i\])
- if i == end: jumps++, end = far
- Complexity: O(n) time, O(1) space

```cpp
class Solution {
public:
    int jump(vector<int>& a) {
        int jumps = 0, end = 0, far = 0;
        for (int i = 0; i + 1 < (int)a.size(); i++) { far = max(far, i + a[i]); if (i == end) { jumps++; end = far; } }
        return jumps;
    }
};
```

**Traps**

- Looping to the last index (adds an extra jump)

**Interviewers ask**

- Jump Game III / IV (BFS on indices).

**Practise**

- [Solve it on LeetCode: Jump Game II](https://leetcode.com/problems/jump-game-ii/)

**Related:** [Greedy algorithms](dsa.md#greedy-algorithms)

[Back to the topic list](#topics)

## Gas Station

*Level 2: Interview-ready*

Pattern: Greedy. A greedy proof question.

**Key idea**

If total gas \< total cost, no answer. Otherwise run once: whenever the tank goes negative at i, no start between the old start and i works, so restart at i+1.


**Points**

- total += g − c; tank += g − c
- if tank \< 0: start = i + 1, tank = 0
- Complexity: O(n) time, O(1) space

```cpp
class Solution {
public:
    int canCompleteCircuit(vector<int>& g, vector<int>& c) {
        int total = 0, tank = 0, start = 0;
        for (int i = 0; i < (int)g.size(); i++) { total += g[i] - c[i]; tank += g[i] - c[i]; if (tank < 0) { start = i + 1; tank = 0; } }
        return total < 0 ? -1 : start;
    }
};
```

**Traps**

- Trying every start (O(n²))

**Interviewers ask**

- Prove why skipping to i+1 is safe.

**Practise**

- [Solve it on LeetCode: Gas Station](https://leetcode.com/problems/gas-station/)

**Related:** [Greedy algorithms](dsa.md#greedy-algorithms)

[Back to the topic list](#topics)

## Kth Smallest Element in a BST

*Level 2: Interview-ready*

Pattern: BST. Inorder traversal of a BST is sorted.

**Key idea**

An inorder walk visits a BST in ascending order. Walk iteratively with a stack and stop at the k-th node.


**Points**

- push left spine
- pop, k−−, if k == 0 return
- go right
- Complexity: O(h + k) time, O(h) space

```cpp
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

**Traps**

- Collecting the whole inorder list (O(n) memory)

**Interviewers ask**

- If the tree changes often: store subtree sizes in each node.

**Practise**

- [Solve it on LeetCode: Kth Smallest Element in a BST](https://leetcode.com/problems/kth-smallest-element-in-a-bst/)

**Related:** [Binary search trees](dsa.md#binary-search-trees)

[Back to the topic list](#topics)

## Construct Binary Tree from Preorder and Inorder

*Level 2: Interview-ready*

Pattern: Trees. Tests understanding of traversals.

**Key idea**

The first preorder value is the root. Its position in inorder splits left and right subtrees. Use a hash map from value to inorder index so each split is O(1).


**Points**

- map value → inorder index
- build(lo, hi): root = pre\[p++\]; left = build(lo, idx−1); right = build(idx+1, hi)
- Complexity: O(n) time, O(n) space

```cpp
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

**Traps**

- Building the left subtree after the right (preorder order matters)

**Interviewers ask**

- From inorder and postorder: build right first.

**Practise**

- [Solve it on LeetCode: Construct Binary Tree from Preorder and Inorder](https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/)

**Related:** [Binary trees](dsa.md#binary-trees)

[Back to the topic list](#topics)

## Binary Tree Right Side View

*Level 2: Interview-ready*

Pattern: BFS. A level-order variant.

**Key idea**

Do a level-order traversal and record the last node of every level.


**Points**

- queue; for each level of size s, the s-th popped node is visible
- Complexity: O(n) time, O(width) space

```cpp
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

**Traps**

- Only following right children (misses a deeper left node)

**Interviewers ask**

- DFS version: visit right first, record when depth == result size.

**Practise**

- [Solve it on LeetCode: Binary Tree Right Side View](https://leetcode.com/problems/binary-tree-right-side-view/)

**Related:** [BFS and graph basics](dsa.md#bfs-and-graph-basics)

[Back to the topic list](#topics)

## Serialize and Deserialize Binary Tree

*Level 3: Advanced*

Pattern: Trees. A Hard question that mixes traversal and design.

**Key idea**

Preorder with a marker for null ('#') describes the tree uniquely. Serialize recursively; deserialize by reading tokens in the same order.


**Points**

- ser: val, then left, then right; '#' for null
- de: read token; '#' → null; else node, left = de(), right = de()
- Complexity: O(n) time and space

```cpp
class Codec {
    void ser(TreeNode* r, string& s) { if (!r) { s += "# "; return; } s += to_string(r->val) + " "; ser(r->left, s); ser(r->right, s); }
    TreeNode* de(istringstream& in) { string t; in >> t; if (t == "#") return nullptr; TreeNode* r = new TreeNode(stoi(t)); r->left = de(in); r->right = de(in); return r; }
public:
    string serialize(TreeNode* root) { string s; ser(root, s); return s; }
    TreeNode* deserialize(string data) { istringstream in(data); return de(in); }
};
```

**Traps**

- Leaving out null markers (preorder alone is ambiguous)

**Interviewers ask**

- Serialize a BST more compactly (no null markers needed).

**Practise**

- [Solve it on LeetCode: Serialize and Deserialize Binary Tree](https://leetcode.com/problems/serialize-and-deserialize-binary-tree/)

**Related:** [Binary trees](dsa.md#binary-trees)

[Back to the topic list](#topics)

## Diameter of Binary Tree

*Level 1: Core*

Pattern: Trees. Height recursion that updates a global answer.

**Key idea**

The longest path through a node = height(left) + height(right). Compute heights bottom-up and keep the best sum.


**Points**

- h(node) = 1 + max(h(l), h(r))
- best = max(best, h(l) + h(r))
- Complexity: O(n) time, O(h) space

```cpp
class Solution {
    int best = 0;
    int h(TreeNode* r) { if (!r) return 0; int a = h(r->left), b = h(r->right); best = max(best, a + b); return 1 + max(a, b); }
public:
    int diameterOfBinaryTree(TreeNode* root) { h(root); return best; }
};
```

**Traps**

- Assuming the path passes through the root

**Interviewers ask**

- Binary Tree Maximum Path Sum (same shape with values).

**Practise**

- [Solve it on LeetCode: Diameter of Binary Tree](https://leetcode.com/problems/diameter-of-binary-tree/)

**Related:** [Binary trees](dsa.md#binary-trees)

[Back to the topic list](#topics)

## Pacific Atlantic Water Flow

*Level 2: Interview-ready*

Pattern: DFS. Reverse the direction: flow uphill from the oceans.

**Key idea**

Instead of checking every cell, start from each ocean's border and move to neighbours that are at least as high. Cells reached from both oceans are the answer.


**Points**

- DFS from top row + left column → pac
- DFS from bottom row + right column → atl
- answer = cells in both
- Complexity: O(mn) time and space

```cpp
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

**Traps**

- Running a search from every cell (O((mn)²))

**Interviewers ask**

- Same trick: Surrounded Regions, Number of Enclaves.

**Practise**

- [Solve it on LeetCode: Pacific Atlantic Water Flow](https://leetcode.com/problems/pacific-atlantic-water-flow/)

**Related:** [DFS, components and cycles](dsa.md#dfs-components-and-cycles)

[Back to the topic list](#topics)

## Course Schedule II

*Level 2: Interview-ready*

Pattern: Topological sort. Return the actual order (Kahn's algorithm).

**Key idea**

Kahn's algorithm: push all courses with in-degree 0; pop one, add it to the order and lower its neighbours' in-degree. If the order has fewer than n courses, there is a cycle.


**Points**

- edge b → a for \[a, b\]
- queue of in-degree 0
- order.size() \< n → return {}
- Complexity: O(V + E) time and space

```cpp
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

**Traps**

- Reversing the edge direction

**Interviewers ask**

- Alien Dictionary (build the graph from word order).

**Practise**

- [Solve it on LeetCode: Course Schedule II](https://leetcode.com/problems/course-schedule-ii/)

**Related:** [Topological sort](dsa.md#topological-sort)

[Back to the topic list](#topics)

## Clone Graph

*Level 2: Interview-ready*

Pattern: BFS. Deep copy with a visited map.

**Key idea**

Map each original node to its copy. BFS from the start; on seeing a neighbour without a copy, create it and enqueue it; always link the copies.


**Points**

- copy\[start\] = new node
- for each popped u, for v in u's neighbours: create copy if missing, link copy\[u\] → copy\[v\]
- Complexity: O(V + E) time and space

```cpp
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

**Traps**

- Creating a second copy of a node already seen (no map)

**Interviewers ask**

- Copy List with Random Pointer uses the same map idea.

**Practise**

- [Solve it on LeetCode: Clone Graph](https://leetcode.com/problems/clone-graph/)

**Related:** [BFS and graph basics](dsa.md#bfs-and-graph-basics)

[Back to the topic list](#topics)

## Cheapest Flights Within K Stops

*Level 2: Interview-ready*

Pattern: Shortest paths. Shortest path with a limit on edges: Bellman–Ford for k+1 rounds.

**Key idea**

Run Bellman–Ford for k+1 rounds (k stops = k+1 flights). Relax from a copy of the previous round's costs so one round uses only one more flight.


**Points**

- dist\[src\] = 0
- repeat k+1 times: nd = dist; for each flight relax nd\[v\] from dist\[u\]; dist = nd
- Complexity: O(k · E) time, O(n) space

```cpp
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

**Traps**

- Relaxing in place (one round can chain several flights)
- Plain Dijkstra ignores the stop limit

**Interviewers ask**

- Dijkstra with (cost, node, stops) states: when is it faster?

**Practise**

- [Solve it on LeetCode: Cheapest Flights Within K Stops](https://leetcode.com/problems/cheapest-flights-within-k-stops/)

**Related:** [Dijkstra and shortest paths](dsa.md#dijkstra-and-shortest-paths)

[Back to the topic list](#topics)

## Reverse Nodes in k-Group

*Level 3: Advanced*

Pattern: Linked list. Hard pointer manipulation with a dummy node.

**Key idea**

Use a dummy head. For each group: check k nodes exist; reverse them by moving each next node to the front of the group; then advance prev to the group's new tail.


**Points**

- count k nodes ahead; stop if fewer
- k−1 times: move cur-\>next to after prev
- prev = cur (old first node, now last)
- Complexity: O(n) time, O(1) space

```cpp
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

**Traps**

- Reversing a final group that has fewer than k nodes

**Interviewers ask**

- Reverse Linked List II (reverse between positions m and n).

**Practise**

- [Solve it on LeetCode: Reverse Nodes in k-Group](https://leetcode.com/problems/reverse-nodes-in-k-group/)

**Related:** [Linked lists](dsa.md#linked-lists)

[Back to the topic list](#topics)

## Copy List with Random Pointer

*Level 2: Interview-ready*

Pattern: Linked list. Deep copy; the O(1)-space weaving trick is the follow-up.

**Key idea**

Weave a copy after every node (A → A' → B → B'). Then A'.random = A.random-\>next. Finally unweave the two lists.


**Points**

- insert copies
- set random of copies
- split lists
- Complexity: O(n) time, O(1) extra

```cpp
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

**Traps**

- Not restoring the original list

**Interviewers ask**

- Hash-map version: simpler, O(n) extra space.

**Practise**

- [Solve it on LeetCode: Copy List with Random Pointer](https://leetcode.com/problems/copy-list-with-random-pointer/)

**Related:** [Linked lists](dsa.md#linked-lists)

[Back to the topic list](#topics)

## Remove Nth Node From End of List

*Level 2: Interview-ready*

Pattern: Linked list. Two pointers with a gap of n.

**Key idea**

Move a fast pointer n steps ahead of a slow one (both starting at a dummy). Move both until fast reaches the last node; slow-\>next is the node to remove.


**Points**

- dummy → head
- fast moves n steps
- move both until fast-\>next is null; slow-\>next = slow-\>next-\>next
- Complexity: O(n) time, O(1) space, one pass

```cpp
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

**Traps**

- No dummy node, so removing the head breaks

**Interviewers ask**

- Delete the middle node of a linked list.

**Practise**

- [Solve it on LeetCode: Remove Nth Node From End of List](https://leetcode.com/problems/remove-nth-node-from-end-of-list/)

**Related:** [Linked lists](dsa.md#linked-lists)

[Back to the topic list](#topics)

## Non-overlapping Intervals

*Level 2: Interview-ready*

Pattern: Intervals. Interval scheduling: keep the earliest-ending ones.

**Key idea**

To keep the most intervals, sort by end and greedily keep an interval when it starts at or after the last kept end. Removals = n − kept.


**Points**

- sort by end
- keep if start ≥ lastEnd
- Complexity: O(n log n) time, O(1) extra

```cpp
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

**Traps**

- Sorting by start and keeping the first

**Interviewers ask**

- Minimum Number of Arrows to Burst Balloons; Meeting Rooms II (count overlap with a min-heap).

**Practise**

- [Solve it on LeetCode: Non-overlapping Intervals](https://leetcode.com/problems/non-overlapping-intervals/)

**Related:** [Interval problems](dsa.md#interval-problems)

[Back to the topic list](#topics)

## Decode String

*Level 2: Interview-ready*

Pattern: Stack. Nested brackets: a stack of (string so far, repeat count).

**Key idea**

On '\[' push the current string and number, then start fresh. On '\]' pop and append the current string count times to the popped string. Digits build the number; letters extend the current string.


**Points**

- digit → k = k·10 + d
- '\[' → push (cur, k); reset
- '\]' → (prev, k) = pop; cur = prev + cur × k
- Complexity: O(output length) time

```cpp
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

**Traps**

- Reading only single-digit counts

**Interviewers ask**

- Recursive-descent version; Basic Calculator.

**Practise**

- [Solve it on LeetCode: Decode String](https://leetcode.com/problems/decode-string/)

**Related:** [Stacks and queues](dsa.md#stacks-and-queues)

[Back to the topic list](#topics)

## Counting Bits

*Level 1: Core*

Pattern: Bit manipulation. DP on bits.

**Key idea**

i has the same set bits as i \>\> 1, plus its lowest bit. So bits\[i\] = bits\[i \>\> 1\] + (i & 1).


**Points**

- r\[0\] = 0
- r\[i\] = r\[i \>\> 1\] + (i & 1)
- Complexity: O(n) time

```cpp
class Solution {
public:
    vector<int> countBits(int n) { vector<int> r(n + 1, 0); for (int i = 1; i <= n; i++) r[i] = r[i >> 1] + (i & 1); return r; }
};
```

**Traps**

- Calling popcount per number (fine, but not the DP they want)

**Interviewers ask**

- Another recurrence: r\[i\] = r\[i & (i − 1)\] + 1.

**Practise**

- [Solve it on LeetCode: Counting Bits](https://leetcode.com/problems/counting-bits/)

**Related:** [Bit manipulation](dsa.md#bit-manipulation)

[Back to the topic list](#topics)

## Longest Increasing Path in a Matrix

*Level 3: Advanced*

Pattern: DP. DFS with memo on a DAG.

**Key idea**

Strictly increasing moves can never cycle, so the grid is a DAG. memo\[r\]\[c\] = 1 + max over larger neighbours of memo of that neighbour. Each cell is computed once.


**Points**

- dfs(r, c) returns memo if set
- try 4 neighbours with a larger value
- answer = max over all cells
- Complexity: O(mn) time and space

```cpp
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

**Traps**

- DFS without memo (exponential)
- Using a visited array (unneeded: no cycles)

**Interviewers ask**

- Topological-sort (peel by out-degree) version.

**Practise**

- [Solve it on LeetCode: Longest Increasing Path in a Matrix](https://leetcode.com/problems/longest-increasing-path-in-a-matrix/)

**Related:** [Dynamic programming](dsa.md#dynamic-programming)

[Back to the topic list](#topics)
