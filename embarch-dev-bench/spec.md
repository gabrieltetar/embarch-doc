# embarch-dev-bench: spec

**Status:** active, 2026-09-04.

What is true now. Why: [decisions.md](decisions.md). Unresolved: [open.md](open.md).

## 1. What it is

The physical rig that plays the DUT's BLE counterpart during a `Study` — it advertises, connects as central or peripheral, exchanges GATT data, runs engineer-authored `.eap` protocol state machines, and will sample power. Zephyr-based C firmware, cross-vendor by design: "one firmware project" means **one shared application source tree** that different west workspaces build for different vendor targets, not one board.

The `Study`/`DevBenchMessage` types and the COBS/postcard wire protocol are owned by [embarch-study-designer](../embarch-study-designer/decisions.md) and treated here as given. `embarch-core` never talks BLE or samples power itself.

**The board, as of 2026-08-31: `nrf54l15dk/nrf54l15/cpuapp` (`workspaces/nordic`).** The ESP32-C5 workspace stays in the tree and working (decision 43). **Enrol it with `link_port_interface = 2`** — this DK's console UART is VCOM1, and detection's lowest-index fallback lands on a port that accepts bytes and never answers.

**v1 scope, explicitly bounded:** BLE plus power sampling only. GPIO/analog stimulus is future scope ([open.md](open.md)). **No power-sampling hardware and no physical DUT connector yet** — a DUT is whatever is in BLE range. **No on-board status indication**: the bench's state is observable only through `embarch-core`.

## 2. Repository layout

```
app/                              shared C source, vendor-agnostic
├── src/
│   ├── main.c                    dispatch loop, three link writers, tap sync
│   ├── ble_bridge.h              internal API mirroring Action/GattOperation
│   ├── ble_bridge_real.c         Action -> Zephyr bt_* calls
│   ├── ble_bridge_stub.c         canned Outcomes, no BLE host (native_sim)
│   ├── serial_protocol.[ch]      COBS framing, hand-written postcard codec
│   ├── eap.h / eap_interp.[ch]   .eap wire types / semantics, no radio in it
│   ├── dev_bench_log.c           a Zephyr log backend emitting LogLines
│   └── study_ffi_{stub,real}.c   fixed decode results / the real staticlib
├── tests/{serial_protocol,dev_bench_log}/     ztest, run on native_sim
├── boards/                       per-board overlays and .conf fragments
└── CMakeLists.txt                referenced by every workspace, never copied

workspaces/                       one west topdir per vendor family
├── nordic/        NCS v3.4.0 + SoftDevice Controller — the current bench
├── espressif/     vanilla Zephyr v4.4.0 + hal_espressif — working, inactive
└── native_sim/    vanilla Zephyr, host process, stubs both bridges
```

Each workspace's manifest lives in a `manifest/` subdirectory, not at the workspace root: `west init -l <dir>` places `.west/` *next to* `<dir>`, so nesting one level down is what keeps each topdir genuinely independent. `app` is a symlink in every workspace, never a copy.

## 3. Invariants

- **Nothing unframed ever reaches the link.** Every byte dev-bench sends is a COBS-framed `DevBenchMessage`, log output included. `CONFIG_LOG_BACKEND_UART=n` is the single most important line in the logging config — that backend defaults to `y` whenever a UART console exists, and on both supported boards the console *is* the protocol link.
- **dev-bench interprets no payload.** It stamps arrival and forwards bytes. What a payload *means* is engineer-declared knowledge that lives host-side; a firmware holding it would need reflashing whenever a DUT's meaning changed.
- **One DUT connection at a time**, enforced in firmware rather than by the controller's link budget.
- **Bonds are RAM-only**, cleared on `Hello` *and* explicitly at study end, so every study pairs from scratch and a second run of a study behaves like the first.
- **A `Hello` is a hard reset**, and it waits for its own disconnect rather than only requesting one.
- **A named thing that is missing fails the step; an unnamed thing that is missing is skipped.** A selective monitor target or an `.eap` source the DUT does not have fails, naming which. The subscribe-to-everything walk logs and skips, because nothing there was named.
- **Loss is counted and reported, never silent.** Dropped transcript entries, dropped notifications, RX overruns, dropped log records, and an oversized inbound frame all produce a `LogLine`.
- **A capacity limit refuses, never truncates.** An oversized `StudyStart`, or a manifest over the wire-length cap, is rejected by name.
- **The bench never manufactures a claim.** No hardware ID without `hwinfo`, no `captured_data` on a stub, no protocol outcome for a run that did not happen.
- **Application code calls only portable Zephyr APIs** (`bt_*`, `gpio_*`, `adc_*`), never anything vendor-proprietary, so the same source survives a workspace swapping its pinned revision.

