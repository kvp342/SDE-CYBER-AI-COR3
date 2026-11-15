"""OA simulation packs: 8 sets x 3 LeetCode problems. Each problem: (slug, title, diff, minutes, pattern, kb id, gist, sketch[], complexity, edges[], code, test)."""
SETS = []
def S(title, focus, date, probs): SETS.append(dict(title=title, focus=focus, date=date, probs=probs))
def Q(slug, title, diff, mins, pattern, kb, gist, sketch, cx, edges, code, test):
    return dict(slug=slug, title=title, diff=diff, mins=mins, pattern=pattern, kb=kb, gist=gist, sketch=sketch, cx=cx, edges=edges, code=code, test=test)

S("Set 1: Warm-up", "Hashing, sliding window, stack", "Sat 13 Feb 2027", [
 Q("valid-anagram", "Valid Anagram", "Easy", 10, "Hashing", "hashing", "Decide whether two strings use exactly the same letters the same number of times.",
   ["Count the 26 letters of s, subtract the letters of t, and check every count is zero.", "Return false early if the lengths differ."],
   "O(n) time, O(1) space", ["Different lengths", "Unicode input (use a hash map instead of an array)"],
   """bool isAnagram(string s, string t) {
    if (s.size() != t.size()) return false;
    int c[26] = {};
    for (int i = 0; i < (int)s.size(); i++) { c[s[i] - 'a']++; c[t[i] - 'a']--; }
    for (int x : c) if (x) return false;
    return true;
}""", """assert(isAnagram("anagram","nagaram")); assert(!isAnagram("rat","car")); assert(!isAnagram("a","ab"));"""),
 Q("find-all-anagrams-in-a-string", "Find All Anagrams in a String", "Medium", 35, "Sliding window", "sliding-window", "Return every start index in s where a rearrangement of p begins.",
   ["Keep a window of length |p| over s with letter counts.", "Add the entering letter, remove the leaving one, and record the start index whenever the window counts equal p's counts."],
   "O(26·n) time, O(1) space", ["p longer than s returns an empty list", "Overlapping answers (both must be reported)"],
   """vector<int> findAnagrams(string s, string p) {
    vector<int> r; if (p.size() > s.size()) return r;
    array<int, 26> a{}, b{}; int k = p.size();
    for (char c : p) a[c - 'a']++;
    for (int i = 0; i < (int)s.size(); i++) {
        b[s[i] - 'a']++;
        if (i >= k) b[s[i - k] - 'a']--;
        if (i >= k - 1 && a == b) r.push_back(i - k + 1);
    }
    return r;
}""", """assert((findAnagrams("cbaebabacd","abc") == vector<int>{0,6})); assert((findAnagrams("abab","ab") == vector<int>{0,1,2})); assert(findAnagrams("a","ab").empty());"""),
 Q("asteroid-collision", "Asteroid Collision", "Medium", 45, "Stack", "stack-queue", "Asteroids move right (positive) or left (negative); when they meet the smaller explodes, equal ones both explode. Return the survivors.",
   ["Scan left to right with a stack of survivors.", "Only a left-moving asteroid can hit the stack top, and only if the top moves right.", "While that holds: if the top is smaller, pop it and keep checking; if equal, pop it and the current one dies; if larger, the current one dies.", "Push the current asteroid if it survived."],
   "O(n) time, O(n) space", ["A left-mover with nothing to its left survives", "Equal sizes destroy both"],
   """vector<int> asteroidCollision(vector<int>& a) {
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
}""", """vector<int> a{5,10,-5}; assert((asteroidCollision(a) == vector<int>{5,10})); vector<int> b{8,-8}; assert(asteroidCollision(b).empty());
vector<int> c{10,2,-5}; assert((asteroidCollision(c) == vector<int>{10})); vector<int> d{-2,-1,1,2}; assert((asteroidCollision(d) == vector<int>{-2,-1,1,2}));"""),
])

