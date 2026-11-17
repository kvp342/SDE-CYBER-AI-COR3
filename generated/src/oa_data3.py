"""OA simulation packs III: sets 17-24, company-style themes in placement season. 24 problems, none repeated from
OA packs I-II or Worked Solutions I-III (checked in test_oa3.py). Same format as oa_data.py."""
SETS = []
def S(title, focus, date, probs): SETS.append(dict(title=title, focus=focus, date=date, probs=probs))
def Q(slug, title, diff, mins, pattern, kb, gist, sketch, cx, edges, code, test):
    return dict(slug=slug, title=title, diff=diff, mins=mins, pattern=pattern, kb=kb, gist=gist, sketch=sketch, cx=cx, edges=edges, code=code, test=test)

S("Set 17: Strings and arrays", "Service-company style: careful string handling", "Sat 17 Jul 2027", [
 Q("longest-common-prefix", "Longest Common Prefix", "Easy", 15, "Strings", "complexity", "Return the longest prefix shared by every string in a list.",
   ["Start with the first string as the prefix; for each other string, shrink the prefix to the part that matches."], "O(total characters) time, O(1) extra space", ["An empty result", "One string only"],
   """string longestCommonPrefix(vector<string>& s) {
    string p = s[0];
    for (auto& w : s) { size_t i = 0; while (i < p.size() && i < w.size() && p[i] == w[i]) i++; p.resize(i); }
    return p;
}""",
   """vector<string> a{"flower","flow","flight"}, b{"dog","racecar","car"}, c{"a"};
assert(longestCommonPrefix(a) == "fl" && longestCommonPrefix(b) == "" && longestCommonPrefix(c) == "a");"""),
 Q("string-compression", "String Compression", "Medium", 30, "Two pointers", "two-pointers", "Compress runs of repeated characters in place (\"aabbccc\" → a2b2c3) and return the new length.",
   ["Read pointer finds the end of each run; write pointer writes the character, then the run length's digits if it is more than 1."], "O(n) time, O(1) space", ["Run lengths of 10 or more (several digits)", "Single characters get no count"],
   """int compress(vector<char>& c) {
    int w = 0, n = c.size();
    for (int i = 0; i < n; ) {
        int j = i; while (j < n && c[j] == c[i]) j++;
        c[w++] = c[i];
        if (j - i > 1) for (char d : to_string(j - i)) c[w++] = d;
        i = j;
    }
    return w;
}""",
   """vector<char> a{'a','a','b','b','c','c','c'}; assert(compress(a) == 6 && string(a.begin(), a.begin() + 6) == "a2b2c3");
vector<char> b{'a'}; assert(compress(b) == 1);
vector<char> c{'a','b','b','b','b','b','b','b','b','b','b','b','b'}; assert(compress(c) == 4 && string(c.begin(), c.begin() + 4) == "ab12");"""),
 Q("text-justification", "Text Justification", "Hard", 45, "Simulation", "complexity", "Lay words out in lines of exactly W characters, spreading spaces evenly (extra spaces go left); the last line is left-aligned.",
   ["Greedily take as many words as fit (word lengths + one space between each).", "Last line or a single word: join with single spaces and pad right.", "Otherwise spaces = (W − letters) / gaps, and the first (W − letters) % gaps gaps get one more."],
   "O(total characters) time", ["A line with one word", "The last line is never fully justified"],
   """vector<string> fullJustify(vector<string>& w, int W) {
    vector<string> r; int n = w.size();
    for (int i = 0; i < n; ) {
        int j = i, len = 0;
        while (j < n && len + (int)w[j].size() + (j - i) <= W) len += w[j++].size();
        string line = w[i]; int gaps = j - i - 1;
        if (j == n || gaps == 0) {
            for (int k = i + 1; k < j; k++) line += " " + w[k];
            line += string(W - line.size(), ' ');
        } else {
            int sp = (W - len) / gaps, extra = (W - len) % gaps;
            for (int k = i + 1; k < j; k++) line += string(sp + (k - i <= extra ? 1 : 0), ' ') + w[k];
        }
        r.push_back(line); i = j;
    }
    return r;
}""",
   """vector<string> a{"This","is","an","example","of","text","justification."};
assert((fullJustify(a, 16) == vector<string>{"This    is    an","example  of text","justification.  "}));
vector<string> b{"What","must","be","acknowledgment","shall","be"};
assert((fullJustify(b, 16) == vector<string>{"What   must   be","acknowledgment  ","shall be        "}));"""),
])

