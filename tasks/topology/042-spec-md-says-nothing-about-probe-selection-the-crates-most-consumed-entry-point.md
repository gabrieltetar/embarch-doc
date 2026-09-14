# 042 — `spec.md` says nothing about probe selection, and that is now the crate's most-consumed entry point

**State:** claimed — leg 111, 2026-09-13, branch `agent/topology/042-spec-md-probe-selection`.
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

## Dispatch note — leg 111, 2026-09-13

**Read this before you write a word into `spec.md`: the "it has room" line above is now wrong, and
that is the one thing in this task file you must not take on trust.** Measured today:
`embarch-topology/spec.md` is **9,037 / 10,240 B — 1,203 B of headroom**, and `check-doc-size.py`'s
reserve floor is **1,200 B**. So the file is **three bytes** from its reserve band. Any section
that actually answers this task's two substantive `Done when` boxes crosses it.

**That is not a reason to write less. It is a reason to plan for the debt, which is exactly what
the reserve band is for** (`.claude/leg.md`: a cap is a debt, not a wall — the gate still passes
inside reserve). Two acceptable outcomes, in order of preference:

1. **Write the section properly and file the debt in the same commit** as
   `tasks/topology/043-compact-topology.md` — **`tasks/topology/`, your own scope**, never
   `tasks/doc/`, which `check-ownership.py` refuses to every worker. `tasks/README.md` has the
   shape; it must carry a literal `**Compacts:** embarch-topology/spec.md`, a `**Size debt due:**`
   date (a park with no date is the one state the size gate fails), an `**In flux:**` answer
   **for that file specifically**, and a `**Must not delete:**` list. You are the only actor who
   will ever hold the context for the flux answer, which is the whole reason you file it rather
   than the supervisor.
2. **Or spend a few hundred bytes of `spec.md` on its way past** — `decisions/crate.md` just went
   12,075 B → 5,054 B in `topology/039`, so if some of `spec.md` is prose that the split moved into
   `decisions/probe-selection.md` and left restated here, deleting it is free and better than
   filing a debt. Check before assuming; do not manufacture a compaction to dodge a task file.

**Do not shrink the section to stay under the line.** A `spec.md` that technically fits and still
does not tell a caller what happens with zero probes has failed this task, and the reserve band
exists precisely so you do not have to make that trade.

Nothing else in `embarch-topology` is in reserve: `open.md` is 2,973 / 5,120 B,
`decisions/probe-selection.md` 5,437 / 12,288 B.

**One repo, one branch, one task.** Code repo `embarch-topology` (you may not need it at all —
this is one documentation file), docs in `embarch-doc`, both on
`agent/topology/042-spec-md-probe-selection`. `embarch-topology` has no path-dep siblings, so its
worktree needs no symlinks.
