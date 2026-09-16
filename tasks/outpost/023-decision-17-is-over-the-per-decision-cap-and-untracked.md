# 023 — `embarch-outpost` decision 17 is over the per-decision cap and untracked

**State:** claimed by agent/outpost/023-decision-17-over-cap, 2026-09-16 12:54
**Reserve (leg 118):** no `embarch-outpost` file is in the last 10% of its cap. If your work pushes
one into reserve, file `tasks/outpost/<NNN>-compact-outpost.md` in the same commit.
**Source:** leg 117, 2026-09-16. `core/063` closed this gap for `embarch-core` decision 30 and named
the real finding as *"nothing is watching it."* I ran the census that implied: **five** decisions
suite-wide are over [`DOC-BUDGET.md`](../../DOC-BUDGET.md)'s **4,096 B per-decision cap** with no pin
in `scripts/decision-size-baseline.json`. `core/063` fixed one; `core/064`, `topology/047` and
`umbrella/068` file three more. **This is the fifth and the smallest breach.**
**Scope:** outpost
**Hardware:** none — doc prose only. No board, no probe, no live Core, no capture read.
**Owner:** no
**Compacts:** `embarch-outpost/decisions/clocks.md`
**In flux:** no. Decision 17 is the two-clocks split — `cycles` measures, `rx_utc_ms` places — and
it has been settled since it was written. What is still open in
[`embarch-ui/open.md`](../../embarch-ui/open.md) and
[`embarch-topology/open.md`](../../embarch-topology/open.md) is that **nothing has compared a
trace's placement against a second stream**, and that no signal tap has read a byte. Those are
**hardware debts against decision 17's claims**, not doc flux: no board is coming to change this
entry's text, and if one ever does it will *add* a measurement rather than rewrite the split.

## What

`embarch-outpost/decisions/clocks.md#17` is **4,559 B** against the 4,096 B cap: **463 B over, 111%
of the limit.** The smallest of the five breaches, and the one most likely to be a straight
compaction rather than a split.

The fork, same as `core/063`'s:

- **One decision stated at length** → compact under 4,096 B without losing the "why not",
  [`DOC-COMPACTION-PASS.md`](../../DOC-COMPACTION-PASS.md) in full, including quoting every cut hunk
  verbatim rather than naming categories. **463 B is a realistic squeeze** — `core/063` cut 698 B out
  of a comparable entry by removing one incident blockquote.
- **One decision that has accreted several arguments** → split into two numbered decisions and
  update `embarch-outpost/decisions.md`'s index, number list **and** size column, same commit.
  **A new decision number is the most expensive thing in this suite to reverse**, so the burden of
  proof is on this branch, and at 111% of cap it is a hard case to make.

**Read it before choosing** rather than assuming the small breach means the easy answer.

## Why now

**Because the per-decision cap has no ledger and no clock.** The file-level ledger has both. A
decision that was never pinned is invisible to everything: `check-doc-size.py --decisions` prints
only its top 20 by size, which is how `embarch-core` decision 30 sat over cap until a reviewer opened
the baseline file while checking something unrelated. Whether that gap should be closed mechanically
is the owner's call under `scripts/`
([`tasks/doc/052`](../doc/052-a-verbatim-split-silently-drops-the-decision-size-pin-of-every-decision-it-moves.md)
records the adjacent defect). **This task is only about the one decision.**

## Watch for

- **Do not add a pin to `scripts/decision-size-baseline.json` to make the number go away.**
  `scripts/` is owner-reserved, and pinning an over-cap decision is the papering-over move.
- **Decision 17 cites `embarch-core` decision 30 by name** for the `rx_utc_ms` per-frame stamp — and
  `core/063` compacted that very decision earlier today (4,248 B → 3,550 B). **Check that what this
  entry says decision 30 does is still what decision 30 says**, against `main`, before you touch
  anything. The cut there was the retired-alias blockquote, not the epoch-clock paragraph, so this
  should hold — but "should hold" is exactly the kind of claim a sweep exists to verify.
- **Keep the "why not".** The entry's load-bearing sentence is that the DUT's counter **cannot** place
  a trace at all because there is no sync point between the two clocks. Losing that invites someone
  re-proposing a single-clock design. Cut measurement detail and narrative, not the impossibility
  argument.
- **Grep the whole doc repo for inbound `decision 17` citations before renumbering anything**, and
  remember a bare `decision 17` in another repo's file means *that* repo's 17 — `embarch-api` and
  `embarch-topology` both have their own real, unrelated decision 17, which is the collision
  `api/099` spent this leg fixing in a shared crate.
- **Report before/after byte counts and the margin left**, the way `core/063` did.

## Done when

- [ ] `embarch-outpost` decision 17 is at or under 4,096 B, or split into two decisions each under
      it, with the branch taken justified in the task body.
- [ ] `embarch-outpost/decisions.md`'s index table matches — numbers and size column.
- [ ] The entry's claim about `embarch-core` decision 30 re-checked against that decision's current
      text on `main`.
- [ ] Every inbound `decision 17` citation still resolves to the claim it was citing.
- [ ] If compacted: every cut hunk quoted verbatim in the task file, per `DOC-COMPACTION-PASS.md`.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
