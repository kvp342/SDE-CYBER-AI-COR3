GAP-FILL · FROM THE EXTERNAL ROADMAP

# The missing pieces with code that runs

Everything the external 6-month roadmap (Google Doc) lists that your kit did not already cover: one DSA problem, the ATM LLD, three machine-coding problems, segment and Fenwick trees with number theory, and an Instagram-style HLD at the end. Each has the requirements to state first, a class diagram in text, the key design decisions, follow-up questions, and a complete C++17 program with a demo that checks its own behaviour. Status: all six programs compile with -Wall -Wextra and pass their checks under AddressSanitizer and UndefinedBehaviorSanitizer.

**How to practise.** Read the requirements, set a 45-minute timer, and write your own design and code before you look. Then compare decisions, not just syntax. In the interview: clarify requirements, list entities, draw classes and relationships, write the core methods, then discuss extensions. See the [OOP](knowledge-base/core-cs.md#oop-the-four-pillars) and [SOLID](knowledge-base/core-cs.md#solid-and-design-patterns) Knowledge Base pages.

| \#  | Design                                                                                                                                                            | Code                      |
|-----|-------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------|
| 1   | [Invert Binary Tree (the one DSA gap)](#01-invert-binary-tree-the-one-dsa-gap)The only must-solve problem from the external roadmap that is in neither your worked solutions nor your A2Z sheet. | `gaps/invert_tree.cpp`    |
| 2   | [ATM (LLD)](#02-atm-lld)A classic state-machine LLD round; the external roadmap lists it and LLD packs I–II did not have it.                                          | `gaps/atm.cpp`            |
| 3   | [Food ordering (machine coding)](#03-food-ordering-machine-coding)Zomato/Swiggy-style machine-coding round: entities, a state machine and pricing rules.                                  | `gaps/food_ordering.cpp`  |
| 4   | [Cache with pluggable eviction (machine coding)](#04-cache-with-pluggable-eviction-machine-coding)Tests interfaces and O(1) data structures together: LRU and LFU behind one EvictionPolicy.              | `gaps/eviction_cache.cpp` |
| 5   | [Inventory management (machine coding)](#05-inventory-management-machine-coding)Entities, validation and an Observer for low-stock alerts.                                                       | `gaps/inventory.cpp`      |
| 6   | [Segment tree, Fenwick tree and number theory](#06-segment-tree-fenwick-tree-and-number-theory)Phase 7 of the external roadmap: range queries and the maths that OAs reuse.                              | `gaps/ds_math.cpp`        |
| 7   | [Instagram-style photo sharing (HLD)](#07-instagram-style-photo-sharing-hld)Upload pipeline, hybrid push/pull feed, estimates                                                                  | —                         |

Compile any design: `g++ -std=c++17 -Wall -pthread gaps/atm.cpp && ./a.out`

## 01. Invert Binary Tree (the one DSA gap)

The only must-solve problem from the external roadmap that is in neither your worked solutions nor your A2Z sheet.

### Requirements to confirm

- Swap the left and right child of every node
- Return the root
- Empty tree returns null

### Design decisions

- Recursion is the 3-line answer; BFS avoids deep recursion on a skewed tree.
- The test checks the level order 4, 7, 2, 9, 6, 3, 1 for both versions.

### Classes

``` text
invertRec(root):  swap children, recurse on both     O(n) time, O(h) stack
invertBfs(root):  queue; swap children of each node   O(n) time, O(width) queue
```

### Follow-up questions

- Is a tree symmetric? (compare left with the mirror of right)
- Do it without extra space (Morris-style traversal).

### C++17 code (`gaps/invert_tree.cpp`)

``` cpp
// Invert Binary Tree (LeetCode 226): swap the children of every node, recursively and iteratively (BFS).
#include <cassert>
#include <iostream>
#include <queue>
#include <utility>
#include <vector>
using namespace std;
struct TreeNode { int val; TreeNode *left = nullptr, *right = nullptr; explicit TreeNode(int v) : val(v) {} };
TreeNode* invertRec(TreeNode* r) { if (!r) return r; swap(r->left, r->right); invertRec(r->left); invertRec(r->right); return r; }
TreeNode* invertBfs(TreeNode* r) {
    queue<TreeNode*> q; if (r) q.push(r);
    while (!q.empty()) { auto n = q.front(); q.pop(); swap(n->left, n->right); if (n->left) q.push(n->left); if (n->right) q.push(n->right); }
    return r;
}
static TreeNode* build(const vector<int>& v, size_t i = 0) { if (i >= v.size() || v[i] < 0) return nullptr; auto n = new TreeNode(v[i]); n->left = build(v, 2 * i + 1); n->right = build(v, 2 * i + 2); return n; }
static void level(TreeNode* r, vector<int>& out) { queue<TreeNode*> q; q.push(r); while (!q.empty()) { auto n = q.front(); q.pop(); if (!n) continue; out.push_back(n->val); q.push(n->left); q.push(n->right); } }
static void free_tree(TreeNode* r) { if (!r) return; free_tree(r->left); free_tree(r->right); delete r; }
int main() {
    for (auto f : {invertRec, invertBfs}) {
        TreeNode* t = build({4, 2, 7, 1, 3, 6, 9}); f(t); vector<int> got; level(t, got);
        assert((got == vector<int>{4, 7, 2, 9, 6, 3, 1})); free_tree(t);
        assert(f(nullptr) == nullptr);
    }
    cout << "invert tree ok\n";
}
```

## 02. ATM (LLD)

A classic state-machine LLD round; the external roadmap lists it and LLD packs I–II did not have it.

### Requirements to confirm

- Insert card, enter PIN (3 tries, then the card is retained), withdraw, eject
- Withdrawals in multiples of 100, limited by balance and by the notes in the machine
- Only one card at a time

### Design decisions

- Explicit state enum: every operation checks the state first, so illegal sequences are rejected.
- Debit the bank only after the machine knows it can dispense; otherwise money is taken but not given.
- Greedy note selection is optimal for 100/200/500/2000; the test proves it against brute force for every amount up to 5,000.

### Classes

``` text
ATM ──> Bank (accounts: card -> {pin, balance})
  - state: Idle | CardInserted | Authenticated
  - notes: note value -> count
  + insert(card)  + enterPin(pin)  + withdraw(amount)  + eject()
  - plan(amount) -> notes?     (greedy, largest note first)
```

### Follow-up questions

- Model states as classes (State pattern) when each state has many operations.
- Concurrency between the ATM and the bank: reserve, dispense, then commit.
- What if the dispenser jams after debiting? (reversal transaction)

### C++17 code (`gaps/atm.cpp`)

``` cpp
// ATM: a state machine (Idle -> CardInserted -> Authenticated -> back to Idle), PIN attempts with card retention,
// withdrawals limited by balance and by the notes in the machine (greedy works for 100/200/500/2000 notes, checked by brute force).
#include <cassert>
#include <iostream>
#include <map>
#include <optional>
#include <string>
using namespace std;
enum class State { Idle, CardInserted, Authenticated };
struct Account { string pin; long long balance; };
class Bank { map<string, Account> acc; public:
    void open(const string& card, string pin, long long bal) { acc[card] = {move(pin), bal}; }
    bool checkPin(const string& c, const string& p) const { auto it = acc.find(c); return it != acc.end() && it->second.pin == p; }
    long long balance(const string& c) const { return acc.at(c).balance; }
    bool debit(const string& c, long long amt) { auto& a = acc.at(c); if (a.balance < amt) return false; a.balance -= amt; return true; } };
class ATM {
    Bank& bank; State st = State::Idle; string card; int tries = 0; map<int, int, greater<int>> notes;   // note -> count, largest first
public:
    explicit ATM(Bank& b) : bank(b) {}
    void load(int note, int count) { notes[note] += count; }
    State state() const { return st; }
    bool insert(const string& c) { if (st != State::Idle) return false; card = c; tries = 0; st = State::CardInserted; return true; }
    string enterPin(const string& p) {
        if (st != State::CardInserted) return "no card";
        if (bank.checkPin(card, p)) { st = State::Authenticated; return "ok"; }
        if (++tries == 3) { st = State::Idle; card.clear(); return "card retained"; }
        return "wrong pin";
    }
    optional<map<int, int, greater<int>>> plan(long long amt) const {      // greedy over available notes
        map<int, int, greater<int>> out; for (auto [n, c] : notes) { long long k = min<long long>(c, amt / n); if (k) out[n] = (int)k; amt -= k * n; }
        if (amt) return nullopt;
        return out;
    }
    string withdraw(long long amt) {
        if (st != State::Authenticated) return "not authenticated";
        if (amt <= 0 || amt % 100) return "amount must be a multiple of 100";
        auto p = plan(amt); if (!p) return "cannot dispense this amount";
        if (!bank.debit(card, amt)) return "insufficient funds";
        for (auto [n, c] : *p) notes[n] -= c;
        return "dispensed";
    }
    void eject() { st = State::Idle; card.clear(); }
};
int main() {
    Bank bank; bank.open("C1", "1234", 10000); ATM atm(bank); atm.load(500, 4); atm.load(200, 5); atm.load(100, 2);
    assert(atm.withdraw(500) == "not authenticated" && atm.insert("C1") && !atm.insert("C2"));
    assert(atm.enterPin("0000") == "wrong pin" && atm.enterPin("1234") == "ok" && atm.state() == State::Authenticated);
    assert(atm.withdraw(150) == "amount must be a multiple of 100" && atm.withdraw(2500) == "dispensed" && bank.balance("C1") == 7500);
    // 2500 used 4x500 + 2x200 + 1x100, so the machine now holds 3x200 + 1x100 = 700
    assert(atm.withdraw(800) == "cannot dispense this amount" && bank.balance("C1") == 7500);   // more than the notes in the machine
    assert(atm.withdraw(700) == "dispensed" && atm.withdraw(100) == "cannot dispense this amount" && bank.balance("C1") == 6800);
    atm.eject(); bank.open("C2", "9999", 50); atm.insert("C2");
    assert(atm.enterPin("1") == "wrong pin" && atm.enterPin("2") == "wrong pin" && atm.enterPin("3") == "card retained" && atm.state() == State::Idle);
    for (int amt = 100; amt <= 5000; amt += 100) {                    // greedy = optimal for these notes: compare with brute force
        int best = 1 << 30; for (int a = 0; a * 2000 <= amt; a++) for (int b = 0; a * 2000 + b * 500 <= amt; b++) for (int c = 0; a * 2000 + b * 500 + c * 200 <= amt; c++) { int d = amt - a * 2000 - b * 500 - c * 200; if (d % 100 == 0) best = min(best, a + b + c + d / 100); }
        int g = 0, left = amt; for (int n : {2000, 500, 200, 100}) { g += left / n; left %= n; }
        assert(g == best);
    }
    cout << "atm ok\n";
}
```

## 03. Food ordering (machine coding)

Zomato/Swiggy-style machine-coding round: entities, a state machine and pricing rules.

### Requirements to confirm

- Restaurants with menus; unavailable items cannot be added
- A cart holds items from one restaurant only
- Coupons (flat or percentage with a cap) and 5% tax
- Order states PLACED → ACCEPTED → PREPARING → OUT_FOR_DELIVERY → DELIVERED; cancel only before PREPARING

### Design decisions

- Coupons are a Strategy: a new offer is a new class.
- Transitions are checked in one function, so illegal jumps (PLACED → PREPARING, cancelling after PREPARING) are rejected.
- Money in whole rupees as integers; the test checks a full bill (280 − 50 + 11 = 241).

### Classes

``` text
FoodApp
  - restaurants: id -> Restaurant { menu: id -> MenuItem }
  - carts: user -> (restaurant, items)
  - orders[]
Coupon <<interface>> discount(subtotal)  ├── FlatOff  └── PercentOff
  + addToCart  + price(user, coupon) -> Bill  + checkout  + advance(orderId, status)
```

### Follow-up questions

- Assign a delivery agent (nearest free agent) and track location.
- Restaurant opening hours and item stock.
- Splitting one cart across restaurants into several orders.

### C++17 code (`gaps/food_ordering.cpp`)

``` cpp
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
```

## 04. Cache with pluggable eviction (machine coding)

Tests interfaces and O(1) data structures together: LRU and LFU behind one EvictionPolicy.

### Requirements to confirm

- get and put in O(1)
- Fixed capacity; evict according to a policy chosen at construction
- LRU and LFU (ties in LFU: least recently used first)

### Design decisions

- The cache never knows which policy it uses (Strategy + dependency injection).
- LFU tracks the minimum frequency so victim() is O(1) amortised.
- Tests cover LRU order, LFU frequency and tie-break, and capacity 0.

### Classes

``` text
EvictionPolicy<K> <<interface>> touched(k) added(k) removed(k) victim()
   ├── LRU<K>  (list + map to list positions)
   └── LFU<K>  (frequency -> list buckets, map to positions, minFreq)
Cache<K, V> ◆── data map, ──> EvictionPolicy
```

### Follow-up questions

- TTL on top (see the key–value store in LLD pack II).
- Thread safety: one mutex, or sharding by key.
- FIFO or random policies as one more class each.

### C++17 code (`gaps/eviction_cache.cpp`)

``` cpp
// Machine coding: a cache with a pluggable eviction policy (Strategy pattern): LRU and LFU behind one interface, O(1) per operation.
#include <cassert>
#include <iostream>
#include <list>
#include <memory>
#include <optional>
#include <string>
#include <unordered_map>
using namespace std;
template <class K> struct EvictionPolicy { virtual ~EvictionPolicy() = default; virtual void touched(const K&) = 0; virtual void added(const K&) = 0; virtual void removed(const K&) = 0; virtual K victim() = 0; };
template <class K> class LRU : public EvictionPolicy<K> {
    list<K> order; unordered_map<K, typename list<K>::iterator> pos;          // front = most recent
public:
    void touched(const K& k) override { order.splice(order.begin(), order, pos.at(k)); }
    void added(const K& k) override { order.push_front(k); pos[k] = order.begin(); }
    void removed(const K& k) override { order.erase(pos.at(k)); pos.erase(k); }
    K victim() override { return order.back(); }
};
template <class K> class LFU : public EvictionPolicy<K> {   // frequency buckets; ties broken by least recent within the lowest frequency
    unordered_map<K, int> freq; unordered_map<int, list<K>> buckets; unordered_map<K, typename list<K>::iterator> pos; int minF = 0;
    void place(const K& k, int f) { buckets[f].push_front(k); pos[k] = buckets[f].begin(); freq[k] = f; }
public:
    void touched(const K& k) override { int f = freq.at(k); buckets[f].erase(pos[k]); if (buckets[f].empty() && minF == f) minF++; place(k, f + 1); }
    void added(const K& k) override { place(k, 1); minF = 1; }
    void removed(const K& k) override { int f = freq.at(k); buckets[f].erase(pos[k]); pos.erase(k); freq.erase(k); }
    K victim() override { while (buckets[minF].empty()) minF++; return buckets[minF].back(); }
};
template <class K, class V> class Cache {
    size_t cap; unordered_map<K, V> data; unique_ptr<EvictionPolicy<K>> policy;
public:
    Cache(size_t c, unique_ptr<EvictionPolicy<K>> p) : cap(c), policy(move(p)) {}
    optional<V> get(const K& k) { auto it = data.find(k); if (it == data.end()) return nullopt; policy->touched(k); return it->second; }
    void put(const K& k, V v) {
        if (cap == 0) return;
        if (data.count(k)) { data[k] = move(v); policy->touched(k); return; }
        if (data.size() == cap) { K old = policy->victim(); policy->removed(old); data.erase(old); }
        data[k] = move(v); policy->added(k);
    }
    size_t size() const { return data.size(); }
};
int main() {
    Cache<int, string> lru(2, make_unique<LRU<int>>());
    lru.put(1, "a"); lru.put(2, "b"); assert(lru.get(1) == "a"); lru.put(3, "c");          // 2 is least recent
    assert(!lru.get(2) && lru.get(1) == "a" && lru.get(3) == "c");
    Cache<int, int> lfu(2, make_unique<LFU<int>>());
    lfu.put(1, 1); lfu.put(2, 2); lfu.get(1); lfu.put(3, 3);                               // 2 has the lowest frequency
    assert(!lfu.get(2) && lfu.get(3) == 3); lfu.put(4, 4);                                  // 1 and 3 both have freq 2; 1 is less recent
    assert(!lfu.get(1) && lfu.get(3) == 3 && lfu.get(4) == 4 && lfu.size() == 2);
    Cache<int, int> zero(0, make_unique<LRU<int>>()); zero.put(1, 1); assert(!zero.get(1));
    cout << "eviction cache ok\n";
}
```

## 05. Inventory management (machine coding)

Entities, validation and an Observer for low-stock alerts.

### Requirements to confirm

- Products with SKU, category, quantity and reorder level
- Stock in and stock out with validation
- Alert subscribers once when stock falls to the reorder level
- List by category and list low-stock items

### Design decisions

- Alerts fire on crossing the level, not on every sale below it, so subscribers are not spammed.
- Invalid quantities and duplicate SKUs are rejected.
- Observer as a list of callbacks: email, dashboard and reorder service can subscribe independently.

### Classes

``` text
Inventory
  - items: sku -> Product { name, category, qty, reorderLevel }
  - subscribers: function(Product)
  + add  + stockIn  + stockOut -> bool  + byCategory  + lowStock  + subscribe
```

### Follow-up questions

- Multiple warehouses and transfers between them.
- Reservations for pending orders (see the checkout design in system design II).
- Audit log of every stock change.

### C++17 code (`gaps/inventory.cpp`)

``` cpp
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
```

## 06. Segment tree, Fenwick tree and number theory

Phase 7 of the external roadmap: range queries and the maths that OAs reuse.

### Requirements to confirm

- Range sum with point updates in O(log n): segment tree and Fenwick tree
- All primes up to N: sieve of Eratosthenes
- Fast modular power, modular inverse (prime modulus), gcd and lcm

### Design decisions

- Both trees are checked against brute-force sums over 2,000 random updates and queries.
- The sieve gives 78,498 primes below 10^6 (the known count).
- modpow uses 128-bit products so b × b never overflows for moduli near 10^18.

### Classes

``` text
SegTree(a)   set(i, v)   sum(l, r)   iterative, 2n array
BIT(n)       add(i, d)   prefix(i)   sum(l, r)
sieve(n) -> primes   modpow(b, e, m)   modinv(a, p) = a^(p-2) mod p
```

### Follow-up questions

- Range updates with lazy propagation; range minimum instead of sum.
- Count inversions or 'smaller after self' with a BIT (OA pack II has one).
- Segmented sieve for primes in a range \[L, R\].

### C++17 code (`gaps/ds_math.cpp`)

``` cpp
// Advanced topics in one file: segment tree (range sum, point update), Fenwick tree (BIT), sieve of Eratosthenes,
// fast modular exponentiation, gcd/lcm, and modular inverse; each checked against brute force.
#include <cassert>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <random>
#include <vector>
using namespace std;
struct SegTree {                                             // iterative, size n, sums
    int n; vector<long long> t;
    explicit SegTree(const vector<long long>& a) : n(a.size()), t(2 * a.size()) { for (int i = 0; i < n; i++) t[n + i] = a[i]; for (int i = n - 1; i > 0; i--) t[i] = t[2 * i] + t[2 * i + 1]; }
    void set(int i, long long v) { for (t[i += n] = v; i > 1; i >>= 1) t[i >> 1] = t[i] + t[i ^ 1]; }
    long long sum(int l, int r) const { long long s = 0; for (l += n, r += n; l < r; l >>= 1, r >>= 1) { if (l & 1) s += t[l++]; if (r & 1) s += t[--r]; } return s; }   // [l, r)
};
struct BIT {                                                 // 1-indexed internally; add and prefix sums in O(log n)
    vector<long long> f; explicit BIT(int n) : f(n + 1) {}
    void add(int i, long long d) { for (i++; i < (int)f.size(); i += i & -i) f[i] += d; }
    long long prefix(int i) const { long long s = 0; for (; i > 0; i -= i & -i) s += f[i]; return s; }   // sum of [0, i)
    long long sum(int l, int r) const { return prefix(r) - prefix(l); }
};
vector<int> sieve(int n) { vector<bool> comp(n + 1); vector<int> p; for (int i = 2; i <= n; i++) { if (comp[i]) continue; p.push_back(i); for (long long j = 1LL * i * i; j <= n; j += i) comp[j] = true; } return p; }
long long modpow(long long b, long long e, long long m) { long long r = 1 % m; b %= m; while (e) { if (e & 1) r = (__int128)r * b % m; b = (__int128)b * b % m; e >>= 1; } return r; }
long long modinv(long long a, long long p) { return modpow(a, p - 2, p); }   // p prime (Fermat)
int main() {
    mt19937 rng(7); vector<long long> a(37); for (auto& x : a) x = rng() % 100;
    SegTree st(a); BIT bit(a.size()); for (size_t i = 0; i < a.size(); i++) bit.add(i, a[i]);
    for (int it = 0; it < 2000; it++) {
        int i = rng() % a.size(); long long v = rng() % 100; st.set(i, v); bit.add(i, v - a[i]); a[i] = v;
        int l = rng() % a.size(), r = rng() % (a.size() + 1); if (l > r) swap(l, r);
        long long brute = accumulate(a.begin() + l, a.begin() + r, 0LL);
        assert(st.sum(l, r) == brute && bit.sum(l, r) == brute);
    }
    auto p = sieve(100); assert(p.size() == 25 && p.back() == 97);
    assert(sieve(1'000'000).size() == 78498);                 // known count of primes below 10^6
    const long long MOD = 1'000'000'007;
    assert(modpow(2, 10, MOD) == 1024 && modpow(3, 0, 7) == 1 && modpow(5, 3, 1) == 0);
    long long x = 1; for (int i = 0; i < 1000; i++) x = x * 7 % MOD; assert(modpow(7, 1000, MOD) == x);
    assert(modinv(3, MOD) * 3 % MOD == 1 && gcd(84, 126) == 42 && lcm(12, 18) == 36);
    cout << "data structures and maths ok\n";
}
```

## 07. Instagram-style photo sharing (HLD)

The one HLD from the external roadmap that the two system design packs did not cover end to end (the news-feed design covers the feed half).

### Requirements

- Upload photos with captions; view a profile grid
- Follow users; home feed of followed users' photos, newest first
- Likes and comments
- Fast feed loads worldwide; uploads durable; feed can be a few seconds stale

### Estimates (assumptions: 100 M daily users, 0.1 uploads and 20 feed views per user a day, 2 MB per photo)

- Photos uploaded per day: **10.0 M**
- Photo storage per day incl. thumbnails (bytes): **24.0 T**
- Storage per year (bytes): **8.8 P**
- Feed requests per day: **2.0 G**
- Average feed requests/s: **23.1 K**
- Peak feed requests/s: **69.4 K**

### Design

``` text
Client ──> CDN (images) ──> Object storage (originals + resized versions)
Client ──> Load balancer ──> API servers ──> Post service ──> Posts DB (sharded by user_id)
                                 │                  └──> upload event ──> Queue ──> Resize workers ──> Object storage
                                 ├──> Feed service ──> Feed cache (Redis: user -> recent post ids)
                                 └──> Graph service ──> Follows DB       Fan-out workers <── Queue (new post)
```

- **Upload:** the client gets a pre-signed URL and uploads straight to object storage; a queue event triggers resizing into thumbnails; the post row stores the object keys.
- **Feed:** fan-out on write for normal users (push the new post id into each follower's feed cache); for accounts with millions of followers, pull their recent posts at read time and merge (the "celebrity problem").
- **Reads:** the feed service returns post ids from cache, hydrates them from a post cache, and image URLs point at the CDN.
- **Data:** posts(post_id, user_id, caption, keys, created_at) sharded by user_id; follows(follower, followee) indexed both ways; likes counted asynchronously.

### Trade-offs and follow-ups

- Push vs pull feeds: push makes reads cheap but writes heavy for big accounts; the hybrid fixes both.
- Ranking instead of newest-first: a ranking service scores candidate posts.
- Deleting a post must remove it from every pushed feed: store ids only and filter deleted ones at read time.
