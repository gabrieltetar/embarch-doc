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
