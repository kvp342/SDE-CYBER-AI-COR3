"""Worked Solutions III: 40 more most-asked problems, none repeated from Worked Solutions I/II or the OA packs.
Same fields as t_probs2.py; every `code` is tested by `test` (see test_probs3.py)."""
LC = lambda slug: f"https://leetcode.com/problems/{slug}/"
REL = {"Two pointers": "two-pointers", "Sliding window": "sliding-window", "Binary search": "binary-search", "Hashing": "hashing",
       "Stack": "stack-queue", "Monotonic stack": "monotonic-stack", "Linked list": "linked-list", "Trees": "trees", "BST": "bst", "BFS": "bfs",
       "DFS": "dfs", "Topological sort": "topo-sort", "Shortest paths": "dijkstra", "Union-Find": "dsu", "MST": "dsu", "Heap": "heap", "DP": "dp",
       "String DP": "lcs", "Backtracking": "recursion", "Greedy": "greedy", "Intervals": "intervals"}
P = []
def add(id, title, slug, lvl, pattern, where, idea, steps, code, test, cx, traps, follow):
    P.append(dict(id="p3-" + id, title=title, slug=slug, cat="Problems", lvl={0: 1, 1: 2, 3: 3}[lvl], aka=[title], why=f"Pattern: {pattern}. {where}",
                  core=idea, points=steps + [f"Complexity: {cx}"], code=code, test=test, pit=traps, ask=follow,
                  prac=[(f"Solve it on LeetCode: {title}", LC(slug))], learn=[], rel=[REL[pattern]]))

# ---------------- Hashing ----------------
add("valid-sudoku", "Valid Sudoku", "valid-sudoku", 1, "Hashing", "A quick check of 2D indexing and sets.",
 ["Each filled digit must be unique in its row, its column and its 3×3 box. Box index = (r / 3) * 3 + c / 3. Keep a seen-flag per (row, digit), (column, digit) and (box, digit)."],
 ["Skip '.' cells", "Compute d = ch - '1' and the box index", "If any of the three flags is set, return false; otherwise set all three"],
 """class Solution {
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
};""",
 """vector<string> s{"53..7....","6..195...",".98....6.","8...6...3","4..8.3..1","7...2...6",".6....28.","...419..5","....8..79"};
vector<vector<char>> b; for (auto& x : s) b.push_back(vector<char>(x.begin(), x.end()));
assert(Solution().isValidSudoku(b)); b[0][0] = '8'; assert(!Solution().isValidSudoku(b));""",
 "O(81) = O(1) time and space", ["Wrong box formula (r / 3 + c / 3 collides)", "Checking that the board is solvable: the problem only asks about filled cells"],
 ["Solve the board (see Sudoku Solver).", "Use one 9-bit mask per row, column and box instead of bool arrays."])

add("k-closest-points", "K Closest Points to Origin", "k-closest-points-to-origin", 1, "Heap", "Top-k with a heap.",
 ["Keep a max-heap of size k keyed by squared distance. When it grows past k, pop the farthest. What remains are the k closest."],
 ["Use x*x + y*y (no square root needed)", "Push each point; pop when size > k", "Empty the heap into the answer"],
 """class Solution {
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
};""",
 """vector<vector<int>> p{{3,3},{5,-1},{-2,4}}; auto r = Solution().kClosest(p, 2); sort(r.begin(), r.end());
assert((r == vector<vector<int>>{{-2,4},{3,3}}));""",
 "O(n log k) time, O(k) space", ["Using a min-heap of all n points (O(n log n), fine but not what they want)", "int overflow in x*x + y*y for large coordinates"],
 ["O(n) average with quickselect (nth_element).", "Points arrive as a stream: the size-k heap still works."])

# ---------------- Two pointers ----------------
add("4sum", "4Sum", "4sum", 1, "Two pointers", "Extends 3Sum; tests duplicate handling.",
 ["Sort. Fix two indices i < j with duplicate skipping, then run two pointers on the rest for target − a[i] − a[j]. Use long long sums: values reach 1e9."],
 ["Sort", "Loop i, skip equal neighbours; loop j > i, skip equal neighbours", "Two pointers l, r; on a match record it and skip duplicates on both sides"],
 """class Solution {
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
};""",
 """vector<int> a{1,0,-1,0,-2,2}; auto r = Solution().fourSum(a, 0);
assert((r == vector<vector<int>>{{-2,-1,1,2},{-2,0,0,2},{-1,0,0,1}}));
vector<int> b{2,2,2,2,2}; assert(Solution().fourSum(b, 8).size() == 1);
vector<int> c{1000000000,1000000000,1000000000,1000000000}; assert(Solution().fourSum(c, -294967296).empty());""",
 "O(n³) time, O(1) extra space", ["int overflow of the four-number sum", "Skipping duplicates of j with j > 0 instead of j > i + 1"],
 ["Generalise to kSum with recursion down to the 2-pointer base case."])

# ---------------- Sliding window ----------------
add("fruit-baskets", "Fruit Into Baskets", "fruit-into-baskets", 1, "Sliding window", "Longest window with at most 2 distinct values.",
 ["Grow the right end; keep counts in a map. While the map has more than 2 keys, shrink from the left. The answer is the largest window seen."],
 ["cnt[f[r]]++", "While cnt.size() > 2: decrement cnt[f[l]], erase at 0, l++", "best = max(best, r - l + 1)"],
 """class Solution {
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
};""",
 """vector<int> a{1,2,1}, b{0,1,2,2}, c{1,2,3,2,2}, d{3,3,3,1,2,1,1,2,3,3,4};
assert(Solution().totalFruit(a) == 3 && Solution().totalFruit(b) == 3 && Solution().totalFruit(c) == 4 && Solution().totalFruit(d) == 5);""",
 "O(n) time, O(1) space (map holds at most 3 keys)", ["Forgetting to erase keys at count 0, so size() never drops"],
 ["At most k distinct values: same code with k instead of 2."])

