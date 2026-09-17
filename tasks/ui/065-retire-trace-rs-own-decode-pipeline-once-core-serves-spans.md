# 065 — Retire `trace.rs`'s own decode-to-lanes pipeline once `embarch-core` serves per-lane spans

**State:** done — escape hatch taken, worker 2026-09-17. `embarch-core`'s `/load/spans` payload
does not carry everything `trace.rs` needs; see `## Escape hatch taken` below. No `embarch-ui` code
changed. `embarch-ui` decision 27 and `open.md` updated to record precisely what is missing;
core-side follow-up filed as `inbox/core-widen-spans-gap-and-consider-axis-diagnostics.md`, **drained
by leg 138 at this unit's fold into `tasks/core/085`**.
**Unparked by leg 137, 2026-09-17 14:20, because its condition is now met** — and `core/076` is
now fully landed and folded (leg 138, doc fold `9e36bf6`), so the route is on `main` in both repos
and nothing about it is still moving.

**Supervisor dispatch note 1 — the escape hatch below is real, and taking it is a success.** The
`## What` body already tells you to check first that the payload carries everything `trace.rs`
builds, and to say so rather than widen `embarch-core` if it does not. I am underlining it: **a unit
that reads both sides, finds a gap, documents precisely what is missing and files the `core`-side
follow-up to `inbox/` is a complete unit**, not a failed one. Do not half-retire the pipeline to
show progress, and do not reach into `embarch-core` under any circumstance.

**Supervisor dispatch note 2 — what actually landed, so you read the right thing.**
`GET /study/{id}/stream/{name}/load/spans` serves `SpansAnswer`
`{unit, t_from, t_to, records_lost, rows, rows_dropped_by_cap, row_cap, rows_unparsed, gaps, lanes}`.
`t_from`/`t_to` are absolute window bounds (`LoadSummary::window_extent` only ever carried their
difference). Reasoning is `embarch-core` decision 65 in `embarch-core/decisions/stream-index.md`;
the route is in `embarch-core/interfaces/studies.md` and `spec.md`. **Note that decision 65 has a
known precision defect under repair in parallel** (`tasks/core/080`, leg 138 unit 3): its CSV-size
extrapolation claims a direction of error it has not shown. That is prose about transfer cost only
— **it says nothing about the payload's shape**, which is what you depend on, so it does not block
you. Do not edit it.

**Supervisor dispatch note 3 — doc-size reserve for `ui`.** Nothing in `embarch-ui` is in the
reserve. The two closest: `embarch-ui/spec.md` **9,035/10,240 B (1,205 B left)** and
`embarch-ui/decisions/trace-view.md` **9,877/12,288 B (2,411 B left)** — decision 27 lives in the
latter and you have room to edit its body properly rather than squeezing. If your work pushes a
file into the reserve, file `tasks/ui/<NNN>-compact-ui.md` in the same commit.

**Previously, from leg 137:** unparked because its condition is met.
`tasks/core/076` landed (code `ef60321` in `embarch-core`, doc `e0d54e6`), so the route exists and
its shape is settled: **`GET /study/{id}/stream/{name}/load/spans`**, serving a `SpansAnswer` of
`{unit, t_from, t_to, records_lost, rows, rows_dropped_by_cap, row_cap, rows_unparsed, gaps, lanes}`
where `lanes` carries `Lane { key, label, unnamed, kind, spans }` and each `Span` is
`{from, to, open_start, open_end, crosses_gap, below_resolution}`. Reasoning recorded as
`embarch-core` decision 65 (`decisions/stream-index.md`). **Before you start, check that the payload
actually carries everything `trace.rs` builds** — `embarch-core`'s own `Lane` doc comment says the
label bookkeeping, point events and browser-search indices `embarch-ui`'s `Lane` carries alongside
these are chart concerns and **stay in `embarch-ui`**, so "retire the decode pipeline" is not the
same as "retire `Lane`". If something `trace.rs` needs is not served, say so rather than widening
`embarch-core` from here.

**Previously:** blocked — unparked when `tasks/core/076` lands. Filed `open` by the `core/075` worker;
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

- [ ] ~~`trace.rs` consumes `embarch-core`'s decoded per-lane spans instead of decoding the CSV
      itself.~~ Not done — see `## Escape hatch taken`.
- [ ] ~~The retired row-decode/clock-health/stale-prefix/lane-building code is deleted, not left
      dead alongside the new call.~~ Not done, for the same reason: nothing was safe to delete.
- [x] `embarch-ui` decision 27 is updated (`decisions/trace-view.md`) — not to record the split
      closing, since it did not, but to record precisely why not, in place of the old open question.
- [x] `embarch-ui/open.md`'s bullet is resolved from a vague wait into a precise, checked blocker.
- [x] Gate green per `../../embarch-fleet/protocol.md` §10 (`embarch-ui` code untouched; docs gate
      run in the doc worktree).
- [x] `changelog.d/ui-trace-spans-gap-checked-not-closable-yet.decided.md`.

## Escape hatch taken

Checked `embarch-core`'s `GET .../load/spans` payload (decisions 64/65, `tasks/core/076`) against
every field `trace.rs` builds, before touching any code, per this task's own instruction. It falls
short three ways, none of them a build mistake on `core`'s side:

1. **`Gap` is `{from, to}` only.** `trace.rs`'s own `Gap` also carries `records_lost`, `row_index`
   and `unbounded_start`, all three rendered today in `app.js`'s gap table (~3860-3861, ~4250-4252).
   Swapping to Core's shape as it stands would delete columns a reader currently sees.
2. **None of the axis-health diagnostics are served** — `frames`, `resolution_ms`, `dual_clock`,
   `unstamped_rows`, `undated_rows`, `dut_backsteps`, `dut_backstep_max_us`, `dut_step_max_us`,
   `dut_clock_refused`, `stale_prefix_rows`, `stale_prefix_step_us`, `out_of_order_rows` — every one
   rendered today in `app.js`'s clock-health notes (~3780-3848). Decisions 62/64 scope these out by
   name as chart geometry / `TraceView`'s own shape, so this is a documented boundary, not a gap to
   quietly widen.
3. **Point events are excluded by the same decisions**, and in `trace.rs` are built in the same
   row-iteration pass as `Lane`/`Span`/`Gap`. As long as they stay excluded, `embarch-ui` must keep
   decoding the raw CSV row-by-row regardless — so `dut_clock_health`, `stale_prefix_end` and the
   row decode itself cannot be deleted even after fixing (1), unless point events are served too.

A partial swap (`Lane`/`Span`/`Gap` only, keeping row-decode for markers/diagnostics) was
considered and rejected: it would either regress the gap table (missing columns) or add a second
source of the same facts beside code that has to stay regardless — not a retirement, and explicitly
what this task's dispatch note says not to do. No `embarch-ui` code was changed.

Follow-up filed to `/home/gabriel/Github/embarch/embarch-doc/inbox/core-widen-spans-gap-and-consider-axis-diagnostics.md`
(scope `core`): widen `Gap`'s three missing fields (mechanical), and decide whether the axis-health
diagnostics/point events are ever in `embarch-core`'s scope to serve, or whether decision 27's split
is permanent.

## Not yours

- Do not touch `embarch-core` — `tasks/core/076` owns the route's shape and implementation.
