**Target:** suite/user-guide.md §6 — after the `embarch-api serial-log` example block (the file is in reserve, 935 B left; one short paragraph)
**Was:** §6 lists build/flash/reset/serial-log and says nothing about `stack`
**Now:** `embarch-api stack plan|fold|restack` (git-only, no config) folds review fixes into their commits and restacks a PR stack; to allow it in auto mode use the single rule `Bash(embarch-api stack:*)` instead of `git rebase *` / `git push --force-with-lease *`. Full text: [embarch-api/interfaces/stack.md](../embarch-api/interfaces/stack.md), decision 96.