add("max-ones-iii", "Max Consecutive Ones III", "max-consecutive-ones-iii", 1, "Sliding window", "Longest window with at most k zeros.",
 ["A window is valid if it holds at most k zeros (flip them). Expand right; when zeros exceed k, move left past a zero."],
 ["zeros += (a[r] == 0)", "While zeros > k: zeros -= (a[l] == 0), l++", "best = max(best, r - l + 1)"],
 """class Solution {
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
};""",
 """vector<int> a{1,1,1,0,0,0,1,1,1,1,0}, b{0,0,1,1,0,0,1,1,1,0,1,1,0,0,0,1,1,1,1};
assert(Solution().longestOnes(a, 2) == 6 && Solution().longestOnes(b, 3) == 10);""",
 "O(n) time, O(1) space", ["Trying to actually flip values in the array"],
 ["Longest Repeating Character Replacement uses the same idea with 'window − max frequency ≤ k'."])

# ---------------- Binary search ----------------
add("min-rotated", "Find Minimum in Rotated Sorted Array", "find-minimum-in-rotated-sorted-array", 1, "Binary search", "Binary search on a property, not a value.",
 ["Compare the middle with the right end. If a[m] > a[r], the minimum is to the right of m; otherwise it is at m or to its left."],
 ["l = 0, r = n - 1; while l < r", "m = l + (r - l) / 2", "a[m] > a[r] ? l = m + 1 : r = m", "Return a[l]"],
 """class Solution {
public:
    int findMin(vector<int>& a) {
        int l = 0, r = a.size() - 1;
        while (l < r) {
            int m = l + (r - l) / 2;
            if (a[m] > a[r]) l = m + 1; else r = m;
        }
        return a[l];
    }
};""",
 """vector<int> a{3,4,5,1,2}, b{4,5,6,7,0,1,2}, c{11,13,15,17}, d{2,1};
assert(Solution().findMin(a) == 1 && Solution().findMin(b) == 0 && Solution().findMin(c) == 11 && Solution().findMin(d) == 1);""",
 "O(log n) time, O(1) space", ["Comparing with a[l] instead of a[r] (fails when the array is not rotated)", "Using r = m - 1, which can skip the minimum"],
 ["With duplicates (II): when a[m] == a[r], do r-- (worst case O(n))."])

add("first-last-pos", "Find First and Last Position of Element in Sorted Array", "find-first-and-last-position-of-element-in-sorted-array", 1, "Binary search", "lower_bound and upper_bound.",
 ["The first position is the first index with a[i] ≥ t (lower bound). The last is one before the first index with a[i] > t (upper bound). If the lower bound is not t, return [-1, -1]."],
 ["lo = lower_bound(t)", "If lo == n or a[lo] != t: return {-1,-1}", "hi = upper_bound(t) - 1"],
 """class Solution {
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
};""",
 """vector<int> a{5,7,7,8,8,10}, e{};
assert((Solution().searchRange(a, 8) == vector<int>{3,4}) && (Solution().searchRange(a, 6) == vector<int>{-1,-1}) && (Solution().searchRange(e, 0) == vector<int>{-1,-1}));""",
 "O(log n) time, O(1) space", ["Finding one match then scanning outwards (O(n) on all-equal arrays)"],
 ["Count occurrences of t: upper − lower.", "In C++ you can use std::lower_bound / std::upper_bound directly."])

add("ship-capacity", "Capacity To Ship Packages Within D Days", "capacity-to-ship-packages-within-d-days", 1, "Binary search", "Binary search on the answer.",
 ["If capacity c works, every larger c works. So binary search c between max(w) and sum(w); check feasibility greedily by filling each day until the next package does not fit."],
 ["lo = max weight, hi = total weight", "days(c): count days by greedy filling", "If days(c) ≤ D: hi = c else lo = c + 1"],
 """class Solution {
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
};""",
 """vector<int> a{1,2,3,4,5,6,7,8,9,10}, b{3,2,2,4,1,4}, c{1,2,3,1,1};
assert(Solution().shipWithinDays(a, 5) == 15 && Solution().shipWithinDays(b, 3) == 6 && Solution().shipWithinDays(c, 4) == 3);""",
 "O(n log(sum)) time, O(1) space", ["Starting lo at 1 (a package heavier than c can never ship)"],
 ["Same shape: Koko Eating Bananas, Split Array Largest Sum, Minimum Days to Make Bouquets."])

add("time-map", "Time Based Key-Value Store", "time-based-key-value-store", 1, "Binary search", "Design question with binary search inside.",
 ["Timestamps for each key arrive in increasing order, so append (time, value) to a vector per key. get(key, t) is the last entry with time ≤ t: upper_bound on t, then step back one."],
 ["set: m[key].push_back({t, v})", "get: it = upper_bound by time; if it is begin, return \"\"", "Return prev(it)->second"],
 """class TimeMap {
    unordered_map<string, vector<pair<int, string>>> m;
public:
    void set(string k, string v, int t) { m[k].push_back({t, v}); }
    string get(string k, int t) {
        auto f = m.find(k); if (f == m.end()) return "";
        auto& v = f->second;
        auto it = upper_bound(v.begin(), v.end(), t, [](int x, const pair<int, string>& p) { return x < p.first; });
        return it == v.begin() ? "" : prev(it)->second;
    }
};""",
 """TimeMap tm; tm.set("foo", "bar", 1); assert(tm.get("foo", 1) == "bar" && tm.get("foo", 3) == "bar");
tm.set("foo", "bar2", 4); assert(tm.get("foo", 4) == "bar2" && tm.get("foo", 5) == "bar2" && tm.get("foo", 0) == "" && tm.get("x", 1) == "");""",
 "set O(1), get O(log n)", ["Using m[k] in get (inserts empty keys)", "lower_bound returns the first time ≥ t, not the last ≤ t"],
 ["What if timestamps are not increasing? Use map<int,string> per key and upper_bound."])

