"""Worked solutions for the most-asked interview problems. Each `code` is a LeetCode-style class; each `test` runs in main() with asserts."""
LC = lambda slug: f"https://leetcode.com/problems/{slug}/"
P = []
def add(id, title, slug, lvl, pattern, where, idea, steps, code, test, cx, traps, follow):
    P.append(dict(id="p-" + id, title=title, cat="Problems", lvl={0: 1, 1: 2, 3: 3}[lvl], aka=[title],
        why=f"Pattern: {pattern}. {where}",
        core=idea, points=steps + [f"Complexity: {cx}"], code=code, test=test, pit=traps, ask=follow,
        prac=[(f"Solve it on LeetCode: {title}", LC(slug))], learn=[], rel=[pattern_rel[pattern]]))

pattern_rel = {"Hashing": "hashing", "Two pointers": "two-pointers", "Sliding window": "sliding-window", "Prefix sum": "prefix-sum",
 "Binary search": "binary-search", "Binary search on the answer": "bs-answer", "Stack": "stack-queue", "Monotonic stack": "monotonic-stack",
 "Linked list": "linked-list", "Heap": "heap", "Trees": "trees", "BST": "bst", "BFS": "bfs", "DFS": "dfs", "Topological sort": "topo-sort",
 "Dijkstra": "dijkstra", "DSU": "dsu", "DP": "dp", "Knapsack": "knapsack", "String DP": "lcs", "Backtracking": "recursion",
 "Intervals": "intervals", "Greedy": "greedy", "Trie": "trie", "Kadane": "dp"}

add("two-sum", "Two Sum", "two-sum", 0, "Hashing", "The most famous first-round question; asked everywhere as a warm-up.",
 ["Brute force checks every pair: O(n²). Instead, walk once and remember each value's index in a hash map. For each x, the partner you need is target − x; if it's already in the map, you're done.",
  "Check the map before inserting x, so an element is never paired with itself."],
 ["For i in 0..n−1: if target − a[i] is in the map, return [map[target − a[i]], i]", "Otherwise store a[i] → i"],
 """class Solution {
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
};""",
 """vector<int> a{2,7,11,15}; assert((Solution().twoSum(a, 9) == vector<int>{0,1}));
vector<int> b{3,3}; assert((Solution().twoSum(b, 6) == vector<int>{0,1}));
vector<int> c{3,2,4}; assert((Solution().twoSum(c, 6) == vector<int>{1,2}));""",
 "O(n) time, O(n) space", ["Inserting before checking (pairs x with itself)", "Returning values instead of indices"],
 ["What if the array is sorted? (two pointers, O(1) space)", "What if there can be many answers? Return all pairs without duplicates."])

add("stock", "Best Time to Buy and Sell Stock", "best-time-to-buy-and-sell-stock", 0, "Greedy", "Amazon and Microsoft favourite; leads into the stock DP family.",
 ["The best sale on day i uses the cheapest price before day i. Track the running minimum and the best difference."],
 ["minPrice = a[0]; best = 0", "For each price: best = max(best, price − minPrice); minPrice = min(minPrice, price)"],
 """class Solution {
public:
    int maxProfit(vector<int>& prices) {
        int lo = INT_MAX, best = 0;
        for (int p : prices) { best = max(best, p - lo); lo = min(lo, p); }
        return best;
    }
};""",
 """vector<int> a{7,1,5,3,6,4}; assert(Solution().maxProfit(a) == 5);
vector<int> b{7,6,4,3,1}; assert(Solution().maxProfit(b) == 0);""",
 "O(n) time, O(1) space", ["p − INT_MAX overflow if the order of the two lines is swapped carelessly (here best is updated first with lo = INT_MAX, which gives a negative number, safe)"],
 ["Unlimited transactions? (sum every positive difference)", "At most k transactions or with cooldown? (state-machine DP)"])

add("product-except-self", "Product of Array Except Self", "product-of-array-except-self", 1, "Prefix sum", "Asked at Amazon, Meta, Microsoft; tests prefix thinking without division.",
 ["answer[i] = (product of everything left of i) × (product of everything right of i). Fill left products in one pass, then multiply by a running right product in a second pass."],
 ["res[i] = product of a[0..i−1]", "Walk from the right with r = 1: res[i] *= r; r *= a[i]"],
 """class Solution {
public:
    vector<int> productExceptSelf(vector<int>& nums) {
        int n = nums.size();
        vector<int> res(n, 1);
        for (int i = 1; i < n; i++) res[i] = res[i - 1] * nums[i - 1];
        int r = 1;
        for (int i = n - 1; i >= 0; i--) { res[i] *= r; r *= nums[i]; }
        return res;
    }
};""",
 """vector<int> a{1,2,3,4}; assert((Solution().productExceptSelf(a) == vector<int>{24,12,8,6}));
vector<int> b{-1,1,0,-3,3}; assert((Solution().productExceptSelf(b) == vector<int>{0,0,9,0,0}));""",
 "O(n) time, O(1) extra space (the output doesn't count)", ["Using division (breaks with zeros, and it's forbidden)"],
 ["Why is the output array not counted as extra space?"])

add("kadane", "Maximum Subarray (Kadane)", "maximum-subarray", 1, "Kadane", "Classic; tests whether you see the 1-D DP hidden in it.",
 ["At each index, the best subarray ending here either extends the best one ending at i−1 or starts fresh at i: cur = max(a[i], cur + a[i]). The answer is the best cur seen."],
 ["cur = best = a[0]", "For i ≥ 1: cur = max(a[i], cur + a[i]); best = max(best, cur)"],
 """class Solution {
public:
    int maxSubArray(vector<int>& nums) {
        int cur = nums[0], best = nums[0];
        for (int i = 1; i < (int)nums.size(); i++) { cur = max(nums[i], cur + nums[i]); best = max(best, cur); }
        return best;
    }
};""",
 """vector<int> a{-2,1,-3,4,-1,2,1,-5,4}; assert(Solution().maxSubArray(a) == 6);
vector<int> b{-3,-1,-2}; assert(Solution().maxSubArray(b) == -1);""",
 "O(n) time, O(1) space", ["Starting best at 0 (wrong when all numbers are negative)"],
 ["Return the start and end indices too.", "Maximum product subarray? (track both max and min)"])

