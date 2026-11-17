"""OA simulation packs II: 8 more sets x 3 LeetCode problems, none repeated from pack I or the 83 worked solutions (checked in test_oa.py).
Same format as oa_data.py."""
SETS = []
def S(title, focus, date, probs): SETS.append(dict(title=title, focus=focus, date=date, probs=probs))
def Q(slug, title, diff, mins, pattern, kb, gist, sketch, cx, edges, code, test):
    return dict(slug=slug, title=title, diff=diff, mins=mins, pattern=pattern, kb=kb, gist=gist, sketch=sketch, cx=cx, edges=edges, code=code, test=test)

S("Set 9: Arrays in place", "Bit tricks, backtracking, cyclic placement", "Sat 6 Mar 2027", [
 Q("missing-number", "Missing Number", "Easy", 10, "Bit manipulation", "bit-manipulation", "An array holds n distinct numbers from 0 to n; find the one missing.",
   ["XOR every index 0..n with every value: equal pairs cancel, leaving the missing number. (Or n(n+1)/2 minus the sum.)"], "O(n) time, O(1) space", ["Missing 0 or missing n"],
   """int missingNumber(vector<int>& a) { int x = a.size(); for (int i = 0; i < (int)a.size(); i++) x ^= i ^ a[i]; return x; }""",
   """vector<int> a{3,0,1}; assert(missingNumber(a) == 2); vector<int> b{9,6,4,2,3,5,7,0,1}; assert(missingNumber(b) == 8); vector<int> c{0}; assert(missingNumber(c) == 1);"""),
 Q("generate-parentheses", "Generate Parentheses", "Medium", 30, "Backtracking", "recursion", "List every valid string of n pairs of parentheses.",
   ["Build left to right: add '(' while fewer than n are open; add ')' while closes are fewer than opens."], "O(Catalan(n) · n)", ["n = 1"],
   """void gen(int n, int open, int close, string& cur, vector<string>& out) {
    if ((int)cur.size() == 2 * n) { out.push_back(cur); return; }
    if (open < n) { cur.push_back('('); gen(n, open + 1, close, cur, out); cur.pop_back(); }
    if (close < open) { cur.push_back(')'); gen(n, open, close + 1, cur, out); cur.pop_back(); }
}
vector<string> generateParenthesis(int n) { vector<string> out; string cur; gen(n, 0, 0, cur, out); return out; }""",
   """assert((generateParenthesis(3) == vector<string>{"((()))","(()())","(())()","()(())","()()()"})); assert(generateParenthesis(1).size() == 1); assert(generateParenthesis(4).size() == 14);"""),
 Q("first-missing-positive", "First Missing Positive", "Hard", 50, "Hashing", "hashing", "Find the smallest positive integer not in an unsorted array, in O(n) time and O(1) extra space.",
   ["The answer is in 1..n+1. Put each value v in 1..n at index v−1 by swapping until it is there or a duplicate blocks it.", "The first index i with a[i] ≠ i+1 gives i+1; if none, n+1."], "O(n) time, O(1) space", ["Duplicates (avoid infinite swaps)", "All negative"],
   """int firstMissingPositive(vector<int>& a) {
    int n = a.size();
    for (int i = 0; i < n; i++) while (a[i] > 0 && a[i] <= n && a[a[i] - 1] != a[i]) swap(a[i], a[a[i] - 1]);
    for (int i = 0; i < n; i++) if (a[i] != i + 1) return i + 1;
    return n + 1;
}""", """vector<int> a{1,2,0}; assert(firstMissingPositive(a) == 3); vector<int> b{3,4,-1,1}; assert(firstMissingPositive(b) == 2); vector<int> c{7,8,9,11,12}; assert(firstMissingPositive(c) == 1); vector<int> d{1,1}; assert(firstMissingPositive(d) == 2);"""),
])

