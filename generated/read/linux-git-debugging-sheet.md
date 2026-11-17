TOOLS · DAILY COMMANDS

# Linux, Git and debugging

Commands you will use in labs, projects and contests. Each one marked "tested" was run in a throw-away folder and its output checked (40 of 40). Copy them, but read what a command does before running it, especially anything that deletes or rewrites history.

**Git rule.** Rewrite history (amend, reset) only on commits you have not pushed; for pushed commits use `git revert`. Never commit keys or `.env` files.

## Files and text

|                                                 |                                                        |        |
|-------------------------------------------------|--------------------------------------------------------|--------|
| `ls -la`                                        | List all files with permissions, including hidden ones | tested |
| `mkdir -p a/b/c && tree a || find a`            | Create nested folders; show them                       | tested |
| `cp -r a backup && mv backup a_old`             | Copy a folder recursively; rename it                   | tested |
| `grep -rn "TODO" .`                             | Search recursively, with line numbers                  | tested |
| `find . -name "*.cpp" -mtime -1`                | Files by name changed in the last day                  | tested |
| `wc -l src/m.cpp`                               | Count lines                                            | tested |
| `sort data.txt | uniq -c | sort -rn | head -3`  | Most frequent lines                                    | tested |
| `awk -F, '{s += $2} END {print s}' marks.csv`   | Sum a CSV column                                       | tested |
| `sed -i 's/old/new/g' notes.txt`                | Replace text in a file                                 | tested |
| `jq '.name' package.json`                       | Read a JSON field                                      | tested |
| `tar -czf src.tgz src && tar -tzf src.tgz`      | Make and list a compressed archive                     | tested |
| `chmod +x run.sh && ./run.sh`                   | Make a script executable and run it                    | tested |
| `find . -name '*.log' -print0 | xargs -0 rm -f` | Delete matching files safely (handles spaces)          | tested |

## Processes and system

|                                             |                                            |        |
|---------------------------------------------|--------------------------------------------|--------|
| `ps aux | head -5`                          | Running processes                          | tested |
| `sleep 30 & echo $! > pid; kill $(cat pid)` | Start a background job; stop it by PID     | tested |
| `df -h . && du -sh src`                     | Disk free; size of a folder                | tested |
| `lsof -p $$ | head -3`                      | Files open by a process (here: this shell) | tested |
| `env | grep ^HOME=`                         | Environment variables                      | tested |
| `command -v g++`                            | Where a program is installed               | tested |
| `ulimit -n`                                 | Open-file limit for this shell             | tested |

## Git: everyday

|                                                                                                                                         |                                  |        |
|-----------------------------------------------------------------------------------------------------------------------------------------|----------------------------------|--------|
| `git init -q demo && cd demo && git status -s`                                                                                          | Start a repository               | tested |
| `git add file.txt && git commit -qm "Add file" && git log --oneline`                                                                    | Stage and commit; short history  | tested |
| `git switch -c feature && git branch`                                                                                                   | Create and switch to a branch    | tested |
| `git diff`                                                                                                                              | Unstaged changes                 | tested |
| `git stash && git stash list && git stash pop`                                                                                          | Put work aside and bring it back | tested |
| `git commit -qam "Edit" && git switch -q main 2>/dev/null || git switch -q master; git merge -q feature && git log --oneline | head -2` | Merge a branch into main         | tested |
| `git log --oneline --graph --all | head -5`                                                                                             | History as a graph               | tested |

## Git: undo safely

|                                                                                               |                                               |        |
|-----------------------------------------------------------------------------------------------|-----------------------------------------------|--------|
| `git restore file.txt`                                                                        | Throw away unstaged edits to a file           | tested |
| `git restore --staged file.txt`                                                               | Unstage a file (keep the edit)                | tested |
| `git commit -q --amend -m "Better message" && git log -1 --format=%s`                         | Fix the last commit message (before pushing)  | tested |
| `git reset --soft HEAD~1 && git status -s`                                                    | Undo the last commit, keep its changes staged | tested |
| `git commit -qm again && git revert --no-edit HEAD >/dev/null && git log --oneline | head -2` | Undo a pushed commit with a new commit        | tested |
| `git reflog | head -3`                                                                        | Find 'lost' commits after a bad reset         | tested |

## Debugging C++

|                                                                                  |                                                               |        |
|----------------------------------------------------------------------------------|---------------------------------------------------------------|--------|
| `g++ -std=c++17 -g -O0 -Wall -Wextra -Wshadow bug.cpp -o bug`                    | Build with debug info and warnings                            | tested |
| `g++ -std=c++17 -g -fsanitize=address,undefined bug.cpp -o bug_san && ./bug_san` | Find out-of-bounds reads at the exact line (AddressSanitizer) | tested |
| `gdb -batch -ex run -ex bt ./crash`                                              | Run in gdb and print the stack after a crash                  | tested |
| `gdb -batch -ex 'break main' -ex run -ex next -ex 'info locals' ./bug`           | Breakpoint, step, show local variables                        | tested |
| `valgrind --leak-check=full -q ./leak`                                           | Find memory leaks                                             | tested |
| `strace -c -f ./hello 2>&1 | tail -4`                                            | Count the system calls a program makes                        | tested |
| `time ./hello`                                                                   | Measure wall-clock and CPU time                               | tested |

## Debugging routine

1.  Reproduce with the smallest input.
2.  Compile with `-g -Wall -Wextra -fsanitize=address,undefined`; most contest bugs show up here.
3.  For crashes, run in gdb and read `bt`; for wrong answers, print state at the first suspicious line.
4.  Fix one thing, rerun the same input, then the edge cases.
