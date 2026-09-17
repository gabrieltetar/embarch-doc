# embarch-core decisions: The stream index

**Status:** active, 2026-09-16.

What `GET /study/{id}/streams` and its siblings report about a tap once it exists: a computed load
answer alongside the byte route, and a tap declared against hardware this bench has no front end for.
Split out of [streams.md](streams.md) on 2026-09-16 (`tasks/core/060`) — capturing and rendering a tap
is one mission, reporting on it to a caller is another. What Core captures and refuses to render in the
first place is [streams.md](streams.md).

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).


## The stream index

### 62 — `GET /study/{id}/stream/{name}/load` answers the outpost's own load repartition, alongside the byte route rather than replacing it
[Suite decision 4](../../suite/decisions.md) named `embarch-core` as the one place an outpost capture's per-subject load shares and its coverage line are computed, because Core is the only component on both the agent's path and the human's, and the only one in the release archive. This is that route's shape.

**A sibling of `/stream/{name}`, not a query flag on it.** `?raw=1` on the existing route already picks between two *files* for the same encoding; the load answer is not a third file, it is a computed result over the rendered one, so it gets its own path segment (`outpost_load.rs`, `study.rs`'s `stream_load_handler`) rather than overloading a query string with a second, unrelated meaning.

**Scoped to `StreamEncoding::OutpostTrace` and refused otherwise, by the same tap the byte route already resolves.** There is no timeline to repartition in a `Samples`/`GattTranscript`/`Raw`/`Text` capture, so a mismatched tap is a `400` naming its real encoding rather than an agent guessing why the numbers came back empty or zero. A tap that has not rendered — no manifest applied yet, or the render failed — is a `404` carrying the same reason `GET /study/{id}/streams`'s own `note` already gives; this route invents no second explanation for the same fact.

**Consumes the rendered CSV; does not touch the raw frames or the manifest.** Core already owns the one decode of the wire (`outpost_manifest.rs`) and already refuses to render a manifest whose `record_layout_version` disagrees with the shared crate's. `outpost_load.rs` reads only the `*.trace.csv` that decode produced, and inherits [`embarch-ui` decision 10 (trace)](../../embarch-ui/decisions/trace-view.md)'s pin verbatim: the column list is checked against `embarch_study_designer::outpost::csv_header()` and refused (`422`) if it differs. [Reversals row 86](../../reversals/rows-73-92.md) is why that check moves with the computation rather than being loosened: a wire change that moves a column is exactly the drift two independent hosts can each get wrong differently, and a host that inherited the arithmetic without the pin would be the same failure with a new address.

**A second implementation, not a second decoder — and known to be temporary.** `embarch-ui/src/trace.rs` keeps computing the same timeline for its own chart until the queued follow-up makes it read this answer instead; until then a change to `RecordKind`, a gap record's semantics, or the five-lies exclusion rules has to land in both files. Suite decision 4 accepts this as a priced, decision-pointed cost — the alternative, a shared host-side analysis crate both Core and the UI depend on, was considered and rejected on cost rather than principle.

**What this route does not carry, because it is chart geometry rather than part of the answer:** windowed binning, the study-step row, and anything of `embarch-ui`'s `TraceView` payload shape (that file's own decision 18, preserved). An agent wanting those still has no route to them, which is unchanged by this one.

### 63 — A tap declared against a source this bench has no front end for says so in the stream index, as a fourth boolean and not a third meaning for `note`
`embarch-dev-bench` accepts a `StreamSource::PowerFrontEnd` tap and captures nothing, because [its decision 24](../../embarch-dev-bench/decisions.md) defers the front end. The tap's only signal is `bytes_written: 0`, which `list_study_streams` defines as *"a tap that was declared and produced nothing"* — an **authoring** outcome. So asking for hardware that does not exist and mis-naming a signal produce identical evidence. `GET /study/{id}/streams` is where that is said: the surface the guide already sends a reader to first.

**Neither alternative survives.** A sentence in `embarch-api`'s `study_power_data` description is not weak, it is **gone** — that alias was retired with the other fixed-channel aliases. A **submit-time refusal** changes study submit behaviour, which no unattended session makes, and the roadmap calls power sampling *deferred, not cancelled*: a study written today against a tap the firmware will support later is not a mistake to reject. Acceptance stays.

**A fourth `#[serde(default)] Option<bool>` on `StudyStreamEntry`**, in the `named`/`timed`/`self_excluded` pattern, `None` meaning a Core predating it; `note` keeps the prose. **Not `note` alone, and the struct's own history is why.** `is_named`'s doc comment records that the old conjunction *"was correct while `note` could only ever mean 'unnamed'. It stopped being correct when a trace gained a second way to be incomplete"* — a third meaning for that field is the same defect one generation on, against a field documented as prose to be read and never branched on.

**Core states this, it does not measure it**, citing `embarch-dev-bench` decision 24 where it sets the flag. No tap's capture changes.