add("longest-consecutive", "Longest Consecutive Sequence", "longest-consecutive-sequence", 1, "Hashing", "Google and Amazon; the O(n) requirement is the whole point.",
 ["Put all numbers in a hash set. Only start counting from x when x − 1 is not in the set (x is the start of a run), then walk x+1, x+2… Each number is visited at most twice, so the total is O(n)."],
 ["set s(all)", "For x in s: if x−1 not in s, count the run from x"],
 """class Solution {
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
};""",
 """vector<int> a{100,4,200,1,3,2}; assert(Solution().longestConsecutive(a) == 4);
vector<int> b{0,3,7,2,5,8,4,6,0,1}; assert(Solution().longestConsecutive(b) == 9);
vector<int> c{}; assert(Solution().longestConsecutive(c) == 0);""",
 "O(n) average time, O(n) space", ["Starting a walk from every number (O(n²) on a long run)", "Sorting (O(n log n), not what's asked)"],
 ["Why is it O(n) even with the inner while loop?"])

add("group-anagrams", "Group Anagrams", "group-anagrams", 1, "Hashing", "Common at Amazon, Uber and service-company OAs.",
 ["Anagrams share a canonical key. Use the sorted word (O(k log k)) or a 26-letter count string (O(k)) as the hash-map key, and append each word to its group."],
 ["key = sorted(word)", "groups[key].push_back(word)"],
 """class Solution {
public:
    vector<vector<string>> groupAnagrams(vector<string>& strs) {
        unordered_map<string, vector<string>> g;
        for (auto& s : strs) { string k = s; sort(k.begin(), k.end()); g[k].push_back(s); }
        vector<vector<string>> res;
        for (auto& [k, v] : g) res.push_back(v);
        return res;
    }
};""",
 """vector<string> a{"eat","tea","tan","ate","nat","bat"}; auto r = Solution().groupAnagrams(a);
assert(r.size() == 3); size_t tot = 0; for (auto& v : r) tot += v.size(); assert(tot == 6);""",
 "O(n·k log k) time, O(n·k) space", ["Using a count array as the key without separators (\"1\",\"11\" collisions)"],
 ["Make the key O(k) instead of O(k log k)."])

add("top-k", "Top K Frequent Elements", "top-k-frequent-elements", 1, "Heap", "Amazon's most-asked heap problem.",
 ["Count frequencies with a hash map, then keep a min-heap of size k keyed by frequency; anything smaller than the heap's top can't be in the answer. Bucket sort by frequency gives O(n)."],
 ["Count", "Push (freq, value) into a min-heap; pop when size > k", "Heap contents are the answer"],
 """class Solution {
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
};""",
 """vector<int> a{1,1,1,2,2,3}; auto r = Solution().topKFrequent(a, 2); sort(r.begin(), r.end()); assert((r == vector<int>{1,2}));""",
 "O(n log k) time, O(n) space", ["Using a max-heap of all n elements (O(n log n))"],
 ["Do it in O(n) with buckets.", "What if the data is a stream?"])

add("3sum", "3Sum", "3sum", 1, "Two pointers", "Top-10 at Meta, Amazon, Microsoft; tests duplicate handling.",
 ["Sort. Fix a[i] and find pairs in a[i+1..n−1] summing to −a[i] with two pointers. Skip equal values of a[i], and skip equal values after finding a triple, so no duplicate triples appear."],
 ["Sort", "For each i (skip a[i] == a[i−1]): l = i+1, r = n−1", "Move l or r by the sum's sign; on a hit, record and skip duplicates on both sides"],
 """class Solution {
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
};""",
 """vector<int> a{-1,0,1,2,-1,-4}; auto r = Solution().threeSum(a); assert((r == vector<vector<int>>{{-1,-1,2},{-1,0,1}}));
vector<int> b{0,0,0,0}; assert(Solution().threeSum(b).size() == 1);""",
 "O(n²) time, O(1) extra space (besides sorting)", ["Not skipping duplicates", "Using a set of triples to dedupe (slow, and interviewers notice)"],
 ["4Sum?", "3Sum closest?"])

add("container", "Container With Most Water", "container-with-most-water", 1, "Two pointers", "Asked at Google and Amazon; the proof is the interview.",
 ["Start with the widest container. The height is limited by the shorter line, so moving the taller line inward can never help: the width shrinks and the height can't exceed the shorter line. Always move the shorter one."],
 ["l = 0, r = n−1", "area = (r − l) × min(h[l], h[r])", "Move the shorter side inward"],
 """class Solution {
public:
    int maxArea(vector<int>& h) {
        int l = 0, r = h.size() - 1, best = 0;
        while (l < r) {
            best = max(best, (r - l) * min(h[l], h[r]));
            if (h[l] < h[r]) l++; else r--;
        }
        return best;
    }
};""",
 """vector<int> a{1,8,6,2,5,4,8,3,7}; assert(Solution().maxArea(a) == 49);
vector<int> b{1,1}; assert(Solution().maxArea(b) == 1);""",
 "O(n) time, O(1) space", ["Moving the taller side"], ["Prove that moving the shorter side never skips the best answer."])

add("trapping-rain", "Trapping Rain Water", "trapping-rain-water", 3, "Two pointers", "The most famous Hard; Google, Amazon, Goldman Sachs.",
 ["Water above bar i = min(maxLeft, maxRight) − h[i]. With two pointers, whichever side has the smaller running maximum is the bottleneck, so that side's water is already known: process it and move inward."],
 ["l, r at ends; lmax = rmax = 0", "If h[l] < h[r]: lmax = max(lmax, h[l]); water += lmax − h[l]; l++", "Else the same on the right"],
 """class Solution {
public:
    int trap(vector<int>& h) {
        int l = 0, r = (int)h.size() - 1, lmax = 0, rmax = 0, w = 0;
        while (l < r) {
            if (h[l] < h[r]) { lmax = max(lmax, h[l]); w += lmax - h[l]; l++; }
            else { rmax = max(rmax, h[r]); w += rmax - h[r]; r--; }
        }
        return w;
    }
};""",
 """vector<int> a{0,1,0,2,1,0,1,3,2,1,2,1}; assert(Solution().trap(a) == 6);
vector<int> b{4,2,0,3,2,5}; assert(Solution().trap(b) == 9);""",
 "O(n) time, O(1) space", ["Off-by-one with prefix arrays", "Forgetting the empty-array case"],
 ["Solve it with prefix/suffix maximum arrays first, then optimise.", "Solve it with a monotonic stack.", "Trapping Rain Water II (2-D, heap + BFS)"])

