// Machine coding: inventory management with categories, stock in and out, and low-stock alerts to subscribers (Observer pattern).
#include <cassert>
#include <functional>
#include <iostream>
#include <map>
#include <stdexcept>
#include <string>
#include <vector>
using namespace std;
struct Product { string sku, name, category; int qty = 0, reorderLevel = 0; };
class Inventory {
    map<string, Product> items; vector<function<void(const Product&)>> subs;
public:
    void subscribe(function<void(const Product&)> f) { subs.push_back(move(f)); }
    void add(Product p) { if (items.count(p.sku)) throw invalid_argument("duplicate sku"); items[p.sku] = move(p); }
    void stockIn(const string& sku, int n) { if (n <= 0) throw invalid_argument("bad quantity"); items.at(sku).qty += n; }
    bool stockOut(const string& sku, int n) {
        auto& p = items.at(sku); if (n <= 0 || n > p.qty) return false;
        bool wasAbove = p.qty > p.reorderLevel; p.qty -= n;
        if (wasAbove && p.qty <= p.reorderLevel) for (auto& f : subs) f(p);          // alert once, when crossing the level
        return true;
    }
    int qty(const string& sku) const { return items.at(sku).qty; }
    vector<string> byCategory(const string& c) const { vector<string> r; for (auto& [s, p] : items) if (p.category == c) r.push_back(s); return r; }
    vector<string> lowStock() const { vector<string> r; for (auto& [s, p] : items) if (p.qty <= p.reorderLevel) r.push_back(s); return r; }
};
int main() {
    Inventory inv; vector<string> alerts; inv.subscribe([&](const Product& p) { alerts.push_back(p.sku); });
    inv.add({"P1", "Pen", "stationery", 50, 10}); inv.add({"P2", "Notebook", "stationery", 20, 5}); inv.add({"P3", "Mouse", "electronics", 8, 3});
    bool threw = false; try { inv.add({"P1", "dup", "x", 1, 1}); } catch (const invalid_argument&) { threw = true; } assert(threw);
    assert(inv.stockOut("P1", 30) && alerts.empty() && inv.stockOut("P1", 10) && alerts == vector<string>{"P1"});   // 50 -> 20 -> 10: crosses at 10
    assert(inv.stockOut("P1", 5) && alerts.size() == 1);                       // already below: no repeat alert
    assert(!inv.stockOut("P1", 100) && !inv.stockOut("P1", 0) && inv.qty("P1") == 5);
    inv.stockIn("P1", 20); assert(inv.stockOut("P1", 16) && alerts.size() == 2);   // refilled above, crossed again
    assert((inv.byCategory("stationery") == vector<string>{"P1", "P2"}) && (inv.lowStock() == vector<string>{"P1"}));
    cout << "inventory ok\n";
}
