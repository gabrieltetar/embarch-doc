# 076 — Serve decoded per-lane spans on a sibling route to `/load`

**State:** open
**Source:** `tasks/core/075` (`embarch-core` decision 64, `embarch-core/decisions/stream-index.md`)
decided this should ship, and filed the building as this task rather than doing it itself
(decision 64 is a decision, not an implementation).
**Scope:** core
**Hardware:** none.
**Owner:** no

## What

`GET /study/{id}/stream/{name}/load` (decision 62) serves only the reduced `LoadSummary`.
`outpost_load.rs` already builds the full timeline underneath it — `Lane`/`Span`/`Gap`, after row
decode, `dut_clock_health`, `stale_prefix_end` and the axis-tier choice — and then discards it once
`summarize` reduces it. `embarch-ui/src/trace.rs` rebuilds the identical timeline itself, because
nothing serves it. Add a sibling route (name and exact response shape are this task's call, e.g.
`/study/{id}/stream/{name}/load/spans`) that serves the decoded per-lane spans directly: make
`Lane`, `Span` and `Gap` (or a purpose-built wire type built from them) `Serialize`, wire a handler
in `study.rs` beside `stream_load_handler`, and document it in `embarch-core/interfaces/studies.md`
and `spec.md`.

**This is a wire-schema bump.** Per `../../embarch-fleet/ops.md` §4, the supervisor announces it
before it lands — do not skip that because the shape feels additive.

## Why now

`embarch-core` decision 64 decided to serve this rather than decline, reasoning that suite decision
4's own bought property — "exactly one implementation of that timeline exists in the suite" — is not
actually true while only the aggregate is shared. `embarch-ui` decision 27 records the split staying
open until this lands.

## Done when

- [ ] The new route serves decoded per-lane spans over HTTP, reusing `outpost_load.rs`'s existing
      decode rather than writing a second one.
- [ ] `embarch-core/interfaces/studies.md` and `spec.md` document the new route.
- [ ] `embarch-core/decisions/stream-index.md` gets the implementation decision (numbered), citing
      decision 64.
- [ ] A follow-up `embarch-ui` task (filed via `inbox/`, since it is outside this task's own repo)
      retires `trace.rs`'s row-decode/clock-health/stale-prefix/lane-building in favor of consuming
      this route. Not this task to file from scratch if `tasks/core/075` already dropped it —
      check `inbox/` and the `embarch-ui` queue first.
- [ ] Gate green per `../../embarch-fleet/protocol.md` §10.
- [ ] `changelog.d/` fragment. `status.d/` fragment if this makes any suite-level doc's description
      of `/load` stale.

## Not yours

- Do not change `embarch-ui` — file its retirement task, do not do the retirement here.
