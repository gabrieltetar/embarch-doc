# 071 — `embarch-ui/open.md` is in reserve

**State:** done
**Source:** `scripts/check-doc-size.py`'s reserve floor, crossed by `tasks/ui/070`'s two new entries
**Scope:** ui
**Hardware:** none
**Owner:** no
**Compacts:** embarch-ui/open.md
**Size debt due:** 2026-09-24
**In flux:** no

## What

`open.md` was **6,630 / 5,120 B (over cap by 1,510 B, past its 2026-09-24 clock)** — one of
three files turning `main`'s `check-doc-size.py` RED. The other two
(`embarch-core/decisions/handshake.md`, `embarch-ui/decisions/shell.md`) are not this task's;
`shell.md` is `tasks/ui/073` and was left untouched, as were `decisions/shape.md` (`069`),
`decisions/topology-boards.md` (`073`) and `decisions/study-designer.md` (`072`).

## What shipped

**Two retirements, no attrition:**

1. **The decision-27 entry left the file outright.** It was marked "settled, permanently — not
   pending" and its content already lives verbatim in `decisions/trace-view.md`'s own decision 27
   (`embarch-core` decision 66 is cited there as the record). A settled entry duplicated in an
   unresolved-only file is redundant, not informative; removing it closes nothing, because nothing
   here was the only place it was said.
2. **The 250,000-row measurement table moved to `decisions/trace-rows.md`'s decision 21** (the
   decision that already owns the served row cap), as a new paragraph: "**250,000 is kept on
   measurement, not extrapolation**" with the full decode/encode-at-scale table. `open.md` kept
   only the genuinely open half — the three Core calls' end-to-end HTTP cost is still unmeasured —
   condensed to two sentences that cite the decision for the settled part.
3. **The GATT-vs-trace placement validation moved to `decisions/time-chart.md`'s decision 34** (the
   Time-chart decision it validates), as a new paragraph citing the `b1e9ec7d` study and its 64/64
   and 125/245 figures. `open.md` kept only the still-open half — no power-capture study has ever
   been run — condensed to one sentence citing the decision.

Every other bullet's wording was tightened (redundant words cut, no fact or trigger removed) to
close the remaining gap to the cap. Nothing else was deleted, no other trigger was rephrased away
from what it names, and no cross-repo pointer (`embarch-study-designer/open.md`, `tasks/core/093`)
was touched.

**Bytes:** `open.md` 6,630 B → **4,867 B** (under its 5,120 B cap, off the ledger). Moved-to files:
`decisions/trace-rows.md` 3,046 B → 3,830 B; `decisions/time-chart.md` 8,910 B → 9,322 B — both
comfortably inside their 12,288 B decision-group cap (trace-rows.md at 31%, time-chart.md at 76%).

**Out of reserve: no, and here is why not.** The reserve floor for a 5,120 B `open.md` is
`max(1,200, 10%) = 1,200 B` from the top, i.e. **3,920 B**. `open.md` sits at **4,867 B (95.1%,
253 B left)** — under cap, but still inside the reserve band. Every remaining bullet is a distinct
open question carrying its own trigger, its own evidence, or a cross-repo pointer nothing else
states; the two moves above were the only cases where a bullet mixed *settled* evidence with a
*still-open* remainder, and both are now made. Getting under 3,920 B from here would mean deleting
an entire question (attrition, forbidden by this task) rather than tightening prose around one —
so this is reported as the honest stopping point, not squeezed further. Follow-up filed:
`tasks/ui/074-compact-ui-open.md` (§5 of the worker contract — a file still in reserve with no
open item pointed at it fails the gate the moment this task's own `Compacts:` line stops counting).

## Done when

- [x] `open.md` out of reserve, or the task says why not. **Said why not, above.**
- [x] **No open question was closed to make room.** Both moves above name where the settled half
      now lives (`decisions/trace-rows.md` 21, `decisions/time-chart.md` 34); the still-open half
      of each stayed in `open.md`, shorter but not gone. The decision-27 removal is not "a question
      closed" — the entry itself said it was settled, permanently, before this task began.
- [x] The decision-27 entry's fate is decided explicitly: **it left the file** — the settled
      sentence and the entry both leave together, per the task's own instruction, since the
      settled content was already recorded (and remains recorded) in `decisions/trace-view.md`.
- [x] Byte numbers before and after: see "What shipped" above.
- [x] Gate green for this file. Whole-repo `check-doc-size.py` still fails on
      `embarch-core/decisions/handshake.md` and `embarch-ui/decisions/shell.md`, both pre-existing
      and out of this task's scope (see claim-line dispatch note). `changelog.d/` fragment dropped.
