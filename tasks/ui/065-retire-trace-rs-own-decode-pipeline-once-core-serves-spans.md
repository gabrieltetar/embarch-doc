# 065 — Retire `trace.rs`'s own decode-to-lanes pipeline once `embarch-core` serves per-lane spans

**State:** blocked — **unparks when `tasks/core/076` lands.** Filed `open` by the `core/075` worker;
changed to `blocked` by leg 136 at filing time, because the drop's own body says *"do not start this
before that route exists and its shape is settled; the route name and payload shape are that task's
call, not this one's"* — and a task nothing can be done on is `blocked`, not `open`. Leaving it
`open` would put it in `queue-status.py`'s dispatchable count and send a worker to consume a route
that does not exist.
**Filed by:** leg 136, 2026-09-17, from
`inbox/ui-retire-trace-rs-decode-pipeline-once-core-serves-spans.md`, verbatim except for this
header. I re-checked the `Hardware: none` claim myself and it holds.
**Owner:** no
**Source:** `embarch-core` decision 64 (`embarch-core/decisions/stream-index.md`), from `tasks/core/075`,
which decided `embarch-core` will serve decoded per-lane spans on a new sibling route and filed the
build as `tasks/core/076`. `tasks/ui/064` (`embarch-ui` decision 27, `trace-view.md`) already records
that the split — `trace.rs` keeping its own row-decode/clock-health/stale-prefix/lane-building —
stays until `embarch-core` closes its side. This is that closing half, on the `embarch-ui` side.
**Filed to `inbox/` rather than `tasks/ui/` directly**, because a `core`-scoped worker cannot write
another sub-project's task queue (`check-ownership.py`).
**Scope:** ui
**Hardware:** none.

## What

Once `tasks/core/076` ships a route serving decoded `Lane`/`Span`/`Gap` (per `embarch-core` decision
64's shape — check `embarch-core/decisions/stream-index.md` and `interfaces/studies.md` for the
actual route name and response, decided in that task, not this one), `embarch-ui/src/trace.rs` can
retire its own row parsing, `dut_clock_health`, `stale_prefix_end`, the axis-tier choice, and
`Lane`/`Span`/`Gap` construction (all four exclusion flags), consuming `embarch-core`'s structure
instead. Keep only what stays chart-specific: windowed binning, `StepBand` projection, and
`TraceView`'s own fields (`embarch-ui` decision 18, preserved — unaffected by this move, since
decision 18 is scoped to what crosses to the browser, not to where the capture gets decoded before
that; `embarch-core` decision 64 and suite decision 4 both read it this way).

**Blocked on `tasks/core/076` landing first** — do not start this before that route exists and its
shape is settled; the route name and payload shape are that task's call, not this one's.

## Why now

`embarch-ui/open.md`'s bullet has said "closing it needs per-span data, or a decision it stays
split" since `ui/051` retired the aggregate. `tasks/core/075`/decision 64 made that decision: yes,
and `tasks/core/076` is building it. This is the other half.

## Done when

- [ ] `trace.rs` consumes `embarch-core`'s decoded per-lane spans instead of decoding the CSV itself.
- [ ] The retired row-decode/clock-health/stale-prefix/lane-building code is deleted, not left dead
      alongside the new call.
- [ ] `embarch-ui` decision 27 is updated to record the split closing (edit the body, per
      `DOC-PROTOCOL.md` — do not append a contradicting note beside the old text).
- [ ] `embarch-ui/open.md`'s bullet about needing per-span data or a decision is resolved.
- [ ] Gate green per `../../embarch-fleet/protocol.md` §10.
- [ ] `changelog.d/` fragment.

## Not yours

- Do not touch `embarch-core` — `tasks/core/076` owns the route's shape and implementation.
