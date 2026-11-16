// 1. Data layout: sum one field over many records. Array of structs drags unused fields through the cache; struct of arrays does not.
#include <cassert>
#include <vector>
#include <cstdint>
#include "bench.h"
struct Order { int64_t id; double price; int32_t qty; char side; char pad[43]; };   // 72 bytes, like a fat record
int main() {
    const int N = 1 << 20; std::vector<Order> aos(N); std::vector<int32_t> qty(N);
    for (int i = 0; i < N; i++) { aos[i].qty = qty[i] = i % 100; aos[i].price = i; }
    long long a = 0, b = 0;
    best_ns_per_op("AoS: sum qty", N, [&] { a = 0; for (auto& o : aos) a += o.qty; keep(a); });
    best_ns_per_op("SoA: sum qty", N, [&] { b = 0; for (int q : qty) b += q; keep(b); });
    long long expect = 0; for (int i = 0; i < N; i++) expect += i % 100;
    assert(a == b && a == expect); std::puts("e1 ok");
}
