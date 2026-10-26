# embarch-core decisions: Streams, manifests, and rendering

**Status:** active, 2026-09-02.

What Core captures for a study and what it refuses to render: tap files, the manifest binding, and being the trace's clock. Pushing a tap's bytes live while the study runs is [streams-live.md](streams-live.md). What the stream index reports back about a tap once it is captured — a computed load answer, and one declared against hardware this bench lacks — is [stream-index.md](stream-index.md).

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

### 88 — A failed capture write reads as lost data, and every sidecar is Core's clock and stays aligned

2026-10-26. A failed append to a tap's raw or rendered file sets `StreamRef.truncated`, the same flag a rotation deletion and a source drop set: a reader's question is "is this complete?", and a disk that filled partway must not answer yes. A failed append to an arrival sidecar does not: the frames are all there, only their time is lost, and the verified frame join already keeps just the prefix before a hole. **A record the raw file refused gets no sidecar row**, because the sidecar is keyed by what the raw file holds; a row for absent bytes would shift every later key.

**Both sidecar kinds stamp Core's own receipt time**, never the record's `rx_utc_ms`. That field is Core's clock only on a direct signal tap, and `OutpostTrace` is accepted on any source, so a bench-mediated trace would have been stamped with the bench's uptime and still reported `timed: true`. (Supersedes the earlier "frames record `rx_utc_ms`" split; the stamps do not move on today's only path.)

**`GET .../arrivals` on a `Text` tap rebases onto what survives.** The sidecar is never rotated and the raw file is, so after the raw file's oldest segment is deleted every offset from the start of the capture is shifted. The route computes the deleted head as (last row's end) - (surviving raw bytes), drops rows wholly inside it, clamps a straddling row to start at 0, shifts the rest, and reports the head length in `X-Arrivals-Head-Deleted`. Rebase rather than refuse, because the consumer joins offsets against `GET .../stream/{name}`, which serves only the survivors; a refused sidecar would cost it every time on a rotated console. Measured: unit tests with fabricated records; no hardware.

