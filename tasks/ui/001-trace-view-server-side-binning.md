# 001 — The Trace view's remaining cost is a 13 MB JSON the browser waits for; bin it server-side

**State:** done — agent/ui/001-trace-view-server-side-binning, 2026-09-04. Gate 7 of 8; the eighth is a mechanism defect, not this work, and is **not** a `blocked` — see below.

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

- [x] A windowed, binned trace endpoint exists, with `from`, `to` and `width`, and
      returns at most `width` bins. `GET /api/trace/{study}/{tap}/bins`; the cap is
      a property (runs are disjoint stretches of the grid), pinned by
      `a_lane_never_returns_more_runs_than_bins_asked_for`.
- [x] The Trace view requests the window it draws rather than the whole capture.
      `Lane.spans` is no longer serialized at all; `span_count` replaces the two
      places `app.js` counted them.
- [x] A test pins the binning against the browser-side aggregation it replaces, so
      the two produce the same picture for the same window. The shipped
      `traceAggregateLane` is kept in `mod browser_reference`, deliberately in its
      naive shape, and `bins_match_the_browser_aggregation_they_replace` runs the
      two against each other over three captures × 40 windows × 4 grid widths.
- [x] A decision entry recording the split from the navigation work and why.
      **A new file rather than a section of `decisions/trace-chart.md`** —
      `embarch-ui/decisions/trace-transfer.md`, decision 18 — because putting a
      load-time decision inside the navigation decision's file is the conflation
      `open.md` warned about, in the docs instead of the code.
- [x] `spec.md`/`decisions.md`/`open.md` updated. The `open.md` bullet is
      **narrowed, not closed**: the transfer is fixed, and the 250,000-row cap is
      now the only term left — with the reason it was set (the browser holding
      112,801 spans) gone, and the remaining reason (server decode) measured only
      at 225,627 rows.
- [x] `changelog.d/ui-trace-windowed-bins.added.md`; `features.d/ui-100-…` updated
      from `Todo — sized, not built` to `Shipped`. **No `status.d/` fragment:**
      nothing in `embarch.md`, `suite/roadmap.md`, the glossary, the user guide or
      the reversals index asserts anything this makes false — `embarch.md` §3's
      `embarch-ui` row says "six tabs live against the real deployed Core", which
      is still true, and the only suite-level mention was the `suite/features.md`
      row, which is assembled from the fragment above.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10). **7 of 8, and the eighth
      is red by construction — see below.**

## The eighth check cannot go green from a worker branch

`scripts/check-docs.py` runs `build_features.py --check`, which fails whenever
`suite/features.md` does not match `features.d/`. `check-ownership.py --scope ui`
refuses `suite/features.md` outright — "is, and stays, outside every worker's
row", in its own words. So the two checks are each individually correct and
**jointly unsatisfiable** for any unit that ships a capability: writing the
`features.d/` row is what the worker is asked to do, and it is what turns the
gate red.

Everything else is green:

    embarch-ui:   cargo build · cargo test (95 passed, 2 ignored) ·
                  cargo clippy --all-targets -D warnings
    embarch-doc:  check-links · check-staleness · check-decision-refs ·
                  check-doc-conventions · check-doc-size · build_changelog --check ·
                  install.py --check
    ownership:    --scope ui clean on the doc branch's own diff;
                  --code-repo clean

`suite/features.md` is left unassembled deliberately. Running
`scripts/build_features.py` makes the eighth check pass and is a one-line fix
at fold time; committing its output from here would be the ownership violation
the check exists to catch. Dropped in `inbox/` as
`doc-features-assembly-makes-every-worker-branch-red.md` — this is the first
unit to write a `features.d/` fragment since the mechanism landed, so it will
now happen to every unit that ships one.

## Hardware-verification debt

**None of this ran against a live Core or a real DUT capture, and it should
before the row's `Verified` column is raised past `local`.** What did run,
host-side: the release binary against a stub Core serving a synthetic capture
built to the reference's shape (225,627 rows / 112,804 spans / 26 lanes), driven
in headless Firefox with real wheel-zoom and double-click-to-fit. What is owed
is one sitting on the owner's own machine: deploy the UI, open the Trace tab on
a real recorded study's outpost tap, and confirm the first paint, a wheel zoom
and a drag pan against a capture Core rendered rather than one this task
generated. The numbers in decision 18 are the synthetic capture's, and they are
labelled as such.
