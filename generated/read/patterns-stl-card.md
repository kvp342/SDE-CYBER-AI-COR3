DSA · QUICK REFERENCE

# Patterns, STL and 30 bugs to avoid

A one-page decision tree from what a problem says to the pattern to try, a two-page C++ STL card with complexities, and the thirty C++ mistakes that most often cost an accepted answer in contests and online assessments. Every STL call on the card was compiled and run (`generated/stl_check.cpp`).

|                                        |
|----------------------------------------|
| [Pattern decision tree](#pattern-decision-tree)       |
| [C++ STL card](#c-stl-card)                |
| [30 common C++ contest bugs](#30-common-c-contest-bugs) |

Start every problem by reading the constraints: n ≤ 20 → exponential is fine; n ≤ 5000 → O(n²); n ≤ 2·10⁵ → O(n log n); n ≤ 10⁷ → O(n).

## Pattern decision tree

Ask the questions top to bottom; the first match is usually the pattern. Each pattern links to its Knowledge Base page.

Is the input sorted, or can you sort it?

|                                                                       |     |                                                                                                |
|-----------------------------------------------------------------------|-----|------------------------------------------------------------------------------------------------|
| Find a pair or triple with a target sum                               | →   | [Two pointers](knowledge-base/dsa.md#two-pointers)                 |
| Find a value, first/last position, or insert point                    | →   | [Binary search](knowledge-base/dsa.md#binary-search)               |
| Minimise the maximum / 'smallest X such that …' with a monotone check | →   | [Binary search on the answer](knowledge-base/dsa.md#binary-search) |
| Merge or count overlapping ranges                                     | →   | [Sort + sweep (intervals)](knowledge-base/dsa.md#interval-problems)        |

Contiguous subarray or substring?

|                                          |     |                                                                                                                         |
|------------------------------------------|-----|-------------------------------------------------------------------------------------------------------------------------|
| Longest/shortest window with a condition | →   | [Sliding window (variable)](knowledge-base/dsa.md#sliding-window)                           |
| Every window of size k                   | →   | [Sliding window (fixed); monotonic deque for max/min](knowledge-base/dsa.md#sliding-window) |
| Subarray sum equals k, with negatives    | →   | [Prefix sum + hash map](knowledge-base/dsa.md#prefix-sums)                                   |
| Maximum subarray sum                     | →   | [Kadane](knowledge-base/dsa.md#dynamic-programming)                                                          |

Next greater/smaller, spans, histograms?

|                                                      |     |                                                                                      |
|------------------------------------------------------|-----|--------------------------------------------------------------------------------------|
| Next greater element, stock span, daily temperatures | →   | [Monotonic stack](knowledge-base/dsa.md#monotonic-stack) |
| Matching brackets, undo, expression evaluation       | →   | [Stack](knowledge-base/dsa.md#stacks-and-queues)               |

Top k, k-th largest, running median, merge k lists?

|                       |     |                                                                                 |
|-----------------------|-----|---------------------------------------------------------------------------------|
| Need repeated min/max | →   | [Heap (priority_queue)](knowledge-base/dsa.md#heaps-and-priority-queues) |
| Running median        | →   | [Two heaps](knowledge-base/dsa.md#heaps-and-priority-queues)             |

Graph or grid?

|                                                          |     |                                                                                 |
|----------------------------------------------------------|-----|---------------------------------------------------------------------------------|
| Shortest path, unweighted / levels                       | →   | [BFS](knowledge-base/dsa.md#bfs-and-graph-basics)                    |
| Shortest path, non-negative weights                      | →   | [Dijkstra](knowledge-base/dsa.md#dijkstra-and-shortest-paths)          |
| Connected components, islands, cycle in undirected graph | →   | [DFS / BFS / DSU](knowledge-base/dsa.md#disjoint-set-union-union-find)        |
| Ordering with prerequisites, cycle in directed graph     | →   | [Topological sort](knowledge-base/dsa.md#topological-sort) |
| Minimum spanning tree                                    | →   | [Kruskal (sort + DSU)](knowledge-base/dsa.md#disjoint-set-union-union-find)   |

Tree?

|                                        |     |                                                                                    |
|----------------------------------------|-----|------------------------------------------------------------------------------------|
| Depth, diameter, path sums, LCA        | →   | [DFS returning values up](knowledge-base/dsa.md#binary-trees) |
| Level by level                         | →   | [BFS by levels](knowledge-base/dsa.md#bfs-and-graph-basics)             |
| Sorted order or k-th smallest in a BST | →   | [Inorder traversal](knowledge-base/dsa.md#binary-search-trees)         |

All combinations, permutations, subsets, boards?

|                               |     |                                                                             |
|-------------------------------|-----|-----------------------------------------------------------------------------|
| Generate everything, n ≤ 20   | →   | [Backtracking](knowledge-base/dsa.md#recursion-and-backtracking) |
| n ≤ 20 and states of a subset | →   | [Bitmask DP](knowledge-base/dsa.md#bitmask-dp)  |

Count ways, min/max cost, overlapping subproblems?

|                                 |     |                                                                      |
|---------------------------------|-----|----------------------------------------------------------------------|
| Choices at each index or cell   | →   | [1-D / 2-D DP](knowledge-base/dsa.md#dynamic-programming) |
| Two strings: LCS, edit distance | →   | [String DP](knowledge-base/dsa.md#string-dp-lcs-and-edit-distance)   |
| Pick items under a capacity     | →   | [Knapsack DP](knowledge-base/dsa.md#dynamic-programming)  |

Prefix lookups, autocomplete, word search?

|                             |     |                                                                |
|-----------------------------|-----|----------------------------------------------------------------|
| Many words sharing prefixes | →   | [Trie](knowledge-base/dsa.md#tries) |

Local best choice provably leads to global best?

|                              |     |                                                                                                   |
|------------------------------|-----|---------------------------------------------------------------------------------------------------|
| Intervals, jumps, scheduling | →   | [Greedy (prove with exchange argument)](knowledge-base/dsa.md#greedy-algorithms) |

## C++ STL card

### vector\<T\>

|                                      |                      |
|--------------------------------------|----------------------|
| `push_back / pop_back / back`        | O(1) amortised       |
| `operator[] / at`                    | O(1)                 |
| `insert / erase in the middle`       | O(n)                 |
| `reserve(n)`                         | avoids reallocations |
| `sort(v.begin(), v.end())`           | O(n log n)           |
| `lower_bound / upper_bound (sorted)` | O(log n)             |

### string

|                                     |                |
|-------------------------------------|----------------|
| `s.substr(pos, len)`                | O(len), copies |
| `s.find(t)`                         | O(n·m) worst   |
| `to_string(x) / stoi(s) / stoll(s)` | conversions    |
| `s += c / s.push_back(c)`           | O(1) amortised |

### deque\<T\>

|                                                 |      |
|-------------------------------------------------|------|
| `push_front / push_back / pop_front / pop_back` | O(1) |
| `operator[]`                                    | O(1) |

### stack\<T\> / queue\<T\>

|                                |          |
|--------------------------------|----------|
| `push / pop / top / front`     | O(1)     |
| `empty() before top()/front()` | required |

### priority_queue\<T\>

|                                                               |                          |
|---------------------------------------------------------------|--------------------------|
| `push / pop`                                                  | O(log n)                 |
| `top`                                                         | O(1), largest by default |
| `min-heap: priority_queue<int, vector<int>, greater<int>>`    |                          |
| `custom: priority_queue<T, vector<T>, decltype(cmp)> pq(cmp)` |                          |

### set / map (red-black tree)

|                                               |                      |
|-----------------------------------------------|----------------------|
| `insert / erase / find / count`               | O(log n)             |
| `lower_bound(x) / upper_bound(x)`             | O(log n)             |
| `iterate in sorted order`                     | O(n)                 |
| `multiset: erase(s.find(x)) removes one copy` | erase(x) removes all |

### unordered_set / unordered_map

|                                       |                          |
|---------------------------------------|--------------------------|
| `insert / erase / find / count`       | O(1) average, O(n) worst |
| `m[key] inserts a default if missing` | use find/count to check  |
| `reserve(n)`                          | fewer rehashes           |

### \<algorithm\>

|                                                 |            |
|-------------------------------------------------|------------|
| `sort / stable_sort`                            | O(n log n) |
| `reverse / rotate`                              | O(n)       |
| `next_permutation`                              | O(n)       |
| `accumulate (<numeric>), use 0LL for long long` | O(n)       |
| `min_element / max_element`                     | O(n)       |
| `unique (after sort) + erase`                   | O(n)       |
| `binary_search`                                 | O(log n)   |
| `__gcd / gcd (C++17 <numeric>)`                 | O(log n)   |

### Others

|                                                         |               |
|---------------------------------------------------------|---------------|
| `pair<int,int>, tuple; structured bindings auto [a, b]` |               |
| `bitset<N>: count, set, test`                           | O(N/64)       |
| `iota(v.begin(), v.end(), 0)`                           | fill 0,1,2…   |
| `__builtin_popcount / __builtin_popcountll`             | GCC bit count |

## 30 common C++ contest bugs

| \#  | Bug                                        | What goes wrong                                                                           | Fix                                            |
|-----|--------------------------------------------|-------------------------------------------------------------------------------------------|------------------------------------------------|
| 1   | int overflow                               | a \* b with ints near 1e9; sums of 1e5 numbers up to 1e9                                  | Use long long; write 1LL \* a \* b             |
| 2   | accumulate with 0                          | accumulate(v.begin(), v.end(), 0) on long longs truncates                                 | Pass 0LL                                       |
| 3   | Signed/unsigned loop                       | for (int i = 0; i \< v.size() - 1; i++) with an empty v: size() − 1 wraps to a huge value | Cast: (int)v.size() - 1                        |
| 4   | Out-of-bounds index                        | a\[i + 1\] at the last index; grid neighbours off the edge                                | Check bounds before indexing                   |
| 5   | Uninitialised variables                    | int ans; then ans = max(ans, x)                                                           | Initialise every variable                      |
| 6   | Global vs local arrays                     | Large local array (1e6 ints) overflows the stack                                          | Make it global or use vector                   |
| 7   | Reset between test cases                   | Globals or containers keep old data across t test cases                                   | Clear or re-create per test                    |
| 8   | endl in loops                              | endl flushes every line: slow output                                                      | Use '\n'                                       |
| 9   | Slow I/O                                   | cin/cout without sync off on 1e6 numbers                                                  | ios::sync_with_stdio(false); cin.tie(nullptr); |
| 10  | Mixing scanf and cin after sync off        | Undefined interleaving once sync is off                                                   | Use one style                                  |
| 11  | map\[key\] creates keys                    | if (m\[x\]) inserts x and can grow the map in a loop                                      | Use m.count(x) or m.find(x)                    |
| 12  | Iterator invalidation                      | Erasing from a vector or map while iterating with the same iterator                       | it = v.erase(it), or collect then erase        |
| 13  | Modifying a container in range-for         | push_back while iterating a vector                                                        | Iterate by index over the old size             |
| 14  | Comparator not strict                      | sort with a \<= b crashes or misorders                                                    | Comparators must be strict: a \< b             |
| 15  | priority_queue order                       | Expecting smallest on top                                                                 | Default is max-heap; use greater\<\> for min   |
| 16  | multiset erase(value)                      | Removes every copy                                                                        | erase(s.find(x)) to remove one                 |
| 17  | Integer division and modulo with negatives | -7 / 2 == -3 and -7 % 2 == -1                                                             | For a positive mod: ((a % m) + m) % m          |
| 18  | Modular arithmetic                         | Forgetting % after each multiply                                                          | Reduce after every operation; use long long    |
| 19  | Floating point equality                    | if (x == 0.3)                                                                             | Compare with an epsilon, or use integers       |
| 20  | pow() for integers                         | pow(10, 9) returns double and can round down                                              | Write a binary exponentiation for integers     |
| 21  | Wrong INF                                  | INT_MAX + 1 overflows during relaxations                                                  | Use 1e18 as long long or check before adding   |
| 22  | memset with non-zero values                | memset(a, 1, sizeof a) sets bytes, not ints                                               | Only 0 and -1 are safe; use fill               |
| 23  | Recursion depth                            | DFS 1e6 deep overflows the stack                                                          | Iterative DFS or BFS                           |
| 24  | Passing big containers by value            | void f(vector\<int\> v) copies on every call                                              | Pass by const reference                        |
| 25  | string += in a loop with s = s + c         | s = s + c copies each time: O(n²)                                                         | Use s += c or s.push_back(c)                   |
| 26  | substr in a loop                           | s.substr inside a loop copies: hidden O(n²)                                               | Use indices or string_view                     |
| 27  | Off-by-one in binary search                | while (lo \< hi) with mid rounding the wrong way loops forever                            | Pick one template and stick to it              |
| 28  | Shadowed variables                         | Declaring n again inside a block hides the outer n                                        | Compile with -Wall -Wshadow                    |
| 29  | Edge cases                                 | n = 1, empty input, all equal, all negative, maximum values                               | Test them before submitting                    |
| 30  | Reading the wrong constraints              | O(n²) for n = 2e5                                                                         | From n, decide the target complexity first     |

Compile practice code with `g++ -std=c++17 -Wall -Wextra -Wshadow -fsanitize=address,undefined`: the sanitizers catch bugs 3, 4, 6 and 12 at the line where they happen.