S("Set 10: Strings and intervals", "Two pointers, interval merging, stack", "Sat 1 May 2027", [
 Q("valid-palindrome", "Valid Palindrome", "Easy", 10, "Two pointers", "two-pointers", "Is a string a palindrome when only letters and digits count and case is ignored?",
   ["Two pointers from both ends; skip non-alphanumeric characters; compare lowercase."], "O(n) time, O(1) space", ["Empty or only spaces is a palindrome"],
   """bool isPalindrome(string s) {
    int i = 0, j = (int)s.size() - 1;
    while (i < j) {
        if (!isalnum((unsigned char)s[i])) { i++; continue; }
        if (!isalnum((unsigned char)s[j])) { j--; continue; }
        if (tolower((unsigned char)s[i]) != tolower((unsigned char)s[j])) return false;
        i++; j--;
    }
    return true;
}""", """assert(isPalindrome("A man, a plan, a canal: Panama")); assert(!isPalindrome("race a car")); assert(isPalindrome(" ")); assert(!isPalindrome("0P"));"""),
 Q("insert-interval", "Insert Interval", "Medium", 30, "Intervals", "intervals", "Insert a new interval into sorted, non-overlapping intervals and merge where needed.",
   ["Copy intervals ending before the new one; merge every interval that overlaps it into one; copy the rest."], "O(n) time", ["New interval before all or after all", "Touching endpoints merge"],
   """vector<vector<int>> insert(vector<vector<int>>& a, vector<int> nw) {
    vector<vector<int>> r; size_t i = 0;
    while (i < a.size() && a[i][1] < nw[0]) r.push_back(a[i++]);
    while (i < a.size() && a[i][0] <= nw[1]) { nw[0] = min(nw[0], a[i][0]); nw[1] = max(nw[1], a[i][1]); i++; }
    r.push_back(nw);
    while (i < a.size()) r.push_back(a[i++]);
    return r;
}""", """vector<vector<int>> a{{1,3},{6,9}}; assert((insert(a,{2,5}) == vector<vector<int>>{{1,5},{6,9}}));
vector<vector<int>> b{{1,2},{3,5},{6,7},{8,10},{12,16}}; assert((insert(b,{4,8}) == vector<vector<int>>{{1,2},{3,10},{12,16}}));
vector<vector<int>> c{}; assert((insert(c,{5,7}) == vector<vector<int>>{{5,7}}));"""),
 Q("longest-valid-parentheses", "Longest Valid Parentheses", "Hard", 50, "Stack", "stack-queue", "Length of the longest well-formed parentheses substring.",
   ["Keep a stack of indices with a base: start with −1. Push the index of each '('. On ')', pop; if the stack is empty, push this index as the new base; else the valid length is i − top."], "O(n) time, O(n) space", ["Empty string", "Leading ')'"],
   """int longestValidParentheses(string s) {
    vector<int> st{-1}; int best = 0;
    for (int i = 0; i < (int)s.size(); i++) {
        if (s[i] == '(') st.push_back(i);
        else { st.pop_back(); if (st.empty()) st.push_back(i); else best = max(best, i - st.back()); }
    }
    return best;
}""", """assert(longestValidParentheses("(()") == 2); assert(longestValidParentheses(")()())") == 4); assert(longestValidParentheses("") == 0); assert(longestValidParentheses("()(()") == 2);"""),
])

S("Set 11: Windows and histograms", "XOR, sliding window, monotonic stack", "Sat 15 May 2027", [
 Q("single-number", "Single Number", "Easy", 10, "Bit manipulation", "bit-manipulation", "Every number appears twice except one; find it with O(1) extra space.",
   ["XOR all numbers: pairs cancel to 0."], "O(n) time, O(1) space", ["Single element array"],
   """int singleNumber(vector<int>& a) { int x = 0; for (int v : a) x ^= v; return x; }""", """vector<int> a{4,1,2,1,2}; assert(singleNumber(a) == 4); vector<int> b{1}; assert(singleNumber(b) == 1);"""),
 Q("subarray-product-less-than-k", "Subarray Product Less Than K", "Medium", 30, "Sliding window", "sliding-window", "Count contiguous subarrays of positive numbers whose product is less than k.",
   ["Grow a window to the right, multiplying; while the product is at least k, divide out from the left. Every window ending at r adds r − l + 1 subarrays."], "O(n) time, O(1) space", ["k ≤ 1 means no subarray qualifies"],
   """int numSubarrayProductLessThanK(vector<int>& a, int k) {
    if (k <= 1) return 0;
    long long prod = 1; int l = 0, cnt = 0;
    for (int r = 0; r < (int)a.size(); r++) { prod *= a[r]; while (prod >= k) prod /= a[l++]; cnt += r - l + 1; }
    return cnt;
}""", """vector<int> a{10,5,2,6}; assert(numSubarrayProductLessThanK(a,100) == 8); vector<int> b{1,2,3}; assert(numSubarrayProductLessThanK(b,0) == 0);"""),
 Q("maximal-rectangle", "Maximal Rectangle", "Hard", 50, "Monotonic stack", "monotonic-stack", "Largest rectangle of 1s in a binary matrix.",
   ["For each row, build column heights of consecutive 1s ending there.", "Each row is then 'largest rectangle in a histogram': a stack of increasing heights; pop and measure when a lower bar arrives."], "O(rows · cols) time, O(cols) space", ["Empty matrix", "All zeros"],
   """int largestRect(const vector<int>& h) {
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
}""", """vector<vector<char>> m{{'1','0','1','0','0'},{'1','0','1','1','1'},{'1','1','1','1','1'},{'1','0','0','1','0'}}; assert(maximalRectangle(m) == 6);
vector<vector<char>> z{{'0'}}; assert(maximalRectangle(z) == 0); vector<vector<char>> o{{'1'}}; assert(maximalRectangle(o) == 1);"""),
])

