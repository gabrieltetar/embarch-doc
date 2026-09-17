# 066 — `embarch-ui/open.md` is in reserve

**State:** blocked — filed by `ui/065` worker, 2026-09-17, in the same commit that pushed the file
into reserve.
**Source:** `scripts/check-doc-size.py`'s reserve floor, hit by `tasks/ui/065`'s rewrite of the
trace-spans bullet (from a one-line "unblocks if `embarch-core` serves decoded per-lane spans" into
the field-for-field finding that it does not, yet) — `embarch-ui/open.md` went from 3,804 to
4,169/5,120 B, **951 B left**, inside the 1,200 B `RESERVE_FLOOR`.
**Scope:** ui
**Hardware:** none
**Owner:** no
**Compacts:** embarch-ui/open.md
**In flux:** yes. The bullet that grew is the trace-spans one, and it is not settled: `ui/065`
filed `/home/gabriel/Github/embarch/embarch-doc/inbox/core-widen-spans-gap-and-consider-axis-diagnostics.md`
asking `embarch-core` to decide whether to widen `Gap`/serve the axis diagnostics, or say decision
27's split is permanent. Whichever way that lands is very likely another edit to this same bullet —
compacting it now risks squeezing prose that is about to change again. **Unparks when** that
`core`-scope task (once filed with a number) lands, whichever way it decides, **or** a later reading
finds the bullet already stable enough to compact regardless — check `tasks/core/` for the filed
follow-up first.
**Size debt due:** 2026-10-01

## What

`embarch-ui/open.md`'s trace-spans bullet (paragraph 3) carries the full field-for-field finding
from `ui/065` at over 900 B — necessary at filing time (a shorter version would have hidden which
of the three gaps blocks what), but a candidate to shrink once the `core`-side decision lands and
the bullet can point at that decision instead of restating the finding inline.

## Why now

The debt is real once a file is within the last 10% of its cap, and recording it is the whole
mechanism (`tasks/ui/021`'s own wording, same rule).

## Done when

- [ ] `embarch-ui/open.md` is out of reserve, or the task says why it cannot be and what was
      deleted instead.
- [ ] Prefer pointing the trace-spans bullet at the settled `core`-side decision over restating the
      finding, once that decision exists — a link is shorter than a re-derivation.
- [ ] Whichever it was is stated, with the byte numbers before and after.

## Must not delete

- The three named gaps (thin `Gap`, absent axis diagnostics, point events built in the same pass as
  `Lane`/`Span`/`Gap`) — these are what stop a future worker from re-deriving `ui/065`'s comparison
  from scratch. Compacting to "blocked on `embarch-core`" alone would lose exactly the information
  this debt exists to keep.
