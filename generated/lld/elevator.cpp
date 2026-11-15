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
