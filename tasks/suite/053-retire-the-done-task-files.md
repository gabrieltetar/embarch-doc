# 053 — Retire the 87 task files that say `done` and were never folded away

**State:** open — drained from `inbox/` and announced 2026-10-29 14:28:58 (`ts` `1793305738.327939`); the 30-minute window closes 14:58:58. A later leg reads the thread and runs it.
**Source:** owner's session, 2026-10-29 — cleanup pass; `queue-status.py` lists 87 `done` rows on `main`
**Scope:** suite
**Hardware:** none
**Owner:** no

## What

Every task file on `main` whose `State:` is `done` at token zero is `git rm`'d, so
`tasks/` holds only work that is still open, claimed or blocked. On 2026-10-29
that was 87 files: core 21, api 18, topology 12, ui 12, study-designer 9,
umbrella 6, dev-bench 4, suite 4, outpost 1. They are the backlog of the fold
bug `tasks/doc/050` and `082` described. The owner fixed the cause the same day
(`fold-commit.py` now retires a task file the fold edited), so this is a one-off:
nothing should refill it.

A file is retired as-is, with one exception: a body that still carries something
with no other home — an unticked `Done when` box, a "left open" or "deliberately
not done" note, a follow-up named nowhere else. That item moves first, into the
owning sub-project's `open.md` or an `inbox/` drop, and the retirement commit
names where it went. Nothing a task recorded is lost by deleting its file.

## Why now

The owner's cleanup pass, 2026-10-29. 87 dead rows make `queue-status.py` output
and every refill sweep longer, and a `done` file is indistinguishable at a glance
from one that is about to be worked.

## Done when

- [ ] `queue-status.py` shows no `done` rows.
- [ ] Each retired file whose body carried an orphaned follow-up has that item
      re-homed, and the commit message names file → destination for each.
- [ ] No doc links a retired task file: `check-links.py` green, every inbound
      link repointed at the decision or commit the task produced.
- [ ] `check-task-numbers.py` green (retired numbers stay retired).
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10). One commit per scope
      is fine; the leg digest lists the count per scope and every re-homed item.
