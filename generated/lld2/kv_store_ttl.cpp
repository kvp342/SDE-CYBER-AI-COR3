// In-memory key-value store with per-key TTL: lazy expiry on read plus a cleanup pass driven by a min-heap; overwriting a key
// must not let its old expiry delete the new value (a version number per key handles that). Clock injected for tests.
#include <cassert>
#include <functional>
#include <iostream>
#include <optional>
#include <queue>
#include <string>
#include <tuple>
#include <unordered_map>
#include <vector>
using namespace std;
class KV {
    struct Entry { string value; long long expires; long long version; };       // expires = -1 means never
    unordered_map<string, Entry> m; long long ver = 0; function<long long()> now;
    priority_queue<tuple<long long, long long, string>, vector<tuple<long long, long long, string>>, greater<>> heap;   // (expires, version, key)
    bool alive(const Entry& e) const { return e.expires < 0 || now() < e.expires; }
public:
    explicit KV(function<long long()> clock) : now(move(clock)) {}
    void set(const string& k, const string& v, long long ttl = -1) {
        long long exp = ttl < 0 ? -1 : now() + ttl; m[k] = {v, exp, ++ver};
        if (exp >= 0) heap.push({exp, ver, k});
    }
    optional<string> get(const string& k) {
        auto it = m.find(k); if (it == m.end()) return nullopt;
        if (!alive(it->second)) { m.erase(it); return nullopt; }        // lazy expiry
        return it->second.value;
    }
    bool del(const string& k) { return m.erase(k) > 0; }
    int cleanup() {                                              // remove everything already expired; O(k log n)
        int removed = 0;
        // std::get is needed here: the member function get() hides it inside the class
        while (!heap.empty() && std::get<0>(heap.top()) <= now()) {
            auto [exp, v, k] = heap.top(); heap.pop();
            auto it = m.find(k);
            if (it != m.end() && it->second.version == v) { m.erase(it); removed++; }   // skip stale heap entries
        }
        return removed;
    }
    size_t size() const { return m.size(); }
};
int main() {
    long long t = 0; KV kv([&] { return t; });
    kv.set("session:1", "asha", 10); kv.set("config", "v1"); kv.set("session:2", "ravi", 5);
    t = 4; assert(kv.get("session:2") == "ravi");
    t = 5; assert(!kv.get("session:2") && kv.get("session:1") == "asha");              // expiry is exclusive at the deadline
    kv.set("session:1", "asha-renewed", 100);                                          // overwrite with a longer TTL
    t = 20; assert(kv.cleanup() == 0 && kv.get("session:1") == "asha-renewed");        // old expiry (10) must not delete it
    kv.set("tmp", "x", 1); t = 21; assert(kv.cleanup() == 1 && kv.size() == 2);       // tmp removed by the cleanup pass
    assert(kv.get("config") == "v1" && kv.del("config") && !kv.get("config") && !kv.del("config"));
    cout << "kv store ok\n";
}