# ---------------- Stack / monotonic stack ----------------
add("min-stack", "Min Stack", "min-stack", 1, "Stack", "Design: O(1) getMin.",
 ["Store, with every pushed value, the minimum of the stack at that point. Then top, pop and getMin are all O(1)."],
 ["push(x): s.push({x, min(x, current min)})", "pop: s.pop()", "getMin: s.top().second"],
 """class MinStack {
    stack<pair<int, int>> s;                      // (value, min so far)
public:
    void push(int x) { s.push({x, s.empty() ? x : min(x, s.top().second)}); }
    void pop() { s.pop(); }
    int top() { return s.top().first; }
    int getMin() { return s.top().second; }
};""",
 """MinStack m; m.push(-2); m.push(0); m.push(-3); assert(m.getMin() == -3); m.pop(); assert(m.top() == 0 && m.getMin() == -2);""",
 "O(1) per operation, O(n) space", ["Keeping one global min variable (wrong after popping the min)"],
 ["Use O(1) extra space by storing differences from the min (watch overflow).", "Max stack with popMax (needs a balanced tree or lazy deletion)."])

add("next-greater-ii", "Next Greater Element II", "next-greater-element-ii", 1, "Monotonic stack", "Circular array trick.",
 ["Walk the array twice (i from 0 to 2n − 1, index i % n) with a stack of indices whose answer is unknown. While the current value beats the value on top, that index's answer is the current value."],
 ["ans filled with -1", "For i in 0..2n-1: x = a[i % n]; pop while a[top] < x, set ans[top] = x", "Push i only in the first pass"],
 """class Solution {
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
};""",
 """vector<int> a{1,2,1}, b{1,2,3,4,3};
assert((Solution().nextGreaterElements(a) == vector<int>{2,-1,2}) && (Solution().nextGreaterElements(b) == vector<int>{2,3,4,-1,4}));""",
 "O(n) time, O(n) space", ["Using ≤ in the pop condition (equal values are not greater)"],
 ["Daily Temperatures is the same idea returning distances."])

add("basic-calc-ii", "Basic Calculator II", "basic-calculator-ii", 1, "Stack", "Expression parsing without parentheses.",
 ["Read numbers left to right, remembering the operator before each. For + and − push ±num; for * and / apply it to the top of the stack at once (higher precedence). The answer is the sum of the stack."],
 ["Build num digit by digit", "At an operator or the end: apply the previous operator, then remember this one and reset num", "Sum the stack"],
 """class Solution {
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
};""",
 """assert(Solution().calculate("3+2*2") == 7 && Solution().calculate(" 3/2 ") == 1 && Solution().calculate(" 3+5 / 2 ") == 5 && Solution().calculate("14-3/2") == 13);""",
 "O(n) time, O(n) space (O(1) possible)", ["Treating spaces as operators", "Forgetting the last number (the sentinel at the end handles it)"],
 ["Add parentheses (Basic Calculator I/III): recurse or push the state on '('.", "Do it in O(1) space by keeping only the last term."])

add("remove-k-digits", "Remove K Digits", "remove-k-digits", 1, "Monotonic stack", "Greedy with an increasing stack.",
 ["To make the number smallest, a digit should be removed when the next digit is smaller. Keep an increasing stack: pop while k > 0 and the top is bigger than the current digit. Remove leftover k from the end, strip leading zeros."],
 ["For each digit: pop while k and top > d (k--); push d", "Pop k more from the end", "Strip leading zeros; empty means \"0\""],
 """class Solution {
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
};""",
 """assert(Solution().removeKdigits("1432219", 3) == "1219" && Solution().removeKdigits("10200", 1) == "200" && Solution().removeKdigits("10", 2) == "0" && Solution().removeKdigits("112", 1) == "11");""",
 "O(n) time, O(n) space", ["Forgetting the leftover k for an increasing string", "Returning an empty string instead of \"0\""],
 ["Largest number by removing k digits: reverse the comparison."])

# ---------------- Linked list ----------------
add("add-two-numbers", "Add Two Numbers", "add-two-numbers", 1, "Linked list", "Digit-by-digit addition with a carry.",
 ["Digits are stored in reverse, so add node by node from the head with a carry, appending to a dummy list. Continue while either list or the carry remains."],
 ["Dummy head, tail pointer, carry = 0", "sum = carry + (l1 ? l1->val : 0) + (l2 ? l2->val : 0)", "Append sum % 10; carry = sum / 10"],
 """class Solution {
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
};""",
 """assert((tov(Solution().addTwoNumbers(mk({2,4,3}), mk({5,6,4}))) == vector<int>{7,0,8}));
assert((tov(Solution().addTwoNumbers(mk({9,9,9,9}), mk({9,9}))) == vector<int>{8,9,0,0,1}));""",
 "O(max(m, n)) time, O(1) extra space besides the output", ["Dropping the final carry"],
 ["Digits in forward order (II): use two stacks or reverse both lists first."])

