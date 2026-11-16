// 2. Traversal order: walk a row-major 2-D array row by row (sequential) versus column by column (strided, cache-hostile).
#include <cassert>
#include <vector>
#include "bench.h"
int main() {
    const int R = 2048, C = 2048; std::vector<int> a(R * C); for (int i = 0; i < R * C; i++) a[i] = i & 7;
    long long s1 = 0, s2 = 0;
    best_ns_per_op("row-major traversal", (long)R * C, [&] { s1 = 0; for (int r = 0; r < R; r++) for (int c = 0; c < C; c++) s1 += a[r * C + c]; keep(s1); });
    best_ns_per_op("column-major traversal", (long)R * C, [&] { s2 = 0; for (int c = 0; c < C; c++) for (int r = 0; r < R; r++) s2 += a[r * C + c]; keep(s2); });
    assert(s1 == s2); std::puts("e2 ok");
}
