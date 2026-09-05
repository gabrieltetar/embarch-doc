# embarch-core: spec

**Status:** active, 2026-09-02.

What is true now. Why: [decisions.md](decisions.md). Unresolved: [open.md](open.md). HTTP surface: [interfaces.md](interfaces.md).

## 1. What it is

The OS-level service that owns the debug probe (flash/reset), the DUT serial console, and the `embarch-dev-bench` serial link. It is the lowest layer in EmbArch and has no idea `embarch-api` or Claude Code exist. It exposes a bearer-token-authed HTTP API and holds the hardware connections so nothing else fights over a USB port.

It is **not**: aware of projects, toolchains, or build commands (it takes a bare `chip`/`firmware_path`/`format` per call); a build system — it never invokes `west` or `arduino-cli`, `embarch-api` sequences check → build → flash → submit, and decision 36 is the one exception, where Core *delegates* to a vendor flasher; or multi-tenant (one process, one hardware connection, one shared token).

```
embarch-api --HTTP+Bearer--> embarch-core --probe-rs/serialport--> DUT hardware
                                  ^  |
                                  |  +--serial, COBS-framed postcard--> embarch-dev-bench
                                  |  +--serial, read-only-------------> a DUT signal wire (outpost)
                     embarch-core CLI (same machine)
```

Reached two ways — over HTTP by `embarch-api`, and by its own CLI (`run`/`install`/`uninstall`/`start`/`stop`/`update`/`detect-dev-bench`/`chip-list`/`logs`/`dev-bench-logs`). Both converge on the same modules and the same `hw_lock`; there is no separate "CLI mode" code path.

## 2. Invariants

- **Every route requires `Authorization: Bearer <token>`**, no exceptions. One shared secret, exact-string compared in `auth_middleware`, resolved from `EMBARCH_TOKEN` and otherwise from the machine-wide file, generated and persisted on first startup. No per-caller identity and no TLS; full lifecycle, threat model and known gaps: [embarch-token.md](../embarch-token.md).
- **One `hw_lock` serialises all hardware access**, held for the whole handler body. Contention returns `503` naming the holder rather than queueing. A separate `study_lock` serialises studies; a signal tap's read-only port takes neither.
- **Every blocking hardware call runs in `tokio::task::spawn_blocking`.** `probe-rs` and `serialport` are synchronous.
- **Probe attach is per-call, never held open.** Open, attach, operate, drop.
- **Identity fails closed.** Before touching hardware, the resolved probe's serial must be enrolled and its live hardware ID must match what was recorded. Unenrolled or mismatched blocks the operation; never a guess.
- **Ambiguity fails loudly.** More than one probe with no `probe_serial`, or more than one dev-bench port candidate, is a named error listing every candidate — never a silent pick.
- **Raw bytes are written before any decode is attempted.** A failed decode costs a rendering, never a capture.
- **A refusal renders nothing rather than guessing.** A manifest that does not verify costs the *names* in a trace, not the trace; an unverifiable time join stamps nothing.
- **Core keeps no persisted "current firmware" record.** A manifest binding lives only as long as the study that made it. Write-ahead state that can go stale is the pattern this suite forbids.
- **`GET /status` says which build answered.** `core_version` is compiled in from `CARGO_PKG_VERSION`, so a caller learns the deployed binary's version **over HTTP** without running it. Consumers **warn** on a skew, never refuse (decision 13). There is no hand-bumped `contract_version` beside it.
- **Errors are plain text on every non-2xx**, so an error's *kind* is only its HTTP status. The designed `{code, message, cause}` body is deferred as cross-repo work (decision 12).
- **Default bind is `127.0.0.1`.** Widening is `embarch-umbrella setup`'s job, per detected topology.

## 3. Deployment

**An installed, autostarting OS service is the normal deployment** — that is what makes the rest of the suite need no launcher: if Core is up at boot, `embarch-api` always finds it running. A foreground `run` is fully supported and is the right choice for debugging Core itself.

Runs natively on Windows, reachable from WSL2 at the session's dynamic host-gateway IP. Windows Firewall needs no inbound rule under the newer Hyper-V-firewall WSL networking mode. Building natively on Windows needs Visual Studio Build Tools' "Desktop development with C++" workload for `link.exe` — a bare `rustup` toolchain is not enough.

`install`/`uninstall`/`start`/`stop`/`update` **self-elevate** (UAC `runas` on Windows, `pkexec`→`sudo` on Linux, `osascript`→`sudo` on macOS); with no GUI and no TTY they print the command and exit nonzero. `update <new-exe>` must be invoked **from the installed binary's own path**, pointing at the new build — the reverse renames the source aside as its own backup and fails mid-way, leaving the service stopped.

