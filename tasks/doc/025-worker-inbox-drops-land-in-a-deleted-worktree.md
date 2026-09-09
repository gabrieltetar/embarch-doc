# 025 — A worker's `inbox/` drop lands in its own worktree and is deleted with it

**State:** open
**Source:** `inbox/worker-inbox-drops-land-in-a-worktree-that-is-deleted.md`,
filed by leg 055 on 2026-09-08 while landing `outpost/013`. Observed directly,
not inferred. Drained into the queue by leg 056.
**Scope:** doc
**Hardware:** none
**Owner:** required — every path that closes it is reserved: the worker template
lives in `embarch-fleet/scripts/install.py`, and `inbox/README.md` is a protocol
README. No agent may write either.

## What

`inbox/` is gitignored, so a drop exists only in the working tree that wrote it.
A **worker** works in `/home/gabriel/Github/embarch/.worktrees/embarch-doc/<slug>/`,
so `inbox/<something>.md` written by a worker lands at
`.worktrees/embarch-doc/<slug>/inbox/`, **not** in
`/home/gabriel/Github/embarch/embarch-doc/inbox/` where the next leg's drain
looks. The supervisor deletes that worktree as soon as the unit lands, and the
drop goes with it, silently.

This happened on 2026-09-08. `outpost/013`'s worker found a broken relative link
in `tasks/api/051-...md`, correctly declined to fix a file outside its scope, and
filed `inbox/api-051-broken-burndown-link.md` into
`.worktrees/embarch-doc/013-readme-overhead-status/inbox/`. The supervisor found
it only because it went looking after reading the worker's report. Nothing
mechanical would have.

`.claude/leg.md` already carries the supervisor-side half of this rule — "read
them at `/home/gabriel/Github/embarch/embarch-doc/inbox/`, by absolute path, and
delete them there" — and the reason it gives (the crossing is safe because the
source is untracked) applies to a worker identically. The worker's own
instructions do not say it.

## Why now

The failure is silent and the loss is total: a finding a worker judged worth
recording, deleted by the supervisor's own cleanup, with no trace in the log, the
gate or git. It costs one sentence in the worker template to close, and every leg
that runs before it is closed can lose a drop the same way. That leg's drop
survived only by luck.

## Done when

- [ ] The worker template (`embarch-fleet/scripts/install.py`'s source for
      `.claude/agents/embarch-worker.md`) tells a worker to write drops to
      `/home/gabriel/Github/embarch/embarch-doc/inbox/` by **absolute** path, for
      the same reason `.claude/leg.md` gives the supervisor.
- [ ] Optionally, `inbox/README.md` states the same, since it is the doc a worker
      reads when deciding how to file one.
- [ ] Optionally, a supervisor-side backstop: sweep a worker's worktree `inbox/`
      into the main checkout before deleting the worktree. Cheap, and it covers
      the workers that predate the template fix.
