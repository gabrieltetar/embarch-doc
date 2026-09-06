# 004 — `embarch-decision-reversals.md` and `suite/features.md` are in reserve

**State:** blocked
**Source:** `scripts/check-doc-size.py` went RED during leg 013's `umbrella/007` fold — both
files crossed their reserve lines inside that fold, one by a supervisor edit and one by an
assembler run.
**Scope:** suite
**Hardware:** none
**Compacts:** embarch-decision-reversals.md, suite/features.md
**In flux:** yes — see "Why blocked". The two files are in flux for **different reasons**,
and only one of them is the ordinary kind.
**Must not delete:** every reversal row's **shape number** and the citation that resolves it
(the shape number is how a row is referred to from elsewhere, and rows are cited by number
from `DOC-PROTOCOL.md` and from sub-project decisions); the "Review-driven reversals"
section's distinction between a reversal *found by review* and one found by a failure; and,
in `suite/features.md`, **nothing** — see below, because deleting from it is not the move.

## What

- **`embarch-decision-reversals.md` — 9,309 / 10,240 B, 931 B left (90.9%).** I put it
  there myself, folding `umbrella/007`'s `status.d/` fragment: the target-count-scanner
  bullet gained the three-day lag between the reversal being documented (2026-09-02) and
  executed (2026-09-05). That lag is the finding, so the bullet earned its bytes — but it
  is the supervisor, not a worker, who spent the reserve here, and the debt is owed the
  same way.
- **`suite/features.md` — 18,537 / 20,480 B, 1,943 B left (90.5%).** Crossed by
  `python3 scripts/build_features.py` during the same fold, which rewrote the
  `umbrella-030` row from `umbrella/007`'s `features.d/` fragment. **No human edited it.**

## The structural problem, which is the real reason this is filed rather than done

**`suite/features.md` is assembled and never hand-edited.** `protocol.md` §3 marks it
`never` for every worker scope; `check-ownership.py` refuses it to all of them; and
`build_features.py` regenerates it wholesale from `features.d/` on every fold. So the
instruction `check-doc-size.py` prints when it goes red — *shorten the file and file a
compaction task* — **names an action nobody is allowed to take on this file, and which the
next fold would overwrite anyway.**

There are only three real moves and **two of them are the owner's**:

1. **Shorten the `features.d/` fragments**, which is where the bytes actually live. 119 rows
   across 9 sections; the fragments are individually owned by their sub-project's workers,
   so this is a per-scope act and not a suite act at all — which is the opposite of how the
   cap is enforced.
2. **Raise the cap for an assembled file**, on the argument that a role cap is a limit on
   what a *reader* should have to hold, and a generated inventory is a lookup table rather
   than a document to read through. `scripts/` is owner-reserved, so this is not the
   fleet's to do.
3. **Split the inventory by section**, which changes what `build_features.py` emits and is
   likewise `scripts/`.

**This file will re-enter reserve on the next feature row whatever anyone does to it
today**, and at 119 rows the growth is monotonic by design — the inventory records what the
suite has, and the suite gains capabilities. Filing a compaction task against it every time
is a treadmill, which is the signal that the cap is being applied to the wrong artifact.

## Why blocked

- **`embarch-decision-reversals.md`** — genuinely in flux. It gains a row whenever any unit
  finds a reversal, and this leg alone edited it once. Unparks when a leg is not actively
  filing reversals into it; the pass itself is ordinary shortening.
- **`suite/features.md`** — blocked on the owner, not on flux. **Do not dispatch a worker at
  it.** Nobody in the fleet can write it, and shortening the fragments is a different task
  in a different scope.

## Done when

- [ ] `embarch-decision-reversals.md` is back under its 9,216 B reserve line, with every
      shape number and citation still findable by search.
- [ ] `suite/features.md` has an answer that is not "compact it": either the cap moves, the
      inventory splits, or the fragments shrink. **Whichever it is, it is a decision, and
      recording it is the point** — otherwise this task is refiled every few folds forever.
- [ ] `DOC-COMPACTION-PASS.md`'s human question answered for whatever pass actually runs.
- [ ] Gate green.