S("Set 2: Counting and graphs", "Two pointers, greedy counting, BFS", "Sat 27 Feb 2027", [
 Q("move-zeroes", "Move Zeroes", "Easy", 10, "Two pointers", "two-pointers", "Move all zeros to the end in place, keeping the order of the other numbers.",
   ["Keep a write index w. Swap each non-zero a[i] into a[w] and advance w."],
   "O(n) time, O(1) space", ["All zeros or no zeros", "Must be in place"],
   """void moveZeroes(vector<int>& a) { int w = 0; for (int i = 0; i < (int)a.size(); i++) if (a[i]) swap(a[w++], a[i]); }""",
   """vector<int> a{0,1,0,3,12}; moveZeroes(a); assert((a == vector<int>{1,3,12,0,0})); vector<int> b{0}; moveZeroes(b); assert((b == vector<int>{0}));"""),
 Q("task-scheduler", "Task Scheduler", "Medium", 35, "Greedy", "greedy", "Tasks A–Z take one unit each; the same task needs n idle units between runs. Find the least total time.",
   ["Let f be the highest task frequency and k the number of tasks with that frequency.", "The most frequent tasks form f−1 blocks of length n+1, plus a final block of k tasks: (f−1)(n+1)+k.", "If there are more tasks than that, no idle time is needed: the answer is max(total tasks, (f−1)(n+1)+k)."],
   "O(N) time, O(1) space", ["n = 0 (answer is the number of tasks)", "Several tasks share the top frequency"],
   """int leastInterval(vector<char>& t, int n) {
    int c[26] = {}; for (char x : t) c[x - 'A']++;
    int f = *max_element(c, c + 26), k = count(c, c + 26, f);
    return max((int)t.size(), (f - 1) * (n + 1) + k);
}""", """vector<char> a{'A','A','A','B','B','B'}; assert(leastInterval(a,2) == 8); assert(leastInterval(a,0) == 6);
vector<char> b{'A','A','A','A','A','A','B','C','D','E','F','G'}; assert(leastInterval(b,2) == 16);"""),
 Q("word-ladder", "Word Ladder", "Hard", 45, "BFS", "bfs", "Change one letter at a time, each step a dictionary word; return the number of words in the shortest sequence from begin to end, or 0.",
   ["BFS from beginWord; each level is one more word in the sequence.", "Neighbours: change each position to every letter a–z and keep the results that are in the word set.", "Erase a word from the set when you enqueue it so it is never visited twice.", "Return the level when endWord is reached; 0 if the queue empties."],
   "O(N · L · 26) time, O(N · L) space", ["endWord not in the list returns 0", "Count words, not steps (begin counts as 1)"],
   """int ladderLength(string b, string e, vector<string>& w) {
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
}""", """vector<string> w{"hot","dot","dog","lot","log","cog"}; assert(ladderLength("hit","cog",w) == 5); vector<string> v{"hot","dot","dog","lot","log"}; assert(ladderLength("hit","cog",v) == 0);"""),
])