S("Set 12: Grids and BFS", "Hashing, flood fill from the border, BFS on indices", "Sat 29 May 2027", [
 Q("contains-duplicate", "Contains Duplicate", "Easy", 10, "Hashing", "hashing", "Does any value appear at least twice?",
   ["Insert into a hash set; a failed insert means a duplicate."], "O(n) time and space", ["Empty array"],
   """bool containsDuplicate(vector<int>& a) { unordered_set<int> s; for (int v : a) if (!s.insert(v).second) return true; return false; }""",
   """vector<int> a{1,2,3,1}; assert(containsDuplicate(a)); vector<int> b{1,2,3,4}; assert(!containsDuplicate(b));"""),
 Q("surrounded-regions", "Surrounded Regions", "Medium", 35, "DFS", "dfs", "Flip every region of 'O' not connected to the border into 'X'.",
   ["Regions touching the border survive. DFS from every border 'O' and mark it safe.", "Then flip remaining 'O' to 'X' and safe marks back to 'O'."], "O(rows · cols)", ["Single row or column", "No 'O' at all"],
   """void mark(vector<vector<char>>& b, int r, int c) {
    if (r < 0 || c < 0 || r >= (int)b.size() || c >= (int)b[0].size() || b[r][c] != 'O') return;
    b[r][c] = 'S'; mark(b, r + 1, c); mark(b, r - 1, c); mark(b, r, c + 1); mark(b, r, c - 1);
}
void solve(vector<vector<char>>& b) {
    int m = b.size(), n = b[0].size();
    for (int i = 0; i < m; i++) { mark(b, i, 0); mark(b, i, n - 1); }
    for (int j = 0; j < n; j++) { mark(b, 0, j); mark(b, m - 1, j); }
    for (auto& row : b) for (char& ch : row) ch = ch == 'S' ? 'O' : 'X';
}""", """vector<vector<char>> b{{'X','X','X','X'},{'X','O','O','X'},{'X','X','O','X'},{'X','O','X','X'}}; solve(b);
assert((b == vector<vector<char>>{{'X','X','X','X'},{'X','X','X','X'},{'X','X','X','X'},{'X','O','X','X'}})); vector<vector<char>> c{{'O'}}; solve(c); assert(c[0][0] == 'O');"""),
 Q("jump-game-iv", "Jump Game IV", "Hard", 45, "BFS", "bfs", "From index i you may move to i−1, i+1 or any j with a[j] == a[i]. Minimum jumps from the first to the last index.",
   ["BFS over indices. Group indices by value; when you first use a value's group, enqueue all of them and then clear the group so it is never scanned again (this keeps BFS linear)."], "O(n) time and space", ["Single element: 0", "Long runs of equal values (clear the group)"],
   """int minJumps(vector<int>& a) {
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
}""", """vector<int> a{100,-23,-23,404,100,23,23,23,3,404}; assert(minJumps(a) == 3); vector<int> b{7}; assert(minJumps(b) == 0); vector<int> c{7,6,9,6,9,6,9,7}; assert(minJumps(c) == 1);"""),
])

