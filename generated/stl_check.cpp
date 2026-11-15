#include <bits/stdc++.h>
using namespace std;
int main() {
    vector<int> v{5, 3, 1}; v.reserve(10); v.push_back(4); v.pop_back(); assert(v.back() == 1 && v.at(0) == 5);
    v.insert(v.begin() + 1, 9); v.erase(v.begin() + 1); sort(v.begin(), v.end()); assert((v == vector<int>{1, 3, 5}));
    assert(*lower_bound(v.begin(), v.end(), 3) == 3 && *upper_bound(v.begin(), v.end(), 3) == 5 && binary_search(v.begin(), v.end(), 5));
    string s = "hello"; assert(s.substr(1, 3) == "ell" && s.find("ll") == 2 && to_string(42) == "42" && stoi("17") == 17 && stoll("10000000000") == 10000000000LL);
    s += '!'; s.push_back('?'); assert(s == "hello!?");
    deque<int> d; d.push_front(1); d.push_back(2); assert(d[0] == 1); d.pop_front(); d.pop_back(); assert(d.empty());
    stack<int> st; st.push(1); assert(!st.empty() && st.top() == 1); queue<int> q; q.push(2); assert(q.front() == 2); q.pop();
    priority_queue<int> mx; mx.push(1); mx.push(3); assert(mx.top() == 3);
    priority_queue<int, vector<int>, greater<int>> mn; mn.push(1); mn.push(3); assert(mn.top() == 1);
    auto cmp = [](const pair<int,int>& a, const pair<int,int>& b) { return a.second > b.second; };
    priority_queue<pair<int,int>, vector<pair<int,int>>, decltype(cmp)> pq(cmp); pq.push({1, 9}); pq.push({2, 4}); assert(pq.top().first == 2);
    set<int> se{4, 1, 7}; assert(*se.lower_bound(2) == 4 && *se.upper_bound(4) == 7 && se.count(1) && se.find(9) == se.end());
    multiset<int> ms{2, 2, 2}; ms.erase(ms.find(2)); assert(ms.size() == 2); ms.erase(2); assert(ms.empty());
    map<string, int> m; m["a"] = 1; assert(m.count("b") == 0); (void)m["b"]; assert(m.size() == 2);   // operator[] inserted "b"
    unordered_map<int, int> um; um.reserve(100); um[3]++; assert(um.find(3)->second == 1);
    vector<int> w{3, 1, 2}; reverse(w.begin(), w.end()); assert((w == vector<int>{2, 1, 3}));
    rotate(w.begin(), w.begin() + 1, w.end()); assert((w == vector<int>{1, 3, 2})); next_permutation(w.begin(), w.end()); assert((w == vector<int>{2, 1, 3}));
    vector<long long> big{2000000000LL, 2000000000LL}; assert(accumulate(big.begin(), big.end(), 0LL) == 4000000000LL);
    assert(*min_element(w.begin(), w.end()) == 1 && *max_element(w.begin(), w.end()) == 3);
    vector<int> u{1, 1, 2, 2, 3}; u.erase(unique(u.begin(), u.end()), u.end()); assert(u.size() == 3);
    assert(gcd(12, 18) == 6 && __gcd(12, 18) == 6);
    stable_sort(u.begin(), u.end()); auto [a, b] = make_pair(1, 2); assert(a + b == 3); tuple<int, char> t{1, 'x'}; assert(get<1>(t) == 'x');
    bitset<8> bs; bs.set(1); bs.set(3); assert(bs.count() == 2 && bs.test(3));
    vector<int> io(4); iota(io.begin(), io.end(), 0); assert(io[3] == 3); assert(__builtin_popcount(7) == 3 && __builtin_popcountll(1LL << 40) == 1);
    assert(-7 / 2 == -3 && -7 % 2 == -1 && ((-7 % 3) + 3) % 3 == 2);   // bug 17
    vector<int> e; assert((int)e.size() - 1 == -1);                       // bug 3, the safe form
    puts("stl ok");
}
