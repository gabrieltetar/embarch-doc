# 039 — Compact `embarch-topology/decisions/crate.md`

**State:** claimed by agent/topology/039-compact-topology, 2026-09-13 20:33 — **unparked
2026-09-13 by the leg folding `topology/041`.** Its stated unpark
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

**Reserve (told at dispatch, 2026-09-13 20:33):** exactly one `embarch-topology` file is in
reserve and it is the one you are compacting — `decisions/crate.md`, **98.3%**, **213 B left**,
the tightest headroom in the suite. So you have essentially no room to write before you cut:
**make the split or the cut your first edit, not your last.** Nothing else in this sub-project is
in reserve. This unit pays its own debt, so it files no new `compact-topology` task unless it
somehow pushes a *different* file into its last 10%.

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

**Corrected at dispatch, 2026-09-13.** The paragraph that stood here argued
`In flux: yes` and was true when written; it is not true now, and the header field above
was updated when this task was unparked while this section was not. Both halves of the
flux it named have settled: `tasks/core/055` landed
(`86345c01a451b0696af36f42c28bf6676478124c`) and `topology/041` closed decision 32 in
this very file. `DOC-COMPACTION-PASS.md`'s "wait for the milestone to close" failure mode
no longer applies here — the milestone closed.

**What makes it urgent rather than merely unparked:** the file is at **98.3%** of its cap
(12075/12288 B, **213 B left**) — the tightest reserve in the whole suite — and its debt
is the **soonest date on the ledger, 2026-09-20**. The next unit to write
`decisions/crate.md` meets the cap mid-flight.

## Done when

- [x] `tasks/core/055` has landed (`embarch-core::resolve_probe` calls `select_probe`) —
      landed 2026-09-13 as `86345c01a451b0696af36f42c28bf6676478124c`.
- [x] Decision 32 marked closed (or superseded) rather than amended-open — closed by
      `topology/041`, 2026-09-13.
- [ ] A compaction pass run per `DOC-COMPACTION-PASS.md`, keeping the hot half of
      decisions 1, 2, 3, 6, 13, 32, 33 and moving the cold half to git / a reversal row.
- [ ] `check-doc-size.py` green for `embarch-topology/decisions/crate.md` with room to
      spare, not just under cap.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `changelog.d/` fragment dropped.
