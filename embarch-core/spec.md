# embarch-core: spec

**Status:** active, 2026-09-02.

What is true now. Why: [decisions.md](decisions.md). Unresolved: [open.md](open.md). HTTP surface **and the on-disk result layout**: [interfaces.md](interfaces.md).

## 1. What it is

The OS-level service that owns the debug probe (flash/reset), the DUT's USB bootloader (bootload, decision 77), the DUT serial console, and the `embarch-dev-bench` serial link. It is the lowest layer in EmbArch and has no idea `embarch-api` or Claude Code exist. It exposes a bearer-token-authed HTTP API and holds the hardware connections so nothing else fights over a USB port.

It is **not**: aware of projects, toolchains, or build commands (it takes a bare `chip`/`firmware_path`/`format` per call); a build system — it never invokes `west` or `arduino-cli`, `embarch-api` sequences check → build → flash → submit, and decision 36 is the one exception, where Core *delegates* to a vendor flasher; or multi-tenant (one process, one hardware connection, one shared token).

```
embarch-api --HTTP+Bearer--> embarch-core --probe-rs/serialport--> DUT hardware
                                  ^  |
                                  |  +--serial, COBS-framed postcard--> embarch-dev-bench
                                  |  +--serial, read-only-------------> a DUT signal wire (outpost)
                     embarch-core CLI (same machine)
```

Reached two ways — over HTTP by `embarch-api`, and by its own CLI (`run`/`install`/`uninstall`/`start`/`stop`/`update`/`detect-dev-bench`/`chip-list`/`flash-backend`/`logs`/`dev-bench-logs`). Both converge on the same modules and the same `hw_lock`; there is no separate "CLI mode" code path.

## 2. Invariants

- **Every route requires `Authorization: Bearer <token>`**, no exceptions — and "every" is asserted mechanically: the test sweep derives its route list from `build_router`'s own source, so a route added without an auth case fails the build rather than shipping open (decision 42). One shared secret, exact-string compared in `auth_middleware`, resolved from `EMBARCH_TOKEN` and otherwise from the machine-wide file, generated and persisted on first startup. No per-caller identity and no TLS; full lifecycle, threat model and known gaps: [embarch-token.md](../embarch-token.md).
- **One `hw_lock` serialises all hardware access**, held for the whole handler body. **A second caller waits up to 500 ms for the first to finish; past that it is refused `503` naming the route holding the lock** (decision 14, built `tasks/core/013`) rather than queueing silently and indefinitely — an unbounded wait is indistinguishable from Core being unresponsive, which is the failure decision 14 exists to rule out. A separate `study_lock` serialises studies and `GET /dev-bench/hello`'s handshake, and the dev-bench identity gate takes `hw_lock`; a signal tap's read-only port takes neither, but registers the port it holds so `/bootload` refuses it by name.
- **Every blocking hardware call runs in `tokio::task::spawn_blocking`.** `probe-rs` and `serialport` are synchronous.
- **Probe attach is per-call, never held open.** Open, attach, operate, drop.
- **A background capture holds its own port, never `hw_lock`** (decision 92): `/signals/{name}/capture` records one declared signal while flash, reset and other signals' exchanges run; an exchange on the captured signal goes through its open handle.
- **A live bench lease gates every hardware route** (decision 93): without its token in `X-Embarch-Lease` a request is `409` naming holder, purpose, start and expiry; with none live, nothing changes. Expiry is lazy; the lease is in memory.
- **Identity fails closed.** Before touching hardware, the resolved probe's serial must be enrolled and its live hardware ID must match what was recorded. Unenrolled or mismatched blocks the operation; never a guess.
- **Ambiguity fails loudly.** More than one probe with no `probe_serial`, or more than one dev-bench port candidate, is a named error listing every candidate — never a silent pick.
- **Raw bytes are written before any decode is attempted.** A failed decode costs a rendering, never a capture.
- **A refusal renders nothing rather than guessing.** A manifest that does not verify costs the *names* in a trace, not the trace; an unverifiable time join stamps nothing.
- **Core keeps no persisted "current firmware" record.** A manifest binding lives only as long as the study that made it. Write-ahead state that can go stale is the pattern this suite forbids.
- **`GET /status` says which build answered.** `core_version` is compiled in from `CARGO_PKG_VERSION`, so a caller learns the deployed binary's version **over HTTP** without running it. Consumers **warn** on a skew, never refuse (decision 13). There is no hand-bumped `contract_version` beside it.
- **Errors are plain text on every non-2xx except `POST /validate`**, so outside that one route an error's *kind* is only its HTTP status. `/validate` renders a `TopologyMismatch` as JSON with a `kind` field on both its `409` and its `503` (decision 59); details: [interfaces.md](interfaces.md). The designed `{code, message, cause}` body for every route is deferred as cross-repo work (decision 12).
- **Default bind is `127.0.0.1`.** Widening is `embarch-umbrella setup`'s job, per detected topology.

## 3. Deployment

**An installed, autostarting OS service is the normal deployment** — that is what makes the rest of the suite need no launcher: if Core is up at boot, `embarch-api` always finds it running. A foreground `run` is fully supported and is the right choice for debugging Core itself.

Runs natively on Windows, reachable from WSL2 at the session's dynamic host-gateway IP. Windows Firewall needs no inbound rule under the newer Hyper-V-firewall WSL networking mode. Building natively on Windows needs Visual Studio Build Tools' "Desktop development with C++" workload for `link.exe` — a bare `rustup` toolchain is not enough.

`install`/`uninstall`/`start`/`stop`/`update` **self-elevate** (UAC `runas` on Windows, `pkexec`→`sudo` on Linux, `osascript`→`sudo` on macOS); with no GUI and no TTY they print the command and exit nonzero. `update <new-exe>` must be invoked **from the installed binary's own path**, pointing at the new build — the reverse renames the source aside as its own backup and fails mid-way, leaving the service stopped.

`run` self-detects SCM versus a console and branches internally: an `sc create`-registered binary must call `StartServiceCtrlDispatcherW` and report `SERVICE_RUNNING` within 30 s or SCM kills the start (error 1053).

## 4. Modules

The module table is in [interfaces/modules.md](interfaces/modules.md): one row per source file and what it owns.

Board identity, enrollment, hardware-ID readback and dev-bench port detection are **not here**: they live in `embarch-topology`, which Core calls as `embarch_topology::hardware`. **The identity gate is chip-aware** (decision 89): `flash`, `reset` and memory reads pass the requested chip, and a probe enrolled for another chip is refused `409 chip-mismatch` before it is opened.

## 5. Constants and knobs

Split into [interfaces/constants.md](interfaces/constants.md) on 2026-09-09
(`tasks/core/030`) when this file reached its size cap — every value, its
`[measured]`/`[assumed]` tag and its provenance note moved verbatim, nothing
cut. That file also has the on-disk path convention (`%ProgramData%\embarch\`
on Windows, `/var/lib/embarch/` elsewhere).
