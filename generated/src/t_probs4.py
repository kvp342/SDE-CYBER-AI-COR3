"""Worked Solutions IV: 25 hard problems (L3) for product-company final rounds, none repeated from Worked Solutions I-III or OA packs I-III.
Same fields as t_probs3.py; every `code` is tested by `test` (see test_probs4.py)."""
LC = lambda slug: f"https://leetcode.com/problems/{slug}/"
REL = {"Two pointers": "two-pointers", "Sliding window": "sliding-window", "Binary search": "binary-search", "Hashing": "hashing",
       "Stack": "stack-queue", "Monotonic stack": "monotonic-stack", "Linked list": "linked-list", "Trees": "trees", "BST": "bst", "BFS": "bfs",
       "DFS": "dfs", "Topological sort": "topo-sort", "Shortest paths": "dijkstra", "Union-Find": "dsu", "MST": "dsu", "String algorithms": "string-algos", "Bitmask BFS": "bitmask-dp", "Interval DP": "dp", "Digit DP": "dp", "Divide and conquer": "recursion", "Simulation": "string-algos", "Geometry and hashing": "hashing", "Trie + backtracking": "trie", "Binary search on the answer": "binary-search", "LIS": "dp", "Grid DP": "dp", "Stock DP": "dp", "Heap": "heap", "DP": "dp",
       "String DP": "lcs", "Backtracking": "recursion", "Greedy": "greedy", "Intervals": "intervals"}
P = []
def add(id, title, slug, lvl, pattern, where, idea, steps, code, test, cx, traps, follow):
    P.append(dict(id="p4-" + id, title=title, slug=slug, cat="Problems", lvl={0: 1, 1: 2, 3: 3}[lvl], aka=[title], why=f"Pattern: {pattern}. {where}",
                  core=idea, points=steps + [f"Complexity: {cx}"], code=code, test=test, pit=traps, ask=follow,
                  prac=[(f"Solve it on LeetCode: {title}", LC(slug))], learn=[], rel=[REL[pattern]]))


# ---------------- String DP and string algorithms
add("wildcard", "Wildcard Matching", "wildcard-matching", 3, "String DP", "Classic 2D DP; '*' is the tricky case.",
 ["dp[i][j] = s[0..i) matches p[0..j). '?' or an equal letter consumes one of each. '*' either matches nothing (dp[i][j−1]) or one more character of s (dp[i−1][j])."],
 ["dp[0][0] = true; dp[0][j] = dp[0][j−1] while p[j−1] is '*'", "Fill row by row with the three cases", "Answer dp[n][m]"],
 """class Solution {
public:
    bool isMatch(string s, string p) {
        int n = s.size(), m = p.size(); vector<vector<char>> dp(n + 1, vector<char>(m + 1, 0)); dp[0][0] = 1;
        for (int j = 1; j <= m; j++) dp[0][j] = p[j - 1] == '*' && dp[0][j - 1];
        for (int i = 1; i <= n; i++)
            for (int j = 1; j <= m; j++) {
                if (p[j - 1] == '*') dp[i][j] = dp[i][j - 1] || dp[i - 1][j];
                else dp[i][j] = (p[j - 1] == '?' || p[j - 1] == s[i - 1]) && dp[i - 1][j - 1];
            }
        return dp[n][m];
    }
};""",
 """Solution S; assert(!S.isMatch("aa", "a") && S.isMatch("aa", "*") && !S.isMatch("cb", "?a") && S.isMatch("adceb", "*a*b") && !S.isMatch("acdcb", "a*c?b") && S.isMatch("", "***"));""",
 "O(nm) time, O(nm) space (O(m) with one row)", ["Forgetting the leading-stars row (pattern '***' matches an empty string)"],
 ["Greedy two-pointer solution with backtracking to the last '*' runs in O(nm) worst case but O(1) space.", "Compare with Regular Expression Matching, where '*' repeats the previous character."])

add("shortest-palindrome", "Shortest Palindrome", "shortest-palindrome", 3, "String algorithms", "KMP prefix function in disguise.",
 ["Add the fewest characters in front: find the longest prefix of s that is a palindrome. Build t = s + '#' + reverse(s); the KMP prefix function at the end of t is that length. Prepend the reverse of the rest."],
 ["t = s + '#' + rev", "Compute the prefix (failure) function of t", "k = pi.back(); return reverse(s.substr(k)) + s"],
 """class Solution {
public:
    string shortestPalindrome(string s) {
        string r(s.rbegin(), s.rend()), t = s + "#" + r; vector<int> pi(t.size(), 0);
        for (size_t i = 1; i < t.size(); i++) {
            int k = pi[i - 1];
            while (k > 0 && t[i] != t[k]) k = pi[k - 1];
            if (t[i] == t[k]) k++;
            pi[i] = k;
        }
        return r.substr(0, s.size() - pi.back()) + s;
    }
};""",
 """Solution S; assert(S.shortestPalindrome("aacecaaa") == "aaacecaaa" && S.shortestPalindrome("abcd") == "dcbabcd" && S.shortestPalindrome("") == "" && S.shortestPalindrome("aba") == "aba");""",
 "O(n) time and space", ["Without the '#', the match can run past the middle"], ["Brute force checks each prefix for being a palindrome in O(n²).", "Explain the prefix function in one sentence."])

