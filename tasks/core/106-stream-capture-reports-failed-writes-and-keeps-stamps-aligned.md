# 106 — A stream capture reports a failed write as lost data, and its arrival sidecars stay on Core's clock and aligned after rotation

**State:** claimed by agent/core/106-stream-capture-reports-failed-writes-and-keeps-stamps-aligned, 2026-10-26 03:42
**Doc reserve (dispatch, 2026-10-26):** nothing in `embarch-core/` is in reserve. If your edit pushes a file into reserve, file `tasks/core/<NNN>-compact-core.md` in the same commit.
**Source:** DeepSeek V4 Pro review 2026-10-25 (embarch-core findings 3, 6 and 1), verified by Opus against embarch-core@40a58ccb
**Scope:** core
**Hardware:** none — every case can be driven with fabricated records and a temporary results directory.
**Owner:** no

## What

There are three ways a study's `streams/` can describe a capture that is not what is on disk. All three are in `embarch-core/src/stream_store.rs` at `40a58cc`.

1. **A failed write reads as a complete capture.** `write_raw`, `write_rendered_row` and `note_arrival` (`:687-698`, `:702-717`, `:748-755`) log a failed append and return. `StreamRef.truncated` (`:774-784`) reflects only a rotation's deletion and drops reported by the source. So a disk that fills, or a file another process locks, partway through a capture ends with the study `completed` and `truncated: false`. The flag's own doc comment (`:300-308`) names this exact outcome as the one it exists to prevent.
2. **A `Text` tap's sidecar offsets point at the wrong bytes once a segment is deleted.** `ArrivalLog::note` keys each row by its byte offset from the start of the capture (`:527-537`). The sidecar is deliberately never rotated (`:623-629`), but the raw `.txt` is. Its oldest segment is deleted on the second rotation (`SegmentedFile::rotate`, `:372-383`), and `read_capture` serves only what survives (`:404-428`). After that deletion, every offset `GET .../arrivals` serves is shifted by the deleted bytes, and nothing refuses or rebases the join. The frame-keyed join, by contrast, verifies itself before use (`outpost_manifest.rs:263`, `:301-304`). embarch-ui's console lane consumes these offsets (`embarch-ui/src/time_chart.rs:707-713`). It takes more than twice `EMBARCH_STREAM_MAX_BYTES` of console text, 64 MiB at the default. `truncated` is `true` by then, but the sidecar is served misaligned anyway.
3. **A frame sidecar stamps whatever clock the record carries.** `note_arrival` stamps an `OutpostTrace` sidecar with the record's own `rx_utc_ms` (`:741-744`). That is Core's clock only on a direct signal tap (`study.rs:2666`). `validate_taps` accepts an `OutpostTrace` encoding on any source, so a trace declared on a dev-bench-mediated source would be stamped with the bench's uptime and still report `timed: true`. The live preview of the same frames already uses `core_rx_utc_ms` (`study.rs:2826`). This is latent today: a via-dev-bench Signal route delivers no bytes at all, because dev-bench never produces a Signal tap's bytes (`embarch-dev-bench/app/src/serial_protocol.h:495-499`).

When this is done, a write failure marks the tap as having lost data. An arrivals read either lines up with the bytes `GET .../stream/{name}` serves or says the head was deleted. A frame sidecar carries Core's receipt time whatever the record says. The worker designs each mechanism. Also fix `interfaces/result-layout.md:19` in the same pass: it still says `<tap>.arrival.csv` is "OutpostTrace only", while `interfaces/streams.md:11` and the code (`stream_store.rs:608-611`) give `Text` taps one too.

## Why now

`embarch-core/spec.md` §2 promises that a failed decode "costs a rendering, never a capture", and the store's own comments promise that a capture that lost data says so. Item 1 breaks that promise silently. Item 3 contradicts `embarch-outpost/spec.md:89` ("a trace's `rx_utc_ms` is Core's real epoch clock") on a declaration Core accepts today. All three sit in the same few functions, so one unit covers them.

## Done when

- [x] A test where the raw append fails mid-capture yields `truncated: true` for that tap, and so does a failure on its rendered file. A failure on the arrival file leaves the frames untimed rather than wrongly timed.
- [x] A test that drives a `Text` tap through two rotations shows that every offset `GET .../arrivals` serves points at the bytes it pointed at when written, or that the route says the head was deleted instead of serving shifted offsets.
- [x] A test that feeds an `OutpostTrace` tap a record whose `rx_utc_ms` differs from Core's clock stamps the sidecar with Core's receipt time.
- [x] `interfaces/result-layout.md` lists both sidecar kinds and their columns.
- [x] No embarch-ui follow-up needed: the route rebases, so its offsets already line up with `GET .../stream/{name}`; the new `X-Arrivals-Head-Deleted` header is optional for it.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped.

## Outcome

Decision 88. Wire change: `GET .../arrivals` on a `Text` tap serves rebased offsets once the raw head is deleted, plus an `X-Arrivals-Head-Deleted` header. Windows build: not run (owner debt, unchanged).
