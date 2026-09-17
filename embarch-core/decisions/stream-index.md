# embarch-core decisions: The stream index

**Status:** active, 2026-09-17.

What `GET /study/{id}/streams` and its siblings report about a tap once it exists: a computed load
answer alongside the byte route, and a tap declared against hardware this bench has no front end for.
Split out of [streams.md](streams.md) on 2026-09-16 (`tasks/core/060`) — capturing and rendering a tap
is one mission, reporting on it to a caller is another. What Core captures and refuses to render in the
first place is [streams.md](streams.md).

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).


## The stream index

### 62 — `GET /study/{id}/stream/{name}/load` answers the outpost's own load repartition, alongside the byte route rather than replacing it
[Suite decision 4](../../suite/decisions.md) named `embarch-core` as the one place an outpost capture's per-subject load shares and coverage line are computed — Core is the only component on both the agent's and human's paths, and the only one in the release archive.

**A sibling of `/stream/{name}`, not a query flag.** `?raw=1` already picks between two *files* for one encoding; the load answer is a computed result over the rendered one, so it gets its own path segment (`outpost_load.rs`, `study.rs`'s `stream_load_handler`) rather than a second, unrelated meaning on the same query string.

**Scoped to `StreamEncoding::OutpostTrace`, by the tap the byte route already resolves.** A mismatched tap is a `400` naming its real encoding, not an agent guessing why the numbers came back empty. An unrendered tap is a `404` carrying `GET /study/{id}/streams`'s own reason — no second explanation for the same fact.

**Reads only the rendered CSV, never the raw frames or manifest.** Core already owns the one decode (`outpost_manifest.rs`) and refuses a `record_layout_version` mismatch there. `outpost_load.rs` inherits `embarch-ui` decision 10 (trace)'s pin verbatim: the column list is checked against `embarch_study_designer::outpost::csv_header()`, `422` if it differs — kept with the computation rather than loosened, per [reversals row 86](../../reversals/rows-73-92.md): a wire change moving a column is exactly the drift two independent hosts can each get wrong differently.

**A second implementation of the timeline, not a second decoder — decisions 64/66 are what that duplication resolves to.** The alternative, a shared host-side analysis crate for Core and the UI, was rejected on cost, not principle (suite decision 4).

**Excluded as chart geometry, not part of the answer:** windowed binning, the study-step row, `embarch-ui`'s `TraceView` payload shape (that file's decision 18, preserved).

### 63 — A tap declared against a source this bench has no front end for says so as a fourth boolean, not a third meaning for `note`
`embarch-dev-bench` accepts a `StreamSource::PowerFrontEnd` tap and captures nothing ([its decision 24](../../embarch-dev-bench/decisions.md) defers the front end). Its only signal, `bytes_written: 0`, is what `list_study_streams` already defines as "declared and produced nothing" — so asking for hardware that does not exist and mis-naming a signal read identically. Said on `GET /study/{id}/streams`.

**Neither alternative survives.** `embarch-api`'s `study_power_data` alias is gone, not weakened — retired with the other fixed-channel aliases. A submit-time refusal would change study submit behaviour for a capability the roadmap calls *deferred, not cancelled* — a study against it today is not a mistake.

**A fourth `#[serde(default)] Option<bool>` on `StudyStreamEntry`**, in the `named`/`timed`/`self_excluded` pattern (`None` = a Core predating it); `note` keeps the prose. Not `note` alone: `is_named`'s doc comment already records that field's conjunction breaking once a trace gained a second way to be incomplete — a third meaning would repeat that defect on a field documented as prose, never branched on.

**Stated, not measured** — citing `embarch-dev-bench` decision 24. No tap's capture changes.

### 64 — `embarch-core` will serve the decoded per-lane spans decision 62 stopped short of, on a new sibling route; that this task decides, a follow-up builds
Decision 62 moved only the *aggregate* (`LoadSummary`). `outpost_load.rs` and `embarch-ui/src/trace.rs` each still independently build the full timeline beneath it — row decode, `dut_clock_health`, `stale_prefix_end`, the axis-tier choice, `Lane`/`Span`/`Gap` construction — `outpost_load.rs`'s own comments call several of these "ported verbatim" from `trace.rs`. `embarch-ui` decision 27 (`trace-view.md`) records that split staying until `embarch-core` closes it. `tasks/core/075` asked whether to.

**Decision 18 does not stand in the way, read on its own text.** [`embarch-ui` decision 18](../../embarch-ui/decisions/trace-transfer.md) decides where *binning* runs and what crosses to the *browser*, not which server holds the decoded capture — [suite decision 4](../../suite/decisions.md) already read it the same way: *"What changes is which server holds the decoded view. The browser's contract is untouched."*

**The call: yes, serve them.** Three reasons: **(1)** not a new transfer category — `embarch-ui`'s server already fetches the full rendered CSV over HTTP to decode itself, and decision 18's 12.6 MB reference figure is the same order of magnitude. **(2)** suite decision 4's bought property — *"exactly one implementation of that timeline exists in the suite"* — was not yet true: `LoadSummary` was one implementation, the timeline it reduces from was still two. **(3)** decision 62 already named this duplication "known to be temporary... until the queued follow-up." Chart geometry (binning, the study-step row, `TraceView`'s shape) stays excluded, unchanged.

