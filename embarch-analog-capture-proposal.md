# Proposal: capturing, viewing and recording one audio-rate analog signal on a bench

**Status:** proposal, 2026-11-18.

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
| 1. Dev-bench analog input | the dev bench's link, 1 Mbaud, **shared** with logs, transcript and step results | 65 to 77 kB/s | **65 to 77 %** | link baud: [dev-bench constants](embarch-dev-bench/spec/constants.md). Low end: COBS only; high end: the transcript entry's 49 B envelope per 244 B [computed there], the worst case on record. A sample chunk's own envelope is unmeasured |
| 2. DUT over a `Signal` tap, UART | a direct UART, 1 Mbaud, **dedicated** | about 66 kB/s | **about 66 %** | `EMBARCH_SIGNAL_BAUD`'s default ([Core constants](embarch-core/interfaces/constants.md), [assumed] there); 12 B of framing per 512 B of samples [derived from stage A's layout]; the DK's whole UART path at 1 Mbaud, through its debug chip where the port is the DK's own ([dev-bench decision](embarch-dev-bench/decisions/link.md)) [assumed] |
| 2. DUT over a `Signal` tap, USB | USB CDC ACM, full speed | about 66 kB/s | low [assumed] | no CDC ACM throughput is measured anywhere in the suite ([embarch-smp spec](embarch-smp/spec.md)) |
| 3. DUT over BLE | 244 B notifications, about 263 a second [derived], **then route 1's link** | 65 to 77 kB/s on the link; **130 to 154 kB/s with a transcript tap**, each notification crossing twice ([decision 55](embarch-study-designer/decisions/payload-meaning.md)) | **over the line** with a transcript | the BLE link at that rate [assumed], unmeasured here |
| 4. Outside the suite | route 2's carriers, read by the engineer's script | as route 2 | as route 2 | as route 2 |

**Each ADC at 32 ksps is [assumed]**, to be checked against the nRF52840 and nRF54L15 product specifications. **Route 1 also assumes 32 ksps through Zephyr's portable ADC API**, the only one the dev bench may call ([spec](embarch-dev-bench/spec.md) §3) [assumed]; route 2's DUT firmware is the engineer's and may use the vendor's driver.

## The four routes against the six items

