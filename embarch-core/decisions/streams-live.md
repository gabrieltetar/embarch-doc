# embarch-core decisions: Pushing a stream tap live

**Status:** active, 2026-09-28.

Split out of [streams.md](streams.md) on 2026-09-28 (`tasks/core/093`) — capturing a tap and rendering it post-hoc is one mission, pushing its bytes live while the study runs is another. What Core captures and refuses to render in the first place is [streams.md](streams.md).

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).


## Pushing a tap live

### 70 — A `Text` tap pushes its chunks live, verbatim; `Raw` pushes nothing
`Text` and `Raw` tap bytes were written to disk and **pushed nowhere** — `StudyEvent` had no variant for them — so the one encoding whose payload a person reads directly was the one no client could watch arrive. Both of `embarch-ui`'s consoles (the reserved `dev-bench` log tap, and a DUT shell declared as a `Text` tap on a notify characteristic) hung off this single gap, in the one arm of `write_stream_record` that wrote the file and returned. `StudyEvent::StreamText` is emitted beside that write, in the shape `SampleBatch` and `GattTranscript` already have three arms up.

**The chunk is carried exactly as it arrived.** No line framing: a record can split a line, and it can split a UTF-8 character. Assembling lines is the consumer's job, because Core inventing line boundaries would be Core interpreting a payload — what this function's own contract refuses and what decision 39 settled by making a tap's declared encoding the only source of meaning. `text` is `from_utf8_lossy`, so a split character costs a replacement character in the *event* and never touches the capture, which keeps the bytes intact. Bounded without a cap of its own: a record is at most `MAX_STREAM_CHUNK_BYTES` (512).

**`Raw` deliberately gets no event**, and says so in the code: a console of hex is noise and nothing has asked for one. Pinned by a test, so adding one later is a decision somebody takes rather than a test nobody had to change.

*No schema bump.* This is the host-side HTTP/SSE surface, not the dev-bench wire protocol. An older `embarch-api` is unaffected: its mirror enum is `#[serde(tag = "kind")]` and an unknown kind already decodes to `StudyStreamItem::Unrecognized` by design.

### 72 — An outpost trace is decoded and pushed live too, and the post-hoc render stays authoritative
`embarch-outpost` decision 10 made a trace study-scoped with no live feed, priced a live one exactly, and judged a complete recording to answer its question just as well. It does — and `embarch-ui`'s Time chart asks a different one: placing a GATT notification inside the step it arrived in, while the run is happening. So Core now decodes each frame as it arrives and pushes `StudyEvent::OutpostRows`. That is [reversals row 112](../../embarch-decision-reversals.md), and **only the feed is reversed**: capture is still study-scoped.

**`render_outpost_traces` is unchanged and still runs.** It has three things a live path cannot have — a whole-capture header pre-pass, so a late header names and dates every record before it; the stale-prefix drop over everything; and the verified arrival join, which refuses the whole join rather than shifting every timestamp. Live is a stated *preview* of it: a frame decoded before any header carries an empty `us` and an empty `name` and says so with `header_seen: false`.

**Rows go out as CSV lines in `outpost::csv_header()`'s own shape, not as a struct.** The consumer already parses those nine positional fields to read a rendered capture, so live and post-hoc decode through literally the same function on the other side rather than through two copies of a column order that belongs to `embarch-study-designer`. The two agree exactly on `frame_index`: both count non-empty zero-delimited runs in order, **including frames that fail their CRC**, because a bad frame still consumed an index while its bytes were being stamped. A test feeds the committed firmware-produced capture through both and compares row for row.

**`LiveDecoder` is held per capture**, on `Capture`, for three individually sufficient reasons: a cycle-counter wrap is only detectable against the previous record, a frame routinely splits across two reads, and the header applies to every frame after it.

### 73 — A `Text` tap gets an arrival sidecar, keyed by byte offset
Every other encoding renders rows that carry Core's own `core_rx_utc_ms`. A `Text` tap's raw file **is** its rendering (decision 30), so there is no rendered row to append one to — and a console read back off disk was bytes with no times anywhere, unplaceable on any shared axis. That is the one stream an engineer most wants to correlate, and it was the only one that could not be.

So `Text` joins `OutpostTrace` in keeping a `<tap>.arrival.csv`, and **each is keyed by the only coordinate its bytes have**: a trace by frame index (`frame_index,rx_utc_ms,frame_bytes`), a console by **byte offset** (`byte_offset,core_rx_utc_ms,bytes`). A reader places a line by the chunk that carried its first byte — exactly as precise as the recording is, since a chunk is one read and several lines completing in one read genuinely did arrive together. Nothing interpolates inside a chunk.

**The stamp is Core's own, explicitly**, not the record's `rx_utc_ms`: a `Text` tap can arrive mediated by dev-bench, whose stamp is that board's uptime and is comparable with nothing outside its own capture ([suite decision 3](../../suite/decisions.md)). The trace's sidecar keeps recording `record.rx_utc_ms`, which on the signal-tap path it arrives by already *is* `current_utc_ms()` — changing it would move every existing trace's stamps for no gain.

*Consequences.* `GET /study/{id}/stream/{name}/arrivals` serves it, because unlike a trace's there is no rendered file to join it into. The sidecar is deliberately unrotated, at ~24 bytes a chunk.
