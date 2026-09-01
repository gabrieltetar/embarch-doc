# embarch-core: milestone 1 — Flash

**Status:** done, 2026-08-11. Milestone 1 (Flash) is part of the shipped foundation ([embarch-roadmap.md](../embarch-roadmap.md) §1), released as `v0.1.0`.. Execution plan for [embarch-roadmap.md](../embarch-roadmap.md)'s Milestone 1. Companion to [embarch-api/milestone-1.md](../embarch-api/milestone-1.md) — that doc covers embarch-api's half of the same milestone. See [design.md](design.md) for the durable architecture record this plan folds decisions back into once they actually ship. For §3.5's `EMBARCH_TOKEN`/Windows-service open question specifically, [milestone-1-implementation-guide.md](milestone-1-implementation-guide.md) diagnoses the root cause and turns the fix into a ready-to-run agent prompt against the real source tree.

## 1. Goal, restated for Core

Milestone 1 exists to stop needing to forward the debug probe's USB device from Windows into WSL2 (today via usbipd-win) just to flash firmware built there. embarch-core's part: run natively on Windows, where the probe is already visible with no forwarding, and be reachable from WSL2 over HTTP so embarch-api (running in WSL2) can drive `/flash`/`/reset`/`/serial-log` against it. This is the deployment embarch-core's own README and `design.md` §7 already anticipated ("reachable from WSL2 if Core runs native on Windows") — milestone 1 is what actually stands that up against real hardware for the first time, rather than leaving it a documented intention.

## 2. Scope for this milestone

- **Board:** `project-a-board` (nRF54L15) only. `project-b-mkr` (STM32F446xx) follows the same steps as a fast-follow once this one works — not required for this milestone to be done.
- **Deployment:** Core built and run on Windows directly (not cross-compiled from WSL2) — the first Windows build of this codebase; only a Linux/WSL2 build has been confirmed so far (§3.1).
- Artifact transfer from WSL2's build output to Core is being solved via UNC-path pass-through (decided for this milestone — see [embarch-api/milestone-1.md](../embarch-api/milestone-1.md) §3.3); no change to Core's `/flash` request contract is needed for that.
- Out of scope: multi-probe selection, per-caller identity, ESP-IDF/`esptool` fallback — none of these are in the way of getting one nRF54L15 board flashing.

## 3. Steps

### 3.1 Confirm Core builds and runs natively on Windows — done (2026-07-21)

embarch-core has only ever been confirmed to build on Linux/WSL2 (release binary present at `embarch-core/target/release/embarch-core`, built 2026-07-17). A Windows build is new ground:

- Install a current stable Rust toolchain on Windows via `rustup` (not any bundled/other toolchain) — same MSRV constraint the README calls out for probe-rs's edition2024 baseline. **Confirmed insufficient on its own**: `rustup`'s bare stable-msvc toolchain has no linker. `cargo build --release` failed with `error: linker link.exe not found` until Visual Studio Build Tools' "Desktop development with C++" workload was installed (via the VS Installer GUI — CLI-driven `setup.exe modify` attempts failed silently, apparently because they couldn't get the UAC elevation the modify operation needs when invoked through WSL interop).
- `cargo build --release` from a native Windows shell (PowerShell or cmd), against a Windows-local checkout of this repo — not through a `\\wsl$` path, since building against a 9P-mounted source tree is slow and occasionally flaky. Clone or copy the repo to an actual Windows path first. **Done**: copied to `C:\Users\dev\source\repos\embarch-core` (no native checkout existed previously); release build succeeds there in ~3 minutes from a clean `Cargo.lock`.
- Confirm probe-rs's Windows USB backend picks up the probe at all (it's a different code path than Linux's libudev-based enumeration) — run the built `embarch-core.exe` and hit `/status` before going further. An empty probe list here is a Windows-driver problem to solve before anything else in this plan matters. **Confirmed**: `/status` returns the attached J-Link (S/N `112233445566`) on the first try, no additional driver setup needed.

### 3.2 Identify the physical probe and confirm its probe-rs target name — done (2026-07-21)

`embarch-api`'s `config.example.toml` has `chip = "nRF54L15_M33"` for `project-a-board` flagged as an unconfirmed placeholder. The board's `boards/nordic/board-a/board.cmake` (in `project-a-fw`) configures `jlink`, `pyocd`, and `nrfutil` runners today — no `openocd`/`stlink` — so the attached probe is almost certainly J-Link-class hardware (a standalone SEGGER J-Link, or the onboard debugger on a Nordic DK). On the Windows machine, with the probe plugged in:

```
probe-rs list
probe-rs chip list | grep -i nrf54
```

Confirm the exact chip target string probe-rs expects, and update `config.example.toml` (in the embarch-api repo) if it differs from the placeholder. This also proves probe-rs recognizes the probe over USB on Windows, ahead of (or alongside) §3.1's `/status` check.