add("concat-words", "Substring with Concatenation of All Words", "substring-with-concatenation-of-all-words", 3, "Sliding window", "Counting window over equal-length words.",
 ["All words have the same length L. For each start offset 0..L−1, slide a window word by word, keeping counts; shrink from the left when a word is over-used; record the start when the window holds exactly all words."],
 ["need = counts of words", "For off in 0..L−1: left = off, seen = {}, cnt = 0", "Take the next word; if unknown reset; else add and shrink while over-used; if cnt == k record left"],
 """class Solution {
public:
    vector<int> findSubstring(string s, vector<string>& words) {
        vector<int> r; if (words.empty()) return r;
        int L = words[0].size(), k = words.size(), n = s.size(); unordered_map<string, int> need;
        for (auto& w : words) need[w]++;
        for (int off = 0; off < L; off++) {
            unordered_map<string, int> seen; int left = off, cnt = 0;
            for (int j = off; j + L <= n; j += L) {
                string w = s.substr(j, L);
                if (!need.count(w)) { seen.clear(); cnt = 0; left = j + L; continue; }
                seen[w]++; cnt++;
                while (seen[w] > need[w]) { seen[s.substr(left, L)]--; cnt--; left += L; }
                if (cnt == k) { r.push_back(left); seen[s.substr(left, L)]--; cnt--; left += L; }
            }
        }
        sort(r.begin(), r.end()); return r;
    }
};""",
 """Solution S; vector<string> a{"foo","bar"}, b{"word","good","best","word"}, c{"bar","foo","the"};
assert((S.findSubstring("barfoothefoobarman", a) == vector<int>{0,9}) && S.findSubstring("wordgoodgoodgoodbestword", b).empty());
assert((S.findSubstring("barfoofoobarthefoobarman", c) == vector<int>{6,9,12}));""",
 "O(n · L) time, O(k) space", ["Duplicate words in the list (use counts, not a set)", "Resetting the window on an unknown word"], ["Simpler O(n · k · L): check every start independently."])

add("word-break-ii", "Word Break II", "word-break-ii", 3, "Backtracking", "Word Break with all answers: memoise by start index.",
 ["From position i, try every dictionary word that matches s at i and recurse on the rest; cache the list of sentences for each i so each suffix is solved once."],
 ["memo[i] = all sentences for s[i..]", "Base: i == n gives one empty sentence", "Join word + ' ' + rest"],
 """class Solution {
    unordered_map<int, vector<string>> memo; unordered_set<string> dict; string s;
    vector<string> go(int i) {
        if (i == (int)s.size()) return {""};
        auto it = memo.find(i); if (it != memo.end()) return it->second;
        vector<string> out;
        for (int j = i + 1; j <= (int)s.size(); j++) {
            string w = s.substr(i, j - i);
            if (!dict.count(w)) continue;
            for (auto& rest : go(j)) out.push_back(rest.empty() ? w : w + " " + rest);
        }
        return memo[i] = out;
    }
public:
    vector<string> wordBreak(string str, vector<string>& words) {
        s = str; dict = unordered_set<string>(words.begin(), words.end()); memo.clear();
        auto r = go(0); sort(r.begin(), r.end()); return r;
    }
};""",
 """Solution S; vector<string> a{"cat","cats","and","sand","dog"}, b{"apple","pen","applepen","pine","pineapple"};
assert((S.wordBreak("catsanddog", a) == vector<string>{"cat sand dog","cats and dog"}));
assert((S.wordBreak("pineapplepenapple", b) == vector<string>{"pine apple pen apple","pine applepen apple","pineapple pen apple"}) && S.wordBreak("catsandog", a).empty());""",
 "Exponential output in the worst case; memo avoids recomputing suffixes", ["Inputs like 'aaaa…b' with words a, aa, aaa: first check Word Break I to fail fast"], ["Return only the count of sentences (a 1D DP)."])

add("remove-invalid-parens", "Remove Invalid Parentheses", "remove-invalid-parentheses", 3, "BFS", "BFS by number of removals.",
 ["Level k of a BFS holds strings with k characters removed. The first level that contains valid strings gives all answers with the minimum removals; stop there."],
 ["Queue with s, visited set", "If any string in the level is valid, collect all valid ones and stop", "Otherwise remove each '(' or ')' once to form the next level"],
 """class Solution {
    bool valid(const string& s) { int b = 0; for (char c : s) { if (c == '(') b++; else if (c == ')' && --b < 0) return false; } return b == 0; }
public:
    vector<string> removeInvalidParentheses(string s) {
        vector<string> level{s}; unordered_set<string> seen{s};
        while (true) {
            vector<string> ok;
            for (auto& t : level) if (valid(t)) ok.push_back(t);
            if (!ok.empty()) { sort(ok.begin(), ok.end()); return ok; }
            vector<string> next;
            for (auto& t : level)
                for (size_t i = 0; i < t.size(); i++)
                    if (t[i] == '(' || t[i] == ')') { string u = t.substr(0, i) + t.substr(i + 1); if (seen.insert(u).second) next.push_back(u); }
            level = next;
        }
    }
};""",
 """Solution S; assert((S.removeInvalidParentheses("()())()") == vector<string>{"(())()","()()()"}) && (S.removeInvalidParentheses("(a)())()") == vector<string>{"(a())()","(a)()()"}) && (S.removeInvalidParentheses(")(") == vector<string>{""}));""",
 "Exponential in the worst case; the visited set prunes duplicates", ["Continuing past the first valid level (gives non-minimal answers)"], ["DFS with counts of extra '(' and ')' to remove is faster in practice."])

