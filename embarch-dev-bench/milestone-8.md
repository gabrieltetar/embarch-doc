# embarch-dev-bench: milestone 8 — Dev Bench Self-Test

**Status:** closed 2026-08-20 (draft 2026-08-18; target board retargeted 2026-08-19, see §2, §6a). Every DoD item is done except §3.6's bond-clearing specifically. Execution plan for [embarch-roadmap.md](../embarch-roadmap.md)'s Milestone 2 ("Dev Bench Self-Test" — filed on disk as `milestone-8`). Companion to [embarch-core/milestone-8.md](../embarch-core/milestone-8.md) (Core's `study.rs` half) and [embarch-api/milestone-8.md](../embarch-api/milestone-8.md) (the `run_study`/`study_status` surface used to drive this milestone's validation). See [design.md](design.md) §3 decisions 8/20/21/25/26 for the durable decisions this doc closes out.

## 1. Goal, restated for dev-bench

`design.md`'s own status line still reads "never run on a physical board — no hardware has been flashed," six weeks after `workspaces/nordic` first compiled cleanly (2026-08-04). This milestone is the first real flash of this firmware onto physical hardware, and closes two decisions that were deliberately left ahead of implementation to unblock exactly this:

- **Decision 21** — `main.c` moves from a fixed demo sequence to real per-`Study` dispatch: on `StudyStart`, validate `steps_crc` (decision 19), dispatch each `Step` through the existing `ble_bridge_real.c` `Action`/`GattOperation` surface (already implemented, decision 16's implementation note — just never run for real), sending `StepResult` after each and `StudyDone` at the end.
- **Decision 8**, closed now rather than deferred (design-questions scope decision, 2026-08-18): the `embarch-study-designer` Rust staticlib gets real west-module wiring and cross-compilation for the nRF54L15 target, so `study_ffi.c` calls the real crate instead of decision 20's stub. This is the bigger of the two — it's the same nRF54 cross-compilation toolchain gap `embarch-study-designer/design.md` §7 has tracked since that crate's own milestone, unstarted until now.

## 2. Scope for this milestone

- **Board: ESP32-C5-WROOM-1 DK (`esp32c5_devkitc/esp32c5/hpcore`), `workspaces/espressif` only** — retargeted 2026-08-19 (§6a) from the original nRF54L15DK/`workspaces/nordic` scope: the nRF54L15DK broke, its RMA replacement never arrived, and the ESP32-C5 (originally only an interim substitute, `design.md` decision 26) had already validated this milestone's entire dispatch/handshake/study mechanism end to end, so this milestone's own scope moved to it rather than staying blocked on hardware that was never coming back in time. `workspaces/native_sim` stays as a host-side sanity check (re-run to confirm no regression, §3.1); `workspaces/nordic` is no longer this milestone's target — see `design.md` decision 4's amendment.
- **No DUT, no BLE connect, no power sampling.** Per the roadmap's own framing ("No client/DUT repo involved... Power sampling is explicitly out of scope"), the self-test `Study` uses **`BleAdvertise`-only steps** (design-questions scope decision, 2026-08-18): dev-bench advertises as a peripheral, bounded by each step's own `timeout_ms`, with no requirement that anything connects to it. This exercises the radio (a real peripheral) and the full dispatch/result path without needing a second BLE device, a real DUT, or power-sampling hardware that doesn't exist yet (decision 24, PPK2 still unacquired).
- **Self-test fixture:** a new `self_test_study.json`, checked into this repo (the capability it validates) rather than `embarch-api` or `embarch-core` — two steps, illustrative shape below (exact `heapless` capacity limits per `embarch-study-designer/design.md` §3 decision 15 apply; `steps_crc` is omitted and auto-filled by `embarch-api`'s `run_study` per that crate's decision 26):

  ```json
  {
    "name": "dev-bench-self-test",
    "steps": [
      {
        "name": "advertise-short",
        "action": { "BleAdvertise": { "local_name": "embarch-selftest", "service_uuids": [], "adv_interval_ms": 100 } },
        "timeout_ms": 3000,
        "power_sample": null,
        "continue_on_fail": false
      },
      {
        "name": "advertise-longer",
        "action": { "BleAdvertise": { "local_name": "embarch-selftest-2", "service_uuids": [], "adv_interval_ms": 500 } },
        "timeout_ms": 5000,
        "power_sample": null,
        "continue_on_fail": true
      }
    ],
    "validations": []
  }
  ```

  Two steps specifically so `StepResult`/`StudyDone` round-tripping (the roadmap's own DoD language) is actually exercised as a sequence, not a single-step edge case; `continue_on_fail: true` on the second step is deliberate so the self-test still reaches `StudyDone` even if `BleAdvertise` semantics turn out to report something other than a clean `Pass` (§5).
- **Out of scope:** GPIO/analog stimulus (`design.md` §1, no `Action` variant exists), a DUT connector, a second vendor workspace, on-board status indication — all already-deferred per `design.md` §4.

## 3. Steps

### 3.1 Re-confirm `native_sim` and the `espressif` cross-compile still build clean — done

`west build -b native_sim app` and `west build -b esp32c5_devkitc/esp32c5/hpcore app` both confirmed building clean (§6a/`design.md` decision 26) — the `espressif` workspace's own first build, not a re-confirmation of prior drift the way this step originally described for `nordic`.

### 3.2 First real hardware flash — done

Flashed via `embarch-core`'s native ESP-JTAG support (`embarch-core/design.md` §3 decision 18), not a human-run `west flash` — decision 13's manual-flash default is reversed for exactly this board (`design.md` decision 13). Board enumerates as a plain USB Serial/JTAG device (a different VID than the nRF54L15DK's SEGGER J-Link, no VCOM) — `embarch-core/milestone-8.md` §3.1's SEGGER-VID auto-detection assumption doesn't apply here; port selection uses the `EMBARCH_DEV_BENCH_PORT` manual override instead (`design.md` decision 26, `embarch-core/milestone-8.md` §5 open question).

### 3.3 Close decision 8: west-module wiring for the Rust staticlib

Author `module.yml` for `embarch-study-designer` as a west-managed module (already listed as checked out under `workspaces/nordic/modules/` per §2's tree, decision 8's original text — the module *reference* exists, its *build wiring* doesn't); add the CMake custom command (`app/CMakeLists.txt`) invoking `cargo build --release --target <triple> --features ffi`; resolve the concrete `<triple>` for the nRF54L15's Cortex-M33 core (expected `thumbv8m.main-none-eabihf` pending confirmation against the actual installed Rust target list — `rustup target list`). This is the same gap `embarch-study-designer/design.md` §7 has open; closing it here closes it there too.

### 3.4 Swap `study_ffi.c` from the decision-20 stub to the real staticlib

Once §3.3's build wiring produces a linkable artifact, `study_ffi.c` calls the real `essd_study_decode_and_verify` (decision 19, `embarch-study-designer`'s `src/ffi.rs`) instead of returning fixed results — no interface change expected, per decision 20's own note, since the call signature was already dictated by the crate's FFI surface.

### 3.5 Implement decision 21's real per-`Study` dispatch in `main.c`

Replace the fixed demo sequence: on `StudyStart`, validate `steps_crc` via §3.4's real call (rejecting with whatever error path decision 19 specifies on mismatch); dispatch each `Step` in order through `ble_bridge_real.c`'s existing `Action`/`GattOperation` surface (already implemented for every action kind per decision 16's 2026-08-04 implementation note — this milestone is its first real-hardware exercise, not new BLE code); send `StepResult { step_index, result }` after each step completes; send `StudyDone { completed }` at the end or on an early stop via `continue_on_fail`.

### 3.6 First real-hardware `Hello`/`HelloAck` handshake — done (bond-clearing itself not separately confirmed)

Validated against `embarch-core/milestone-8.md` §3.2's handshake code — `Hello`→`HelloAck` succeeded for real (§6a). Decision 11's bond-clearing-on-`Hello` behavior was not separately exercised this pass (no reconnect/re-pair scenario was run to observe it) — code path unchanged from what already runs on `Hello`, but not directly observed firing on this board yet.

### 3.7 First real-hardware run of the self-test `Study` — done

Submitted via [embarch-api/milestone-8.md](../embarch-api/milestone-8.md)'s `run_study` against the fixture in §2 — `StepResult`(Pass)×2/`StudyDone{completed:true}` round-tripped end to end on physical hardware (§6a), closing the exact gap the roadmap names this milestone for.

### 3.8 Confirm the stale-firmware `doctor` check fires correctly — done

Decision 25's check compares `HelloAck.firmware_version` against the repo's own `git describe`. The check didn't actually exist in code yet — `embarch-umbrella`'s doctor only had twelve checks despite `design.md` §5's table already listing thirteen (a real doc/code drift, not just an untested check). Implemented for real: `embarch-core`'s new `GET /dev-bench/hello` endpoint (opens the link, runs `Hello`/`HelloAck`, reports `firmware_version`, closes — no `Study` involved) plus `embarch-umbrella`'s new doctor check 13, comparing that against `git describe --always --dirty --abbrev=8` on a configured `embarch-dev-bench` checkout. Live-validated both ways against the real ESP32-C5: committed the current milestone-8 work, flashed that build, made one further commit, and reflashed it — `doctor` `FAIL`ed naming both hashes while the older build was on the board, then `PASS`ed once the newer build was reflashed. Found and fixed a real bug along the way: `app/CMakeLists.txt`'s `git describe` `execute_process` only reruns when CMake reconfigures, and CMake doesn't treat "the commit checked out right now" as a tracked dependency by default — an incremental `west build` after a plain `git commit` was silently keeping the *previous* configure's stale `APP_FIRMWARE_VERSION`. Fixed via `CMAKE_CONFIGURE_DEPENDS` on the resolved `.git/HEAD`/ref/`index`. Also found: running the check from Windows against a WSL2 checkout over a `\\wsl.localhost\...` UNC path spuriously reports `-dirty` always (Windows' git can't read this repo's `app/` symlinks over that path) — not a check bug, just a reason `dev_bench_repo_path` needs to be a path native to whichever machine runs `embarch doctor` (on this suite's `wsl-host` topology, that means WSL2 itself).

## 4. Definition of done

**Status (2026-08-19/20): every item is now done for real against physical hardware except §3.6's bond-clearing specifically.** §3.1–3.2 and §3.5–3.8 all ran successfully on the real ESP32-C5, including §3.8's stale-firmware `doctor` check — implemented for the first time this pass and live-validated both ways (flash an old build → `doctor` `FAIL`s naming both hashes; reflash current → `PASS`).

- [x] `native_sim` and `espressif` builds both confirmed clean against current dependencies (§3.1).
- [x] Firmware flashed onto the physical ESP32-C5-WROOM-1 DK for the first time ever (§3.2).
- [x] Decision 8 closed: CMake-invoked `cargo rustc` wiring + resolved Rust target triple (`riscv32imac-unknown-none-elf`), producing a real linked staticlib in the `espressif` build (§3.3).
- [x] `study_ffi.c` calls the real crate, not the stub; `steps_crc` validated for real against a real payload (§3.4).
- [x] `main.c` dispatches a real multi-step `Study` end to end — `StepResult` per step, `StudyDone` at completion (§3.5).
- [ ] `Hello`/`HelloAck` handshake confirmed on real hardware (done); bond-clearing specifically not yet separately observed firing (§3.6).
- [x] The self-test `Study` (§2's fixture) runs successfully end to end via `embarch-api`'s `run_study`/`study_status`, against real hardware (§3.7).
- [x] Stale-firmware `doctor` check confirmed against a real flashed/reflashed board (§3.8).
- [x] `design.md`'s status line and decisions 8/20/21/25/26 updated to reflect real implementation, not design-only, per `DOC-PROTOCOL.md` §5.

## 5. Open questions / risks carried into execution

- ~~**Decision 8's cross-compile toolchain is the single biggest risk in this milestone.**~~ — resolved: the `espressif` workspace's own `riscv32imac-unknown-none-elf` target links cleanly (§6a, `design.md` decision 26); the analogous nRF54L15 question is moot now that this milestone no longer targets that board.
- ~~**`BleAdvertise`'s `Outcome` semantics with no connection attempted are unstated.**~~ — resolved empirically 2026-08-20: dev-bench reports `Pass` as soon as advertising starts, not after holding the step open for the full `timeout_ms` — confirmed repeatedly against the real ESP32-C5 (a 20-25 second `timeout_ms` still produced a terminal `"completed"` status within about a second of submission, both via the CLI and MCP paths). This is fast enough that it ruled out a live watchdog-lapse test via a human-timed physical USB unplug (`embarch-core/milestone-8.md` §3.4/§5) — there's no reaction-time window between `StudyStart` succeeding and the step's `StepResult` arriving. An independent confirmation signal (the PC running Core additionally scanning for the advertised device over its own Bluetooth adapter) remains a real idea worth having eventually, but is still OS-dependent code, explicitly deferred past this milestone.
- ~~**The J-Link multi-VCOM question.**~~ — moot for this milestone now that its target board is the ESP32-C5, which has no J-Link/VCOM at all (native USB Serial/JTAG instead, `design.md` decision 26); still a real open question if the nRF54L15DK is ever revisited (`design.md` §4, `embarch-core/design.md` §10).
- ~~**Rust target triple for nRF54L15 (§3.3) is a guess pending confirmation.**~~ — moot for this milestone; the ESP32-C5's own triple (`riscv32imac-unknown-none-elf`) is confirmed working, no ABI footgun found (`design.md` decision 26).
- ~~**`embarch-core`'s SEGGER-VID-based auto-detection doesn't apply to this board.**~~ — resolved 2026-08-19/20: `dev_bench.rs` now recognizes this board's own VID (`0x303A`, Espressif's registered USB VID, confirmed empirically against the real board's Windows enumeration) directly, alongside SEGGER's — see `embarch-core/design.md` §5/§10, `embarch-core/milestone-8.md` §5. `EMBARCH_DEV_BENCH_PORT` is no longer needed for this board.

## 6a. Board retargeted from nRF54L15DK to ESP32-C5 (2026-08-19)

In parallel, `design.md` decision 26 stands up a temporary ESP32-C5-WROOM-1 substitute board (`workspaces/espressif`) so this milestone's actual validation shape — real per-`Study` dispatch, `Hello`/`HelloAck`, a physical self-test `Study` completing — gets a real run on different silicon while waiting, rather than sitting idle. **Updated 2026-08-19/20: no longer build-level only.** `embarch-core/design.md` §3 decision 18 (reversing this doc's own decision 13) gave Core real ESP-JTAG flashing support, validated end to end: the ESP32-C5 was flashed, `Hello`/`HelloAck`'d, and ran the §2 self-test fixture for real — `StepResult`(Pass)×2/`StudyDone{completed:true}` — via `embarch-api`'s existing `run-study`/`study-status` CLI. A devicetree fix (console wiring pointed at unconnected header pins, not the USB-connected `usb_serial` node) and a DTR/RTS reset gotcha were found and the former fixed along the way (`design.md` decision 26's own text). This is real evidence the whole dispatch/handshake/study mechanism works against physical BLE hardware. **Retargeted 2026-08-19, same day:** rather than continue treating this as merely "tracked separately" while waiting on the nRF54L15DK's RMA replacement (which never arrived), this milestone's own scope and Definition of Done (§2, §4) were moved onto the ESP32-C5 — the board that actually ran the validation. The nRF54L15DK is no longer this milestone's target; a future re-run against it, if that board is ever revisited, would be new work, not a reopening of this milestone.

## 6. Changelog

- 2026-08-19/20 — **§3.8 (stale-firmware `doctor` check) closed — DoD now fully done except §3.6's bond-clearing specifically.** Implemented (`GET /dev-bench/hello` in `embarch-core`, doctor check 13 in `embarch-umbrella`) and live-validated both ways against the real board, surfacing and fixing a real CMake configure-dependency bug along the way. §5's SEGGER-VID and `BleAdvertise`-timing open items also resolved: `dev_bench.rs` now recognizes this board's VID directly, and `BleAdvertise` is confirmed to report `Pass` near-instantly (which is also why a live watchdog-lapse test via human-timed USB unplug wasn't achievable — see `embarch-core/milestone-8.md` §3.4/§5). Full detail in `design.md` decision 25's update and its 2026-08-19/20 changelog entry.
- 2026-08-19 — **Milestone retargeted: board scope (§2) and Definition of Done (§4) moved from the nRF54L15DK to the ESP32-C5-WROOM-1 DK.** The already-successful ESP32-C5 self-test run (§6a, below) now counts directly against this milestone's own DoD instead of being tracked as a separate, non-counting interim validation — §3.1/3.2/3.5/3.6/3.7 checked done; §3.6's bond-clearing specifically and §3.8 (stale-firmware `doctor`) remain open regardless of board. §5's nRF54L15-specific open questions (cross-compile risk, J-Link multi-VCOM, Rust target triple) are moot for this milestone now; a new open question recorded instead — `embarch-core`'s SEGGER-VID auto-detection doesn't cover this board's own VID, so port selection still relies on a manual override. Recorded as a decision reversal: [embarch-decision-reversals.md](../embarch-decision-reversals.md) row 13.
- 2026-08-19/20 — §6a updated: the ESP32-C5 interim substitute ran the §2 self-test fixture end to end for real (`embarch-core/design.md` §3 decision 18's new ESP-JTAG flashing support, reversing `design.md` decision 13) — `HelloAck`→`StepResult`(Pass)×2→`StudyDone{completed:true}`. This document's own Definition of Done (§4) is unaffected and stays entirely nRF54L15DK-scoped, per its own explicit §2 scope line.
- 2026-08-19 — New §6a: the physical nRF54L15DK broke (confirmed hardware fault, replacement ordered, ETA ~1 week), blocking §3.2 onward. This milestone's own nRF54L15DK-only scope and DoD are unchanged; `design.md` decision 26's interim ESP32-C5 substitute workspace is recorded as a parallel, separately-tracked build-level confirmation, not a scope change.
- 2026-08-18 — §3.3–3.5 implemented for real: decision 8's cross-compile/link (`thumbv8m.main-none-eabi`, soft-float — a real ABI gotcha found and fixed) and decision 21's real per-`Study` dispatch (`BleAdvertise`-only), verified end to end on `native_sim` against real Rust-encoder-produced bytes. `nordic` builds clean, not yet flashed onto real hardware. `design.md` updated to match (decisions 8/20/21, §4, new changelog entry). §3.1/3.2/3.6/3.7/3.8 (everything needing the physical board) remain.
- 2026-08-18 — Initial draft, scoping dev-bench's half of Milestone 2 (Dev Bench Self-Test): first-ever real hardware flash, closing decision 8 (Rust cross-compile/west-module wiring, brought into this milestone's scope rather than left deferred) and decision 21 (real per-`Study` dispatch) together, validated against a new `BleAdvertise`-only `self_test_study.json` fixture submitted via `embarch-api`'s `run_study`.
