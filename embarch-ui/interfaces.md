# embarch-ui: interfaces

**Status:** active, 2026-09-09. Split out of [spec.md](spec.md) ([DOC-COMPACTION.md](../DOC-COMPACTION.md) §3) when it reached its size cap — a reference section, not cut. Why: [decisions.md](decisions.md).

## The trace chart

The reference reference-dut capture is the working shape to design against: **147.5 s, 225,606 rows, 112,801 spans, 26 lanes.** Wheel zooms at the pointer, drag pans, the window is clamped to the capture. Lanes scroll vertically with the axis and step row pinned; they can be filtered, hidden and reordered. **What filtering may and may not touch is an invariant and it is stated in [spec.md](spec.md), not here** — a reference file is the wrong home for a fact someone has to hold in their head before they change lane filtering ([DOC-COMPACTION.md](../DOC-COMPACTION.md) §3's hot/cold split; the reasoning is `decisions/trace-chart.md`).

It stays SVG. Sub-pixel spans aggregate into per-pixel occupancy runs per lane, so **the element count is bounded by pixels × lanes, not by the dataset**: ~2,500 rects worst case, 27 ms to redraw. Aggregation is exact — a run splits wherever a gap, a below-resolution flag or an open edge changes.

**That aggregation runs on the server, and the view asks for the window it is about to draw** (decision 18). `GET /api/trace/{study}/{tap}/bins?from&to&width` returns at most `width` runs per lane; the view's own payload carries no spans at all, only each lane's `span_count`. The spans were not part of the payload, they were the payload — 12.6 MB of a 12.6 MB JSON on a reference-shaped capture — so first paint is **12.7 KB + 30.5 KB** and a window costs **1–6 ms** end to end. The browser never draws from a window's bins that is not the window it is drawing.

Two view caps, both served rather than restated (`decisions/trace-rows.md` 21, `decisions/study-designer.md` 22): **250,000 rows per view** (`MAX_ROWS`, `TraceView::row_cap`), reported rather than swallowed, and a name-length limit (`MAX_STREAM_NAME_LEN`, `ActionsResponse::max_stream_name_len`) applied where a name is chosen rather than at submit.

## What the Study Designer is served

`GET /api/study-designer/actions` is this tab's one channel for anything the browser must not restate — a limit, a vocabulary, or a fact about the firmware repo. A test asserts `app.js` holds no copy of any of it, and the response struct's own literal in `study_designer.rs` is what makes the positive half compiler-enforced: a field added without a line there does not compile.

| Field | What it carries | Why served |
|---|---|---|
| `max_monitor_targets` | `limits::MAX_MONITOR_TARGETS` | the selective-monitor picker stops here |
| `max_stream_name_len` | `limits::MAX_STREAM_NAME_LEN` | a default tap name is sliced to it, or not sliced at all when it is unknown |
| `max_protocols_per_study` | `limits::MAX_PROTOCOLS_PER_STUDY` | how many distinct protocols the rows may name between them |
| `max_record_magic_len` | `limits::MAX_RECORD_MAGIC_LEN` | the framing cell names an over-long magic rather than trimming it |
| `max_struct_fields` | `limits::MAX_STRUCT_FIELDS` | the layout editor's per-group ceiling |
| `scalar_types` | `ScalarType::ALL`'s eighteen spellings, picker order | the layout editor's type dropdown; **an empty list is an empty picker and a refusal** |
| `dev_bench_log_levels` | `DevBenchLogLevel::ALL` as `{value, label, note, default}` | the level picker. `value` is the bare PascalCase a saved study carries; `default` is served because *which* level is the default is a fact of the enum, and a picker that pre-selected nothing would show `Off` first — the one level a study must never reach by not choosing |
| `dev_bench_limits` | the three advisory dev-bench capacities | the caps note. `null` renders as **unknown**, never as "within caps" |
| `protocols` | every `.eap` block, `{name, file, resolved, states[{name, terminal, outcome}]}` | the `RunProtocol` row's two pickers. A block that parsed but did not **resolve** is listed with its name and no states, because that is a different fact from a protocol that is not there |
| `unparsed_files` | stems of `.eap` files that did not parse at all | a file that did not parse declares nothing nameable, so a row pointing into one can only be told apart from a row pointing at a deleted protocol by saying some file is unreadable |
| `struct_layouts` | `study-structs.toml` entries, **field definitions and not just names** | one shape read by both the tap's decoder dropdown (which needs `name`) and the layout editor (which needs the fields), rather than a second route over one file |

### The routes this tab owns

Under `/api/study-designer/`. `404` with no project open, `400` for authoring, `502` + the error for a Core hop, `500` for local I/O.

| Method | Path | Notes |
|---|---|---|
| `GET` | `actions` | the table above, plus the merged action list |
| `POST` | `preflight` | builds the study a run would submit and reports what it is: counts, the protocols the rows named, `protocols_wire_len`, and one sentence per advisory cap it is over. **Never gates** |
| `GET` | `protocols` | every `.eap` file with its text, its resolved blocks, its errors, and the repo's duplicate protocol names |
| `GET`·`PUT`·`DELETE` | `protocols/{stem}` | `PUT` refuses unparseable text with `EapError`'s own `line {n}: …` unchanged, so the editor's band and the message cannot disagree about where the problem is. `DELETE` refuses a referenced protocol (`409`). The stem is validated here and again in `eap_repo::save` |
| `POST` | `protocols/check` | **`200` even when `ok` is false** — reporting errors is its purpose, the shape `version-check` already uses |
| `POST`·`DELETE` | `registry`, `registry/{name}` | `previous_name` in the body makes edit and rename one form: absent is the upsert, present and different reference-checks the old name first |
| `GET`·`POST`·`DELETE` | `structs`, `structs/{name}` | every write through `StructRegistry::save`, so validation stays the crate's |
| `GET` | `studies/{slug}/summary` | what a saved study *is*, without loading it into the table — the read-only preview for a run-only file, and what the version-check dialog reads |
| `POST` | `studies/{slug}/run` | runs a saved file as it is on disk: reseal all three, run the crate's own pre-flight locally, submit |

**One structured error body, and only one.** The three `409` refusals carry `{error, referenced_by:[{slug, name, steps}], unscannable}`, because the payload is a list the dialog renders as a table and a table reconstructed by splitting a sentence is a parser. Every other error here is plain text, and the browser renders a refusal it cannot parse verbatim.

Both registries' `save` rewrite the whole TOML through `to_string_pretty`, so **comments in a hand-edited `study-actions.toml` or `study-structs.toml` are lost.** Already true of the upsert these grew out of; an edit form makes it routine. A comment-preserving writer is a new dependency and its own decision.

