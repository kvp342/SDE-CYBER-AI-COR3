LOW-LEVEL DESIGN · 6 DESIGNS

# LLD pack with code that runs

Six designs that come up in machine-coding and LLD rounds. Each has the requirements to state first, a class diagram in text, the key design decisions, follow-up questions, and a complete C++17 program with a demo that checks its own behaviour. Status: all six compile with -Wall -Wextra and pass their checks under AddressSanitizer and UndefinedBehaviorSanitizer.

**How to practise.** Read the requirements, set a 45-minute timer, and write your own design and code before you look. Then compare decisions, not just syntax. In the interview: clarify requirements, list entities, draw classes and relationships, write the core methods, then discuss extensions. See the [OOP](knowledge-base/core-cs.md#oop-the-four-pillars) and [SOLID](knowledge-base/core-cs.md#solid-and-design-patterns) Knowledge Base pages.

| \#  | Design                                                                                                               | Code                   |
|-----|----------------------------------------------------------------------------------------------------------------------|------------------------|
| 1   | [Parking lot](#01-parking-lot)A common machine-coding question; tests modelling and extensibility.                           | `lld/parking_lot.cpp`  |
| 2   | [Library management](#02-library-management)Classic OOP question: entities, state transitions and notifications.                    | `lld/library.cpp`      |
| 3   | [Splitwise (expense sharing)](#03-splitwise-expense-sharing)A common machine-coding question; tests money handling and a small algorithm. | `lld/splitwise.cpp`    |
| 4   | [Elevator system](#04-elevator-system)Tests state modelling and a scheduling policy; interviewers care about the reasoning.     | `lld/elevator.cpp`     |
| 5   | [Rate limiter](#05-rate-limiter)Common in backend and security interviews; also a system design building block.              | `lld/rate_limiter.cpp` |
| 6   | [LRU cache](#06-lru-cache)Asked as both DSA (LeetCode 146) and LLD; generic and O(1) is expected.                         | `lld/lru_cache.cpp`    |

Compile any design: `g++ -std=c++17 -Wall -pthread lld/parking_lot.cpp && ./a.out`

## 01. Parking lot

A common machine-coding question; tests modelling and extensibility.

### Requirements to confirm

- Levels with spots of three sizes; bikes, cars and trucks
- Park in the nearest spot that fits; issue a ticket
- Charge on exit by started hour and vehicle size
- Report free spots

### Design decisions

- Strategy pattern for pricing: weekend or flat-rate pricing is a new class, not an edit to ParkingLot (open/closed).
- Smallest spot that fits on the lowest level keeps large spots free for trucks.
- Money as integers; time passed in so tests are deterministic.

### Classes

``` text
Vehicle { plate, size }            Spot { level, number, size, plate? }
Ticket { id, plate, level, spot, entryMinute }
PricingStrategy <<interface>>  fee(size, minutes)
   └── HourlyPricing
ParkingLot ◆── Spot[levels][spots]
           ◆── Ticket (active, by id)
           ──> PricingStrategy
  park(vehicle, minute) -> Ticket?    leave(ticketId, minute) -> fee
```

### Follow-up questions

- Multiple entry gates at once: lock per level, or an atomic spot claim.
- Electric-vehicle charging spots and reservations.
- How would you find a free spot in O(1)? (free lists per size per level)

### C++17 code (`lld/parking_lot.cpp`)

``` cpp
// Parking lot: levels of sized spots, nearest-fit allocation, tickets, pluggable pricing.
#include <cassert>
#include <iostream>
#include <map>
#include <memory>
#include <optional>
#include <string>
#include <vector>
using namespace std;

enum class Size { Small = 0, Medium = 1, Large = 2 };           // bike, car, truck

struct Vehicle { string plate; Size size; };

struct Spot {
    int level, number; Size size; optional<string> plate;        // plate set while occupied
    bool fits(const Vehicle& v) const { return !plate && size >= v.size; }
};

struct Ticket { int id; string plate; int level, spot; long long entryMinute; };

class PricingStrategy {                                          // Strategy: pricing can change without touching ParkingLot
public:
    virtual ~PricingStrategy() = default;
    virtual long long fee(Size s, long long minutes) const = 0;  // in rupees
};
class HourlyPricing : public PricingStrategy {
    map<Size, long long> perHour{{Size::Small, 10}, {Size::Medium, 30}, {Size::Large, 60}};
public:
    long long fee(Size s, long long minutes) const override { return perHour.at(s) * ((minutes + 59) / 60); }  // started hours
};

class ParkingLot {
    vector<vector<Spot>> levels;
    map<int, Ticket> active;                                     // ticket id -> ticket
    map<string, Size> sizeOf;
    unique_ptr<PricingStrategy> pricing;
    int nextTicket = 1;
public:
    ParkingLot(const vector<vector<Size>>& layout, unique_ptr<PricingStrategy> p) : pricing(move(p)) {
        for (int l = 0; l < (int)layout.size(); l++) {
            levels.emplace_back();
            for (int i = 0; i < (int)layout[l].size(); i++) levels[l].push_back({l, i, layout[l][i], nullopt});
        }
    }
    // Nearest fit: lowest level, then the smallest spot that fits (keeps large spots for trucks).
    optional<Ticket> park(const Vehicle& v, long long minute) {
        Spot* best = nullptr;
        for (auto& level : levels) {
            for (auto& s : level) if (s.fits(v) && (!best || s.size < best->size)) best = &s;
            if (best) break;
        }
        if (!best) return nullopt;
        best->plate = v.plate; sizeOf[v.plate] = v.size;
        Ticket t{nextTicket++, v.plate, best->level, best->number, minute};
        active[t.id] = t;
        return t;
    }
    long long leave(int ticketId, long long minute) {
        auto it = active.find(ticketId);
        if (it == active.end()) throw invalid_argument("unknown ticket");
        Ticket t = it->second; active.erase(it);
        levels[t.level][t.spot].plate.reset();
        return pricing->fee(sizeOf[t.plate], minute - t.entryMinute);
    }
    int freeSpots() const { int n = 0; for (auto& l : levels) for (auto& s : l) n += !s.plate; return n; }
};

int main() {
    ParkingLot lot({{Size::Small, Size::Medium, Size::Large}, {Size::Medium, Size::Medium}}, make_unique<HourlyPricing>());
    auto car = lot.park({"KA01", Size::Medium}, 0);
    assert(car && car->level == 0 && car->spot == 1);            // medium spot, not the large one
    auto truck = lot.park({"TN09", Size::Large}, 0);
    assert(truck && truck->spot == 2);
    auto bike = lot.park({"AP07", Size::Small}, 0);
    assert(bike && bike->spot == 0);
    auto car2 = lot.park({"MH12", Size::Medium}, 10);
    assert(car2 && car2->level == 1);                            // level 0 full
    assert(!lot.park({"DL03", Size::Large}, 20));                // no large spot left
    assert(lot.leave(car->id, 61) == 60);                        // 61 minutes = 2 started hours x 30
    assert(lot.leave(truck->id, 30) == 60);
    assert(lot.freeSpots() == 3);
    try { lot.leave(999, 0); assert(false); } catch (const invalid_argument&) {}
    cout << "parking lot ok\n";
}
```

## 02. Library management

Classic OOP question: entities, state transitions and notifications.

### Requirements to confirm

- Books with several copies; members with a loan limit
- Check out and return with a due date; fine for late returns
- Reserve a book when no copy is free; notify the first waiting member
- A held copy can only be taken by that member

### Design decisions

- Copy status is a small state machine: Available → Loaned → (OnHold →) Loaned → Available.
- Observer for notifications: email or SMS senders subscribe without the Library knowing about them.
- FIFO queue per ISBN makes holds fair.

### Classes

``` text
Book { isbn, title }   Copy { id, isbn, status: Available | Loaned | OnHold }
Member { id, name, maxLoans }   Loan { copyId, memberId, day, due }
Library ◆── Book, Copy, Member, Loan
        ◆── holds: isbn -> queue<memberId>
        ──> listeners (Observer)  notify(memberId, message)
  checkout(member, isbn, day)  giveBack(copy, day) -> fine  reserve(member, isbn)
```

### Follow-up questions

- Hold expiry if the member does not collect in 3 days.
- Search by title or author (an index or full-text search).
- Concurrency: two members checking out the last copy at once.

### C++17 code (`lld/library.cpp`)

``` cpp
// Library: books and copies, members, loans with due dates and fines, reservations with notification (Observer).
#include <cassert>
#include <deque>
#include <functional>
#include <iostream>
#include <map>
#include <string>
#include <vector>
using namespace std;

struct Book { string isbn, title; };
enum class CopyStatus { Available, Loaned, OnHold };
struct Copy { int id; string isbn; CopyStatus status = CopyStatus::Available; };
struct Member { int id; string name; int maxLoans = 3; };
struct Loan { int copyId, memberId, day, due; };

class Library {
    map<string, Book> books;
    map<int, Copy> copies;
    map<int, Member> members;
    map<int, Loan> loans;                                        // copy id -> loan
    map<string, deque<int>> holds;                               // isbn -> waiting member ids (FIFO)
    map<int, int> holdFor;                                       // copy id -> member it is held for
    vector<function<void(int, const string&)>> listeners;        // Observer: notify(memberId, message)
    int nextCopy = 1;
    static constexpr int LOAN_DAYS = 14, FINE_PER_DAY = 2;
    void notify(int m, const string& msg) { for (auto& f : listeners) f(m, msg); }
    int loansOf(int m) const { int n = 0; for (auto& [c, l] : loans) n += l.memberId == m; return n; }
public:
    void onNotify(function<void(int, const string&)> f) { listeners.push_back(move(f)); }
    void addBook(const Book& b, int count) { books[b.isbn] = b; for (int i = 0; i < count; i++) { copies[nextCopy] = {nextCopy, b.isbn}; nextCopy++; } }
    void addMember(const Member& m) { members[m.id] = m; }

    int checkout(int memberId, const string& isbn, int day) {     // returns copy id, or -1
        if (loansOf(memberId) >= members.at(memberId).maxLoans) return -1;
        for (auto& [id, c] : copies) {
            bool heldForMe = c.status == CopyStatus::OnHold && holdFor[id] == memberId;
            if (c.isbn == isbn && (c.status == CopyStatus::Available || heldForMe)) {
                if (heldForMe) { holdFor.erase(id); holds[isbn].pop_front(); }
                c.status = CopyStatus::Loaned;
                loans[id] = {id, memberId, day, day + LOAN_DAYS};
                return id;
            }
        }
        return -1;
    }
    void reserve(int memberId, const string& isbn) { holds[isbn].push_back(memberId); }

    int giveBack(int copyId, int day) {                          // returns the fine
        Loan l = loans.at(copyId); loans.erase(copyId);
        int fine = max(0, day - l.due) * FINE_PER_DAY;
        Copy& c = copies[copyId];
        auto& q = holds[c.isbn];
        if (!q.empty()) { c.status = CopyStatus::OnHold; holdFor[copyId] = q.front(); notify(q.front(), books[c.isbn].title + " is ready for you"); }
        else c.status = CopyStatus::Available;
        return fine;
    }
};

int main() {
    Library lib; vector<pair<int, string>> inbox;
    lib.onNotify([&](int m, const string& msg) { inbox.push_back({m, msg}); });
    lib.addBook({"978-0262046305", "Introduction to Algorithms"}, 1);
    lib.addMember({1, "Asha"}); lib.addMember({2, "Ravi"}); lib.addMember({3, "Meera", 1});
    int c = lib.checkout(1, "978-0262046305", 0);
    assert(c == 1 && lib.checkout(2, "978-0262046305", 0) == -1);    // no copy free
    lib.reserve(2, "978-0262046305");
    assert(lib.giveBack(c, 20) == 12);                                // 6 days late x 2
    assert(inbox.size() == 1 && inbox[0].first == 2);                 // Ravi notified
    assert(lib.checkout(3, "978-0262046305", 21) == -1);              // held for Ravi, not Meera
    assert(lib.checkout(2, "978-0262046305", 21) == 1);
    assert(lib.giveBack(1, 30) == 0);
    lib.addBook({"111", "Clean Code"}, 2);
    assert(lib.checkout(3, "111", 0) != -1 && lib.checkout(3, "111", 0) == -1);  // Meera's limit is 1
    cout << "library ok\n";
}
```

## 03. Splitwise (expense sharing)

A common machine-coding question; tests money handling and a small algorithm.

### Requirements to confirm

- Add an expense paid by one person and split among several
- Equal, exact-amount and percentage splits
- Show each person's net balance
- Suggest a short list of payments that settles everyone

### Design decisions

- Paise as 64-bit integers: no floating-point rounding; remainders go to named people so totals always match.
- Validation in each strategy (exact amounts add up, percentages add to 100).
- Settlement: greedy largest debtor pays largest creditor, at most n − 1 payments (minimum count is NP-hard in general).

### Classes

``` text
SplitStrategy <<interface>>  shares(total, people) -> amounts
   ├── EqualSplit   ├── ExactSplit(amounts)   └── PercentSplit(percentages)
Ledger ◆── net: user -> paise (positive = is owed)
  addExpense(payer, total, people, strategy)   balance(user)   settle() -> [(from, to, amount)]
```

### Follow-up questions

- Groups, currencies and exchange rates.
- Editing or deleting an expense (store expenses, recompute balances).
- Why is the minimum number of transactions hard? (subset-sum style partitioning)

### C++17 code (`lld/splitwise.cpp`)

``` cpp
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
```

## 04. Elevator system

Tests state modelling and a scheduling policy; interviewers care about the reasoning.

### Requirements to confirm

- Several cars; hall calls (from a floor) and car calls (from inside)
- Assign each hall call to the best car
- Cars serve stops in their direction before reversing (LOOK)
- Simulate time in ticks

### Design decisions

- An ordered set of stops gives the next stop up or down in O(log n).
- LOOK scheduling avoids starvation better than nearest-first.
- Cost = distance, plus the detour if the car must finish its sweep first.

### Classes

``` text
Dir { Idle, Up, Down }
Elevator { id, floor, dir, stops: ordered set<int> }
  addStop(f)  cost(f)  step()
Controller ◆── Elevator[]
  hallCall(floor) -> car id   carCall(car, floor)   tick(n)
```

### Follow-up questions

- Capacity and weight limits; express elevators for high floors.
- Peak-hour policies (morning up-peak).
- Making controller and cars run on separate threads safely.

### C++17 code (`lld/elevator.cpp`)

``` cpp
// Elevator system: each car runs LOOK (keep going while requests remain ahead, then reverse);
// the controller assigns a hall call to the car with the lowest estimated cost.
#include <cassert>
#include <cstdlib>
#include <iostream>
#include <set>
#include <vector>
using namespace std;

enum class Dir { Idle, Up, Down };

class Elevator {
public:
    int id, floor = 0; Dir dir = Dir::Idle; set<int> stops; vector<int> visited;
    explicit Elevator(int i) : id(i) {}
    void addStop(int f) { if (f != floor) stops.insert(f); }
    // Cost estimate: distance, plus a penalty if the car must turn around first.
    int cost(int f) const {
        int d = abs(f - floor);
        if (dir == Dir::Idle || (dir == Dir::Up && f >= floor) || (dir == Dir::Down && f <= floor)) return d;
        int turn = dir == Dir::Up ? *stops.rbegin() : *stops.begin();
        return abs(turn - floor) + abs(turn - f);
    }
    void step() {                                                // move one floor per tick
        if (stops.empty()) { dir = Dir::Idle; return; }
        if (dir == Dir::Idle) {                                  // start toward the nearest pending stop
            auto up = stops.upper_bound(floor);
            int dUp = up == stops.end() ? 1 << 30 : *up - floor;
            int dDown = up == stops.begin() ? 1 << 30 : floor - *prev(up);
            dir = dUp < dDown ? Dir::Up : Dir::Down;
        }
        if (dir == Dir::Up && stops.upper_bound(floor) == stops.end()) dir = Dir::Down;      // nothing above: reverse
        if (dir == Dir::Down && stops.lower_bound(floor) == stops.begin()) dir = Dir::Up;    // nothing below: reverse
        floor += dir == Dir::Up ? 1 : -1;
        if (stops.erase(floor)) visited.push_back(floor);
        if (stops.empty()) dir = Dir::Idle;
    }
};

class Controller {
public:
    vector<Elevator> cars;
    explicit Controller(int n) { for (int i = 0; i < n; i++) cars.emplace_back(i); }
    int hallCall(int f) {                                        // returns the car id chosen
        int best = 0;
        for (auto& c : cars) if (c.cost(f) < cars[best].cost(f)) best = c.id;
        cars[best].addStop(f);
        return best;
    }
    void carCall(int car, int f) { cars[car].addStop(f); }
    void tick(int n = 1) { while (n--) for (auto& c : cars) c.step(); }
};

int main() {
    Controller ctl(2);
    ctl.cars[1].floor = 10;
    assert(ctl.hallCall(2) == 0);                                // car 0 at floor 0 is closer
    assert(ctl.hallCall(9) == 1);                                // car 1 at floor 10 is closer
    ctl.tick(2); assert(ctl.cars[0].floor == 2 && ctl.cars[0].dir == Dir::Idle);
    ctl.carCall(0, 7); ctl.carCall(0, 4); ctl.carCall(0, 1);
    ctl.tick(1); assert(ctl.cars[0].floor == 1 && ctl.cars[0].dir == Dir::Down);   // nearest stop (1) first
    ctl.tick(6); assert(ctl.cars[0].floor == 7);                 // then sweeps up through 4 to 7
    assert((ctl.cars[0].visited == vector<int>{2, 1, 4, 7}));
    assert(ctl.cars[1].floor == 9);
    cout << "elevator ok\n";
}
```

## 05. Rate limiter

Common in backend and security interviews; also a system design building block.

### Requirements to confirm

- Limit requests per client
- Allow short bursts but cap the average rate
- Exact limits for sensitive endpoints such as login
- Safe under concurrent requests

### Design decisions

- Token bucket: O(1) memory per client, allows bursts; sliding log: exact but stores every timestamp.
- Clock injection makes time-based tests deterministic.
- A mutex guards shared state; tested with 8 threads (exactly capacity granted) and ThreadSanitizer.

### Classes

``` text
RateLimiter <<interface>>  allow(client) -> bool
   ├── TokenBucket(capacity, ratePerSec, clock)      buckets: client -> {tokens, last}
   └── SlidingWindowLog(limit, windowSec, clock)    log: client -> deque<timestamps>
Clock = function<double()>  (injected; tests use a fake clock)
```

### Follow-up questions

- Distributed limiting: Redis with atomic scripts, or a gateway.
- Sliding window counter (two fixed windows weighted) as a cheaper approximation.
- What to return: HTTP 429 with Retry-After.

### C++17 code (`lld/rate_limiter.cpp`)

``` cpp
// Rate limiter: token bucket and sliding-window log behind one interface, per-client state,
// an injected clock for deterministic tests, and a mutex for thread safety.
#include <cassert>
#include <deque>
#include <functional>
#include <iostream>
#include <memory>
#include <mutex>
#include <string>
#include <thread>
#include <unordered_map>
#include <vector>
using namespace std;
using Clock = function<double()>;                                 // seconds

class RateLimiter {
public:
    virtual ~RateLimiter() = default;
    virtual bool allow(const string& client) = 0;
};

class TokenBucket : public RateLimiter {                          // allows bursts up to capacity, refills steadily
    struct Bucket { double tokens, last; };
    double capacity, ratePerSec; Clock now; unordered_map<string, Bucket> b; mutex m;
public:
    TokenBucket(double cap, double rate, Clock c) : capacity(cap), ratePerSec(rate), now(move(c)) {}
    bool allow(const string& id) override {
        lock_guard<mutex> g(m);
        double t = now();
        auto it = b.find(id);
        if (it == b.end()) it = b.emplace(id, Bucket{capacity, t}).first;
        Bucket& k = it->second;
        k.tokens = min(capacity, k.tokens + (t - k.last) * ratePerSec); k.last = t;
        if (k.tokens < 1) return false;
        k.tokens -= 1; return true;
    }
};

class SlidingWindowLog : public RateLimiter {                     // exact: at most `limit` requests in any `window` seconds
    size_t limit; double window; Clock now; unordered_map<string, deque<double>> log; mutex m;
public:
    SlidingWindowLog(size_t l, double w, Clock c) : limit(l), window(w), now(move(c)) {}
    bool allow(const string& id) override {
        lock_guard<mutex> g(m);
        double t = now(); auto& q = log[id];
        while (!q.empty() && t - q.front() >= window) q.pop_front();
        if (q.size() >= limit) return false;
        q.push_back(t); return true;
    }
};

int main() {
    double fake = 0; Clock clock = [&] { return fake; };
    TokenBucket tb(3, 1.0, clock);                                // burst of 3, then 1 per second
    assert(tb.allow("a") && tb.allow("a") && tb.allow("a") && !tb.allow("a"));
    assert(tb.allow("b"));                                        // clients are independent
    fake = 1.0; assert(tb.allow("a") && !tb.allow("a"));
    fake = 10;  int ok = 0; for (int i = 0; i < 5; i++) ok += tb.allow("a"); assert(ok == 3);   // never above capacity

    fake = 0; SlidingWindowLog sw(2, 60, clock);
    assert(sw.allow("x") && sw.allow("x") && !sw.allow("x"));
    fake = 59.9; assert(!sw.allow("x"));
    fake = 60;   assert(sw.allow("x"));                           // the first request has left the window

    double frozen = 0; TokenBucket shared(1000, 0, [&] { return frozen; });
    int granted = 0; mutex gm; vector<thread> ts;
    for (int t = 0; t < 8; t++) ts.emplace_back([&] { int mine = 0; for (int i = 0; i < 500; i++) mine += shared.allow("api"); lock_guard<mutex> g(gm); granted += mine; });
    for (auto& t : ts) t.join();
    assert(granted == 1000);                                      // 4000 attempts, exactly capacity granted
    cout << "rate limiter ok\n";
}
```

## 06. LRU cache

Asked as both DSA (LeetCode 146) and LLD; generic and O(1) is expected.

### Requirements to confirm

- get(key) and put(key, value) in O(1)
- Evict the least recently used item when full
- Updating a key refreshes it
- Generic key and value types

### Design decisions

- list::splice moves a node to the front without invalidating iterators.
- optional\<V\> instead of a sentinel value such as -1.
- Capacity 0 rejected in the constructor.

### Classes

``` text
LRUCache<K, V>
  cap
  items: list<pair<K, V>>          front = most recent
  pos:   unordered_map<K, list iterator>
  get(k) -> optional<V>   put(k, v)   size()
```

### Follow-up questions

- Thread safety: one mutex, or sharded caches.
- LFU, TTL expiry, or size-based eviction.
- Why not std::map? (O(log n) and no recency order)

### C++17 code (`lld/lru_cache.cpp`)

``` cpp
// LRU cache: O(1) get and put with a doubly linked list (recency order) and a hash map (key -> list node).
#include <cassert>
#include <iostream>
#include <list>
#include <optional>
#include <string>
#include <unordered_map>
using namespace std;

template <class K, class V>
class LRUCache {
    size_t cap;
    list<pair<K, V>> items;                                       // front = most recently used
    unordered_map<K, typename list<pair<K, V>>::iterator> pos;
public:
    explicit LRUCache(size_t capacity) : cap(capacity) { if (!cap) throw invalid_argument("capacity must be positive"); }
    optional<V> get(const K& k) {
        auto it = pos.find(k);
        if (it == pos.end()) return nullopt;
        items.splice(items.begin(), items, it->second);          // move to front, iterators stay valid
        return it->second->second;
    }
    void put(const K& k, V v) {
        if (auto it = pos.find(k); it != pos.end()) {
            it->second->second = move(v);
            items.splice(items.begin(), items, it->second);
            return;
        }
        if (items.size() == cap) { pos.erase(items.back().first); items.pop_back(); }   // evict least recently used
        items.emplace_front(k, move(v));
        pos[k] = items.begin();
    }
    size_t size() const { return items.size(); }
};

int main() {
    LRUCache<int, string> c(2);
    c.put(1, "one"); c.put(2, "two");
    assert(c.get(1) == "one");                                    // 1 is now most recent
    c.put(3, "three");                                            // evicts 2
    assert(!c.get(2) && c.get(3) == "three");
    c.put(1, "uno");                                              // update keeps size
    assert(c.size() == 2 && c.get(1) == "uno");
    c.put(4, "four");                                             // evicts 3 (1 was used more recently)
    assert(!c.get(3) && c.get(4) == "four" && c.get(1) == "uno");
    try { LRUCache<int, int> bad(0); assert(false); } catch (const invalid_argument&) {}
    LRUCache<string, int> big(1000);
    for (int i = 0; i < 100000; i++) big.put(to_string(i % 1500), i);
    assert(big.size() == 1000);
    cout << "lru cache ok\n";
}
```