S("Set 18: Graphs", "Product-company style: degrees, reachability, bridges", "Sat 24 Jul 2027", [
 Q("find-the-town-judge", "Find the Town Judge", "Easy", 15, "Graph degrees", "bfs", "The judge trusts nobody and is trusted by everyone else; find them or return -1.",
   ["Score = in-degree − out-degree; the judge is the only person with score n − 1."], "O(n + edges) time, O(n) space", ["n = 1 with no trust pairs (the single person is the judge)"],
   """int findJudge(int n, vector<vector<int>>& t) {
    vector<int> d(n + 1);
    for (auto& e : t) { d[e[0]]--; d[e[1]]++; }
    for (int i = 1; i <= n; i++) if (d[i] == n - 1) return i;
    return -1;
}""",
   """vector<vector<int>> a{{1,2}}, b{{1,3},{2,3}}, c{{1,3},{2,3},{3,1}}, e{};
assert(findJudge(2, a) == 2 && findJudge(3, b) == 3 && findJudge(3, c) == -1 && findJudge(1, e) == 1);"""),
 Q("keys-and-rooms", "Keys and Rooms", "Medium", 25, "DFS", "dfs", "Room 0 is open; each room holds keys to other rooms. Can you enter every room?",
   ["Graph reachability from node 0: DFS with a stack and a visited array, count visited rooms."], "O(rooms + keys) time, O(rooms) space", ["Keys to rooms already visited"],
   """bool canVisitAllRooms(vector<vector<int>>& rooms) {
    vector<bool> seen(rooms.size()); vector<int> st{0}; seen[0] = true; int cnt = 1;
    while (!st.empty()) {
        int u = st.back(); st.pop_back();
        for (int v : rooms[u]) if (!seen[v]) { seen[v] = true; cnt++; st.push_back(v); }
    }
    return cnt == (int)rooms.size();
}""",
   """vector<vector<int>> a{{1},{2},{3},{}}, b{{1,3},{3,0,1},{2},{0}};
assert(canVisitAllRooms(a) && !canVisitAllRooms(b));"""),
 Q("critical-connections-in-a-network", "Critical Connections in a Network", "Hard", 50, "Bridges (Tarjan)", "dfs", "Return every connection whose removal disconnects the network (the bridges).",
   ["DFS assigning discovery times tin[u]; low[u] = smallest tin reachable from u's subtree using one back edge.", "Edge (u, v) to a child v is a bridge when low[v] > tin[u]."],
   "O(V + E) time, O(V + E) space", ["Skip the edge back to the parent", "Disconnected graphs: start DFS from every unvisited node"],
   """vector<vector<int>> criticalConnections(int n, vector<vector<int>>& con) {
    vector<vector<int>> g(n); for (auto& e : con) { g[e[0]].push_back(e[1]); g[e[1]].push_back(e[0]); }
    vector<int> tin(n, -1), low(n); int timer = 0; vector<vector<int>> r;
    function<void(int, int)> dfs = [&](int u, int p) {
        tin[u] = low[u] = timer++;
        for (int v : g[u]) {
            if (v == p) continue;
            if (tin[v] != -1) low[u] = min(low[u], tin[v]);
            else { dfs(v, u); low[u] = min(low[u], low[v]); if (low[v] > tin[u]) r.push_back({u, v}); }
        }
    };
    for (int i = 0; i < n; i++) if (tin[i] == -1) dfs(i, -1);
    return r;
}""",
   """auto norm = [](vector<vector<int>> v) { for (auto& e : v) sort(e.begin(), e.end()); sort(v.begin(), v.end()); return v; };
vector<vector<int>> a{{0,1},{1,2},{2,0},{1,3}}, b{{0,1}}, c{{0,1},{1,2},{2,3},{3,1},{3,4}};
assert((norm(criticalConnections(4, a)) == vector<vector<int>>{{1,3}}) && (norm(criticalConnections(2, b)) == vector<vector<int>>{{0,1}}));
assert((norm(criticalConnections(5, c)) == vector<vector<int>>{{0,1},{3,4}}));"""),
])

