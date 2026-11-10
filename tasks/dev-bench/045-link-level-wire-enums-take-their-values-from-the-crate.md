# 045 — The link-level wire enums take their values from the crate

**State:** done
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

- [x] Every C enum in `app/src/serial_protocol.h` and `app/src/ble_bridge.h` whose values are a Rust enum's postcard index takes them from `crate_limits.h` and asserts the variant count; any that cannot is named in the decision with the reason.
- [x] Both bench images (`nrf54l15dk/nrf54l15/cpuapp`, `esp32c5_devkitc/esp32c5/hpcore`) and the `native_sim` app build, and `app/tests/serial_protocol` passes on `native_sim`.
- [x] Decision 56's "Not covered" sentence is removed or narrowed to what is left.
- [x] Gate green (`../../embarch-fleet/gate.md`); `changelog.d/` fragment dropped.

## Outcome

Twelve enums added to `gen_crate_limits.py`'s `ENUMS`, their six source files to `crate_limits.cmake`'s inputs. Derived, each with a `_COUNT` assert: `dbm_tag`, `dbm_action_tag`, `dbm_gatt_op_kind` and `gatt_operation_kind`, `dbm_security_level` and `ble_security_level`, both GATT direction and event-kind pairs, `dbm_unit`, both stream tags, and the `DBM_LOG_LEVEL_*` defines. Three needed their own reading, recorded in decision 56: `GattOperation`'s retired `StreamCapture` stays a hand-typed 5; the log levels are also asserted equal to Zephyr's `LOG_LEVEL_*` in `dev_bench_log.c`; `BleRole` and `BleAddressKind` are bytes compared in `main.c` and the decoder, now against the crate's value instead of a literal. Not derived because they are bench-internal and mapped, not cast: `ble_role`, `ble_address_kind`, `action_kind`, `outcome_kind`.

Built with the fleet's `west`, from the main checkout's workspaces against this worktree: `serial_protocol` 67/67, `dev_bench_log` 15/15, `scan_seen_mfg` 7/7, `scan_seen_names` 12/12 on `native_sim`; the `native_sim` app, `nrf54l15dk/nrf54l15/cpuapp` (RAM 157,400 B) and `esp32c5_devkitc/esp32c5/hpcore` (`sram0_0_seg` 333,360 B) all clean, sizes unchanged, so no value moved. The ESP32-C5 build needs the venv's `bin/` on `PATH` for `esptool`. Drift checked against altered copies of the crate: an inserted `Action` variant stops the compile on its `_COUNT` assert, and swapping `DevBenchLogLevel`'s `Error` and `Warn` stops it on the Zephyr-severity asserts.
