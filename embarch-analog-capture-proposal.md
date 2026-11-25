# Proposal: capturing, viewing and recording one audio-rate analog signal on a bench

**Status:** proposal, 2026-11-18. Route 1 with a dedicated USB CDC sample link **chosen by the bench owner, 2026-11-24**; built, EMB-470 to EMB-479; waiting on the first bench measurements (EMB-478).

Spans `embarch-core`, `embarch-study-designer`, `embarch-api`, `embarch-ui` and `embarch-dev-bench`, which is why it sits at this repo's root ([DOC-PROTOCOL.md](DOC-PROTOCOL.md) §3). Opened by EMB-213. **An engineer evaluating a sensor concept before any custom board exists has to see and record its signal before a detector can be written**: a contact microphone slid over a textured surface, one event per bump. Piezo pickups and vibration sensors are the same need. What the research pass asks of the HIL design is [notes/hil/13-research-phase.md](notes/hil/13-research-phase.md).

## The need

1. **Source**: an electret microphone on a breakout with its own op-amp, or a bare capsule with a bias resistor and a coupling capacitor, wired to the ADC of a Nordic dev kit: an nRF52840 DK on the DUT side, the nRF54L15 DK as the dev bench.
2. **Rate and size**: one channel at 16 to 32 ksps, 12 to 16 bit. **Worst case 64 kB/s**; a 30 s scan is 1.92 MB of samples, many scans a session.
3. **A live view** while the sensor moves, to see whether each bump makes a distinct event.
4. **A recording** an analysis script reads (CSV or WAV), stating the sample rate and any dropped samples.
5. **Offline event counting** on the recording, against a known count.
6. **On-device counting** later, the same detector in DUT firmware.

## What the suite has today

- **A rate reaches the decode only from `PowerFrontEnd { sample_hz }`** (`embarch-core` `src/study.rs`, `write_stream_record`); every other `Samples` tap stamps each sample with its record's arrival time ([decoders.md](embarch-study-designer/interfaces/decoders.md)). **No bench board streams samples from a general analog input**: the dev bench has none ([spec](embarch-dev-bench/spec.md) §1), decision 24's PPK2 is not ordered, and pd-bench reads VBUS only for its own source check ([its decisions](embarch-dev-bench/decisions/pd-bench.md)).
- **A `Signal` tap is read by Core itself** ([embarch-study-designer decision 39](embarch-study-designer/decisions/streams.md)). **Binary samples on one would be garbled**: Core splits every read at each `0x0A` byte, whatever the encoding, decodes each piece on its own from its first byte, and drops a trailing odd byte. **A piece cut mid-sample, by a newline byte or by any odd-length read, shifts every sample of the piece after it** (`embarch-core` `src/study.rs`, `read_signal_tap`, read from the source, not run). The raw file keeps the bytes unchanged.
- **A host study takes only `Text` taps** ([embarch-core decision 98](embarch-core/decisions/host-study.md)). **A bench study takes a `Raw` `Signal` tap**, and holds it open for as long as a step's `delay_before_ms` ([embarch-study-designer decision 42](embarch-study-designer/decisions/study.md)): a `BleAdvertise` step passes with no peer (`embarch-dev-bench` `app/src/ble_bridge_real.c`, `execute_advertise`), so its delay is a scan of fixed length. Read from the source, not run.
- **A capture outside a study** exists ([embarch-core decision 92](embarch-core/decisions/signal-capture.md)), but its reads return lossy UTF-8, which destroys binary samples.
- **Losses**: a tap's `dropped` count reaches `truncated` ([taps.md](embarch-study-designer/interfaces/taps.md)). **End to end, `Study.record_checks` verifies a magic and a CRC-32 per record** ([decision 70](embarch-study-designer/decisions/payload-meaning.md)), on a bench study only: `HostStudy` has no such field.
- **The live view** decimates a series server-side, one point in N, and says so ([embarch-ui decision 31](embarch-ui/decisions/live-study.md)). A 32 ksps series reaching it live is unmeasured.
- **The recording**: one CSV row per sample (`rx_utc_ms, step_name, value, unit, channel_id, core_rx_utc_ms`), 40 to 47 B [derived from the row shape, by step-name length], so **38 to 45 MB for a 30 s scan** beside its 1.92 MB of raw samples. No WAV anywhere.

## Throughput, one 16-bit channel at 32 ksps

8N1 costs 10 bits a byte, so **1 Mbaud carries 100 kB/s** and **460800 baud carries 46 kB/s**, below 64 kB/s: the outpost's measured 460800-baud link ([its spec](embarch-outpost/spec.md) §4) cannot carry this signal, and its 21.9 KB/s used under half of it ([roadmap](suite/roadmap.md)).

| Route | Carrier | Needed | Load | Basis |
|---|---|---|---|---|
| **1. Dev-bench analog input, dedicated CDC sample link (chosen)** | USB CDC ACM, full speed, **its own port**, apart from the 1 Mbaud control link | about 66 kB/s | low [assumed] | 528 B per 512 B of samples [derived from the block]; no CDC ACM throughput is measured anywhere in the suite ([embarch-smp spec](embarch-smp/spec.md)) |
| 1, as first proposed | the control link, 1 Mbaud, **shared** with logs, transcript and step results | 65 to 77 kB/s | **65 to 77 %** | [dev-bench constants](embarch-dev-bench/spec/constants.md). **Why it was the weak point**; the sample link removes it |
| 2. DUT over a `Signal` tap, UART | a direct UART, 1 Mbaud, dedicated | about 66 kB/s | about 66 % | `EMBARCH_SIGNAL_BAUD`'s default ([Core constants](embarch-core/interfaces/constants.md), [assumed]) |
| 3. DUT over BLE | 244 B notifications, about 263 a second [derived], then the control link | 65 to 77 kB/s on the link; 130 to 154 with a transcript tap ([decision 55](embarch-study-designer/decisions/payload-meaning.md)) | **over the line** | unmeasured here |
| 4. Outside the suite | route 2's carriers, read by the engineer's script | as route 2 | as route 2 | as route 2 |

