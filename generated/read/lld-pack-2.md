LOW-LEVEL DESIGN · 6 MORE DESIGNS

# LLD pack II with code that runs

Six more designs that come up in machine-coding and LLD rounds, none repeated from LLD pack I. Each has the requirements to state first, a class diagram in text, the key design decisions, follow-up questions, and a complete C++17 program with a demo that checks its own behaviour. Status: all six compile with -Wall -Wextra and pass their checks under AddressSanitizer and UndefinedBehaviorSanitizer.

**How to practise.** Read the requirements, set a 45-minute timer, and write your own design and code before you look. Then compare decisions, not just syntax. In the interview: clarify requirements, list entities, draw classes and relationships, write the core methods, then discuss extensions. See the [OOP](knowledge-base/core-cs.md#oop-the-four-pillars) and [SOLID](knowledge-base/core-cs.md#solid-and-design-patterns) Knowledge Base pages.

| \#  | Design                                                                                                                                        | Code                       |
|-----|-----------------------------------------------------------------------------------------------------------------------------------------------|----------------------------|
| 1   | [Tic-tac-toe (N × N)](#01-tic-tac-toe-n--n)A favourite warm-up machine-coding round: clean state, validation and an O(1) win check.                        | `lld2/tic_tac_toe.cpp`     |
| 2   | [Vending machine](#02-vending-machine)Tests state, money handling and an algorithm (change-making) in one design.                                         | `lld2/vending_machine.cpp` |
| 3   | [Movie ticket booking with seat holds](#03-movie-ticket-booking-with-seat-holds)The concurrency question behind BookMyShow-style designs: two people must never get one seat. | `lld2/movie_booking.cpp`   |
| 4   | [Logger with levels and sinks](#04-logger-with-levels-and-sinks)Shows interfaces, the open/closed principle and thread safety in a small space.                       | `lld2/logger.cpp`          |
| 5   | [Key–value store with TTL](#05-keyvalue-store-with-ttl)A small Redis: data structures, expiry and a subtle overwrite bug.                                        | `lld2/kv_store_ttl.cpp`    |
| 6   | [Snake and ladder](#06-snake-and-ladder)Machine-coding staple: rules as data, players in a queue, testable randomness.                                    | `lld2/snake_ladder.cpp`    |

Compile any design: `g++ -std=c++17 -Wall -pthread lld2/tic_tac_toe.cpp && ./a.out`

## 01. Tic-tac-toe (N × N)

A favourite warm-up machine-coding round: clean state, validation and an O(1) win check.

### Requirements to confirm

- Board size N, two players, X starts
- Reject moves outside the board, on a taken cell, out of turn, or after the game ends
- Detect win and draw after every move

### Design decisions

- Counters per row, column and diagonal make the win check O(1) instead of scanning the board (O(N)).
- Illegal moves throw with a clear message; the caller decides how to show them.
- The game owns its state; a UI or network layer only calls play().

### Classes

``` text
Game
  - n, moves, turn
  - board[n][n]
  - rows[n], cols[n], diag, anti     (+1 for X, -1 for O)
  + play(player, r, c) -> Ok | Win | Draw   (throws on illegal moves)
  + current() -> 'X' | 'O'
```

### Follow-up questions

- K-in-a-row on an M × N board (Gomoku): check runs from the last move.
- Undo: keep a move stack and reverse the counters.
- A bot player behind a Player interface (Strategy).

### C++17 code (`lld2/tic_tac_toe.cpp`)

``` cpp
// Tic-tac-toe for an N x N board: move validation, turn order, and O(1) win detection with row/column/diagonal counters.
#include <cassert>
#include <iostream>
#include <stdexcept>
#include <vector>
using namespace std;
enum class Result { Ok, Win, Draw };
class Game {
    int n, moves = 0, turn = 0;                                   // turn 0 = X, 1 = O
    vector<vector<char>> board; vector<int> rows, cols; int diag = 0, anti = 0; bool over = false;
public:
    explicit Game(int size) : n(size), board(size, vector<char>(size, '.')), rows(size), cols(size) {}
    char current() const { return turn ? 'O' : 'X'; }
    Result play(char who, int r, int c) {                       // throws invalid_argument on an illegal move
        if (over) throw invalid_argument("game is over");
        if (who != current()) throw invalid_argument("not your turn");
        if (r < 0 || c < 0 || r >= n || c >= n) throw invalid_argument("outside the board");
        if (board[r][c] != '.') throw invalid_argument("cell taken");
        board[r][c] = who; int d = who == 'X' ? 1 : -1; moves++;
        rows[r] += d; cols[c] += d; if (r == c) diag += d; if (r + c == n - 1) anti += d;
        if (abs(rows[r]) == n || abs(cols[c]) == n || abs(diag) == n || abs(anti) == n) { over = true; return Result::Win; }
        if (moves == n * n) { over = true; return Result::Draw; }
        turn ^= 1; return Result::Ok;
    }
};
static bool throws(Game& g, char w, int r, int c) { try { g.play(w, r, c); } catch (const invalid_argument&) { return true; } return false; }
int main() {
    Game g(3);                                                    // X wins on the top row
    assert(g.play('X', 0, 0) == Result::Ok && g.play('O', 1, 0) == Result::Ok && g.play('X', 0, 1) == Result::Ok && g.play('O', 1, 1) == Result::Ok);
    assert(g.play('X', 0, 2) == Result::Win && throws(g, 'O', 2, 2));
    Game d(3);                                                    // anti-diagonal win for O
    d.play('X', 0, 0); d.play('O', 0, 2); d.play('X', 1, 0); d.play('O', 1, 1); d.play('X', 2, 2); assert(d.play('O', 2, 0) == Result::Win);
    Game e(3); int seq[9][2] = {{0,0},{0,1},{0,2},{1,1},{1,0},{1,2},{2,1},{2,0},{2,2}}; Result last = Result::Ok;   // a draw
    for (int i = 0; i < 9; i++) last = e.play(i % 2 ? 'O' : 'X', seq[i][0], seq[i][1]);
    assert(last == Result::Draw);
    Game f(4); assert(throws(f, 'O', 0, 0) && !throws(f, 'X', 0, 0) && throws(f, 'O', 0, 0) && throws(f, 'O', 4, 0));
    cout << "tic-tac-toe ok\n";
}
```

## 02. Vending machine

Tests state, money handling and an algorithm (change-making) in one design.

### Requirements to confirm

- Items with codes, prices and stock
- Accept only some coins; show the balance
- Sell if the item exists, is in stock and is paid for, and exact change can be given
- Refund on request

### Design decisions

- Inserted coins join the float before change is computed, so they can be used for the change itself.
- Change uses a bounded-coin DP, not greedy: greedy fails when coins run out.
- Money as integers (smallest unit) to avoid floating-point errors.

### Classes

``` text
VendingMachine
  - items: code -> Item { name, price, qty }
  - coins: value -> count      (machine's float)
  - inserted[], credit
  + insert(coin) -> bool       + select(code) -> Sale { ok, reason, change }
  + refund() -> coins          - makeChange(amount, stock) -> coins?  (bounded coin DP)
```

### Follow-up questions

- Model states explicitly (Idle, HasMoney, Dispensing) with the State pattern.
- Card payments and a timeout that refunds automatically.
- Maintenance mode for restocking and collecting coins.

### C++17 code (`lld2/vending_machine.cpp`)

``` cpp
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
```

## 03. Movie ticket booking with seat holds

The concurrency question behind BookMyShow-style designs: two people must never get one seat.

### Requirements to confirm

- Show with named seats
- Hold several seats all-or-nothing for a few minutes
- Confirm only your own unexpired hold
- Expired holds free the seat
- Many users at once

### Design decisions

- One mutex per show makes hold() atomic: the test races 16 threads for one seat and exactly one wins.
- Lazy expiry: a hold is checked when touched, so no timer thread is needed.
- The clock is injected, so expiry is tested without sleeping.

### Classes

``` text
Show
  - seats: id -> State { Free | Held | Booked, user, until }
  - mutex, clock, holdSecs
  + hold(user, seatIds) -> bool       (all or nothing)
  + confirm(user, seatIds) -> bool
  + status(seatId) -> Seat
```

### Follow-up questions

- Scale out: per-show locks, or a database row lock / conditional update (UPDATE … WHERE status = 'Free').
- Payment failure after a hold: release, with an idempotent confirm.
- Distributed holds with Redis SET NX and a TTL.

### C++17 code (`lld2/movie_booking.cpp`)

``` cpp
// Movie ticket booking: seats are held for a few minutes, then confirmed or released; holds expire; concurrent holds on one seat:
// exactly one user wins. Clock is injected for tests.
#include <cassert>
#include <functional>
#include <iostream>
#include <map>
#include <mutex>
#include <string>
#include <thread>
#include <vector>
using namespace std;
enum class Seat { Free, Held, Booked };
class Show {
    struct State { Seat s = Seat::Free; string user; long long until = 0; };
    map<string, State> seats; mutex m; function<long long()> now; long long holdSecs;
    void expire(State& st) { if (st.s == Seat::Held && now() >= st.until) st = State{}; }
public:
    Show(vector<string> ids, function<long long()> clock, long long hold = 300) : now(move(clock)), holdSecs(hold) { for (auto& id : ids) seats[id]; }
    bool hold(const string& user, const vector<string>& ids) {   // all-or-nothing
        lock_guard<mutex> g(m);
        for (auto& id : ids) { auto it = seats.find(id); if (it == seats.end()) return false; expire(it->second); if (it->second.s != Seat::Free) return false; }
        for (auto& id : ids) seats[id] = {Seat::Held, user, now() + holdSecs};
        return true;
    }
    bool confirm(const string& user, const vector<string>& ids) {
        lock_guard<mutex> g(m);
        for (auto& id : ids) { auto& st = seats.at(id); expire(st); if (st.s != Seat::Held || st.user != user) return false; }
        for (auto& id : ids) seats[id].s = Seat::Booked;
        return true;
    }
    Seat status(const string& id) { lock_guard<mutex> g(m); auto& st = seats.at(id); expire(st); return st.s; }
};
int main() {
    long long t = 0; Show s({"A1", "A2", "A3"}, [&] { return t; });
    assert(s.hold("asha", {"A1", "A2"}) && !s.hold("ravi", {"A2", "A3"}) && s.status("A3") == Seat::Free);   // all-or-nothing
    assert(!s.confirm("ravi", {"A1"}) && s.confirm("asha", {"A1", "A2"}) && s.status("A1") == Seat::Booked);
    assert(s.hold("ravi", {"A3"})); t = 299; assert(s.status("A3") == Seat::Held); t = 300; assert(s.status("A3") == Seat::Free);   // hold expired
    assert(!s.confirm("ravi", {"A3"}) && s.hold("meera", {"A3"}));
    long long t2 = 0; Show big({"B1"}, [&] { return t2; }); int wins = 0; mutex wm; vector<thread> ts;
    for (int i = 0; i < 16; i++) ts.emplace_back([&, i] { if (big.hold("user" + to_string(i), {"B1"})) { lock_guard<mutex> g(wm); wins++; } });
    for (auto& th : ts) th.join();
    assert(wins == 1);                                            // 16 threads race for one seat
    cout << "movie booking ok\n";
}
```

## 04. Logger with levels and sinks

Shows interfaces, the open/closed principle and thread safety in a small space.

### Requirements to confirm

- Levels DEBUG \< INFO \< WARN \< ERROR
- Several outputs (console, memory, file), each with its own minimum level
- Consistent line format
- Safe to call from many threads

### Design decisions

- New outputs are new Sink classes; Logger never changes (open/closed).
- Format once per call, then fan out to the sinks.
- One mutex around the fan-out: the test writes 2,000 lines from 8 threads with none lost.

### Classes

``` text
Sink <<interface>>  { min: Level; write(line) }
   ├── StreamSink(ostream)
   └── MemorySink (lines[])
Logger ◆── Sink[]
  + add(sink)   + log(level, msg)   + debug/info/warn/error(msg)
```

### Follow-up questions

- Asynchronous logging with a queue and a background writer.
- Log rotation by size or date in a FileSink.
- Structured (JSON) logs for a SIEM.

### C++17 code (`lld2/logger.cpp`)

``` cpp
// Logger: levels, several sinks each with its own minimum level, a formatter, and thread safety.
#include <cassert>
#include <iostream>
#include <memory>
#include <mutex>
#include <sstream>
#include <string>
#include <thread>
#include <vector>
using namespace std;
enum class Level { Debug, Info, Warn, Error };
static const char* name(Level l) { static const char* n[] = {"DEBUG", "INFO", "WARN", "ERROR"}; return n[(int)l]; }
class Sink { public: Level min; explicit Sink(Level m) : min(m) {} virtual ~Sink() = default; virtual void write(const string& line) = 0; };
class StreamSink : public Sink { ostream& os; public: StreamSink(ostream& o, Level m) : Sink(m), os(o) {} void write(const string& l) override { os << l << '\n'; } };
class MemorySink : public Sink { public: vector<string> lines; explicit MemorySink(Level m) : Sink(m) {} void write(const string& l) override { lines.push_back(l); } };
class Logger {
    vector<shared_ptr<Sink>> sinks; mutex m; string source;
public:
    explicit Logger(string src) : source(move(src)) {}
    void add(shared_ptr<Sink> s) { lock_guard<mutex> g(m); sinks.push_back(move(s)); }
    void log(Level l, const string& msg) {
        string line = string("[") + name(l) + "] " + source + ": " + msg;   // format once, outside the per-sink loop
        lock_guard<mutex> g(m);
        for (auto& s : sinks) if (l >= s->min) s->write(line);
    }
    void debug(const string& s) { log(Level::Debug, s); } void info(const string& s) { log(Level::Info, s); }
    void warn(const string& s) { log(Level::Warn, s); } void error(const string& s) { log(Level::Error, s); }
};
int main() {
    ostringstream console; auto mem = make_shared<MemorySink>(Level::Debug);
    Logger log("payments"); log.add(make_shared<StreamSink>(console, Level::Warn)); log.add(mem);
    log.debug("cache miss"); log.info("order 42 paid"); log.warn("retrying gateway"); log.error("gateway down");
    assert(console.str() == "[WARN] payments: retrying gateway\n[ERROR] payments: gateway down\n");
    assert(mem->lines.size() == 4 && mem->lines[0] == "[DEBUG] payments: cache miss");
    auto many = make_shared<MemorySink>(Level::Info); Logger l2("api"); l2.add(many); vector<thread> ts;
    for (int t = 0; t < 8; t++) ts.emplace_back([&, t] { for (int i = 0; i < 250; i++) l2.info("t" + to_string(t)); });
    for (auto& th : ts) th.join();
    assert(many->lines.size() == 2000);                           // no lost or torn lines
    cout << "logger ok\n";
}
```

## 05. Key–value store with TTL

A small Redis: data structures, expiry and a subtle overwrite bug.

### Requirements to confirm

- set(key, value, ttl?) / get / del
- Expired keys behave as missing
- Expired keys are cleaned up without scanning everything
- Overwriting a key replaces its expiry

### Design decisions

- Two expiry paths: lazy on get, and cleanup() popping the min-heap (Redis also combines lazy and active expiry).
- A version number per write: an old heap entry for an overwritten key is skipped instead of deleting the new value (the test checks exactly this).
- Expiry is exclusive at the deadline; the test pins it.

### Classes

``` text
KV
  - map: key -> Entry { value, expires, version }
  - heap: min (expires, version, key)
  - clock
  + set(k, v, ttl)   + get(k) -> value?   + del(k)   + cleanup() -> removed
```

### Follow-up questions

- LRU eviction when memory is full (combine with the LRU cache from pack I).
- Persistence: append-only log and snapshots.
- Thread safety and sharding by key hash.

### C++17 code (`lld2/kv_store_ttl.cpp`)

``` cpp
// In-memory key-value store with per-key TTL: lazy expiry on read plus a cleanup pass driven by a min-heap; overwriting a key
// must not let its old expiry delete the new value (a version number per key handles that). Clock injected for tests.
#include <cassert>
#include <functional>
#include <iostream>
#include <optional>
#include <queue>
#include <string>
#include <tuple>
#include <unordered_map>
#include <vector>
using namespace std;
class KV {
    struct Entry { string value; long long expires; long long version; };       // expires = -1 means never
    unordered_map<string, Entry> m; long long ver = 0; function<long long()> now;
    priority_queue<tuple<long long, long long, string>, vector<tuple<long long, long long, string>>, greater<>> heap;   // (expires, version, key)
    bool alive(const Entry& e) const { return e.expires < 0 || now() < e.expires; }
public:
    explicit KV(function<long long()> clock) : now(move(clock)) {}
    void set(const string& k, const string& v, long long ttl = -1) {
        long long exp = ttl < 0 ? -1 : now() + ttl; m[k] = {v, exp, ++ver};
        if (exp >= 0) heap.push({exp, ver, k});
    }
    optional<string> get(const string& k) {
        auto it = m.find(k); if (it == m.end()) return nullopt;
        if (!alive(it->second)) { m.erase(it); return nullopt; }        // lazy expiry
        return it->second.value;
    }
    bool del(const string& k) { return m.erase(k) > 0; }
    int cleanup() {                                              // remove everything already expired; O(k log n)
        int removed = 0;
        // std::get is needed here: the member function get() hides it inside the class
        while (!heap.empty() && std::get<0>(heap.top()) <= now()) {
            auto [exp, v, k] = heap.top(); heap.pop();
            auto it = m.find(k);
            if (it != m.end() && it->second.version == v) { m.erase(it); removed++; }   // skip stale heap entries
        }
        return removed;
    }
    size_t size() const { return m.size(); }
};
int main() {
    long long t = 0; KV kv([&] { return t; });
    kv.set("session:1", "asha", 10); kv.set("config", "v1"); kv.set("session:2", "ravi", 5);
    t = 4; assert(kv.get("session:2") == "ravi");
    t = 5; assert(!kv.get("session:2") && kv.get("session:1") == "asha");              // expiry is exclusive at the deadline
    kv.set("session:1", "asha-renewed", 100);                                          // overwrite with a longer TTL
    t = 20; assert(kv.cleanup() == 0 && kv.get("session:1") == "asha-renewed");        // old expiry (10) must not delete it
    kv.set("tmp", "x", 1); t = 21; assert(kv.cleanup() == 1 && kv.size() == 2);       // tmp removed by the cleanup pass
    assert(kv.get("config") == "v1" && kv.del("config") && !kv.get("config") && !kv.del("config"));
    cout << "kv store ok\n";
}
```

## 06. Snake and ladder

Machine-coding staple: rules as data, players in a queue, testable randomness.

### Requirements to confirm

- Board size and a set of snakes and ladders
- Players take turns; a six gives another roll
- Overshooting the last square means staying put
- First to land exactly on the last square wins
- Reject invalid boards

### Design decisions

- Snakes and ladders are one map of jumps; no separate classes are needed.
- Dice are injected, so tests script exact rolls (the 14 → 20 → snake → extra roll path is tested).
- The constructor validates the board (no jump from the last square, no jump onto another jump).

### Classes

``` text
Game
  - size, jumps: from -> to       (snakes go down, ladders go up)
  - players: queue<(name, pos)>
  - dice: function<int()>         (injected: random in play, scripted in tests)
  + turn() -> name   + won() -> winner   + position(name)
```

### Follow-up questions

- Multiple dice, or a crooked dice for testing.
- Saving and resuming a game.
- Rule variations behind a Rules interface (Strategy).

### C++17 code (`lld2/snake_ladder.cpp`)

``` cpp
// Snake and ladder: board validation, players in turn order, injectable dice (deterministic tests), exact landing on 100,
// and an extra roll on a six.
#include <cassert>
#include <deque>
#include <functional>
#include <iostream>
#include <map>
#include <stdexcept>
#include <string>
#include <vector>
using namespace std;
class Game {
    int size; map<int, int> jumps; deque<pair<string, int>> players; function<int()> dice; string winner;
public:
    Game(int n, map<int, int> j, vector<string> names, function<int()> d) : size(n), jumps(move(j)), dice(move(d)) {
        for (auto& [from, to] : jumps) {
            if (from <= 1 || from >= size || to < 1 || to > size || from == to) throw invalid_argument("bad snake or ladder");
            if (jumps.count(to)) throw invalid_argument("jump lands on another jump");
        }
        for (auto& p : names) players.push_back({p, 1});
    }
    string turn() {                                              // returns the player who moved; sets winner
        auto [name, pos] = players.front(); players.pop_front();
        while (true) {
            int r = dice(); if (r < 1 || r > 6) throw logic_error("bad dice");
            if (pos + r <= size) { pos += r; auto it = jumps.find(pos); if (it != jumps.end()) pos = it->second; }   // overshoot: stay
            if (pos == size) { winner = name; players.push_back({name, pos}); return name; }
            if (r != 6) break;                                   // a six gives another roll
        }
        players.push_back({name, pos}); return name;
    }
    const string& won() const { return winner; }
    int position(const string& n) const { for (auto& [p, pos] : players) if (p == n) return pos; return -1; }
};
static bool throwsOn(map<int, int> j) { try { Game g(30, j, {"x"}, [] { return 1; }); } catch (const invalid_argument&) { return true; } return false; }
int main() {
    vector<int> rolls{3, 2, 6, 1, 4, 5}; size_t k = 0;
    Game g(30, {{4, 14}, {9, 27}, {17, 7}, {20, 1}}, {"asha", "ravi"}, [&] { return rolls[k++]; });
    g.turn(); assert(g.position("asha") == 14);                  // 1 + 3 = 4, ladder up to 14
    g.turn(); assert(g.position("ravi") == 3);
    g.turn(); assert(g.position("asha") == 2);                   // 14 + 6 = 20, snake down to 1; the six gives a roll of 1
    g.turn(); assert(g.position("ravi") == 7);
    g.turn(); assert(g.position("asha") == 7 && g.won().empty());
    vector<int> r2{6, 2, 5, 2, 1}; size_t k2 = 0; Game o(10, {}, {"a"}, [&] { return r2[k2++]; });
    o.turn(); assert(o.position("a") == 9);                      // 6 then 2 (extra roll)
    o.turn(); assert(o.position("a") == 9);                      // 5 would overshoot 10: stay
    o.turn(); assert(o.position("a") == 9);                      // 2 also overshoots
    o.turn(); assert(o.won() == "a" && o.position("a") == 10);    // exact landing wins
    assert(throwsOn({{30, 1}}) && throwsOn({{5, 5}}) && throwsOn({{3, 12}, {12, 2}}) && !throwsOn({{3, 12}, {13, 2}}));
    cout << "snake and ladder ok\n";
}
```