**Nothing here ships the route** — the shape (a sibling of `/load` serving `Lane`/`Span`/`Gap`, made `Serialize`) is settled by the implementing task, filed as `tasks/core/076`. The matching `embarch-ui` follow-up is outside this repo's ownership row, dropped to `inbox/`.

**Corrected 2026-09-17 (`tasks/core/085`), reasoning in decision 66.** This entry's closing sentence originally read *"Serving spans is what closes the gap decision 4 opened and decision 62 left standing."* `tasks/ui/065` checked `/load/spans`'s served payload against `trace.rs` field-for-field and found it does not: both files still independently decode the CSV, because axis-health diagnostics and point events are excluded from this route and always will be (decision 66). Suite decision 4's *"exactly one implementation"* property is **not closed by this route and cannot be** — decision 66 is the record of why that is now a permanent, checked fact rather than a gap still closing.

### 65 — `GET /study/{id}/stream/{name}/load/spans` serves decision 64's spans; the CSV half of its size argument is now measured, and holds
Built by `tasks/core/076`. Additive: `/load` unchanged, still exactly `LoadSummary`.

**Shape.** `Lane`/`Span`/`Gap` are `pub`+`Serialize`. Response is `SpansAnswer`: `{unit, t_from, t_to, records_lost, rows, rows_dropped_by_cap, row_cap, rows_unparsed, gaps: [Gap], lanes: [Lane]}`. `t_from`/`t_to` are the window's absolute bounds — `LoadSummary::window_extent` only ever carried their difference.

**One decode, two reductions.** The CSV-to-timeline body is a private `decode_with_cap`; `summarize` reduces its `Decoded` to `LoadSummary`, a new `spans_answer` reduces the same `Decoded` to `SpansAnswer` — no further computation. `study.rs`'s two handlers share one tap-resolution helper and differ only in which function gets the CSV.

**The CSV half, measured.** No reference-shaped CSV (225,627 rows/112,804 spans/26 lanes, decision 18's 12.6 MB figure) exists to re-measure. Measurable instead: `embarch-core`'s own real-firmware fixture renders to **43,573 B / 831 rows — 52.367 B/row** [measured 2026-09-17]. Extrapolated to 225,627 rows: **≈11.8 MB** — order-of-magnitude only, direction of error not established: `rx_utc_ms` is empty throughout, row width spans 22–67 B within the fixture itself (~3x, 51.4 B mean), and the fixture's 4-lane/7-name profile is structurally unlike the reference's 26-lane/112,804-span one. **Holds: same order of magnitude as 12.6 MB regardless** — decision 64 stands; no response-shape change follows.

### 66 — `Gap` widens to full parity with `trace.rs`'s own shape; the axis-health diagnostics and point events decision 62 called chart geometry stay out, permanently
`tasks/core/085`, from `tasks/ui/065`'s field-for-field check of decision 65's payload against `trace.rs`'s own `Lane`/`Span`/`Gap`/`TraceView`.

**`Gap` widens.** `{from, to}` becomes `{from, to, records_lost, cycle_span, frame_index, row_index, unbounded_start}` — the same seven fields `trace.rs`'s own `Gap` carries, computed off the same `Row.a`/`Row.b`/`Row.frame_index` already read at the call site and the same per-frame `unbounded_start` rule already used for `from`/`to`. Mechanical: no new bookkeeping, matching Rust types (`u32`/`u32`/`u64`/`usize`/`bool`), so a caller merging both shapes never re-derives one.

**Axis-health diagnostics and point events stay out, permanently, not pending.** Two reasons:
- **Already scoped out by name.** `frames`, `resolution_ms`, `dual_clock`, `unstamped_rows`, `undated_rows`, `dut_backsteps`, `dut_backstep_max_us`, `dut_step_max_us`, `dut_clock_refused`, `stale_prefix_rows`, `stale_prefix_step_us`, `out_of_order_rows` are all fields of `trace.rs`'s own `TraceView` struct — decision 62's exclusion of "`embarch-ui`'s `TraceView` payload shape" already names this exact set. Point events are excluded the same way `outpost_load.rs`'s own `Lane` doc comment already states: they and the browser-search indices `trace.rs`'s `Lane` carries "are chart concerns and stay there."
- **Serving them would not close anything.** `tasks/ui/065` found that even the widened `Gap` above lets `embarch-ui` delete nothing: point events are built in `trace.rs`'s same row-iteration pass as `Lane`/`Span`/`Gap`, so as long as they stay excluded the row decode, `dut_clock_health` and `stale_prefix_end` all stay too. Serving the diagnostics alone would add a second source of the same facts beside code that has to stay regardless, not retire it — the partial swap `tasks/ui/065` considered and rejected.

**So `embarch-ui` decision 27's split is not waiting on `embarch-core` — it is permanent**, and decision 64's closing sentence above is corrected to match. `tasks/ui/067` closes `embarch-ui/open.md`'s bullet on that basis.

---
