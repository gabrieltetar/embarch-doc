# 089 — `gate.md` has no bullet for a Python repo, and sixteen `atlas` tasks now sit in the queue

**State:** open
**Source:** the 2026-10-25 leg, filing the 2026-10-20 inbox batch: sixteen drops were scoped `atlas`, the first `atlas` tasks the queue has held (`tasks/atlas/001`–`016`).
**Scope:** doc
**Hardware:** none
**Owner:** required — the fix is a line in `embarch-fleet/gate.md` (and possibly `.claude/leg.md`'s worktree table), both owner-reserved.

## What

`embarch-fleet/gate.md` says what a unit passes before it merges: `cargo build`/`test`/`clippy` for a Rust repo, and since 2026-10-25 an npm bullet for `embarch-chat`. `embarch-atlas` is neither. Its own `CLAUDE.md` says commit once `.venv/bin/pytest -q` is green, and run `check-client-names.py --repo .` before every commit. The `.venv` lives in the main checkout, so a worker's worktree under `embarch/.worktrees/embarch-atlas/<slug>/` has none, and nothing tells the worker or the supervisor which interpreter the gate runs, or whether the worktree needs its own venv.

When this is done, `gate.md` names the atlas gate the way it names the npm one, and `.claude/leg.md` says what an atlas worktree needs before its first test run (a venv of its own, or the main checkout's `.venv/bin/pytest` run against the worktree's `src`).

## Why now

`queue-status.py` counts the `atlas` tasks as dispatchable, so the next leg can send a worker at one. That worker would have to invent its own gate, and the supervisor re-running it would be checking against a list nobody wrote. The 2026-10-25 leg did not dispatch an `atlas` task for this reason. A second reason applies only to `atlas/016`: the owner has uncommitted work on the `standard` document kind in `embarch-atlas-wt` (branch `fix/field-findings`), and that task builds on it.

## Done when

- [ ] `gate.md` has an atlas (Python) bullet naming the test command and the client-name check.
- [ ] `.claude/leg.md` says what an `embarch-atlas` worktree needs for that command to run.