S("Set 19: Dynamic programming", "DP-heavy rounds: 1D, chains, palindromes", "Sat 31 Jul 2027", [
 Q("min-cost-climbing-stairs", "Min Cost Climbing Stairs", "Easy", 10, "1D DP", "dp", "Pay cost[i] to step on stair i, then climb 1 or 2; start at 0 or 1. Minimum cost to reach the top.",
   ["dp[i] = min(dp[i−1] + cost[i−1], dp[i−2] + cost[i−2]); keep only two values."], "O(n) time, O(1) space", ["The top is one past the last stair"],
   """int minCostClimbingStairs(vector<int>& c) {
    int a = 0, b = 0;
    for (int i = 2; i <= (int)c.size(); i++) { int x = min(b + c[i - 1], a + c[i - 2]); a = b; b = x; }
    return b;
}""",
   """vector<int> a{10,15,20}, b{1,100,1,1,1,100,1,1,100,1}; assert(minCostClimbingStairs(a) == 15 && minCostClimbingStairs(b) == 6);"""),
 Q("longest-string-chain", "Longest String Chain", "Medium", 30, "DP on sorted order", "dp", "A word is a predecessor of another if inserting one letter makes it. Find the longest chain.",
   ["Sort words by length. dp[word] = 1 + max dp[word with one letter removed] over all removals found so far."], "O(n · L²) time, O(n · L) space", ["Several words of the same length", "Chains that skip a length do not count"],
   """int longestStrChain(vector<string>& w) {
    sort(w.begin(), w.end(), [](const string& a, const string& b) { return a.size() < b.size(); });
    unordered_map<string, int> dp; int best = 0;
    for (auto& s : w) {
        int cur = 1;
        for (size_t i = 0; i < s.size(); i++) {
            auto it = dp.find(s.substr(0, i) + s.substr(i + 1));
            if (it != dp.end()) cur = max(cur, it->second + 1);
        }
        dp[s] = cur; best = max(best, cur);
    }
    return best;
}""",
   """vector<string> a{"a","b","ba","bca","bda","bdca"}, b{"xbc","pcxbcf","xb","cxbc","pcxbc"}, c{"abcd","dbqca"};
assert(longestStrChain(a) == 4 && longestStrChain(b) == 5 && longestStrChain(c) == 1);"""),
 Q("minimum-insertion-steps-to-make-a-string-palindrome", "Minimum Insertion Steps to Make a String Palindrome", "Hard", 50, "String DP", "lcs", "Fewest characters to insert anywhere so the string becomes a palindrome.",
   ["Characters already in the longest palindromic subsequence can stay; every other one needs a partner inserted.", "Answer = n − LPS(s), and LPS(s) = LCS(s, reverse(s))."],
   "O(n²) time, O(n²) space (O(n) with two rows)", ["Already a palindrome (answer 0)"],
   """int minInsertions(string s) {
    int n = s.size(); string t(s.rbegin(), s.rend()); vector<vector<int>> dp(n + 1, vector<int>(n + 1));
    for (int i = 1; i <= n; i++)
        for (int j = 1; j <= n; j++)
            dp[i][j] = s[i - 1] == t[j - 1] ? dp[i - 1][j - 1] + 1 : max(dp[i - 1][j], dp[i][j - 1]);
    return n - dp[n][n];
}""",
   """assert(minInsertions("zzazz") == 0 && minInsertions("mbadm") == 2 && minInsertions("leetcode") == 5);"""),
])