add("longest-substring", "Longest Substring Without Repeating Characters", "longest-substring-without-repeating-characters", 1, "Sliding window", "Top-5 most asked overall.",
 ["Keep a window with no repeats. Remember the last index of each character; when s[r] was seen inside the window, jump l to one past that index."],
 ["last[c] = −1 for all c; l = 0", "For each r: if last[s[r]] ≥ l, l = last[s[r]] + 1", "last[s[r]] = r; best = max(best, r − l + 1)"],
 """class Solution {
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
};""",
 """assert(Solution().lengthOfLongestSubstring("abcabcbb") == 3);
assert(Solution().lengthOfLongestSubstring("bbbbb") == 1);
assert(Solution().lengthOfLongestSubstring("pwwkew") == 3);
assert(Solution().lengthOfLongestSubstring("") == 0);""",
 "O(n) time, O(alphabet) space", ["Moving l backwards when the old index is outside the window (the ≥ l check prevents it)"],
 ["At most k distinct characters?", "Return the substring itself."])

add("min-window", "Minimum Window Substring", "minimum-window-substring", 3, "Sliding window", "Hard sliding-window favourite at Meta, LinkedIn, Uber.",
 ["Count what t needs. Expand r; when the window covers all of t (need count reaches 0), shrink l as far as possible while still covering, recording the smallest window."],
 ["need[c] from t; missing = |t|", "Expand r: if need[s[r]] > 0, missing−−; need[s[r]]−−", "While missing == 0: record; need[s[l]]++; if it becomes > 0, missing++; l++"],
 """class Solution {
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
};""",
 """assert(Solution().minWindow("ADOBECODEBANC", "ABC") == "BANC");
assert(Solution().minWindow("a", "a") == "a");
assert(Solution().minWindow("a", "aa") == "");""",
 "O(|s| + |t|) time, O(alphabet) space", ["Forgetting duplicate letters in t", "Recording the window after shrinking past validity"],
 ["Why does each character enter and leave at most once?"])

add("subarray-sum-k", "Subarray Sum Equals K", "subarray-sum-equals-k", 1, "Prefix sum", "Common at Meta, Google; the trap is trying a sliding window.",
 ["Negative numbers break sliding windows. A subarray (j, i] sums to k exactly when prefix[i] − prefix[j] = k. Keep counts of every prefix seen; at each i add count[prefix − k]."],
 ["count[0] = 1; s = 0", "For x: s += x; ans += count[s − k]; count[s]++"],
 """class Solution {
public:
    int subarraySum(vector<int>& nums, int k) {
        unordered_map<long long, int> cnt{{0, 1}};
        long long s = 0; int ans = 0;
        for (int x : nums) { s += x; auto it = cnt.find(s - k); if (it != cnt.end()) ans += it->second; cnt[s]++; }
        return ans;
    }
};""",
 """vector<int> a{1,1,1}; assert(Solution().subarraySum(a, 2) == 2);
vector<int> b{1,2,3}; assert(Solution().subarraySum(b, 3) == 2);
vector<int> c{1,-1,0}; assert(Solution().subarraySum(c, 0) == 3);""",
 "O(n) time, O(n) space", ["Missing cnt[0] = 1", "Using a sliding window"],
 ["Longest subarray with sum k?", "Count subarrays divisible by k?"])

add("search-rotated", "Search in Rotated Sorted Array", "search-in-rotated-sorted-array", 1, "Binary search", "Microsoft, Amazon, LinkedIn staple.",
 ["At any mid, one half [lo, mid] or [mid, hi] is sorted. Check whether the target lies in the sorted half's range; if so search there, otherwise search the other half."],
 ["If a[lo] ≤ a[mid]: left half sorted; go left if a[lo] ≤ target < a[mid]", "Else right half sorted; go right if a[mid] < target ≤ a[hi]"],
 """class Solution {
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
};""",
 """vector<int> a{4,5,6,7,0,1,2}; assert(Solution().search(a, 0) == 4); assert(Solution().search(a, 3) == -1);
vector<int> b{1}; assert(Solution().search(b, 0) == -1);
vector<int> c{3,1}; assert(Solution().search(c, 1) == 1);""",
 "O(log n) time, O(1) space", ["Using < instead of ≤ in a[lo] ≤ a[mid] (fails on two elements)"],
 ["With duplicates? (worst case O(n): shrink lo/hi when a[lo] == a[mid] == a[hi])", "Find the rotation point / minimum."])

add("koko", "Koko Eating Bananas", "koko-eating-bananas", 1, "Binary search on the answer", "The textbook binary-search-on-answer problem.",
 ["If Koko can finish at speed k, she can at any faster speed: feasibility is monotone. Binary search k in [1, max pile]; check(k) sums ceil(pile / k) hours."],
 ["lo = 1, hi = max(piles)", "check(k): Σ ⌈p/k⌉ ≤ h", "Find the smallest k where check is true"],
 """class Solution {
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
};""",
 """vector<int> a{3,6,7,11}; assert(Solution().minEatingSpeed(a, 8) == 4);
vector<int> b{30,11,23,4,20}; assert(Solution().minEatingSpeed(b, 5) == 30); assert(Solution().minEatingSpeed(b, 6) == 23);""",
 "O(n log max) time, O(1) space", ["int overflow in the hours sum", "Starting lo at 0 (division by zero)"],
 ["Capacity to ship packages in D days.", "Split array largest sum."])

