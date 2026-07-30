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
- 2026-07-29 — Added Milestone 5 (Dev Bench Scoping): design-only scoping of `embarch-dev-bench`, resolved via Q&A directly into `embarch-dev-bench/design.md`. Not added to Rochambeau's includes list — no code shipped.