## 4. Link and threading contracts

The link UART has **three writers**, which is why `link_tx_mutex` is held across *build-and-send* rather than just send — the build half is what races, since every sender builds into the shared `tx_scratch`:

| Writer | Thread | Contract |
|---|---|---|
| dispatch loop | main | builds and sends directly |
| transcript TX thread | its own | drains a `k_msgq` the BLE sink fills |
| log backend | Zephyr's log thread | `CONFIG_LOG_MODE_DEFERRED`, so backends never run in the caller's context |

Inbound is **interrupt-driven**: an ISR drains the FIFO into a 2 KB ring buffer and the parser reads frames out of that. The buffer is sized to *scheduling latency, not a whole frame* — Core sends `Hello` then `StudyStart` and then waits, so nothing arrives during the long BLE calls the loop blocks in.

Three sinks, with deliberately different threading contracts:

- **`ble_bridge_set_transcript_sink`** — called from Zephyr's BT RX thread *and* the dispatch thread, so entries are built as a **stack local** (a shared static would tear under a notification arriving mid-emit) and the sink does one bounded `K_NO_WAIT` copy into a queue. Blocking the BT RX thread would stall the very notifications being recorded.
- **`ble_log_sink`** — only ever invoked from the dispatch thread inside `ble_bridge_execute`, so it may write the UART directly. BLE callbacks that want to say something record it in a static and let the dispatch thread speak after the wait completes.
- **the log backend sink** — deferred, except on the fatal path, where `log_panic()` switches to synchronous processing in the faulting context and the sink is told to skip the mutex and write directly. Getting the fault out is the point, and Core resyncs on the next delimiter.

## 5. Constants and budgets

| Name | Value | Provenance |
|---|---|---|
| link baud | 1 Mbaud | must equal Core's `DEV_BENCH_BAUD` exactly, or the first `Hello` fails to decode |
| `current-speed` overlay | `&uart20` on the DK | [measured 2026-08-31] the DK's `zephyr,console` is already `uart20`, so only the baud needed setting |
| `link_rx_ring` | 2 KB | [assumed] scheduling latency, deliberately not `DBM_MAX_FRAME_LEN` — §4 |
| `DBM_MAX_INBOUND_FRAME_LEN` | 9,415 B | [measured] Core sends only `Hello` and `StudyStart`; sized to `StudyStart`, not the general bound |
| `DBM_MAX_OUTBOUND_FRAME_LEN` | 3,082 B | [measured] `StepResult`'s bound — the largest message dev-bench can produce |
| `DBM_MAX_TRANSCRIPT_PAYLOAD_LEN` | 244 B | one full 247-byte ATT MTU minus the 3-byte ATT header |
| `DBM_MAX_EVENT_ARMS_PER_STATE` | 2 | [measured] the crate allows 4; an arm is the heaviest thing a state holds and 4 costs ~9 KB more, and both worked protocols use one |
| `DBM_MAX_PROTOCOLS_WIRE_LEN` | 3 KB | [measured] a byte cap over the whole span; the eleven count ceilings multiply to a bound nothing would send (decision 41) |
| `SCAN_SEEN_MAX` | 256 | [measured] 12 advertisers seen in three minutes at the bench; costs ~9 KB of static RAM |
| `BLE_MAX_MONITOR_SUBSCRIPTIONS` | 32 | [assumed] deliberately not the wire type's 128 worst case |
| `CONFIG_MAIN_STACK_SIZE` | 8192 | [measured] a board fragment silently overrode `prj.conf` with 2048 — Zephyr merges the fragment last and the later value wins with no warning |
| `CONFIG_BT_MAX_CONN` | 2 | on Nordic this is forced: the SoftDevice Controller gives central `BT_MAX_CONN − BT_CTLR_SDC_PERIPHERAL_COUNT` slots, so 1 leaves central **zero** and builds cleanly with a silently broken role |
| `CONFIG_LOG_BUFFER_SIZE` | 1 KB | [measured] a `Debug` burst overruns it and says so (`N record(s) dropped`) |
| disconnect wait | 2 s | [assumed] far longer than a local disconnect needs; timing out leaves the prior behaviour |

**SRAM is the binding constraint on the ESP32-C5** and has overflowed three times; it now sits at **87.04%** [measured], and the largest remaining lever on it is `tx_scratch`'s dead `StudyStart` member ([open.md](open.md)). The nRF54L15DK is far roomier: FLASH 18.97%, RAM 58.57% of 256 KB.