add("valid-parens", "Valid Parentheses", "valid-parentheses", 0, "Stack", "The standard stack opener in first rounds.",
 ["Push opening brackets. On a closing bracket the stack top must be its matching opener; pop it. At the end the stack must be empty."],
 ["Map ) → (, ] → [, } → {", "Mismatch or empty stack on a closer → false"],
 """class Solution {
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
};""",
 """assert(Solution().isValid("()[]{}")); assert(!Solution().isValid("(]")); assert(!Solution().isValid("(")); assert(Solution().isValid("{[]}"));""",
 "O(n) time, O(n) space", ["Forgetting the final empty check", "Popping an empty stack"], ["Minimum additions to make it valid?", "Longest valid parentheses (Hard)"])

add("daily-temps", "Daily Temperatures", "daily-temperatures", 1, "Monotonic stack", "The cleanest next-greater-element problem.",
 ["Keep a stack of indices with decreasing temperatures. When a warmer day arrives, every colder day on the stack has found its answer: pop and record the distance."],
 ["For i: while stack top is colder than t[i], res[top] = i − top, pop", "Push i"],
 """class Solution {
public:
    vector<int> dailyTemperatures(vector<int>& t) {
        vector<int> res(t.size(), 0), st;
        for (int i = 0; i < (int)t.size(); i++) {
            while (!st.empty() && t[st.back()] < t[i]) { res[st.back()] = i - st.back(); st.pop_back(); }
            st.push_back(i);
        }
        return res;
    }
};""",
 """vector<int> a{73,74,75,71,69,72,76,73}; assert((Solution().dailyTemperatures(a) == vector<int>{1,1,4,2,1,1,0,0}));""",
 "O(n) time (each index pushed and popped once), O(n) space", ["Storing temperatures instead of indices"], ["Next greater element in a circular array."])

add("histogram", "Largest Rectangle in Histogram", "largest-rectangle-in-histogram", 3, "Monotonic stack", "Hard-round favourite at Google and Amazon; base for Maximal Rectangle.",
 ["For each bar, the widest rectangle of its height spans between its previous smaller and next smaller bars. An increasing stack finds both: when a bar is popped, the current index is its next smaller and the new stack top is its previous smaller."],
 ["Append a 0-height sentinel", "Pop while h[top] ≥ h[i]: width = i − (new top) − 1", "Area = h[popped] × width"],
 """class Solution {
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
};""",
 """vector<int> a{2,1,5,6,2,3}; assert(Solution().largestRectangleArea(a) == 10);
vector<int> b{2,4}; assert(Solution().largestRectangleArea(b) == 4);""",
 "O(n) time, O(n) space", ["Forgetting the sentinel, so bars left on the stack are never measured"], ["Maximal rectangle of 1s in a matrix (apply this per row)."])

add("reverse-list", "Reverse Linked List", "reverse-linked-list", 0, "Linked list", "Asked in almost every first round; often followed by the recursive version.",
 ["Walk the list re-pointing each node's next to the previous node. Save next before overwriting it."],
 ["prev = null, cur = head", "nx = cur.next; cur.next = prev; prev = cur; cur = nx", "Return prev"],
 """class Solution {
public:
    ListNode* reverseList(ListNode* head) {
        ListNode* prev = nullptr;
        while (head) { ListNode* nx = head->next; head->next = prev; prev = head; head = nx; }
        return prev;
    }
};""",
 """assert((tov(Solution().reverseList(mk({1,2,3,4,5}))) == vector<int>{5,4,3,2,1})); assert(Solution().reverseList(nullptr) == nullptr);""",
 "O(n) time, O(1) space", ["Losing the rest of the list"], ["Reverse recursively.", "Reverse nodes between positions m and n.", "Reverse in groups of k (Hard)."])

add("cycle-ii", "Linked List Cycle II", "linked-list-cycle-ii", 1, "Linked list", "Floyd's algorithm; the proof is a common follow-up.",
 ["Slow moves 1, fast moves 2; if they meet there's a cycle. Then move one pointer to head and step both by 1: they meet at the cycle start, because head-to-start distance equals meeting-point-to-start distance (mod cycle length)."],
 ["Detect: slow/fast meet", "Reset one to head; step both by 1 until equal"],
 """class Solution {
public:
    ListNode* detectCycle(ListNode* head) {
        ListNode *s = head, *f = head;
        while (f && f->next) {
            s = s->next; f = f->next->next;
            if (s == f) { s = head; while (s != f) { s = s->next; f = f->next; } return s; }
        }
        return nullptr;
    }
};""",
 """ListNode* h = mk({3,2,0,-4}); h->next->next->next->next = h->next; assert(Solution().detectCycle(h) == h->next);
assert(Solution().detectCycle(mk({1,2})) == nullptr);""",
 "O(n) time, O(1) space", ["Checking f->next->next without checking f->next"], ["Prove why the second phase meets at the start.", "Find the cycle length."])

add("merge-k", "Merge K Sorted Lists", "merge-k-sorted-lists", 3, "Heap", "Amazon, Google, Meta Hard; tests heap use with pointers.",
 ["Push each list's head into a min-heap keyed by value. Pop the smallest, append it, push its next. Every node goes through the heap once."],
 ["Min-heap of (val, node)", "Pop, append, push node->next"],
 """class Solution {
public:
    ListNode* mergeKLists(vector<ListNode*>& lists) {
        auto cmp = [](ListNode* a, ListNode* b) { return a->val > b->val; };
        priority_queue<ListNode*, vector<ListNode*>, decltype(cmp)> pq(cmp);
        for (auto l : lists) if (l) pq.push(l);
        ListNode dummy(0); ListNode* t = &dummy;
        while (!pq.empty()) { auto n = pq.top(); pq.pop(); t->next = n; t = n; if (n->next) pq.push(n->next); }
        return dummy.next;
    }
};""",
 """vector<ListNode*> ls{mk({1,4,5}), mk({1,3,4}), mk({2,6})}; assert((tov(Solution().mergeKLists(ls)) == vector<int>{1,1,2,3,4,4,5,6}));
vector<ListNode*> e{}; assert(Solution().mergeKLists(e) == nullptr);""",
 "O(N log k) time, O(k) space", ["Pushing null heads"], ["Divide and conquer: merge pairs (same complexity, no heap).", "What if lists are huge files on disk? (external merge)"])