S("Set 3: Windows and greedy", "Fixed and variable windows, two-pass greedy", "Sat 13 Mar 2027", [
 Q("maximum-average-subarray-i", "Maximum Average Subarray I", "Easy", 10, "Sliding window", "sliding-window", "Find the largest average of any contiguous block of length k.",
   ["Sum the first k numbers, then slide: add the entering number, subtract the leaving one, keep the best sum. Divide once at the end."],
   "O(n) time, O(1) space", ["Negative numbers (start best at the first window, not 0)"],
   """double findMaxAverage(vector<int>& a, int k) {
    long long s = 0; for (int i = 0; i < k; i++) s += a[i];
    long long best = s; for (int i = k; i < (int)a.size(); i++) { s += a[i] - a[i - k]; best = max(best, s); }
    return (double)best / k;
}""", """vector<int> a{1,12,-5,-6,50,3}; assert(fabs(findMaxAverage(a,4) - 12.75) < 1e-9); vector<int> b{-1}; assert(fabs(findMaxAverage(b,1) + 1) < 1e-9);"""),
 Q("longest-repeating-character-replacement", "Longest Repeating Character Replacement", "Medium", 35, "Sliding window", "sliding-window", "With at most k letter changes, find the longest block of one repeated letter.",
   ["A window is fixable if its length minus the count of its most common letter is at most k.", "Expand right; track the highest count seen; while the window is not fixable, move left.", "The highest count never needs to go down: the answer only grows when it grows."],
   "O(n) time, O(1) space", ["k = 0", "Whole string fixable"],
   """int characterReplacement(string s, int k) {
    int c[26] = {}, mx = 0, l = 0, best = 0;
    for (int r = 0; r < (int)s.size(); r++) {
        mx = max(mx, ++c[s[r] - 'A']);
        while (r - l + 1 - mx > k) c[s[l++] - 'A']--;
        best = max(best, r - l + 1);
    }
    return best;
}""", """assert(characterReplacement("ABAB",2) == 4); assert(characterReplacement("AABABBA",1) == 4); assert(characterReplacement("AAAA",0) == 4);"""),
 Q("candy", "Candy", "Hard", 45, "Greedy", "greedy", "Each child gets at least one candy; a child rated higher than a neighbour gets more than that neighbour. Find the minimum total.",
   ["Left to right: if rating rises, give one more than the left neighbour.", "Right to left: if rating is higher than the right neighbour, take max(current, right + 1).", "Sum the array."],
   "O(n) time, O(n) space", ["Equal neighbours have no constraint", "Strictly falling ratings"],
   """int candy(vector<int>& r) {
    int n = r.size(); vector<int> c(n, 1);
    for (int i = 1; i < n; i++) if (r[i] > r[i - 1]) c[i] = c[i - 1] + 1;
    for (int i = n - 2; i >= 0; i--) if (r[i] > r[i + 1]) c[i] = max(c[i], c[i + 1] + 1);
    return accumulate(c.begin(), c.end(), 0);
}""", """vector<int> a{1,0,2}; assert(candy(a) == 5); vector<int> b{1,2,2}; assert(candy(b) == 4); vector<int> c{1,3,4,5,2}; assert(candy(c) == 11);"""),
])

S("Set 4: Stacks and binary search", "DP warm-up, stack evaluation, partition search", "Sat 24 Apr 2027", [
 Q("climbing-stairs", "Climbing Stairs", "Easy", 10, "DP", "dp", "Count the ways to climb n steps taking 1 or 2 at a time.",
   ["ways(n) = ways(n−1) + ways(n−2): the Fibonacci recurrence. Keep two variables."],
   "O(n) time, O(1) space", ["n = 1"],
   """int climbStairs(int n) { long long a = 1, b = 1; for (int i = 2; i <= n; i++) { long long c = a + b; a = b; b = c; } return b; }""",
   """assert(climbStairs(1) == 1); assert(climbStairs(2) == 2); assert(climbStairs(3) == 3); assert(climbStairs(10) == 89);"""),
 Q("evaluate-reverse-polish-notation", "Evaluate Reverse Polish Notation", "Medium", 25, "Stack", "stack-queue", "Evaluate an expression written in postfix form with + − × ÷ (division truncates toward zero).",
   ["Push numbers on a stack.", "On an operator, pop b then a (order matters for − and ÷) and push a op b.", "C++ integer division already truncates toward zero."],
   "O(n) time, O(n) space", ["Negative numbers such as \"-11\" are numbers, not operators", "Operand order for − and ÷"],
   """int evalRPN(vector<string>& t) {
    vector<long long> st;
    for (auto& x : t) {
        if (x.size() == 1 && string("+-*/").find(x) != string::npos) {
            long long b = st.back(); st.pop_back(); long long a = st.back(); st.pop_back();
            st.push_back(x == "+" ? a + b : x == "-" ? a - b : x == "*" ? a * b : a / b);
        } else st.push_back(stoll(x));
    }
    return st.back();
}""", """vector<string> a{"2","1","+","3","*"}; assert(evalRPN(a) == 9); vector<string> b{"4","13","5","/","+"}; assert(evalRPN(b) == 6);
vector<string> c{"10","6","9","3","+","-11","*","/","*","17","+","5","+"}; assert(evalRPN(c) == 22);"""),
 Q("median-of-two-sorted-arrays", "Median of Two Sorted Arrays", "Hard", 55, "Binary search", "binary-search", "Find the median of two sorted arrays in logarithmic time.",
   ["Binary search a cut i in the smaller array A; the cut in B is j = (m+n+1)/2 − i, so the left halves together hold half the elements.", "The cut is right when A[i−1] ≤ B[j] and B[j−1] ≤ A[i] (use ±infinity past the ends).", "If A[i−1] > B[j] move left, else move right.", "Median: max of the left sides (odd total), or its average with the min of the right sides (even total)."],
   "O(log min(m, n)) time, O(1) space", ["One array empty", "All of A smaller than all of B"],
   """double findMedianSortedArrays(vector<int>& A, vector<int>& B) {
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
}""", """vector<int> a{1,3}, b{2}; assert(findMedianSortedArrays(a,b) == 2.0); vector<int> c{1,2}, d{3,4}; assert(findMedianSortedArrays(c,d) == 2.5);
vector<int> e{}, f{1}; assert(findMedianSortedArrays(e,f) == 1.0); vector<int> g{1,2,3}, h{4,5,6,7}; assert(findMedianSortedArrays(g,h) == 4.0);"""),
])

