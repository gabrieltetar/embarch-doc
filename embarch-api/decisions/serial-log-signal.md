# embarch-api decisions: serial_log reads a declared signal

**Status:** active, 2026-10-28.

Index: [../decisions.md](../decisions.md). Surface: [../interfaces/tools-build-flash.md](../interfaces/tools-build-flash.md). Builds on `embarch-core` decision 79 and [hardware-selection.md](hardware-selection.md) 70.

### 94 — `serial_log` takes `signal`; Core resolves it, this crate never does
Field use on a USB PD board: the DUT console moved between a UART bridge and a CDC ACM port twice, `serial_log` failed on a re-enumerating port just after a reset while the signal path to the same console worked, and five calls named a bench project only to reach the DUT's COM name. A declared direct signal already carries the port's USB serial and baud, and Core resolves it to the current name and waits `port_wait_ms` for a port that is coming back.

`serial_log` (tool and `serial-log` subcommand) therefore takes `signal` (and `port_wait_ms`, CLI `--port-wait-ms`), the documented preferred form: it calls `CoreClient::serial_log_signal`, which sends `GET /serial-log?signal=..&duration_ms=..` and sends **no `port`, and `baud` only when the caller gave one** (an override; otherwise the signal's baud is Core's). No project is needed (CLI `project` is required only without `--signal`). `project`/`port` stay as the fallback for a port nobody declared, unchanged, including decision 70's refusal to pick a port on a caller's behalf.

**One resolver, Core's.** This crate does not look the signal up in `/signals` and `/serial-ports` itself: a second resolver would disagree with exchange's on the first edge case, and decision 70's reasoning about inferring hardware facts applies unchanged. The cost is a dependency on a Core half (`/serial-log` accepting `signal`, filed as `core-serial-log-resolves-a-declared-signal` in the inbox). **Until it lands, the signal form is refused by Core** (today's `SerialLogQuery` requires `port`, so a 400 reaches the caller verbatim); nothing in this crate falls back silently to a guessed port. Measured: the request shape against a mock Core only; no real Core or board was touched.