add("reorder-list", "Reorder List", "reorder-list", 1, "Linked list", "Combines three basic list moves.",
 ["L0 → Ln → L1 → Ln−1 …: find the middle (slow/fast), reverse the second half, then merge the two halves alternately."],
 ["Slow/fast to the middle; cut after slow", "Reverse the second half", "Weave: a->next = b, b->next = old a->next"],
 """class Solution {
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
};""",
 """ListNode* a = mk({1,2,3,4}); Solution().reorderList(a); assert((tov(a) == vector<int>{1,4,2,3}));
ListNode* b = mk({1,2,3,4,5}); Solution().reorderList(b); assert((tov(b) == vector<int>{1,5,2,4,3}));""",
 "O(n) time, O(1) space", ["Not cutting the first half (creates a cycle)"],
 ["Could you do it with a deque? (Yes, O(n) extra space.)"])

add("sort-list", "Sort List", "sort-list", 1, "Linked list", "Merge sort on a list.",
 ["Merge sort fits lists: split at the middle with slow/fast pointers, sort each half, merge two sorted lists. No random access needed."],
 ["Base case: 0 or 1 node", "Split with slow/fast (fast starts at head->next so two nodes split)", "Merge the sorted halves with a dummy head"],
 """class Solution {
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
};""",
 """assert((tov(Solution().sortList(mk({4,2,1,3}))) == vector<int>{1,2,3,4}) && (tov(Solution().sortList(mk({-1,5,3,4,0}))) == vector<int>{-1,0,3,4,5}) && tov(Solution().sortList(nullptr)).empty());""",
 "O(n log n) time, O(log n) stack space", ["Starting fast at head for two nodes: the split never shrinks (infinite recursion)"],
 ["O(1) space: bottom-up merge sort with sizes 1, 2, 4, …"])

add("palindrome-list", "Palindrome Linked List", "palindrome-linked-list", 0, "Linked list", "Middle + reverse.",
 ["Find the middle, reverse the second half, then compare the first half with the reversed half node by node."],
 ["Slow/fast to the middle", "Reverse from slow", "Compare until the reversed half ends"],
 """class Solution {
public:
    bool isPalindrome(ListNode* h) {
        ListNode *s = h, *f = h;
        while (f && f->next) { s = s->next; f = f->next->next; }
        ListNode* prev = nullptr;
        while (s) { ListNode* n = s->next; s->next = prev; prev = s; s = n; }
        for (ListNode* a = h; prev; a = a->next, prev = prev->next) if (a->val != prev->val) return false;
        return true;
    }
};""",
 """assert(Solution().isPalindrome(mk({1,2,2,1})) && !Solution().isPalindrome(mk({1,2})) && Solution().isPalindrome(mk({1,2,3,2,1})) && Solution().isPalindrome(mk({1})));""",
 "O(n) time, O(1) space", ["The list is left modified: mention restoring it if the interviewer cares"],
 ["Restore the list after checking (reverse the second half again)."])

# ---------------- Trees ----------------
add("path-sum-iii", "Path Sum III", "path-sum-iii", 1, "Trees", "Prefix sums on a root-to-node path.",
 ["Count downward paths summing to t. Along the current root-to-node path, keep counts of prefix sums. At a node with running sum s, paths ending here = count[s − t]. Add s before going down, remove it when coming back."],
 ["cnt[0] = 1", "dfs(node, s): s += val; ans += cnt[s - t]; cnt[s]++; recurse; cnt[s]--", "Use long long sums"],
 """class Solution {
    unordered_map<long long, int> cnt; int ans = 0, t = 0;
    void dfs(TreeNode* n, long long s) {
        if (!n) return;
        s += n->val;
        auto it = cnt.find(s - t); if (it != cnt.end()) ans += it->second;
        cnt[s]++; dfs(n->left, s); dfs(n->right, s); cnt[s]--;
    }
public:
    int pathSum(TreeNode* root, int target) { t = target; cnt[0] = 1; dfs(root, 0); return ans; }
};""",
 """assert(Solution().pathSum(tree({"10","5","-3","3","2","null","11","3","-2","null","1"}), 8) == 3);
assert(Solution().pathSum(tree({"5","4","8","11","null","13","4","7","2","null","null","5","1"}), 22) == 3);""",
 "O(n) time, O(h) space for the path (map entries)", ["Forgetting to undo cnt[s]++ (sibling subtrees then share prefixes)", "int overflow"],
 ["Path Sum II: return the paths from root to leaf with sum t (backtracking)."])

add("flatten-tree", "Flatten Binary Tree to Linked List", "flatten-binary-tree-to-linked-list", 1, "Trees", "In-place pointer rewiring.",
 ["Morris-style: at each node with a left child, find the rightmost node of the left subtree, attach the current right subtree there, move the left subtree to the right, clear left. Move right."],
 ["cur = root; while cur", "If cur->left: p = rightmost of cur->left; p->right = cur->right; cur->right = cur->left; cur->left = null", "cur = cur->right"],
 """class Solution {
public:
    void flatten(TreeNode* root) {
        for (TreeNode* cur = root; cur; cur = cur->right)
            if (cur->left) {
                TreeNode* p = cur->left;
                while (p->right) p = p->right;
                p->right = cur->right; cur->right = cur->left; cur->left = nullptr;
            }
    }
};""",
 """TreeNode* r = tree({"1","2","5","3","4","null","6"}); Solution().flatten(r); vector<int> v;
for (TreeNode* c = r; c; c = c->right) { assert(!c->left); v.push_back(c->val); } assert((v == vector<int>{1,2,3,4,5,6}));""",
 "O(n) time, O(1) space", ["Leaving left pointers set"],
 ["Recursive version with a 'prev' pointer in reverse preorder (right, left, root)."])

