# 023 — Nothing times the request path that serves a 250k-row trace; only `parse` itself is measured

**State:** claimed — leg 072
**Source:** `embarch-ui/open.md` — the 250,000-row cap bullet: "whether 1.69 s of server-side decode is acceptable against whatever answers `/study/{id}/streams` (unmeasured — nothing here times the request path, only `parse` itself)"
**Scope:** ui
**Hardware:** none — the existing `trace::scratch_view::synth_capture` builds the capture in
memory, with no file on disk and no board.
**Owner:** no

## What

The row cap is kept at 250,000 against a real measurement of **decode** — 257 ms at 250k, 604 ms
at 500k, 1.69 s at 1M, with resident view JSON of 4.48/9.03/18.1 MB [measured 2026-09-09]. What
that measurement cannot say is what a *request* costs, because nothing times the path from the
handler that answers a trace request down through decode and back out. Decode is a component of
that number, not the number.

Extend the existing `#[ignore]`d `measure_the_row_cap_at_scale` — or add a sibling beside it in
the same style — to time the **handler path** at the same three row counts, and record the result
in `embarch-ui/open.md` beside the decode figures, tagged **measured** with its date and build
profile the way the existing line is. If the request path cannot be exercised without a live
Core, say so plainly in the bullet rather than approximating it: an unmeasurable number stated as
measured is worse than the gap.

**Do not change the cap.** 250,000 is a decision with a recorded reason; this task supplies the
one input that decision named as missing, and whoever revisits the cap does so with it.

## Why now

`open.md` names this as the specific unknown that would have to be answered before the cap is
revisited, and the expensive half — a synthetic capture at three scales — is already built and
committed. The remaining work is instrumenting a path that already runs.

## Done when

- [ ] The request path is timed at 250k / 500k / 1M rows, or the bullet says why it cannot be.
- [ ] `embarch-ui/open.md`'s row-cap bullet carries the new figures, tagged measured, dated, with
      the build profile.
- [ ] The cap itself is unchanged, and nothing in this task's diff argues for changing it.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `changelog.d/` fragment dropped.