S("Set 20: Heaps and greedy", "Priority queues and exchange arguments", "Sat 7 Aug 2027", [
 Q("last-stone-weight", "Last Stone Weight", "Easy", 10, "Heap", "heap", "Repeatedly smash the two heaviest stones; return the weight of the last stone (or 0).",
   ["Max-heap: pop two, push the difference if non-zero."], "O(n log n) time, O(n) space", ["All stones destroyed (return 0)"],
   """int lastStoneWeight(vector<int>& s) {
    priority_queue<int> pq(s.begin(), s.end());
    while (pq.size() > 1) { int a = pq.top(); pq.pop(); int b = pq.top(); pq.pop(); if (a != b) pq.push(a - b); }
    return pq.empty() ? 0 : pq.top();
}""",
   """vector<int> a{2,7,4,1,8,1}, b{1}, c{2,2}; assert(lastStoneWeight(a) == 1 && lastStoneWeight(b) == 1 && lastStoneWeight(c) == 0);"""),
 Q("hand-of-straights", "Hand of Straights", "Medium", 30, "Greedy with an ordered map", "greedy", "Can the cards be split into groups of k consecutive values?",
   ["The smallest remaining card must start a group. Walk an ordered count map; for each value with count f, take f from each of the next k values."], "O(n log n) time, O(n) space", ["n not divisible by k", "Duplicates"],
   """bool isNStraightHand(vector<int>& h, int k) {
    if (h.size() % k) return false;
    map<int, int> c; for (int x : h) c[x]++;
    for (auto it = c.begin(); it != c.end(); ++it) {
        int f = it->second; if (!f) continue;
        for (int d = 0; d < k; d++) {
            auto jt = c.find(it->first + d);
            if (jt == c.end() || jt->second < f) return false;
            jt->second -= f;
        }
    }
    return true;
}""",
   """vector<int> a{1,2,3,6,2,3,4,7,8}, b{1,2,3,4,5}; assert(isNStraightHand(a, 3) && !isNStraightHand(b, 4));"""),
 Q("ipo", "IPO", "Hard", 50, "Two heaps / greedy", "heap", "Start with capital w; do at most k projects, each needing capital[i] and adding profit[i]. Maximise final capital.",
   ["Sort projects by required capital. Each round, push every affordable project's profit into a max-heap and take the best one."], "O(n log n) time, O(n) space", ["No affordable project left: stop early"],
   """int findMaximizedCapital(int k, int w, vector<int>& p, vector<int>& c) {
    int n = p.size(); vector<pair<int, int>> v; for (int i = 0; i < n; i++) v.push_back({c[i], p[i]});
    sort(v.begin(), v.end());
    priority_queue<int> pq; int i = 0;
    while (k--) {
        while (i < n && v[i].first <= w) pq.push(v[i++].second);
        if (pq.empty()) break;
        w += pq.top(); pq.pop();
    }
    return w;
}""",
   """vector<int> p{1,2,3}, c1{0,1,1}, c2{0,1,2}; assert(findMaximizedCapital(2, 0, p, c1) == 4 && findMaximizedCapital(3, 0, p, c2) == 6);"""),
])

S("Set 21: Hashing and prefix sums", "Maps, remainders and 'at most k' counting", "Sat 14 Aug 2027", [
 Q("isomorphic-strings", "Isomorphic Strings", "Easy", 10, "Hashing", "hashing", "Can the characters of s be replaced one-to-one to get t?",
   ["Remember the last position each character was seen in s and in t; they must always match."], "O(n) time, O(1) space", ["Two characters mapping to the same one ('badc' → 'baba' is false)"],
   """bool isIsomorphic(string s, string t) {
    int a[256] = {}, b[256] = {};
    for (size_t i = 0; i < s.size(); i++) {
        unsigned char x = s[i], y = t[i];
        if (a[x] != b[y]) return false;
        a[x] = b[y] = i + 1;
    }
    return true;
}""",
   """assert(isIsomorphic("egg", "add") && !isIsomorphic("foo", "bar") && isIsomorphic("paper", "title") && !isIsomorphic("badc", "baba"));"""),
 Q("continuous-subarray-sum", "Continuous Subarray Sum", "Medium", 30, "Prefix sums mod k", "prefix-sum", "Is there a subarray of length at least 2 whose sum is a multiple of k?",
   ["Two prefix sums with the same remainder mod k bound a subarray divisible by k. Store the first index of each remainder (remainder 0 at index −1)."], "O(n) time, O(min(n, k)) space", ["Length must be at least 2", "Zeros: [0, 0] is divisible by any k"],
   """bool checkSubarraySum(vector<int>& a, int k) {
    unordered_map<int, int> first{{0, -1}}; int s = 0;
    for (int i = 0; i < (int)a.size(); i++) {
        s = (s + a[i]) % k;
        auto it = first.find(s);
        if (it == first.end()) first[s] = i;
        else if (i - it->second >= 2) return true;
    }
    return false;
}""",
   """vector<int> a{23,2,4,6,7}, b{23,2,6,4,7}, c{5,0,0,0}, d{1,0};
assert(checkSubarraySum(a, 6) && checkSubarraySum(b, 6) && !checkSubarraySum(b, 13) && checkSubarraySum(c, 3) && !checkSubarraySum(d, 2));"""),
 Q("subarrays-with-k-different-integers", "Subarrays with K Different Integers", "Hard", 50, "Sliding window (at most k)", "sliding-window", "Count subarrays with exactly k distinct values.",
   ["exactly(k) = atMost(k) − atMost(k − 1). atMost uses a sliding window: for each right end, all windows ending there with left ≥ l are valid (r − l + 1 of them)."], "O(n) time, O(n) space", ["The answer can exceed int for large n in variants: use long long inside"],
   """long long atMost(vector<int>& a, int k) {
    unordered_map<int, int> c; int l = 0; long long res = 0;
    for (int i = 0; i < (int)a.size(); i++) {
        if (c[a[i]]++ == 0) k--;
        while (k < 0) { if (--c[a[l]] == 0) k++; l++; }
        res += i - l + 1;
    }
    return res;
}
int subarraysWithKDistinct(vector<int>& a, int k) { return atMost(a, k) - atMost(a, k - 1); }""",
   """vector<int> a{1,2,1,2,3}, b{1,2,1,3,4}; assert(subarraysWithKDistinct(a, 2) == 7 && subarraysWithKDistinct(b, 3) == 3);"""),
])

