// 8. Price-level order book: prices are integer ticks in a known band, so each side is an array indexed by tick.
// Add and cancel are O(1); the best price moves with a short scan only when its level empties.
#include <cassert>
#include <cstdint>
#include <map>
#include <random>
#include <vector>
#include "bench.h"
class Book {
    int lo; std::vector<int64_t> bids, asks; int bestBid = -1, bestAsk = -1;   // indices into the arrays; -1 = empty
public:
    Book(int loTick, int hiTick) : lo(loTick), bids(hiTick - loTick + 1), asks(hiTick - loTick + 1) {}
    void add(bool buy, int tick, int64_t qty) {
        int i = tick - lo; auto& side = buy ? bids : asks; side[i] += qty;
        if (buy && (bestBid < 0 || i > bestBid)) bestBid = i;
        if (!buy && (bestAsk < 0 || i < bestAsk)) bestAsk = i;
    }
    void cancel(bool buy, int tick, int64_t qty) {
        int i = tick - lo; auto& side = buy ? bids : asks; side[i] -= qty; assert(side[i] >= 0);
        if (buy && i == bestBid) while (bestBid >= 0 && bids[bestBid] == 0) bestBid--;
        if (!buy && i == bestAsk) { while (bestAsk >= 0 && bestAsk < (int)asks.size() && asks[bestAsk] == 0) bestAsk++; if (bestAsk == (int)asks.size()) bestAsk = -1; }
    }
    int bestBidTick() const { return bestBid < 0 ? -1 : bestBid + lo; }
    int bestAskTick() const { return bestAsk < 0 ? -1 : bestAsk + lo; }
};
int main() {
    Book b(1000, 2000); b.add(true, 1500, 10); b.add(true, 1490, 5); b.add(false, 1510, 7); b.add(false, 1505, 3);
    assert(b.bestBidTick() == 1500 && b.bestAskTick() == 1505); b.cancel(true, 1500, 10); assert(b.bestBidTick() == 1490);
    b.cancel(false, 1505, 3); assert(b.bestAskTick() == 1510); b.cancel(false, 1510, 7); assert(b.bestAskTick() == -1);
    // Randomised check against a std::map reference
    std::mt19937 g(1); Book bk(0, 999); std::map<int, int64_t> rb, ra;
    for (int s = 0; s < 200000; s++) {
        bool buy = g() & 1; int t = buy ? 300 + g() % 200 : 500 + g() % 200; auto& ref = buy ? rb : ra;
        if (ref.count(t) && (g() & 1)) { int64_t q = ref[t]; bk.cancel(buy, t, q); ref.erase(t); } else { bk.add(buy, t, 1); ref[t] += 1; }
        assert(bk.bestBidTick() == (rb.empty() ? -1 : rb.rbegin()->first)); assert(bk.bestAskTick() == (ra.empty() ? -1 : ra.begin()->first));
    }
    const long N = 2'000'000; Book hot(0, 9999); std::map<int, int64_t> m; std::vector<int> ticks(N); for (auto& t : ticks) t = 4000 + g() % 2000;
    best_ns_per_op("std::map add + best", N, [&] { for (int t : ticks) { m[t] += 1; keep(m.rbegin()->first); } }, 3);
    best_ns_per_op("array book add + best", N, [&] { for (int t : ticks) { hot.add(true, t, 1); keep(hot.bestBidTick()); } }, 3);
    std::puts("e8 ok");
}
