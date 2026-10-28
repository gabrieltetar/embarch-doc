# 060 — `decisions/enrollment.md` and `spec.md` are in reserve, and nothing filed the debt

**State:** done — 2026-10-28, closed by `tasks/topology/066`'s leg (verbatim split of decision 41 and 16; see below).
**Source:** `scripts/check-doc-size.py`, 2026-10-25. The owner's commits `bff9e91c`, `b93e48f7`,
`689e726f` (decisions 37–39, 2026-10-06) and `b85b23be` (decision 41, bench boards, 2026-10-09)
pushed both files into their reserve without a `Compacts:` line. The gate reported it only on
2026-10-25, once `embarch-study-designer/open.md`'s over-cap failure stopped masking it. Filed by
the supervisor, which did not write these bytes.
**Scope:** topology
**Hardware:** none
**Owner:** no

**Size debt due:** 2026-11-01
**In flux:** yes — `decisions/enrollment.md` only. `tasks/topology/059` wrote decision 44 into
`decisions/validation.md`, not this file, and split `spec.md` verbatim (below); `tasks/suite/046` (a bench
board owns a signal and is read and validated by its probe) extends decision 41 itself. Squeezing
either file now writes a clean statement of something two queued tasks are about to change.
**Must not delete:** nothing specific is known to the filer, which did not write these bytes. Treat
every measured fact in either file (in `spec.md`, the STM32 identity reads that decisions 37–39
added: the halted UID read on ARMv6 parts, the all-zero ID, the guarded attach) as evidence, not
prose: each reads as an assumption once its date or its board goes.

## What

`embarch-topology/decisions/enrollment.md` is **12,045 / 12,288 B (243 B left)** and
`embarch-topology/spec.md` is **9,550 / 10,240 B (690 B left)**, both inside the reserve band of
`DOC-BUDGET.md`. When done, both are out of reserve, or this task says why one cannot be.

## Why now

The gate fails on a file in reserve that no task names, so `check-docs.py` was red on `main` for
every unit in the suite until this was filed.

## The move

**A verbatim split first** (`DOC-BUDGET.md`: a split restates nothing, so `In flux: yes` does not
forbid one). `decisions/enrollment.md` holds decisions 14, 15, 16, 28, 35 and 41; decision 41 (a
bench board enrolled with no role) is the newest and the one `suite/046` extends, so moving it to
a topic file of its own is the obvious seam and pays the debt without shortening anything. Check inbound links before
moving a decision (`check-decision-refs.py`, and `tasks/umbrella/022` nearly moved the wrong one).
`spec.md` compacts only where there is no seam. Whoever next writes either file in a unit
(`topology/059` is the likely one) does this in the same commit, closing only that file's item.

## Done when

- [x] Both files out of reserve (`scripts/check-doc-size.py --pressure`), or this task says per
      file why not.
- [x] Any decision moved keeps its number, and every link to it resolves.
- [x] `DOC-COMPACTION-PASS.md`'s human question answered in the compactor's own words.
- [x] Gate green (`../../../embarch-fleet/gate.md`).

## 2026-10-26, `topology/059`

`spec.md` is paid: 059 wrote one bullet into it and moved "What each consumer owns now" verbatim to
`spec/consumers.md` (now 81.7%); no measured STM32 identity fact moved or changed. Its item is closed
and it is off `Compacts:`. `decisions/enrollment.md` was not written by 059 and is untouched; it
stays parked on `suite/046` (decision 41).

## 2026-10-28, `topology/066`

`decisions/enrollment.md` is out of reserve: 12,122 B -> 10,395 B. Decisions 41 and 16 moved verbatim
to `decisions/enrollment-bench.md` (2,372 B); 41 keeps a pointer in `enrollment.md` because
`embarch-core/decisions/roles.md` and `embarch-dev-bench/decisions/pd-bench.md` link that path for
it. No text in `enrollment.md` was shortened, so the `suite/046` flux was not touched. `spec.md` was
paid on 2026-10-26 (above). Human question: yes, `spec.md` still answers it; nothing in it moved.
