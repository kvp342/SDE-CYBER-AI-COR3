// Tic-tac-toe for an N x N board: move validation, turn order, and O(1) win detection with row/column/diagonal counters.
#include <cassert>
#include <iostream>
#include <stdexcept>
#include <vector>
using namespace std;
enum class Result { Ok, Win, Draw };
class Game {
    int n, moves = 0, turn = 0;                                   // turn 0 = X, 1 = O
    vector<vector<char>> board; vector<int> rows, cols; int diag = 0, anti = 0; bool over = false;
public:
    explicit Game(int size) : n(size), board(size, vector<char>(size, '.')), rows(size), cols(size) {}
    char current() const { return turn ? 'O' : 'X'; }
    Result play(char who, int r, int c) {                       // throws invalid_argument on an illegal move
        if (over) throw invalid_argument("game is over");
        if (who != current()) throw invalid_argument("not your turn");
        if (r < 0 || c < 0 || r >= n || c >= n) throw invalid_argument("outside the board");
        if (board[r][c] != '.') throw invalid_argument("cell taken");
        board[r][c] = who; int d = who == 'X' ? 1 : -1; moves++;
        rows[r] += d; cols[c] += d; if (r == c) diag += d; if (r + c == n - 1) anti += d;
        if (abs(rows[r]) == n || abs(cols[c]) == n || abs(diag) == n || abs(anti) == n) { over = true; return Result::Win; }
        if (moves == n * n) { over = true; return Result::Draw; }
        turn ^= 1; return Result::Ok;
    }
};
static bool throws(Game& g, char w, int r, int c) { try { g.play(w, r, c); } catch (const invalid_argument&) { return true; } return false; }
int main() {
    Game g(3);                                                    // X wins on the top row
    assert(g.play('X', 0, 0) == Result::Ok && g.play('O', 1, 0) == Result::Ok && g.play('X', 0, 1) == Result::Ok && g.play('O', 1, 1) == Result::Ok);
    assert(g.play('X', 0, 2) == Result::Win && throws(g, 'O', 2, 2));
    Game d(3);                                                    // anti-diagonal win for O
    d.play('X', 0, 0); d.play('O', 0, 2); d.play('X', 1, 0); d.play('O', 1, 1); d.play('X', 2, 2); assert(d.play('O', 2, 0) == Result::Win);
    Game e(3); int seq[9][2] = {{0,0},{0,1},{0,2},{1,1},{1,0},{1,2},{2,1},{2,0},{2,2}}; Result last = Result::Ok;   // a draw
    for (int i = 0; i < 9; i++) last = e.play(i % 2 ? 'O' : 'X', seq[i][0], seq[i][1]);
    assert(last == Result::Draw);
    Game f(4); assert(throws(f, 'O', 0, 0) && !throws(f, 'X', 0, 0) && throws(f, 'O', 0, 0) && throws(f, 'O', 4, 0));
    cout << "tic-tac-toe ok\n";
}
