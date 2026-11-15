// Splitwise: expenses with equal, exact and percentage splits, balances, and debt simplification.
// Money is kept in paise (integers) so splits never lose a rupee to floating point.
#include <cassert>
#include <iostream>
#include <map>
#include <memory>
#include <numeric>
#include <queue>
#include <stdexcept>
#include <string>
#include <tuple>
#include <vector>
using namespace std;
using Paise = long long;

class SplitStrategy {                                            // Strategy for how one expense is divided
public:
    virtual ~SplitStrategy() = default;
    virtual vector<Paise> shares(Paise total, size_t people) const = 0;
};
class EqualSplit : public SplitStrategy {
public:
    vector<Paise> shares(Paise total, size_t n) const override {
        vector<Paise> s(n, total / (Paise)n);
        for (size_t i = 0; i < (size_t)(total % (Paise)n); i++) s[i]++;   // spread the remainder, first come first
        return s;
    }
};
class ExactSplit : public SplitStrategy {
    vector<Paise> amounts;
public:
    explicit ExactSplit(vector<Paise> a) : amounts(move(a)) {}
    vector<Paise> shares(Paise total, size_t n) const override {
        if (amounts.size() != n || accumulate(amounts.begin(), amounts.end(), 0LL) != total) throw invalid_argument("exact amounts must add up");
        return amounts;
    }
};
class PercentSplit : public SplitStrategy {
    vector<int> pct;
public:
    explicit PercentSplit(vector<int> p) : pct(move(p)) {}
    vector<Paise> shares(Paise total, size_t n) const override {
        if (pct.size() != n || accumulate(pct.begin(), pct.end(), 0) != 100) throw invalid_argument("percentages must add to 100");
        vector<Paise> s(n); Paise used = 0;
        for (size_t i = 0; i < n; i++) used += s[i] = total * pct[i] / 100;
        s[0] += total - used;                                     // rounding leftover to the first person
        return s;
    }
};

class Ledger {
    map<string, Paise> net;                                       // positive: is owed money; negative: owes
public:
    void addExpense(const string& payer, Paise total, const vector<string>& people, const SplitStrategy& how) {
        auto s = how.shares(total, people.size());
        net[payer] += total;
        for (size_t i = 0; i < people.size(); i++) net[people[i]] -= s[i];
    }
    Paise balance(const string& u) const { auto it = net.find(u); return it == net.end() ? 0 : it->second; }
    // Greedy simplification: repeatedly settle the largest debtor with the largest creditor (at most n-1 payments).
    vector<tuple<string, string, Paise>> settle() const {
        priority_queue<pair<Paise, string>> cred, debt;
        for (auto& [u, v] : net) { if (v > 0) cred.push({v, u}); else if (v < 0) debt.push({-v, u}); }
        vector<tuple<string, string, Paise>> pay;
        while (!cred.empty()) {
            auto [c, cu] = cred.top(); cred.pop(); auto [d, du] = debt.top(); debt.pop();
            Paise x = min(c, d); pay.push_back({du, cu, x});
            if (c > x) cred.push({c - x, cu});
            if (d > x) debt.push({d - x, du});
        }
        return pay;
    }
};

int main() {
    Ledger l;
    l.addExpense("Asha", 100000, {"Asha", "Ravi", "Meera"}, EqualSplit());             // Rs 1000 dinner
    l.addExpense("Ravi", 60000, {"Asha", "Ravi"}, ExactSplit({20000, 40000}));         // Rs 600 cab
    l.addExpense("Meera", 30000, {"Asha", "Ravi", "Meera"}, PercentSplit({50, 25, 25})); // Rs 300 snacks
    assert(l.balance("Asha") == 100000 - 33334 - 20000 - 15000);  // 31666
    assert(l.balance("Ravi") == 60000 - 33333 - 40000 - 7500);    // -20833
    assert(l.balance("Asha") + l.balance("Ravi") + l.balance("Meera") == 0);
    auto pay = l.settle();
    assert(pay.size() <= 2);
    Paise sum = 0;
    for (auto& [from, to, amt] : pay) sum += amt;
    assert(sum == 31666);                                         // everything owed to Asha is paid
    try { l.addExpense("Asha", 100, {"Asha", "Ravi"}, PercentSplit({60, 30})); assert(false); } catch (const invalid_argument&) {}
    for (auto& [from, to, amt] : pay) cout << from << " pays " << to << " Rs " << amt / 100 << "." << amt % 100 << "\n";
    cout << "splitwise ok\n";
}