add("lru", "LRU Cache", "lru-cache", 1, "Linked list", "One of the most-asked design questions for freshers at Amazon, Microsoft, Swiggy.",
 ["Need O(1) get and put with recency order. A hash map gives O(1) lookup of a node; a doubly linked list gives O(1) move-to-front and remove-from-back. std::list + splice does both."],
 ["map key → list iterator", "get: splice the node to the front", "put: update or insert at front; if over capacity, erase the back and its map entry"],
 """class LRUCache {
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
};""",
 """LRUCache c(2); c.put(1,1); c.put(2,2); assert(c.get(1) == 1); c.put(3,3); assert(c.get(2) == -1); c.put(4,4);
assert(c.get(1) == -1); assert(c.get(3) == 3); assert(c.get(4) == 4);""",
 "O(1) per operation, O(capacity) space", ["Forgetting to move on update", "Erasing from the map after popping (dangling)"],
 ["Make it thread-safe.", "LFU cache (Hard).", "How does Redis approximate LRU?"])

add("level-order", "Binary Tree Level Order Traversal", "binary-tree-level-order-traversal", 1, "BFS", "Base for zigzag, right view, and many tree BFS questions.",
 ["BFS with a queue; process exactly the current queue size each round to keep levels separate."],
 ["q = [root]", "While q: sz = q.size(); pop sz nodes into one level, pushing children"],
 """class Solution {
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
};""",
 """auto r = Solution().levelOrder(tree({"3","9","20","null","null","15","7"})); assert((r == vector<vector<int>>{{3},{9,20},{15,7}}));
assert(Solution().levelOrder(nullptr).empty());""",
 "O(n) time, O(width) space", ["Reading q.size() inside the loop condition (it changes)"], ["Zigzag order.", "Right side view.", "Average of each level."])

add("lca", "Lowest Common Ancestor of a Binary Tree", "lowest-common-ancestor-of-a-binary-tree", 1, "Trees", "Asked at Meta, Amazon, Microsoft; short code, tricky reasoning.",
 ["Recurse: return the node if it's p or q. If the left and right subtrees each return non-null, this node is the LCA; otherwise pass up whichever side is non-null."],
 ["Base: null, p or q → return it", "L = lca(left), R = lca(right)", "Both non-null → root; else the non-null one"],
 """class Solution {
public:
    TreeNode* lowestCommonAncestor(TreeNode* root, TreeNode* p, TreeNode* q) {
        if (!root || root == p || root == q) return root;
        TreeNode* L = lowestCommonAncestor(root->left, p, q);
        TreeNode* R = lowestCommonAncestor(root->right, p, q);
        return L && R ? root : (L ? L : R);
    }
};""",
 """TreeNode* t = tree({"3","5","1","6","2","0","8","null","null","7","4"});
assert(Solution().lowestCommonAncestor(t, t->left, t->right) == t);
assert(Solution().lowestCommonAncestor(t, t->left, t->left->right->right) == t->left);""",
 "O(n) time, O(h) space", ["Assuming it's a BST (that version walks by value)"], ["LCA in a BST.", "What if p or q may not exist in the tree?"])

add("validate-bst", "Validate Binary Search Tree", "validate-binary-search-tree", 1, "BST", "Tests whether you know the BST property is global, not parent-child.",
 ["Every node must lie strictly between bounds inherited from its ancestors. Pass (lo, hi) down: left child gets (lo, val), right child gets (val, hi). Use long long or pointers for the bounds."],
 ["valid(node, lo, hi): lo < val < hi", "Recurse left with hi = val, right with lo = val"],
 """class Solution {
    bool ok(TreeNode* n, long long lo, long long hi) {
        if (!n) return true;
        if (n->val <= lo || n->val >= hi) return false;
        return ok(n->left, lo, n->val) && ok(n->right, n->val, hi);
    }
public:
    bool isValidBST(TreeNode* root) { return ok(root, LLONG_MIN, LLONG_MAX); }
};""",
 """assert(Solution().isValidBST(tree({"2","1","3"}))); assert(!Solution().isValidBST(tree({"5","1","4","null","null","3","6"})));
assert(!Solution().isValidBST(tree({"5","4","6","null","null","3","7"})));""",
 "O(n) time, O(h) space", ["Only comparing a node with its children", "int bounds failing for INT_MIN/INT_MAX values"], ["Do it with an inorder traversal (must be strictly increasing).", "Recover a BST with two swapped nodes."])

add("max-path-sum", "Binary Tree Maximum Path Sum", "binary-tree-maximum-path-sum", 3, "Trees", "Google and Meta Hard; the 'return one thing, record another' pattern.",
 ["A path can bend at one node. For each node, the best path through it is val + best downward gain from left + from right (ignoring negative gains). But only one side can be returned to the parent."],
 ["gain(n) = n.val + max(0, gain(left), gain(right))… returning only one side", "best = max(best, val + max(0,L) + max(0,R))"],
 """class Solution {
    int best = INT_MIN;
    int gain(TreeNode* n) {
        if (!n) return 0;
        int L = max(0, gain(n->left)), R = max(0, gain(n->right));
        best = max(best, n->val + L + R);
        return n->val + max(L, R);
    }
public:
    int maxPathSum(TreeNode* root) { gain(root); return best; }
};""",
 """assert(Solution().maxPathSum(tree({"1","2","3"})) == 6); assert(Solution().maxPathSum(tree({"-10","9","20","null","null","15","7"})) == 42);
assert(Solution().maxPathSum(tree({"-3"})) == -3);""",
 "O(n) time, O(h) space", ["Returning L + R to the parent (that's not a path)", "Initialising best to 0 (fails on all-negative trees)"], ["Diameter of a binary tree (same pattern with edge counts)."])

add("islands", "Number of Islands", "number-of-islands", 1, "DFS", "Most-asked graph problem; grid as an implicit graph.",
 ["Scan the grid; each unvisited '1' starts a new island. Flood-fill it (DFS or BFS) and mark visited so it isn't counted again."],
 ["For each cell == '1': count++, flood fill", "Fill: mark '0', recurse into 4 neighbours inside bounds"],
 """class Solution {
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
};""",
 """vector<vector<char>> g{{'1','1','0','0','0'},{'1','1','0','0','0'},{'0','0','1','0','0'},{'0','0','0','1','1'}}; assert(Solution().numIslands(g) == 3);""",
 "O(rows × cols) time and space (recursion)", ["Deep recursion on big grids (use BFS or an explicit stack)", "Not mentioning that you modify the input"], ["Max area of an island.", "Number of distinct islands.", "Do it with DSU."])

