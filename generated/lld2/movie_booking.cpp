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
