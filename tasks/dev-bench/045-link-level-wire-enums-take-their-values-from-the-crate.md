# 045 — The link-level wire enums take their values from the crate

**State:** claimed by agent/dev-bench/045-link-level-wire-enums-take-their-values-from-the-crate, 2026-11-10 04:48 (toolchain, supervisor's own hands)
**Source:** `dev-bench/010` (landed 2026-11-10, `embarch-dev-bench` `759c402`), whose decision 56 covered the `.eap` enums only and says so
**Issue:** EMB-132
**Scope:** dev-bench
**Hardware:** toolchain — this repo's Zephyr tree is gitignored, so a worktree cannot build it (`tasks/README.md`, Hardware field). Build from the worktree against the main checkout's `workspaces/*` with the fleet's `west` at `/home/gabriel/Github/embarch/.west-venv/bin/west`, as `dev-bench/010` did.
**Owner:** no

## What

`embarch-dev-bench` decision 56 added `app/cmake/gen_crate_limits.py`, which writes `crate_limits.h` at configure time: every `usize` const in the crate's `src/limits.rs`, and for each enum in its `ENUMS` table each variant's declaration index (postcard's wire value) plus a `_COUNT`. `ENUMS` lists six `.eap` enums. Every other C enum whose values are a Rust enum's postcard index is still typed 0, 1, 2… by hand under a "Mirrors `X`" comment, so a variant inserted anywhere but the end of the Rust enum renumbers the wire while the bench decodes with the old table.

The hand-mirrored ones, by their Rust names: `DevBenchMessage` (the C message tag), `Action` and `SecurityLevel` and `DevBenchLogLevel` (`src/study.rs`), `GattDirection` and `GattEventKind` (`src/gatt.rs`, mirrored in both `app/src/serial_protocol.h` and `app/src/ble_bridge.h`), `Unit` (`src/sample.rs`), and the stream source and scope tags (`src/streams.rs`). Read each one before adding it: a C enum whose values are not the Rust declaration order, or that carries a value the Rust enum does not, needs its own reading rather than a mechanical row.

Direction, from the issue: one `ENUMS` row per enum, its source file added to `app/cmake/crate_limits.cmake`'s configure-time inputs, and the C enum's values taken from the generated macros with a `_COUNT` assert, the way decision 56 did for `eap.h`.

## Why now

Decision 56 landed today and names this as what it did not cover. These are the enums every message on the link crosses, so they are the ones where a silent renumbering costs most.

## Done when

- [ ] Every C enum in `app/src/serial_protocol.h` and `app/src/ble_bridge.h` whose values are a Rust enum's postcard index takes them from `crate_limits.h` and asserts the variant count; any that cannot is named in the decision with the reason.
- [ ] Both bench images (`nrf54l15dk/nrf54l15/cpuapp`, `esp32c5_devkitc/esp32c5/hpcore`) and the `native_sim` app build, and `app/tests/serial_protocol` passes on `native_sim`.
- [ ] Decision 56's "Not covered" sentence is removed or narrowed to what is left.
- [ ] Gate green (`../../embarch-fleet/gate.md`); `changelog.d/` fragment dropped.
