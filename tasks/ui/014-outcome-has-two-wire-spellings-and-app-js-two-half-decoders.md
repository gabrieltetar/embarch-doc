# 014 — `Outcome` reaches `app.js` in two wire shapes from two routes of one service, and each of its two decoders is silent on the other's input

**State:** claimed
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

- [ ] One decoder in `app.js` handles a step outcome, whichever shape it arrived in.
- [ ] A `Fail` from either route renders as a failure, with its reason, in every place an outcome
      is shown.
- [ ] Neither decoder can silently render an unrecognised shape as a pass or a neutral.
- [ ] Gate green; `changelog.d/ui-*` fragment.
