# embarch-dev-bench: spec

**Status:** active, 2026-09-04.

What is true now. Why: [decisions.md](decisions.md). Unresolved: [open.md](open.md).

## 1. What it is

The physical rig that plays the DUT's BLE counterpart during a `Study` — it advertises, connects as central or peripheral, exchanges GATT data, runs engineer-authored `.eap` protocol state machines, and will sample power. Zephyr-based C firmware, cross-vendor by design: "one firmware project" means **one shared application source tree** that different west workspaces build for different vendor targets, not one board.

The `Study`/`DevBenchMessage` types and the COBS/postcard wire protocol are owned by [embarch-study-designer](../embarch-study-designer/decisions.md) and treated here as given. `embarch-core` never talks BLE or samples power itself.

**The board, as of 2026-08-31: `nrf54l15dk/nrf54l15/cpuapp` (`workspaces/nordic`).** The ESP32-C5 workspace stays in the tree, working (decision 43). **Enrol it with `link_port_interface = 2`** — this DK's console UART is VCOM1, and detection's lowest-index fallback lands on a port that accepts bytes and never answers.

**A second app, `pd-bench/`, is a USB PD partner** (decisions 48, 49): a Zephyr USB-C port on a NUCLEO-G0B1RE, a sink on the X-NUCLEO-SNK1M1 or dual role on the X-NUCLEO-DRP1M1 (`-DSHIELD=x_nucleo_drp1m1`, 5 V source from its CN3 supply), scripted over its console shell with `signal_exchange`, enrolled as a bench board. It shares no code with `app/` and never speaks the wire.

**v1 scope, explicitly bounded:** BLE plus power sampling only. GPIO/analog stimulus is future scope ([open.md](open.md)). **No power-sampling hardware and no physical DUT connector yet** — a DUT is whatever is in BLE range. **No on-board status indication**: state is observable only through `embarch-core`.

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

pd-bench/                         the USB PD partner (decision 48): its own
                                  app, shell only, built from a workspace
                                  with the patched USB-C stack

workspaces/                       one west topdir per vendor family
├── nordic/        NCS v3.4.0 + SoftDevice Controller — the current bench
├── espressif/     vanilla Zephyr v4.4.0 + hal_espressif — working, inactive
└── native_sim/    vanilla Zephyr, host process, stubs both bridges
```

Each workspace's manifest lives in a `manifest/` subdirectory, not at the workspace root: `west init -l <dir>` places `.west/` *next to* `<dir>`, so nesting keeps each topdir independent. `app` is a symlink in every workspace, never a copy.

## 3. Invariants

- **Nothing unframed ever reaches the link.** Every byte dev-bench sends is a COBS-framed `DevBenchMessage`, log output included. `CONFIG_LOG_BACKEND_UART=n` is the single most important line in the logging config — it defaults to `y` whenever a UART console exists, and on both supported boards the console *is* the protocol link.
- **dev-bench interprets no payload.** It stamps arrival and forwards bytes. What a payload *means* is engineer-declared knowledge that lives host-side; a firmware holding it would need reflashing on every meaning change.
- **One DUT connection at a time**, enforced in firmware, not the controller's link budget.
- **Bonds are RAM-only**, cleared on `Hello` *and* explicitly at study end, so every study pairs from scratch and behaves like the first.
- **A `Hello` is a hard reset**, and it waits for its own disconnect, not just requesting one.
- **A named thing missing fails the step; an unnamed thing missing is skipped.** A selective monitor target or an `.eap` source the DUT does not have fails, naming which. The subscribe-to-everything walk logs and skips, because nothing there was named.
- **Loss is counted and reported, never silent.** Dropped transcript entries, notifications and log records, RX overruns, and an oversized inbound frame all produce a `LogLine`.
- **A capacity limit refuses, never truncates.** An oversized `StudyStart`, or a manifest over the wire-length cap, is rejected by name.
- **The bench never manufactures a claim.** No hardware ID without `hwinfo`, no `captured_data` on a stub, no protocol outcome for a run that did not happen.
- **Application code calls only portable Zephyr APIs** (`bt_*`, `gpio_*`, `adc_*`), never anything vendor-proprietary.

## 4. Link and threading contracts

The link UART has **three writers**, which is why `link_tx_mutex` is held across *build-and-send*, not just send — the build half is what races, since every sender builds into the shared `tx_scratch`:

| Writer | Thread | Contract |
|---|---|---|
| dispatch loop | main | builds and sends directly |
| transcript TX thread | its own | drains a `k_msgq` the BLE sink fills |
| log backend | Zephyr's log thread | `CONFIG_LOG_MODE_DEFERRED`, so backends never run in the caller's context |

Inbound is **interrupt-driven**: an ISR drains the FIFO into a 2 KB ring buffer. The buffer is sized to *scheduling latency, not a whole frame* — Core sends `Hello` then `StudyStart` and waits, so nothing arrives during the long BLE calls the loop blocks in.

Three sinks, with deliberately different threading contracts:

- **`ble_bridge_set_transcript_sink`** — called from Zephyr's BT RX thread *and* the dispatch thread, so entries are built as a **stack local** — a shared static would tear mid-emit — and the sink does one bounded `K_NO_WAIT` copy into a queue; blocking the BT RX thread would stall the very notifications being recorded.
- **`ble_log_sink`** — only ever invoked from the dispatch thread inside `ble_bridge_execute`, so it may write the UART directly. BLE callbacks record what they want said in a static; the dispatch thread speaks once the wait completes.
- **the log backend sink** — deferred, except on the fatal path, where `log_panic()` switches to synchronous processing and the sink skips the mutex, writing directly. Getting the fault out is the point, and Core resyncs on the next delimiter.

## 5. Constants and budgets

Every load-bearing constant, with its provenance: [spec/constants.md](spec/constants.md).