add("zigzag", "Binary Tree Zigzag Level Order Traversal", "binary-tree-zigzag-level-order-traversal", 1, "BFS", "Level order with a twist.",
 ["Normal BFS level by level; reverse every second level (or fill each level's vector from the back)."],
 ["Queue with root", "For each level: pop size nodes, write val at index i or size-1-i", "Flip the direction flag"],
 """class Solution {
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
};""",
 """assert((Solution().zigzagLevelOrder(tree({"3","9","20","null","null","15","7"})) == vector<vector<int>>{{3},{20,9},{15,7}}));""",
 "O(n) time, O(n) space", ["Changing the order children are pushed instead of the write order (breaks lower levels)"],
 ["Vertical order traversal (sort by column, then row, then value)."])

add("lca-bst", "Lowest Common Ancestor of a Binary Search Tree", "lowest-common-ancestor-of-a-binary-search-tree", 1, "BST", "Use the BST order.",
 ["If both values are smaller than the node, the LCA is on the left; if both larger, on the right; otherwise this node splits them and is the LCA."],
 ["Loop from the root", "Both < val: go left; both > val: go right", "Else return the node"],
 """class Solution {
public:
    TreeNode* lowestCommonAncestor(TreeNode* r, TreeNode* p, TreeNode* q) {
        while (r) {
            if (p->val < r->val && q->val < r->val) r = r->left;
            else if (p->val > r->val && q->val > r->val) r = r->right;
            else return r;
        }
        return nullptr;
    }
};""",
 """TreeNode* r = tree({"6","2","8","0","4","7","9","null","null","3","5"});
TreeNode *two = r->left, *eight = r->right, *four = r->left->right;
assert(Solution().lowestCommonAncestor(r, two, eight) == r && Solution().lowestCommonAncestor(r, two, four) == two);""",
 "O(h) time, O(1) space", ["Using the general binary-tree LCA (works but ignores the BST property)"],
 ["What if p or q may be missing from the tree? Check existence first."])

add("delete-bst", "Delete Node in a BST", "delete-node-in-a-bst", 1, "BST", "The three deletion cases.",
 ["Find the node. No left child: return right. No right child: return left. Two children: copy the smallest value of the right subtree into the node, then delete that value from the right subtree."],
 ["Recurse left or right by comparing keys", "Handle the 0/1-child cases by returning the other child", "Two children: successor = leftmost of right"],
 """class Solution {
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
};""",
 """auto inorder = [](TreeNode* t) { vector<int> v; function<void(TreeNode*)> go = [&](TreeNode* x) { if (!x) return; go(x->left); v.push_back(x->val); go(x->right); }; go(t); return v; };
TreeNode* r = Solution().deleteNode(tree({"5","3","6","2","4","null","7"}), 3); assert((inorder(r) == vector<int>{2,4,5,6,7}));
r = Solution().deleteNode(r, 5); assert((inorder(r) == vector<int>{2,4,6,7})); assert((inorder(Solution().deleteNode(r, 0)) == vector<int>{2,4,6,7}));""",
 "O(h) time, O(h) stack", ["Losing a subtree in the two-children case"],
 ["Insert into a BST; check the tree stays balanced (AVL / red-black discussion)."])

add("distance-k", "All Nodes Distance K in Binary Tree", "all-nodes-distance-k-in-binary-tree", 1, "BFS", "Turn the tree into a graph.",
 ["Record each node's parent with a DFS. Then BFS from the target over three neighbours (left, right, parent) for k steps; the nodes in the queue are the answer."],
 ["DFS to fill parent[]", "BFS from target with a visited set, k levels", "Return the values in the last level"],
 """class Solution {
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
};""",
 """TreeNode* r = tree({"3","5","1","6","2","0","8","null","null","7","4"});
auto v = Solution().distanceK(r, r->left, 2); sort(v.begin(), v.end()); assert((v == vector<int>{1,4,7}));""",
 "O(n) time, O(n) space", ["Revisiting the node you came from (use a visited set)"],
 ["Do it without the parent map: return distances up the recursion."])

# ---------------- BFS / DFS on graphs ----------------
add("open-lock", "Open the Lock", "open-the-lock", 1, "BFS", "Shortest path in an implicit graph.",
 ["States are the 10,000 four-digit strings; each has 8 neighbours (turn one wheel up or down). BFS from \"0000\" avoiding deadends; the level when the target appears is the answer."],
 ["Put deadends in a visited set; if \"0000\" is dead return -1", "BFS by levels", "For each wheel, try ±1 mod 10"],
 """class Solution {
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
};""",
 """vector<string> a{"0201","0101","0102","1212","2002"}, b{"8888"}, c{"8887","8889","8878","8898","8788","8988","7888","9888"};
assert(Solution().openLock(a, "0202") == 6 && Solution().openLock(b, "0009") == 1 && Solution().openLock(c, "8888") == -1);""",
 "O(10⁴ · 8) time and space", ["Wheel arithmetic for 0 → 9 (use + 9 mod 10)"],
 ["Bidirectional BFS roughly halves the explored states."])

add("shortest-binary", "Shortest Path in Binary Matrix", "shortest-path-in-binary-matrix", 1, "BFS", "Grid BFS with 8 directions.",
 ["BFS from the top-left over 0-cells in 8 directions, counting cells on the path. Mark cells as visited when pushed. Blocked start or end means -1."],
 ["If g[0][0] or g[n-1][n-1] is 1: return -1", "dist starts at 1", "Pop, check if it is the end, push 8 neighbours"],
 """class Solution {
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
};""",
 """vector<vector<int>> a{{0,1},{1,0}}, b{{0,0,0},{1,1,0},{1,1,0}}, c{{1,0,0},{1,1,0},{1,1,0}}, d{{0}};
assert(Solution().shortestPathBinaryMatrix(a) == 2 && Solution().shortestPathBinaryMatrix(b) == 4 && Solution().shortestPathBinaryMatrix(c) == -1 && Solution().shortestPathBinaryMatrix(d) == 1);""",
 "O(n²) time and space", ["Marking visited when popped (cells get pushed many times)"],
 ["Weighted cells: Dijkstra. A* with Chebyshev distance as the heuristic."])

