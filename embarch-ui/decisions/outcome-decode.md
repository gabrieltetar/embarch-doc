# embarch-ui decisions: Decoding a step outcome

**Status:** active, 2026-09-02.

One decoder for a step's pass/fail/timed-out outcome, shared by the step
table and the trace chart's step row. Split out of
[trace-chart.md](trace-chart.md) on 2026-09-08 ([DOC-COMPACTION-PASS.md](../../DOC-COMPACTION-PASS.md)):
a distinct mission from that file's chart-navigation half of decision 10, moved
verbatim rather than squeezed.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 23 — One outcome decoder in `app.js`, not one per wire shape, and an unrecognised shape is drawn as visibly wrong rather than falling through

**One three-variant enum reaches `app.js` in two wire shapes, because it reaches one consumer through two routes.** `GET /study/{id}`'s `result` (and `events.json`, and the SSE `StepCompleted`) carry the **tagged** form `"Pass"` | `{"Fail":{"reason":…}}` | `"TimedOut"` — `embarch-study-designer`'s own `Outcome`. `GET /study/{id}/steps` carries a deliberately **flattened** one instead: a bare `"Pass"`/`"Fail"`/`"TimedOut"` string with `reason` beside it, so a caller drawing a band need not re-implement the enum's wire shape. That flattening is sound alone; what forces the duplication is the tagged form still reaching the *same* renderer through the other route.

**Kept the fork bounded to this repo rather than pushed onto the wire.** The alternative — one shape per concept, so `GET /study/{id}` also flattens — reaches into `embarch-core`, outside this sub-project, and the tagged shape is what `embarch-study-designer`'s own result type *is*: flattening it earlier would be re-deriving server-side truth for a client's convenience, the mistake decision 18 already exists to avoid the other way round. Two call sites and one shared decoder is a few dozen lines; renegotiating a wire contract elsewhere is not a call this repo gets to make.

**`decodeOutcome(outcome, reason)` is now the only place either shape is read.** It returns `{kind, reason}` with `kind` one of `"pass"`, `"fail"`, `"timedout"`, `"unknown"` — never derived by testing for one shape and falling back to the other on a miss, which is how the two decoders went silent on each other's input. `outcomeBadge` (step table) and `traceOutcomeColor` (trace chart's step row) both call it; neither re-parses `outcome` itself, and `reason` is the flattened shape's sibling field, ignored when the tagged shape's own `Fail.reason` is present.

**`kind: "unknown"` renders as wrong, not neutral, everywhere it can appear.** A bare `"Fail"` handed to the tagged-only decoder used to draw `badge-neutral "—"`; a tagged `Fail` handed to the flat-only decoder used to colour the trace band `var(--info)` and print `[object Object]`. Neither read as an error. Now: the step table draws a red `badge-danger "?"` reading *"unrecognised outcome"*, and the trace band keeps `traceOutcomeColor`'s red stroke but fills with `tr-cross`. Both are a visible failure of the *rendering*, not a third calm state beside pass and fail.

**Amended (`tasks/ui/015`): the trace band's first fill was `tr-gap`, and that was wrong.** `tr-gap` (decision 10, `trace-view.md`) is a report from the DUT's ring buffer — an interval the *firmware* said it lost records in — not a fact about what the client could render. An unparsed `Outcome` is a client-side fact with nothing to do with dropped hardware records; filling it with `tr-gap` made the view assert a hardware fault that never happened, distinguishable from a real one only by hovering. `tr-cross` was already the honest token for that, so the fix is a one-line swap, not a third hatch: the red stroke (still `traceOutcomeColor`'s danger colour) carries "this is wrong," and the fill carries the reason — both causes, and why they count as one, are named at decision 10 (chart half, [trace-chart.md](trace-chart.md)).