S("Set 22: Trees", "Recursion on trees, level indices, greedy from the leaves", "Sat 21 Aug 2027", [
 Q("symmetric-tree", "Symmetric Tree", "Easy", 10, "Tree recursion", "trees", "Is the tree a mirror of itself?",
   ["Compare left and right subtrees as mirrors: values equal, outer pair mirrors, inner pair mirrors."], "O(n) time, O(h) stack", ["Empty tree is symmetric"],
   """bool mirror(TreeNode* a, TreeNode* b) {
    if (!a || !b) return a == b;
    return a->val == b->val && mirror(a->left, b->right) && mirror(a->right, b->left);
}
bool isSymmetric(TreeNode* r) { return !r || mirror(r->left, r->right); }""",
   """assert(isSymmetric(tree({"1","2","2","3","4","4","3"})) && !isSymmetric(tree({"1","2","2","null","3","null","3"})));"""),
 Q("maximum-width-of-binary-tree", "Maximum Width of Binary Tree", "Medium", 30, "BFS with indices", "bfs", "Width of a level = distance between its leftmost and rightmost nodes, counting the gaps. Return the maximum.",
   ["Number nodes like a heap (children 2i and 2i + 1). Subtract each level's first index so numbers stay small; width = last − first + 1."], "O(n) time, O(n) space", ["Index overflow on deep skewed trees (normalise per level, use unsigned 64-bit)"],
   """int widthOfBinaryTree(TreeNode* root) {
    if (!root) return 0;
    unsigned long long best = 0; queue<pair<TreeNode*, unsigned long long>> q; q.push({root, 0});
    while (!q.empty()) {
        int n = q.size(); unsigned long long base = q.front().second, first = 0, last = 0;
        for (int i = 0; i < n; i++) {
            auto [x, id] = q.front(); q.pop(); id -= base;
            if (i == 0) first = id;
            last = id;
            if (x->left) q.push({x->left, 2 * id});
            if (x->right) q.push({x->right, 2 * id + 1});
        }
        best = max(best, last - first + 1);
    }
    return (int)best;
}""",
   """assert(widthOfBinaryTree(tree({"1","3","2","5","3","null","9"})) == 4 && widthOfBinaryTree(tree({"1","3","2","5","null","null","9","6","null","7"})) == 7 && widthOfBinaryTree(tree({"1","3","2","5"})) == 2);"""),
 Q("binary-tree-cameras", "Binary Tree Cameras", "Hard", 50, "Greedy DFS (tree states)", "trees", "A camera covers its node, parent and children. Minimum cameras to cover every node.",
   ["Post-order states: 0 = not covered, 1 = has a camera, 2 = covered without one. Null counts as covered.", "If a child is uncovered, put a camera here; else if a child has a camera, this node is covered; else it is uncovered and its parent will handle it.", "Add one camera if the root ends uncovered."],
   "O(n) time, O(h) stack", ["The root left uncovered", "Order of evaluation: run the DFS before reading the counter"],
   """int cams;
int go(TreeNode* n) {
    if (!n) return 2;
    int l = go(n->left), r = go(n->right);
    if (l == 0 || r == 0) { cams++; return 1; }
    return (l == 1 || r == 1) ? 2 : 0;
}
int minCameraCover(TreeNode* root) { cams = 0; int s = go(root); return cams + (s == 0); }""",
   """assert(minCameraCover(tree({"0","0","null","0","0"})) == 1 && minCameraCover(tree({"0","0","null","0","null","0","null","null","0"})) == 2 && minCameraCover(tree({"0"})) == 1);"""),
])

