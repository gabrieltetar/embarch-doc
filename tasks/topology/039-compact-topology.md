# 039 — Compact `embarch-topology/decisions/crate.md`

**State:** open — **unparked 2026-09-13 by the leg folding `topology/041`.** Its stated unpark
condition was `tasks/core/055` landing; it landed today
(`86345c01a451b0696af36f42c28bf6676478124c`), and `topology/041` then closed decision 32 in the
same file. Both halves of the handoff this task was waiting on are settled, so `blocked` had
stopped meaning "nothing here can be done" — which is the only thing it is allowed to mean.
**Source:** `scripts/check-doc-size.py`, run as part of `tasks/topology/038`'s gate —
`embarch-topology/decisions/crate.md` landed at 95.0% of its cap (11676/12288 B, 612 B
left) after that task's decision 33 and decision 32 amendment, with no debt filed.
Filed in the same commit per `../../embarch-fleet/protocol.md` §5 and `tasks/README.md`.
**Scope:** topology
**Hardware:** none — reading and rewriting one doc file.
**Owner:** no

**Compacts:** embarch-topology/decisions/crate.md
**Size debt due:** 2026-09-20
**In flux:** no — **was `yes`, and the flux it named is over.** This file's own
Must-not-delete list below stated the condition explicitly: *"until `core/055` lands and either
decision can be written as settled rather than as an in-progress handoff."* `core/055` landed and
`topology/041` wrote the close, so decisions 32 and 33 can now be compacted as settled history
rather than as a live handoff.
**Must not delete:** decision 32's **close** — that both copies of the probe-selection rule are
gone and `embarch-core::resolve_probe` delegates to `select_probe`, threading a caller `action`
(`embarch-core` decision 61). The superseded 2026-09-13 *amendment* ("the topology half is landed;
`embarch-core` still holds its copy") is now provenance and may go, but **the fact that the
duplication is closed on both sides must survive.** Decision 33's three-divergence reconciliation
stays — what was chosen for zero-probes, the multi-probe predicate, and each error string, and
why; that is the hot half and nothing has superseded it.

## What

`embarch-topology/decisions/crate.md` (decisions 1, 2, 3, 6, 13, 32, 33) is in reserve —
the last 10% of its cap — and not yet blocked on anything else. Run a compaction pass
per `DOC-COMPACTION-PASS.md`, keeping the hot half (claim, constraint, invariant,
rejected alternatives with their one-clause reason, failure signature) and cutting the
cold half (provenance/dates, incident narrative, investigation log, superseded
reasoning) to git history, with a 250 B reversal row for anything cold worth keeping at
all. A split (moving decision 32/33 to their own topic file, or moving older cold
material out) is the default remedy to try first (`DOC-BUDGET.md` §2); squeeze only
where there is no seam.

## Why now

**In flux: yes.** Decision 32 is deliberately still open — `tasks/core/055` (blocked on
`038`'s landing) is the other half of the exact duplication this file's decisions 32/33
describe, and until it lands, decision 32's amendment and decision 33's reconciliation
are both live reference material for whoever picks that task up, not settled history yet.
Compacting now risks writing a clean, cold-feeling account of a close that has not
actually happened on the `embarch-core` side. `DOC-COMPACTION-PASS.md`'s own failure
mode: "Compacting a doc whose subsystem is still in flux — you would write a clean
statement of something about to be wrong, and destroy the alternatives you are about to
need. Wait for the milestone to close."

**This parks the pass, not the reserve** (`DOC-BUDGET.md` §2): the next unit that writes
`decisions/crate.md` before `core/055` lands still meets the cap mid-flight and must
compact then, carrying this task's `Must not delete:` list and closing only this item.

## Done when

- [ ] `tasks/core/055` has landed (`embarch-core::resolve_probe` calls `select_probe`).
- [ ] Decision 32 marked closed (or superseded) rather than amended-open.
- [ ] A compaction pass run per `DOC-COMPACTION-PASS.md`, keeping the hot half of
      decisions 1, 2, 3, 6, 13, 32, 33 and moving the cold half to git / a reversal row.
- [ ] `check-doc-size.py` green for `embarch-topology/decisions/crate.md` with room to
      spare, not just under cap.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `changelog.d/` fragment dropped.