`run` self-detects SCM versus a console and branches internally: an `sc create`-registered binary must call `StartServiceCtrlDispatcherW` and report `SERVICE_RUNNING` within 30 s or SCM kills the start (error 1053).

## 4. Modules

| Module | Owns |
|---|---|
| `main.rs` | CLI; `init_tracing()` (stderr + daily-rolling file), token resolution, `AppState`, Axum start |
| `api.rs` | router, handlers, `auth_middleware` |
| `hardware.rs` | probe-rs: list, flash, reset; `resolve_probe`/`open_probe`; target-power pre-flight |
| `flash_backend.rs` | per-chip-family backend choice and vendor-tool discovery (decision 36) |
| `chip_resolve.rs` | Zephyr SoC → probe-rs chip target, validated against probe-rs's own registry |
| `serial.rs` | fixed-duration UART capture (not a stream) |
| `logs.rs` | `latest_log_file`/`tail_lines`/`FollowState`, one implementation behind the CLI and both HTTP routes |
| `dev_bench_log.rs` | the bench's own daily-rolling debug file, plus `classify()` and Core's boundary markers |
| `service.rs` | registration via `service-manager`; a `windows` submodule for the real SCM dispatch |
| `elevate.rs` | `is_elevated()`/`ensure_elevated_or_fallback()` |
| `token_store.rs` | resolves/generates/persists the machine-wide token file; `local_data_dir()` |
| `dev_bench_link.rs` | the serial transport: postcard+COBS encode/decode, open-per-study, all I/O in `spawn_blocking` |
| `study.rs` | `/study*` handlers, handshake, `study_lock`, in-memory job registry, host watchdog, `EventsJsonWriter`, the version gate, signal-tap reader threads |
| `stream_store.rs` | `streams/`, `index.json`, segment rotation, the keep-last-N sweep. Holds no column knowledge |

Board identity, enrollment, hardware-ID readback and dev-bench port detection are **not here**: they live in `embarch-topology`, which Core calls as `embarch_topology::hardware`.

## 5. Result layout

```
study_results/<study_id>/
├── events.json          the StudyResult: steps (with both time edges), provenance, streams
│                        written incrementally, `.partial` until StudyDone
└── streams/
    ├── index.json       per tap: id, name, files, encoding, alias, rendered, note
    ├── <tap>.bin        byte-for-byte what arrived — written first, always
    ├── <tap>.1.bin      the previous segment, after one rotation
    ├── <tap>.csv        the rendering, for Samples / GattTranscript / Struct
    ├── <tap>.txt        a Text tap: raw and rendering are the same bytes
    └── <tap>.arrival.csv  OutpostTrace only: frame_index,rx_utc_ms,frame_bytes
```

`named` and `timed` are two independent booleans in the index and on the wire — a trace can be named and untimed, or neither.

## 6. Constants and knobs

| Name | Value | Provenance |
|---|---|---|
| `WATCHDOG_GRACE_MS` | 10,000 | [measured 2026-08-27] 2,000 threw away a completed 300 s capture; the margin covers post-deadline flush backlog, which scales with how much the step captured — not link latency |
| `RESET_PULSE_MS` | 50 | [assumed] |
| dev-bench link baud | 1 Mbaud | [assumed] |
| `EMBARCH_SIGNAL_BAUD` | 1 Mbaud | [assumed] a `SignalLink` records where a signal goes, not how fast it talks |
| `EMBARCH_STREAM_MAX_BYTES` | 32 MiB, 2 segments | [assumed] |
| `EMBARCH_STUDY_RESULTS_KEEP` | 50 (`0` disables) | [assumed] |
| `MAX_UNDECODABLE_FRAMES` | 10 | [assumed] separates one lost frame from a noise stream |
| log retention | 7 daily files | [assumed] |
| `EMBARCH_FLASH_BACKEND` | — | forces a backend; forcing probe-rs onto a refused family logs a warning |
| `EMBARCH_JLINK_EXE` / `_NRFUTIL_EXE` / `_NRFJPROG_EXE` | — | vendor-tool overrides, searched after `PATH` and before default install dirs |
| `EMBARCH_TOKEN` | — | explicit env var wins over the machine-wide file |

Paths follow one convention: `%ProgramData%\embarch\` on Windows, `/var/lib/embarch/` elsewhere — token, `logs/core.log.<date>`, `logs/dev-bench.log.<date>`, `study_results/`, and `embarch-topology`'s `enrollment.toml`.