add("course-schedule", "Course Schedule", "course-schedule", 1, "Topological sort", "Amazon and Google; cycle detection in a directed graph.",
 ["Courses are nodes, prerequisites are edges. All courses can be finished exactly when the graph has no cycle. Kahn's algorithm: repeatedly take nodes with in-degree 0; if you process all n, there's no cycle."],
 ["Build adjacency and in-degrees", "Queue all in-degree-0 nodes; pop, decrement neighbours", "Return processed == n"],
 """class Solution {
public:
    bool canFinish(int n, vector<vector<int>>& pre) {
        vector<vector<int>> adj(n); vector<int> indeg(n, 0);
        for (auto& e : pre) { adj[e[1]].push_back(e[0]); indeg[e[0]]++; }
        queue<int> q; for (int i = 0; i < n; i++) if (!indeg[i]) q.push(i);
        int done = 0;
        while (!q.empty()) { int u = q.front(); q.pop(); done++; for (int v : adj[u]) if (--indeg[v] == 0) q.push(v); }
        return done == n;
    }
};""",
 """vector<vector<int>> a{{1,0}}; assert(Solution().canFinish(2, a)); vector<vector<int>> b{{1,0},{0,1}}; assert(!Solution().canFinish(2, b));""",
 "O(V + E) time and space", ["Reversing the edge direction (harmless here, wrong in Course Schedule II's order)"], ["Return a valid order (Course Schedule II).", "Do it with DFS colouring."])

add("rotting-oranges", "Rotting Oranges", "rotting-oranges", 1, "BFS", "Multi-source BFS; Amazon's favourite grid BFS.",
 ["All rotten oranges start the BFS together. Each BFS level is one minute. At the end, if any fresh orange remains, return −1."],
 ["Queue all rotten cells; count fresh", "BFS level by level, rotting neighbours and decrementing fresh", "Answer = levels used, or −1"],
 """class Solution {
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
};""",
 """vector<vector<int>> a{{2,1,1},{1,1,0},{0,1,1}}; assert(Solution().orangesRotting(a) == 4);
vector<vector<int>> b{{2,1,1},{0,1,1},{1,0,1}}; assert(Solution().orangesRotting(b) == -1);
vector<vector<int>> c{{0,2}}; assert(Solution().orangesRotting(c) == 0);""",
 "O(rows × cols) time and space", ["Counting a minute after the last level (stop when fresh is 0)"], ["01 Matrix (distance to nearest 0).", "Walls and gates."])

add("network-delay", "Network Delay Time", "network-delay-time", 1, "Dijkstra", "The standard Dijkstra question.",
 ["Shortest time for the signal to reach every node = the largest shortest-path distance from k. Run Dijkstra with a min-heap; if any node is unreachable, return −1."],
 ["dist[k] = 0; heap (d, node)", "Pop; skip stale; relax edges", "Answer = max(dist) or −1"],
 """class Solution {
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
};""",
 """vector<vector<int>> t{{2,1,1},{2,3,1},{3,4,1}}; assert(Solution().networkDelayTime(t, 4, 2) == 2);
vector<vector<int>> u{{1,2,1}}; assert(Solution().networkDelayTime(u, 2, 2) == -1);""",
 "O((V + E) log V) time", ["Not skipping stale heap entries (still correct, slower)", "1-indexed nodes"], ["Cheapest flights within K stops (Bellman-Ford / BFS by stops).", "Path with minimum effort."])

add("provinces", "Number of Provinces", "number-of-provinces", 1, "DSU", "Connected components; a clean place to show Union-Find.",
 ["Each city starts alone. For every connected pair, union their sets; each successful union reduces the count of components by one."],
 ["parent[i] = i; comps = n", "For i < j with isConnected[i][j]: if unite(i, j), comps−−"],
 """class Solution {
    vector<int> p;
    int find(int x) { return p[x] == x ? x : p[x] = find(p[x]); }
public:
    int findCircleNum(vector<vector<int>>& g) {
        int n = g.size(), comps = n; p.resize(n); iota(p.begin(), p.end(), 0);
        for (int i = 0; i < n; i++) for (int j = i + 1; j < n; j++)
            if (g[i][j]) { int a = find(i), b = find(j); if (a != b) { p[a] = b; comps--; } }
        return comps;
    }
};""",
 """vector<vector<int>> a{{1,1,0},{1,1,0},{0,0,1}}; assert(Solution().findCircleNum(a) == 2);
vector<vector<int>> b{{1,0,0},{0,1,0},{0,0,1}}; assert(Solution().findCircleNum(b) == 3);""",
 "O(n² α(n)) time, O(n) space", ["Comparing raw parents instead of roots"], ["Solve it with DFS too.", "Redundant connection.", "Accounts merge."])

add("house-robber", "House Robber", "house-robber", 1, "DP", "The first DP most interviewers ask.",
 ["At house i you either rob it (take a[i] + best up to i−2) or skip it (best up to i−1). Only the last two values are needed."],
 ["dp[i] = max(dp[i−1], dp[i−2] + a[i])", "Keep two variables"],
 """class Solution {
public:
    int rob(vector<int>& a) {
        int prev2 = 0, prev1 = 0;
        for (int x : a) { int cur = max(prev1, prev2 + x); prev2 = prev1; prev1 = cur; }
        return prev1;
    }
};""",
 """vector<int> a{1,2,3,1}; assert(Solution().rob(a) == 4); vector<int> b{2,7,9,3,1}; assert(Solution().rob(b) == 12);""",
 "O(n) time, O(1) space", ["Greedy 'take every other house'"], ["Houses in a circle (House Robber II).", "Houses on a tree (House Robber III)."])

