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