S("Set 5: Simulation and shortest paths", "Cycle detection, sorting, Dijkstra on a grid", "Sat 8 May 2027", [
 Q("happy-number", "Happy Number", "Easy", 15, "Linked list", "linked-list", "Repeatedly replace a number by the sum of the squares of its digits; is 1 reached?",
   ["The sequence either reaches 1 or loops. Use Floyd's slow and fast pointers on the sequence (or a set of seen values)."],
   "O(log n) per step; few steps in practice", ["n = 1 is happy"],
   """int nxt(int n) { int s = 0; while (n) { s += (n % 10) * (n % 10); n /= 10; } return s; }
bool isHappy(int n) { int s = n, f = nxt(n); while (f != 1 && s != f) { s = nxt(s); f = nxt(nxt(f)); } return f == 1; }""",
   """assert(isHappy(19)); assert(!isHappy(2)); assert(isHappy(1)); assert(isHappy(7));"""),
 Q("car-fleet", "Car Fleet", "Medium", 30, "Stack", "monotonic-stack", "Cars drive toward a target and cannot pass; a faster car that catches up joins the slower one as a fleet. How many fleets arrive?",
   ["Sort cars by position, closest to the target first.", "Compute each car's arrival time (target − position) / speed.", "A car that would arrive later than the fleet ahead of it starts a new fleet; otherwise it joins that fleet. Count new fleets."],
   "O(n log n) time, O(n) space", ["Equal arrival times merge", "Use floating point or compare by cross-multiplication"],
   """int carFleet(int target, vector<int>& pos, vector<int>& sp) {
    int n = pos.size(); vector<pair<int, double>> c(n);
    for (int i = 0; i < n; i++) c[i] = {pos[i], (double)(target - pos[i]) / sp[i]};
    sort(c.rbegin(), c.rend());
    int fleets = 0; double cur = 0;
    for (auto& [p, t] : c) if (t > cur) { fleets++; cur = t; }
    return fleets;
}""", """vector<int> p{10,8,0,5,3}, s{2,4,1,1,3}; assert(carFleet(12,p,s) == 3); vector<int> p2{3}, s2{3}; assert(carFleet(10,p2,s2) == 1); vector<int> p3{0,2,4}, s3{4,2,1}; assert(carFleet(100,p3,s3) == 1);"""),
 Q("swim-in-rising-water", "Swim in Rising Water", "Hard", 45, "Shortest paths", "dijkstra", "In an n × n grid of heights, at time t you can stand on cells of height ≤ t. Find the earliest time to go from top-left to bottom-right.",
   ["The cost of a path is its highest cell. Run Dijkstra where the distance is the max height along the path.", "Pop the cell with the smallest current max; push neighbours with max(current, their height).", "The first time the target is popped, its value is the answer."],
   "O(n² log n) time, O(n²) space", ["Start cell height counts", "Binary search on t plus BFS also works"],
   """int swimInWater(vector<vector<int>>& g) {
    int n = g.size(); vector<vector<int>> seen(n, vector<int>(n));
    priority_queue<array<int, 3>, vector<array<int, 3>>, greater<>> pq; pq.push({g[0][0], 0, 0}); int d[] = {1, 0, -1, 0, 1};
    while (true) {
        auto [t, r, c] = pq.top(); pq.pop();
        if (r == n - 1 && c == n - 1) return t;
        if (seen[r][c]++) continue;
        for (int k = 0; k < 4; k++) { int x = r + d[k], y = c + d[k + 1]; if (x >= 0 && y >= 0 && x < n && y < n && !seen[x][y]) pq.push({max(t, g[x][y]), x, y}); }
    }
}""", """vector<vector<int>> a{{0,2},{1,3}}; assert(swimInWater(a) == 3);
vector<vector<int>> b{{0,1,2,3,4},{24,23,22,21,5},{12,13,14,15,16},{11,17,18,19,20},{10,9,8,7,6}}; assert(swimInWater(b) == 16); vector<vector<int>> c{{0}}; assert(swimInWater(c) == 0);"""),
])