S("Set 23: Matrices", "Grid recursion, staircase search, heap from the border", "Sat 28 Aug 2027", [
 Q("flood-fill", "Flood Fill", "Easy", 10, "DFS on a grid", "dfs", "Recolour the connected region of the starting pixel's colour.",
   ["DFS from the start, painting cells of the original colour. If the new colour equals the old one, return at once (otherwise infinite recursion)."], "O(R · C) time and stack", ["New colour equal to the old colour"],
   """void paint(vector<vector<int>>& g, int r, int c, int from, int to) {
    if (r < 0 || c < 0 || r >= (int)g.size() || c >= (int)g[0].size() || g[r][c] != from) return;
    g[r][c] = to;
    paint(g, r + 1, c, from, to); paint(g, r - 1, c, from, to); paint(g, r, c + 1, from, to); paint(g, r, c - 1, from, to);
}
vector<vector<int>> floodFill(vector<vector<int>>& g, int sr, int sc, int color) {
    if (g[sr][sc] != color) paint(g, sr, sc, g[sr][sc], color);
    return g;
}""",
   """vector<vector<int>> a{{1,1,1},{1,1,0},{1,0,1}}, b{{0,0,0},{0,0,0}};
assert((floodFill(a, 1, 1, 2) == vector<vector<int>>{{2,2,2},{2,2,0},{2,0,1}}) && (floodFill(b, 0, 0, 0) == vector<vector<int>>{{0,0,0},{0,0,0}}));"""),
 Q("search-a-2d-matrix-ii", "Search a 2D Matrix II", "Medium", 25, "Staircase search", "binary-search", "Rows and columns are each sorted ascending. Is the target present?",
   ["Start at the top-right corner: if it is too big move left, if too small move down. Each step removes a row or a column."], "O(R + C) time, O(1) space", ["Binary search per row works too but is O(R log C)"],
   """bool searchMatrix(vector<vector<int>>& m, int t) {
    int r = 0, c = m[0].size() - 1;
    while (r < (int)m.size() && c >= 0) {
        if (m[r][c] == t) return true;
        if (m[r][c] > t) c--; else r++;
    }
    return false;
}""",
   """vector<vector<int>> m{{1,4,7,11,15},{2,5,8,12,19},{3,6,9,16,22},{10,13,14,17,24},{18,21,23,26,30}};
assert(searchMatrix(m, 5) && !searchMatrix(m, 20) && searchMatrix(m, 30) && !searchMatrix(m, 0));"""),
 Q("trapping-rain-water-ii", "Trapping Rain Water II", "Hard", 55, "Min-heap from the border", "heap", "A height map on a grid: how much rain water stays trapped?",
   ["Water level is set by the lowest wall around. Push all border cells into a min-heap. Pop the lowest; for each unseen neighbour, it holds max(0, level − height) water; push it with level max(level, height)."],
   "O(RC log(RC)) time, O(RC) space", ["Grids smaller than 3 × 3 trap nothing"],
   """int trapRainWater(vector<vector<int>>& h) {
    int R = h.size(), C = h[0].size(); if (R < 3 || C < 3) return 0;
    priority_queue<array<int, 3>, vector<array<int, 3>>, greater<>> pq; vector<vector<bool>> seen(R, vector<bool>(C));
    for (int r = 0; r < R; r++) for (int c = 0; c < C; c++)
        if (r == 0 || c == 0 || r == R - 1 || c == C - 1) { pq.push({h[r][c], r, c}); seen[r][c] = true; }
    int water = 0, dr[] = {1, -1, 0, 0}, dc[] = {0, 0, 1, -1};
    while (!pq.empty()) {
        auto [ht, r, c] = pq.top(); pq.pop();
        for (int k = 0; k < 4; k++) {
            int nr = r + dr[k], nc = c + dc[k];
            if (nr < 0 || nc < 0 || nr >= R || nc >= C || seen[nr][nc]) continue;
            seen[nr][nc] = true; water += max(0, ht - h[nr][nc]); pq.push({max(ht, h[nr][nc]), nr, nc});
        }
    }
    return water;
}""",
   """vector<vector<int>> a{{1,4,3,1,3,2},{3,2,1,3,2,4},{2,3,3,2,3,1}}, b{{3,3,3,3,3},{3,2,2,2,3},{3,2,1,2,3},{3,2,2,2,3},{3,3,3,3,3}};
assert(trapRainWater(a) == 4 && trapRainWater(b) == 10);"""),
])

