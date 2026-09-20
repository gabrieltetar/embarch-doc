# 069 — `embarch-ui/decisions/shape.md` and `spec.md` are in reserve

**State:** open
**Source:** `scripts/check-doc-size.py`'s reserve floor, crossed by decision 28 (the launcher's
focus-the-existing-tab change) and its one-line `spec.md` body edit
**Scope:** ui
**Hardware:** none
**Owner:** no
**Compacts:** embarch-ui/decisions/shape.md, embarch-ui/spec.md
**Size debt due:** 2026-10-17

## What

`decisions/shape.md` is **12,194 / 12,288 B (99.2%), 94 B left** and `spec.md` is
**11,211 / 10,240 B — 971 B OVER, up from 9,227 when this was filed** (`tasks/ui/070`, 2026-09-17: the Study Designer's row in the six-tab table, four new invariants about served facts, advisory caps, destructive-edit refusals and unchecked captures, and the `.dialog` count). Both are out of reserve when this closes, or the task
says why not and what was deleted instead.

`shape.md` is the file that matters: it now carries decisions 1, 2, 3, 9 and 28, and **28 alone is
most of its mass** — the measured focus round trip, four UI Automation invariants, the strategy
registry, the page title as a load-bearing interface, and four rejected alternatives.
`DOC-COMPACTION.md` §2 prefers a **split** over a squeeze and there is a clean seam here: 1, 2 and
9 are what the project *is* (one consolidated process, zero-build, the repo), while 3 and 28 are
both about the **VS Code launcher** and cite each other — 28 extends 3's thin-launcher stance
directly. A verbatim split of 3 + 28 into `decisions/launcher.md` restates nothing.

`spec.md` **was** one line over the floor and wanting a squeeze; it is now 971 B past its cap and wants a real one. The four invariants `ui/070` added are the kind this file exists for — each is a fact someone has to hold before they change the Study Designer — so the squeeze is elsewhere, or it is a split.

**`spec.md`'s half is paid, 2026-09-19** — by the unit that made the flux, in the same commit, as `DOC-BUDGET.md` requires. Decision 44's three Topology invariants would have taken it to 12,987 B, so the split it had been wanting landed instead: every invariant about **what a capture renders as** — the unnamed trace, the gap band, the axis tier, the stale prefix, the run badge, the unchecked capture, the outcome decoder, the capped ring, the partial line, `lagged`, `interrupted`, the post-run re-read and the shared axis — moved **verbatim** into `embarch-ui/spec/capture-rendering.md`, taking the trace chart's own paragraph with it. That file's mission is what a row, a gap, a clock and a console line *mean* once they reach the browser; `spec.md` keeps what this UI is and what it refuses. Nothing was reworded and nothing was deleted.

**Bytes:** `spec.md` 12,239 B → 10,154 B (under its 10,240 B cap, off the ledger). New `spec/capture-rendering.md`: 4,030 B. `decisions/shape.md`'s half is **untouched and still open** — 12,194 / 12,288 B, still wanting the launcher split this task describes.

**The human question, for the half that moved:** yes. `spec.md` alone still answers what someone needs to change the UI's *shape* — the five tabs, the Core boundary, the served-vocabulary rule, the roles-and-boards model — and a reader touching how a capture is drawn now has one file that is only about that, rather than thirteen bullets interleaved with tab descriptions. The two readers were never the same person.

## Why now

The debt is real once a file is within one amendment of its cap, and recording it is the
mechanism (`tasks/topology/014`'s wording, same rule): an unfiled file in reserve is what
`check-doc-size.py` fails on, not the reserve itself. 94 B left means the next correction to any
of the five decisions in `shape.md` cannot land without paying first.

## In flux: no

Nothing queued against `embarch-ui` targets either file for further edits as of 2026-09-17.
Decision 28 landed with its code in the same pass, and the only work it left open is a human's
manual pass over the launcher — a verification step, not a pending prose change.

## Done when

- [ ] `decisions/shape.md` and `spec.md` are both out of reserve, or the task says why not.
      **`spec.md` done 2026-09-19** (split into `spec/capture-rendering.md`, 12,239 → 10,154 B);
      `decisions/shape.md` still open.
- [ ] A split along the launcher seam (3 + 28) was preferred over deleting live reasoning, per
      `DOC-COMPACTION.md` §2 — or the report says why the seam was rejected.
- [ ] If it split: every inbound citation to `decisions/shape.md` still resolves, and
      `decisions.md`'s group table gained the new row.
- [ ] Decision 28's four invariants, the page-title interface and its four rejected alternatives
      survive in full — each one is a defect that was measured, not reasoned, and the title
      paragraph is what stops a later rename from silently restoring the original bug.
- [ ] Byte numbers before and after, for every file touched.
- [ ] `DOC-COMPACTION-PASS.md`'s human question answered in the report, in your own words: can
      `spec.md` alone answer what someone needs to work on the launcher today?
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10), `changelog.d/` fragment dropped.