| Item | 1. Dev-bench analog input | 2. DUT over a `Signal` tap | 3. DUT over BLE | 4. Outside the suite |
|---|---|---|---|---|
| 1. Source | the dev bench's ADC; **a bench with no DUT** ([13](notes/hil/13-research-phase.md#a-bench-with-no-dut)) | the DUT's ADC | the DUT's ADC | the DUT's ADC |
| 2. Rate | shared link, 65 to 77 %; the portable ADC API at 32 ksps unverified | dedicated link, about 66 %, or CDC ACM | BLE unmeasured, then route 1's link | as 2 |
| 3. Live view | the existing rate-carrying decode | stage B | the existing decode, no rate | the script's own, if any |
| 4. Recording | rate declared; drops counted, not placed | stage A: raw bytes, drops placed by the DUT's index and CRC; stage B: in the suite | no rate; drops counted | the script's |
| 5. Offline count | the engineer's ([13](notes/hil/13-research-phase.md#the-detector-being-researched)) | the engineer's | the engineer's | the engineer's |
| 6. On-device count | the sensor moves to the DUT | **same wiring, same firmware** | same wiring | same wiring |
| Evidence | **`by: bench`**, once its image is released ([13](notes/hil/13-research-phase.md#who-samples-decides-the-evidence)) | stage A: raw bytes, no measurement; stage B: `by: dut` | `by: dut` | no study record |
| Suite work | dev-bench firmware, a source variant, a wire bump and reflash | stage A: none; stage B: five repos | a rate; the link's headroom | none |

## Recommended: route 2, in two stages

- **The most margin of the three suite routes**, on a link nothing else shares.
- **It starts with no suite change**, and every later one is general: any sensor a DUT streams needs a binary `Signal` tap with a declared rate.
- **The detector is researched on the ADC that will run it** (item 6), with no rewiring between research and on-device counting.
- **What it costs: every value is `by: dut`**, the DUT's own word from firmware the agent may have written ([13](notes/hil/13-research-phase.md#who-samples-decides-the-evidence)), **so its answer about the sensor is development evidence until route 1 exists.** Route 1 is the route when research numbers must reach a published report as bench evidence; it stays under Open, not rejected.
- **Route 3 is rejected at this rate**: two hops onto a shared link that already lost frames at a far lower rate ([decision 70](embarch-study-designer/decisions/payload-meaning.md)). **Route 4 is stage A without** a study record, a topology-resolved port and Core's run log, so it brings nothing route 2 does not.

### Stage A: the first capture

**No suite change; by design, not run.**

1. **DUT firmware** (the engineer's repo): the ADC at the chosen rate, double-buffered; **each block a 4 B magic, the 4 B index of its first sample, 256 `i16` samples and a CRC-32/ISO-HDLC** over the preceding bytes, out a UART at 1 Mbaud or a CDC ACM port.
2. **Topology**: the port declared as a direct `dut-to-host` signal, with its baud.
3. **A bench study**: one whole-study `Raw` tap on the signal; **`record_checks` naming the tap with the magic**; one `BleAdvertise` step whose `delay_before_ms` is the scan's length, during which the person slides the sensor. The advertising is a placeholder the study needs no peer for.
4. **After the run**: `<tap>.bin` holds the bytes as sent, and **Core reports which blocks verified** (decision 70). **The engineer's script places each gap by the blocks' indices**, writes one WAV per gap-free segment with the gaps listed, and counts events. No live view yet.

### Stage B: in the suite, as issues once accepted

| Repo | Change |
|---|---|
| `embarch-study-designer` | **A declared rate for a tap with no `PowerFrontEnd`**, host-only and keyed by tap id as `record_checks` is, so the dev-bench wire does not change; **a `Raw` tap and `record_checks` on `HostStudy`**, so a scan needs no placeholder step and can end on a `Prompt`; for a framed tap, where a record's samples start and which field is the index of its first, so **a gap is placed by index, never inferred from arrival times** |
| `embarch-core` | **Split a read at newlines for a `Text` tap only**; **carry a partial sample from one read to the next**, or decode a framed tap per verified record rather than per read; host-study `Raw` taps and `Samples` batches to the live feed |
| `embarch-api` | **A WAV export** of a `Samples` tap with a declared rate: one file per gap-free segment, the gaps listed beside them, refused for a tap with no rate |
| `embarch-ui` | **Measure the live series at 32 ksps** and decimate before the browser if it does not hold; authoring the rate and framing once host-study rows exist ([host-study proposal](embarch-host-study-proposal.md)) |
| `embarch-doc` | A studies-guide section for an audio-rate analog signal |

## What stays outside the suite

- **The event detector.** What a payload means is the engineer's ([embarch-study-designer decision 52](embarch-study-designer/decisions/payload-meaning.md)), and the dev bench interprets no payload ([spec](embarch-dev-bench/spec.md) §3). A generic excursion-count reducer is the HIL design's question ([13](notes/hil/13-research-phase.md#the-detector-being-researched)), not a detector.
- **The DUT's sampling and counting firmware** (items 1 and 6), and stage A's analysis script, which the agent may write: in a report its count is tagged `(analysis)`, never a measurement ([13](notes/hil/13-research-phase.md#the-detector-being-researched)).
- **The sensor's analog front end**: bias, gain and coupling are hardware the engineer chooses.

## Open

- **Route 1, the dev bench's own analog input**, for `by: bench` evidence and as the first hardware a power front end could reuse [inference]: a source variant (`PowerFrontEnd` names an instrument), 32 ksps through the portable ADC API, and its share of the link.
- **Whether a suite-shipped DUT module, outpost-style, frames stage A's blocks** so every engineer does not write it. The outpost itself samples no pin ([embarch-outpost spec](embarch-outpost/spec.md) §1).
- **The ADC rates, the nRF52840's UART at 1 Mbaud and CDC ACM's throughput**: [assumed] until the first bench measures them.
- **Whether the live feed holds 32 ksps**, end to end from Core's batches to the browser.
- **What a scan costs the person** once a host study ends it on a `Prompt`: the person's go on the card before it starts, as for any host study holding a prompt ([02](notes/hil/02-study.md#how-a-study-runs-as-the-procedure-would-say-it)).

**Fold:** each stage moves into its sub-projects' docs as it is accepted and leaves this file; the file is deleted once nothing in it is still proposed.