add("int-to-english", "Integer to English Words", "integer-to-english-words", 3, "Simulation", "Careful case handling under time pressure.",
 ["Split into groups of three digits (units, thousand, million, billion). Each group under 1000 is spoken the same way: hundreds, then tens (with 10–19 special), then ones."],
 ["Tables for 1–19 and tens", "helper(n < 1000)", "Walk groups from billions down; skip zero groups; 0 is 'Zero'"],
 """class Solution {
    vector<string> lo{"", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen"};
    vector<string> tens{"", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"};
    string three(int n) {
        string r;
        if (n >= 100) { r = lo[n / 100] + " Hundred"; n %= 100; }
        if (n >= 20) { r += (r.empty() ? "" : " ") + tens[n / 10]; n %= 10; }
        if (n > 0) r += (r.empty() ? "" : " ") + lo[n];
        return r;
    }
public:
    string numberToWords(int num) {
        if (num == 0) return "Zero";
        vector<pair<int, string>> g{{1000000000, "Billion"}, {1000000, "Million"}, {1000, "Thousand"}, {1, ""}}; string r;
        for (auto& [v, name] : g)
            if (num >= v) { string part = three(num / v) + (name.empty() ? "" : " " + name); r += (r.empty() ? "" : " ") + part; num %= v; }
        return r;
    }
};""",
 """Solution S; assert(S.numberToWords(123) == "One Hundred Twenty Three" && S.numberToWords(12345) == "Twelve Thousand Three Hundred Forty Five");
assert(S.numberToWords(1234567) == "One Million Two Hundred Thirty Four Thousand Five Hundred Sixty Seven" && S.numberToWords(0) == "Zero" && S.numberToWords(1000010) == "One Million Ten");""",
 "O(1) (at most 10 digits)", ["Extra spaces around empty parts", "Numbers like 1,000,010 with zero groups in the middle"], ["Indian numbering (lakh, crore) instead: groups of 3 then 2 digits."])

# ---------------- DP
add("dungeon", "Dungeon Game", "dungeon-game", 3, "Grid DP", "DP that must run backwards.",
 ["need[i][j] = minimum health when entering cell (i, j) to survive to the end. From the bottom-right: need = max(1, min(need right, need down) − dungeon[i][j])."],
 ["Pad with INT_MAX borders; need[n][m−1] = need[n−1][m] = 1", "Fill from bottom-right to top-left", "Answer need[0][0]"],
 """class Solution {
public:
    int calculateMinimumHP(vector<vector<int>>& d) {
        int n = d.size(), m = d[0].size(); vector<vector<int>> need(n + 1, vector<int>(m + 1, INT_MAX));
        need[n][m - 1] = need[n - 1][m] = 1;
        for (int i = n - 1; i >= 0; i--)
            for (int j = m - 1; j >= 0; j--)
                need[i][j] = max(1, min(need[i + 1][j], need[i][j + 1]) - d[i][j]);
        return need[0][0];
    }
};""",
 """vector<vector<int>> a{{-2,-3,3},{-5,-10,1},{10,30,-5}}, b{{0}}, c{{100}}; Solution S; assert(S.calculateMinimumHP(a) == 7 && S.calculateMinimumHP(b) == 1 && S.calculateMinimumHP(c) == 1);""",
 "O(nm) time and space", ["Going top-left to bottom-right (needs two quantities, does not work)", "Health must stay at least 1"], ["Why does a forward DP fail? (A path's best end health and minimum need conflict.)"])

add("stock-iii", "Best Time to Buy and Sell Stock III", "best-time-to-buy-and-sell-stock-iii", 3, "Stock DP", "State machine with two transactions.",
 ["Track four states: after first buy, first sell, second buy, second sell. Each day update them in order; the second buy uses the profit from the first sell."],
 ["b1 = max(b1, −p); s1 = max(s1, b1 + p)", "b2 = max(b2, s1 − p); s2 = max(s2, b2 + p)", "Answer s2"],
 """class Solution {
public:
    int maxProfit(vector<int>& p) {
        int b1 = INT_MIN, s1 = 0, b2 = INT_MIN, s2 = 0;
        for (int x : p) { b1 = max(b1, -x); s1 = max(s1, b1 + x); b2 = max(b2, s1 - x); s2 = max(s2, b2 + x); }
        return s2;
    }
};""",
 """vector<int> a{3,3,5,0,0,3,1,4}, b{1,2,3,4,5}, c{7,6,4,3,1}; Solution S; assert(S.maxProfit(a) == 6 && S.maxProfit(b) == 4 && S.maxProfit(c) == 0);""",
 "O(n) time, O(1) space", ["Updating with yesterday's values is not needed here: same-day buy and sell adds nothing"], ["At most k transactions: Stock IV.", "Prefix best and suffix best arrays give another O(n) solution."])

add("stock-iv", "Best Time to Buy and Sell Stock IV", "best-time-to-buy-and-sell-stock-iv", 3, "Stock DP", "Generalise the state machine to k.",
 ["buy[j], sell[j] for the j-th transaction, j = 1..k. If k ≥ n/2, the limit does not bind: sum every positive day-to-day rise."],
 ["If 2k ≥ n: greedy sum of rises", "Else for each price, for j = 1..k: buy[j] = max(buy[j], sell[j−1] − p); sell[j] = max(sell[j], buy[j] + p)", "Answer sell[k]"],
 """class Solution {
public:
    int maxProfit(int k, vector<int>& p) {
        int n = p.size();
        if (2 * k >= n) { int s = 0; for (int i = 1; i < n; i++) s += max(0, p[i] - p[i - 1]); return s; }
        vector<int> buy(k + 1, INT_MIN), sell(k + 1, 0);
        for (int x : p)
            for (int j = 1; j <= k; j++) { buy[j] = max(buy[j], sell[j - 1] - x); sell[j] = max(sell[j], buy[j] + x); }
        return sell[k];
    }
};""",
 """vector<int> a{2,4,1}, b{3,2,6,5,0,3}, c{1,2,4,2,5,7,2,4,9,0}; Solution S; assert(S.maxProfit(2, a) == 2 && S.maxProfit(2, b) == 7 && S.maxProfit(4, c) == 15 && S.maxProfit(2, c) == 13);""",
 "O(nk) time, O(k) space", ["Huge k without the greedy shortcut (time and memory)"], ["With a cooldown or a fee: change the transitions."])

