# 001 — The Trace view's remaining cost is a 13 MB JSON the browser waits for; bin it server-side

**State:** claimed by agent/ui/001-trace-view-server-side-binning, 2026-09-04 23:05

**Doc-size reserve at dispatch (supervisor, leg 009):** **no `embarch-ui` file is in
reserve** — the only file in reserve suite-wide is `embarch-umbrella/spec.md`, and it
is filed. So you have normal headroom; if any `embarch-ui` file enters reserve on your
commit, file `tasks/doc/<NNN>-compact-ui.md` in the same commit
(`tasks/README.md` has the shape).
**Source:** [embarch-ui/open.md](../../embarch-ui/open.md) — "The Trace view's cost at real volume is the transfer, not the cap."
**Scope:** ui
**Hardware:** none

## What

`embarch-ui`'s Trace view serializes a whole capture to the browser and then
aggregates it there. On the reference capture that is **225,606 rows — 90% of the
250,000-row cap — arriving as a ~13 MB JSON** the browser blocks on and then holds
112,801 spans from. Decision 10's aggregation already made *drawing* independent of
dataset size, so load time is the only remaining term.

Build the `?from&to&width` endpoint `open.md` names: the same binning the browser
does today, done in Rust on the server, returning at most `width` bins for the
requested window. The view asks for the window it is about to draw instead of the
whole file.

`open.md` is explicit that this is **not** to be folded into the navigation work —
that was a redraw problem and this is a load-time one, "and conflating them is how a
measured decision turns back into a guess." Keep them separate in the code and in
the decision you write.

## Why now

It is the last named cost in a view that is otherwise finished, the fix is fully
specified in `open.md`, and it needs no board: a fixture capture exercises the whole
path. It also removes a live failure — the row cap only holds because the reference
study was two and a half minutes long, and a five-minute one overflows it.

## Scope warning

If it turns out the trace rows are served by `embarch-core` rather than by
`embarch-ui`, **stop and report that in this file** rather than reaching into
another repo (`../../embarch-fleet/protocol.md` §5 rule 2). A task that needs two
repos was mis-filed and is the supervisor's to re-scope.

## Done when

- [ ] A windowed, binned trace endpoint exists, with `from`, `to` and `width`, and
      returns at most `width` bins.
- [ ] The Trace view requests the window it draws rather than the whole capture.
- [ ] A test pins the binning against the browser-side aggregation it replaces, so
      the two produce the same picture for the same window.
- [ ] A decision entry recording the split from the navigation work and why.
- [ ] `spec.md`/`decisions.md`/`open.md` updated — the `open.md` bullet is answered
      or narrowed to whatever is genuinely left.
- [ ] `changelog.d/` fragment dropped; `status.d/` fragment for any suite-level fact
      this makes false; `features.d/ui-*` row if it is a new user-visible capability.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
