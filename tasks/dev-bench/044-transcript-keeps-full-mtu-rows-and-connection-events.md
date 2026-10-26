# 044 — The GATT transcript drops every notification over ~213 bytes and never records a connect or disconnect

**State:** open
**Source:** DeepSeek V4 Pro review 2026-10-25 (embarch-dev-bench findings 2 and 5), verified by Opus against embarch-dev-bench@52822069
**Scope:** dev-bench
**Hardware:** toolchain — C in `app/src/main.c`, `app/src/serial_protocol.h` and `app/src/ble_bridge_real.c`, plus a `native_sim` ztest, built in the **main checkout** (this repo's Zephyr trees are gitignored, so a worktree cannot build it). Seeing connection rows in a real study needs the bench, so that half leaves a hardware-verification debt (`../../embarch-fleet/protocol.md` §7).
**Owner:** no

## What

Two holes in the transcript, which the suite calls "the complete story of the connection" (`embarch-study-designer/decisions/payload-meaning.md`).

1. **Full-MTU notifications never fit their record (finding 2).** The transcript TX thread encodes each entry into `record->bytes`, which is `DBM_MAX_STREAM_CHUNK_BYTES` = 256 B (`serial_protocol.h:85`, `:407`; `main.c:474-481`). The encoded entry costs varint(uptime ms) + 1 + 1 + 17 + 17 + 1 + 2 bytes before the payload (`serial_protocol.c:847-880`), about 43 B. So any payload over ~213 B fails to encode, against the 244 B that spec §5 and `DBM_MAX_TRANSCRIPT_PAYLOAD_LEN` promise. Such a row is dropped and counted, so the tap says `truncated: true`.

   The branch's own comment says this "cannot happen" (`main.c:483-489`), because it compares the payload to the buffer and forgets the envelope. The end-of-study LogLine then names the wrong cause, "(queue full)" (`:1520-1522`). The pinned wire test encodes into a 308 B `DBM_MAX_TRANSCRIPT_RECORD_LEN` buffer (`tests/serial_protocol/src/main.c:1286`) that the real path does not use. The notify-tap fan-out carries the raw payload and is not affected.
2. **No connect or disconnect row is ever emitted (finding 5).** `BLE_GATT_EVT_CONNECTED`/`DISCONNECTED` exist (`ble_bridge.h:344-345`), and `GattEventKind` documents both (`embarch-study-designer/interfaces/gatt-types.md:21`). Neither `connected_cb` nor `disconnected_cb` (`ble_bridge_real.c:585-613`) emits one. Decision 37 and the comment at `main.c:1502-1511` both justify the bond-clear's position by saying its disconnect "deserves to reach Core with everything else". It cannot, for two reasons: no entry is produced, and `close_all_taps()` (`:1500`) runs before `ble_bridge_clear_bonds()` (`:1515`), which is the opposite of the "before the drain" order the comment states.

**Proposed direction**, which leaves room for the design:

- Size the transcript record to what an entry can encode to. The crate's own `MAX_STREAM_CHUNK_BYTES` is 512, so a larger record is wire-legal. Check what the change costs in the ESP32-C5's SRAM: `tx_scratch` is sized by `StudyStart`, so it may cost nothing there.
- Emit connection rows from the two callbacks, which `transcript_emit` already allows from BT RX context. The disconnect reason goes in the one byte the entry has room for, and the field the reason uses is recorded.
- Order the end of a study so the bond-clear disconnect lands before the transcript tap closes, or amend decision 37 to say why it does not.

## Why now

Both board fragments set `CONFIG_BT_L2CAP_TX_MTU=247` specifically so that a full notification arrives in one piece (decision 28). Today a notification of that size is exactly what the transcript loses, and the loss is reported with the wrong cause. Connection rows are the first thing a reader checks when a study says "disconnected during X", and two docs say they are there.

## Done when

- [ ] A notification with a 244 B payload and both UUIDs reaches the transcript tap. A `native_sim` ztest encodes such an entry into the buffer the TX thread actually uses, not a larger stand-in, and asserts that it fits.
- [ ] The end-of-study loss line names the cause of each drop it counts, so queue-full and does-not-fit are not merged into one.
- [ ] Every connect and every disconnect the bridge sees produces a transcript row, and a disconnect row carries its HCI reason.
- [ ] The bond-clear disconnect at study end is in the transcript, or decision 37 and the comment at `main.c:1502-1511` stop saying it is.
- [ ] Both bench images build: `nrf54l15dk/nrf54l15/cpuapp` from `workspaces/nordic` and `esp32c5_devkitc/esp32c5/hpcore` from `workspaces/espressif`. The ESP32-C5's SRAM figure in spec §5 is re-measured if the record size moved. Run with `/home/gabriel/Github/embarch/.west-venv/bin/west` from the main checkout's workspace directories, per `README.md`.
- [ ] The `app/tests/serial_protocol` suite passes on `native_sim`. Core's and the crate's pinned frames still match if the record shape changed; it should not need to.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/` fragment for anything suite-level it made false. `spec.md` (9,632 of 10,240 B) is already inside its reserve, so new reasoning goes in `decisions/capture.md` or `decisions/ble.md`.
