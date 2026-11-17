// Machine coding: a cache with a pluggable eviction policy (Strategy pattern): LRU and LFU behind one interface, O(1) per operation.
#include <cassert>
#include <iostream>
#include <list>
#include <memory>
#include <optional>
#include <string>
#include <unordered_map>
using namespace std;
template <class K> struct EvictionPolicy { virtual ~EvictionPolicy() = default; virtual void touched(const K&) = 0; virtual void added(const K&) = 0; virtual void removed(const K&) = 0; virtual K victim() = 0; };
template <class K> class LRU : public EvictionPolicy<K> {
    list<K> order; unordered_map<K, typename list<K>::iterator> pos;          // front = most recent
public:
    void touched(const K& k) override { order.splice(order.begin(), order, pos.at(k)); }
    void added(const K& k) override { order.push_front(k); pos[k] = order.begin(); }
    void removed(const K& k) override { order.erase(pos.at(k)); pos.erase(k); }
    K victim() override { return order.back(); }
};
template <class K> class LFU : public EvictionPolicy<K> {   // frequency buckets; ties broken by least recent within the lowest frequency
    unordered_map<K, int> freq; unordered_map<int, list<K>> buckets; unordered_map<K, typename list<K>::iterator> pos; int minF = 0;
    void place(const K& k, int f) { buckets[f].push_front(k); pos[k] = buckets[f].begin(); freq[k] = f; }
public:
    void touched(const K& k) override { int f = freq.at(k); buckets[f].erase(pos[k]); if (buckets[f].empty() && minF == f) minF++; place(k, f + 1); }
    void added(const K& k) override { place(k, 1); minF = 1; }
    void removed(const K& k) override { int f = freq.at(k); buckets[f].erase(pos[k]); pos.erase(k); freq.erase(k); }
    K victim() override { while (buckets[minF].empty()) minF++; return buckets[minF].back(); }
};
template <class K, class V> class Cache {
    size_t cap; unordered_map<K, V> data; unique_ptr<EvictionPolicy<K>> policy;
public:
    Cache(size_t c, unique_ptr<EvictionPolicy<K>> p) : cap(c), policy(move(p)) {}
    optional<V> get(const K& k) { auto it = data.find(k); if (it == data.end()) return nullopt; policy->touched(k); return it->second; }
    void put(const K& k, V v) {
        if (cap == 0) return;
        if (data.count(k)) { data[k] = move(v); policy->touched(k); return; }
        if (data.size() == cap) { K old = policy->victim(); policy->removed(old); data.erase(old); }
        data[k] = move(v); policy->added(k);
    }
    size_t size() const { return data.size(); }
};
int main() {
    Cache<int, string> lru(2, make_unique<LRU<int>>());
    lru.put(1, "a"); lru.put(2, "b"); assert(lru.get(1) == "a"); lru.put(3, "c");          // 2 is least recent
    assert(!lru.get(2) && lru.get(1) == "a" && lru.get(3) == "c");
    Cache<int, int> lfu(2, make_unique<LFU<int>>());
    lfu.put(1, 1); lfu.put(2, 2); lfu.get(1); lfu.put(3, 3);                               // 2 has the lowest frequency
    assert(!lfu.get(2) && lfu.get(3) == 3); lfu.put(4, 4);                                  // 1 and 3 both have freq 2; 1 is less recent
    assert(!lfu.get(1) && lfu.get(3) == 3 && lfu.get(4) == 4 && lfu.size() == 2);
    Cache<int, int> zero(0, make_unique<LRU<int>>()); zero.put(1, 1); assert(!zero.get(1));
    cout << "eviction cache ok\n";
}
