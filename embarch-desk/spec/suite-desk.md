# embarch-desk: suite desks and worktrees, continued

**Status:** active, 2026-11-10. Split out of [../spec.md](../spec.md) §1 on 2026-11-10, verbatim, when that file reached its reserve line. The close-out invariant (decisions 83, 84) stays in spec.md §2.

**A suite desk** (decision 70) works on repos that sit side by side: Start work makes a folder per issue holding worktrees for the issue's repo and the docs, and symlinks for the rest, so sibling paths build as they do in the main clones. **The window is the folder's `<key>.code-workspace`** (decision 91), the code repo's worktree first: Start work, *Open in VS Code* and a session's folder link all open it, and a folder made by hand links as itself.

**A worktree of a west project builds its own module** (decision 80): Start work writes `ZEPHYR_MODULES` — the workspace's Zephyr modules with the main clone swapped for the worktree — into the worktree's `.claude/settings.local.json` `env`; outside a west workspace nothing is written, and a missing `west` or a module with no `name:` is a warning in its answer.

**A folder whose login lacks `embarch-api` is flagged** (decision 82): `GET /desks` marks it and a session starting there is told every missing piece in order (the user-scope `claude mcp add` command, `embarch init` when the repo has no config of its own) and not to flash by hand; the desk only reads `.claude.json`.