add("frog-jump", "Frog Jump", "frog-jump", 3, "DP", "DP over (stone, last jump).",
 ["For each stone keep the set of jump sizes that can land on it. From a stone reached with jump k, try k − 1, k, k + 1 (positive) to stones that exist."],
 ["map<stone, set<jump>>; stones[0] gets {0}", "For each stone in order, for each k in its set, for d in k−1..k+1 with d > 0: add d to stone + d if it exists", "Answer: last stone's set not empty"],
 """class Solution {
public:
    bool canCross(vector<int>& stones) {
        unordered_map<int, unordered_set<int>> can; for (int s : stones) can[s];
        can[stones[0]].insert(0);
        for (int s : stones)
            for (int k : can[s])
                for (int d = k - 1; d <= k + 1; d++)
                    if (d > 0 && can.count(s + d)) can[s + d].insert(d);
        return !can[stones.back()].empty();
    }
};""",
 """vector<int> a{0,1,3,5,6,8,12,17}, b{0,1,2,3,4,8,9,11}, c{0,2}; Solution S; assert(S.canCross(a) && !S.canCross(b) && !S.canCross(c));""",
 "O(n²) time and space", ["Modifying a set while iterating it (only later stones are changed, so it is safe here)", "The first jump must be exactly 1"], ["Return the minimum number of jumps."])

add("russian-doll", "Russian Doll Envelopes", "russian-doll-envelopes", 3, "LIS", "2D LIS with a sorting trick.",
 ["Sort by width ascending and, for equal widths, height descending. Then the answer is the longest strictly increasing subsequence of heights (the descending tie-break stops two equal widths from nesting)."],
 ["Sort with the tie-break", "Patience LIS: lower_bound into tails", "Answer tails.size()"],
 """class Solution {
public:
    int maxEnvelopes(vector<vector<int>>& e) {
        sort(e.begin(), e.end(), [](const vector<int>& a, const vector<int>& b) { return a[0] != b[0] ? a[0] < b[0] : a[1] > b[1]; });
        vector<int> tails;
        for (auto& x : e) { auto it = lower_bound(tails.begin(), tails.end(), x[1]); if (it == tails.end()) tails.push_back(x[1]); else *it = x[1]; }
        return tails.size();
    }
};""",
 """vector<vector<int>> a{{5,4},{6,4},{6,7},{2,3}}, b{{1,1},{1,1},{1,1}}, c{{4,5},{4,6},{6,7},{2,3},{1,1}}; Solution S; assert(S.maxEnvelopes(a) == 3 && S.maxEnvelopes(b) == 1 && S.maxEnvelopes(c) == 4);""",
 "O(n log n) time, O(n) space", ["Ascending heights for equal widths (lets equal widths nest)"], ["Boxes in 3D: sort and an O(n²) DP."])

add("cherry-pickup-ii", "Cherry Pickup II", "cherry-pickup-ii", 3, "Grid DP", "Two walkers at once.",
 ["Both robots move down one row each step, so the state is (row, col1, col2). dp = cherries collected from this row down; count a shared cell once; try the 9 move pairs."],
 ["dp over rows from the bottom", "cur[c1][c2] = grid[r][c1] + (c1 != c2 ? grid[r][c2] : 0) + best of 9 next pairs", "Answer dp[0][0][m−1]"],
 """class Solution {
public:
    int cherryPickup(vector<vector<int>>& g) {
        int n = g.size(), m = g[0].size(); vector<vector<int>> nxt(m, vector<int>(m, 0)), cur(m, vector<int>(m, 0));
        for (int r = n - 1; r >= 0; r--) {
            for (int a = 0; a < m; a++)
                for (int b = 0; b < m; b++) {
                    int best = 0;
                    if (r + 1 < n)
                        for (int da = -1; da <= 1; da++) for (int db = -1; db <= 1; db++) {
                            int x = a + da, y = b + db;
                            if (x >= 0 && y >= 0 && x < m && y < m) best = max(best, nxt[x][y]);
                        }
                    cur[a][b] = g[r][a] + (a != b ? g[r][b] : 0) + best;
                }
            swap(cur, nxt);
        }
        return nxt[0][m - 1];
    }
};""",
 """vector<vector<int>> a{{3,1,1},{2,5,1},{1,5,5},{2,1,1}}, b{{1,0,0,0,0,0,1},{2,0,0,0,0,3,0},{2,0,9,0,0,0,0},{0,3,0,5,4,0,0},{1,0,2,3,0,0,6}};
Solution S; assert(S.cherryPickup(a) == 24 && S.cherryPickup(b) == 28);""",
 "O(n · m² · 9) time, O(m²) space", ["Counting a cell twice when both robots stand on it"], ["Cherry Pickup I: one walker goes there and back (model as two walkers moving together)."])

