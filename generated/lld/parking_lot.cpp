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