add("bipartite", "Is Graph Bipartite?", "is-graph-bipartite", 1, "BFS", "Two-colouring.",
 ["Colour each uncoloured node 0 and BFS; every neighbour must get the opposite colour. A neighbour with the same colour means an odd cycle: not bipartite. Start from every node (the graph may be disconnected)."],
 ["color[] = -1", "For each uncoloured node: BFS", "Same colour on an edge → false"],
 """class Solution {
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
};""",
 """vector<vector<int>> a{{1,2,3},{0,2},{0,1,3},{0,2}}, b{{1,3},{0,2},{1,3},{0,2}}, c{{},{2},{1}};
assert(!Solution().isBipartite(a) && Solution().isBipartite(b) && Solution().isBipartite(c));""",
 "O(V + E) time, O(V) space", ["Starting only from node 0 (misses other components)"],
 ["Possible Bipartition (dislikes list): build the graph, same check.", "Union-Find version: union all neighbours of u; u must not join them."])

add("safe-states", "Find Eventual Safe States", "find-eventual-safe-states", 1, "Topological sort", "Kahn's algorithm on the reversed graph.",
 ["A node is safe if every path leads to a terminal node. Reverse the edges and run Kahn's algorithm from the terminal nodes (out-degree 0): everything removed is safe; nodes on or leading into cycles never reach 0."],
 ["outdeg[u] = g[u].size(); rev[v].push_back(u)", "Queue all nodes with outdeg 0", "Pop u, mark safe, for p in rev[u]: if --outdeg[p] == 0 push"],
 """class Solution {
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
};""",
 """vector<vector<int>> a{{1,2},{2,3},{5},{0},{5},{},{}}, b{{1,2,3,4},{1,2},{3,4},{0,4},{}};
assert((Solution().eventualSafeNodes(a) == vector<int>{2,4,5,6}) && (Solution().eventualSafeNodes(b) == vector<int>{4}));""",
 "O(V + E) time and space", ["Using in-degree on the original graph (answers a different question)"],
 ["DFS with three colours (white, grey on stack, black safe) gives the same answer."])

add("min-effort", "Path With Minimum Effort", "path-with-minimum-effort", 1, "Shortest paths", "Dijkstra with a max instead of a sum.",
 ["The cost of a path is its largest height step. Dijkstra still works: the cost to reach a neighbour is max(cost so far, |height difference|), and it never decreases along a path."],
 ["dist all INF, dist[0][0] = 0, min-heap of (dist, r, c)", "Pop; skip stale entries; stop at the bottom-right", "Relax 4 neighbours with max()"],
 """class Solution {
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
};""",
 """vector<vector<int>> a{{1,2,2},{3,8,2},{5,3,5}}, b{{1,2,3},{3,8,4},{5,3,5}}, c{{1,2,1,1,1},{1,2,1,2,1},{1,2,1,2,1},{1,2,1,2,1},{1,1,1,2,1}};
assert(Solution().minimumEffortPath(a) == 2 && Solution().minimumEffortPath(b) == 1 && Solution().minimumEffortPath(c) == 0);""",
 "O(RC log(RC)) time, O(RC) space", ["Summing the differences instead of taking the max"],
 ["Alternative: binary search the effort + BFS, or Kruskal with Union-Find until start and end connect."])

# ---------------- MST and Union-Find ----------------
add("min-cost-points", "Min Cost to Connect All Points", "min-cost-to-connect-all-points", 1, "MST", "Minimum spanning tree (Prim).",
 ["Connect all points with minimum total Manhattan distance = an MST of the complete graph. Prim's O(n²) version is simplest for a dense graph: keep each point's cheapest edge to the tree, add the cheapest point, update."],
 ["minEdge[i] = INF, minEdge[0] = 0", "n times: pick the unused point with the smallest minEdge, add it", "Update every unused point's minEdge with its distance to the new point"],
 """class Solution {
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
};""",
 """vector<vector<int>> a{{0,0},{2,2},{3,10},{5,2},{7,0}}, b{{3,12},{-2,5},{-4,1}}, c{{0,0}};
assert(Solution().minCostConnectPoints(a) == 20 && Solution().minCostConnectPoints(b) == 18 && Solution().minCostConnectPoints(c) == 0);""",
 "O(n²) time, O(n) space", ["Kruskal on all n² edges works but sorts ~n²/2 edges (slower for n = 1000)"],
 ["Explain Kruskal with Union-Find and when it beats Prim (sparse graphs)."])

add("network-connected", "Number of Operations to Make Network Connected", "number-of-operations-to-make-network-connected", 1, "Union-Find", "Count components.",
 ["With fewer than n − 1 cables it is impossible. Otherwise, every redundant cable can be moved, and you need components − 1 moves. Count components with Union-Find."],
 ["If edges < n - 1: return -1", "Union every cable; components = n − successful unions", "Return components − 1"],
 """class Solution {
    vector<int> par;
    int find(int x) { return par[x] == x ? x : par[x] = find(par[x]); }
public:
    int makeConnected(int n, vector<vector<int>>& cables) {
        if ((int)cables.size() < n - 1) return -1;
        par.resize(n); iota(par.begin(), par.end(), 0); int comps = n;
        for (auto& c : cables) { int a = find(c[0]), b = find(c[1]); if (a != b) { par[a] = b; comps--; } }
        return comps - 1;
    }
};""",
 """vector<vector<int>> a{{0,1},{0,2},{1,2}}, b{{0,1},{0,2},{0,3},{1,2},{1,3}}, c{{0,1},{0,2},{0,3},{1,2}};
assert(Solution().makeConnected(4, a) == 1 && Solution().makeConnected(6, b) == 2 && Solution().makeConnected(6, c) == -1);""",
 "O((n + E) α(n)) time, O(n) space", ["Counting redundant cables instead of components (only the count check needs them)"],
 ["Add union by rank and explain why α(n) is effectively constant."])