S("Set 13: Search and counting DP", "Binary search, combination DP, string DP", "Sat 5 Jun 2027", [
 Q("find-peak-element", "Find Peak Element", "Medium", 20, "Binary search", "binary-search", "Return the index of any element greater than its neighbours, in O(log n).",
   ["If a[mid] < a[mid+1], a peak lies to the right; otherwise at mid or to the left."], "O(log n) time", ["Array of one element", "Strictly increasing array"],
   """int findPeakElement(vector<int>& a) { int lo = 0, hi = a.size() - 1; while (lo < hi) { int m = (lo + hi) / 2; if (a[m] < a[m + 1]) lo = m + 1; else hi = m; } return lo; }""",
   """vector<int> a{1,2,3,1}; assert(findPeakElement(a) == 2); vector<int> b{1,2,1,3,5,6,4}; int p = findPeakElement(b); assert(p == 1 || p == 5); vector<int> c{1}; assert(findPeakElement(c) == 0);"""),
 Q("coin-change-ii", "Coin Change II", "Medium", 30, "DP", "dp", "Count the combinations of coins that make an amount (order does not matter).",
   ["dp[x] = ways to make x. Loop coins on the outside and amounts inside, so each combination is counted once: dp[x] += dp[x − coin]."], "O(coins · amount)", ["Amount 0 has one way", "Loop order swapped counts permutations instead"],
   """int change(int amount, vector<int>& coins) {
    vector<unsigned long long> dp(amount + 1, 0); dp[0] = 1;
    for (int c : coins) for (int x = c; x <= amount; x++) dp[x] += dp[x - c];
    return (int)dp[amount];
}""", """vector<int> a{1,2,5}; assert(change(5,a) == 4); vector<int> b{2}; assert(change(3,b) == 0); vector<int> c{10}; assert(change(10,c) == 1); assert(change(0,a) == 1);"""),
 Q("distinct-subsequences", "Distinct Subsequences", "Hard", 40, "DP", "lcs", "Count the subsequences of s that equal t.",
   ["dp[j] = ways to form the first j characters of t. For each character of s, go j from right to left: if s[i] == t[j−1], dp[j] += dp[j−1]."], "O(|s| · |t|) time, O(|t|) space", ["t longer than s gives 0", "Iterate j backwards so each s character is used once"],
   """int numDistinct(string s, string t) {
    vector<unsigned long long> dp(t.size() + 1, 0); dp[0] = 1;
    for (char ch : s) for (int j = t.size(); j >= 1; j--) if (ch == t[j - 1]) dp[j] += dp[j - 1];
    return (int)dp[t.size()];
}""", """assert(numDistinct("rabbbit","rabbit") == 3); assert(numDistinct("babgbag","bag") == 5); assert(numDistinct("a","ab") == 0);"""),
])