add("strange-printer", "Strange Printer", "strange-printer", 3, "Interval DP", "Interval DP with a merge on equal ends.",
 ["dp[i][j] = turns to print s[i..j]. Start with dp[i+1][j] + 1 (print s[i] alone); for every k in (i, j] with s[k] == s[i], print them in one stroke: dp[i+1][k−1] + dp[k][j]."],
 ["Length 1 costs 1", "Fill by increasing length", "Answer dp[0][n−1]"],
 """class Solution {
public:
    int strangePrinter(string s) {
        int n = s.size(); vector<vector<int>> dp(n + 1, vector<int>(n + 1, 0));
        for (int i = n - 1; i >= 0; i--)
            for (int j = i; j < n; j++) {
                dp[i][j] = 1 + (i + 1 <= j ? dp[i + 1][j] : 0);
                for (int k = i + 1; k <= j; k++)
                    if (s[k] == s[i]) dp[i][j] = min(dp[i][j], (i + 1 <= k - 1 ? dp[i + 1][k - 1] : 0) + dp[k][j]);
            }
        return dp[0][n - 1];
    }
};""",
 """Solution S; assert(S.strangePrinter("aaabbb") == 2 && S.strangePrinter("aba") == 2 && S.strangePrinter("abcabc") == 5 && S.strangePrinter("a") == 1);""",
 "O(n³) time, O(n²) space", ["Off-by-one on empty inner intervals"], ["Removing consecutive duplicates first shrinks n without changing the answer."])

add("digit-one", "Number of Digit One", "number-of-digit-one", 3, "Digit DP", "Count by position.",
 ["Count how often 1 appears at each decimal position. For position value p, split n into high = n / (10p), cur = (n / p) % 10, low = n % p: ones = high·p + (cur > 1 ? p : cur == 1 ? low + 1 : 0)."],
 ["Loop p = 1, 10, 100, … while p ≤ n", "Add the formula for each position", "Use long long for p"],
 """class Solution {
public:
    int countDigitOne(int n) {
        long long total = 0;
        for (long long p = 1; p <= n; p *= 10) {
            long long high = n / (p * 10), cur = (n / p) % 10, low = n % p;
            total += high * p + (cur > 1 ? p : cur == 1 ? low + 1 : 0);
        }
        return (int)total;
    }
};""",
 """Solution S; int brute = 0; for (int i = 1; i <= 2024; i++) for (int x = i; x; x /= 10) brute += x % 10 == 1;
assert(S.countDigitOne(13) == 6 && S.countDigitOne(0) == 0 && S.countDigitOne(100) == 21 && S.countDigitOne(2024) == brute);""",
 "O(log n) time, O(1) space", ["Overflow of p near INT_MAX (use long long)"], ["Count any digit d (careful with 0 and leading zeros)."])

# ---------------- Stack, geometry, heaps
add("basic-calculator", "Basic Calculator", "basic-calculator", 3, "Stack", "Parentheses with + and − only.",
 ["Keep a running result and a sign. On '(' push the current result and sign and start fresh; on ')' pop and combine: result = saved + savedSign × result."],
 ["Parse numbers digit by digit", "'+'/'−' add the pending number with the sign, set the new sign", "'(' push (result, sign); ')' finish the number, then combine with the popped pair"],
 """class Solution {
public:
    int calculate(string s) {
        long long res = 0, num = 0; int sign = 1; stack<pair<long long, int>> st;
        for (char c : s) {
            if (isdigit(c)) num = num * 10 + (c - '0');
            else if (c == '+' || c == '-') { res += sign * num; num = 0; sign = c == '+' ? 1 : -1; }
            else if (c == '(') { st.push({res, sign}); res = 0; sign = 1; }
            else if (c == ')') { res += sign * num; num = 0; auto [r, sg] = st.top(); st.pop(); res = r + sg * res; }
        }
        return (int)(res + sign * num);
    }
};""",
 """Solution S; assert(S.calculate("1 + 1") == 2 && S.calculate(" 2-1 + 2 ") == 3 && S.calculate("(1+(4+5+2)-3)+(6+8)") == 23 && S.calculate("-(2+3)") == -5 && S.calculate("1-(-2)") == 3);""",
 "O(n) time, O(n) stack", ["Unary minus at the start or after '('", "Forgetting the last number after the loop"], ["Add * and / (Basic Calculator III): recursion per parenthesis level."])

add("max-points", "Max Points on a Line", "max-points-on-a-line", 3, "Geometry and hashing", "Exact slopes, not doubles.",
 ["For each point, count the other points by normalised direction (dx, dy) divided by their gcd with a fixed sign. The biggest count + 1 is the best line through that point."],
 ["For i: map<pair<int,int>, int>", "dx, dy; g = gcd; normalise sign so dx > 0, or dx == 0 and dy > 0", "best = max(best, count + 1)"],
 """class Solution {
public:
    int maxPoints(vector<vector<int>>& p) {
        int n = p.size(), best = min(n, 1);
        for (int i = 0; i < n; i++) {
            map<pair<int, int>, int> cnt;
            for (int j = i + 1; j < n; j++) {
                int dx = p[j][0] - p[i][0], dy = p[j][1] - p[i][1], g = gcd(dx, dy);
                dx /= g; dy /= g;
                if (dx < 0 || (dx == 0 && dy < 0)) { dx = -dx; dy = -dy; }
                best = max(best, ++cnt[{dx, dy}] + 1);
            }
        }
        return best;
    }
};""",
 """vector<vector<int>> a{{1,1},{2,2},{3,3}}, b{{1,1},{3,2},{5,3},{4,1},{2,3},{1,4}}, c{{0,0}}; Solution S; assert(S.maxPoints(a) == 3 && S.maxPoints(b) == 4 && S.maxPoints(c) == 1);""",
 "O(n² log n) time, O(n) space", ["Floating-point slopes (precision errors)", "Vertical lines (dx = 0)"], ["Duplicate points: count them separately and add to every line."])

