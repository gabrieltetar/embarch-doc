# embarch-core decisions: Streams, manifests, and rendering

**Status:** active, 2026-09-02.

What Core captures for a study and what it refuses to render: tap files, the manifest binding, and being the trace's clock. What the stream index reports back about a tap once it is captured — a computed load answer, and one declared against hardware this bench lacks — is [stream-index.md](stream-index.md).

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).


## Streams, manifests, rendering

### 30 — Core captures stream taps for a study's duration, including a port it opens itself
The consuming half of `embarch-study-designer` decision 39 and of `embarch-outpost`.

**A second serial port belongs to a wire, not a device.** A direct-route signal tap is a bridge with the DUT's TX pin on it and nothing else, so it takes **neither lock** — blocking a `/flash` on a read-only listener would invent contention that does not exist — while its lifetime stays bounded by the study.

**`streams/` replaces the three fixed CSVs as paths**, written incrementally with **raw bytes always before any decode**, which is what makes a run with a bad layout recoverable. `streams/index.json` exists because a handler has no `Study` in hand — Core keeps no resident copy of a finished study — so the name a caller asks for has to resolve to a file off disk. That is also what stops a tap name escaping the streams directory: only a name the index already carries resolves to anything.

> **Retired 2026-09-11 (`tasks/suite/015`).** `GET /study/{id}/power-data`, `/waveform-data` and
> `/gatt-data` — kept as aliases for one release — are gone, along with `serve_alias`,
> `StreamIndex::find_alias`, `alias_for`, and the persisted `alias` field on every
> `streams/index.json` entry and on `GET /study/{id}/streams`'s response. The pre-`streams/`
> on-disk fallback (`data.csv`/`waveform.csv`/`gatt.csv` at the old fixed paths) was dead code by
> then: `streams/index.json`'s name → file mapping was always the load-bearing job.

**A manifest is bound by the study's own flash and verified by build ID** — **selection whose lifetime is that study**, never a persisted "current firmware" record. On mismatch Core writes the raw stream and **renders nothing**: rendering against the nearest available manifest produces a trace that is completely readable and completely wrong, relabelling every marker and thread. Loud beats plausible. It rides as a sibling of `firmware` on the call that already carries the artifact, parsed **before** the flash so a build problem is reported while the person who ran the build is watching, stored **after** it succeeds, and **keyed per chip** because `/flash` also writes the bench's firmware. Refusal costs the *names*, never the capture.

**Core is the trace's clock, and a join it cannot verify stamps nothing.** The frame index counts non-empty runs between delimiters on both sides, so a frame that later fails its CRC still consumes one — indexing by *successfully decoded* frames would silently shift every stamp after the first corrupt one. The raw file rotates and the arrival log does not, so each row carries its frame's length and the renderer checks the alignments agree: a trace shifted by three frames is readable, wrong, and indistinguishable from a correct one. Rendering is post-hoc from the complete file, which is what lets a late header name every record before it — a claim the code did not honour until the header was found in a pre-pass, leaving 488 of 9205 rows unnamed *and* untimed inside a stream whose index said `named: true`. What stays refused is *invention*.

Retention is two-segment rotation plus a count-based keep-last-N sweep, so it needs no clock, with the truncation marker firing on the **deletion** rather than the rotation. A stale prefix on a signal port is discarded on open — a TX-only DUT transmits whether or not anyone listens, and one study's first six records sat 195 s ahead of the seventh — though [the clear is not sufficient](../open.md).

### 38 — Core renders a `Struct`-encoded tap and holds no more column knowledge than before
The store takes the study's declared decoders alongside its taps, because a struct tap's CSV *header* is the engineer's field list and cannot be derived from the encoding — the one place this differs from the encodings whose headers are compile-time constants of the shared crate. Core still knows no field name, width, or byte order. **The failed-decode row is Core's, and it is a row rather than a log line:** dropping it would leave a record that genuinely arrived indistinguishable from a notification that never came, and a warning in `core.log` is not visible to whoever opens the CSV.

### 39 — The third pre-flight seal, and the two indices a manifest cannot check about itself
`validate_study` recomputes `protocols_crc` too, and that seal exists for a reason the others make plain by contrast: `Study.decoders` is covered by **none** of them, because a layout only decides how Core *renders* a byte already captured, and re-rendering with a corrected layout must leave it the same study. A protocol is the opposite — dev-bench executes it — so corrupting one in flight would have firmware writing different bytes to a DUT's control point than the study said. Three sibling seals, checked independently, so a rejection names which third arrived wrong. **`validate_protocol` is called, not reimplemented.** The two indices it structurally cannot see are Core's, because they live on a `Step`: a `RunProtocol`'s protocol index and entry state, which nothing else in the suite resolves.

### 70 — A `Text` tap pushes its chunks live, verbatim; `Raw` pushes nothing
`Text` and `Raw` tap bytes were written to disk and **pushed nowhere** — `StudyEvent` had no variant for them — so the one encoding whose payload a person reads directly was the one no client could watch arrive. Both of `embarch-ui`'s consoles (the reserved `dev-bench` log tap, and a DUT shell declared as a `Text` tap on a notify characteristic) hung off this single gap, in the one arm of `write_stream_record` that wrote the file and returned. `StudyEvent::StreamText` is emitted beside that write, in the shape `SampleBatch` and `GattTranscript` already have three arms up.

**The chunk is carried exactly as it arrived.** No line framing: a record can split a line, and it can split a UTF-8 character. Assembling lines is the consumer's job, because Core inventing line boundaries would be Core interpreting a payload — what this function's own contract refuses and what decision 39 settled by making a tap's declared encoding the only source of meaning. `text` is `from_utf8_lossy`, so a split character costs a replacement character in the *event* and never touches the capture, which keeps the bytes intact. Bounded without a cap of its own: a record is at most `MAX_STREAM_CHUNK_BYTES` (512).

**`Raw` deliberately gets no event**, and says so in the code: a console of hex is noise and nothing has asked for one. Pinned by a test, so adding one later is a decision somebody takes rather than a test nobody had to change.

*No schema bump.* This is the host-side HTTP/SSE surface, not the dev-bench wire protocol. An older `embarch-api` is unaffected: its mirror enum is `#[serde(tag = "kind")]` and an unknown kind already decodes to `StudyStreamItem::Unrecognized` by design.

---
