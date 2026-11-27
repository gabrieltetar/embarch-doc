# embarch-core: modules

**Status:** active, 2026-11-09. Split out of [spec.md](../spec.md) §4 the same day, when that file passed its reserve line ([DOC-COMPACTION.md](../../DOC-COMPACTION.md) §3) — the table moved verbatim, nothing cut.

| Module | Owns |
|---|---|
| `main.rs` | CLI; `init_tracing()` (stderr + daily-rolling file), token resolution, `AppState`, Axum start |
| `api.rs` | router, handlers, `auth_middleware` |
| `hardware.rs` | probe-rs: list, flash, reset; `resolve_probe`/`open_probe`; target-power pre-flight |
| `bootload.rs` | `POST /bootload`'s flow around `embarch-smp`: image check, bootloader entry, upload, reset, the application's return (decision 77) |
| `flash_backend.rs` | per-chip-family backend choice and vendor-tool discovery (decision 36) |
| `chip_resolve.rs` | Zephyr SoC → probe-rs chip target, validated against probe-rs's own registry |
| `serial.rs` | fixed-duration UART capture (not a stream) |
| `logs.rs` | `latest_log_file`/`tail_lines`, one implementation behind the CLI and `/logs/recent` |
| `dev_bench_log.rs` | the bench's own daily-rolling debug file, plus `classify()` and Core's boundary markers |
| `service.rs` | registration via `service-manager`; a `windows` submodule for the real SCM dispatch |
| `elevate.rs` | `is_elevated()`/`ensure_elevated_or_fallback()` |
| `token_store.rs` | resolves/generates/persists the agent and person token files (decision 109), `Scope`, `Tokens`; `local_data_dir()` |
| `measurements.rs` | `measurements.json`: the declared reducers over a study's captures, as it ends (decision 113) |
| `signing.rs` | the Ed25519 key, `record.dsse.json` (DSSE over an in-toto Statement), the declarations ledger, `POST /auth/challenge` (decision 110) |
| `call_log.rs` | `call-log.jsonl`: the layer that chains one entry per gated call, refusals included, folds repeated reads, names each answer's entry in headers; `GET /call-log` (decision 122) |
| `definitions.rs`, `confirmations.rs` | HIL definitions kept by hash, the premade suites read from `EMBARCH_SUITES_DIR`, the cards' nonces; six routes (decision 133) |
| `test_runs.rs` | a run re-expanded and registered prepared under its id, and its go card (decision 134); two routes |
| `manual.rs` | a manual verdict, a unit's declared serial and the person's name as run-log entries, five routes (decision 147) |
| `test_publish.rs` | a Test run's `report-data.json` (the crate's roll-up, every run on the unit) and its publish over `publish.rs`'s signing; two routes (decisions 148, 149) |
| `run_log.rs` | `run-log.jsonl`: the chained entry per run, publish and discard, the discard refused by scope, the retention split, four routes (decision 111) |
| `dev_bench_link.rs` | the serial transport: postcard+COBS encode/decode, open-per-study, all I/O in `spawn_blocking` |
| `study.rs` | `/study*` handlers, handshake, `study_lock`, in-memory job registry, host watchdog, `EventsJsonWriter`, the version gate, signal-tap reader threads |
| `host_study.rs` | `POST /host-studies`, `/study/{id}/cancel`, `/study/{id}/prompt`: the executor, teardown, taps, prompts (95, 98, 105, 107) |
| `stream_store.rs` | `streams/`, `index.json`, segment rotation, the keep-last-N sweep (sparing a session's `session.keep` directory, decision 125). Holds no column knowledge |
| `analog_tap.rs` | a framed analog tap's decoder: partial records carried across reads, gaps by index, marker edges, `events.csv` rows (decision 125) |
| `outpost_manifest.rs` | `ManifestSlot`: binds a flash's `outpost-manifest.json` to the DUT it flashed, checks the running firmware's build ID against it before rendering a trace, and refuses to render (never to warn) on a mismatch |
| `outpost_load.rs` | Per-subject load shares and the coverage line over a rendered `*.trace.csv` (decision 62, suite decision 4) — the answer `GET /study/{id}/stream/{name}/load` serves. Consumes the CSV `outpost_manifest.rs` already produced; never touches the raw frames or the manifest. The decoded timeline it reduces from is not served (`/load/spans` retired, decision 91); `embarch-ui` keeps its own decode permanently |
| `readback.rs` | `readback`: a board's flashed segments read back through the probe, hashed, and the state that holds; the bench-firmware list loader (decision 142). No caller yet |