S("Set 14: Design and counting", "Arithmetic, monotonic stack class, Fenwick tree", "Sat 19 Jun 2027", [
 Q("plus-one", "Plus One", "Easy", 10, "Two pointers", "two-pointers", "Add one to a number stored as an array of digits.",
   ["From the last digit: if it is below 9, add one and stop; else set it to 0 and carry. If every digit carried, put a 1 in front."], "O(n)", ["All nines"],
   """vector<int> plusOne(vector<int> d) { for (int i = d.size() - 1; i >= 0; i--) { if (d[i] < 9) { d[i]++; return d; } d[i] = 0; } d.insert(d.begin(), 1); return d; }""",
   """assert((plusOne({1,2,3}) == vector<int>{1,2,4})); assert((plusOne({9}) == vector<int>{1,0})); assert((plusOne({9,9}) == vector<int>{1,0,0}));"""),
 Q("online-stock-span", "Online Stock Span", "Medium", 30, "Monotonic stack", "monotonic-stack", "Design a class: for each new price, return how many consecutive days (including today) had a price at most today's.",
   ["Keep a stack of (price, span) with decreasing prices. Pop every entry with price ≤ today and add its span to today's."], "Amortised O(1) per call", ["Equal prices are popped too"],
   """class StockSpanner {
    vector<pair<int, int>> st;
public:
    int next(int price) { int span = 1; while (!st.empty() && st.back().first <= price) { span += st.back().second; st.pop_back(); } st.push_back({price, span}); return span; }
};""", """StockSpanner s; vector<int> got; for (int p : {100,80,60,70,60,75,85}) got.push_back(s.next(p)); assert((got == vector<int>{1,1,1,2,1,4,6}));"""),
 Q("count-of-smaller-numbers-after-self", "Count of Smaller Numbers After Self", "Hard", 50, "Binary search", "binary-search", "For each element, count the smaller elements to its right.",
   ["Compress values to ranks. Walk from the right with a Fenwick (binary indexed) tree: the answer for a[i] is the count of ranks below its own; then add its rank."], "O(n log n) time, O(n) space", ["Equal values do not count as smaller", "Negative numbers (compress first)"],
   """vector<int> countSmaller(vector<int>& a) {
    vector<int> v(a); sort(v.begin(), v.end()); v.erase(unique(v.begin(), v.end()), v.end());
    int m = v.size(); vector<int> bit(m + 1, 0), res(a.size());
    for (int i = (int)a.size() - 1; i >= 0; i--) {
        int r = lower_bound(v.begin(), v.end(), a[i]) - v.begin();   // 0-based rank; count ranks < r
        int c = 0; for (int x = r; x > 0; x -= x & -x) c += bit[x];
        res[i] = c;
        for (int x = r + 1; x <= m; x += x & -x) bit[x]++;
    }
    return res;
}""", """vector<int> a{5,2,6,1}; assert((countSmaller(a) == vector<int>{2,1,1,0})); vector<int> b{-1,-1}; assert((countSmaller(b) == vector<int>{0,0})); vector<int> c{-1}; assert((countSmaller(c) == vector<int>{0}));"""),
])

S("Set 15: Union-find and merge sort", "DSU, interval DP on strings, counting with merge sort", "Sat 26 Jun 2027", [
 Q("redundant-connection", "Redundant Connection", "Medium", 25, "Union-find", "dsu", "A tree plus one extra edge is given; return the edge that, removed, leaves a tree (the last such edge in the input).",
   ["Union-find over the edges in order: the first edge whose ends are already connected closes the cycle."], "O(n α(n))", ["Return the last cycle edge in input order (the first one that fails)"],
   """vector<int> findRedundantConnection(vector<vector<int>>& e) {
    vector<int> p(e.size() + 1); iota(p.begin(), p.end(), 0);
    function<int(int)> f = [&](int x) { return p[x] == x ? x : p[x] = f(p[x]); };
    for (auto& ed : e) { int a = f(ed[0]), b = f(ed[1]); if (a == b) return ed; p[a] = b; }
    return {};
}""", """vector<vector<int>> a{{1,2},{1,3},{2,3}}; assert((findRedundantConnection(a) == vector<int>{2,3})); vector<vector<int>> b{{1,2},{2,3},{3,4},{1,4},{1,5}}; assert((findRedundantConnection(b) == vector<int>{1,4}));"""),
 Q("longest-palindromic-subsequence", "Longest Palindromic Subsequence", "Medium", 30, "DP", "lcs", "Length of the longest subsequence that reads the same both ways.",
   ["dp[i][j] for s[i..j]: equal ends give dp[i+1][j−1] + 2; otherwise max(dp[i+1][j], dp[i][j−1]). Fill i from the end."], "O(n²) time and space", ["Single character is 1"],
   """int longestPalindromeSubseq(string s) {
    int n = s.size(); vector<vector<int>> dp(n, vector<int>(n, 0));
    for (int i = n - 1; i >= 0; i--) { dp[i][i] = 1; for (int j = i + 1; j < n; j++) dp[i][j] = s[i] == s[j] ? dp[i + 1][j - 1] + 2 : max(dp[i + 1][j], dp[i][j - 1]); }
    return dp[0][n - 1];
}""", """assert(longestPalindromeSubseq("bbbab") == 4); assert(longestPalindromeSubseq("cbbd") == 2); assert(longestPalindromeSubseq("a") == 1);"""),
 Q("reverse-pairs", "Reverse Pairs", "Hard", 35, "Divide and conquer", "complexity", "Count pairs i < j with a[i] > 2·a[j].",
   ["Merge sort. Before merging two sorted halves, count for each left element how many right elements r satisfy left > 2·r with one moving pointer; then merge."], "O(n log n)", ["Use 64-bit for 2·a[j]", "Negative numbers"],
   """long long sortCount(vector<int>& a, int lo, int hi) {
    if (hi - lo <= 1) return 0;
    int mid = (lo + hi) / 2; long long c = sortCount(a, lo, mid) + sortCount(a, mid, hi);
    for (int i = lo, j = mid; i < mid; i++) { while (j < hi && (long long)a[i] > 2LL * a[j]) j++; c += j - mid; }
    inplace_merge(a.begin() + lo, a.begin() + mid, a.begin() + hi);
    return c;
}
int reversePairs(vector<int>& a) { return (int)sortCount(a, 0, a.size()); }""",
   """vector<int> a{1,3,2,3,1}; assert(reversePairs(a) == 2); vector<int> b{2,4,3,5,1}; assert(reversePairs(b) == 3); vector<int> c{2147483647,2147483647,2147483647,2147483647,2147483647,2147483647}; assert(reversePairs(c) == 0);"""),
])