S("Set 6: Mediums under pressure", "Binary search on a window, union-find, interval DP", "Sat 22 May 2027", [
 Q("find-k-closest-elements", "Find K Closest Elements", "Medium", 25, "Binary search", "binary-search", "From a sorted array, return the k values closest to x in ascending order (ties go to the smaller value).",
   ["The answer is a block a[lo..lo+k). Binary search lo in [0, n−k].", "Compare x − a[mid] with a[mid+k] − x: if the left end is farther, the block must start after mid; otherwise at or before mid."],
   "O(log(n − k) + k) time", ["x outside the array range", "Ties prefer the smaller value"],
   """vector<int> findClosestElements(vector<int>& a, int k, int x) {
    int lo = 0, hi = a.size() - k;
    while (lo < hi) { int mid = (lo + hi) / 2; if (x - a[mid] > a[mid + k] - x) lo = mid + 1; else hi = mid; }
    return vector<int>(a.begin() + lo, a.begin() + lo + k);
}""", """vector<int> a{1,2,3,4,5}; assert((findClosestElements(a,4,3) == vector<int>{1,2,3,4})); assert((findClosestElements(a,4,-1) == vector<int>{1,2,3,4}));
vector<int> b{1,1,2,3,4,5}; assert((findClosestElements(b,4,6) == vector<int>{2,3,4,5}));"""),
 Q("accounts-merge", "Accounts Merge", "Medium", 35, "Union-find", "dsu", "Accounts that share any email belong to the same person; merge them and output each person's sorted emails.",
   ["Give every email an id. Union all emails inside each account with its first email.", "Group emails by their root, remember a name per email, sort each group and put the name first."],
   "O(E log E) time for the sorting, near-linear for the unions", ["Same name does not mean same person", "An account with a single email"],
   """struct DSU { vector<int> p; int f(int x) { return p[x] == x ? x : p[x] = f(p[x]); } void u(int a, int b) { p[f(a)] = f(b); } };
vector<vector<string>> accountsMerge(vector<vector<string>>& acc) {
    unordered_map<string, int> id; unordered_map<string, string> name; DSU d;
    for (auto& a : acc) for (int i = 1; i < (int)a.size(); i++) { if (!id.count(a[i])) { id[a[i]] = d.p.size(); d.p.push_back(d.p.size()); } name[a[i]] = a[0]; d.u(id[a[i]], id[a[1]]); }
    map<int, vector<string>> g; for (auto& [e, i] : id) g[d.f(i)].push_back(e);
    vector<vector<string>> r;
    for (auto& [root, v] : g) { sort(v.begin(), v.end()); v.insert(v.begin(), name[v[0]]); r.push_back(v); }
    return r;
}""", """vector<vector<string>> a{{"John","js@m.com","jn@m.com"},{"John","js@m.com","j00@m.com"},{"Mary","mary@m.com"},{"John","jb@m.com"}};
auto r = accountsMerge(a); sort(r.begin(), r.end()); assert(r.size() == 3);
assert((r[0] == vector<string>{"John","j00@m.com","jn@m.com","js@m.com"})); assert((r[1] == vector<string>{"John","jb@m.com"})); assert((r[2] == vector<string>{"Mary","mary@m.com"}));"""),
 Q("burst-balloons", "Burst Balloons", "Hard", 30, "DP", "dp", "Bursting balloon i earns left × i × right of its current neighbours. Find the maximum total.",
   ["Pad the array with 1 at both ends.", "Think of the last balloon k burst in the open interval (l, r): its neighbours are then l and r.", "dp[l][r] = max over l < k < r of dp[l][k] + dp[k][r] + a[l]·a[k]·a[r]. Fill by increasing interval length."],
   "O(n³) time, O(n²) space", ["Choosing the first balloon to burst does not split the problem; the last one does"],
   """int maxCoins(vector<int>& v) {
    vector<int> a{1}; a.insert(a.end(), v.begin(), v.end()); a.push_back(1); int n = a.size();
    vector<vector<int>> dp(n, vector<int>(n, 0));
    for (int len = 2; len < n; len++) for (int l = 0; l + len < n; l++) { int r = l + len;
        for (int k = l + 1; k < r; k++) dp[l][r] = max(dp[l][r], dp[l][k] + dp[k][r] + a[l] * a[k] * a[r]); }
    return dp[0][n - 1];
}""", """vector<int> a{3,1,5,8}; assert(maxCoins(a) == 167); vector<int> b{1,5}; assert(maxCoins(b) == 10);"""),
])

