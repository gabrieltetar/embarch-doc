# 083 — Task 076's "Resolved" section still asserts decision 65's retracted directional claim

**State:** open — drained from `inbox/core-task-076-retains-retracted-likely-low-claim.md` by leg 138
at `ui/065`'s fold, 2026-09-17. Body unchanged apart from this line, the number, and the scope
correction below.
**Source:** review of `core/080` (merge `74c410b` in `embarch-doc`). `core/080` corrected
`embarch-core/decisions/stream-index.md` decision 65 from "likely-low ... understating a populated
capture's row width" to "order-of-magnitude, direction of error not established," naming the
rx_utc_ms gap, the fixture's own ~3x row-width spread (22–67 B around a 51.4 B mean), and the
4-lane/7-name vs 26-lane/112,804-span structural mismatch. `tasks/core/076-serve-decoded-per-lane-spans-on-a-load-sibling-route.md`
carries the identical CSV-size argument in its own "Resolved (this task, 2026-09-17)" section
(lines ~82-85) and was not touched by `core/080`'s commit.
**Scope:** core
**Hardware:** none — one paragraph of a completed task file; re-checked by leg 138 and it holds.
**Owner:** no

**Scope corrected from `doc` to `core` by leg 138 at the drain.** The only path this touches is
`tasks/core/076-…md`, which `check-ownership.py` places squarely inside a `core` worker's row
(`tasks/core/**`). Filed as `doc` it would have sat in the queue behind the owner-reserved band and
waited for a human who does not need to be involved.

## What

`tasks/core/076...md`'s "Resolved" paragraph still reads: "≈ 11.8 MB, a likely-low estimate (this
fixture's `rx_utc_ms` column is empty throughout, which understates a populated capture's row
width). The comparison holds: same order of magnitude as 12.6 MB, not materially smaller." It then
says "Full writeup: decision 65, `embarch-core/decisions/stream-index.md`" — pointing a reader at
a decision file that no longer makes this claim. The task file is `done`, not itself something a
worker will revisit, so nothing else will naturally correct it. This is not a contradiction `core/080`
introduced — it is the retracted claim surviving in a second document `core/080` did not know to
touch, which is the residue class `DOC-COMPACTION-PASS.md`-era reviews keep finding once a
directional claim gets walked back.

Update `tasks/core/076...md`'s "Resolved" paragraph to match the corrected framing (or add a short
dated note pointing forward to decision 65's `core/080` correction), so a reader of the task file
alone doesn't come away with the retracted "likely-low" claim as settled fact.

## Why now

Found during `core/080`'s decision-contradiction review. Left standing, it is the specific failure
mode the review charter targets: a retracted claim that reads as live somewhere the fix didn't
reach.

## Done when

- [ ] `tasks/core/076...md`'s "Resolved" section either matches decision 65's current
      (`core/080`) language or explicitly notes it was superseded there, with a date.
- [ ] No other completed task file in `tasks/core/` still states the CSV estimate as "likely-low"
      or "understating" (grep for both terms turned up only this file and the changelog fragment,
      which is dated and not misleading).
- [ ] Gate green.