### 64 — `embarch-core` will serve the decoded per-lane spans decision 62 stopped short of, on a new sibling route; that this task decides, a follow-up builds
Decision 62 moved only the *aggregate* (`LoadSummary`) off `embarch-ui`. `outpost_load.rs` and `embarch-ui/src/trace.rs` each still independently build the full timeline underneath it — row decode, `dut_clock_health`, `stale_prefix_end`, the axis-tier choice, and `Lane`/`Span`/`Gap` construction with its four exclusion flags — `outpost_load.rs`'s own comments call several of these functions "ported verbatim" from `trace.rs`. `embarch-ui` decision 27 (`trace-view.md`) records that split staying until `embarch-core` closes it. `tasks/core/075` asked whether to.

**Decision 18 does not stand in the way, read on its own text.** [`embarch-ui` decision 18](../../embarch-ui/decisions/trace-transfer.md) decides where *binning* runs and what crosses to the *browser* — `GET /api/trace/{study}/{tap}/bins`'s payload, "the view's own payload drops `lanes[].spans` entirely." It never mentions which server holds the decoded capture that gets binned; "one decoded capture is cached server-side" names a fact about the browser leg, not a constraint on the Core-to-`embarch-ui`-server leg. [Suite decision 4](../../suite/decisions.md) already read it the same way and said so directly: *"What changes is which server holds the decoded view. The browser's contract is untouched."* So `embarch-ui` decision 27's premise — that decision 18 keeps decoded spans off the browser, not off the Core call — holds; it is not wider than that.

**The call: yes, serve them.** Three reasons, not one:
- **Not a new category of transfer.** `embarch-ui`'s server already fetches the full rendered CSV from `embarch-core` over HTTP to do its own decode (`state.core.get_study_stream`). Decision 18 measured a reference capture's decoded spans at 12.6 MB serialized — the same order of magnitude as the CSV that already crosses this same call today, not a new size class introduced by this move.
- **Suite decision 4's own stated property isn't actually true yet.** It bought *"an agent can obtain [the load answer] without re-implementing the timeline, and exactly one implementation of that timeline exists in the suite."* `LoadSummary` is one implementation; the timeline it is reduced from is still two, by `outpost_load.rs`'s own admission. `tasks/ui/064` found this duplication wider than `embarch-ui/open.md`'s bullet said. Serving spans is what closes the gap decision 4 opened and decision 62 left standing.
- **Decision 62 already named this as coming.** Its own text calls the duplication "known to be temporary... until the queued follow-up makes it read this answer instead." This decision is that follow-up answering whether, not a reopening of 62's own scope — chart geometry (binning, the study-step row, `TraceView`'s shape) stays excluded, unchanged.

**Nothing here ships the route.** Per `tasks/core/075`'s supervisor note 2, deciding is this task's job; building is not. The shape: a sibling of `/load` (name and exact response settled by the implementing task, not this one) serving `Lane`/`Span`/`Gap` — made `Serialize` — that `outpost_load.rs` already builds internally before reducing them to `LoadSummary`. Filed as `tasks/core/076`. It is a wire-schema bump: the supervisor announces it before it lands (`../../embarch-fleet/ops.md` §4). The matching `embarch-ui` follow-up — retiring `trace.rs`'s own row-decode/clock-health/stale-prefix/lane-building once it can consume this instead — is outside this repo's ownership row and is dropped to `inbox/`, not filed here.

### 65 — `GET /study/{id}/stream/{name}/load/spans` serves decision 64's spans; the CSV half of its size argument is now measured, and holds
Built by `tasks/core/076`. Additive: `/load` unchanged, still exactly `LoadSummary`.

**Shape.** `Lane`/`Span`/`Gap` are now `pub`+`Serialize` (were private). Response is `SpansAnswer`: `{unit, t_from, t_to, records_lost, rows, rows_dropped_by_cap, row_cap, rows_unparsed, gaps: [Gap], lanes: [Lane]}`. `t_from`/`t_to` are the window's absolute bounds — `LoadSummary::window_extent` only ever carried their difference.

**One decode, two reductions.** The CSV-to-timeline body is factored into a private `decode_with_cap`; `summarize` still reduces its `Decoded` to `LoadSummary`, and a new `spans_answer` reduces the same `Decoded` to `SpansAnswer`, no further computation. `study.rs`'s two handlers share one tap-resolution helper and differ only in which function gets the CSV.

**The CSV half, measured.** No reference-shaped CSV (225,627 rows/112,804 spans/26 lanes, decision 18's 12.6 MB figure) exists to re-measure — not checked in; `embarch-ui`'s `EMBARCH_VIEW_CSV` scratch test reads an arbitrary local path. Measurable instead: `embarch-core`'s own real-firmware fixture renders to **43,573 B / 831 rows — 52.367 B/row** [measured 2026-09-17]. Extrapolated to 225,627 rows: **≈ 11.8 MB** — order-of-magnitude, direction of error not established: `rx_utc_ms` is empty throughout, row width already spans 22–67 B within the fixture itself (~3x, around a 51.4 B mean), and the fixture's 4-lane/7-name profile is structurally unlike the reference's 26-lane/112,804-span one (decision 18), so the row-kind mix this average assumes may not generalize either way. **Holds: same order of magnitude as 12.6 MB regardless** — decision 64 stands; no response-shape change follows.

---
