# core: history

**Status:** active, 2026-09-02. Assembled from `changelog.d/` fragments by `scripts/build_changelog.py`; newest window first. Capped at 20 KB: over that, whole windows roll off the end, oldest first — never the newest, so a single over-cap window stays and says so — into [archive/](archive/).

## 2026-11

### Added
- A bench instrument's value carries its declared U, resolution and calibration; past its due date it is judged calibration_expired: [decision 140](../embarch-core/decisions/instrument-metrology.md)
- A Test run raises a setup prompt before each bench after the first and admits enrolment and signal calls while it waits; an agent's answer is relayed. Decision 139.
- Core refuses the agent's token an observation or a clearance prompt (403), records each answer's scope, takes an observation's value as a person measurement (decision 138).
- Core runs a started Test run test by test under the failure policy, judges each with the shared crate, and answers GET /test-runs/{id} (decision 136).
- `POST /test-runs/{id}/go` (the person's token) starts a prepared run and moves the bench lease to it; `/cancel` ends it; the lease returns to its session. Decision 135.
- Core registers a prepared Test run it re-expands and serves its go card, with a nonce for the person only: `POST /test-runs`, `GET /test-runs/{run_id}/card` (decision 134).
- Core keeps HIL definitions by hash, reads premade suites from EMBARCH_SUITES_DIR, and records a person-only confirmation in the run log (decision 133).
- Core reads a host step's declared parse out of its reply, records it in events.json and writes measurements.json for a host study (decision 131).
- Core keeps the declared signal and instrument serial ports open for a lease's or a study's life and lists them in the signed record (decision 130).
- Core's `run --service` and `run --store <dir>` keep the key, logs and identity in their own store; /status and the challenge say `mode` and `keyid` (decision 129).
- Core: a run's signed record names its call-log range (`observed.call_log`), and publish writes `call-log-segment.jsonl` beside the run-log segment ([publish](../embarch-core/interfaces/publish.md)).
- Core releases a bench lease after 30 minutes with no hardware call, whatever client renews it; a renew after it is refused naming the idle release (decision 123).
- Core chains every call to a lease-gated route, refusals too, into `call-log.jsonl`; answers name their entry; `GET /call-log` reads a range ([decision 122](../embarch-core/decisions/call-log.md)).
- Core: GET /study/{id}/measurements returns a finished run's measurements.json unchanged, no publish; distinct 404/409/410/422 refusals ([decision 121](../embarch-core/decisions/measurements.md))
- Core takes a swept run's earlier files back through PUT /study/{id}/restore, checked against its logged manifest, so a republish works (decision 120).
- Core's publish files route serves the run's own files (measurements.json, events.json, streams) at the pending revision, before publish signs them (EMB-241).
- Core signs a publish manifest and report-data.json for a study run, takes notes by scope and hash, and records the run log head ([decisions 116-119](../embarch-core/decisions/publish.md)).
- Core computes a study's declared measurements as it ends and writes `measurements.json`, a signed subject of the run record ([decision 113](../embarch-core/decisions/measurements.md)).
- Core keeps a hash-chained run log, retention sweeps no unpublished run, and only the person token discards a failing run (decisions 111, 112).
- Core signs each study run's record (Ed25519, DSSE over an in-toto Statement) and answers a fixed-frame `POST /auth/challenge`: [decision 110](../embarch-core/decisions/signing.md).
- Core writes an agent token and a person token and records which one each request carried; nothing is refused by scope yet (decision 109).

### Changed
- Core refuses identity routes (enroll, signals, instruments, bootload ports, dev-bench link) to the agent's token under --service, 403; dev Core unchanged (core decision 132).
- Core builds against host schema v25 (`embarch-study-designer` decision 108): it accepts a host study whose steps declare a `parse` or whose prompts declare a kind, and does not act on either yet.
- Core refuses a study with a GATT notify tap no step subscribes to, at submit; run_study is refused the same way.
- Core's persisted record of what it flashed: spec invariant and /status row now say so; spec.md out of reserve (signing text moved to spec/signing.md).
- Core appends each flash and bootload, with its load segments, scope and call-log seq, to flashed-images.jsonl, and reads it at start, so last_images survives a restart.
- Core: `PUT /instruments` and `POST /signals` accept and store a declaration's `safe_off`, refusing a bad line with `400`; nothing sends it yet (topology decision 49).
- The Core README no longer carries an endpoint count or a file/endpoint list; it points at the interface docs.
- report-data.json carries observed.call_log {head, first_seq, last_seq, count} from the signed record, when it has one (core/148, paired with api/185); see interfaces/publish.md.
- Core refuses every lease-gated call, the lease holder's too, while a study runs; only the study's cancel is admitted (decision 95).
- Core refuses POST /instruments/{name}/exchange for every caller with 409 naming a host study Instrument step; decision 104 (embarch-core/decisions/instruments.md).
- core open.md no longer owes verify check 8: embarch-api decision 121 checks the zip segment against the signed head; the publish entry stays unverifiable offline.
- Core's release workflow signs every archive with cosign (Sigstore keyless) and uploads a `.sigstore.json` bundle beside it; see [spec](../embarch-core/spec.md) §3.
- Core open.md: never-exercised bullets split out to open/never-exercised.md, verbatim.
- `GET /dev-bench/hello` serves the bench's build as `dev_bench_version`, not `firmware_version`, the DUT's name on a Study; the wire `HelloAck` is unchanged (108).
- Core's study pre-flight now refuses a one-shot monitor step inside an open monitor window, with the crate's message (core decision 90).
- Core decisions split: probes.md now holds probe selection; chip mapping moved to chip-mapping.md; spec.md module table moved to interfaces/modules.md.

### Fixed
- Retention sweeps nothing, and GET /studies lists everything, while Core's run log cannot be read or verified (decision 111).
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
