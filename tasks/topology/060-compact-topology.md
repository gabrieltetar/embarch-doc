# 060 — `decisions/enrollment.md` and `spec.md` are in reserve, and nothing filed the debt

**State:** blocked — both files are about to be rewritten by queued work (see `In flux`). Unparks
when `tasks/topology/059` lands, or is closed without touching either file; the clock below runs
regardless, and a verbatim split needs no unpark at all.
**Source:** `scripts/check-doc-size.py`, 2026-10-25. The owner's commits `bff9e91c`, `b93e48f7`,
`689e726f` (decisions 37–39, 2026-10-06) and `b85b23be` (decision 41, bench boards, 2026-10-09)
pushed both files into their reserve without a `Compacts:` line. The gate reported it only on
2026-10-25, once `embarch-study-designer/open.md`'s over-cap failure stopped masking it. Filed by
the supervisor, which did not write these bytes.
**Scope:** topology
**Hardware:** none
**Owner:** no

**Compacts:** embarch-topology/decisions/enrollment.md, embarch-topology/spec.md
**Size debt due:** 2026-11-01
**In flux:** yes — both. `tasks/topology/059` (a probe moved to a board of another chip refused by
name before any attach) changes what enrolment validation asserts, and `tasks/suite/046` (a bench
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

- [ ] Both files out of reserve (`scripts/check-doc-size.py --pressure`), or this task says per
      file why not.
- [ ] Any decision moved keeps its number, and every link to it resolves.
- [ ] `DOC-COMPACTION-PASS.md`'s human question answered in the compactor's own words.
- [ ] Gate green (`../../../embarch-fleet/gate.md`).
