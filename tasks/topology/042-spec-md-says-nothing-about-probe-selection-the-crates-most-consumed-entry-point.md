# 042 — `spec.md` says nothing about probe selection, and that is now the crate's most-consumed entry point

**State:** open
**Source:** the supervisor's answer to `DOC-COMPACTION-PASS.md`'s human question while folding
`tasks/topology/039`, 2026-09-13. That unit split decisions 32 and 33 out of
`decisions/crate.md` into a new `decisions/probe-selection.md` and paid the size debt cleanly. The
question a compaction unit is actually judged on is *"can `spec.md` alone answer what someone
needs to work on this component today?"* — and for this crate the honest answer turned out to be
**no, not for probe selection**, which is a gap the split made visible rather than one it caused.
**Scope:** topology
**Hardware:** none — one documentation file. No board, no probe, no live Core, no deploy.
**Owner:** no

## What

`embarch-topology/spec.md` (9,037 B, well under cap) has eight sections — *What it is*, *Shape*,
*The declared facts*, *Storage and roles*, *What validation asserts, and what it cannot*, *What
each consumer owns now*, *What a caller may assume across calls*, *Where it stands*. Grepping it
for `select_probe`, `probe selection`, `multi-probe`, `zero-probe` and `ambiguous` returns
**nothing at all.**

Meanwhile:

- **`select_probe` is the single home of the probe-selection rule for the whole suite.**
  `embarch-topology` decision 32 closed the duplication in 2026-09-13's `topology/041`, and
  `embarch-core::resolve_probe` now *delegates* to it, threading a caller `action`
  (`embarch-core` decision 61, landed as `86345c01a451b0696af36f42c28bf6676478124c`).
- **Decision 33 reconciles three behavioural divergences** that a caller can observe directly:
  what happens with zero probes attached, the multi-probe predicate, and each error string.
- Both of those now live in `decisions/probe-selection.md`, which is where the reasoning
  belongs — but a decision file is the *why*, and `spec.md` is supposed to be the *what*.

So someone arriving at this crate today to work on, or call, its most cross-repo-consumed entry
point learns of its existence only by reading the decision set or the source. `spec.md`'s own
*What each consumer owns now* section is exactly where the delegation belongs and does not
mention it.

## Why now

**The split is what made this findable, and the moment after a split is when it is cheapest to
fix.** `decisions/crate.md` went 12,075 B (98.3%) → 5,054 B (41.1%) and `probe-selection.md` is a
new file at 5,437 B (44.2%), so there is real headroom on both sides and on `spec.md`. Nothing is
in flux: decision 32 is closed on both sides of the boundary, decision 33 is settled, and
`core/055` has landed.

This is also the second time in two days that a defect was found in a *sentence that does not
exist* rather than in one that is wrong — `topology/040`'s hardest finding was a comment whose
subject had been deleted three weeks earlier, and it survived two passes that were checking
numbers. A section missing from `spec.md` is the same class: no citation points at it, so no
sweep will ever visit it.

## Done when

- [ ] `spec.md` states, in the *Shape* or *What each consumer owns now* section, that probe
      selection is this crate's and that `embarch-core` delegates to it rather than holding a
      copy — linking decisions 32 and 33 by number, not by file path.
- [ ] A caller can learn from `spec.md` alone what the three observable behaviours are
      (zero probes, multiple probes, the error text contract) or where to read them, without
      being sent to the source.
- [ ] `spec.md` stays clear of its reserve line — it has room, but check with
      `check-doc-size.py` rather than assuming.
- [ ] Do **not** restate decisions 32/33's reasoning in `spec.md`. `DOC-PROTOCOL.md`'s
      no-restatement rule applies, and duplicating the very text a split just consolidated would
      be the exact failure this crate spent a unit undoing.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `changelog.d/` fragment. A numbered decision only if something was actually decided —
      writing down what is already true decides nothing.
