// 3. Lock-free single-producer single-consumer ring buffer. One writer owns `tail`, one reader owns `head`;
// acquire/release ordering publishes each slot. Capacity is a power of two so wrap-around is a mask.
#include <array>
#include <atomic>
#include <cassert>
#include <cstddef>
#include <optional>
#include <thread>
#include "bench.h"
template <class T, size_t N> class Spsc {
    static_assert((N & (N - 1)) == 0, "capacity must be a power of two");
    std::array<T, N> buf;
    alignas(64) std::atomic<size_t> head{0};   // read position, written by the consumer only
    alignas(64) std::atomic<size_t> tail{0};   // write position, written by the producer only (separate cache line: no false sharing)
public:
    bool push(const T& v) {
        size_t t = tail.load(std::memory_order_relaxed);
        if (t - head.load(std::memory_order_acquire) == N) return false;     // full
        buf[t & (N - 1)] = v; tail.store(t + 1, std::memory_order_release); return true;
    }
    std::optional<T> pop() {
        size_t h = head.load(std::memory_order_relaxed);
        if (h == tail.load(std::memory_order_acquire)) return std::nullopt;   // empty
        T v = buf[h & (N - 1)]; head.store(h + 1, std::memory_order_release); return v;
    }
};
int main() {
    Spsc<int, 4> small; assert(small.push(1) && small.push(2) && small.push(3) && small.push(4) && !small.push(5));
    assert(*small.pop() == 1); assert(small.push(5)); for (int e : {2, 3, 4, 5}) assert(*small.pop() == e); assert(!small.pop());
    static Spsc<long, 1024> q; const long M = 2'000'000; bool ordered = true;
    best_ns_per_op("SPSC transfer (2 threads)", M, [&] {
        std::thread prod([&] { for (long i = 0; i < M; i++) while (!q.push(i)) {} });
        long expect = 0; while (expect < M) if (auto v = q.pop()) { ordered &= (*v == expect); expect++; }
        prod.join();
    }, 3);
    assert(ordered); std::puts("e3 ok");
}
