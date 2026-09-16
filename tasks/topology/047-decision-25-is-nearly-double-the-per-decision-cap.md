# 047 — `embarch-topology` decision 25 is 7,818 B — nearly double the per-decision cap, and nothing tracks it

**State:** open
**Source:** leg 117, 2026-09-16. `core/063` closed the same gap for `embarch-core` decision 30 and
its own framing was *"nothing is watching it, and that is the actual finding."* I ran the full
census that task implied and it turned out to be true four more times: **five** decisions across the
suite are over [`DOC-BUDGET.md`](../../DOC-BUDGET.md)'s **4,096 B per-decision cap** with no pin in
`scripts/decision-size-baseline.json`, so nothing reports them and no ledger has a clock for them.
`core/063` fixed one and `core/064` files another. **This is the largest of the remaining four, and
the largest in the suite.**
**Scope:** topology
**Hardware:** none — doc prose only. No board, no probe, no live Core, no deploy.
**Owner:** no
**Compacts:** `embarch-topology/decisions/validation-classifier.md`
**In flux:** no — decision 25 is a *closed* classifier defect: two functions that had to agree on
which chips carry the `FICR.INFO.DEVICEID` pair, and did not. The fix landed. What is still open in
[`open.md`](../../embarch-topology/open.md) is a **hardware** gap, not doc flux — `nRF54L10`,
`nRF54L05` and `nRF54LM20A` take the same arm with no silicon ever attached — and no board is
coming to change this entry's text.

## What

`embarch-topology/decisions/validation-classifier.md#25` is **7,818 B** against a 4,096 B cap:
**3,722 B over, 191% of the limit**, and the single largest decision entry in the suite. Every other
over-cap decision is within ~3 KB of the line; this one is nearly a second decision's worth of prose
on its own.

The task is the same fork `core/063` faced, and it is much more likely to fall the other way here:

- **One decision that has accreted several arguments** → split it into two numbered decisions and
  update `embarch-topology/decisions.md`'s index — number list **and** size column, same commit.
- **One decision stated at length** → compact the entry under 4,096 B without losing the "why not",
  [`DOC-COMPACTION-PASS.md`](../../DOC-COMPACTION-PASS.md) in full, including quoting every cut hunk
  verbatim rather than naming categories.

**Read it before choosing.** At 191% of cap the split branch is genuinely on the table in a way it
was not for decision 30 (152 B over, compacted). But **a new decision number is the most expensive
thing in this suite to reverse**, so the burden of proof is on splitting: you have to be able to
name two claims that a citation could want to point at *separately*. If every inbound citation lands
on the same claim, it is one decision stated at length and you compact it.

## Why now

**Because the per-decision cap has no ledger and no clock.** The file-level ledger has both — a leg
spends its first unit on the oldest overdue entry. A decision that was never pinned is invisible to
everything: `check-doc-size.py --decisions` prints only its top 20 by size, which is how
`embarch-core` decision 30 sat over cap unnoticed until a reviewer opened the baseline file while
checking something unrelated. Whether that gap should be closed mechanically is the owner's call
under `scripts/` ([`tasks/doc/052`](../doc/052-a-verbatim-split-silently-drops-the-decision-size-pin-of-every-decision-it-moves.md)
records the adjacent defect). **This task is only about the one decision.**

## Watch for

- **Do not add a pin to `scripts/decision-size-baseline.json` to make the number go away.**
  `scripts/` is owner-reserved, and pinning an over-cap decision is the papering-over move, not the
  fix. `core/063` was told the same thing and did not.
- **Grep the whole doc repo for inbound `decision 25` citations before renumbering anything**, and
  remember a bare `decision 25` in another repo's file means *that* repo's 25, not this one. If you
  split, every existing citation still has to resolve to whichever half carries the claim it was
  citing, and `check-decision-refs.py` must stay green.
- **This entry's subject matter is a silent-failure story** — `"nRF54"` starts with `"nRF5"`, so
  unlisted nRF54L spellings matched the classic arm's guard first and never reached the newer pair,
  in both functions at once. That kind of reasoning is exactly what a compaction must **keep**: it
  is the "why not" that stops someone re-introducing the fall-through. Cut narrative and
  measurements, not the mechanism.
- **Report the before and after byte counts and the margin left**, the way `core/063` did.

## Done when

- [ ] `embarch-topology` decision 25 is at or under 4,096 B, or split into two decisions each under
      it, with the branch taken justified in the task body.
- [ ] `embarch-topology/decisions.md`'s index table matches — numbers and size column.
- [ ] Every inbound `decision 25` citation still resolves to the claim it was citing.
- [ ] If compacted: every cut hunk quoted verbatim in the task file, per `DOC-COMPACTION-PASS.md`.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
