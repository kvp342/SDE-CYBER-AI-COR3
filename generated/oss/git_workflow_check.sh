#!/usr/bin/env bash
# Runs the open-source guide's git workflow end to end against local bare repositories standing in for GitHub
# (upstream = the project, origin = your fork). Every command here is the one printed in the guide.
set -euo pipefail
T=$(mktemp -d); cd "$T"; export GIT_AUTHOR_NAME=you GIT_AUTHOR_EMAIL=you@example.com GIT_COMMITTER_NAME=you GIT_COMMITTER_EMAIL=you@example.com
git init -q --bare -b main upstream.git && git init -q --bare -b main fork.git
git clone -q upstream.git seed && (cd seed && echo "v1" > app.txt && git add . && git commit -qm "initial" && git push -q origin main)
git clone -q upstream.git maint && git -C maint config user.email m@example.com
git --git-dir=fork.git fetch -q upstream.git main:main                     # "Fork" on GitHub = a server-side copy
# ---- the guide's commands
git clone -q fork.git project && cd project
git remote add upstream ../upstream.git
git remote -v | grep -q upstream
git switch -q -c fix-typo-in-readme
echo "v1 fixed" > app.txt && git add app.txt && git commit -qm "Fix typo in app.txt"
git push -q -u origin fix-typo-in-readme
# meanwhile the project moves on
(cd ../maint && git pull -q && echo "other" > other.txt && git add . && git commit -qm "maintainer change" && git push -q)
git fetch -q upstream
git rebase -q upstream/main
git push -q --force-with-lease origin fix-typo-in-readme
test "$(git log --oneline upstream/main..HEAD | wc -l)" -eq 1                 # exactly your one commit on top
test -f other.txt                                                             # the maintainer's change is underneath
git switch -q main && git merge -q --ff-only upstream/main && git push -q origin main   # keep your fork's main in sync
test "$(git rev-parse main)" = "$(git rev-parse upstream/main)"
echo "git workflow OK: fork, branch, commit, push, sync with upstream, rebase, force-with-lease, fast-forward main"