add("coin-change", "Coin Change", "coin-change", 1, "Knapsack", "Most-asked unbounded-knapsack problem; greedy fails on it.",
 ["dp[x] = fewest coins to make x. dp[x] = min over coins c ≤ x of dp[x − c] + 1. Greedy fails (coins 1, 3, 4 for 6: greedy gives 3, best is 2)."],
 ["dp[0] = 0, others = ∞", "For x in 1..amount, for c: dp[x] = min(dp[x], dp[x−c] + 1)", "Answer dp[amount] or −1"],
 """class Solution {
public:
    int coinChange(vector<int>& coins, int amount) {
        vector<int> dp(amount + 1, INT_MAX); dp[0] = 0;
        for (int x = 1; x <= amount; x++)
            for (int c : coins) if (c <= x && dp[x - c] != INT_MAX) dp[x] = min(dp[x], dp[x - c] + 1);
        return dp[amount] == INT_MAX ? -1 : dp[amount];
    }
};""",
 """vector<int> a{1,2,5}; assert(Solution().coinChange(a, 11) == 3); vector<int> b{2}; assert(Solution().coinChange(b, 3) == -1);
vector<int> c{1,3,4}; assert(Solution().coinChange(c, 6) == 2); assert(Solution().coinChange(a, 0) == 0);""",
 "O(amount × coins) time, O(amount) space", ["INT_MAX + 1 overflow", "Using greedy"], ["Count the number of ways (Coin Change II: coins in the outer loop).", "Print the coins used."])

add("lis", "Longest Increasing Subsequence", "longest-increasing-subsequence", 1, "DP", "Asked for both the O(n²) DP and the O(n log n) follow-up.",
 ["O(n²): dp[i] = 1 + max dp[j] for j < i with a[j] < a[i]. O(n log n): keep tails[len] = smallest possible tail of an increasing subsequence of length len+1; for each x, replace the first tail ≥ x (lower_bound) or append."],
 ["tails = []", "For x: it = lower_bound(tails, x); replace or push_back", "Answer = tails.size()"],
 """class Solution {
public:
    int lengthOfLIS(vector<int>& a) {
        vector<int> tails;
        for (int x : a) {
            auto it = lower_bound(tails.begin(), tails.end(), x);
            if (it == tails.end()) tails.push_back(x); else *it = x;
        }
        return tails.size();
    }
};""",
 """vector<int> a{10,9,2,5,3,7,101,18}; assert(Solution().lengthOfLIS(a) == 4); vector<int> b{7,7,7,7}; assert(Solution().lengthOfLIS(b) == 1);
vector<int> c{0,1,0,3,2,3}; assert(Solution().lengthOfLIS(c) == 4);""",
 "O(n log n) time, O(n) space", ["Thinking tails is the subsequence itself (it isn't)", "upper_bound for strictly increasing (use lower_bound)"], ["Print the actual subsequence.", "Russian doll envelopes (Hard)."])

add("lcs", "Longest Common Subsequence", "longest-common-subsequence", 1, "String DP", "The base of all two-string DP.",
 ["dp[i][j] = LCS of a[0..i) and b[0..j). If a[i−1] == b[j−1], dp[i][j] = dp[i−1][j−1] + 1; else max(dp[i−1][j], dp[i][j−1])."],
 ["(n+1) × (m+1) table, row/column 0 are 0", "Fill row by row", "Space-optimise to two rows"],
 """class Solution {
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
};""",
 """assert(Solution().longestCommonSubsequence("abcde", "ace") == 3); assert(Solution().longestCommonSubsequence("abc", "def") == 0);""",
 "O(n × m) time, O(m) space", ["Mixing string index i−1 with dp index i"], ["Print the LCS.", "Shortest common supersequence.", "Longest palindromic subsequence."])

add("edit-distance", "Edit Distance", "edit-distance", 1, "String DP", "Google, Amazon, Microsoft; real-world use in spell checkers and diff.",
 ["dp[i][j] = edits to turn a[0..i) into b[0..j). Equal last characters cost nothing (diagonal). Otherwise 1 + min(insert dp[i][j−1], delete dp[i−1][j], replace dp[i−1][j−1]). Base: dp[i][0] = i, dp[0][j] = j."],
 ["Fill base row and column", "Apply the transition", "Answer dp[n][m]"],
 """class Solution {
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
};""",
 """assert(Solution().minDistance("horse", "ros") == 3); assert(Solution().minDistance("intention", "execution") == 5); assert(Solution().minDistance("", "a") == 1);""",
 "O(n × m) time and space (O(m) with two rows)", ["Wrong base cases"], ["Reduce to O(min(n, m)) space.", "One edit distance (O(n))."])

add("partition-subset", "Partition Equal Subset Sum", "partition-equal-subset-sum", 1, "Knapsack", "0/1 knapsack in disguise; Amazon and Meta.",
 ["Equal halves exist iff some subset sums to total/2 (total must be even). Boolean 0/1 knapsack over sums, iterating sums downwards so each number is used once."],
 ["If total is odd → false", "dp[0] = true; for x: for s = T..x: dp[s] |= dp[s − x]"],
 """class Solution {
public:
    bool canPartition(vector<int>& a) {
        int total = accumulate(a.begin(), a.end(), 0);
        if (total % 2) return false;
        int T = total / 2; vector<char> dp(T + 1, 0); dp[0] = 1;
        for (int x : a) for (int s = T; s >= x; s--) dp[s] |= dp[s - x];
        return dp[T];
    }
};""",
 """vector<int> a{1,5,11,5}; assert(Solution().canPartition(a)); vector<int> b{1,2,3,5}; assert(!Solution().canPartition(b));""",
 "O(n × total) time, O(total) space", ["Iterating sums upwards (reuses a number)"], ["Use a bitset for speed.", "Target sum (count sign assignments)."])

add("subsets", "Subsets", "subsets", 1, "Backtracking", "The entry point to backtracking; often followed by Subsets II.",
 ["Each element is either in or out: a binary decision tree with 2ⁿ leaves. Recurse with pick / skip, or iterate: for each element, copy every existing subset and add it."],
 ["go(i): if i == n, record", "Pick a[i], go(i+1), unpick; go(i+1)"],
 """class Solution {
    vector<vector<int>> res; vector<int> cur;
    void go(vector<int>& a, int i) {
        if (i == (int)a.size()) { res.push_back(cur); return; }
        cur.push_back(a[i]); go(a, i + 1); cur.pop_back();
        go(a, i + 1);
    }
public:
    vector<vector<int>> subsets(vector<int>& a) { go(a, 0); return res; }
};""",
 """vector<int> a{1,2,3}; auto r = Solution().subsets(a); assert(r.size() == 8); sort(r.begin(), r.end()); assert(r[0].empty() || r.front() == vector<int>{});""",
 "O(n × 2ⁿ) time, O(n) recursion depth", ["Forgetting to pop after the pick branch"], ["Subsets II with duplicates (sort, skip equal siblings).", "Do it with bitmasks."])

