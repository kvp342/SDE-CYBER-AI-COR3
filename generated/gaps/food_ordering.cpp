// Machine coding: food ordering. Restaurants and menus, a cart per user (one restaurant at a time), order state machine
// PLACED -> ACCEPTED -> PREPARING -> OUT_FOR_DELIVERY -> DELIVERED (or CANCELLED before PREPARING), billing with tax and coupon.
#include <cassert>
#include <iostream>
#include <map>
#include <memory>
#include <stdexcept>
#include <string>
#include <vector>
using namespace std;
enum class Status { Placed, Accepted, Preparing, OutForDelivery, Delivered, Cancelled };
struct MenuItem { string id, name; int price; bool available = true; };
struct Restaurant { string id, name; map<string, MenuItem> menu; };
struct Coupon { virtual ~Coupon() = default; virtual int discount(int subtotal) const = 0; };
struct FlatOff : Coupon { int amt, minOrder; FlatOff(int a, int m) : amt(a), minOrder(m) {} int discount(int s) const override { return s >= minOrder ? amt : 0; } };
struct PercentOff : Coupon { int pct, cap; PercentOff(int p, int c) : pct(p), cap(c) {} int discount(int s) const override { return min(s * pct / 100, cap); } };
struct Bill { int subtotal, discount, tax, total; };
struct Order { int id; string user, restaurant; map<string, int> items; Bill bill; Status status = Status::Placed; };
class FoodApp {
    map<string, Restaurant> rs; map<string, pair<string, map<string, int>>> carts; vector<Order> orders;
    static bool next(Status from, Status to) {
        if (to == Status::Cancelled) return from == Status::Placed || from == Status::Accepted;
        return (int)to == (int)from + 1 && from != Status::Delivered && from != Status::Cancelled;
    }
public:
    void add(Restaurant r) { rs[r.id] = move(r); }
    void addToCart(const string& user, const string& rid, const string& item, int qty) {
        auto& m = rs.at(rid).menu; if (!m.count(item) || !m[item].available) throw invalid_argument("item unavailable");
        auto& c = carts[user]; if (!c.second.empty() && c.first != rid) throw invalid_argument("cart has items from another restaurant");
        c.first = rid; c.second[item] += qty;
    }
    Bill price(const string& user, const Coupon* coupon = nullptr) const {
        auto& c = carts.at(user); int sub = 0; for (auto& [id, q] : c.second) sub += rs.at(c.first).menu.at(id).price * q;
        int d = coupon ? coupon->discount(sub) : 0, tax = (sub - d) * 5 / 100;   // 5% tax on the discounted amount
        return {sub, d, tax, sub - d + tax};
    }
    int checkout(const string& user, const Coupon* coupon = nullptr) {
        auto it = carts.find(user); if (it == carts.end() || it->second.second.empty()) throw invalid_argument("empty cart");
        orders.push_back({(int)orders.size() + 1, user, it->second.first, it->second.second, price(user, coupon)}); carts.erase(it);
        return orders.back().id;
    }
    bool advance(int id, Status to) { auto& o = orders.at(id - 1); if (!next(o.status, to)) return false; o.status = to; return true; }
    const Order& order(int id) const { return orders.at(id - 1); }
};
int main() {
    FoodApp app; app.add({"R1", "Dosa Corner", {{"m1", {"m1", "Masala dosa", 120}}, {"m2", {"m2", "Filter coffee", 40}}, {"m3", {"m3", "Vada", 60, false}}}});
    app.add({"R2", "Biryani House", {{"b1", {"b1", "Veg biryani", 220}}}});
    app.addToCart("asha", "R1", "m1", 2); app.addToCart("asha", "R1", "m2", 1);
    bool threw = false; try { app.addToCart("asha", "R2", "b1", 1); } catch (const invalid_argument&) { threw = true; } assert(threw);
    threw = false; try { app.addToCart("asha", "R1", "m3", 1); } catch (const invalid_argument&) { threw = true; } assert(threw);
    FlatOff flat(50, 250); PercentOff pct(20, 30);
    Bill b = app.price("asha", &flat); assert(b.subtotal == 280 && b.discount == 50 && b.tax == 11 && b.total == 241);
    b = app.price("asha", &pct); assert(b.discount == 30 && b.total == 250 + 12);
    int id = app.checkout("asha", &flat); assert(app.order(id).bill.total == 241);
    assert(!app.advance(id, Status::Preparing) && app.advance(id, Status::Accepted) && app.advance(id, Status::Preparing));
    assert(!app.advance(id, Status::Cancelled) && app.advance(id, Status::OutForDelivery) && app.advance(id, Status::Delivered) && !app.advance(id, Status::Delivered));
    app.addToCart("ravi", "R2", "b1", 1); int id2 = app.checkout("ravi"); assert(app.advance(id2, Status::Cancelled) && !app.advance(id2, Status::Accepted));
    cout << "food ordering ok\n";
}
