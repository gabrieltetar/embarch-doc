# 014 — `embarch-topology/open.md` is in reserve

**State:** open
**Source:** `scripts/check-doc-size.py`'s reserve floor, added 2026-09-07
**Scope:** topology
**Hardware:** none
**Owner:** no
**Compacts:** embarch-topology/open.md
**Size debt due:** 2026-10-08

## What

`open.md` is **4,206 / 5,120 B (82.1%), 914 B left**. It crossed on the rule
change rather than on an edit: reserve was 90% of a limit, which for a 5 KB
`open.md` is 512 B, and 512 B is not one amendment's runway — the 2026-09-06
fold records single additions of 350 B, ~940 B and 1,548 B. Reserve is now
`max(1200 B, 10%)` from the top.

**Prefer a split.** [DOC-COMPACTION.md](../../DOC-COMPACTION.md) §2: a split
restates nothing, so it costs no argument, and a file warned 1.2 KB out still
has a seam to cut. This one may not have a seam — a 5 KB `open.md` is a role
cap on a single file, and `tasks/umbrella/009` records reaching exactly that
wall — in which case say so and delete an answered question instead.

`topology/008` took this same file from 97.9% to 56.0% on 2026-09-06 by
deleting answered questions, so the recent history of what is answerable is
short and worth reading before cutting.

## Why now

The debt is real once a file is within one amendment of its cap, and recording
it is the whole mechanism: an unfiled file in reserve is what
`check-doc-size.py` fails on, not the reserve itself.

## In flux: no

Nothing here is mid-argument as of 2026-09-07 — `topology/012` and `013` are
open against `decisions.md`, not this file.

## Done when

- [ ] `open.md` is out of reserve, or the task says why it cannot be and what
      was deleted instead.
- [ ] Whichever it was — split or delete — is stated, with the byte numbers
      before and after.

## Spend recorded against this task

**2026-09-08, leg 054, folding `topology/022` (doc `e420bf5`): `open.md` 4,841 → 5,016 B, +175,
leaving 104 B of headroom against the 5,120 cap.** `topology/022` amended `decisions/crate.md`
decision 4 to say the `embarch-umbrella/src/token.rs` mirror is closed, and its reviewer found that
the mirrors bullet here still counted that mirror among two that "still raise the
extract-or-CI-diff question" — a line the unit's own landing made wrong. I corrected it in the fold
rather than filing it, and the correction costs bytes because the honest version has to say *how*
the mirror closed (a direct call, which is a third answer neither of this bullet's two had) rather
than just dropping it. Recorded here rather than filed as a new task, per `tasks/topology/022`'s own
reserve note. **104 B is the tightest this file has been**; the next edit to it very likely cannot
be paid this way and this pass should run first.
