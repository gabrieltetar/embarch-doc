# 067 — Close decision 27's split as permanent, not a wait on `embarch-core`

**State:** open

**Filed by the supervisor, leg 139, drafted by the `core/085` worker.** The body below is that
worker's, unchanged. **It was written on the `core` branch and I lifted it off before merging**:
`tasks/ui/**` is not in a `core` worker's row (`protocol.md` §3), `check-ownership.py` refused the
branch over exactly this path, and **the instruction to file it there was mine** — `tasks/core/085`'s
dispatch note said "any `embarch-ui` follow-up is a task file in `tasks/ui/`, filed by you". That
was wrong and the worker was right to obey it; filing another scope's task is the supervisor's to
do, not a worker's. Recorded here rather than silently re-homed because the check caught a real
violation and it should stay visible that it caught one.

**Two ordering facts the body cannot know.** (1) `tasks/ui/066-compact-ui.md` is `blocked` on
`In flux: yes`, and leg 138's reasoning for that block was that `embarch-ui/open.md`'s decision-27
bullet *"will change again once `core/085` resolves"*. **`core/085` has now resolved**, and this
task is what changes that bullet — so whoever runs **this** task is the last writer of that bullet,
and `066` should be re-assessed for unblocking immediately afterwards, not before. (2) If your edit
here leaves `embarch-ui/open.md` in reserve with `066` still blocked, `.claude/leg.md`'s rule applies
and you compact that file as part of **this** unit, carrying `066`'s `Must not delete:` list.

**Source:** `embarch-core` decision 66 (`embarch-core/decisions/stream-index.md`), from
`tasks/core/085`. That task took the boundary call `tasks/ui/065` left open: whether
`embarch-core` ever serves the axis-health diagnostics and point events `trace.rs` still needs.
Decision 66's answer is no, permanently, for two independent reasons (already-named scope per
decision 62's `TraceView`-shape exclusion, and the point-event pass-coupling `ui/065` found makes
serving anything less than everything a non-retirement). A `core`-scoped worker cannot write this
repo's task queue, hence this file rather than a direct edit there.
**Scope:** ui
**Hardware:** none.

## What

Two small, precise edits, both already substantively correct and needing only their last sentence
updated from "waiting on `embarch-core`'s call" to "settled, permanently split":

1. `embarch-ui/open.md`'s bullet ("Settled as split-for-now, decision 27 — checked against
   `embarch-core`'s spans route and still blocked, precisely") currently ends *"Not this crate's
   fix — widening `embarch-core`'s `Gap` or diagnostics is filed to `inbox/`, not decided here."*
   That widening decision has now been made (`embarch-core` decision 66): `Gap` widened, everything
   else stays out, permanently. Update the closing sentence to say so and cite decision 66, and drop
   "split-for-now" from the bullet's own lead-in — it is no longer "for now."
2. `embarch-ui/decisions/trace-view.md` decision 27's closing sentence *"Widening `embarch-core`'s
   `Gap` or its diagnostics is that repo's call, filed to `inbox/` rather than decided or built
   here"* is now stale in the same way — the call has been made. Correct it to state the outcome
   (permanent split, `Gap` widened for parity but insufficient alone because point events stay
   excluded) and cite `embarch-core` decision 66.

No code change. `trace.rs` is unaffected — this task only updates the two docs that currently
describe the split as pending a decision that has since been taken.

## Why now

Leaving these two files saying "waiting on `embarch-core`" after `embarch-core` has answered is
exactly the stale-pointer failure mode `tasks/ui/042`/`048`/`063` already exist to prevent — a
reader who next asks "did `embarch-core` ever decide?" gets sent to `inbox/`, which no longer holds
the answer.

## Done when

- [ ] `embarch-ui/open.md`'s bullet ends stating the split is permanent, citing `embarch-core`
      decision 66, not "filed to `inbox/`, not decided here."
- [ ] `embarch-ui/decisions/trace-view.md` decision 27's closing sentence updated the same way.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `changelog.d/ui-decision-27-split-closed-as-permanent.md`.
