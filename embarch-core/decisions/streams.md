# embarch-core decisions: Streams, manifests, and rendering

**Status:** active, 2026-09-02.

What Core captures for a study and what it refuses to render: tap files, the manifest binding, and being the trace's clock.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).


## Streams, manifests, rendering

### 30 — Core captures stream taps for a study's duration, including a port it opens itself
The consuming half of `embarch-study-designer` decision 39 and of `embarch-outpost`.

**A second serial port belongs to a wire, not a device.** A direct-route signal tap is a bridge with the DUT's TX pin on it and nothing else, so it takes **neither lock** — blocking a `/flash` on a read-only listener would invent contention that does not exist — while its lifetime stays bounded by the study.

**`streams/` replaces the three fixed CSVs as paths**, written incrementally with **raw bytes always before any decode**, which is what makes a run with a bad layout recoverable. `streams/index.json` exists because a handler has no `Study` in hand — Core keeps no resident copy of a finished study — so the name a caller asks for has to resolve to a file off disk. That is also what stops a tap name escaping the streams directory: only a name the index already carries resolves to anything.

> **Retired 2026-09-11 (`tasks/suite/015`).** `GET /study/{id}/power-data`, `/waveform-data` and
> `/gatt-data` — kept as aliases for one release — are gone, along with `serve_alias`,
> `StreamIndex::find_alias`, `alias_for`, and the persisted `alias` field on every
> `streams/index.json` entry and on `GET /study/{id}/streams`'s response. The route sweep is 23 cases
> over 22 registered routes.
>
> **Two things this settled that the grant had left open.** `alias_for` mapped a `PowerFrontEnd`
> source to `"power"` — a capture that cannot exist, since power profiling is deferred with no
> hardware ordered. And `serve_alias`'s **pre-`streams/` on-disk fallback was dead code**: all 50
> studies under this machine's `study_results/` carry a `streams/index.json` [measured 2026-09-11],
> so the branch that reads `data.csv`/`waveform.csv`/`gatt.csv` at the old fixed paths had nothing
> left to serve. That is evidence from one machine rather than proof about all of them — but this
> suite has shipped exactly one release, and it is the release that wrote `streams/`.
>
> `streams/index.json` itself stays. Resolving the aliases was its second job; the name → file
> mapping in the paragraph above was always the load-bearing one.

**A manifest is bound by the study's own flash and verified by build ID** — **selection whose lifetime is that study**, never a persisted "current firmware" record. On mismatch Core writes the raw stream and **renders nothing**: rendering against the nearest available manifest produces a trace that is completely readable and completely wrong, relabelling every marker and thread. Loud beats plausible. It rides as a sibling of `firmware` on the call that already carries the artifact, parsed **before** the flash so a build problem is reported while the person who ran the build is watching, stored **after** it succeeds, and **keyed per chip** because `/flash` also writes the bench's firmware. Refusal costs the *names*, never the capture.

**Core is the trace's clock, and a join it cannot verify stamps nothing.** The frame index counts non-empty runs between delimiters on both sides, so a frame that later fails its CRC still consumes one — indexing by *successfully decoded* frames would silently shift every stamp after the first corrupt one. The raw file rotates and the arrival log does not, so each row carries its frame's length and the renderer checks the alignments agree: a trace shifted by three frames is readable, wrong, and indistinguishable from a correct one. Rendering is post-hoc from the complete file, which is what lets a late header name every record before it — a claim the code did not honour until the header was found in a pre-pass, leaving 488 of 9205 rows unnamed *and* untimed inside a stream whose index said `named: true`. What stays refused is *invention*.

Retention is two-segment rotation plus a count-based keep-last-N sweep, so it needs no clock, with the truncation marker firing on the **deletion** rather than the rotation. A stale prefix on a signal port is discarded on open — a TX-only DUT transmits whether or not anyone listens, and one study's first six records sat 195 s ahead of the seventh — though [the clear is not sufficient](../open.md).

### 38 — Core renders a `Struct`-encoded tap and holds no more column knowledge than before
The store takes the study's declared decoders alongside its taps, because a struct tap's CSV *header* is the engineer's field list and cannot be derived from the encoding — the one place this differs from the encodings whose headers are compile-time constants of the shared crate. Core still knows no field name, width, or byte order. **The failed-decode row is Core's, and it is a row rather than a log line:** dropping it would leave a record that genuinely arrived indistinguishable from a notification that never came, and a warning in `core.log` is not visible to whoever opens the CSV.

### 39 — The third pre-flight seal, and the two indices a manifest cannot check about itself
`validate_study` recomputes `protocols_crc` too, and that seal exists for a reason the others make plain by contrast: `Study.decoders` is covered by **none** of them, because a layout only decides how Core *renders* a byte already captured, and re-rendering with a corrected layout must leave it the same study. A protocol is the opposite — dev-bench executes it — so corrupting one in flight would have firmware writing different bytes to a DUT's control point than the study said. Three sibling seals, checked independently, so a rejection names which third arrived wrong. **`validate_protocol` is called, not reimplemented.** The two indices it structurally cannot see are Core's, because they live on a `Step`: a `RunProtocol`'s protocol index and entry state, which nothing else in the suite resolves.

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

---
