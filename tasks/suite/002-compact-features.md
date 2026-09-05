# 002 — suite/features.md is in reserve, and it is the one file that always will be

**State:** blocked
**Source:** scripts/check-doc-size.py --pressure
**Scope:** suite
**Hardware:** none
**Compacts:** suite/features.md
**In flux:** yes — structurally, and permanently: every landing task adds or rewrites a row
**Must not delete:** any row. `DOC-COMPACTION.md` §2 gives this file the interfaces cap for the interfaces reason — every row must be present and the budget is spent on rows. Also keep the caveats that are facts about a capability rather than restatements of a decision: `deploy-core` reporting `landed` through a cancelled elevation, the Windows registry half being type-checked and not run, the brick hazard being closed.

## What

At ~93% of 15 KB. A 2026-09-04 pass took it 14706 → 14221 without dropping a
row, by cutting cells that broke this file's own opening rule — *deliberately a
pointer: the reasoning is in the owning decision, never restated here*. That
technique still has some room and `scripts/check-duplication.py` reports the
overlaps against each `spec.md`, but it is a diminishing return.

**This is a supervisor task, not a worker task** (`tasks/README.md`: a `suite`
scope is never dispatched), because a shared suite-level doc is outside every
worker's ownership row.

## Why blocked, and why that is different here

Every other file in the reserve is in flux because of specific open work.
This one is in flux **by construction**: it is an inventory of a suite under
active development, so a row lands roughly as often as a task does. There is no
state in which it is quiet, which means "wait for the flux to pass" is not an
available answer and §8's warning does not resolve it.

So this task is parked on the owner deciding the shape, not on other work
landing. The honest options, none of them free:

- **Split by maturity** — shipped rows in one file, Todo/Proposed/Retired in
  another. Cheap and it halves the file, but the whole value of this inventory
  is reading built and unbuilt side by side, which is exactly what it is for.
- **Split by sub-project**, one file each, with an index. Consistent with §3,
  and it destroys the one-page suite-wide read that made this file catch three
  status lies.
- **Drop the Retired rows** to `history/`. They are the cheapest bytes and the
  loudest ones — "Retired: it only ever worked against a foreground Core" is a
  rejection that stops being re-proposed because it is visible here.
- **Accept a larger cap for this role specifically**, on the argument §2 already
  concedes for an inventory: every row must be present, so the file's size is a
  function of the suite's size and not of anyone's discipline.

**Unparks when the owner picks one.** Do not compact it further in the meantime;
the last pass took the cells that were genuinely restating a decision.

## Done when

- [ ] The shape is decided and recorded, in `DOC-COMPACTION.md` §2 if it changes
      a cap and in this file's header if it changes what belongs here.
- [ ] Every capability the suite has is still findable in one place, whatever
      that place is.
- [ ] Gate green, `changelog.d/suite-*` fragment dropped.
