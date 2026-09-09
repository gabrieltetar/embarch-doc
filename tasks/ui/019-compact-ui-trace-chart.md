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

- [x] `decisions/trace-chart.md` is clear of its reserve line.
- [x] Every `Must not delete:` item above is still readable — check by grep
      against the post-compaction file, not by re-reading for feel.
- [x] The commit message answers `DOC-COMPACTION-PASS.md`'s question in the
      compactor's own words.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).

## Resolution — split, not squeeze

`DOC-BUDGET.md`'s split-first rule applied cleanly: decision 23 (the outcome
decoder) is a distinct mission from decision 10's chart-navigation half, and
this sub-project already splits `decisions.md` by mission into per-topic files
— decision 10 itself is already split three ways across `trace-view.md`
(trace half), `topology-tab.md` (routing half) and this file (chart half).
Decision 23 moved verbatim into a new `decisions/outcome-decode.md`, nothing
shortened, nothing paraphrased. `trace-chart.md` fell from 11,833 B to 8,801 B
(clear of both the file cap and its reserve), decision 10's own pinned
8,192 B baseline stayed intact (8,178 B after moving the split-out pointer
into the file's header rather than appending it after decision 10's body —
appending it there had pushed the pinned section to 8,429 B, over its own
ratchet, which is a separate, tighter cap than the file-level one).
`decisions.md`'s index table gained a row (`outcome-decode.md` | 23 | one
outcome decoder for both wire shapes) and lost nothing else. No decision
numbers moved, no cold reasoning was cut, no new numbered decision was
authored (this leg runs in burndown mode, which forbids that).

**Can `spec.md` alone answer what someone needs to work on this component
today?** Yes, and the split didn't change that answer either way — `spec.md`
already states the outcome-decoder invariant (line 75, citing decision 23) and
the trace-chart invariants without needing the decision prose; the decisions
files exist for "why is it like this", which is a different question the pass
protects rather than answers. This pass's job was narrower: make the *why*
loadable again without deleting any of it. It is — the file that was 96.3%
full is now two files, each with headroom, and every `Must not delete:` item
is still present verbatim (checked by grep, not by feel).

**Renumbered from 016 by the owner's session, 2026-09-07.** A leg filed this as `016` in the same hour the owner's session filed `018` as `016`, both from `check-doc-size.py`'s reserve, and `check-task-numbers.py` caught the collision on `main`. History had already recorded `016` under the other slug, and `tasks/README.md` says a number is never reused, so this file moved rather than that one. Nothing about the debt changed.
