# embarch-core: design

**Status:** draft, 2026-07-17. Written to document the existing `embarch-core` implementation — the design discussion that produced it happened as a chat, not a durable record; this file is meant to be that durable record going forward. Append changes to the Changelog (§11) rather than silently editing history above it.

## 1. Purpose and scope

`embarch-core` is the OS-level service that owns the debug probe (flash/reset) and the serial console log. It is deliberately the lowest layer in EmbArch: it has no idea the EmbArch API or Claude Code exist. It exposes four bearer-token-authed HTTP endpoints and holds the hardware connection so nothing else has to fight over the USB port.

embarch-core is **not**:
- Aware of "projects," toolchains, or build commands. It takes a bare `chip` / `firmware_path` / `format` per call — the concept of a named project with its own build config lives entirely in `embarch-api`.
- A build system. It flashes whatever file it's given; it never invokes `west`, `arduino-cli`, or anything else.
- Multi-tenant. It's one process, one hardware connection, one shared token, matching the single-engineer scope of the whole EmbArch stack (see `embarch-api/design.md` §3.1).

## 2. Architecture overview

```
embarch-api --HTTP+Bearer--> embarch-core --probe-rs/serialport--> hardware
                                    ^
                                    |
                         embarch-core CLI (same machine)
```

`embarch-core` is reached two ways: over HTTP by `embarch-api` (the normal Claude-Code-driven path), and directly via its own CLI (`main.rs`'s `run`/`install`/`uninstall` subcommands) for local operation and service management. Both paths converge on the same `hardware`/`serial` modules and the same `hw_lock` — there is no separate code path for "CLI mode."

## 3. Locked-in design decisions and rationale

1. **Language: Rust**, with **probe-rs used as a library, not shelled out to as a CLI.** Calling `probe_rs::flashing`/`probe_rs::probe` directly (rather than spawning a `probe-rs` binary) avoids subprocess/parsing overhead and gives typed errors (`anyhow::Context`) instead of scraping CLI output.
2. **HTTP framework: Axum.** Chosen for the same reason `embarch-api` also ended up in Rust (per its design doc) — one toolchain across the whole stack, plus Axum's `State`/middleware model maps cleanly onto the `AppState { token, hw_lock }` shape Core needs.
3. **Cross-platform service install via the `service-manager` crate.** `install`/`uninstall` register the same `run` command as a systemd unit on Linux or a Windows Service via `sc.exe` — one code path, OS detection handled entirely inside the crate (`service.rs`'s `manager()`), not hand-rolled per-OS logic.
4. **A single `hw_lock: Arc<Mutex<()>>` serializes all hardware access.** `/flash`, `/reset`, and `/serial-log` each acquire it for the duration of the call. This is what actually enforces "nothing else has to fight over the USB port" — without it, a CLI-triggered flash and an HTTP-triggered reset could race on the same probe.
5. **Bearer-token auth via Axum middleware, not "trust the local port."** Core may end up reachable over a real network (WSL2-to-Windows today, or a LAN if Core moves to a Pi — see §7), so an unauthenticated HTTP surface isn't acceptable even at single-engineer scale. The check is a plain exact-string compare against `EMBARCH_TOKEN` (`auth_middleware` in `api.rs`) — deliberately not OAuth or anything session-based, matching the single-user scope.
6. **Default bind address `0.0.0.0`, not `127.0.0.1`.** This is deliberate, not an oversight (`main.rs`'s CLI help text says so explicitly): the point of Core is to be reachable from WSL2 if Core runs native on Windows, or from the LAN if Core later moves to a Raspberry Pi. `--bind`/`--port` remain overridable.
7. **Blocking hardware calls always run through `tokio::task::spawn_blocking`.** `probe-rs` and `serialport` are synchronous APIs; every handler in `api.rs` wraps its hardware call in `spawn_blocking` so a slow flash or a serial read with a multi-second `duration_ms` never stalls the Tokio runtime's async executor.

## 4. Endpoint reference

All routes require `Authorization: Bearer <token>` (see §6).

| Method | Path | Body / Query | Response |
|---|---|---|---|
| `GET` | `/status` | — | `{ status: "ok", probes: [ProbeInfo] }` — every debug probe probe-rs currently sees over USB (ST-Link, J-Link, CMSIS-DAP, FTDI, ESP USB-JTAG, etc). |
| `POST` | `/flash` | `{"chip": "...", "firmware_path": "...", "format": "elf"}` | `{ flashed: true, chip }` |
| `POST` | `/reset` | `{"chip": "..."}` | `{ reset: true }` |
| `GET` | `/serial-log` | `?port=...&baud=115200&duration_ms=2000` | `{ port, lines: [String] }` |

`chip` is an opaque probe-rs target name (e.g. `STM32F407VG`, `nRF52840_xxAA`, `esp32c3`) — Core does not validate it beyond whatever `probe.attach()` itself rejects. `format` is one of `elf` / `bin` / `hex` / `uf2` / `idf`, parsed by `hardware::parse_format`; an unrecognized value is rejected with an explicit error rather than silently defaulting. `firmware_path` is read from Core's own local disk — the caller is responsible for getting the file onto whatever machine Core runs on (see §7).

Handler errors return `(StatusCode::INTERNAL_SERVER_ERROR, String)`, rendered by Axum as a **plain-text body**, not JSON — callers (embarch-api's `core_client.rs`) must parse JSON only on 2xx and read non-2xx bodies as plain text. The `String` is the full `anyhow` error chain (`format!("{e:?}")` in `internal_err`, `api.rs`), not just the outermost `.context(...)` message — an earlier version used `Display` (`{e}`), which silently dropped every underlying cause (e.g. a real probe-rs I/O error collapsed to the single word "flashing failed"). `internal_err` also logs the same chain server-side via `tracing::error!` before returning it, so a failure is visible in Core's own log even if the caller never surfaces the response body. Found and fixed during milestone-1 §3.3 hardware validation, when a genuine `/flash` failure (a WSL2 path Core's Windows process couldn't open) was completely undiagnosable from either the HTTP response or Core's log until this was fixed.

## 5. Hardware access details

- **Single-probe assumption.** `open_first_probe()` in `hardware.rs` takes the first probe-rs finds via `Lister::list_all()`. Correct at single-board scope; the moment a second probe is attached, this is the one function that needs to grow a selector (most likely by serial number, which `ProbeInfo` already surfaces via `/status`).
- **Probe attach is per-call, not held open.** Each `flash`/`reset` call opens the probe, attaches to the target `chip`, does the operation, and lets the session drop — there's no persistent probe connection held across requests. This trades a little latency per call for not having to reason about a stale/broken persistent session.
- **`hw_lock` scope.** The mutex guard is held for the entire handler body (`_guard = state.hw_lock.lock().await`), so a `/flash` in progress blocks a concurrent `/reset` or `/serial-log` from starting, rather than just serializing at the probe-rs call level.
- **Serial log is a fixed-duration capture, not a stream.** `serial::read_log` opens the port, reads in a poll loop with a 200ms per-read timeout until `duration_ms` elapses, then returns the accumulated lines. There's no long-lived streaming/subscription endpoint — each call is a bounded snapshot.

## 6. Security model

Auth is a single shared secret, `EMBARCH_TOKEN`, checked via exact-string comparison in `auth_middleware` against every request's `Authorization` header. The value itself comes from `token_store::resolve_token()` (called from `main.rs`'s `run()`): an explicit `EMBARCH_TOKEN` env var wins if set; otherwise the machine-wide token file (`token_store.rs`, §8) is reused if present, or generated and persisted on first startup. Full lifecycle (generation, storage, transport, rotation, threat model, known gaps) is documented in [embarch-token.md](../embarch-token.md) rather than here — that includes the no-per-caller-identity limitation. The insecure `dev-token-change-me` fallback this replaced is gone entirely (milestone-2, §11).

## 7. Deployment model

**Confirmed via milestone-1 (2026-07-21):** `embarch-core` runs natively on Windows (built with `cargo build --release` against a native Windows checkout — a `\\wsl$`-mounted source tree was deliberately avoided, per the milestone plan), reachable from a WSL2 guest via the `0.0.0.0` bind at the WSL2 session's dynamic host-gateway IP (`ip route show default` from inside WSL2 — `172.29.64.1` on this machine, expected to change across WSL2 restarts). Windows Firewall did not need an explicit inbound rule: this machine's WSL networking mode is the newer "WSL (Hyper-V firewall)" NAT, whose `Get-NetFirewallHyperVProfile` profiles default to `DefaultInboundAction: NotConfigured` (permissive) rather than the regular Public-profile Windows Firewall (which the host's other network adapters were categorized as, and which would likely have blocked an unsolicited inbound connection). Building natively on Windows required installing Visual Studio Build Tools' "Desktop development with C++" workload for `link.exe` — a bare `rustup`-installed toolchain alone is not sufficient, since only the MSVC target ships without a bundled linker.

**Anticipated move: a LAN-reachable Raspberry Pi.** The `0.0.0.0` default bind and the CLI's cross-platform service install already anticipate this — no code changes should be needed to point Core's HTTP server at a Pi and reach it over the LAN.

**Artifact-transfer gap, shared with embarch-api's design doc §9 — closed for the WSL2-same-PC case, still open in general.** `/flash`'s `firmware_path` is read from Core's own local disk, so a WSL2-built artifact's path is meaningless to a Windows-hosted Core. For this specific topology (Core on Windows, build in WSL2, same physical machine), embarch-api's `artifact_path_for_core` config field (embarch-api/design.md §4) closes the gap by sending Core the artifact's `\\wsl.localhost\<distro>\...` UNC form instead — confirmed working end-to-end during milestone-1 (a real `west`-built `.hex` flashed onto the physical nRF54L15 board via this path). This does **not** generalize to Core running on a genuinely separate machine (e.g. a future Pi deployment) — that case still has no mechanism to get the artifact's bytes onto Core's filesystem, and remains embarch-api/design.md §9/§12's open gap to solve (multipart upload to `/flash`, a shared network mount, or an explicit push-artifact step). Core's contract (`firmware_path` is a local path) doesn't need to change for any of those solutions.

## 8. Module layout

```
src/
├── main.rs        — CLI (clap): `run`, `install`, `uninstall`; resolves the token via token_store, builds AppState, starts Axum
├── api.rs         — Axum router, handlers, bearer-token auth middleware
├── hardware.rs    — probe-rs: list probes, flash, reset
├── serial.rs      — serialport: read the UART console log
├── service.rs     — service-manager: register/remove as a background OS service
└── token_store.rs — resolves/generates/persists the machine-wide EMBARCH_TOKEN file (embarch-token.md §3.1)
```

## 9. Relationship to embarch-api

Core has zero knowledge of embarch-api, MCP, Claude Code, or the concept of a "project" — it only ever sees the four endpoints' bare parameters (`chip`, `firmware_path`, `format`, `port`, `baud`, `duration_ms`). Every project-name-to-config mapping, build orchestration, and MCP tool surface lives entirely in `embarch-api` (see `embarch-api/design.md`). The embarch-core CLI is a second, independent caller of the exact same HTTP API used by embarch-api — not a privileged or special code path — which is why `install`/`uninstall` just point the OS service manager back at the same `run` subcommand rather than needing separate service-mode logic.

## 10. Open questions / future work

- **No ESP-IDF UART-bootloader flashing.** probe-rs's `Format::Idf` covers some ESP flashing via USB-JTAG, but the classic UART bootloader path most ESP-IDF workflows use isn't covered. The planned escape hatch is an `esptool` subprocess fallback in `hardware.rs`, not yet implemented.
- **No multi-probe selection.** `open_first_probe()` takes the first probe-rs finds. Fine at single-board scope; the moment a second probe is attached, this is the one function that needs a serial-number selector (see §5).
- **`EMBARCH_TOKEN` is a single shared static token, not per-caller credentials.** Tracked as an open question in [embarch-token.md](../embarch-token.md) §8, which is the source of truth for the token's full lifecycle — see §6 above.
- **The `sc.exe`-installed-Windows-service environment gap (milestone-1 §3.5) has a fix applied in code (milestone-2, §11) but not yet validated on real Windows hardware** — `service.rs`'s `install()` now writes the `Environment` registry value via `winreg` when an explicit `EMBARCH_TOKEN` is set, but this couldn't be exercised on the Linux machine the change was written on. Needs confirming on the real Windows box per `milestone-2.md` §3.5 before this is considered closed.

## 11. Changelog

- 2026-07-17 — Initial draft, written to document the existing embarch-core implementation.
- 2026-07-20 — Moved from `embarch-core-design.md` (repo root) to `embarch-core/design.md` as part of the embarch-doc per-sub-project restructure; no content changes.
- 2026-07-21 — Milestone-1 hardware validation (§3.1–3.4): confirmed the native-Windows build (requires the VS Build Tools C++ workload, not just `rustup`'s bare toolchain), confirmed the real probe-rs chip target is `nRF54L15` (not the `nRF54L15_M33` placeholder), validated `/status`/`/serial-log`/`/reset`/`/flash` against the physical board-a board from WSL2, and confirmed WSL2⟷Windows reachability needs no explicit Windows Firewall rule on this machine's networking mode (§7). Also fixed a real bug found during this validation: `api.rs`'s `internal_err` used to discard the full `anyhow` error chain via `Display`, returning/logging only the outermost context string — now uses `Debug` and logs server-side too (§4). §3.5 (`EMBARCH_TOKEN` surviving an installed Windows service) remains open — diagnosed, not yet fixed (§10).
- 2026-07-21 — Milestone-2 (§3.1–3.4, code-side): removed the `dev-token-change-me` fallback entirely and added `token_store.rs` (§6, §8), implementing `resolve_token()`'s explicit-env-var-else-reuse-or-generate-machine-wide-file precedence, with `chmod 600` on Unix and an `icacls`-based ACL restriction on Windows. Applied the previously-diagnosed `sc.exe` service-environment fix to `service.rs`: `install()` now passes `ServiceInstallCtx.environment` through when an explicit `EMBARCH_TOKEN` is set (fixing Linux/macOS via `systemd.rs`'s existing handling) and writes the Windows `Environment` registry value via `winreg` (§10). `cargo build`/`cargo clippy --all-targets -- -D warnings` clean; `token_store`'s generate/reuse/permission behavior and the explicit-env-var path were exercised on this Linux machine (`/var/lib/embarch` itself isn't writable unprivileged here, so generate/reuse was verified against a temp-path unit test rather than the real path). The Windows ACL code and the Windows registry-write code are unverified — need real Windows hardware validation (`milestone-2.md` §3.5, §10 above).
