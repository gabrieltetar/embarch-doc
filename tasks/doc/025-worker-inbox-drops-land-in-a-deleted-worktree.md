# 025 — A worker's `inbox/` drop lands in its own worktree and is deleted with it

**State:** closed
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

- [x] The worker template (`embarch-fleet/scripts/install.py`'s source for
      `.claude/agents/embarch-worker.md`) tells a worker to write drops to
      `/home/gabriel/Github/embarch/embarch-doc/inbox/` by **absolute** path, for
      the same reason `.claude/leg.md` gives the supervisor.
- [x] Optionally, `inbox/README.md` states the same, since it is the doc a worker
      reads when deciding how to file one.
- [x] Optionally, a supervisor-side backstop: sweep a worker's worktree `inbox/`
      into the main checkout before deleting the worktree. Cheap, and it covers
      the workers that predate the template fix.

## Closed (owner session, 2026-09-08)

All three boxes, in `embarch-fleet` `9acf44a` — the templates, which is the only
place any of them may be written:

- `templates/.claude/agents/embarch-worker.md` — the drop bullet now names
  `{{DOC_REPO}}/inbox/` by absolute path, carries the reason (`inbox/` is
  gitignored, so a bare path lands in the worktree the supervisor is about to
  delete) and the `outpost/013` incident, and the "stay in your worktrees"
  bullet below it now names this as its one exception. Without that second edit
  the two bullets contradict each other, which is how a worker talks itself back
  into the relative path.
- `templates/protocol/inbox.README.md` — the same rule in the "Who may write
  here" section.
- `templates/.claude/leg.md` — the supervisor sweeps a worker's doc worktree
  `inbox/` into the main checkout before removing the tree. Taken rather than
  left optional because the drop's own complaint is that **nothing mechanical**
  would have caught this; an instruction to a worker is not a mechanism, and
  this costs the supervisor one `ls`.

`embarch-reviewer` needed no change: `leg.md` already requires it to be spawned
into the owner's checkout, so its relative `inbox/` is already the right
directory. `embarch-auditor` likewise runs from an ordinary session.

Deployed by latch, not by hand: `scripts/deploy.py --queue` pinned `9acf44a`
while leg 056 was mid-flight, so an `embarch-deployer` renders it into
`embarch-doc`'s `.claude/` and `inbox/README.md` at the next leg boundary and
the fleet loses no uptime. Until that lands, the instance copies still carry the
old text — the queued render, not this commit, is what closes the loop.

No `changelog.d/` or `status.d/` fragment: nothing in the suite's own docs
changed, only the fleet's instructions to itself.