# ---------------- Backtracking ----------------
add("combination-sum-ii", "Combination Sum II", "combination-sum-ii", 1, "Backtracking", "Duplicates in the input.",
 ["Sort. At each depth, try each candidate once per value: skip a[i] if i > start and a[i] == a[i−1]. Each number is used at most once, so recurse with i + 1. Stop early when a[i] exceeds the remaining target."],
 ["Sort", "dfs(start, rem): if rem == 0 record", "for i ≥ start: skip same-value siblings; break if a[i] > rem; recurse i + 1"],
 """class Solution {
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
};""",
 """vector<int> a{10,1,2,7,6,1,5}, b{2,5,2,1,2};
assert((Solution().combinationSum2(a, 8) == vector<vector<int>>{{1,1,6},{1,2,5},{1,7},{2,6}}));
assert((Solution().combinationSum2(b, 5) == vector<vector<int>>{{1,2,2},{5}}));""",
 "O(2ⁿ) worst case time, O(n) depth", ["Skipping with i > 0 instead of i > start (loses [1,1,6])"],
 ["Combination Sum III (k numbers from 1–9)."])

add("palindrome-partitioning", "Palindrome Partitioning", "palindrome-partitioning", 1, "Backtracking", "Cut points with a palindrome check.",
 ["From position s, try every end e where s[s..e] is a palindrome, take it, and recurse from e + 1. A precomputed table pal[i][j] makes each check O(1)."],
 ["pal[i][j] = s[i]==s[j] && (j - i < 2 || pal[i+1][j-1]) (fill i from the end)", "dfs(start): at the end record the path", "Try each palindromic piece"],
 """class Solution {
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
};""",
 """assert((Solution().partition("aab") == vector<vector<string>>{{"a","a","b"},{"aa","b"}}) && (Solution().partition("a") == vector<vector<string>>{{"a"}}));
assert(Solution().partition("aaaa").size() == 8);""",
 "O(n · 2ⁿ) time, O(n²) table", ["Filling the table with i ascending (pal[i+1][j-1] not ready yet)"],
 ["Palindrome Partitioning II: minimum cuts with DP in O(n²)."])

add("sudoku-solver", "Sudoku Solver", "sudoku-solver", 3, "Backtracking", "Constraint backtracking with bitmasks.",
 ["Keep a 9-bit mask of used digits per row, column and box. Go through empty cells in order; for each, try digits not in any of the three masks, set, recurse, unset on failure."],
 ["Build masks and the list of empty cells", "solve(k): if k == empties.size() return true", "For each free digit: set bits, write, recurse; undo"],
 """class Solution {
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
};""",
 """vector<string> s{"53..7....","6..195...",".98....6.","8...6...3","4..8.3..1","7...2...6",".6....28.","...419..5","....8..79"};
vector<vector<char>> b; for (auto& x : s) b.push_back(vector<char>(x.begin(), x.end())); Solution().solveSudoku(b);
vector<string> want{"534678912","672195348","198342567","859761423","426853791","713924856","961537284","287419635","345286179"};
for (int r = 0; r < 9; r++) assert(string(b[r].begin(), b[r].end()) == want[r]);""",
 "Exponential worst case, fast in practice; O(81) space", ["Forgetting to reset the cell to '.' when backtracking past it"],
 ["Speed-up: always fill the empty cell with the fewest options next (MRV heuristic)."])

# ---------------- Greedy / intervals ----------------
add("partition-labels", "Partition Labels", "partition-labels", 1, "Greedy", "Last occurrence trick.",
 ["Record the last index of each letter. Scan, extending the current part's end to the last index of every letter seen. When i reaches that end, close the part."],
 ["last[c] for each letter", "end = max(end, last[s[i]])", "If i == end: record i - start + 1, start = i + 1"],
 """class Solution {
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
};""",
 """assert((Solution().partitionLabels("ababcbacadefegdehijhklij") == vector<int>{9,7,8}) && (Solution().partitionLabels("eccbbbbdec") == vector<int>{10}));""",
 "O(n) time, O(1) space", ["Closing a part before checking every letter inside it"],
 ["This is Merge Intervals in disguise: each letter is the interval [first, last]."])

add("interval-intersections", "Interval List Intersections", "interval-list-intersections", 1, "Intervals", "Two pointers on sorted intervals.",
 ["Both lists are sorted and disjoint. The overlap of A[i] and B[j] is [max starts, min ends] if that is non-empty. Then drop whichever interval ends first."],
 ["lo = max(a0, b0), hi = min(a1, b1)", "If lo ≤ hi record", "Advance the pointer whose interval ends first"],
 """class Solution {
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
};""",
 """vector<vector<int>> A{{0,2},{5,10},{13,23},{24,25}}, B{{1,5},{8,12},{15,24},{25,26}}, C{}, D{{1,7}};
assert((Solution().intervalIntersection(A, B) == vector<vector<int>>{{1,2},{5,5},{8,10},{15,23},{24,24},{25,25}}));
assert(Solution().intervalIntersection(C, D).empty());""",
 "O(m + n) time, O(1) extra space", ["Advancing both pointers after a match"],
 ["Meeting scheduler: first common slot of at least d minutes (same loop, check hi − lo ≥ d)."])

