# 075 — Decide whether `/load` serves decoded per-lane spans, or record why it will not

**State:** open
**Filed by:** leg 135, from `inbox/core-outpost-load-per-span-endpoint.md`, written by the `ui/064`
worker while landing that unit. Filed verbatim below except for this header and the two supervisor
notes. I re-checked the `Hardware: none` claim myself and it holds: deciding this is a read of
`outpost_load.rs`, `trace.rs`, the `/load` handler and four decisions — no board, no probe, no live
Core.
**Source:** `tasks/ui/064` (merge `b0fc860`), which settled the `embarch-ui` side as
**`embarch-ui` decision 27** — the split stays until `embarch-core` serves per-lane spans — and
explicitly declined to assert what `embarch-core` should do.
**Scope:** core
**Hardware:** none.
**Owner:** no

**Doc-size reserve for `core`:** `embarch-core/decisions/auth.md` is **11,356/12,288 B (932 B
left)**, filed as `tasks/core/046` and blocked — **do not write into it.** Nothing else of core's is
in reserve. Run `python3 scripts/check-doc-size.py --pressure` before and after.

**Supervisor note 1 — "declines and records why" is a first-class outcome here, not a consolation.**
The filer says so itself, and it is the cheaper answer: `embarch-ui` has already recorded decision
27 accepting the split, so a `no` costs a decision entry in `embarch-core` and closes the question
for both repos. A `yes` is a **wire change** with consumers, and see note 2.

**Supervisor note 2 — deciding is in scope; shipping the endpoint is not, in this unit.** Serving a
new structure on `/load` or a sibling route changes a wire surface that `embarch-api`, `embarch-ui`
and the user guide read. A worker may **write the decision** recording which way it goes and why;
it may **not** implement the route. If the decision is to build it, file the implementation as a
separate task and say so — the supervisor announces a wire-schema bump before it lands
(`../../embarch-fleet/ops.md` §4).

**Supervisor note 3 — verify `embarch-ui`'s premise before building on it.** This drop and decision
27 both rest on the claim that `embarch-ui` decision 18 keeps decoded spans off the *browser* but
not off the Core-to-`embarch-ui` call. That reading is `ui/064`'s, made from `embarch-ui`'s side.
**Read decision 18 yourself.** If it is wider than that, this task's premise fails and saying so is
the right outcome.

---

## What

`embarch-core/src/outpost_load.rs` and `embarch-ui/src/trace.rs` each independently decode a
rendered `*.trace.csv` into the same `Lane`/`Span`/`Gap` shapes — row parsing, `dut_clock_health`,
`stale_prefix_end`, the axis-tier decision, and the four exclusion flags (`open_start`, `open_end`,
`crosses_gap`, `below_resolution`). `outpost_load.rs`'s own comments say several of these functions
are "ported verbatim" from `trace.rs`. `embarch-core` decision 62 / suite decision 4 moved only the
*aggregate* (`LoadSummary`) off `embarch-ui`; the per-lane spans `embarch-ui` needs for its chart
(windowed binning, `embarch-ui` decision 18) are not served, so `embarch-ui` has to keep its own
copy of the whole decode pipeline to get them — not just the `Lane`/`Span`/`Gap` types and the four
flags, the row decode and clock-health/stale-prefix search too.

If `embarch-core` served the decoded per-lane spans it already builds internally (before reducing
them to `LoadSummary`) — on `/study/{id}/stream/{name}/load` or a sibling call — `embarch-ui` could
consume that structure directly and retire its own row-decode/clock-health/stale-prefix/
lane-building code, keeping only the chart-specific work (windowed binning, `StepBand` projection,
`TraceView`'s own fields). This would not conflict with `embarch-ui` decision 18, which keeps
decoded spans off the *browser* wire, not off the Core-to-`embarch-ui` call — `embarch-ui` already
fetches the full rendered CSV from Core over HTTP today (`state.core.get_study_stream` in
`embarch-ui/src/main.rs`), so this would not be a new category of transfer, just a different shape
for one that already happens.

## Why now

`embarch-ui/open.md`'s bullet has said "closing it needs per-span data, or a decision it stays
split" since `ui/051` retired the aggregate, and nobody had evaluated which. `embarch-ui` task 064
did: the duplication is wider than the bullet said, and the per-span shape that would close it is
nameable and does not appear to conflict with anything already decided on either side. `embarch-ui`
recorded decision 27 accepting the split until this closes, because the choice of whether to build
it is `embarch-core`'s to make, not `embarch-ui`'s to assert.

## Done when

- [ ] `embarch-core` decides whether to serve decoded per-lane spans (what shape, on the existing
      `/load` response or a sibling call), or declines and records why — a cost this note did not
      account for, most plausibly. **Either way it is a numbered decision in `embarch-core`**, citing
      decision 62 and `embarch-ui` decision 27.
- [ ] Supervisor note 3's check on `embarch-ui` decision 18 answered explicitly, from decision 18's
      own text.
- [ ] If it ships, a follow-up `embarch-ui` task retires `trace.rs`'s own row-decode/clock-health/
      stale-prefix/lane-building in favor of consuming `embarch-core`'s structure. **Not this
      task** — file it, do not do it.
- [ ] A `changelog.d/` fragment.
- [ ] Gate green per `../../embarch-fleet/protocol.md` §10.

## Not yours

- **Do not implement the endpoint** (supervisor note 2).
- **Do not change `embarch-ui`** — decision 27 is `ui/064`'s and stands until this task closes.
- **Do not touch `embarch-core/decisions/auth.md`** — in reserve, parked under `tasks/core/046`.
