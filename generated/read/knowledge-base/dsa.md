# DSA

[All categories](README.md) · 32 topics

## Topics

- [Time and space complexity](#time-and-space-complexity)
- [C++ and the STL](#c-and-the-stl)
- [Hashing and frequency maps](#hashing-and-frequency-maps)
- [Two pointers](#two-pointers)
- [Sliding window](#sliding-window)
- [Prefix sums](#prefix-sums)
- [Binary search](#binary-search)
- [Binary search on the answer](#binary-search-on-the-answer)
- [Linked lists](#linked-lists)
- [Recursion and backtracking](#recursion-and-backtracking)
- [Stacks and queues](#stacks-and-queues)
- [Monotonic stack](#monotonic-stack)
- [Heaps and priority queues](#heaps-and-priority-queues)
- [Greedy algorithms](#greedy-algorithms)
- [Interval problems](#interval-problems)
- [Bit manipulation](#bit-manipulation)
- [Binary trees](#binary-trees)
- [Binary search trees](#binary-search-trees)
- [BFS and graph basics](#bfs-and-graph-basics)
- [DFS, components and cycles](#dfs-components-and-cycles)
- [Dijkstra and shortest paths](#dijkstra-and-shortest-paths)
- [Topological sort](#topological-sort)
- [Disjoint set union (Union-Find)](#disjoint-set-union-union-find)
- [Dynamic programming](#dynamic-programming)
- [Knapsack and subset DP](#knapsack-and-subset-dp)
- [String DP: LCS and edit distance](#string-dp-lcs-and-edit-distance)
- [Bitmask DP](#bitmask-dp)
- [DP on trees](#dp-on-trees)
- [Tries](#tries)
- [Segment trees and Fenwick trees](#segment-trees-and-fenwick-trees)
- [String algorithms: KMP, Z, hashing](#string-algorithms-kmp-z-hashing)
- [Competitive programming and contests](#competitive-programming-and-contests)

## Time and space complexity

*Level 0: Foundation*

Every interview answer ends with 'what's the complexity?'. It is also how you pick an approach before writing code: the input limit tells you which complexities will pass.

**Key idea**

Big-O describes how running time or memory grows as the input size n grows, ignoring constants. A judge runs roughly 10⁸ simple operations per second, so you can estimate before coding.

Read n from the constraints and work backwards: n ≤ 10 allows O(n!), n ≤ 20 allows O(2ⁿ), n ≤ 500 allows O(n³), n ≤ 5000 allows O(n²), n ≤ 10⁶ needs O(n log n) or O(n), and n ≥ 10⁹ needs O(log n) or O(1) maths.

Space counts extra memory you allocate, including the recursion stack. A recursive DFS on a path of 10⁵ nodes uses 10⁵ stack frames, which can overflow.


**Points**

- Nested loops over the same array → O(n²); halving each step → O(log n)
- Sorting is O(n log n); a hash map lookup is O(1) average, O(n) worst
- Amortised O(1): vector push\_back doubles capacity occasionally
- Recursion: work per call × number of calls (draw the tree)
- Two pointers moving one way each → O(n) total, not O(n²)

**Traps**

- Forgetting the cost of string concatenation inside a loop
- Calling .size() or erase on the front of a vector inside a loop (erase is O(n))
- Saying O(1) for unordered\_map without mentioning worst case when asked

**Interviewers ask**

- What is the complexity of your solution, time and space?
- Can you do better than O(n²)?
- Why is building a heap O(n) and not O(n log n)?

**Practise**

- [Two Sum](https://leetcode.com/problems/two-sum/)
- [Contains Duplicate](https://leetcode.com/problems/contains-duplicate/)

**Learn more**

- [Big-O cheat sheet](https://www.bigocheatsheet.com)
- [Striver A2Z sheet](https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/)

**Related:** [C++ and the STL](#c-and-the-stl) · [Binary search](#binary-search)

[Back to the topic list](#topics)

## C++ and the STL

*Level 0: Foundation*

You chose C++ for DSA. In interviews and OAs, fluent STL saves 5–10 minutes per problem, and HFT firms test C++ more deeply than anyone.

**Key idea**

Containers: vector (dynamic array), deque, list, set/map (red-black tree, ordered, O(log n)), unordered\_set/unordered\_map (hash table, O(1) average), priority\_queue (binary heap, max by default), stack, queue.

Algorithms: sort, stable\_sort, lower\_bound/upper\_bound (on sorted ranges), binary\_search, reverse, accumulate, max\_element, next\_permutation, unique (with erase).

Idioms: auto and range-for, structured bindings (auto \[a, b\] = p), lambdas as comparators, emplace\_back, fast I/O with ios::sync\_with\_stdio(false); cin.tie(nullptr).


**Points**

- priority\_queue\<int, vector\<int\>, greater\<int\>\> is a min-heap
- map\[key\] inserts a default if missing; use find or count to check
- lower\_bound → first ≥ x; upper\_bound → first \> x
- Use long long when sums can pass 2·10⁹
- Pass big containers by reference (const vector\<int\>&)

```cpp
vector<int> a = {5, 1, 4};
sort(a.begin(), a.end(), [](int x, int y) { return x > y; });
unordered_map<int,int> freq; for (int x : a) freq[x]++;
priority_queue<int, vector<int>, greater<int>> minh(a.begin(), a.end());
auto it = lower_bound(a.rbegin(), a.rend(), 4); // works on reversed order
```

**Traps**

- Iterator invalidation after erase/push\_back
- Comparator must be a strict weak ordering (use \<, never \<=)
- Copying a vector into a function by value inside recursion

**Interviewers ask**

- Difference between map and unordered\_map?
- How does vector grow?
- What is RAII?
- Why is unordered\_map worst case O(n)?

**Practise**

- [Top K Frequent Elements](https://leetcode.com/problems/top-k-frequent-elements/)
- [Group Anagrams](https://leetcode.com/problems/group-anagrams/)

**Learn more**

- [takeuforward STL](https://takeuforward.org/c/c-stl-tutorial-most-asked-stl-functions-in-c/)
- [learncpp.com](https://www.learncpp.com)
- [cppreference](https://en.cppreference.com)

**Related:** [Time and space complexity](#time-and-space-complexity) · [OOP: the four pillars](core-cs.md#oop-the-four-pillars)

[Back to the topic list](#topics)

## Hashing and frequency maps

*Level 1: Core*

Turns many O(n²) 'have I seen this?' searches into O(n). It is the first optimisation interviewers expect.

**Key idea**

A hash table stores keys in buckets chosen by a hash function. Average lookup, insert and delete are O(1); collisions make the worst case O(n).

Patterns: count frequencies, remember the index where a value was first seen, check complements (target − x), group by a canonical key (sorted string for anagrams).


**Points**

- Two Sum: store value → index, check target − x before inserting x
- Anagram key: sorted string or 26-count array
- Use an array of 26/128 instead of a map when the alphabet is small

**Traps**

- Inserting before checking (pairs an element with itself)
- Using unordered\_map with pair keys (needs a custom hash)

**Interviewers ask**

- How does a hash map handle collisions?
- Why not always use a hash map?

**Practise**

- [Two Sum](https://leetcode.com/problems/two-sum/)
- [Group Anagrams](https://leetcode.com/problems/group-anagrams/)
- [Longest Consecutive Sequence](https://leetcode.com/problems/longest-consecutive-sequence/)

**Learn more**

- [Striver A2Z sheet](https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/)

**Related:** [Prefix sums](#prefix-sums) · [Sliding window](#sliding-window)

[Back to the topic list](#topics)

## Two pointers

*Level 1: Core*

One of the five most frequent interview patterns. Turns pair searches in sorted data from O(n²) into O(n).

**Key idea**

Keep two indices and move them based on a comparison. On a sorted array, if a\[i\] + a\[j\] is too small move i right; if too large move j left. Each pointer moves at most n times, so the total is O(n).

Variants: opposite ends (pair sum, container with most water), same direction fast/slow (remove duplicates, linked-list cycle), and fixing one element then running two pointers on the rest (3Sum, O(n²)).


**Points**

- Needs sorted input or a monotone condition
- 3Sum: sort, fix i, two pointers on i+1..n−1, skip duplicates
- Partitioning (Dutch national flag) is three pointers

```cpp
sort(a.begin(), a.end());
int i = 0, j = n - 1;
while (i < j) {
    int s = a[i] + a[j];
    if (s == target) return {i, j};
    if (s < target) i++; else j--;
}
```

**Traps**

- Not skipping duplicates in 3Sum
- Using it on unsorted data without sorting

**Interviewers ask**

- Why does moving the smaller side work in Container With Most Water?
- Prove two pointers doesn't miss a pair.

**Practise**

- [3Sum](https://leetcode.com/problems/3sum/)
- [Container With Most Water](https://leetcode.com/problems/container-with-most-water/)
- [Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/)

**Learn more**

- [Striver A2Z sheet](https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/)
- [NeetCode practice](https://neetcode.io/practice)

**Related:** [Sliding window](#sliding-window) · [Binary search](#binary-search)

[Back to the topic list](#topics)

## Sliding window

*Level 1: Core*

Covers most 'longest/shortest substring or subarray such that…' questions, which appear in nearly every company's list.

**Key idea**

Maintain a window \[l, r\]. Expand r each step; while the window breaks the rule, shrink l. Every index enters and leaves once, so it's O(n).

Fixed-size windows slide by adding a\[r\] and removing a\[r−k\]. Variable windows need the condition to be monotone: if a window is invalid, every bigger window containing it is invalid too.

'Exactly k' problems are often solved as atMost(k) − atMost(k−1).


**Points**

- Track counts in a map or array for character windows
- Answer is updated after the shrink loop (longest) or inside it (shortest)
- Negative numbers break the monotone condition → use prefix sums instead

```cpp
int best = 0;
for (int l = 0, r = 0; r < n; r++) {
    add(a[r]);
    while (!valid()) remove(a[l++]);
    best = max(best, r - l + 1);
}
```

**Traps**

- Using it on sums with negative numbers
- Forgetting to remove a\[l\] before l++

**Interviewers ask**

- Why is it O(n) when there's a nested while loop?
- How do you handle 'exactly k distinct'?

**Practise**

- [Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/)
- [Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/)
- [Longest Repeating Character Replacement](https://leetcode.com/problems/longest-repeating-character-replacement/)

**Learn more**

- [Striver A2Z sheet](https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/)

**Related:** [Two pointers](#two-pointers) · [Prefix sums](#prefix-sums) · [Hashing and frequency maps](#hashing-and-frequency-maps)

[Back to the topic list](#topics)

## Prefix sums

*Level 1: Core*

Range sums in O(1) and 'count subarrays with sum k' in O(n). Works with negative numbers where sliding window fails.

**Key idea**

pre\[i\] = a\[0\] + … + a\[i−1\]. The sum of a\[l..r\] is pre\[r+1\] − pre\[l\].

To count subarrays summing to k: walk once, keep a map of how many times each prefix value has appeared; at each step add seen\[pre − k\]. Start with seen\[0\] = 1.

2D prefix sums give rectangle sums in O(1); difference arrays apply range updates in O(1) then rebuild.


**Points**

- seen\[0\] = 1 handles subarrays starting at index 0
- Use long long for prefix arrays
- XOR prefix works the same way for XOR queries

```cpp
unordered_map<long long,int> seen{{0, 1}};
long long s = 0; int ways = 0;
for (int x : a) { s += x; ways += seen[s - k]; seen[s]++; }
```

**Traps**

- Off-by-one between pre\[r+1\] and pre\[r\]
- Forgetting the initial seen\[0\] = 1

**Interviewers ask**

- Why doesn't a sliding window work for Subarray Sum Equals K?

**Practise**

- [Subarray Sum Equals K](https://leetcode.com/problems/subarray-sum-equals-k/)
- [Range Sum Query 2D Immutable](https://leetcode.com/problems/range-sum-query-2d-immutable/)
- [Continuous Subarray Sum](https://leetcode.com/problems/continuous-subarray-sum/)

**Learn more**

- [Striver A2Z sheet](https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/)

**Related:** [Hashing and frequency maps](#hashing-and-frequency-maps) · [Sliding window](#sliding-window) · [Segment trees and Fenwick trees](#segment-trees-and-fenwick-trees)

[Back to the topic list](#topics)

## Binary search

*Level 1: Core*

Asked at every level, and the bug-prone template interviewers watch closely. Step 4 of Striver's sheet.

**Key idea**

On a sorted range, compare with the middle and discard half. O(log n).

Think of it as finding the boundary of a predicate that is false…false then true…true. Search for the first true. This one template covers lower\_bound, first/last occurrence, rotated arrays and peaks.

Use mid = lo + (hi − lo) / 2 to avoid overflow.


**Points**

- Rotated sorted array: one half is always sorted; check which
- Peak element: compare a\[mid\] with a\[mid+1\]
- Search a 2D sorted matrix as a flattened 1D array

```cpp
int lo = 0, hi = n - 1, ans = n;
while (lo <= hi) {
    int mid = lo + (hi - lo) / 2;
    if (a[mid] >= x) { ans = mid; hi = mid - 1; }
    else lo = mid + 1;
}
```

**Traps**

- Infinite loop from lo = mid with lo \< hi
- Wrong boundary returned (first vs last)

**Interviewers ask**

- Find the first and last position of an element.
- Search in a rotated sorted array with duplicates.

**Practise**

- [Search In Rotated Sorted Array](https://leetcode.com/problems/search-in-rotated-sorted-array/)
- [Find First And Last Position Of Element In Sorted Array](https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/)
- [Find Peak Element](https://leetcode.com/problems/find-peak-element/)

**Learn more**

- [Striver A2Z sheet](https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/)

**Related:** [Binary search on the answer](#binary-search-on-the-answer) · [Two pointers](#two-pointers)

[Back to the topic list](#topics)

## Binary search on the answer

*Level 2: Interview-ready*

A favourite Medium/Hard twist at Amazon, Google and in OAs. Recognising it is most of the work.

**Key idea**

When the question asks for the minimum (or maximum) value X such that something is feasible, and feasibility is monotone in X, binary search over X and write an O(n) check(X).

Classic shapes: 'minimise the largest sum when splitting into k parts', 'minimum speed/capacity to finish in D days', 'maximise the minimum distance between cows'.


**Points**

- Range of X: from the smallest possible answer to the largest
- check(X) is usually greedy
- Total O(n log range)

```text
long long lo = MIN_ANS, hi = MAX_ANS, ans = hi;
while (lo <= hi) {
    long long mid = lo + (hi - lo) / 2;
    if (ok(mid)) { ans = mid; hi = mid - 1; } else lo = mid + 1;
}
```

**Traps**

- Wrong bounds (lo too high excludes the answer)
- Non-monotone check

**Interviewers ask**

- How do you know the answer space is monotone?

**Practise**

- [Koko Eating Bananas](https://leetcode.com/problems/koko-eating-bananas/)
- [Split Array Largest Sum](https://leetcode.com/problems/split-array-largest-sum/)
- [Capacity To Ship Packages Within D Days](https://leetcode.com/problems/capacity-to-ship-packages-within-d-days/)

**Learn more**

- [Striver A2Z sheet](https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/)

**Related:** [Binary search](#binary-search) · [Greedy algorithms](#greedy-algorithms)

[Back to the topic list](#topics)

## Linked lists

*Level 1: Core*

Pointer manipulation questions are common in first rounds and test careful coding. Step 6 of the sheet.

**Key idea**

Each node holds a value and a pointer to the next. Insertion/deletion at a known node is O(1); access by index is O(n).

Core techniques: a dummy head node to avoid edge cases, fast/slow pointers (middle, cycle detection by Floyd's algorithm, cycle start), and iterative reversal with prev/curr/next.


**Points**

- Reverse: three pointers, return prev
- Cycle start: after meeting, move one pointer to head, step both by 1
- Merge two sorted lists with a dummy node
- LRU cache = hash map + doubly linked list

```text
ListNode* prev = nullptr; ListNode* cur = head;
while (cur) { ListNode* nx = cur->next; cur->next = prev; prev = cur; cur = nx; }
return prev;
```

**Traps**

- Dereferencing null on fast-\>next-\>next
- Losing the rest of the list before re-linking

**Interviewers ask**

- Detect and remove a cycle.
- Reverse nodes in k-groups.
- Design an LRU cache.

**Practise**

- [Reverse Linked List](https://leetcode.com/problems/reverse-linked-list/)
- [Linked List Cycle Ii](https://leetcode.com/problems/linked-list-cycle-ii/)
- [Lru Cache](https://leetcode.com/problems/lru-cache/)
- [Reverse Nodes In K Group](https://leetcode.com/problems/reverse-nodes-in-k-group/)

**Learn more**

- [Striver A2Z sheet](https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/)

**Related:** [Two pointers](#two-pointers)

[Back to the topic list](#topics)

## Recursion and backtracking

*Level 1: Core*

The base for trees, graphs and DP. Subsets, permutations and N-Queens are standard interview questions.

**Key idea**

Recursion: solve a problem using smaller copies of itself; define the base case first, then trust the call.

Backtracking explores a decision tree: choose, recurse, un-choose. It's exhaustive, so complexity is the size of the tree (2ⁿ for subsets, n! for permutations).

Prune early: stop a branch as soon as it cannot lead to a valid answer.


**Points**

- Pick / not-pick for subsets
- Swap-based or used\[\] array for permutations
- Skip duplicates by sorting and checking i \> start && a\[i\] == a\[i−1\]

```cpp
void go(int i, vector<int>& cur) {
    if (i == n) { res.push_back(cur); return; }
    cur.push_back(a[i]); go(i + 1, cur); cur.pop_back(); // pick
    go(i + 1, cur);                                    // skip
}
```

**Traps**

- Forgetting to un-choose
- Copying vectors in every call

**Interviewers ask**

- Generate all valid parentheses.
- Solve N-Queens.
- What's the complexity of your backtracking?

**Practise**

- [Subsets Ii](https://leetcode.com/problems/subsets-ii/)
- [Permutations](https://leetcode.com/problems/permutations/)
- [Combination Sum](https://leetcode.com/problems/combination-sum/)
- [N Queens](https://leetcode.com/problems/n-queens/)

**Learn more**

- [Striver A2Z sheet](https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/)

**Related:** [Dynamic programming](#dynamic-programming) · [Bitmask DP](#bitmask-dp)

[Back to the topic list](#topics)

## Stacks and queues

*Level 1: Core*

Expression parsing, bracket matching and undo-style problems. Step 9 of the sheet, and the base for monotonic stacks.

**Key idea**

A stack is last-in-first-out; a queue is first-in-first-out. Both give O(1) push and pop.

Use a stack when the most recent unfinished item matters (brackets, function calls, undo). Use a queue for processing in arrival order (BFS, scheduling).


**Points**

- Valid parentheses with a stack of opening brackets
- Min-stack keeps a second stack of current minimums
- Queue using two stacks: amortised O(1)

**Traps**

- Popping an empty stack
- Using std::stack when you need to iterate (use vector)

**Interviewers ask**

- Implement a queue with stacks.
- Design a min-stack.

**Practise**

- [Valid Parentheses](https://leetcode.com/problems/valid-parentheses/)
- [Min Stack](https://leetcode.com/problems/min-stack/)
- [Evaluate Reverse Polish Notation](https://leetcode.com/problems/evaluate-reverse-polish-notation/)

**Learn more**

- [Striver A2Z sheet](https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/)

**Related:** [Monotonic stack](#monotonic-stack) · [BFS and graph basics](#bfs-and-graph-basics)

[Back to the topic list](#topics)

## Monotonic stack

*Level 2: Interview-ready*

Solves next-greater, stock span and largest-rectangle problems in O(n). A common Medium/Hard step-up.

**Key idea**

Keep a stack whose values are always increasing (or decreasing). When a new element breaks the order, pop: each popped element has just found its next greater (or smaller) element.

Every element is pushed and popped once, so the total is O(n). Store indices, not values, so you can compute distances and widths.


**Points**

- Largest rectangle in histogram: previous and next smaller
- Daily temperatures: next greater, answer = index distance
- Sum of subarray minimums: count contributions with previous/next smaller

```cpp
vector<int> nge(n, -1); stack<int> st;
for (int i = 0; i < n; i++) {
    while (!st.empty() && a[st.top()] < a[i]) { nge[st.top()] = a[i]; st.pop(); }
    st.push(i);
}
```

**Traps**

- Strict vs non-strict comparison with duplicates (double counting)

**Interviewers ask**

- Largest rectangle in a histogram.
- Trapping rain water with a stack.

**Practise**

- [Daily Temperatures](https://leetcode.com/problems/daily-temperatures/)
- [Largest Rectangle In Histogram](https://leetcode.com/problems/largest-rectangle-in-histogram/)
- [Sum Of Subarray Minimums](https://leetcode.com/problems/sum-of-subarray-minimums/)

**Learn more**

- [Striver A2Z sheet](https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/)

**Related:** [Stacks and queues](#stacks-and-queues)

[Back to the topic list](#topics)

## Heaps and priority queues

*Level 2: Interview-ready*

Top-K, merging sorted lists, scheduling and Dijkstra all use a heap. Very common at Amazon.

**Key idea**

A binary heap keeps the smallest (or largest) element on top. Push and pop are O(log n); peek is O(1); building from n items is O(n).

Top K largest: keep a min-heap of size k; pop when it grows past k. Streaming median: a max-heap for the lower half and a min-heap for the upper half, kept balanced.


**Points**

- K-way merge: push the head of each list
- Use pair\<int,int\> to sort by priority then id
- Lazy deletion: skip stale entries when popped

**Traps**

- Default priority\_queue is a max-heap
- Sorting everything when you only need top k

**Interviewers ask**

- Find the median of a data stream.
- Why is heapify O(n)?

**Practise**

- [Kth Largest Element In An Array](https://leetcode.com/problems/kth-largest-element-in-an-array/)
- [Merge K Sorted Lists](https://leetcode.com/problems/merge-k-sorted-lists/)
- [Find Median From Data Stream](https://leetcode.com/problems/find-median-from-data-stream/)
- [Task Scheduler](https://leetcode.com/problems/task-scheduler/)

**Learn more**

- [Striver A2Z sheet](https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/)

**Related:** [Dijkstra and shortest paths](#dijkstra-and-shortest-paths) · [Greedy algorithms](#greedy-algorithms)

[Back to the topic list](#topics)

## Greedy algorithms

*Level 2: Interview-ready*

Short code, but you must justify it. Interviewers ask 'why does greedy work here?'.

**Key idea**

Make the locally best choice at each step and never revisit it. It works only when an exchange argument holds: any optimal solution can be changed step by step into the greedy one without getting worse.

Most greedy solutions start by sorting: by end time (activity selection), by ratio (fractional knapsack), by deadline (job sequencing).


**Points**

- Interval scheduling: sort by end, take if start ≥ last end
- Jump game: track the furthest reachable index
- If greedy fails on a small counterexample → it's DP

**Traps**

- Assuming greedy works without testing a counterexample (0/1 knapsack)

**Interviewers ask**

- Prove your greedy choice is safe.
- When would greedy fail here?

**Practise**

- [Jump Game Ii](https://leetcode.com/problems/jump-game-ii/)
- [Non Overlapping Intervals](https://leetcode.com/problems/non-overlapping-intervals/)
- [Gas Station](https://leetcode.com/problems/gas-station/)

**Learn more**

- [Striver A2Z sheet](https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/)

**Related:** [Interval problems](#interval-problems) · [Dynamic programming](#dynamic-programming)

[Back to the topic list](#topics)

## Interval problems

*Level 2: Interview-ready*

Merge intervals and meeting rooms are top-asked at Google, Microsoft and Amazon.

**Key idea**

Sort by start (to merge) or by end (to choose the most non-overlapping). Then sweep once.

For 'how many overlap at once' (meeting rooms), sweep over events: +1 at start, −1 at end, and track the maximum; or use a min-heap of end times.


**Points**

- Merge: if start ≤ last end, extend; else push new
- Insert interval: three phases (before, overlapping, after)

**Traps**

- Touching intervals: decide whether \[1,2\] and \[2,3\] overlap

**Interviewers ask**

- Minimum meeting rooms needed.
- Merge overlapping intervals.

**Practise**

- [Merge Intervals](https://leetcode.com/problems/merge-intervals/)
- [Insert Interval](https://leetcode.com/problems/insert-interval/)
- [Non Overlapping Intervals](https://leetcode.com/problems/non-overlapping-intervals/)

**Learn more**

- [Striver A2Z sheet](https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/)

**Related:** [Greedy algorithms](#greedy-algorithms) · [Heaps and priority queues](#heaps-and-priority-queues)

[Back to the topic list](#topics)

## Bit manipulation

*Level 1: Core*

Quick wins in OAs (single number, power of two), and the base for bitmask DP.

**Key idea**

x & 1 tests odd; x & (x−1) clears the lowest set bit; x & −x isolates it; a ^ a = 0, so XOR of all elements leaves the one that appears once.

A mask of n bits represents a subset of n items: loop mask from 0 to 2ⁿ − 1 to enumerate all subsets.


**Points**

- \_\_builtin\_popcount(x) counts set bits
- Check bit i: (x \>\> i) & 1; set: x \| (1 \<\< i)
- Use 1LL \<\< i for i ≥ 31

**Traps**

- Operator precedence: write (x & 1) == 0 with brackets

**Interviewers ask**

- Find the two numbers that appear once.
- Count bits from 0 to n.

**Practise**

- [Single Number](https://leetcode.com/problems/single-number/)
- [Counting Bits](https://leetcode.com/problems/counting-bits/)
- [Subsets](https://leetcode.com/problems/subsets/)

**Learn more**

- [Striver A2Z sheet](https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/)
- [cp-algorithms: bit manipulation](https://cp-algorithms.com/algebra/bit-manipulation.html)

**Related:** [Bitmask DP](#bitmask-dp) · [Tries](#tries)

[Back to the topic list](#topics)

## Binary trees

*Level 2: Interview-ready*

The largest single topic in interviews. Step 13–14 of the sheet.

**Key idea**

Traversals: preorder, inorder, postorder (DFS) and level order (BFS with a queue). Know both recursive and iterative versions.

Most tree problems are 'return something from each subtree and combine': height, diameter, balanced check, max path sum. Write a function that returns the subtree answer and updates a global best.

Lowest common ancestor: if both sides return non-null, the current node is the LCA.


**Points**

- Diameter = max over nodes of leftHeight + rightHeight
- Serialize with preorder + null markers
- Views (left/right/top/bottom) use BFS with column index

```cpp
int best = INT_MIN;
int gain(TreeNode* r) {
    if (!r) return 0;
    int L = max(0, gain(r->left)), R = max(0, gain(r->right));
    best = max(best, r->val + L + R);
    return r->val + max(L, R);
}
```

**Traps**

- Confusing 'path through node' with 'path returned to parent'
- Recursion depth on skewed trees

**Interviewers ask**

- Maximum path sum.
- Serialize and deserialize a tree.
- Lowest common ancestor.

**Practise**

- [Binary Tree Maximum Path Sum](https://leetcode.com/problems/binary-tree-maximum-path-sum/)
- [Lowest Common Ancestor Of A Binary Tree](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/)
- [Serialize And Deserialize Binary Tree](https://leetcode.com/problems/serialize-and-deserialize-binary-tree/)
- [Diameter Of Binary Tree](https://leetcode.com/problems/diameter-of-binary-tree/)

**Learn more**

- [Striver A2Z sheet](https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/)

**Related:** [Binary search trees](#binary-search-trees) · [DP on trees](#dp-on-trees) · [BFS and graph basics](#bfs-and-graph-basics)

[Back to the topic list](#topics)

## Binary search trees

*Level 2: Interview-ready*

Common follow-up to tree questions; inorder-sorted property shows up everywhere.

**Key idea**

Left subtree \< node \< right subtree. Inorder traversal gives sorted order. Search, insert and delete are O(h): O(log n) if balanced, O(n) if skewed.

Validate with a (low, high) range passed down, not just comparing with children.


**Points**

- Kth smallest = kth node in inorder
- LCA in BST: walk down using values
- std::set/map are balanced BSTs (red-black)

**Traps**

- Validating only parent-child pairs

**Interviewers ask**

- Validate a BST.
- Delete a node from a BST.

**Practise**

- [Validate Binary Search Tree](https://leetcode.com/problems/validate-binary-search-tree/)
- [Kth Smallest Element In A Bst](https://leetcode.com/problems/kth-smallest-element-in-a-bst/)
- [Delete Node In A Bst](https://leetcode.com/problems/delete-node-in-a-bst/)

**Learn more**

- [Striver A2Z sheet](https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/)

**Related:** [Binary trees](#binary-trees) · [Binary search](#binary-search)

[Back to the topic list](#topics)

## BFS and graph basics

*Level 1: Core*

Graphs are in almost every product-company loop. BFS gives shortest paths when every edge costs the same.

**Key idea**

Store a graph as an adjacency list: vector\<vector\<int\>\> adj(n). Grids are implicit graphs with 4 neighbours.

BFS uses a queue and visits nodes in order of distance from the source, so the first time you reach a node is its shortest path. O(V + E).

Multi-source BFS starts with all sources in the queue (rotting oranges, nearest 0). 0-1 BFS uses a deque for edges of weight 0 or 1.


**Points**

- Mark visited when pushing, not when popping
- Grid: dr/dc arrays for directions
- Bipartite check = BFS 2-colouring

```cpp
vector<int> dist(n, -1); queue<int> q; dist[s] = 0; q.push(s);
while (!q.empty()) {
    int u = q.front(); q.pop();
    for (int v : adj[u]) if (dist[v] == -1) { dist[v] = dist[u] + 1; q.push(v); }
}
```

**Traps**

- Marking visited on pop → duplicates in queue

**Interviewers ask**

- Rotting oranges.
- Word ladder.
- Is the graph bipartite?

**Practise**

- [Rotting Oranges](https://leetcode.com/problems/rotting-oranges/)
- [Word Ladder](https://leetcode.com/problems/word-ladder/)
- [Is Graph Bipartite](https://leetcode.com/problems/is-graph-bipartite/)
- [Number Of Islands](https://leetcode.com/problems/number-of-islands/)

**Learn more**

- [Striver A2Z sheet](https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/)
- [CSES problem set](https://cses.fi/problemset/)

**Related:** [DFS, components and cycles](#dfs-components-and-cycles) · [Dijkstra and shortest paths](#dijkstra-and-shortest-paths) · [Topological sort](#topological-sort)

[Back to the topic list](#topics)

## DFS, components and cycles

*Level 1: Core*

Connected components, cycle detection and flood fill are standard graph questions.

**Key idea**

DFS goes deep along one path before backtracking. Recursive or with an explicit stack. O(V + E).

Undirected cycle: you reach a visited node that isn't your parent. Directed cycle: you reach a node still on the current recursion path (keep an inStack array or 3 colours).

Count components by starting a DFS from every unvisited node.


**Points**

- Flood fill on grids is DFS
- Directed cycle check = topo sort fails
- Bridges/articulation points use discovery and low times (L3)

**Traps**

- Stack overflow on 10⁶-node grids: use iterative DFS or BFS

**Interviewers ask**

- Detect a cycle in a directed graph.
- Number of islands.
- Clone a graph.

**Practise**

- [Number Of Islands](https://leetcode.com/problems/number-of-islands/)
- [Clone Graph](https://leetcode.com/problems/clone-graph/)
- [Course Schedule](https://leetcode.com/problems/course-schedule/)

**Learn more**

- [Striver A2Z sheet](https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/)
- [CSES problem set](https://cses.fi/problemset/)

**Related:** [BFS and graph basics](#bfs-and-graph-basics) · [Topological sort](#topological-sort) · [Disjoint set union (Union-Find)](#disjoint-set-union-union-find)

[Back to the topic list](#topics)

## Dijkstra and shortest paths

*Level 2: Interview-ready*

The standard weighted shortest path. Asked at Google, Uber, Flipkart.

**Key idea**

Dijkstra: a min-heap of (distance, node). Pop the closest, relax its edges. Works only with non-negative weights. O((V + E) log V).

Bellman-Ford relaxes all edges V−1 times, handles negative edges and detects negative cycles, O(VE). Floyd-Warshall gives all pairs in O(V³) for small V.


**Points**

- Skip stale heap entries: if (d \> dist\[u\]) continue
- Cheapest flights within K stops: BFS by level or Bellman-Ford with K rounds
- Path reconstruction with a parent array

```cpp
vector<long long> d(n, INF); d[s] = 0;
priority_queue<pair<long long,int>, vector<pair<long long,int>>, greater<>> pq; pq.push({0, s});
while (!pq.empty()) {
    auto [du, u] = pq.top(); pq.pop();
    if (du > d[u]) continue;
    for (auto [v, w] : adj[u]) if (d[u] + w < d[v]) { d[v] = d[u] + w; pq.push({d[v], v}); }
}
```

**Traps**

- Using Dijkstra with negative edges
- int overflow on distances

**Interviewers ask**

- Why does Dijkstra fail with negative weights?
- Network delay time.

**Practise**

- [Network Delay Time](https://leetcode.com/problems/network-delay-time/)
- [Path With Minimum Effort](https://leetcode.com/problems/path-with-minimum-effort/)
- [Cheapest Flights Within K Stops](https://leetcode.com/problems/cheapest-flights-within-k-stops/)

**Learn more**

- [Striver A2Z sheet](https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/)
- [cp-algorithms: Dijkstra](https://cp-algorithms.com/graph/dijkstra.html)

**Related:** [BFS and graph basics](#bfs-and-graph-basics) · [Heaps and priority queues](#heaps-and-priority-queues)

[Back to the topic list](#topics)

## Topological sort

*Level 2: Interview-ready*

Course schedule and build-order questions; also how you detect cycles in directed graphs.

**Key idea**

An order of a DAG's nodes where every edge goes forward. Kahn's algorithm: push all nodes with in-degree 0, pop, decrement neighbours, push any that reach 0. If you output fewer than V nodes, there's a cycle.

DFS version: add a node to the list after visiting all its children, then reverse.


**Points**

- Alien dictionary: build edges from adjacent words
- Longest path in a DAG = DP in topo order

**Traps**

- Not handling disconnected nodes

**Interviewers ask**

- Course schedule II.
- Alien dictionary.

**Practise**

- [Course Schedule Ii](https://leetcode.com/problems/course-schedule-ii/)
- [Course Schedule](https://leetcode.com/problems/course-schedule/)
- [Parallel Courses](https://leetcode.com/problems/parallel-courses/)

**Learn more**

- [Striver A2Z sheet](https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/)

**Related:** [DFS, components and cycles](#dfs-components-and-cycles) · [BFS and graph basics](#bfs-and-graph-basics)

[Back to the topic list](#topics)

## Disjoint set union (Union-Find)

*Level 2: Interview-ready*

Fast connectivity for dynamic merging, Kruskal's MST and 'accounts merge'.

**Key idea**

Each set has a root. find(x) follows parents to the root; union(a, b) links roots. With path compression and union by size, each operation is almost O(1) (inverse Ackermann).

Kruskal's minimum spanning tree: sort edges by weight, add an edge if its ends are in different sets.


**Points**

- Count components = number of successful unions subtracted from n
- Redundant connection: the edge whose ends are already joined

```cpp
vector<int> p(n), sz(n, 1); iota(p.begin(), p.end(), 0);
function<int(int)> find = [&](int x) { return p[x] == x ? x : p[x] = find(p[x]); };
auto unite = [&](int a, int b) { a = find(a); b = find(b); if (a == b) return false;
    if (sz[a] < sz[b]) swap(a, b); p[b] = a; sz[a] += sz[b]; return true; };
```

**Traps**

- Forgetting to call find before comparing

**Interviewers ask**

- Number of provinces.
- Accounts merge.
- Minimum spanning tree.

**Practise**

- [Number Of Provinces](https://leetcode.com/problems/number-of-provinces/)
- [Redundant Connection](https://leetcode.com/problems/redundant-connection/)
- [Accounts Merge](https://leetcode.com/problems/accounts-merge/)

**Learn more**

- [Striver A2Z sheet](https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/)
- [cp-algorithms: DSU](https://cp-algorithms.com/data_structures/disjoint_set_union.html)

**Related:** [DFS, components and cycles](#dfs-components-and-cycles)

[Back to the topic list](#topics)

## Dynamic programming

*Level 2: Interview-ready*

The topic that separates L2 from L3. Striver step 16 is the longest; product companies ask at least one DP.

**Key idea**

DP = recursion + remembering answers to overlapping subproblems. Recipe: (1) define the state in words, e.g. dp\[i\] = best answer for the first i items; (2) write the transition from smaller states; (3) base cases; (4) the order to fill; (5) where the answer is.

Go memoised recursion → bottom-up table → space-optimised (keep only the last row). Interviewers love seeing all three.

Families: 1D (climbing stairs, house robber), grid paths, 0/1 and unbounded knapsack, subsequences (LIS, LCS, edit distance), partitions (palindrome partitioning, matrix chain), stocks (state machine), DP on trees, bitmask DP.


**Points**

- Complexity = number of states × work per transition
- If greedy fails on a counterexample, think DP
- Print the solution by walking back through choices

```cpp
// 0/1 knapsack, space-optimised
vector<int> dp(W + 1, 0);
for (int i = 0; i < n; i++)
    for (int w = W; w >= wt[i]; w--)
        dp[w] = max(dp[w], dp[w - wt[i]] + val[i]);
```

**Traps**

- Iterating capacity upwards in 0/1 knapsack (turns it unbounded)
- Wrong base case for empty prefix

**Interviewers ask**

- Explain your state and transition.
- Can you reduce the space?
- Edit distance.
- Longest increasing subsequence in O(n log n).

**Practise**

- [House Robber](https://leetcode.com/problems/house-robber/)
- [Coin Change](https://leetcode.com/problems/coin-change/)
- [Longest Increasing Subsequence](https://leetcode.com/problems/longest-increasing-subsequence/)
- [Edit Distance](https://leetcode.com/problems/edit-distance/)
- [Partition Equal Subset Sum](https://leetcode.com/problems/partition-equal-subset-sum/)

**Learn more**

- [Striver A2Z sheet](https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/)
- [AtCoder Educational DP contest](https://atcoder.jp/contests/dp)

**Related:** [Knapsack and subset DP](#knapsack-and-subset-dp) · [String DP: LCS and edit distance](#string-dp-lcs-and-edit-distance) · [Bitmask DP](#bitmask-dp) · [DP on trees](#dp-on-trees) · [Recursion and backtracking](#recursion-and-backtracking)

[Back to the topic list](#topics)

## Knapsack and subset DP

*Level 2: Interview-ready*

Subset-sum, partition and coin-change are all knapsack in disguise.

**Key idea**

0/1 knapsack: each item once; loop capacity downwards. Unbounded (coin change): items reusable; loop capacity upwards.

Subset sum to target T: boolean dp\[t\]. Partition equal subset: subset sum to total/2. Count of subsets with difference d: subset sum to (total + d)/2.


**Points**

- Coin change (min coins): dp\[x\] = min(dp\[x − c\] + 1)
- Coin change II (count ways): loop coins outside, amounts inside

**Traps**

- Order of loops changes combinations vs permutations

**Interviewers ask**

- Target sum.
- Partition equal subset sum.

**Practise**

- [Coin Change Ii](https://leetcode.com/problems/coin-change-ii/)
- [Target Sum](https://leetcode.com/problems/target-sum/)
- [Partition Equal Subset Sum](https://leetcode.com/problems/partition-equal-subset-sum/)

**Learn more**

- [Striver A2Z sheet](https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/)

**Related:** [Dynamic programming](#dynamic-programming)

[Back to the topic list](#topics)

## String DP: LCS and edit distance

*Level 2: Interview-ready*

Two-string comparison problems are a fixed pattern; once learned, a whole family falls.

**Key idea**

dp\[i\]\[j\] = answer for prefixes a\[0..i) and b\[0..j). If a\[i−1\] == b\[j−1\], extend the diagonal; otherwise take the best of dropping one character.

Edit distance: min of insert dp\[i\]\[j−1\], delete dp\[i−1\]\[j\], replace dp\[i−1\]\[j−1\], each +1. Shortest common supersequence and longest palindromic subsequence (LCS of s and reverse(s)) follow.


**Points**

- Space-optimise to two rows
- Distinct subsequences counts ways

**Traps**

- Off-by-one between string index and dp index

**Interviewers ask**

- Edit distance.
- Longest common subsequence and print it.

**Practise**

- [Longest Common Subsequence](https://leetcode.com/problems/longest-common-subsequence/)
- [Edit Distance](https://leetcode.com/problems/edit-distance/)
- [Distinct Subsequences](https://leetcode.com/problems/distinct-subsequences/)

**Learn more**

- [Striver A2Z sheet](https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/)

**Related:** [Dynamic programming](#dynamic-programming) · [String algorithms: KMP, Z, hashing](#string-algorithms-kmp-z-hashing)

[Back to the topic list](#topics)

## Bitmask DP

*Level 3: Advanced*

L3/L4 topic for hard rounds, OAs at top firms and HFT. Shows up when n ≤ 20.

**Key idea**

The state includes a mask of which items are used: dp\[mask\] or dp\[mask\]\[last\]. 2ⁿ masks × n transitions → O(2ⁿ·n) or O(2ⁿ·n²).

Travelling salesman: dp\[mask\]\[i\] = shortest path visiting mask and ending at i.


**Points**

- Iterate submasks: for (s = m; s; s = (s − 1) & m)
- Memory: 2²⁰ × 20 ints ≈ 80 MB, watch limits

**Traps**

- Using it when n is 40 (meet-in-the-middle instead)

**Interviewers ask**

- Shortest path visiting all nodes.

**Practise**

- [Shortest Path Visiting All Nodes](https://leetcode.com/problems/shortest-path-visiting-all-nodes/)
- [Partition To K Equal Sum Subsets](https://leetcode.com/problems/partition-to-k-equal-sum-subsets/)
- [CSES: Elevator Rides](https://cses.fi/problemset/task/1653)

**Learn more**

- [cp-algorithms: submask enumeration](https://cp-algorithms.com/algebra/all-submasks.html)
- [CSES problem set](https://cses.fi/problemset/)

**Related:** [Dynamic programming](#dynamic-programming) · [Bit manipulation](#bit-manipulation)

[Back to the topic list](#topics)

## DP on trees

*Level 3: Advanced*

Hard-round favourite: house robber III, max path sum, rerooting.

**Key idea**

Compute dp for each node from its children in a post-order DFS. Often each node returns a small tuple (take, skip).

Rerooting: compute answers for one root, then move the root to each child in O(1) to get answers for all roots in O(n).


**Points**

- House Robber III returns {rob, notRob}
- Sum of distances in tree is the classic rerooting problem

**Traps**

- Recomputing subtrees (O(n²))

**Interviewers ask**

- House robber on a tree.

**Practise**

- [House Robber Iii](https://leetcode.com/problems/house-robber-iii/)
- [Sum Of Distances In Tree](https://leetcode.com/problems/sum-of-distances-in-tree/)
- [CSES: Tree Distances I](https://cses.fi/problemset/task/1132)

**Learn more**

- [USACO Guide: DP on trees](https://usaco.guide/gold/dp-trees)
- [CSES problem set](https://cses.fi/problemset/)

**Related:** [Binary trees](#binary-trees) · [Dynamic programming](#dynamic-programming)

[Back to the topic list](#topics)

## Tries

*Level 2: Interview-ready*

Autocomplete, word search and max-XOR problems. Last step of Striver's sheet.

**Key idea**

A tree where each edge is a character; the path from the root spells a prefix. Insert and search are O(word length).

A bit trie stores numbers bit by bit from the top; to maximise XOR with x, greedily go to the opposite bit at each level.


**Points**

- Node: array of 26 children + end flag (+ count for prefix counts)
- Word Search II: trie + DFS on the grid

```text
struct Node { Node* ch[26] = {}; bool end = false; };
void insert(Node* r, const string& w) {
    for (char c : w) { if (!r->ch[c - 'a']) r->ch[c - 'a'] = new Node(); r = r->ch[c - 'a']; }
    r->end = true;
}
```

**Traps**

- Memory: 26 pointers per node; use array pools for big inputs

**Interviewers ask**

- Implement a trie.
- Maximum XOR of two numbers.

**Practise**

- [Implement Trie Prefix Tree](https://leetcode.com/problems/implement-trie-prefix-tree/)
- [Word Search Ii](https://leetcode.com/problems/word-search-ii/)
- [Maximum Xor Of Two Numbers In An Array](https://leetcode.com/problems/maximum-xor-of-two-numbers-in-an-array/)

**Learn more**

- [Striver A2Z sheet](https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/)

**Related:** [Bit manipulation](#bit-manipulation) · [String algorithms: KMP, Z, hashing](#string-algorithms-kmp-z-hashing)

[Back to the topic list](#topics)

## Segment trees and Fenwick trees

*Level 3: Advanced*

L3: range queries with updates. Needed for CP, CSES and harder OAs (Google, D. E. Shaw).

**Key idea**

A segment tree stores an aggregate (sum, min, max) for each segment; query and point update are O(log n). With lazy propagation it supports range updates too.

A Fenwick tree (BIT) is shorter code for prefix sums with point updates, O(log n) each, using i & −i.


**Points**

- Size the segment tree array 4n
- Count inversions with a BIT over compressed values

```cpp
// Fenwick, 1-indexed
vector<long long> bit(n + 1);
void add(int i, long long v) { for (; i <= n; i += i & -i) bit[i] += v; }
long long sum(int i) { long long s = 0; for (; i > 0; i -= i & -i) s += bit[i]; return s; }
```

**Traps**

- Forgetting to push lazy values down before recursing

**Interviewers ask**

- Range sum query, mutable.
- Count of smaller numbers after self.

**Practise**

- [Range Sum Query Mutable](https://leetcode.com/problems/range-sum-query-mutable/)
- [Count Of Smaller Numbers After Self](https://leetcode.com/problems/count-of-smaller-numbers-after-self/)
- [CSES: Range Queries](https://cses.fi/problemset/)

**Learn more**

- [cp-algorithms: segment tree](https://cp-algorithms.com/data_structures/segment_tree.html)
- [cp-algorithms: Fenwick tree](https://cp-algorithms.com/data_structures/fenwick.html)

**Related:** [Prefix sums](#prefix-sums)

[Back to the topic list](#topics)

## String algorithms: KMP, Z, hashing

*Level 3: Advanced*

Pattern matching in O(n + m). Appears in hard rounds and CP.

**Key idea**

KMP builds a prefix function: pi\[i\] = length of the longest proper prefix of s\[0..i\] that is also a suffix. Matching never moves backwards in the text.

The Z-function z\[i\] = length of the longest substring starting at i that matches a prefix. Search pattern + '$' + text.

Rolling hash (Rabin-Karp) compares substrings in O(1) after O(n) preprocessing; use two moduli to reduce collisions.


**Points**

- Shortest palindrome: KMP on s + '#' + reverse(s)
- Repeated substring pattern via prefix function

**Traps**

- Single-modulus hashing can be broken by anti-hash tests

**Interviewers ask**

- Find the first occurrence of a pattern in O(n + m).

**Practise**

- [Find The Index Of The First Occurrence In A String](https://leetcode.com/problems/find-the-index-of-the-first-occurrence-in-a-string/)
- [Shortest Palindrome](https://leetcode.com/problems/shortest-palindrome/)
- [Repeated Substring Pattern](https://leetcode.com/problems/repeated-substring-pattern/)

**Learn more**

- [cp-algorithms: prefix function](https://cp-algorithms.com/string/prefix-function.html)
- [cp-algorithms: Z-function](https://cp-algorithms.com/string/z-function.html)
- [cp-algorithms: string hashing](https://cp-algorithms.com/string/string-hashing.html)

**Related:** [Tries](#tries) · [String DP: LCS and edit distance](#string-dp-lcs-and-edit-distance)

[Back to the topic list](#topics)

## Competitive programming and contests

*Level 3: Advanced*

Ratings are a filter recruiters understand, contests train speed under pressure (exactly what OAs test), and HFT firms hire heavily from strong CP profiles.

**Key idea**

Do one LeetCode weekly contest and one Codeforces Div 2/3 round a week. After each, upsolve the first problem you couldn't solve.

The CP31 sheet gives 31 problems per rating band (800 → 1900): climb in order. CSES gives 300 classic problems by topic.

Targets from your plan: LC 1800+ or CF 1400+ by mid-2027 for Big Tech; CF 1600–1900+ for HFT.


**Points**

- Read all problems first; solve in order of confidence
- Stress-test with a brute force on random inputs
- Keep a contest log: problem, idea, mistake

**Traps**

- Grinding new contests without upsolving
- Chasing rating over interview skills before L2 is done

**Interviewers ask**

- (Interviews rarely ask about CP; your rating speaks on the resume)

**Practise**

- [Codeforces](https://codeforces.com)
- [LeetCode contests](https://leetcode.com/contest/)
- [CSES problem set](https://cses.fi/problemset/)
- [AtCoder](https://atcoder.jp)

**Learn more**

- [USACO Guide](https://usaco.guide)
- [cp-algorithms](https://cp-algorithms.com)
- [clist.by contest calendar](https://clist.by)

**Related:** [Online assessments (OAs)](career.md#online-assessments-oas) · [Time and space complexity](#time-and-space-complexity)

[Back to the topic list](#topics)