S("Set 7: Arrays and answer search", "In-place tricks, interval greedy, binary search on the answer", "Sat 12 Jun 2027", [
 Q("rotate-array", "Rotate Array", "Medium", 20, "Two pointers", "two-pointers", "Rotate an array to the right by k steps in place.",
   ["k %= n. Reverse the whole array, then reverse the first k elements, then the rest."],
   "O(n) time, O(1) space", ["k larger than n", "k = 0"],
   """void rotate(vector<int>& a, int k) { k %= a.size(); reverse(a.begin(), a.end()); reverse(a.begin(), a.begin() + k); reverse(a.begin() + k, a.end()); }""",
   """vector<int> a{1,2,3,4,5,6,7}; rotate(a,3); assert((a == vector<int>{5,6,7,1,2,3,4})); vector<int> b{-1,-100,3,99}; rotate(b,6); assert((b == vector<int>{3,99,-1,-100}));"""),
 Q("minimum-number-of-arrows-to-burst-balloons", "Minimum Number of Arrows to Burst Balloons", "Medium", 30, "Intervals", "intervals", "Balloons are intervals on a line; a vertical arrow at x bursts every balloon covering x. Find the fewest arrows.",
   ["Sort by end. Shoot the first arrow at the first end.", "A balloon starting after the current arrow position needs a new arrow at its end; touching counts as burst."],
   "O(n log n) time", ["Touching intervals share an arrow (use >, not ≥)", "Large coordinates: compare, do not subtract"],
   """int findMinArrowShots(vector<vector<int>>& p) {
    sort(p.begin(), p.end(), [](auto& a, auto& b) { return a[1] < b[1]; });
    int arrows = 1; long long x = p[0][1];
    for (auto& b : p) if (b[0] > x) { arrows++; x = b[1]; }
    return arrows;
}""", """vector<vector<int>> a{{10,16},{2,8},{1,6},{7,12}}; assert(findMinArrowShots(a) == 2); vector<vector<int>> b{{1,2},{3,4},{5,6},{7,8}}; assert(findMinArrowShots(b) == 4);
vector<vector<int>> c{{1,2},{2,3},{3,4},{4,5}}; assert(findMinArrowShots(c) == 2);"""),
 Q("split-array-largest-sum", "Split Array Largest Sum", "Hard", 40, "Binary search", "binary-search", "Split the array into k non-empty contiguous parts so the largest part sum is as small as possible.",
   ["Binary search the answer S between max(a) and sum(a).", "Check S greedily: fill parts left to right, starting a new part when adding the next number would exceed S. S works if at most k parts are needed.", "Find the smallest S that works."],
   "O(n log(sum)) time, O(1) space", ["Low bound must be max(a), not 0", "Use long long for sums"],
   """int splitArray(vector<int>& a, int k) {
    long long lo = *max_element(a.begin(), a.end()), hi = accumulate(a.begin(), a.end(), 0LL);
    while (lo < hi) {
        long long mid = (lo + hi) / 2, cur = 0; int parts = 1;
        for (int x : a) { if (cur + x > mid) { parts++; cur = 0; } cur += x; }
        if (parts <= k) hi = mid; else lo = mid + 1;
    }
    return lo;
}""", """vector<int> a{7,2,5,10,8}; assert(splitArray(a,2) == 18); vector<int> b{1,2,3,4,5}; assert(splitArray(b,2) == 9); vector<int> c{1,4,4}; assert(splitArray(c,3) == 4);"""),
])

