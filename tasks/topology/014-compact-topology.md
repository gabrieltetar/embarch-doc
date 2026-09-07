# 014 — `embarch-topology/open.md` is in reserve

**State:** open
**Source:** `scripts/check-doc-size.py`'s reserve floor, added 2026-09-07
**Scope:** topology
**Hardware:** none
**Owner:** no
**Compacts:** embarch-topology/open.md

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
