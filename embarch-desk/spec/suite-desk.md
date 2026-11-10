# embarch-desk: suite desks and worktrees, continued

**Status:** active, 2026-11-10. Split out of [../spec.md](../spec.md) §1 on 2026-11-10, verbatim, when that file reached its reserve line. The close-out invariant (decisions 83, 84) stays in spec.md §2.

**A suite desk** (decision 70) works on repos that sit side by side: Start work makes a folder per issue holding worktrees for the issue's repo and the docs, and symlinks for the rest, so sibling paths build as they do in the main clones.

**A worktree of a west project builds its own module** (decision 80): Start work writes `ZEPHYR_MODULES` — the workspace's Zephyr modules with the main clone swapped for the worktree — into the worktree's `.claude/settings.local.json` `env`; outside a west workspace nothing is written, and a missing `west` or a module with no `name:` is a warning in its answer.

**A folder whose login lacks `embarch-api` is flagged** (decision 82): `GET /desks` marks it and a session starting there is told the user-scope `claude mcp add` command; the desk only reads `.claude.json`.
