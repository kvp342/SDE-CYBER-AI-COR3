// LRU cache: O(1) get and put with a doubly linked list (recency order) and a hash map (key -> list node).
#include <cassert>
#include <iostream>
#include <list>
#include <optional>
#include <string>
#include <unordered_map>
using namespace std;

template <class K, class V>
class LRUCache {
    size_t cap;
    list<pair<K, V>> items;                                       // front = most recently used
    unordered_map<K, typename list<pair<K, V>>::iterator> pos;
public:
    explicit LRUCache(size_t capacity) : cap(capacity) { if (!cap) throw invalid_argument("capacity must be positive"); }
    optional<V> get(const K& k) {
        auto it = pos.find(k);
        if (it == pos.end()) return nullopt;
        items.splice(items.begin(), items, it->second);          // move to front, iterators stay valid
        return it->second->second;
    }
    void put(const K& k, V v) {
        if (auto it = pos.find(k); it != pos.end()) {
            it->second->second = move(v);
            items.splice(items.begin(), items, it->second);
            return;
        }
        if (items.size() == cap) { pos.erase(items.back().first); items.pop_back(); }   // evict least recently used
        items.emplace_front(k, move(v));
        pos[k] = items.begin();
    }
    size_t size() const { return items.size(); }
};

int main() {
    LRUCache<int, string> c(2);
    c.put(1, "one"); c.put(2, "two");
    assert(c.get(1) == "one");                                    // 1 is now most recent
    c.put(3, "three");                                            // evicts 2
    assert(!c.get(2) && c.get(3) == "three");
    c.put(1, "uno");                                              // update keeps size
    assert(c.size() == 2 && c.get(1) == "uno");
    c.put(4, "four");                                             // evicts 3 (1 was used more recently)
    assert(!c.get(3) && c.get(4) == "four" && c.get(1) == "uno");
    try { LRUCache<int, int> bad(0); assert(false); } catch (const invalid_argument&) {}
    LRUCache<string, int> big(1000);
    for (int i = 0; i < 100000; i++) big.put(to_string(i % 1500), i);
    assert(big.size() == 1000);
    cout << "lru cache ok\n";
}
