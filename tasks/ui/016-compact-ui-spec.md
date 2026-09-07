# 016 — `embarch-ui/spec.md` is in reserve

**State:** open
**Source:** `scripts/check-doc-size.py`'s reserve floor, added 2026-09-07
**Scope:** ui
**Hardware:** none
**Owner:** no
**Compacts:** embarch-ui/spec.md

## What

`spec.md` is **9,213 / 10,240 B (90.0%), 1,027 B left** — the tightest of the
five sub-project `spec.md` files, and it crossed on the rule change rather than
on an edit: reserve was 90% of a limit, and reserve is now
`max(1200 B, 10%)` from the top so that a file is warned while it still has a
seam to cut rather than 22 bytes before the wall.

**Prefer a split.** [DOC-COMPACTION.md](../../DOC-COMPACTION.md) §2: a split
restates nothing, so it costs no argument. A `spec.md` splits by surface — the
way `embarch-umbrella` split `decisions/projects.md` into `integration.md` and
`embarch-api` split `decisions.md` by mission — and the seam has to be checked
for inbound links before it is cut, which is the step
`tasks/umbrella/022` records getting right and nearly getting wrong.

Run `scripts/check-duplication.py embarch-ui` first: a `spec.md` in reserve
next to a `decisions/` directory in reserve usually means one of them is
re-arguing what the other owns, and deleting a duplicate is cheaper than either
a split or a squeeze.

## Why now

The debt is real once a file is within one amendment of its cap, and recording
it is the whole mechanism: an unfiled file in reserve is what
`check-doc-size.py` fails on, not the reserve itself. Two other `ui` size debts
are already open (`011` on `decisions/study-designer.md` at 224 B left, and the
`suite/features.md` row in `tasks/suite/004`), so a `ui` worker should read all
three before choosing where to spend a unit.

## In flux: no

Nothing in `spec.md` is mid-argument as of 2026-09-07. `ui/015` is open against
the trace view's rendering, not the spec.

## Done when

- [ ] `spec.md` is out of reserve, or the task says why it cannot be and what
      was done instead.
- [ ] Whichever it was — split, delete a duplicate, or squeeze — is stated,
      with the byte numbers before and after, and the seam's inbound links
      named if it was a split.