# ---------------- DP ----------------
add("house-robber-ii", "House Robber II", "house-robber-ii", 1, "DP", "Circular version of House Robber.",
 ["The first and last houses are adjacent, so you cannot take both. Answer = max(rob houses 0..n−2, rob houses 1..n−1), each a plain House Robber in O(1) space."],
 ["n == 1: return a[0]", "line(l, r): prev2, prev1 rolling max", "Return max(line(0, n-2), line(1, n-1))"],
 """class Solution {
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
};""",
 """vector<int> a{2,3,2}, b{1,2,3,1}, c{1,2,3}, d{5};
assert(Solution().rob(a) == 3 && Solution().rob(b) == 4 && Solution().rob(c) == 3 && Solution().rob(d) == 5);""",
 "O(n) time, O(1) space", ["Forgetting n == 1 (both ranges become empty)"],
 ["House Robber III: houses on a binary tree (return (take, skip) per node)."])

add("target-sum", "Target Sum", "target-sum", 1, "DP", "Reduces to subset-sum counting.",
 ["Split the numbers into a plus set P and a minus set N: P − N = t and P + N = S, so P = (S + t) / 2. Count subsets with that sum using a 1D knapsack (iterate sums downwards)."],
 ["If |t| > S or (S + t) odd: return 0", "goal = (S + t) / 2; dp[0] = 1", "For each x: for s from goal down to x: dp[s] += dp[s - x]"],
 """class Solution {
public:
    int findTargetSumWays(vector<int>& a, int t) {
        int S = accumulate(a.begin(), a.end(), 0);
        if (abs(t) > S || (S + t) % 2) return 0;
        int goal = (S + t) / 2; vector<int> dp(goal + 1); dp[0] = 1;
        for (int x : a) for (int s = goal; s >= x; s--) dp[s] += dp[s - x];
        return dp[goal];
    }
};""",
 """vector<int> a{1,1,1,1,1}, b{1}, c{0,0,0,0,0,0,0,0,1}, d{100};
assert(Solution().findTargetSumWays(a, 3) == 5 && Solution().findTargetSumWays(b, 1) == 1 && Solution().findTargetSumWays(c, 1) == 256 && Solution().findTargetSumWays(d, -200) == 0);""",
 "O(n · goal) time, O(goal) space", ["Iterating sums upwards (uses an item twice)", "Missing the |t| > S check (negative index)"],
 ["Explain why zeros double the count (each 0 can be + or −)."])

add("maximal-square", "Maximal Square", "maximal-square", 1, "DP", "Grid DP with a min of three.",
 ["dp[i][j] = side of the largest all-1 square with bottom-right corner (i, j) = 1 + min(top, left, top-left) when the cell is '1'. Track the maximum side and return its square."],
 ["dp sized (R+1) × (C+1) to avoid edge checks", "If m[i][j] == '1': dp = 1 + min of three neighbours", "Return best²"],
 """class Solution {
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
};""",
 """vector<string> s{"10100","10111","11111","10010"}; vector<vector<char>> m; for (auto& x : s) m.push_back(vector<char>(x.begin(), x.end()));
vector<vector<char>> z{{'0','1'},{'1','0'}}, o{{'0'}};
assert(Solution().maximalSquare(m) == 4 && Solution().maximalSquare(z) == 1 && Solution().maximalSquare(o) == 0);""",
 "O(RC) time, O(RC) space (O(C) with one row)", ["Returning the side instead of the area"],
 ["Maximal Rectangle: histogram + stack per row.", "Count all square submatrices: sum every dp value."])

add("stock-cooldown", "Best Time to Buy and Sell Stock with Cooldown", "best-time-to-buy-and-sell-stock-with-cooldown", 1, "DP", "State machine DP.",
 ["Three states at the end of each day: hold (own a share), sold (sold today), rest (no share, free to buy). hold = max(hold, rest − p); sold = hold + p; rest = max(rest, sold). Cooldown is enforced because you can only buy from rest."],
 ["hold = -INF, sold = 0, rest = 0", "Update all three from the previous day's values", "Answer max(sold, rest)"],
 """class Solution {
public:
    int maxProfit(vector<int>& p) {
        int hold = INT_MIN / 2, sold = 0, rest = 0;
        for (int x : p) {
            int h = max(hold, rest - x), s = hold + x, r = max(rest, sold);
            hold = h; sold = s; rest = r;
        }
        return max(sold, rest);
    }
};""",
 """vector<int> a{1,2,3,0,2}, b{1}, c{2,1};
assert(Solution().maxProfit(a) == 3 && Solution().maxProfit(b) == 0 && Solution().maxProfit(c) == 0);""",
 "O(n) time, O(1) space", ["Updating in place so today's sold uses today's hold"],
 ["With a transaction fee; at most k transactions (Stock IV)."])

add("interleaving-string", "Interleaving String", "interleaving-string", 1, "String DP", "2D DP over two prefixes.",
 ["dp[i][j] = can the first i chars of s1 and the first j chars of s2 form the first i + j chars of s3? It is true if the last char came from s1 (dp[i−1][j] and s1[i−1] == s3[i+j−1]) or from s2 (similarly)."],
 ["If lengths do not add up: false", "dp[0][0] = true", "Fill row by row; return dp[m][n]"],
 """class Solution {
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
};""",
 """assert(Solution().isInterleave("aabcc", "dbbca", "aadbbcbcac") && !Solution().isInterleave("aabcc", "dbbca", "aadbbbaccc") && Solution().isInterleave("", "", ""));""",
 "O(mn) time, O(mn) space (O(n) with one row)", ["Greedy matching from s1 first (fails when both strings offer the same char)"],
 ["Reduce to O(n) space with a single row."])
