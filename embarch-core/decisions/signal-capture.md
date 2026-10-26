# embarch-core decisions: Capturing a declared signal in the background

**Status:** active, 2026-10-26.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md). HTTP surface: [../interfaces/topology.md](../interfaces/topology.md). Sibling: [signal-exchange.md](signal-exchange.md) (decision 79, whose reason for refusing a held-open session this keeps).

### 92 — `POST|GET|DELETE /signals/{name}/capture`: a background read of one port that never takes `hw_lock`

A USB PD test needs both consoles at once: the bench board driven one command at a time while the DUT's log records what its policy engine did, for 10 to 60 s. `/serial-log` and an exchange each hold `hw_lock` for their whole read, so a log capture starves every exchange on the other console, and a capture ends at `serial::MAX_DURATION_MS` (10 s), under the client's 15 s timeout. The field answered with 69 hand-written serial scripts in six weeks.

**A capture is a thread that owns only its own port.** `POST` opens the signal's port and returns `{id, ...}` at once; `GET ?after=<offset>&limit=` returns the bytes from that offset (lossy UTF-8, escape codes left in, never ending mid-character while the capture runs) with `next_offset`, `state` and `gaps`; `DELETE` stops it, answers with what it holds from `after`, and drops it. None of the three takes `hw_lock`: flash, reset and exchanges on other signals run while it records, and the lock is still never held across an agent's thinking time, which is decision 79's reason for refusing a held-open session. The request that starts it returns in milliseconds, so a capture is not bounded by the client's 15 s timeout; only each `GET` is.

**Caps, both reasoned, not measured.** `max_s` default 60, max 600; `max_bytes` default 1 MiB, max 16 MiB, held in memory. A capture ends `expired` at `max_s` or `byte_cap` at `max_bytes`, and stays readable until the next capture on its signal replaces it or `DELETE` drops it. Out of range is a `400` before the signal is looked up.

**One capture per signal.** A second `POST` on a signal whose capture is still running is a `409` naming the first. `409` also for a `via-dev-bench` route, a port not enumerable now, and a port a study tap holds. The capture registers its port in `tap_ports`, so `POST /bootload` refuses it by name like a tap's.

**An exchange on the captured signal goes through the capture.** A COM port opens once, so the exchange is handed to the capture's thread, which writes through its open handle and reads the reply through a tee: the reply is returned as today and its bytes also land in the capture. `discard_pending` has nothing to do there (the capture has already consumed pending input). While the port is away, an exchange answers `409` at once rather than waiting.

**Reset and re-enumeration.** A UART bridge does not drop when its board resets, so the capture holds the boot lines ("arm, then reset") with no gap. A read error (a USB CDC ACM device re-enumerating) makes the capture `reopening`: it writes `[embarch: port lost]` into the byte stream, records a `gap` `{offset, lost_at_ms, reopened_at_ms}`, resolves the signal again every 250 ms, and on success writes `[embarch: port reopened]` and goes on.

**Not done: one port owner with a study's signal tap.** The two are separate readers today. A capture refuses a port a tap holds, but a study that starts afterwards and names a captured signal is not refused by name; its open fails at the OS. Merging them is `open.md`'s item and the `core` task for console capture during a host study.

**Rejected: `GET` as a long poll.** A wait on the request would put the client's timeout back in the loop; the caller polls with `after`.

### 94 — A capture stamps each line with when its first byte was received, on a UTC clock an exchange reply shares

`bench_exchange` merges two consoles into one timeline, and a capture's `GET` carried only a byte range, so the client stamped a line with the poll that first saw it, a ceiling within its poll interval. Core is where the bytes arrive, so it records the time (api decision 89, `tasks/core/115`).

**Wire, additive.** `GET`/`DELETE /signals/{name}/capture` gain `started_utc_ms` (the capture's start, UTC ms since the Unix epoch) and `lines: [{offset, rx_ms}]`: one entry per line whose **first byte** lies in `[offset, next_offset)`, `offset` absolute in the capture's byte space (the same as `gaps`), `rx_ms` relative to `started_utc_ms`, ascending. `POST` answers the same shape with `lines: []`. `POST /signals/{name}/exchange` gains `started_utc_ms` beside `elapsed_ms`, so a reply spans `[started_utc_ms, started_utc_ms + elapsed_ms]` on the capture's clock. A client that ignores the fields is unaffected.

**Stamped at the first byte, not the newline.** A line is entered when its first byte is appended, so a half-received line is already placed and a slow line carries when it began. Every line is stamped, including the `[embarch: port lost]` and `[embarch: port reopened]` markers; a line's offset is always a byte after a `\n` or 0, so offsets match `text` across a gap.

**Resolution is the read, not the byte.** The time is the capture thread's clock when its `read()` returned the chunk, so lines in one chunk share a time and a line is placed within the port's read latency (a USB-UART bridge's 1 to 16 ms latency timer, assumed, not measured). `rx_ms` is a monotonic `Instant` offset; `started_utc_ms` is wall time sampled once, so within a capture times are exact to the millisecond and across captures they carry the wall clock's own error (assumed small on one host; not measured). Memory: 16 bytes per line, worst case one per byte of `max_bytes` (256 MB at the 16 MiB cap on an all-newline console); reasoned as acceptable, not measured.

**Rejected: timing the newline.** It would order a long line by its end, which is not when its cause happened.
