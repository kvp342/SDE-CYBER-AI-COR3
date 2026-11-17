// Vending machine: inventory, accepted coins, selection, and change from a limited coin stock (refund if exact change is impossible).
#include <cassert>
#include <iostream>
#include <map>
#include <optional>
#include <string>
#include <vector>
using namespace std;
struct Item { string name; int price, qty; };
class VendingMachine {
    map<string, Item> items; map<int, int> coins;                 // coin value -> count held
    vector<int> inserted; int credit = 0;
    optional<map<int, int>> makeChange(int amount, map<int, int> stock) const {   // DP over coin counts: exact change if possible
        vector<optional<map<int, int>>> best(amount + 1); best[0] = map<int, int>{};
        for (auto [v, cnt] : stock)
            for (int k = 0; k < cnt; k++)
                for (int a = amount; a >= v; a--)
                    if (best[a - v] && (!best[a] || 1 + total(*best[a - v]) < total(*best[a]))) { auto m = *best[a - v]; if (m[v] < cnt) { m[v]++; best[a] = m; } }
        return best[amount];
    }
    static int total(const map<int, int>& m) { int t = 0; for (auto& [v, c] : m) t += c; return t; }
public:
    void stock(const string& code, Item it) { items[code] = it; }
    void loadCoins(int value, int count) { coins[value] += count; }
    bool insert(int coin) { if (coin != 1 && coin != 2 && coin != 5 && coin != 10) return false; inserted.push_back(coin); credit += coin; return true; }
    int balance() const { return credit; }
    struct Sale { bool ok; string reason; map<int, int> change; };
    Sale select(const string& code) {
        auto it = items.find(code);
        if (it == items.end()) return {false, "unknown item", {}};
        if (it->second.qty == 0) return {false, "sold out", {}};
        if (credit < it->second.price) return {false, "insert more money", {}};
        auto stockWith = coins; for (int c : inserted) stockWith[c]++;
        auto ch = makeChange(credit - it->second.price, stockWith);
        if (!ch) return {false, "exact change only", {}};
        coins = stockWith; for (auto [v, c] : *ch) coins[v] -= c;  // keep inserted coins, pay out change
        it->second.qty--; inserted.clear(); credit = 0;
        return {true, "", *ch};
    }
    map<int, int> refund() { map<int, int> r; for (int c : inserted) r[c]++; inserted.clear(); credit = 0; return r; }
};
int main() {
    VendingMachine vm; vm.stock("A1", {"water", 15, 2}); vm.stock("B2", {"chips", 20, 0}); vm.loadCoins(5, 1); vm.loadCoins(1, 2);
    assert(!vm.insert(3) && vm.insert(10) && vm.insert(10) && vm.balance() == 20);
    assert(vm.select("B2").reason == "sold out" && vm.select("Z9").reason == "unknown item");
    auto s = vm.select("A1"); assert(s.ok && s.change == (map<int, int>{{5, 1}}));          // 20 - 15 = one 5 coin
    vm.insert(10); vm.insert(10); s = vm.select("A1"); assert(!s.ok && s.reason == "exact change only");   // the 5 is gone, two 1s cannot make 5
    auto r = vm.refund(); assert(r == (map<int, int>{{10, 2}}) && vm.balance() == 0);
    vm.insert(10); vm.insert(5); s = vm.select("A1"); assert(s.ok && s.change.empty());    // exact money
    vm.insert(10); assert(vm.select("A1").reason == "sold out");
    cout << "vending machine ok\n";
}
