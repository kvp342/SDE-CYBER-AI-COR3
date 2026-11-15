// Library: books and copies, members, loans with due dates and fines, reservations with notification (Observer).
#include <cassert>
#include <deque>
#include <functional>
#include <iostream>
#include <map>
#include <string>
#include <vector>
using namespace std;

struct Book { string isbn, title; };
enum class CopyStatus { Available, Loaned, OnHold };
struct Copy { int id; string isbn; CopyStatus status = CopyStatus::Available; };
struct Member { int id; string name; int maxLoans = 3; };
struct Loan { int copyId, memberId, day, due; };

class Library {
    map<string, Book> books;
    map<int, Copy> copies;
    map<int, Member> members;
    map<int, Loan> loans;                                        // copy id -> loan
    map<string, deque<int>> holds;                               // isbn -> waiting member ids (FIFO)
    map<int, int> holdFor;                                       // copy id -> member it is held for
    vector<function<void(int, const string&)>> listeners;        // Observer: notify(memberId, message)
    int nextCopy = 1;
    static constexpr int LOAN_DAYS = 14, FINE_PER_DAY = 2;
    void notify(int m, const string& msg) { for (auto& f : listeners) f(m, msg); }
    int loansOf(int m) const { int n = 0; for (auto& [c, l] : loans) n += l.memberId == m; return n; }
public:
    void onNotify(function<void(int, const string&)> f) { listeners.push_back(move(f)); }
    void addBook(const Book& b, int count) { books[b.isbn] = b; for (int i = 0; i < count; i++) { copies[nextCopy] = {nextCopy, b.isbn}; nextCopy++; } }
    void addMember(const Member& m) { members[m.id] = m; }

    int checkout(int memberId, const string& isbn, int day) {     // returns copy id, or -1
        if (loansOf(memberId) >= members.at(memberId).maxLoans) return -1;
        for (auto& [id, c] : copies) {
            bool heldForMe = c.status == CopyStatus::OnHold && holdFor[id] == memberId;
            if (c.isbn == isbn && (c.status == CopyStatus::Available || heldForMe)) {
                if (heldForMe) { holdFor.erase(id); holds[isbn].pop_front(); }
                c.status = CopyStatus::Loaned;
                loans[id] = {id, memberId, day, day + LOAN_DAYS};
                return id;
            }
        }
        return -1;
    }
    void reserve(int memberId, const string& isbn) { holds[isbn].push_back(memberId); }

    int giveBack(int copyId, int day) {                          // returns the fine
        Loan l = loans.at(copyId); loans.erase(copyId);
        int fine = max(0, day - l.due) * FINE_PER_DAY;
        Copy& c = copies[copyId];
        auto& q = holds[c.isbn];
        if (!q.empty()) { c.status = CopyStatus::OnHold; holdFor[copyId] = q.front(); notify(q.front(), books[c.isbn].title + " is ready for you"); }
        else c.status = CopyStatus::Available;
        return fine;
    }
};

int main() {
    Library lib; vector<pair<int, string>> inbox;
    lib.onNotify([&](int m, const string& msg) { inbox.push_back({m, msg}); });
    lib.addBook({"978-0262046305", "Introduction to Algorithms"}, 1);
    lib.addMember({1, "Asha"}); lib.addMember({2, "Ravi"}); lib.addMember({3, "Meera", 1});
    int c = lib.checkout(1, "978-0262046305", 0);
    assert(c == 1 && lib.checkout(2, "978-0262046305", 0) == -1);    // no copy free
    lib.reserve(2, "978-0262046305");
    assert(lib.giveBack(c, 20) == 12);                                // 6 days late x 2
    assert(inbox.size() == 1 && inbox[0].first == 2);                 // Ravi notified
    assert(lib.checkout(3, "978-0262046305", 21) == -1);              // held for Ravi, not Meera
    assert(lib.checkout(2, "978-0262046305", 21) == 1);
    assert(lib.giveBack(1, 30) == 0);
    lib.addBook({"111", "Clean Code"}, 2);
    assert(lib.checkout(3, "111", 0) != -1 && lib.checkout(3, "111", 0) == -1);  // Meera's limit is 1
    cout << "library ok\n";
}
