// Invert Binary Tree (LeetCode 226): swap the children of every node, recursively and iteratively (BFS).
#include <cassert>
#include <iostream>
#include <queue>
#include <utility>
#include <vector>
using namespace std;
struct TreeNode { int val; TreeNode *left = nullptr, *right = nullptr; explicit TreeNode(int v) : val(v) {} };
TreeNode* invertRec(TreeNode* r) { if (!r) return r; swap(r->left, r->right); invertRec(r->left); invertRec(r->right); return r; }
TreeNode* invertBfs(TreeNode* r) {
    queue<TreeNode*> q; if (r) q.push(r);
    while (!q.empty()) { auto n = q.front(); q.pop(); swap(n->left, n->right); if (n->left) q.push(n->left); if (n->right) q.push(n->right); }
    return r;
}
static TreeNode* build(const vector<int>& v, size_t i = 0) { if (i >= v.size() || v[i] < 0) return nullptr; auto n = new TreeNode(v[i]); n->left = build(v, 2 * i + 1); n->right = build(v, 2 * i + 2); return n; }
static void level(TreeNode* r, vector<int>& out) { queue<TreeNode*> q; q.push(r); while (!q.empty()) { auto n = q.front(); q.pop(); if (!n) continue; out.push_back(n->val); q.push(n->left); q.push(n->right); } }
static void free_tree(TreeNode* r) { if (!r) return; free_tree(r->left); free_tree(r->right); delete r; }
int main() {
    for (auto f : {invertRec, invertBfs}) {
        TreeNode* t = build({4, 2, 7, 1, 3, 6, 9}); f(t); vector<int> got; level(t, got);
        assert((got == vector<int>{4, 7, 2, 9, 6, 3, 1})); free_tree(t);
        assert(f(nullptr) == nullptr);
    }
    cout << "invert tree ok\n";
}