**Confirmed**: `probe-rs list` shows the attached J-Link (`1366:1024:112233445566`). `probe-rs chip list` shows the nRF54L Series has exactly two variants, `nRF54L15` and `nRF54LM20A` — no `_M33` (or any core-variant) suffix exists in probe-rs's target database for this chip. The `nRF54L15_M33` placeholder was wrong; both `embarch-api/config.example.toml` and `config.toml` are updated to `chip = "nRF54L15"`.

### 3.3 Run Core in the foreground and validate all four endpoints manually — done (2026-07-21)

Before wiring embarch-api into the loop, prove Core itself works end-to-end against real hardware, isolated from every other moving part:

```
$env:EMBARCH_TOKEN = "some-long-random-string"
.\target\release\embarch-core.exe run
```

From WSL2 (see §3.4 for the address), exercise each endpoint with `curl` and a bearer token:

- `GET /status` — board-a's probe appears in the list.
- `POST /reset` — succeeds against the confirmed `chip` string (§3.2).
- `POST /flash` — first pass with a `firmware_path` copied manually onto the Windows machine, sidestepping the WSL2 artifact-transfer question entirely, to isolate "can Core flash this board at all" from "can Core reach a WSL2-built artifact."
- `GET /serial-log` — confirm the shell UART port name Windows assigns the board (`COM<N>`), and that a capture returns real console output.

**Confirmed, with two real findings along the way:**
- `GET /status`, `GET /serial-log` (port `COM5`, the J-Link CDC UART — returned an empty buffer in a 2s window with no active serial traffic, endpoint itself works), and `POST /reset` all succeeded from WSL2 on the first pass.
- `POST /flash` initially failed with an opaque `500 flashing failed` and **no detail anywhere** — not in the HTTP response, not in Core's log. Root cause: `api.rs`'s `internal_err` discarded the full `anyhow` chain via `Display`; fixed to use `Debug` and to log server-side too (`embarch-core/design.md` §4, §11). Once fixed, the real error was `An IO error has occurred while reading the firmware file. / The system cannot find the path specified.` — because the `firmware_path` sent was a WSL2 path (`/home/...`), meaningless to Core running on Windows. Flashing actually succeeded once a Windows-visible UNC path (`\\wsl.localhost\Ubuntu-24.04\...`) was used instead — see `embarch-api/milestone-1.md` §3.3 for how this gets wired automatically going forward, and this doc's §7 (deployment model, in `design.md`) for the durable record.
- The eventual successful `/flash` call was validated end-to-end against the physical board (probe-rs's page-by-page download log confirmed real programming, not a no-op), invoked via `embarch-api flash project-a-board --firmware-path <UNC path>` rather than a raw `curl` — see `embarch-api/milestone-1.md` §3.5.

### 3.4 Make Core reachable from WSL2 at a stable address — done (2026-07-21)

No `.wslconfig` exists on this machine today, so WSL2 is on default NAT networking — `localhost`/`127.0.0.1` from WSL2 does **not** reach a Windows-hosted service; WSL2 must use the Windows host's IP as seen from inside WSL2 (currently `172.29.64.1`, from `ip route show default` — this address is assigned per WSL2 session and can change across restarts). Two options, not mutually exclusive:

- **Use the dynamic IP directly.** Re-resolve it each session (`ip route show default | awk '{print $3}'`) and update embarch-api's `[core].base_url` when it changes. Zero setup, but brittle across reboots.
- **Enable WSL2 mirrored networking** (`%UserProfile%\.wslconfig`: `[wsl2]` / `networkingMode=mirrored`, then `wsl --shutdown` and restart). Makes `localhost` shared between Windows and WSL2, so `base_url` can just be `http://localhost:4884` permanently. Recommended one-time fix given how much this milestone leans on WSL2⟷Windows networking staying reliable — but it's an environment change outside either repo's code, worth confirming works on this Windows build/version before relying on it.
- Either way, confirm Core's bind address/port (`0.0.0.0:4884` default, per `main.rs`) is actually reachable through Windows Firewall from WSL2's virtual adapter — WSL2 traffic is sometimes categorized as a "Public" network profile by Windows Firewall, which would silently block inbound connections to Core.

**Confirmed, went with the dynamic-IP option for now (mirrored networking not tried):** `172.29.64.1` reached Core from WSL2 with zero Windows Firewall configuration needed. Turns out this machine's WSL networking uses the newer "WSL (Hyper-V firewall)" NAT mode (`vEthernet (WSL (Hyper-V firewall))`, distinct from the plain `vEthernet (WSL)` adapter older WSL2 versions use) — `Get-NetFirewallHyperVProfile` shows all three of its profiles (`Domain`/`Private`/`Public`) at `DefaultInboundAction: NotConfigured`, i.e. permissive by default, separate from the regular Windows Firewall profiles (which this machine's actual network adapters, Wi-Fi/NordLynx, are both categorized `Public` under — the concern this section originally raised). No `embarch-api` config or firewall change was needed beyond setting `base_url` to the resolved IP. The dynamic-IP fragility this section calls out is real and unaddressed — `base_url` will need updating after a WSL2/Windows restart; mirrored networking remains a reasonable follow-up if that friction becomes annoying, but wasn't necessary to unblock this milestone.

