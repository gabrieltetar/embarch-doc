# 019 — `embarch-ui/decisions/trace-chart.md` crossed into reserve

**State:** claimed by agent/ui/019-compact-ui-trace-chart, 2026-09-08 22:34
**Source:** `ui/015` amended decision 23 to correct the `tr-gap`/`tr-cross` mixup
it was filed to fix, spending 663 B and pushing this file into reserve. `ui/017`
spent a further net 135 B stating `tr-cross`'s complete two-cause scope in
decision 10 rather than only in decision 23 — see its `Source:` line.
**Scope:** ui
**Hardware:** none
**Owner:** no

**Compacts:** embarch-ui/decisions/trace-chart.md
**Size debt due:** 2026-09-24
**In flux:** **no.** No open `ui` task touches this file. Decision 10 (the
chart half — zoom/pan/aggregation/study-action row, amended by `ui/017` to
state `tr-cross`'s two-cause scope) and decision 23 (the outcome decoder,
amended by `ui/015` and trimmed by `ui/017`) are both settled: nothing queued
rewrites either.
**Must not delete:** decision 10's three findings-of-the-same-shape list (the
overlapping-spans invariant, "a thread is never inside itself", and the
step-row clipping fix) — each is the only written record of a specific bug a
Rust test did not catch. The three-projection-pitfalls list (stale prefix,
anchor-is-a-frame's-arrival, clip-don't-move) and the gap-record-must-not-anchor
paragraph — load-bearing for anyone re-touching the projection. Decision 23's
two-wire-shapes explanation and the reason the fork stays client-side rather
than pushed onto the wire. The `ui/015` amendment paragraph itself must survive
compaction in substance: that `tr-gap` was tried first and was wrong, and why.

## What

`decisions/trace-chart.md` is **11,833 B against a 12,288 B cap** (96.3%,
455 B left) after `ui/017`'s decision-10/decision-23 edit (net +135 B: a new
two-cause statement for `tr-cross` in decision 10, kept under decision 10's
own 8,192 B pinned baseline — `check-doc-size.py` refused the first, larger
draft at 8,336 B, so the sentence was cut to fit the 173 B of headroom that
baseline still had — offset in the file total by trimming decision 23's now-
redundant paraphrase of the same claim). Nothing is blocked today; the next
edit to this file likely is.

## Why now

`check-doc-size.py --pressure` flags a file in reserve with no task naming it,
and `DOC-COMPACTION.md` §2 makes the spending commit the filing commit. `ui/015`
is that commit here.

## Done when

- [ ] `decisions/trace-chart.md` is clear of its reserve line.
- [ ] Every `Must not delete:` item above is still readable — check by grep
      against the post-compaction file, not by re-reading for feel.
- [ ] The commit message answers `DOC-COMPACTION-PASS.md`'s question in the
      compactor's own words.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).

**Renumbered from 016 by the owner's session, 2026-09-07.** A leg filed this as `016` in the same hour the owner's session filed `018` as `016`, both from `check-doc-size.py`'s reserve, and `check-task-numbers.py` caught the collision on `main`. History had already recorded `016` under the other slug, and `tasks/README.md` says a number is never reused, so this file moved rather than that one. Nothing about the debt changed.