add("skyline", "The Skyline Problem", "the-skyline-problem", 3, "Heap", "Sweep line with a multiset of heights.",
 ["Make events: a start (x, −h) and an end (x, +h); sort so starts come before ends and taller starts first. Keep a multiset of active heights (with 0). When the maximum changes, emit a key point."],
 ["Events sorted", "Start: insert h; end: erase one h", "If max height changed, push (x, max)"],
 """class Solution {
public:
    vector<vector<int>> getSkyline(vector<vector<int>>& b) {
        vector<pair<int, int>> ev;
        for (auto& x : b) { ev.push_back({x[0], -x[2]}); ev.push_back({x[1], x[2]}); }
        sort(ev.begin(), ev.end());
        multiset<int> h{0}; int prev = 0; vector<vector<int>> r;
        for (auto [x, y] : ev) {
            if (y < 0) h.insert(-y); else h.erase(h.find(y));
            int cur = *h.rbegin();
            if (cur != prev) { r.push_back({x, cur}); prev = cur; }
        }
        return r;
    }
};""",
 """vector<vector<int>> a{{2,9,10},{3,7,15},{5,12,12},{15,20,10},{19,24,8}}, b{{0,2,3},{2,5,3}}; Solution S;
assert((S.getSkyline(a) == vector<vector<int>>{{2,10},{3,15},{7,12},{12,0},{15,10},{20,8},{24,0}}) && (S.getSkyline(b) == vector<vector<int>>{{0,3},{5,0}}));""",
 "O(n log n) time, O(n) space", ["erase(value) removes every copy; erase one with find", "Two buildings touching at the same height must not create a dip"], ["Divide and conquer merge, like merge sort."])

add("course-schedule-iii", "Course Schedule III", "course-schedule-iii", 3, "Greedy", "Exchange argument with a max-heap.",
 ["Take courses in order of deadline. Add each one; if the total time passes its deadline, drop the longest course taken so far (it frees the most time and keeps the count)."],
 ["Sort by deadline", "Push duration; time += d", "If time > deadline: time −= top; pop"],
 """class Solution {
public:
    int scheduleCourse(vector<vector<int>>& c) {
        sort(c.begin(), c.end(), [](const vector<int>& a, const vector<int>& b) { return a[1] < b[1]; });
        priority_queue<int> pq; int t = 0;
        for (auto& x : c) { pq.push(x[0]); t += x[0]; if (t > x[1]) { t -= pq.top(); pq.pop(); } }
        return pq.size();
    }
};""",
 """vector<vector<int>> a{{100,200},{200,1300},{1000,1250},{2000,3200}}, b{{1,2}}, c{{3,2},{4,3}}; Solution S; assert(S.scheduleCourse(a) == 3 && S.scheduleCourse(b) == 1 && S.scheduleCourse(c) == 0);""",
 "O(n log n) time, O(n) space", ["Sorting by duration instead of deadline"], ["Prove the swap: replacing a longer course by a shorter one never hurts later choices."])

add("hire-workers", "Minimum Cost to Hire K Workers", "minimum-cost-to-hire-k-workers", 3, "Heap", "Sort by ratio, keep smallest qualities.",
 ["In a group everyone is paid at the highest wage/quality ratio in it. Sort by ratio; for each worker as the captain (highest ratio so far), pay ratio × (sum of the k smallest qualities seen). Keep those with a max-heap."],
 ["Sort by wage/quality", "Push quality, sum += q; if size > k pop the largest", "When size == k: best = min(best, sum × ratio)"],
 """class Solution {
public:
    double mincostToHireWorkers(vector<int>& q, vector<int>& w, int k) {
        int n = q.size(); vector<pair<double, int>> v;
        for (int i = 0; i < n; i++) v.push_back({(double)w[i] / q[i], q[i]});
        sort(v.begin(), v.end());
        priority_queue<int> pq; long long sum = 0; double best = 1e18;
        for (auto [r, qq] : v) {
            pq.push(qq); sum += qq;
            if ((int)pq.size() > k) { sum -= pq.top(); pq.pop(); }
            if ((int)pq.size() == k) best = min(best, sum * r);
        }
        return best;
    }
};""",
 """vector<int> q1{10,20,5}, w1{70,50,30}, q2{3,1,10,10,1}, w2{4,8,2,2,7}; Solution S;
assert(fabs(S.mincostToHireWorkers(q1, w1, 2) - 105.0) < 1e-6 && fabs(S.mincostToHireWorkers(q2, w2, 3) - 30.666666667) < 1e-6);""",
 "O(n log n) time, O(n) space", ["Integer division for the ratio"], ["Why the captain must be the highest ratio in the group."])

