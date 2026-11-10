# embarch-dev-bench: constants and budgets

**Status:** active, 2026-11-06.

Split verbatim from [../spec.md](../spec.md) §5 (`tasks/dev-bench/040`), when the PD bench decisions put that file in its reserve. Nothing below is reworded. Every load-bearing constant with its provenance. Current truth: [../spec.md](../spec.md).

| Name | Value | Provenance |
|---|---|---|
| link baud | 1 Mbaud | must equal Core's `DEV_BENCH_BAUD` exactly, or the first `Hello` fails to decode |
| `current-speed` overlay | `&uart20` on the DK | [measured 2026-08-31] the DK's `zephyr,console` is already `uart20`, so only the baud needed setting |
| `link_rx_ring` | 2 KB | [assumed] scheduling latency, deliberately not `DBM_MAX_FRAME_LEN` — §4 |
| `DBM_MAX_INBOUND_FRAME_LEN` | 12,507 B | [computed from `serial_protocol.h`] Core sends only `Hello` and `StudyStart`; sized to `StudyStart`, which gained `DBM_MAX_PROTOCOLS_WIRE_LEN` at schema v15 (decision 41) |
| `DBM_MAX_OUTBOUND_FRAME_LEN` | 3,082 B | [measured] `StepResult`'s bound — the largest message dev-bench can produce |
| `DBM_MAX_TRANSCRIPT_PAYLOAD_LEN` | 244 B | one full 247-byte ATT MTU minus the 3-byte ATT header |
| `DBM_MAX_STREAM_CHUNK_BYTES` | 293 B | [computed from `serial_protocol.h`] the worst-case encoded transcript entry, 244 B plus a 49-byte envelope; the crate allows 512 (decision 53) |
| `DBM_MAX_EVENT_ARMS_PER_STATE` | 2 | [measured] the crate allows 4; an arm is the heaviest thing a state holds and 4 costs ~9 KB more, and both worked protocols use one |
| `DBM_MAX_PROTOCOLS_WIRE_LEN` | 3 KB | [measured] a byte cap over the whole span; the eleven count ceilings multiply to a bound nothing would send (decision 41) |
| `SCAN_SEEN_MAX` | 256 | [measured] 12 advertisers seen in three minutes at the bench; costs ~9 KB of static RAM |
| `SCAN_SEEN_MFG_PAYLOAD_MAX` | 4 B | [assumed] kept small on purpose — decision 44's one identified use is a 2-byte FICR suffix; costs 2,816 B [measured] of the ESP32-C5's SRAM across all 256 entries |
| `BLE_MAX_MONITOR_SUBSCRIPTIONS` | 32 | [assumed] deliberately not the wire type's 128 worst case |
| `CONFIG_MAIN_STACK_SIZE` | 8192 | [measured] a board fragment silently overrode `prj.conf` with 2048 — Zephyr merges the fragment last and the later value wins with no warning |
| `CONFIG_BT_MAX_CONN` | 2 | on Nordic this is forced: the SoftDevice Controller gives central `BT_MAX_CONN − BT_CTLR_SDC_PERIPHERAL_COUNT` slots, so 1 leaves central **zero** and builds cleanly with a silently broken role |
| `CONFIG_LOG_BUFFER_SIZE` | 1 KB | [measured] a `Debug` burst overruns it and says so (`N record(s) dropped`) |
| disconnect wait | 2 s | [assumed] far longer than a local disconnect needs; timing out leaves the prior behaviour |

**SRAM is the binding constraint on the ESP32-C5** and has overflowed three times; it now sits at **87.85%** [measured, dev-bench task 044] of 378,384 B, and the largest remaining lever on it is `tx_scratch`'s dead `StudyStart` member ([open.md](../open.md)). The nRF54L15DK is far roomier: FLASH 19.08%, RAM 59.67% of 256 KB [measured, dev-bench task 044].
