ONLINE ASSESSMENT · SIMULATION PACKS

# 8 timed OAs 3 problems · 90 minutes

Eight practice online assessments in the shape most fresher coding rounds use: three problems, one timer, no help. 24 different LeetCode problems, none repeated across sets and none from the 83 worked solutions you already have. Each set has a question page (open it when the timer starts) and a solution page (open it only after you have scored yourself).

## Index

| \#  | Set                                                                                               | Suggested date  | Mix       | Max |     |
|-----|---------------------------------------------------------------------------------------------------|-----------------|-----------|-----|-----|
| 1   | [Warm-up](#set-1-warm-up)Hashing, sliding window, stack                                                  | Sat 13 Feb 2027 | E · M · M | 500 |     |
| 2   | [Counting and graphs](#set-2-counting-and-graphs)Two pointers, greedy counting, BFS                                 | Sat 27 Feb 2027 | E · M · H | 600 |     |
| 3   | [Windows and greedy](#set-3-windows-and-greedy)Fixed and variable windows, two-pass greedy                         | Sat 13 Mar 2027 | E · M · H | 600 |     |
| 4   | [Stacks and binary search](#set-4-stacks-and-binary-search)DP warm-up, stack evaluation, partition search                | Sat 24 Apr 2027 | E · M · H | 600 |     |
| 5   | [Simulation and shortest paths](#set-5-simulation-and-shortest-paths)Cycle detection, sorting, Dijkstra on a grid             | Sat 8 May 2027  | E · M · H | 600 |     |
| 6   | [Mediums under pressure](#set-6-mediums-under-pressure)Binary search on a window, union-find, interval DP              | Sat 22 May 2027 | M · M · H | 700 |     |
| 7   | [Arrays and answer search](#set-7-arrays-and-answer-search)In-place tricks, interval greedy, binary search on the answer | Sat 12 Jun 2027 | M · M · H | 700 |     |
| 8   | [Final dress rehearsal](#set-8-final-dress-rehearsal)Counting, DP with counts, string DP                              | Sat 3 Jul 2027  | E · M · H | 600 |     |
| ·   | [How to run a set, and the scoring guide](#how-to-run-a-set)                                                |                 |           |     |     |

Dates follow the plan: sets 1–3 during the Hard pass before the exam break (22 Mar – 7 Apr), set 4 after it, 5–6 in May, 7–8 in the placement sprint. Move a date if a test or the AWS exam (week of 19 Apr) clashes. Problem statements are on LeetCode; the one-line summaries, sketches and code here are original. Every reference solution was compiled with `g++ -std=c++17 -Wall -fsanitize=address,undefined` and passed its tests.

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

Maximum points per set: set 1: 500, set 2: 600, set 3: 600, set 4: 600, set 5: 600, set 6: 700, set 7: 700, set 8: 600. Because the maximum differs, score yourself as a percentage of the set's maximum:

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

## SET 1. Warm-up

90 minutes · maximum 500 points · suggested date Sat 13 Feb 2027. Topics are hidden on purpose: working out the pattern is part of the test.

Problem 1[Valid Anagram ↗](https://leetcode.com/problems/valid-anagram/)Easy10 min · 100 pts

Decide whether two strings use exactly the same letters the same number of times.

https://leetcode.com/problems/valid-anagram/

Your score: \_\_\_\_\_\_ / 100    Time used: \_\_\_\_\_\_ min    Wrong submissions: \_\_\_\_\_\_

Problem 2[Find All Anagrams in a String ↗](https://leetcode.com/problems/find-all-anagrams-in-a-string/)Medium35 min · 200 pts

Return every start index in s where a rearrangement of p begins.

https://leetcode.com/problems/find-all-anagrams-in-a-string/

Your score: \_\_\_\_\_\_ / 200    Time used: \_\_\_\_\_\_ min    Wrong submissions: \_\_\_\_\_\_

Problem 3[Asteroid Collision ↗](https://leetcode.com/problems/asteroid-collision/)Medium45 min · 200 pts

Asteroids move right (positive) or left (negative); when they meet the smaller explodes, equal ones both explode. Return the survivors.

https://leetcode.com/problems/asteroid-collision/

Your score: \_\_\_\_\_\_ / 200    Time used: \_\_\_\_\_\_ min    Wrong submissions: \_\_\_\_\_\_

Total: \_\_\_\_\_\_ / 500 = \_\_\_\_\_\_ %    [Solutions for this set →](#set-1-solutions)

## SET 1. Solutions

Focus: Hashing, sliding window, stack. Read the sketch first, then rewrite the code yourself from memory.

### 1. [Valid Anagram](https://leetcode.com/problems/valid-anagram/) Easy [Hashing](knowledge-base/dsa.md#hashing-and-frequency-maps)

1.  Count the 26 letters of s, subtract the letters of t, and check every count is zero.
2.  Return false early if the lengths differ.

**Complexity:** O(n) time, O(1) space   **Edge cases:** Different lengths; Unicode input (use a hash map instead of an array)

``` text
bool isAnagram(string s, string t) {
    if (s.size() != t.size()) return false;
    int c[26] = {};
    for (int i = 0; i < (int)s.size(); i++) { c[s[i] - 'a']++; c[t[i] - 'a']--; }
    for (int x : c) if (x) return false;
    return true;
}
```

### 2. [Find All Anagrams in a String](https://leetcode.com/problems/find-all-anagrams-in-a-string/) Medium [Sliding window](knowledge-base/dsa.md#sliding-window)

1.  Keep a window of length \|p\| over s with letter counts.
2.  Add the entering letter, remove the leaving one, and record the start index whenever the window counts equal p's counts.

**Complexity:** O(26·n) time, O(1) space   **Edge cases:** p longer than s returns an empty list; Overlapping answers (both must be reported)

``` cpp
vector<int> findAnagrams(string s, string p) {
    vector<int> r; if (p.size() > s.size()) return r;
    array<int, 26> a{}, b{}; int k = p.size();
    for (char c : p) a[c - 'a']++;
    for (int i = 0; i < (int)s.size(); i++) {
        b[s[i] - 'a']++;
        if (i >= k) b[s[i - k] - 'a']--;
        if (i >= k - 1 && a == b) r.push_back(i - k + 1);
    }
    return r;
}
```

### 3. [Asteroid Collision](https://leetcode.com/problems/asteroid-collision/) Medium [Stack](knowledge-base/dsa.md#stacks-and-queues)

1.  Scan left to right with a stack of survivors.
2.  Only a left-moving asteroid can hit the stack top, and only if the top moves right.
3.  While that holds: if the top is smaller, pop it and keep checking; if equal, pop it and the current one dies; if larger, the current one dies.
4.  Push the current asteroid if it survived.

**Complexity:** O(n) time, O(n) space   **Edge cases:** A left-mover with nothing to its left survives; Equal sizes destroy both

``` cpp
vector<int> asteroidCollision(vector<int>& a) {
    vector<int> st;
    for (int x : a) {
        bool alive = true;
        while (alive && x < 0 && !st.empty() && st.back() > 0) {
            if (st.back() < -x) st.pop_back();
            else { if (st.back() == -x) st.pop_back(); alive = false; }
        }
        if (alive) st.push_back(x);
    }
    return st;
}
```

## SET 2. Counting and graphs

90 minutes · maximum 600 points · suggested date Sat 27 Feb 2027. Topics are hidden on purpose: working out the pattern is part of the test.

Problem 1[Move Zeroes ↗](https://leetcode.com/problems/move-zeroes/)Easy10 min · 100 pts

Move all zeros to the end in place, keeping the order of the other numbers.

https://leetcode.com/problems/move-zeroes/

Your score: \_\_\_\_\_\_ / 100    Time used: \_\_\_\_\_\_ min    Wrong submissions: \_\_\_\_\_\_

Problem 2[Task Scheduler ↗](https://leetcode.com/problems/task-scheduler/)Medium35 min · 200 pts

Tasks A–Z take one unit each; the same task needs n idle units between runs. Find the least total time.

https://leetcode.com/problems/task-scheduler/

Your score: \_\_\_\_\_\_ / 200    Time used: \_\_\_\_\_\_ min    Wrong submissions: \_\_\_\_\_\_

Problem 3[Word Ladder ↗](https://leetcode.com/problems/word-ladder/)Hard45 min · 300 pts

Change one letter at a time, each step a dictionary word; return the number of words in the shortest sequence from begin to end, or 0.

https://leetcode.com/problems/word-ladder/

Your score: \_\_\_\_\_\_ / 300    Time used: \_\_\_\_\_\_ min    Wrong submissions: \_\_\_\_\_\_

Total: \_\_\_\_\_\_ / 600 = \_\_\_\_\_\_ %    [Solutions for this set →](#set-2-solutions)

## SET 2. Solutions

Focus: Two pointers, greedy counting, BFS. Read the sketch first, then rewrite the code yourself from memory.

### 1. [Move Zeroes](https://leetcode.com/problems/move-zeroes/) Easy [Two pointers](knowledge-base/dsa.md#two-pointers)

1.  Keep a write index w. Swap each non-zero a\[i\] into a\[w\] and advance w.

**Complexity:** O(n) time, O(1) space   **Edge cases:** All zeros or no zeros; Must be in place

``` cpp
void moveZeroes(vector<int>& a) { int w = 0; for (int i = 0; i < (int)a.size(); i++) if (a[i]) swap(a[w++], a[i]); }
```

### 2. [Task Scheduler](https://leetcode.com/problems/task-scheduler/) Medium [Greedy](knowledge-base/dsa.md#greedy-algorithms)

1.  Let f be the highest task frequency and k the number of tasks with that frequency.
2.  The most frequent tasks form f−1 blocks of length n+1, plus a final block of k tasks: (f−1)(n+1)+k.
3.  If there are more tasks than that, no idle time is needed: the answer is max(total tasks, (f−1)(n+1)+k).

**Complexity:** O(N) time, O(1) space   **Edge cases:** n = 0 (answer is the number of tasks); Several tasks share the top frequency

``` cpp
int leastInterval(vector<char>& t, int n) {
    int c[26] = {}; for (char x : t) c[x - 'A']++;
    int f = *max_element(c, c + 26), k = count(c, c + 26, f);
    return max((int)t.size(), (f - 1) * (n + 1) + k);
}
```

### 3. [Word Ladder](https://leetcode.com/problems/word-ladder/) Hard [BFS](knowledge-base/dsa.md#bfs-and-graph-basics)

1.  BFS from beginWord; each level is one more word in the sequence.
2.  Neighbours: change each position to every letter a–z and keep the results that are in the word set.
3.  Erase a word from the set when you enqueue it so it is never visited twice.
4.  Return the level when endWord is reached; 0 if the queue empties.

**Complexity:** O(N · L · 26) time, O(N · L) space   **Edge cases:** endWord not in the list returns 0; Count words, not steps (begin counts as 1)

``` cpp
int ladderLength(string b, string e, vector<string>& w) {
    unordered_set<string> d(w.begin(), w.end()); if (!d.count(e)) return 0;
    queue<string> q; q.push(b); d.erase(b);
    for (int lvl = 1; !q.empty(); lvl++) {
        for (int s = q.size(); s--; ) {
            string u = q.front(); q.pop(); if (u == e) return lvl;
            for (int i = 0; i < (int)u.size(); i++) { char o = u[i];
                for (char c = 'a'; c <= 'z'; c++) { u[i] = c; if (d.count(u)) { d.erase(u); q.push(u); } }
                u[i] = o; }
        }
    }
    return 0;
}
```

## SET 3. Windows and greedy

90 minutes · maximum 600 points · suggested date Sat 13 Mar 2027. Topics are hidden on purpose: working out the pattern is part of the test.

Problem 1[Maximum Average Subarray I ↗](https://leetcode.com/problems/maximum-average-subarray-i/)Easy10 min · 100 pts

Find the largest average of any contiguous block of length k.

https://leetcode.com/problems/maximum-average-subarray-i/

Your score: \_\_\_\_\_\_ / 100    Time used: \_\_\_\_\_\_ min    Wrong submissions: \_\_\_\_\_\_

Problem 2[Longest Repeating Character Replacement ↗](https://leetcode.com/problems/longest-repeating-character-replacement/)Medium35 min · 200 pts

With at most k letter changes, find the longest block of one repeated letter.

https://leetcode.com/problems/longest-repeating-character-replacement/

Your score: \_\_\_\_\_\_ / 200    Time used: \_\_\_\_\_\_ min    Wrong submissions: \_\_\_\_\_\_

Problem 3[Candy ↗](https://leetcode.com/problems/candy/)Hard45 min · 300 pts

Each child gets at least one candy; a child rated higher than a neighbour gets more than that neighbour. Find the minimum total.

https://leetcode.com/problems/candy/

Your score: \_\_\_\_\_\_ / 300    Time used: \_\_\_\_\_\_ min    Wrong submissions: \_\_\_\_\_\_

Total: \_\_\_\_\_\_ / 600 = \_\_\_\_\_\_ %    [Solutions for this set →](#set-3-solutions)

## SET 3. Solutions

Focus: Fixed and variable windows, two-pass greedy. Read the sketch first, then rewrite the code yourself from memory.

### 1. [Maximum Average Subarray I](https://leetcode.com/problems/maximum-average-subarray-i/) Easy [Sliding window](knowledge-base/dsa.md#sliding-window)

1.  Sum the first k numbers, then slide: add the entering number, subtract the leaving one, keep the best sum. Divide once at the end.

**Complexity:** O(n) time, O(1) space   **Edge cases:** Negative numbers (start best at the first window, not 0)

``` cpp
double findMaxAverage(vector<int>& a, int k) {
    long long s = 0; for (int i = 0; i < k; i++) s += a[i];
    long long best = s; for (int i = k; i < (int)a.size(); i++) { s += a[i] - a[i - k]; best = max(best, s); }
    return (double)best / k;
}
```

### 2. [Longest Repeating Character Replacement](https://leetcode.com/problems/longest-repeating-character-replacement/) Medium [Sliding window](knowledge-base/dsa.md#sliding-window)

1.  A window is fixable if its length minus the count of its most common letter is at most k.
2.  Expand right; track the highest count seen; while the window is not fixable, move left.
3.  The highest count never needs to go down: the answer only grows when it grows.

**Complexity:** O(n) time, O(1) space   **Edge cases:** k = 0; Whole string fixable

``` text
int characterReplacement(string s, int k) {
    int c[26] = {}, mx = 0, l = 0, best = 0;
    for (int r = 0; r < (int)s.size(); r++) {
        mx = max(mx, ++c[s[r] - 'A']);
        while (r - l + 1 - mx > k) c[s[l++] - 'A']--;
        best = max(best, r - l + 1);
    }
    return best;
}
```

### 3. [Candy](https://leetcode.com/problems/candy/) Hard [Greedy](knowledge-base/dsa.md#greedy-algorithms)

1.  Left to right: if rating rises, give one more than the left neighbour.
2.  Right to left: if rating is higher than the right neighbour, take max(current, right + 1).
3.  Sum the array.

**Complexity:** O(n) time, O(n) space   **Edge cases:** Equal neighbours have no constraint; Strictly falling ratings

``` cpp
int candy(vector<int>& r) {
    int n = r.size(); vector<int> c(n, 1);
    for (int i = 1; i < n; i++) if (r[i] > r[i - 1]) c[i] = c[i - 1] + 1;
    for (int i = n - 2; i >= 0; i--) if (r[i] > r[i + 1]) c[i] = max(c[i], c[i + 1] + 1);
    return accumulate(c.begin(), c.end(), 0);
}
```

## SET 4. Stacks and binary search

90 minutes · maximum 600 points · suggested date Sat 24 Apr 2027. Topics are hidden on purpose: working out the pattern is part of the test.

Problem 1[Climbing Stairs ↗](https://leetcode.com/problems/climbing-stairs/)Easy10 min · 100 pts

Count the ways to climb n steps taking 1 or 2 at a time.

https://leetcode.com/problems/climbing-stairs/

Your score: \_\_\_\_\_\_ / 100    Time used: \_\_\_\_\_\_ min    Wrong submissions: \_\_\_\_\_\_

Problem 2[Evaluate Reverse Polish Notation ↗](https://leetcode.com/problems/evaluate-reverse-polish-notation/)Medium25 min · 200 pts

Evaluate an expression written in postfix form with + − × ÷ (division truncates toward zero).

https://leetcode.com/problems/evaluate-reverse-polish-notation/

Your score: \_\_\_\_\_\_ / 200    Time used: \_\_\_\_\_\_ min    Wrong submissions: \_\_\_\_\_\_

Problem 3[Median of Two Sorted Arrays ↗](https://leetcode.com/problems/median-of-two-sorted-arrays/)Hard55 min · 300 pts

Find the median of two sorted arrays in logarithmic time.

https://leetcode.com/problems/median-of-two-sorted-arrays/

Your score: \_\_\_\_\_\_ / 300    Time used: \_\_\_\_\_\_ min    Wrong submissions: \_\_\_\_\_\_

Total: \_\_\_\_\_\_ / 600 = \_\_\_\_\_\_ %    [Solutions for this set →](#set-4-solutions)

## SET 4. Solutions

Focus: DP warm-up, stack evaluation, partition search. Read the sketch first, then rewrite the code yourself from memory.

### 1. [Climbing Stairs](https://leetcode.com/problems/climbing-stairs/) Easy [DP](knowledge-base/dsa.md#dynamic-programming)

1.  ways(n) = ways(n−1) + ways(n−2): the Fibonacci recurrence. Keep two variables.

**Complexity:** O(n) time, O(1) space   **Edge cases:** n = 1

``` text
int climbStairs(int n) { long long a = 1, b = 1; for (int i = 2; i <= n; i++) { long long c = a + b; a = b; b = c; } return b; }
```

### 2. [Evaluate Reverse Polish Notation](https://leetcode.com/problems/evaluate-reverse-polish-notation/) Medium [Stack](knowledge-base/dsa.md#stacks-and-queues)

1.  Push numbers on a stack.
2.  On an operator, pop b then a (order matters for − and ÷) and push a op b.
3.  C++ integer division already truncates toward zero.

**Complexity:** O(n) time, O(n) space   **Edge cases:** Negative numbers such as "-11" are numbers, not operators; Operand order for − and ÷

``` cpp
int evalRPN(vector<string>& t) {
    vector<long long> st;
    for (auto& x : t) {
        if (x.size() == 1 && string("+-*/").find(x) != string::npos) {
            long long b = st.back(); st.pop_back(); long long a = st.back(); st.pop_back();
            st.push_back(x == "+" ? a + b : x == "-" ? a - b : x == "*" ? a * b : a / b);
        } else st.push_back(stoll(x));
    }
    return st.back();
}
```

### 3. [Median of Two Sorted Arrays](https://leetcode.com/problems/median-of-two-sorted-arrays/) Hard [Binary search](knowledge-base/dsa.md#binary-search)

1.  Binary search a cut i in the smaller array A; the cut in B is j = (m+n+1)/2 − i, so the left halves together hold half the elements.
2.  The cut is right when A\[i−1\] ≤ B\[j\] and B\[j−1\] ≤ A\[i\] (use ±infinity past the ends).
3.  If A\[i−1\] \> B\[j\] move left, else move right.
4.  Median: max of the left sides (odd total), or its average with the min of the right sides (even total).

**Complexity:** O(log min(m, n)) time, O(1) space   **Edge cases:** One array empty; All of A smaller than all of B

``` cpp
double findMedianSortedArrays(vector<int>& A, vector<int>& B) {
    if (A.size() > B.size()) return findMedianSortedArrays(B, A);
    int m = A.size(), n = B.size(), lo = 0, hi = m;
    while (lo <= hi) {
        int i = (lo + hi) / 2, j = (m + n + 1) / 2 - i;
        int la = i ? A[i - 1] : INT_MIN, ra = i < m ? A[i] : INT_MAX, lb = j ? B[j - 1] : INT_MIN, rb = j < n ? B[j] : INT_MAX;
        if (la > rb) hi = i - 1;
        else if (lb > ra) lo = i + 1;
        else return (m + n) % 2 ? max(la, lb) : (max(la, lb) + (double)min(ra, rb)) / 2;
    }
    return 0;
}
```

## SET 5. Simulation and shortest paths

90 minutes · maximum 600 points · suggested date Sat 8 May 2027. Topics are hidden on purpose: working out the pattern is part of the test.

Problem 1[Happy Number ↗](https://leetcode.com/problems/happy-number/)Easy15 min · 100 pts

Repeatedly replace a number by the sum of the squares of its digits; is 1 reached?

https://leetcode.com/problems/happy-number/

Your score: \_\_\_\_\_\_ / 100    Time used: \_\_\_\_\_\_ min    Wrong submissions: \_\_\_\_\_\_

Problem 2[Car Fleet ↗](https://leetcode.com/problems/car-fleet/)Medium30 min · 200 pts

Cars drive toward a target and cannot pass; a faster car that catches up joins the slower one as a fleet. How many fleets arrive?

https://leetcode.com/problems/car-fleet/

Your score: \_\_\_\_\_\_ / 200    Time used: \_\_\_\_\_\_ min    Wrong submissions: \_\_\_\_\_\_

Problem 3[Swim in Rising Water ↗](https://leetcode.com/problems/swim-in-rising-water/)Hard45 min · 300 pts

In an n × n grid of heights, at time t you can stand on cells of height ≤ t. Find the earliest time to go from top-left to bottom-right.

https://leetcode.com/problems/swim-in-rising-water/

Your score: \_\_\_\_\_\_ / 300    Time used: \_\_\_\_\_\_ min    Wrong submissions: \_\_\_\_\_\_

Total: \_\_\_\_\_\_ / 600 = \_\_\_\_\_\_ %    [Solutions for this set →](#set-5-solutions)

## SET 5. Solutions

Focus: Cycle detection, sorting, Dijkstra on a grid. Read the sketch first, then rewrite the code yourself from memory.

### 1. [Happy Number](https://leetcode.com/problems/happy-number/) Easy [Linked list](knowledge-base/dsa.md#linked-lists)

1.  The sequence either reaches 1 or loops. Use Floyd's slow and fast pointers on the sequence (or a set of seen values).

**Complexity:** O(log n) per step; few steps in practice   **Edge cases:** n = 1 is happy

``` text
int nxt(int n) { int s = 0; while (n) { s += (n % 10) * (n % 10); n /= 10; } return s; }
bool isHappy(int n) { int s = n, f = nxt(n); while (f != 1 && s != f) { s = nxt(s); f = nxt(nxt(f)); } return f == 1; }
```

### 2. [Car Fleet](https://leetcode.com/problems/car-fleet/) Medium [Stack](knowledge-base/dsa.md#monotonic-stack)

1.  Sort cars by position, closest to the target first.
2.  Compute each car's arrival time (target − position) / speed.
3.  A car that would arrive later than the fleet ahead of it starts a new fleet; otherwise it joins that fleet. Count new fleets.

**Complexity:** O(n log n) time, O(n) space   **Edge cases:** Equal arrival times merge; Use floating point or compare by cross-multiplication

``` cpp
int carFleet(int target, vector<int>& pos, vector<int>& sp) {
    int n = pos.size(); vector<pair<int, double>> c(n);
    for (int i = 0; i < n; i++) c[i] = {pos[i], (double)(target - pos[i]) / sp[i]};
    sort(c.rbegin(), c.rend());
    int fleets = 0; double cur = 0;
    for (auto& [p, t] : c) if (t > cur) { fleets++; cur = t; }
    return fleets;
}
```

### 3. [Swim in Rising Water](https://leetcode.com/problems/swim-in-rising-water/) Hard [Shortest paths](knowledge-base/dsa.md#dijkstra-and-shortest-paths)

1.  The cost of a path is its highest cell. Run Dijkstra where the distance is the max height along the path.
2.  Pop the cell with the smallest current max; push neighbours with max(current, their height).
3.  The first time the target is popped, its value is the answer.

**Complexity:** O(n² log n) time, O(n²) space   **Edge cases:** Start cell height counts; Binary search on t plus BFS also works

``` cpp
int swimInWater(vector<vector<int>>& g) {
    int n = g.size(); vector<vector<int>> seen(n, vector<int>(n));
    priority_queue<array<int, 3>, vector<array<int, 3>>, greater<>> pq; pq.push({g[0][0], 0, 0}); int d[] = {1, 0, -1, 0, 1};
    while (true) {
        auto [t, r, c] = pq.top(); pq.pop();
        if (r == n - 1 && c == n - 1) return t;
        if (seen[r][c]++) continue;
        for (int k = 0; k < 4; k++) { int x = r + d[k], y = c + d[k + 1]; if (x >= 0 && y >= 0 && x < n && y < n && !seen[x][y]) pq.push({max(t, g[x][y]), x, y}); }
    }
}
```

## SET 6. Mediums under pressure

90 minutes · maximum 700 points · suggested date Sat 22 May 2027. Topics are hidden on purpose: working out the pattern is part of the test.

Problem 1[Find K Closest Elements ↗](https://leetcode.com/problems/find-k-closest-elements/)Medium25 min · 200 pts

From a sorted array, return the k values closest to x in ascending order (ties go to the smaller value).

https://leetcode.com/problems/find-k-closest-elements/

Your score: \_\_\_\_\_\_ / 200    Time used: \_\_\_\_\_\_ min    Wrong submissions: \_\_\_\_\_\_

Problem 2[Accounts Merge ↗](https://leetcode.com/problems/accounts-merge/)Medium35 min · 200 pts

Accounts that share any email belong to the same person; merge them and output each person's sorted emails.

https://leetcode.com/problems/accounts-merge/

Your score: \_\_\_\_\_\_ / 200    Time used: \_\_\_\_\_\_ min    Wrong submissions: \_\_\_\_\_\_

Problem 3[Burst Balloons ↗](https://leetcode.com/problems/burst-balloons/)Hard30 min · 300 pts

Bursting balloon i earns left × i × right of its current neighbours. Find the maximum total.

https://leetcode.com/problems/burst-balloons/

Your score: \_\_\_\_\_\_ / 300    Time used: \_\_\_\_\_\_ min    Wrong submissions: \_\_\_\_\_\_

Total: \_\_\_\_\_\_ / 700 = \_\_\_\_\_\_ %    [Solutions for this set →](#set-6-solutions)

## SET 6. Solutions

Focus: Binary search on a window, union-find, interval DP. Read the sketch first, then rewrite the code yourself from memory.

### 1. [Find K Closest Elements](https://leetcode.com/problems/find-k-closest-elements/) Medium [Binary search](knowledge-base/dsa.md#binary-search)

1.  The answer is a block a\[lo..lo+k). Binary search lo in \[0, n−k\].
2.  Compare x − a\[mid\] with a\[mid+k\] − x: if the left end is farther, the block must start after mid; otherwise at or before mid.

**Complexity:** O(log(n − k) + k) time   **Edge cases:** x outside the array range; Ties prefer the smaller value

``` cpp
vector<int> findClosestElements(vector<int>& a, int k, int x) {
    int lo = 0, hi = a.size() - k;
    while (lo < hi) { int mid = (lo + hi) / 2; if (x - a[mid] > a[mid + k] - x) lo = mid + 1; else hi = mid; }
    return vector<int>(a.begin() + lo, a.begin() + lo + k);
}
```

### 2. [Accounts Merge](https://leetcode.com/problems/accounts-merge/) Medium [Union-find](knowledge-base/dsa.md#disjoint-set-union-union-find)

1.  Give every email an id. Union all emails inside each account with its first email.
2.  Group emails by their root, remember a name per email, sort each group and put the name first.

**Complexity:** O(E log E) time for the sorting, near-linear for the unions   **Edge cases:** Same name does not mean same person; An account with a single email

``` cpp
struct DSU { vector<int> p; int f(int x) { return p[x] == x ? x : p[x] = f(p[x]); } void u(int a, int b) { p[f(a)] = f(b); } };
vector<vector<string>> accountsMerge(vector<vector<string>>& acc) {
    unordered_map<string, int> id; unordered_map<string, string> name; DSU d;
    for (auto& a : acc) for (int i = 1; i < (int)a.size(); i++) { if (!id.count(a[i])) { id[a[i]] = d.p.size(); d.p.push_back(d.p.size()); } name[a[i]] = a[0]; d.u(id[a[i]], id[a[1]]); }
    map<int, vector<string>> g; for (auto& [e, i] : id) g[d.f(i)].push_back(e);
    vector<vector<string>> r;
    for (auto& [root, v] : g) { sort(v.begin(), v.end()); v.insert(v.begin(), name[v[0]]); r.push_back(v); }
    return r;
}
```

### 3. [Burst Balloons](https://leetcode.com/problems/burst-balloons/) Hard [DP](knowledge-base/dsa.md#dynamic-programming)

1.  Pad the array with 1 at both ends.
2.  Think of the last balloon k burst in the open interval (l, r): its neighbours are then l and r.
3.  dp\[l\]\[r\] = max over l \< k \< r of dp\[l\]\[k\] + dp\[k\]\[r\] + a\[l\]·a\[k\]·a\[r\]. Fill by increasing interval length.

**Complexity:** O(n³) time, O(n²) space   **Edge cases:** Choosing the first balloon to burst does not split the problem; the last one does

``` cpp
int maxCoins(vector<int>& v) {
    vector<int> a{1}; a.insert(a.end(), v.begin(), v.end()); a.push_back(1); int n = a.size();
    vector<vector<int>> dp(n, vector<int>(n, 0));
    for (int len = 2; len < n; len++) for (int l = 0; l + len < n; l++) { int r = l + len;
        for (int k = l + 1; k < r; k++) dp[l][r] = max(dp[l][r], dp[l][k] + dp[k][r] + a[l] * a[k] * a[r]); }
    return dp[0][n - 1];
}
```

## SET 7. Arrays and answer search

90 minutes · maximum 700 points · suggested date Sat 12 Jun 2027. Topics are hidden on purpose: working out the pattern is part of the test.

Problem 1[Rotate Array ↗](https://leetcode.com/problems/rotate-array/)Medium20 min · 200 pts

Rotate an array to the right by k steps in place.

https://leetcode.com/problems/rotate-array/

Your score: \_\_\_\_\_\_ / 200    Time used: \_\_\_\_\_\_ min    Wrong submissions: \_\_\_\_\_\_

Problem 2[Minimum Number of Arrows to Burst Balloons ↗](https://leetcode.com/problems/minimum-number-of-arrows-to-burst-balloons/)Medium30 min · 200 pts

Balloons are intervals on a line; a vertical arrow at x bursts every balloon covering x. Find the fewest arrows.

https://leetcode.com/problems/minimum-number-of-arrows-to-burst-balloons/

Your score: \_\_\_\_\_\_ / 200    Time used: \_\_\_\_\_\_ min    Wrong submissions: \_\_\_\_\_\_

Problem 3[Split Array Largest Sum ↗](https://leetcode.com/problems/split-array-largest-sum/)Hard40 min · 300 pts

Split the array into k non-empty contiguous parts so the largest part sum is as small as possible.

https://leetcode.com/problems/split-array-largest-sum/

Your score: \_\_\_\_\_\_ / 300    Time used: \_\_\_\_\_\_ min    Wrong submissions: \_\_\_\_\_\_

Total: \_\_\_\_\_\_ / 700 = \_\_\_\_\_\_ %    [Solutions for this set →](#set-7-solutions)

## SET 7. Solutions

Focus: In-place tricks, interval greedy, binary search on the answer. Read the sketch first, then rewrite the code yourself from memory.

### 1. [Rotate Array](https://leetcode.com/problems/rotate-array/) Medium [Two pointers](knowledge-base/dsa.md#two-pointers)

1.  k %= n. Reverse the whole array, then reverse the first k elements, then the rest.

**Complexity:** O(n) time, O(1) space   **Edge cases:** k larger than n; k = 0

``` cpp
void rotate(vector<int>& a, int k) { k %= a.size(); reverse(a.begin(), a.end()); reverse(a.begin(), a.begin() + k); reverse(a.begin() + k, a.end()); }
```

### 2. [Minimum Number of Arrows to Burst Balloons](https://leetcode.com/problems/minimum-number-of-arrows-to-burst-balloons/) Medium [Intervals](knowledge-base/dsa.md#interval-problems)

1.  Sort by end. Shoot the first arrow at the first end.
2.  A balloon starting after the current arrow position needs a new arrow at its end; touching counts as burst.

**Complexity:** O(n log n) time   **Edge cases:** Touching intervals share an arrow (use \>, not ≥); Large coordinates: compare, do not subtract

``` cpp
int findMinArrowShots(vector<vector<int>>& p) {
    sort(p.begin(), p.end(), [](auto& a, auto& b) { return a[1] < b[1]; });
    int arrows = 1; long long x = p[0][1];
    for (auto& b : p) if (b[0] > x) { arrows++; x = b[1]; }
    return arrows;
}
```

### 3. [Split Array Largest Sum](https://leetcode.com/problems/split-array-largest-sum/) Hard [Binary search](knowledge-base/dsa.md#binary-search)

1.  Binary search the answer S between max(a) and sum(a).
2.  Check S greedily: fill parts left to right, starting a new part when adding the next number would exceed S. S works if at most k parts are needed.
3.  Find the smallest S that works.

**Complexity:** O(n log(sum)) time, O(1) space   **Edge cases:** Low bound must be max(a), not 0; Use long long for sums

``` cpp
int splitArray(vector<int>& a, int k) {
    long long lo = *max_element(a.begin(), a.end()), hi = accumulate(a.begin(), a.end(), 0LL);
    while (lo < hi) {
        long long mid = (lo + hi) / 2, cur = 0; int parts = 1;
        for (int x : a) { if (cur + x > mid) { parts++; cur = 0; } cur += x; }
        if (parts <= k) hi = mid; else lo = mid + 1;
    }
    return lo;
}
```

## SET 8. Final dress rehearsal

90 minutes · maximum 600 points · suggested date Sat 3 Jul 2027. Topics are hidden on purpose: working out the pattern is part of the test.

Problem 1[First Unique Character in a String ↗](https://leetcode.com/problems/first-unique-character-in-a-string/)Easy10 min · 100 pts

Return the index of the first letter that appears exactly once, or −1.

https://leetcode.com/problems/first-unique-character-in-a-string/

Your score: \_\_\_\_\_\_ / 100    Time used: \_\_\_\_\_\_ min    Wrong submissions: \_\_\_\_\_\_

Problem 2[Number of Longest Increasing Subsequence ↗](https://leetcode.com/problems/number-of-longest-increasing-subsequence/)Medium35 min · 200 pts

Count how many strictly increasing subsequences have the maximum length.

https://leetcode.com/problems/number-of-longest-increasing-subsequence/

Your score: \_\_\_\_\_\_ / 200    Time used: \_\_\_\_\_\_ min    Wrong submissions: \_\_\_\_\_\_

Problem 3[Regular Expression Matching ↗](https://leetcode.com/problems/regular-expression-matching/)Hard45 min · 300 pts

Match a whole string against a pattern with '.' (any letter) and '\*' (zero or more of the previous element).

https://leetcode.com/problems/regular-expression-matching/

Your score: \_\_\_\_\_\_ / 300    Time used: \_\_\_\_\_\_ min    Wrong submissions: \_\_\_\_\_\_

Total: \_\_\_\_\_\_ / 600 = \_\_\_\_\_\_ %    [Solutions for this set →](#set-8-solutions)

## SET 8. Solutions

Focus: Counting, DP with counts, string DP. Read the sketch first, then rewrite the code yourself from memory.

### 1. [First Unique Character in a String](https://leetcode.com/problems/first-unique-character-in-a-string/) Easy [Hashing](knowledge-base/dsa.md#hashing-and-frequency-maps)

1.  Count letters in one pass; return the first index whose count is 1 in a second pass.

**Complexity:** O(n) time, O(1) space   **Edge cases:** No unique letter returns −1

``` text
int firstUniqChar(string s) { int c[26] = {}; for (char x : s) c[x - 'a']++; for (int i = 0; i < (int)s.size(); i++) if (c[s[i] - 'a'] == 1) return i; return -1; }
```

### 2. [Number of Longest Increasing Subsequence](https://leetcode.com/problems/number-of-longest-increasing-subsequence/) Medium [DP](knowledge-base/dsa.md#dynamic-programming)

1.  len\[i\] = longest increasing subsequence ending at i; cnt\[i\] = how many of that length.
2.  For each j \< i with a\[j\] \< a\[i\]: a longer length from j resets cnt\[i\] to cnt\[j\]; an equal length adds cnt\[j\].
3.  Sum cnt\[i\] over all i with len\[i\] equal to the maximum.

**Complexity:** O(n²) time, O(n) space   **Edge cases:** All equal values (every single element counts); Reset, do not add, when a longer length appears

``` cpp
int findNumberOfLIS(vector<int>& a) {
    int n = a.size(), best = 0, ans = 0; vector<int> len(n, 1), cnt(n, 1);
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < i; j++) if (a[j] < a[i]) {
            if (len[j] + 1 > len[i]) { len[i] = len[j] + 1; cnt[i] = cnt[j]; }
            else if (len[j] + 1 == len[i]) cnt[i] += cnt[j];
        }
        if (len[i] > best) { best = len[i]; ans = cnt[i]; } else if (len[i] == best) ans += cnt[i];
    }
    return ans;
}
```

### 3. [Regular Expression Matching](https://leetcode.com/problems/regular-expression-matching/) Hard [DP](knowledge-base/dsa.md#dynamic-programming)

1.  dp\[i\]\[j\] = does s\[i..\] match p\[j..\]? dp\[n\]\[m\] = true.
2.  first = i \< n and (p\[j\] == s\[i\] or p\[j\] == '.').
3.  If p\[j+1\] is '\*': dp\[i\]\[j\] = dp\[i\]\[j+2\] (use zero copies) or (first and dp\[i+1\]\[j\]) (use one more).
4.  Otherwise dp\[i\]\[j\] = first and dp\[i+1\]\[j+1\]. Fill from the back.

**Complexity:** O(nm) time and space   **Edge cases:** 'a\*' can match the empty string; The match must cover the whole string

``` cpp
bool isMatch(string s, string p) {
    int n = s.size(), m = p.size(); vector<vector<bool>> dp(n + 1, vector<bool>(m + 1, false)); dp[n][m] = true;
    for (int i = n; i >= 0; i--) for (int j = m - 1; j >= 0; j--) {
        bool first = i < n && (p[j] == s[i] || p[j] == '.');
        if (j + 1 < m && p[j + 1] == '*') dp[i][j] = dp[i][j + 2] || (first && dp[i + 1][j]);
        else dp[i][j] = first && dp[i + 1][j + 1];
    }
    return dp[0][0];
}
```