S("Set 24: Final mixed", "One of each: two pointers, grid DFS, two multisets", "Sat 4 Sep 2027", [
 Q("valid-palindrome-ii", "Valid Palindrome II", "Easy", 15, "Two pointers", "two-pointers", "Can the string become a palindrome by deleting at most one character?",
   ["Move pointers inwards; at the first mismatch, try skipping the left or the right character and check the rest."], "O(n) time, O(1) space", ["Only one deletion allowed: do not recurse again"],
   """bool isPal(const string& s, int i, int j) { while (i < j) if (s[i++] != s[j--]) return false; return true; }
bool validPalindrome(string s) {
    int i = 0, j = s.size() - 1;
    while (i < j) { if (s[i] != s[j]) return isPal(s, i + 1, j) || isPal(s, i, j - 1); i++; j--; }
    return true;
}""",
   """assert(validPalindrome("aba") && validPalindrome("abca") && !validPalindrome("abc") && validPalindrome("deeee"));"""),
 Q("max-area-of-island", "Max Area of Island", "Medium", 25, "DFS on a grid", "dfs", "Largest 4-connected group of 1s in a grid.",
   ["DFS from each land cell, sinking cells (set to 0) as they are counted so each is counted once."], "O(R · C) time, O(R · C) stack in the worst case", ["All water (answer 0)"],
   """int area(vector<vector<int>>& g, int r, int c) {
    if (r < 0 || c < 0 || r >= (int)g.size() || c >= (int)g[0].size() || !g[r][c]) return 0;
    g[r][c] = 0;
    return 1 + area(g, r + 1, c) + area(g, r - 1, c) + area(g, r, c + 1) + area(g, r, c - 1);
}
int maxAreaOfIsland(vector<vector<int>>& g) {
    int best = 0;
    for (int r = 0; r < (int)g.size(); r++) for (int c = 0; c < (int)g[0].size(); c++) best = max(best, area(g, r, c));
    return best;
}""",
   """vector<vector<int>> a{{1,1,0},{0,1,0},{0,0,1}}, b{{0,0,0,0,0,0,0,0}}, c{{1,1,0,0,0},{1,1,0,0,0},{0,0,0,1,1},{0,0,0,1,1}};
assert(maxAreaOfIsland(a) == 3 && maxAreaOfIsland(b) == 0 && maxAreaOfIsland(c) == 4);"""),
 Q("sliding-window-median", "Sliding Window Median", "Hard", 50, "Two multisets", "heap", "Median of every window of size k.",
   ["Keep the smaller half in lo and the larger in hi (lo has the extra element when k is odd).", "Insert into the right half, remove the element leaving the window from whichever half holds it, then rebalance."],
   "O(n log k) time, O(k) space", ["Overflow when averaging two large ints (convert to double first)", "Duplicates: erase one copy with find, not the value"],
   """vector<double> medianSlidingWindow(vector<int>& a, int k) {
    multiset<int> lo, hi; vector<double> r;
    auto balance = [&]() {
        while (lo.size() > hi.size() + 1) { hi.insert(*prev(lo.end())); lo.erase(prev(lo.end())); }
        while (hi.size() > lo.size()) { lo.insert(*hi.begin()); hi.erase(hi.begin()); }
    };
    for (int i = 0; i < (int)a.size(); i++) {
        if (lo.empty() || a[i] <= *prev(lo.end())) lo.insert(a[i]); else hi.insert(a[i]);
        if (i >= k) { int out = a[i - k]; if (out <= *prev(lo.end())) lo.erase(lo.find(out)); else hi.erase(hi.find(out)); }
        balance();
        if (i >= k - 1) r.push_back(k % 2 ? (double)*prev(lo.end()) : ((double)*prev(lo.end()) + (double)*hi.begin()) / 2.0);
    }
    return r;
}""",
   """vector<int> a{1,3,-1,-3,5,3,6,7}, b{1,2,3,4,2,3,1,4,2}, c{2147483647,2147483647};
assert((medianSlidingWindow(a, 3) == vector<double>{1,-1,-1,3,5,6}) && (medianSlidingWindow(b, 3) == vector<double>{2,3,3,3,2,3,2}));
assert((medianSlidingWindow(c, 2) == vector<double>{2147483647.0}) && (medianSlidingWindow(b, 4) == vector<double>{2.5,2.5,3,2.5,2.5,2.5}));"""),
])