S("Set 8: Final dress rehearsal", "Counting, DP with counts, string DP", "Sat 3 Jul 2027", [
 Q("first-unique-character-in-a-string", "First Unique Character in a String", "Easy", 10, "Hashing", "hashing", "Return the index of the first letter that appears exactly once, or −1.",
   ["Count letters in one pass; return the first index whose count is 1 in a second pass."],
   "O(n) time, O(1) space", ["No unique letter returns −1"],
   """int firstUniqChar(string s) { int c[26] = {}; for (char x : s) c[x - 'a']++; for (int i = 0; i < (int)s.size(); i++) if (c[s[i] - 'a'] == 1) return i; return -1; }""",
   """assert(firstUniqChar("leetcode") == 0); assert(firstUniqChar("loveleetcode") == 2); assert(firstUniqChar("aabb") == -1);"""),
 Q("number-of-longest-increasing-subsequence", "Number of Longest Increasing Subsequence", "Medium", 35, "DP", "dp", "Count how many strictly increasing subsequences have the maximum length.",
   ["len[i] = longest increasing subsequence ending at i; cnt[i] = how many of that length.", "For each j < i with a[j] < a[i]: a longer length from j resets cnt[i] to cnt[j]; an equal length adds cnt[j].", "Sum cnt[i] over all i with len[i] equal to the maximum."],
   "O(n²) time, O(n) space", ["All equal values (every single element counts)", "Reset, do not add, when a longer length appears"],
   """int findNumberOfLIS(vector<int>& a) {
    int n = a.size(), best = 0, ans = 0; vector<int> len(n, 1), cnt(n, 1);
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < i; j++) if (a[j] < a[i]) {
            if (len[j] + 1 > len[i]) { len[i] = len[j] + 1; cnt[i] = cnt[j]; }
            else if (len[j] + 1 == len[i]) cnt[i] += cnt[j];
        }
        if (len[i] > best) { best = len[i]; ans = cnt[i]; } else if (len[i] == best) ans += cnt[i];
    }
    return ans;
}""", """vector<int> a{1,3,5,4,7}; assert(findNumberOfLIS(a) == 2); vector<int> b{2,2,2,2,2}; assert(findNumberOfLIS(b) == 5); vector<int> c{1,2,4,3,5,4,7,2}; assert(findNumberOfLIS(c) == 3);"""),
 Q("regular-expression-matching", "Regular Expression Matching", "Hard", 45, "DP", "dp", "Match a whole string against a pattern with '.' (any letter) and '*' (zero or more of the previous element).",
   ["dp[i][j] = does s[i..] match p[j..]? dp[n][m] = true.", "first = i < n and (p[j] == s[i] or p[j] == '.').", "If p[j+1] is '*': dp[i][j] = dp[i][j+2] (use zero copies) or (first and dp[i+1][j]) (use one more).", "Otherwise dp[i][j] = first and dp[i+1][j+1]. Fill from the back."],
   "O(nm) time and space", ["'a*' can match the empty string", "The match must cover the whole string"],
   """bool isMatch(string s, string p) {
    int n = s.size(), m = p.size(); vector<vector<bool>> dp(n + 1, vector<bool>(m + 1, false)); dp[n][m] = true;
    for (int i = n; i >= 0; i--) for (int j = m - 1; j >= 0; j--) {
        bool first = i < n && (p[j] == s[i] || p[j] == '.');
        if (j + 1 < m && p[j + 1] == '*') dp[i][j] = dp[i][j + 2] || (first && dp[i + 1][j]);
        else dp[i][j] = first && dp[i + 1][j + 1];
    }
    return dp[0][0];
}""", """assert(!isMatch("aa","a")); assert(isMatch("aa","a*")); assert(isMatch("ab",".*")); assert(isMatch("aab","c*a*b")); assert(!isMatch("mississippi","mis*is*p*."));"""),
])
