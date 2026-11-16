// 4. Object pool: preallocate objects and recycle them through a free list instead of calling new/delete on the hot path.
#include <cassert>
#include <cstddef>
#include <new>
#include <vector>
#include "bench.h"
struct Msg { long id; double px; int qty; };
template <class T> class Pool {
    union Slot { Slot* next; alignas(T) unsigned char obj[sizeof(T)]; };
    std::vector<Slot> slots; Slot* free_ = nullptr;
public:
    explicit Pool(size_t n) : slots(n) { for (auto& s : slots) { s.next = free_; free_ = &s; } }
    template <class... A> T* make(A&&... a) { if (!free_) return nullptr; Slot* s = free_; free_ = s->next; return new (s->obj) T{a...}; }
    void destroy(T* p) { p->~T(); Slot* s = reinterpret_cast<Slot*>(p); s->next = free_; free_ = s; }
};
int main() {
    Pool<Msg> pool(2); Msg* a = pool.make(1L, 1.0, 1); Msg* b = pool.make(2L, 2.0, 2);
    assert(a && b && a != b && !pool.make(3L, 3.0, 3)); pool.destroy(a); Msg* c = pool.make(4L, 4.0, 4); assert(c == a && c->id == 4); pool.destroy(b); pool.destroy(c);
    const long N = 1'000'000; Pool<Msg> big(64); long sum = 0;
    best_ns_per_op("new/delete", N, [&] { for (long i = 0; i < N; i++) { Msg* m = new Msg{i, 1.0, 1}; sum += m->qty; keep(m); delete m; } });
    best_ns_per_op("pool make/destroy", N, [&] { for (long i = 0; i < N; i++) { Msg* m = big.make(i, 1.0, 1); sum += m->qty; keep(m); big.destroy(m); } });
    assert(sum == 10 * N); std::puts("e4 ok");
}
