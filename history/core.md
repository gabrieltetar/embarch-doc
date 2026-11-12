# core: history

**Status:** active, 2026-09-02. Assembled from `changelog.d/` fragments by `scripts/build_changelog.py`; newest window first. Capped at 20 KB: over that, whole windows roll off the end, oldest first — never the newest, so a single over-cap window stays and says so — into [archive/](archive/).

## 2026-11

### Changed
- `GET /dev-bench/hello` serves the bench's build as `dev_bench_version`, not `firmware_version`, the DUT's name on a Study; the wire `HelloAck` is unchanged (108).
- Core's study pre-flight now refuses a one-shot monitor step inside an open monitor window, with the crate's message (core decision 90).
- Core decisions split: probes.md now holds probe selection; chip mapping moved to chip-mapping.md; spec.md module table moved to interfaces/modules.md.
## 2026-10

### Added
- Core: POST /signals/{name}/exchange writes one line to a writable signal and returns the reply under hw_lock; taps use the signal's own baud (decision 79).
- Core: `POST /live/mem-read` reads ranges of a role's target memory under one halt, behind the identity gate.
- Core: `port_wait_ms` on the signal exchange waits for a USB console that is re-enumerating after a reset.
- `POST /probes/enroll` without a role enrolls a named bench board; `DELETE /probes/by-serial/{serial}` retracts one (decision 83).
- Core: GET /serial-log takes signal= (resolved at request time, waits port_wait_ms, reads at the signal's baud); port= unchanged — decision 101.
- A host study runs `Repeat` with per-pass markers; `GET/POST /study/{id}/line-counts` counts each `LineCount` per pass and in total from the raw tap files.
- `POST /host-studies` accepts `Text` signal taps: a tapped console opens once for the whole study, exchanges write through it, and each line is stored with Core's receive time. Decision 98.
- Core: POST /live/core-state reads DHCSR and PC samples without halting, or registers under one halt; mem-read gains found/left/halt_count (decision 97).
- Core runs host studies: `POST /host-studies` executes Exchange and Wait steps, teardown on every exit, `POST /study/{id}/cancel` (core decision 95).
- Capture reads stamp each line with its receive time (`lines`, `started_utc_ms`); exchange replies carry `started_utc_ms`. Additive; decision 94.
- Core gains `/lease`: one session holds the whole bench across calls, others get 409 by name; `GET /status` adds `lease` and `last_images` (decision 93).
- Core: `/signals/{name}/capture` records a declared signal in the background, no `hw_lock`; exchanges on it use its port ([decision 92](../embarch-core/decisions/signal-capture.md)).
- POST /probes/enroll adds displaced, vacated and vacated_kept when an enrol moves a role; absent otherwise (core decision 87).

### Changed
- Windows `install` over a registered service rewrites it in place, keeps its `Environment`, and applies the restart policy via `sc failure` ([decision 106](../embarch-core/decisions/platform.md)).
- Instrument pacing comments in embarch-core now say it runs from the end of the previous exchange, matching topology's field doc; `mark_sent` is `mark_exchanged`. No behaviour change.
- Core: POST /study answers 409 up front for a tap on a captured signal, instead of an OS port error after flash (core decision 102).
- Core's live-read halt_count now takes the identity gate's share from topology's Validation.halts instead of inferring it by chip prefix (core decision 97).
- Core refuses a submitted study whose Notify or Indicate step has a wait budget of 0, naming the step and operation, before any hardware is touched.
- Core: a signal exchange reports bytes_read, echo_seen, written, port_lost (a 200, not a 500), port identity and DHCSR core state when silent, and reads a mid-line marker to line end (decision 85).

### Fixed
- Core: a signal exchange matches `until` only after the command's echo, so a shell's prompt on port open no longer ends the read early (decision 79).
- Core: flash and reset attach through topology's guarded attach, so they never rewrite a running STM32's clock enables (decision 80).
- `POST /flash` resets the core after the download, so a flashed STM32G0 runs its new image instead of staying halted in the flash algorithm (decision 82).
- Two capture-timing tests (capture lines, two tapped consoles) no longer flake under a full parallel run: they wait on the byte count, not a sleep.
- Core's exchange, capture, study and pre-flight name every candidate port when a signal's declared serial is ambiguous (409 on HTTP); the wait never retries it (decision 96).
- Capture routes now sit under the bearer-token sweep; a bare .route( line fails the scan (core decision 42).
- `flash`, `reset` and memory reads refuse a requested chip that differs from the probe's enrolled chip with a 409 before any attach (decision 89).
- Core: a failed raw or rendered append marks a stream tap truncated; arrival sidecars always stamp Core's clock and a Text tap's offsets are rebased after rotation (decision 88).
- Core: POST /study refuses an empty record magic (decision 86); the trace CSV blanks a step name with CR/LF too, via the crate's csv_cell_ok.
- Dev-bench identity gate now takes hw_lock; GET /dev-bench/hello holds study_lock during its handshake (409 vs POST /study).
- A console exchange's write and read now share one `timeout_ms` instead of the read getting a fresh one after the write (decision 79).
- An exchange's line is written within `timeout_ms`, retried while the device throttles, and fails with the bytes taken instead of answering for a line sent with a hole in it.
- `POST /flash` with `erase: true` skips alias and non-writable NVM (STM32 option bytes), checks all ranges first, and answers `erased` ranges. [decision 84](../embarch-core/decisions/flashing.md)

### Removed
- Retired the GET /study/{id}/stream/{name}/load/spans route and decisions 65 and 66; no caller ever used it (core decision 91).