# ---------------- Graphs, divide and conquer, binary search
add("word-search-ii", "Word Search II", "word-search-ii", 3, "Trie + backtracking", "Search all words at once with a trie.",
 ["Insert every word into a trie. DFS from each cell, walking the trie as you move; when a node ends a word, record it and clear the marker so it is reported once."],
 ["Build the trie with a word pointer at terminal nodes", "DFS(r, c, node): mark the cell, try 4 neighbours, unmark", "Prune: stop when the trie has no child for the letter"],
 """class Solution {
    struct Node { Node* nx[26] = {}; string* word = nullptr; };
    vector<Node> pool; vector<string> out;
    void dfs(vector<vector<char>>& b, int r, int c, Node* n) {
        char ch = b[r][c]; if (ch == '#' || !n->nx[ch - 'a']) return;
        n = n->nx[ch - 'a'];
        if (n->word) { out.push_back(*n->word); n->word = nullptr; }
        b[r][c] = '#';
        int dr[] = {1, -1, 0, 0}, dc[] = {0, 0, 1, -1};
        for (int k = 0; k < 4; k++) { int nr = r + dr[k], nc = c + dc[k]; if (nr >= 0 && nc >= 0 && nr < (int)b.size() && nc < (int)b[0].size()) dfs(b, nr, nc, n); }
        b[r][c] = ch;
    }
public:
    vector<string> findWords(vector<vector<char>>& b, vector<string>& words) {
        size_t total = 1; for (auto& w : words) total += w.size();
        pool.assign(total, Node()); size_t used = 1; Node* root = &pool[0];
        for (auto& w : words) { Node* n = root; for (char ch : w) { if (!n->nx[ch - 'a']) n->nx[ch - 'a'] = &pool[used++]; n = n->nx[ch - 'a']; } n->word = &w; }
        out.clear();
        for (int r = 0; r < (int)b.size(); r++) for (int c = 0; c < (int)b[0].size(); c++) dfs(b, r, c, root);
        sort(out.begin(), out.end()); return out;
    }
};""",
 """vector<vector<char>> b{{'o','a','a','n'},{'e','t','a','e'},{'i','h','k','r'},{'i','f','l','v'}}, c{{'a','b'},{'c','d'}};
vector<string> w{"oath","pea","eat","rain"}, w2{"abcb"}; Solution S;
assert((S.findWords(b, w) == vector<string>{"eat","oath"}) && S.findWords(c, w2).empty());""",
 "O(cells · 4 · 3^(L−1)) worst case; the trie shares prefixes", ["Reporting a word twice (clear the marker)", "Reusing a cell in one word (mark it while on the path)"], ["Prune trie nodes whose subtree has no words left."])

add("large-island", "Making A Large Island", "making-a-large-island", 3, "Union-Find", "Label islands, then try each water cell.",
 ["Label each island with an id and record its size. For each 0, add 1 + the sizes of the distinct islands around it. If there is no 0, the answer is the whole grid."],
 ["DFS/BFS labelling with ids from 2", "size[id]", "For each 0: set of neighbour ids, sum sizes + 1"],
 """class Solution {
public:
    int largestIsland(vector<vector<int>>& g) {
        int n = g.size(), id = 2, best = 0; vector<int> sz(2, 0);
        int dr[] = {1, -1, 0, 0}, dc[] = {0, 0, 1, -1};
        for (int r = 0; r < n; r++) for (int c = 0; c < n; c++) if (g[r][c] == 1) {
            int cnt = 0; vector<pair<int, int>> st{{r, c}}; g[r][c] = id;
            while (!st.empty()) {
                auto [x, y] = st.back(); st.pop_back(); cnt++;
                for (int k = 0; k < 4; k++) { int a = x + dr[k], b = y + dc[k]; if (a >= 0 && b >= 0 && a < n && b < n && g[a][b] == 1) { g[a][b] = id; st.push_back({a, b}); } }
            }
            sz.push_back(cnt); best = max(best, cnt); id++;
        }
        for (int r = 0; r < n; r++) for (int c = 0; c < n; c++) if (g[r][c] == 0) {
            set<int> ids; for (int k = 0; k < 4; k++) { int a = r + dr[k], b = c + dc[k]; if (a >= 0 && b >= 0 && a < n && b < n && g[a][b] > 1) ids.insert(g[a][b]); }
            int s = 1; for (int x : ids) s += sz[x]; best = max(best, s);
        }
        return best;
    }
};""",
 """vector<vector<int>> a{{1,0},{0,1}}, b{{1,1},{1,0}}, c{{1,1},{1,1}}, d{{0,0},{0,0}}; Solution S; assert(S.largestIsland(a) == 3 && S.largestIsland(b) == 4 && S.largestIsland(c) == 4 && S.largestIsland(d) == 1);""",
 "O(n²) time and space", ["Counting the same island twice when it touches the cell on two sides (use a set)"], ["Union-Find gives the same result without labels."])

add("bus-routes", "Bus Routes", "bus-routes", 3, "BFS", "BFS over buses, not stops.",
 ["Map each stop to the buses that serve it. BFS where one level is one more bus: from the current stops, take every unused bus and add all its stops."],
 ["If source == target: 0", "stop → buses map", "Level by level; mark buses and stops used"],
 """class Solution {
public:
    int numBusesToDestination(vector<vector<int>>& routes, int s, int t) {
        if (s == t) return 0;
        unordered_map<int, vector<int>> at; for (int i = 0; i < (int)routes.size(); i++) for (int x : routes[i]) at[x].push_back(i);
        vector<bool> usedBus(routes.size()); unordered_set<int> seen{s}; queue<int> q; q.push(s);
        for (int buses = 1; !q.empty(); buses++)
            for (int n = q.size(); n--; ) {
                int stop = q.front(); q.pop();
                for (int b : at[stop]) {
                    if (usedBus[b]) continue;
                    usedBus[b] = true;
                    for (int x : routes[b]) { if (x == t) return buses; if (seen.insert(x).second) q.push(x); }
                }
            }
        return -1;
    }
};""",
 """vector<vector<int>> a{{1,2,7},{3,6,7}}, b{{7,12},{4,5,15},{6},{15,19},{9,12,13}}; Solution S;
assert(S.numBusesToDestination(a, 1, 6) == 2 && S.numBusesToDestination(b, 15, 12) == -1 && S.numBusesToDestination(a, 3, 3) == 0);""",
 "O(total stops) time and space", ["BFS over stops with every pair edge (quadratic in route length)"], ["Return the actual sequence of buses."])