**Each ADC at 32 ksps is [assumed]** until the first bench measures it. **The portable ADC API is not used**: the nRF52 backend calls nrfx SAADC directly, a narrow exception ([embarch-dev-bench decision 60](embarch-dev-bench/decisions/analog.md)).

## The four routes against the six items

| Item | 1. Dev-bench input (chosen) | 2. DUT over a `Signal` tap | 3. DUT over BLE | 4. Outside the suite |
|---|---|---|---|---|
| 1. Source | the dev bench's ADC; **a bench with no DUT** ([13](notes/hil/13-research-phase.md#a-bench-with-no-dut)) | the DUT's ADC | the DUT's ADC | the DUT's ADC |
| 2. Rate | dedicated CDC link, about 66 kB/s | dedicated link, about 66 %, or CDC ACM | BLE unmeasured, then route 1's link | as 2 |
| 3. Live view | min/max per column, clip indicator (decision 11) | the existing decode, then min/max | the existing decode, no rate | the script's own, if any |
| 4. Recording | rate in the start header; drops placed by the block index and CRC | raw bytes, drops placed by the DUT's index and CRC | no rate; drops counted | the script's |
| 5. Offline count | WAV export (decision 12), then the engineer's ([13](notes/hil/13-research-phase.md#the-detector-being-researched)) | the engineer's | the engineer's | the engineer's |
| 6. On-device count | the sensor moves to the DUT (a rewire) | same wiring, same firmware | same wiring | same wiring |
| Evidence | **`by: bench`**, once its image is released ([13](notes/hil/13-research-phase.md#who-samples-decides-the-evidence)) | `by: dut`; raw bytes, no measurement | `by: dut` | no study record |
| Suite work | EMB-470 to EMB-479 below | Later; a binary `Signal` tap first | a rate; the link's headroom | none |

## Chosen: route 1, with a dedicated USB CDC sample link

**The bench owner's call, 2026-11-24.** What the first draft recommended (route 2) and why it no longer does:

- **Route 1's weak point was the shared control link** (65 to 77 % of 1 Mbaud). A dedicated USB CDC port for samples removes it, so route 1 carries the signal with margin and no other traffic on its wire.
- **Route 1's evidence is `by: bench`**, the bench's own measurement from a released image ([13](notes/hil/13-research-phase.md#who-samples-decides-the-evidence)), where route 2's every value is `by: dut`.
- **The portable ADC API at 32 ksps was unverified**; decision 2 below replaces it with nrfx SAADC on nRF52, one recorded exception.
- **Route 3 stays rejected** (two hops onto a shared link that already lost frames, [decision 70](embarch-study-designer/decisions/payload-meaning.md)); **route 4** brings nothing route 1 does not.
- **Route 2 moves to Later.** Its cost, a rewire between research and on-device counting, stays true.

### The thirteen decisions

All thirteen are folded and built (EMB-470 to EMB-479), so none is restated here: the dev bench's in [decisions 60 to 66](embarch-dev-bench/decisions/analog.md) and [spec/analog.md](embarch-dev-bench/spec/analog.md); the session and block layout in [embarch-study-designer decisions 104 to 106](embarch-study-designer/decisions/analog-capture.md); Core's in [decision 124](embarch-core/decisions/probes.md), [125](embarch-core/decisions/streams.md) and [126](embarch-core/decisions/analog-capture.md); the live view in [embarch-ui decision 105](embarch-ui/decisions/live-series.md); the WAV export in [embarch-api decision 130](embarch-api/decisions/audio-export.md); the walkthrough in [the studies guide](suite/studies-guide.md) §5.

**What corrects the first draft:** Core's newline split and partial-sample loss for a binary tap (see "What the suite has today") is route 1's problem too, now EMB-475; a gap is placed by block index, never from arrival times; `record_checks` verifies each block's magic and CRC.

**The analog noise floor with DC/DC on and off** is unmeasured: EMB-478.

## Later

- **nRF54L15 and STM32 backends** behind decision 2's interface.
- **A multi-channel nRF52 backend** (TIMER and PPI).
- **Route 2:** a DUT-side streaming module emitting the same blocks, so research and on-device counting share wiring and firmware; its stage A needs no suite change beyond the block format.
- **A test-signal loopback.**

## What stays outside the suite

- **The event detector.** What a payload means is the engineer's ([embarch-study-designer decision 52](embarch-study-designer/decisions/payload-meaning.md)), and the dev bench interprets no payload ([spec](embarch-dev-bench/spec.md) §3). A generic excursion-count reducer is the HIL design's question ([13](notes/hil/13-research-phase.md#the-detector-being-researched)).
- **The analysis script**, which an LLM agent may write: its count is tagged `(analysis)`, never a measurement.
- **The sensor's analog front end**: bias, gain and coupling are the engineer's hardware.

## Open

- **CDC ACM throughput and the ADC rate** are [assumed] until the first bench measures them.
- **Whether the live feed holds 32 ksps**, end to end from Core's batches to the browser.

**Fold:** the Later list and the open measurements remain. Deleted once nothing in it is still proposed.