add("merge-intervals", "Merge Intervals", "merge-intervals", 1, "Intervals", "Top-asked at Google, Meta, Bloomberg.",
 ["Sort by start. Walk once: if the current interval starts before the last merged one ends, extend the end; otherwise start a new merged interval."],
 ["Sort by start", "If start ≤ last.end: last.end = max(last.end, end); else push"],
 """class Solution {
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
};""",
 """vector<vector<int>> a{{1,3},{2,6},{8,10},{15,18}}; assert((Solution().merge(a) == vector<vector<int>>{{1,6},{8,10},{15,18}}));
vector<vector<int>> b{{1,4},{4,5}}; assert((Solution().merge(b) == vector<vector<int>>{{1,5}}));""",
 "O(n log n) time, O(n) output", ["Setting end = x.end instead of max (a long interval swallowing a short one)"], ["Insert interval.", "Meeting rooms II (minimum rooms)."])

add("kth-largest", "Kth Largest Element in an Array", "kth-largest-element-in-an-array", 1, "Heap", "Asked with the follow-up 'can you beat O(n log n)?'.",
 ["Keep a min-heap of size k: its top is the k-th largest. Quickselect averages O(n)."],
 ["Push each x; pop when size > k", "Return top"],
 """class Solution {
public:
    int findKthLargest(vector<int>& a, int k) {
        priority_queue<int, vector<int>, greater<int>> pq;
        for (int x : a) { pq.push(x); if ((int)pq.size() > k) pq.pop(); }
        return pq.top();
    }
};""",
 """vector<int> a{3,2,1,5,6,4}; assert(Solution().findKthLargest(a, 2) == 5); vector<int> b{3,2,3,1,2,4,5,5,6}; assert(Solution().findKthLargest(b, 4) == 4);""",
 "O(n log k) time, O(k) space", ["Max-heap of everything (O(n log n))"], ["Quickselect (average O(n), worst O(n²)).", "nth_element in C++."])

add("trie", "Implement Trie (Prefix Tree)", "implement-trie-prefix-tree", 1, "Trie", "Common design-style question; base for autocomplete and Word Search II.",
 ["Each node has 26 children and an end-of-word flag. Insert walks/creates nodes; search walks and checks the flag; startsWith only walks."],
 ["insert: create missing children, mark end", "search: walk, return end flag", "startsWith: walk, return true"],
 """class Trie {
    struct Node { Node* ch[26] = {}; bool end = false; };
    Node* root = new Node();
    Node* walk(const string& w) { Node* n = root; for (char c : w) { n = n->ch[c - 'a']; if (!n) return nullptr; } return n; }
public:
    void insert(string w) { Node* n = root; for (char c : w) { if (!n->ch[c - 'a']) n->ch[c - 'a'] = new Node(); n = n->ch[c - 'a']; } n->end = true; }
    bool search(string w) { Node* n = walk(w); return n && n->end; }
    bool startsWith(string p) { return walk(p) != nullptr; }
};""",
 """Trie t; t.insert("apple"); assert(t.search("apple")); assert(!t.search("app")); assert(t.startsWith("app")); t.insert("app"); assert(t.search("app"));""",
 "O(length) per operation, O(total characters × 26) space", ["Leaking memory (mention a destructor or arena)"], ["Word Search II.", "Autocomplete top-3 suggestions.", "Max XOR with a bit trie."])

add("jump-game", "Jump Game", "jump-game", 1, "Greedy", "A short greedy problem that tests whether you'd reach for DP unnecessarily.",
 ["Track the furthest index reachable so far. If you ever stand on an index beyond it, you're stuck."],
 ["reach = 0", "For i: if i > reach → false; reach = max(reach, i + a[i])"],
 """class Solution {
public:
    bool canJump(vector<int>& a) {
        int reach = 0;
        for (int i = 0; i < (int)a.size(); i++) { if (i > reach) return false; reach = max(reach, i + a[i]); }
        return true;
    }
};""",
 """vector<int> a{2,3,1,1,4}; assert(Solution().canJump(a)); vector<int> b{3,2,1,0,4}; assert(!Solution().canJump(b));""",
 "O(n) time, O(1) space", ["O(n²) DP when greedy suffices"], ["Minimum number of jumps (Jump Game II, greedy BFS by levels)."])

add("median-stream", "Find Median from Data Stream", "find-median-from-data-stream", 3, "Heap", "Classic two-heap design; Google, Amazon, Microsoft.",
 ["Keep the smaller half in a max-heap and the larger half in a min-heap, sizes equal or the max-heap one bigger. The median is the max-heap top, or the average of both tops."],
 ["Push to lo (max-heap), move lo's top to hi", "If hi is bigger, move hi's top back to lo", "Median from the tops"],
 """class MedianFinder {
    priority_queue<int> lo;                                   // max-heap: smaller half
    priority_queue<int, vector<int>, greater<int>> hi;        // min-heap: larger half
public:
    void addNum(int x) {
        lo.push(x); hi.push(lo.top()); lo.pop();
        if (hi.size() > lo.size()) { lo.push(hi.top()); hi.pop(); }
    }
    double findMedian() { return lo.size() > hi.size() ? lo.top() : (lo.top() + (double)hi.top()) / 2.0; }
};""",
 """MedianFinder m; m.addNum(1); m.addNum(2); assert(m.findMedian() == 1.5); m.addNum(3); assert(m.findMedian() == 2.0);""",
 "O(log n) per add, O(1) median", ["Integer division when averaging", "int overflow when adding two big tops (cast first)"], ["If all numbers are in 0..100? (counting array)", "Sliding window median."])

TOPICS = P