add("visit-all-nodes", "Shortest Path Visiting All Nodes", "shortest-path-visiting-all-nodes", 3, "Bitmask BFS", "BFS over (node, visited set).",
 ["State = (node, mask of visited nodes). Start from every node at once with its own bit set. BFS; the first state whose mask is full gives the answer."],
 ["Queue all (i, 1 << i)", "seen[mask][node]", "Expand to neighbours with mask | 1 << nb"],
 """class Solution {
public:
    int shortestPathLength(vector<vector<int>>& g) {
        int n = g.size(), full = (1 << n) - 1; vector<vector<bool>> seen(1 << n, vector<bool>(n));
        queue<pair<int, int>> q; for (int i = 0; i < n; i++) { q.push({i, 1 << i}); seen[1 << i][i] = true; }
        for (int d = 0; !q.empty(); d++)
            for (int k = q.size(); k--; ) {
                auto [u, m] = q.front(); q.pop();
                if (m == full) return d;
                for (int v : g[u]) { int nm = m | 1 << v; if (!seen[nm][v]) { seen[nm][v] = true; q.push({v, nm}); } }
            }
        return -1;
    }
};""",
 """vector<vector<int>> a{{1,2,3},{0},{0},{0}}, b{{1},{0,2,4},{1,3,4},{2},{1,2}}, c{{}}; Solution S; assert(S.shortestPathLength(a) == 4 && S.shortestPathLength(b) == 4 && S.shortestPathLength(c) == 0);""",
 "O(2ⁿ · n²) time, O(2ⁿ · n) space", ["Starting from node 0 only (the best start may be elsewhere)"], ["Relation to the travelling salesman DP (Held–Karp)."])

add("range-sum-count", "Count of Range Sum", "count-of-range-sum", 3, "Divide and conquer", "Merge sort on prefix sums.",
 ["Count pairs i < j of prefix sums with lower ≤ P[j] − P[i] ≤ upper. In merge sort, both halves are sorted, so for each left element two moving pointers find the valid range in the right half."],
 ["P[0] = 0, P[i+1] = P[i] + a[i] (long long)", "sort(lo, hi): recurse, then count with two pointers, then merge", "Answer the total count"],
 """class Solution {
    long long lo_, hi_;
    long long go(vector<long long>& p, int l, int r) {            // [l, r)
        if (r - l <= 1) return 0;
        int m = (l + r) / 2; long long cnt = go(p, l, m) + go(p, m, r);
        int a = m, b = m;
        for (int i = l; i < m; i++) {
            while (a < r && p[a] - p[i] < lo_) a++;
            while (b < r && p[b] - p[i] <= hi_) b++;
            cnt += b - a;
        }
        inplace_merge(p.begin() + l, p.begin() + m, p.begin() + r);
        return cnt;
    }
public:
    int countRangeSum(vector<int>& a, int lower, int upper) {
        lo_ = lower; hi_ = upper; vector<long long> p(a.size() + 1, 0);
        for (size_t i = 0; i < a.size(); i++) p[i + 1] = p[i] + a[i];
        return (int)go(p, 0, p.size());
    }
};""",
 """vector<int> a{-2,5,-1}, b{0}, c{2147483647,-2147483648,-1,0}; Solution S; assert(S.countRangeSum(a, -2, 2) == 3 && S.countRangeSum(b, 0, 0) == 1 && S.countRangeSum(c, -1, 0) == 4);""",
 "O(n log n) time, O(n) space", ["int overflow in prefix sums (the third test)"], ["A Fenwick tree over compressed prefix sums also works."])

add("kth-pair-distance", "Find K-th Smallest Pair Distance", "find-k-th-smallest-pair-distance", 3, "Binary search on the answer", "Count pairs ≤ d with two pointers.",
 ["Sort. Binary search the distance d; for a given d, count pairs with difference ≤ d using a sliding left pointer. The smallest d with count ≥ k is the answer."],
 ["Sort", "lo = 0, hi = max − min", "count(d): for r, move l while a[r] − a[l] > d; add r − l"],
 """class Solution {
public:
    int smallestDistancePair(vector<int>& a, int k) {
        sort(a.begin(), a.end()); int lo = 0, hi = a.back() - a[0];
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2; long long cnt = 0;
            for (int l = 0, r = 0; r < (int)a.size(); r++) { while (a[r] - a[l] > mid) l++; cnt += r - l; }
            if (cnt >= k) hi = mid; else lo = mid + 1;
        }
        return lo;
    }
};""",
 """vector<int> a{1,3,1}, b{1,1,1}, c{1,6,1}, d{62,100,4}; Solution S; assert(S.smallestDistancePair(a, 1) == 0 && S.smallestDistancePair(b, 2) == 0 && S.smallestDistancePair(c, 3) == 5 && S.smallestDistancePair(d, 2) == 58);""",
 "O(n log n + n log W) time, O(1) extra space", ["Counting with int (n² pairs can overflow)"], ["K-th smallest element in a sorted matrix uses the same idea."])
