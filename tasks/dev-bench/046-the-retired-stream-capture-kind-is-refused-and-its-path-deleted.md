# 046 — The retired stream-capture GATT kind is refused, and its capture path is deleted

**State:** claimed by agent/dev-bench/046-the-retired-stream-capture-kind-is-refused-and-its-path-deleted, 2026-11-10 05:16
**Source:** `dev-bench/045` (landed 2026-11-10, `embarch-dev-bench` `3daa719`), which derived every other `GattOperation` value from the crate and left this one typed by hand because the decoder still has an arm for it
**Issue:** EMB-133
**Scope:** dev-bench
**Hardware:** toolchain — this repo's Zephyr tree is gitignored, so a worktree cannot build it (`tasks/README.md`, Hardware field). Build from the worktree against the main checkout's `workspaces/*` with the fleet's `west`, as `dev-bench/045` did.
**Owner:** no

## What

`embarch-study-designer` decision 39 retired `GattOperation::StreamCapture` and removed the variant, so no host built since schema v8 can send kind 5, and the `Hello`/`HelloAck` schema check refuses an older one. The bench still carries the whole path for it:

- `app/src/serial_protocol.h` `enum dbm_gatt_op_kind`: `DBM_GATT_OP_STREAM_CAPTURE = 5`, typed by hand, with a comment explaining why.
- `app/src/serial_protocol.c`: the decoder's `case DBM_GATT_OP_STREAM_CAPTURE:` arm.
- `app/src/ble_bridge.h`: `GATT_OP_STREAM_CAPTURE = 5` in `enum gatt_operation_kind`, the `ble_stream_sample_handler` type and `ble_bridge_set_stream_handler()`, with its comment block.
- `app/src/ble_bridge_real.c`: `case GATT_OP_STREAM_CAPTURE`, the `streaming` flag and its routing in the notify callback, `stream_handler` and its user data, the setter, and every comment that cites the capture kind as a precedent.
- `app/src/ble_bridge_stub.c`: the stub's setter and its `stream_handler`.

Nothing calls `ble_bridge_set_stream_handler()`, so a capture step on the bench today counts and drops every notification. The tap that replaced it is `StreamSource::GattNotify`.

Delete the path, refuse kind 5 the way the decoder refuses any other unknown `GattOperation` kind, and let both C GATT enums take every value from `crate_limits.h` with the `_COUNT` assert. Comments elsewhere that cite the capture kind as a precedent (the "its own budget is the window" note, for one) are reworded to stand on their own or point at what still exists.

## Why now

A decoder arm for a kind nothing can send is a slot a future crate variant could be read into, and a capture path with no sink reads as a feature that works. It is also decision 56's last hand-typed wire value.

## Done when

- [ ] A `StudyStart` carrying `GattOperation` kind 5 is refused by the decoder the way any unknown kind is, with a `serial_protocol` ztest.
- [ ] No `STREAM_CAPTURE` or stream-handler code is left in `app/src/`, and both C GATT operation enums take every value from `crate_limits.h`.
- [ ] Both bench images (`nrf54l15dk/nrf54l15/cpuapp`, `esp32c5_devkitc/esp32c5/hpcore`) and the `native_sim` app build, and the `native_sim` ztest suites pass.
- [ ] Decision 56 no longer describes a hand-typed 5.
- [ ] Gate green (`../../embarch-fleet/gate.md`); `changelog.d/` fragment dropped.
