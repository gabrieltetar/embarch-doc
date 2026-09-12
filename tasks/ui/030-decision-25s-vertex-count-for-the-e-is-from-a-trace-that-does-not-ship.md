# 030 — Decision 25's vertex count for the E is from a trace that does not ship

**State:** done (leg 091)
**Source:** refill sweep for scope spread, leg 090, 2026-09-11. Filed rather than dispatched because
leg 090 reached its four-unit cap; not yet re-verified by a supervisor, so **check every line number
below against the source before you act on it** — they are as the sweep reported them.
**Scope:** ui
**Hardware:** none.
**Owner:** no

## What

`embarch-ui/decisions/shell.md:29` says the inline header glyph is

> **16 vertices for the E, 15 plus a 4-vertex counter for the A, 657 B inline.**

Counting coordinate pairs per `Z`-terminated loop in the shipped path
(`embarch-ui/assets/index.html:34`) gives **22 plus a 4-vertex counter** for the first path and
**15 plus 4** for the second. So the A half of the sentence is exactly right and the E half is not.

The decision's own next clause is the explanation: the glyph is drawn in `"union"` mode, where the E
path is *the whole silhouette with the A painted over it*, so it necessarily carries more vertices
than a plain E. 16 is the E's count from the non-union trace — a number for an artifact that does
not ship. The sweep reports the sentence's other two numbers as correct: the standalone
`assets/brand/embarch-mark.svg` is 693 B with 53 vertices as stated, and `657 B inline` is exact.

## Why it costs something

Small, but this decision exists to make the inline glyph auditable — its whole argument is that the
simplification is checkable against the committed path. A number that does not match the committed
path is the one kind of error that argument cannot survive, and the next person to re-count will
re-derive the union explanation from scratch to account for the gap.

## What to do

Correct the E's count, **counting the coordinate pairs in `index.html:34` yourself** rather than
taking 22 from this task, and keep the union-mode clause that explains why the count is what it is.
Re-check the other two numbers in the same sentence while you are there. No rendered pixel changes
and no new numbered decision.

## A second, separable thing in the same sub-project

`decisions/gatt-capture.md:29` says of the uppercase-name bug: *"A separate value class opts out."*
That class — `.sd-param > span.sd-param-value` (`assets/style.css:650-655`) — is reported to have
**zero call sites** (`grep -c sd-param-value assets/app.js assets/index.html` → `0, 0`), decision 17
having replaced the inline `.sd-param` checkbox list with the targets dialog (`sd-targets-name`,
`app.js:2048`). So the documented opt-out is a dead rule.

Verify it, then either delete the dead CSS and correct the sentence, or — if the class is reachable
by some path the grep misses — say so here. **Do not delete the CSS without the sentence, or the
sentence without the CSS**; either alone leaves the same drift pointing the other way.

## Done when

- [x] Decision 25's E vertex count matches the committed inline path, verified by counting it.
      Recounted `index.html:34`'s first path myself: 22 coordinate pairs before the first `Z`, then
      a 4-vertex counter loop — matches the task's own recount, not the stale 16. Corrected
      `shell.md:29` to "22 vertices plus a 4-vertex counter for the E".
- [x] The union-mode explanation and the two correct numbers survive.
      `embarch-mark.svg` is still 693 B; grepped its path data and it does trace to 53 vertices as
      stated. `657 B inline` re-measured via `wc -c` on the two `<path>` elements in
      `index.html:34` and is exact.
- [x] `gatt-capture.md:29`'s opt-out claim and `.sd-param-value` are settled together, or the reason
      they were left is written here.
      Confirmed zero call sites (`grep -c sd-param-value assets/app.js assets/index.html` → `0, 0`).
      Deleted the dead rule and its comment from `style.css` (was lines 644-655) and corrected the
      sentence in `gatt-capture.md` to say the opt-out is dead now that decision 17's dialog
      replaced the checkbox list it styled.
- [x] No rendered colour or layout change, no new numbered decision.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10). `changelog.d/` fragment.