S("Set 16: Final mixed", "Backtracking, tree centres, interval DP", "Sat 10 Jul 2027", [
 Q("letter-combinations-of-a-phone-number", "Letter Combinations of a Phone Number", "Medium", 20, "Backtracking", "recursion", "Return all letter strings a phone keypad digit string could spell.",
   ["Backtrack over digits, appending each letter of the current digit's key."], "O(4^n · n)", ["Empty input returns an empty list, not [\"\"]"],
   """vector<string> letterCombinations(string d) {
    if (d.empty()) return {};
    static const string key[] = {"", "", "abc", "def", "ghi", "jkl", "mno", "pqrs", "tuv", "wxyz"};
    vector<string> out; string cur;
    function<void(int)> go = [&](int i) { if (i == (int)d.size()) { out.push_back(cur); return; } for (char ch : key[d[i] - '0']) { cur.push_back(ch); go(i + 1); cur.pop_back(); } };
    go(0); return out;
}""", """assert((letterCombinations("23") == vector<string>{"ad","ae","af","bd","be","bf","cd","ce","cf"})); assert(letterCombinations("").empty()); assert(letterCombinations("7").size() == 4);"""),
 Q("minimum-height-trees", "Minimum Height Trees", "Medium", 30, "Topological sort", "topo-sort", "Return every root that gives a tree of minimum height.",
   ["Peel leaves layer by layer (like Kahn's algorithm on degrees). The last one or two nodes left are the centres."], "O(n)", ["n = 1 returns [0]"],
   """vector<int> findMinHeightTrees(int n, vector<vector<int>>& e) {
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
}""", """vector<vector<int>> a{{1,0},{1,2},{1,3}}; assert((findMinHeightTrees(4,a) == vector<int>{1})); vector<vector<int>> b{{3,0},{3,1},{3,2},{3,4},{5,4}}; assert((findMinHeightTrees(6,b) == vector<int>{3,4})); vector<vector<int>> c{}; assert((findMinHeightTrees(1,c) == vector<int>{0}));"""),
 Q("minimum-cost-to-cut-a-stick", "Minimum Cost to Cut a Stick", "Hard", 40, "DP", "dp", "Cuts at given positions on a stick of length n; each cut costs the current piece's length. Minimise the total.",
   ["Sort cuts and add 0 and n as ends. dp[i][j] = minimum cost to make every cut strictly between ends i and j = min over k of dp[i][k] + dp[k][j] + (c[j] − c[i])."], "O(m³) for m cuts", ["Interval DP like Burst Balloons: choose the first cut in the range"],
   """int minCost(int n, vector<int> cuts) {
    cuts.push_back(0); cuts.push_back(n); sort(cuts.begin(), cuts.end());
    int m = cuts.size(); vector<vector<int>> dp(m, vector<int>(m, 0));
    for (int len = 2; len < m; len++) for (int i = 0; i + len < m; i++) {
        int j = i + len; dp[i][j] = INT_MAX;
        for (int k = i + 1; k < j; k++) dp[i][j] = min(dp[i][j], dp[i][k] + dp[k][j] + cuts[j] - cuts[i]);
    }
    return dp[0][m - 1];
}""", """assert(minCost(7,{1,3,4,5}) == 16); assert(minCost(9,{5,6,1,4,2}) == 22);"""),
])