### 3.5 Install Core as a Windows service once validated

Once §3.3's manual foreground validation passes, switch Core to running unattended so nobody has to remember to start it every session:

```
# As Administrator:
.\target\release\embarch-core.exe install
```

`service-manager` registers it via `sc.exe` (already implemented, per `service.rs`/README — this milestone is its first real exercise on Windows). Confirm `EMBARCH_TOKEN` is actually available to the installed service: `sc.exe`-registered services don't inherit an interactive shell's environment variables, so the token set via `$env:EMBARCH_TOKEN` in §3.3 will likely not carry over. Verify this and, if it doesn't, resolve it (a service-level environment variable set through the Services console/`sc.exe`, or a small `service.rs` change) before treating the installed service as equivalent to the validated foreground run.

## 4. Definition of done

- `embarch-core.exe` runs on Windows (foreground or installed as a service) with the real probe attached. **Done for foreground; installed-service form not yet exercised (§3.5 remains open).**
- `/status` shows board-a's probe; the real probe-rs `chip` string is confirmed and recorded (§3.2). **Done.**
- `/flash`, `/reset`, `/serial-log` all succeed against the physical board-a board, called from WSL2 over the network (§3.4) — not just `curl localhost` on the Windows box itself. **Done** — `/flash` via `embarch-api flash`, `/reset`/`/serial-log`/`/status` via direct `curl`, all from WSL2 (§3.3).
- No USB forwarding (`usbipd attach`/`usbipd bind`) is involved anywhere in this path. **Confirmed** — `usbipd list` shows the J-Link's bus ID as "Not shared" throughout; Core reached it natively on Windows the whole time.

## 5. Open questions / risks carried into execution

- ~~Windows build of this codebase is unverified until §3.1 actually happens~~ — **resolved (§3.1)**: builds and runs, but only after installing the VS Build Tools C++ workload (a real prerequisite the original plan didn't call out — bare `rustup` is not enough).
- `EMBARCH_TOKEN` delivery to a `sc.exe`-registered service is untested (§3.5) — may need a small `service.rs` change if the naive approach doesn't carry the env var through. **Still open** — root cause now fully diagnosed (`milestone-1-implementation-guide.md` Prompt 1) but the fix has not been applied to `service.rs` yet; `environment: None` is still unconditional as of 2026-07-21.
- ~~Exact chip target string for the nRF54L15, and the exact `COM` port for the shell UART, are both unconfirmed~~ — **resolved (§3.2/§3.3)**: `nRF54L15`, `COM5`.
- ~~Windows Firewall behavior toward WSL2's virtual network adapter is unconfirmed~~ — **resolved (§3.4)**: no rule needed on this machine's WSL networking mode, though this is specific to the "WSL (Hyper-V firewall)" NAT mode and could differ on an older WSL2/Windows build.
- **New:** the `firmware_path` a WSL2-side caller sends must be a path Windows can open (a `\\wsl.localhost\<distro>\...` UNC form) — a plain WSL2 path silently fails with an I/O error that, until this session's `internal_err` fix, was completely invisible to the caller and to Core's own log (§3.3; durable record in `embarch-core/design.md` §4, §7).

## 6. Changelog

- 2026-07-20 — Initial draft, scoping Core's half of Milestone 1 (Flash).
- 2026-07-21 — Linked the new `milestone-1-implementation-guide.md` from the header — it diagnoses §3.5's `EMBARCH_TOKEN`/Windows-service gap (root cause confirmed against the pinned `service-manager` crate source: `sc.rs` never reads `ServiceInstallCtx.environment`, unlike `systemd.rs`/`launchd.rs`) and turns the fix into a ready-to-run prompt.
- 2026-07-21 — §3.1–3.4 validated against real hardware: Windows build succeeds (needs the VS Build Tools C++ workload), chip target confirmed `nRF54L15`, all four endpoints exercised from WSL2 against the physical board-a board, and WSL2⟷Windows reachability confirmed with no firewall changes needed on this machine. Found and fixed a real bug along the way (`api.rs`'s `internal_err` was discarding the full `anyhow` error chain — see `design.md` §4/§11) and a real gap (WSL2 paths aren't openable by a Windows-hosted Core; needs a `\\wsl.localhost\...` UNC path — see `design.md` §7 and `embarch-api/milestone-1.md` §3.3). §3.5 remains open: diagnosed but not yet fixed.
