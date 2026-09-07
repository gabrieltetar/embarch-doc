# 014 — `Outcome` reaches `app.js` in two wire shapes from two routes of one service, and each of its two decoders is silent on the other's input

**State:** done
**Source:** suite review pass 2026-09-06, dimension 5 (cross-surface consistency). Code-confirmed.
**Scope:** ui
**Hardware:** none
**Owner:** no

## What

One three-variant enum, two wire shapes:

- **Tagged**, inside `events.json`, `GET /study/{id}`'s `result`, and the SSE `StepCompleted`:
  `"Pass"` | `{"Fail":{"reason":…}}` | `"TimedOut"` — `embarch-study-designer/src/result.rs`'s
  `Outcome`, no `rename_all`.
- **Flattened**, on `GET /study/{id}/steps`: `embarch-core/src/study.rs:2795-2797`,
  `pub outcome: String` + `pub reason: Option<String>`, documented at
  `embarch-core/interfaces.md:49` as *"a bare `"Pass"`/`"Fail"`/`"TimedOut"` with `reason` beside
  it, not `Outcome`'s tagged JSON"*.

`app.js` carries a decoder for each and neither degrades loudly on the other's input:

- `app.js:2310-2316`, `outcomeBadge` — **tagged**:
  `if (outcome === "Pass") … if (outcome && outcome.Fail) { … outcome.Fail.reason … }` then
  `return badge-neutral "—"`. Hand it a bare `"Fail"` and it renders a neutral dash.
- `app.js:4041-4046`, `traceOutcomeColor` — **bare**:
  `if (outcome === "Fail") return "var(--danger)"; … return "var(--info)"`, and `:4353-4355`
  renders `b.outcome` straight into text. Hand it a tagged `Fail` and it colours the band
  `var(--info)` while the tooltip prints `[object Object]`.

The flattening itself is deliberate and argued (`embarch-core/src/study.rs:2782-2787`: a caller
drawing a band should not re-implement the enum's wire shape). What is unargued is that the tagged
form still reaches the **same consumer** through `GET /study/{id}`, which is what forces the
duplication.

Candidate direction: one shared decoder in `app.js` that accepts either shape and renders a
failure as a failure in both — the bounded fix, entirely in this repo. If the right answer is
instead one shape per concept on the wire, that crosses into `embarch-core` and belongs back in
`inbox/` as `Scope: suite`.

## Why now

Both decoders are correct for their own feed, so nothing catches the cross: the failure mode of
each on the other's input is a neutral badge and a blue band, not an error. A step that failed can
render as a step that did not, in the surface an engineer is looking at to find out whether it did.
None of `tasks/ui/003` through `ui/013` touches outcome decoding.

## Done when

- [x] One decoder in `app.js` handles a step outcome, whichever shape it arrived in.
- [x] A `Fail` from either route renders as a failure, with its reason, in every place an outcome
      is shown.
- [x] Neither decoder can silently render an unrecognised shape as a pass or a neutral.
- [x] Gate green; `changelog.d/ui-*` fragment.

## Resolution

**Fork taken: one shared decoder in `app.js`, bounded to this repo.** `embarch-core`'s flattening
(`GET /study/{id}/steps`) is sound on its own — a caller drawing a band should not re-implement
the enum's wire shape — and the tagged form is what `embarch-study-designer`'s own `Outcome` *is*.
Neither side should change; the duplication was purely a client-side gap. See `embarch-ui`
decision 23 (`decisions/trace-chart.md`) for the full argument.

`decodeOutcome(outcome, reason)` is now the only place either shape is read, returning
`{kind, reason}` with `kind` one of `pass`/`fail`/`timedout`/`unknown`. Both `outcomeBadge` (step
table) and `traceOutcomeColor` (trace chart's step row) call it instead of re-parsing `outcome`
themselves.

An unrecognised shape (`kind: "unknown"`) is drawn as visibly wrong, not neutral: the step table
shows a red `badge-danger "?"` reading "unrecognised outcome" (previously a neutral `—` dash), and
the trace band keeps the danger-red stroke but fills with the `tr-gap` hatch pattern already used
for a dropped-record gap — a span this view cannot vouch for — instead of a solid fill or the old
`var(--info)` blue.

Gate: `cargo build`, `cargo test` (101 passed, 2 pre-existing ignored), and
`cargo clippy --all-targets -- -D warnings` all clean in `embarch-ui`. No JS lint/test harness
exists for `app.js` beyond `embarch-ui/src/trace.rs`'s `dump_a_view_for_the_browser_harness`,
which is `#[ignore]`d and manual (no `node` on this machine; it drives headless Firefox by hand) —
not run as part of this gate.
