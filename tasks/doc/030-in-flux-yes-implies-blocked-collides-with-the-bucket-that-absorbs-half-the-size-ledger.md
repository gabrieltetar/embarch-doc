# 030 — `In flux: yes` implies `blocked` collides with the bucket that already absorbs half the size ledger, and nothing has picked

**State:** open
**Source:** `tasks/doc/028`'s closure, owner's session 2026-09-09 — the one part of that task deliberately left undecided, extracted so it does not die with the file
**Scope:** doc
**Hardware:** none
**Owner:** required

## What

Two rules in this repo point opposite ways for the same four task files, and both are written down
as if the other did not exist.

- **`.claude/leg.md`**: a compaction task whose target is mid-change carries `In flux: yes`, and such
  a task must be `blocked`, naming what unparks it. An `open` one means the filer got it wrong.
  Leg 057 found two and corrected them by hand on that basis.
- **`scripts/check-doc-size.py`**'s own header calls `blocked` *"the parked state that absorbed 13
  of 28 debts"* and treats that absorption as the failure it is trying to end — a debt that is
  filed, at a wall, and invisible is worse than an unfiled one, which at least fails the gate.

So moving an `In flux: yes` task to `blocked` satisfies the first rule by doing exactly what the
second names as the problem. Four tasks sit on that contradiction today: `core/022`,
`dev-bench/012`, `doc/024`, `study-designer/006`. Each has a live, well-argued flux reason, so none
of them is simply a filer's mistake.

## Why now

`tasks/doc/028` built a gate check for the task-state vocabulary and had to decide whether to
enforce this rule as part of it. It did not, and said why in `check-task-state.py`'s header: picking
a winner silently, inside a checker, because one rule was easier to code, is the move `doc/028`
exists to stop. So the check **warns** on these four and fails on nothing, which keeps the
contradiction visible and unresolved rather than resolved wrongly.

That is the right holding position and it is not an answer. Left alone, the warning becomes
furniture — four lines nobody reads, on a corpus where the underlying debt keeps growing.

## Why this is `Owner: required`

Both sides are reserved paths: `.claude/leg.md` is the supervisor's own contract and
`scripts/check-doc-size.py` is the gate. A supervisor that can edit its own constraints has none.

## What the answer might be, without pre-deciding it

Three shapes, and the third is the one worth beating:

1. **`In flux: yes` stops implying `blocked`** and becomes an ordinary annotation on an `open`
   task — the flux reason is already prose that says what not to delete, and a leg reads it before
   compacting. Cheapest, and it concedes that the rule was over-strict.
2. **It keeps implying `blocked`**, and `check-doc-size.py` stops treating `blocked` as parked for
   this subclass — a debt blocked on *flux* is different from one blocked on another task.
3. **A third state for exactly this** — a debt that is real, owned, and correctly not actionable
   yet. That is what both rules are groping at from different sides, and it would let
   `check-doc-size.py` keep counting parked-on-a-task debts as the problem they are.

Note that (3) costs a fifth word in a vocabulary that was just enumerated and enforced, which is a
real price and should be paid deliberately if at all.

## Done when

- [ ] One of the three (or something else) is chosen and the reasoning is written where the losing
      rule lives, not only where the winning one does — both `.claude/leg.md` and
      `check-doc-size.py`'s header currently state their side as settled.
- [ ] The four tasks above end in whatever state the answer implies, and `check-task-state.py`'s
      warning either fires on nothing or is removed.
- [ ] If a fifth state is chosen: `tasks/README.md`, `check-task-state.py`'s `LEGAL`,
      `queue-status.py`'s `classify()` and `fold-commit.py`'s terminal set all learn it in the same
      change. Four consumers read this vocabulary and they must not disagree.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
