# embarch: feature roadmap

**Status:** draft, 2026-07-20.

## Milestones

### 1 - Flash

Projects : API - Core
The goal is to use the EmbArch suite to flash the firmware to avoid having to forward the USB from windows to WSL2.
Ideally "west flash" can be used.
Steps : [embarch-api/milestone-1.md](embarch-api/milestone-1.md), [embarch-core/milestone-1.md](embarch-core/milestone-1.md)

### 2 - Token

Projects : API - Core
The goal is to replace the insecure `dev-token-change-me` fallback with an auto-generated, machine-wide token file Core persists and embarch-api discovers on its own — no more hand-copying `EMBARCH_TOKEN` between the two. Also folds in the already-diagnosed `sc.exe` Windows-service environment-variable fix. Full target design : [embarch-token.md](embarch-token.md).
Steps : [embarch-api/milestone-2.md](embarch-api/milestone-2.md), [embarch-core/milestone-2.md](embarch-core/milestone-2.md)

### 3 - Study Designer

Projects : Study Designer (new) - Core - API - Dev Bench
Design-only milestone (no code; repo now exists at [gabrieltetar/embarch-study-designer](https://github.com/gabrieltetar/embarch-study-designer), empty). The goal is to scope `embarch-study-designer`, a shared `no_std` Rust library defining the data types for hardware-in-the-loop studies of a DUT — BLE advertise/connect/data-exchange/validation plus power profiling, used for fuzz testing and dev-time automated unit/integration testing — compiled independently by `embarch-core`, `embarch-api`, and future `embarch-dev-bench` firmware. Full target design : [embarch-study-designer/design.md](embarch-study-designer/design.md).
Steps : [embarch-study-designer/milestone-3.md](embarch-study-designer/milestone-3.md)

### 4 - Study Designer Implementation

Projects : Study Designer
The goal is to actually implement `embarch-study-designer` per Milestone 3's design (`embarch-study-designer/design.md`): the crate now exists with its full type model, wire-format tooling (`steps_crc`, CSV rendering), schema versioning, and a `core-validation`-gated `SignalCheck` evaluator, all `#![no_std]` and tested. Not yet in scope: wiring `embarch-core`/`embarch-api` to actually depend on this crate (they don't yet), and `embarch-dev-bench` firmware itself, which remains the next step and stays blocked on real hardware existing (design.md §7).
Steps : none yet — implemented directly against `design.md` rather than a separately-planned execution sequence; add a `embarch-study-designer/milestone-4.md` if this needs its own execution plan later.

### 5 - Dev Bench Scoping

Projects : Dev Bench (new)
Design-only milestone (no code; repo now exists at [gabrieltetar/embarch-dev-bench](https://github.com/gabrieltetar/embarch-dev-bench), empty). The goal is to scope `embarch-dev-bench`, the Zephyr-based C firmware that plays the DUT's BLE counterpart and samples power during a `Study`, cross-vendor by design (one shared application spanning multiple vendor-specific west workspaces, not one board or one silicon vendor). Full target design : [embarch-dev-bench/design.md](embarch-dev-bench/design.md).
Steps : none yet — resolved via Q&A directly into `design.md` rather than a separately-planned execution sequence.

### 6 - Onboarding

Projects : Umbrella (new) - API - Core
The goal is to make the suite installable and usable by a firmware engineer who has never seen it — one archive to download, `embarch setup` to configure whatever topology their machine is, `embarch init` to integrate a firmware repo, and `embarch doctor` to say what's wrong. Introduces the sixth sub-project `embarch-umbrella` (binary `embarch`), whose central design point is that Core-as-an-autostarting-OS-service is what removes the need for a launcher at all, so umbrella owns setup and verification rather than process management. Also folds in `base_url = "auto"` in API (retiring the WSL2 gateway IP that goes stale on every WSL restart), `start`/`stop` in Core, and the first real release binaries the suite has ever had. Full target design : [embarch-umbrella/design.md](embarch-umbrella/design.md); the guide it has to satisfy : [embarch-user-guide.md](embarch-user-guide.md).
Steps : [embarch-umbrella/milestone-6.md](embarch-umbrella/milestone-6.md)

## Next

Not yet numbered milestones — the buckets [embarch.md](embarch.md) and [embarch-features.md](embarch-features.md) refer to as "Next".

- **Dev-bench on real hardware.** `embarch-dev-bench`'s firmware builds for the nRF54L15DK but has never been flashed or run on a board, and `embarch-core`'s dev-bench port auto-detection has never met a real J-Link ([embarch-dev-bench/design.md](embarch-dev-bench/design.md) §4, [embarch-core/design.md](embarch-core/design.md) §10). Everything downstream of that — the `/study*` endpoints, `run_study`/`study_status`, power-sampling hardware, the stimulus/sensing rig — is blocked behind it.
- **`embarch-core`/`embarch-api` actually depending on `embarch-study-designer`** as a Cargo dependency; today all three define or assume the study types independently ([embarch-study-designer/design.md](embarch-study-designer/design.md)).
- **`embarch-promptu`** — the curated library of firmware-specific skills, subagents, and prompt patterns. Planned, no repo ([embarch-promptu/design.md](embarch-promptu/design.md)).

## Later

- **EmbArch UI.** A small local UI where an engineer sees whether Core is up and drives `embarch-api`'s operations by hand, without asking an agent and without typing CLI subcommands. Out of Milestone 6's scope, but Milestone 6's `--json` output on `embarch status`/`doctor` exists to be its data source ([embarch-umbrella/design.md](embarch-umbrella/design.md) §10).
- **Core on a Raspberry Pi, reachable over the LAN.** Detected and verified as of Milestone 6, but flashing from a separate machine stays blocked on the artifact-transfer gap (`embarch-api/design.md` §9), and cross-machine token distribution stays manual (`embarch-token.md` §8). A deliberately late milestone.
- **macOS validation.** Milestone 6 ships macOS support reasoned-only, with no machine to test on; validating it means a Mac-only engineer walking the user guide.
- **`embarch-atlas`** — static analysis and graph visualization of a firmware codebase, for agents and engineers. Paused, no repo (see [embarch.md](embarch.md) §2).

## Release

### 1 - Rochambeau
1.x.x
Date : ?
includes : 
Milestone 1
Milestone 2

## Changelog

- 2026-07-20 — Initial draft, Milestone 1 (Flash).
- 2026-07-21 — Added Milestone 2 (Token); added it to Rochambeau's includes list.
- 2026-07-27 — Added Milestone 3 (Study Designer): design-only scoping of `embarch-study-designer`, a new shared library sub-project. Not added to Rochambeau's includes list since this milestone ships no code.
- 2026-07-28 — Milestone 3 substantially closed (`embarch-study-designer/milestone-3.md` §3.1–3.5, most of §3.6): data model, wire format, Core endpoint surface, and result storage all resolved; repo created (empty). Only the nRF54 cross-compilation toolchain/build-wiring question remains, blocked on real dev-bench hardware.
- 2026-07-28 — Milestone 3 further closed (`embarch-study-designer/milestone-3.md` §3.7–3.8): the crate's data types now use fixed-capacity `heapless` collections rather than assuming a heap allocator on dev-bench firmware, and `embarch-api`'s future `run_study`/`study_status` tool/CLI names and param shapes are locked in ahead of implementation. Still only the nRF54 cross-compilation toolchain/build-wiring question (§3.6) remains open, blocked on real dev-bench hardware. Still not added to Rochambeau's includes list — no code shipped.
- 2026-07-29 — Added Milestone 4 (Study Designer Implementation): `embarch-study-designer` now has real, tested code implementing Milestone 3's design. Not added to Rochambeau's includes list yet — `embarch-core`/`embarch-api` don't consume it as a dependency yet, and `embarch-dev-bench` firmware (the next step) hasn't started.
- 2026-08-05 — Added Milestone 6 (Onboarding): the new `embarch-umbrella` sub-project plus `base_url = "auto"` in API, `start`/`stop` in Core, the suite's first release binaries, and the rewritten user guide. Also added the **Next** and **Later** buckets this file was missing entirely — [embarch.md](embarch.md) §2 and [embarch-features.md](embarch-features.md) already referred to "`embarch-roadmap.md`'s Later bucket" and "`embarch-roadmap.md` Next" as if they existed, so those were dangling cross-references (`DOC-PROTOCOL.md` §5). Not added to Rochambeau's includes list yet — no code shipped.
- 2026-07-29 — Added Milestone 5 (Dev Bench Scoping): design-only scoping of `embarch-dev-bench`, resolved via Q&A directly into `embarch-dev-bench/design.md`. Not added to Rochambeau's includes list — no code shipped.
