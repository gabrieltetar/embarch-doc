# Proposal: one generic stream pipeline (DUT log capture and scripted shell interaction as instances of it)

**Status:** proposal, 2026-08-25.

**Where it stands: inbound half ACCEPTED 2026-08-25; outbound half still a proposal.** Originally: proposal, 2026-08-24, revised three times the same day, not accepted and deliberately not written into any `design.md`.

**What changed.** Scoping [embarch-outpost](embarch-outpost/design.md) — a DUT-side trace UART whose capture would have become the **fourth** near-identical pipeline here — the read direction was accepted and folded into the living docs: [embarch-study-designer/design.md](embarch-study-designer/design.md) §3 decision 39 (`Study.streams`, `StreamTap`/`StreamSource`/`StreamEncoding`, new §4.8; the schema bump written here as 5 → 6 landed as **7 → 8** — decisions 42/43 were implemented first and took v6/v7), [embarch-core/decisions.md](embarch-core/decisions.md) §3 decision 30 (`streams/`, retention, the parameterised route), [embarch-dev-bench/design.md](embarch-dev-bench/design.md) §3 decision 29 (dev-bench stops interpreting payloads; decision 22 marked **superseded**), [embarch-api/design.md](embarch-api/design.md) §3 decision 39, [embarch-ui/design.md](embarch-ui/design.md) §3 decision 10, and a row in [embarch-decision-reversals.md](embarch-decision-reversals.md). One genuinely new source variant the proposal never had, added by the outpost: **`StreamSource::Signal { name }`** — a signal **Core reads itself**, over a wire that bypasses dev-bench, with the carrier resolved by [embarch-topology](embarch-topology/design.md) §3 decision 18 rather than named in the study.

**Update 2026-08-25, second pass:** one more piece of the inbound half — §5's `DataChannel` collapse (below: "`DataChannel::PowerSamples | SensorWaveform` -> `DataChannel::Stream { name }`") — has now also been accepted, into [embarch-study-designer/design.md](embarch-study-designer/design.md) §3 decision 19's own amendment rather than into decision 39. It was deliberately left out of the first fold-in, and was the third of the open questions Phase A left behind. What that pass reached is close to this proposal's shape but not identical, and the difference is worth recording: a stream-named source **carries no `step_index` at all**, because a tap's scope is declared rather than per-step. This proposal kept `ValidationSource`'s `step_index` alongside the new variant, which would have asked authors for a field with no meaning.

**Update 2026-08-25, third pass — the accepted half is now partly *implemented*, not just folded in.** Milestone 7 Phase B item 0 shipped `streams_crc`, `Step.power_sample`'s retirement, and the `ValidationSource` reshape above, at schema **v9** (this file's own 5 → 6 went stale twice over). Two things worth carrying back here, since this proposal argued the change was cheap and one of them qualifies that: the `DataChannel` collapse landed as **two variants plus a separate `ValidationSource::Tap`** rather than a `DataChannel::Stream { name }` variant, for the `step_index` reason the second pass above records; and the dev-bench half cost **+654 bytes of firmware**, not the shrink §5 assumed, because dev-bench's decoder never walked the `streams` span a seal over it has to cover. Still not built, and still what §5 describes: `streams/`, retention, the parameterised route, and dev-bench's payload-interpretation deletion.

**Update 2026-08-25, fourth pass — the host end of the accepted half is now real.** Milestone 7 Phase B item 1 built `embarch-core`'s side: `study_results/<id>/streams/`, one file per declared tap, replacing the three fixed CSV writers this proposal called out by name (§3's table, §7's "`data.csv` / `waveform.csv` as special-cased writers" row), with the old routes surviving as endpoint aliases exactly as §7 predicted. Two things this proposal did not anticipate, both now recorded in [embarch-core/decisions.md](embarch-core/decisions.md) §3 decision 30: a per-study `streams/index.json` is *required* for those aliases to work at all, because the handler serving one holds no `Study`; and a `Text`-encoded tap gets one file rather than two, since its decode is the identity — §5's proposed `streams/<name>.{log,csv,bin}` triple over-counts by one for that case. **Item 2 followed the same day and built `embarch-api`'s own tool surface**: `study_stream_data { study_id, name, raw? }` and `list_study_streams { study_id }`, with the three per-channel tools kept unchanged as aliases for one release — the client-side mirror of the endpoint aliases §7 predicted. One thing this proposal is worth checking against there too: §5 imagined reading a capture by naming it, and said nothing about how a caller *learns* the names. `list_study_streams` is that, and its real content turned out to be `truncated` rather than the names — a capture that lost data must not read as a whole one, and the three aliases structurally cannot say. **What is still not built from the inbound half: dev-bench's payload-interpretation deletion (item 3)**, which is the piece this proposal opened with and the only one that removes the `f32` interpretation sitting in shipped firmware.

**What did not change, and is still only proposed:** the entire **write direction** — `Action::StreamSend`, `StreamExpect`, and the scripted-shell-interaction case (§4.2, §4.3, §7). Nothing in the suite sends anything to a DUT this way yet, and the outpost is TX-only from the DUT, so adopting a step type nothing emits would be building an unused capability. §10's fold-in table below is **stale for the inbound half** — the decision numbers it reserved were taken by different, unrelated decisions before this was accepted (Milestone 6 landed first), and the real numbers are the ones listed above.

This file therefore survives rather than being deleted per §10's original plan: half of it is now history, half of it is still a live proposal. Spans four repos (`embarch-study-designer`, `embarch-dev-bench`, `embarch-core`, `embarch-api`) plus the `embarch-ui` Study Designer tab, which is why it sits at this repo's root rather than in one sub-project's folder (`DOC-PROTOCOL.md` §3).

**In one line:** the suite is on its way to three near-identical capture pipelines that differ only in what the bytes mean — replace them with one, where the *source*, the *sink*, and the *decoding* are declared parameters, the firmware never interprets a payload, and everything a study does to a DUT stays authored up front and CRC-sealed.

**Revision history, because each revision changed the shape rather than the detail.**

- **v1** answered "can I get the NUS logs during a study?" with a third capture channel (`LogStart`/`LogChunkBatch`/`LogEnd`, `Study.log_tap`, `device-log.txt`, `/device-log`, `study_log_data`) alongside power and sensor-waveform. Wrong shape: a device log and a PPG waveform are *the same operation* — subscribe to a notify characteristic, forward what arrives, write it down incrementally — differing only in how the bytes are rendered. A third parallel pipeline would have set the pattern that every future kind of data needs its own.
- **v2** generalized to one pipeline with a declared source and encoding.
- **v3** made it bidirectional with a live, mid-study console (`StreamWrite` at any time, `POST /study/{id}/stream/{name}`, a cancel endpoint, a terminal pane). **Overshot the requirement and is withdrawn** — see §7's own note.
- **v4 (this one)** puts the write direction where it belongs: **an action step, authored with the study**. The engineer types the string at authoring time, optionally names a string to confirm against the DUT's log output, and the whole thing is sealed into `Study.steps` like every other step. This is strictly smaller than v3 — it deletes the largest firmware change, the new HTTP surface, the cancel-endpoint dependency, and the reproducibility problem, all at once, and needs no new message from Core to dev-bench at all.

## 1. What's actually there today

Three pipelines converging on the same shape by accident rather than by design:

| | Source | Wire | Sink | Ever run? |
|---|---|---|---|---|
| Power | dev-bench's own sampling hardware | `StreamStart`/`StreamChunkBatch`/`StreamEnd`, `StreamChannel::Power` | `data.csv` | **No** |
| Sensor waveform | a GATT notify characteristic (`GattOperation::StreamCapture`) | same, `StreamChannel::SensorWaveform` | `waveform.csv` | **No** |
| GATT activity | every notify characteristic (`GattMonitorAll`) | inline in `StepResult.gatt_activity` | `events.json` | Yes — came back empty |
| *(device log)* | *a GATT notify characteristic* | *— nothing —* | *—* | *n/a* |
| *(shell interaction)* | *write a string, watch the log for a response* | *— nothing —* | *—* | *n/a* |

The middle two rows are the same operation. The first differs only in where the bytes originate. The last two are the gaps that opened this proposal, and both are served by the same tap.

**The timing point that makes this cheap:** *nothing has ever put a single sample through the streaming path.* [embarch-study-designer/design.md](embarch-study-designer/design.md) §3 decision 25's own index row says so — "UART baud rate/Core CSV-writing consumption not yet exercised — no hardware streams samples yet" — and [embarch-roadmap.md](embarch-roadmap.md) Milestone 4 exists precisely to "exercise `PowerSampleWindow`/`StreamChunkBatch` end-to-end for the first time." The types are shipped, Core's CSV writers are written, and no real byte has crossed either. Generalizing now costs a schema bump and some deletions; generalizing after Milestone 4 costs migrating the one thing that will by then be load-bearing. **This is the cheapest this change will ever be**, and the window closes at Milestone 4.

**The second, sharper reason — and it is worse than the docs alone suggest.** [embarch-dev-bench/design.md](embarch-dev-bench/design.md) §3 decision 22 has `main.c`'s stream handler decoding "each raw notification as a sequence of little-endian `f32` values," with a real `unit`/`channel_id` mapping deferred to "a compile-time constant per board/sensor." That is **an assumption about what a DUT's bytes mean** — the category [embarch-study-designer/design.md](embarch-study-designer/design.md) §3 decision 35 rules out: *no EmbArch component should ever present an inference about what a specific piece of hardware or firmware does as established fact.* A plausible guess (many sensor streams are f32 arrays) that is wrong for a log, wrong for a packed 16-bit ADC stream, wrong for anything framed.

Reading the doc, that assumption looks like unwritten firmware. **Reading the code, it is already in the shipped wire type**, which is a stronger reason to act and was worth checking rather than assuming (§1.1):

```rust
StreamChunkBatch {                      // embarch-study-designer/src/protocol.rs
    base_utc_ms: u64,
    sample_interval_ms: u32,            // <- assumes evenly-spaced samples
    unit: Unit,
    channel_id: u8,
    values: Vec<f32, MAX_BATCH_SAMPLES>, // <- f32, not bytes
}
```

Two commitments baked in, not one. **`values: Vec<f32>`** means the only thing this link can carry is decoded floats — a log line has no representation here at all. And **`base_utc_ms` + `sample_interval_ms`** reconstructs each timestamp as `base + i * interval`, a model that is right for a sampler ticking at a fixed rate and structurally wrong for anything asynchronous: a notification arrives when the DUT decides to send it, and no interval reconstructs that. Neither is a firmware detail that could be fixed in firmware — both are the wire type, in the crate all three components compile in.

### 1.1 Verified against the code, not just the docs

Every load-bearing claim above was checked against the real sibling repos rather than taken from these docs, which is how the two corrections in this section were found. What holds, what didn't, and one thing nobody had noticed:

| Claim | Verdict |
|---|---|
| `STUDY_DESIGNER_SCHEMA_VERSION == 4`, `StreamChannel { Power, SensorWaveform }`, `DataChannel` has `PowerSamples`/`SensorWaveform`, `StepResult` carries `power_samples_ref`/`waveform_ref`, `GattOperation::StreamCapture` exists | **Confirmed**, all as documented |
| Core really does write `data.csv`/`waveform.csv` and serve them (`study.rs`, `serve_study_csv`) | **Confirmed** |
| The f32 assumption is planned firmware, not yet written | **Wrong as stated** — it is in the shipped `StreamChunkBatch` wire type, plus an evenly-spaced-timestamp model the docs never mention. Corrected above |
| `StreamChunkBatch` replaced `StreamChunk` (decision 25) | **Not quite** — both variants are still live in `DevBenchMessage`, and `study.rs` handles both (two separate match arms). One more thing the reshape gets to collapse |
| The link has no notion of text | **Wrong** — `DevBenchMessage::LogLine { text: String<MAX_LOG_LINE_LEN> }` already exists. See below; this is a naming hazard, not a solution |

**The `LogLine` collision, worth stating loudly.** `DevBenchMessage::LogLine` is **dev-bench's own firmware log** ([embarch-dev-bench/design.md](embarch-dev-bench/design.md) §3 decision 7), not the DUT's — framed properly rather than interleaved as raw bytes, which would corrupt COBS framing. So "log" in this protocol already means something, and it is not what this proposal is about. Anything named here must not blur that: a DUT's log arrives as a `Text`-encoded **stream tap**, dev-bench's own log stays `LogLine`. Two sources, two mechanisms, one word — name the tap after the DUT (`console`, `dut-log`) rather than reusing "log" bare.

**Incidental gap found while checking.** Core's handler for dev-bench's `LogLine` is one line — `tracing::debug!(study_id, "dev-bench: {text}")` (`study.rs`). Dev-bench's own log during a study goes to Core's rolling log file and **never reaches that study's results directory**, so debugging a study after the fact means correlating two files by timestamp. Not this proposal's job to fix, and not a blocker — but once `streams/` exists, giving dev-bench's own log a reserved tap there is nearly free, and worth doing in the same pass rather than leaving the asymmetry.

## 2. Non-goals

- **Ships no knowledge about any specific DUT.** No NUS UUID constant, no "NUS means logs," no payload-format guess, no shell grammar, no prompt detection anywhere in this suite's code. Every interpretation is declared by whoever actually knows: the engineer for a DUT's characteristics and strings, dev-bench for its own power front end.
- **No live/interactive console** — withdrawn with v3, see §7. Everything a study sends to a DUT is authored before submission and sealed by `steps_crc` (§3 decision 17).
- **Does not replace `serial_log`** ([embarch-decision-reversals.md](embarch-decision-reversals.md) row 11) or **`GattMonitorAll`** — see §8.
- **Does not fix the ~50% DUT connect-and-discover flake rate** (milestone 9 §6). A tap sits downstream of a working connection and inherits it.

## 3. The pipeline

One mechanism, four declared parameters: **where bytes come from, where written bytes go, how long the tap lives, and how to render what arrives.**

```
                              dev-bench                          host (Core)
                        (moves bytes both ways,             (decodes, renders, appends,
                          never interprets)                        serves)

  GattNotify{svc,chr} ──┐                                 ┌──> Text ─────> streams/<name>.log
                        ├─> StreamOpen{id}                │                (inbound + outbound)
  PowerFrontEnd{hz} ────┘    StreamChunkBatch{id,          ├──> Samples{layout,unit,
                              [{rx_utc_ms,outbound,bytes}]}│      channel_id} -> <name>.csv
                             StreamClose{id,dropped}       └──> Raw ──────> streams/<name>.bin

  GattWrite{svc,chr}  <───  Action::StreamSend{stream_id, payload, expect}
                            ── dispatched by dev-bench as an ordinary step,
                               from the Study it already received ──
```

Two load-bearing properties:

1. **dev-bench moves bytes and stamps arrival times. It never interprets a payload.** Interpretation happens host-side, where `std`, a growable buffer, and the engineer's own declared choice all live. That is what collapses three pipelines into one, and it is decision 35's principle applied to the read direction.
2. **The write direction needs no new message and no new lifecycle.** A `StreamSend` step arrives inside the `Study` dev-bench already receives, and executes in order like every other step. Core sends nothing mid-study; dev-bench's receive-then-run loop is unchanged.

## 4. `embarch-study-designer` — types

### 4.1 Taps

`Study` gains one top-level field, sibling to `steps`/`validations`:

**`streams: heapless::Vec<StreamTap, {limits::MAX_STREAMS_PER_STUDY}>`**

```
StreamTap {
    id: u8,                                        // wire handle; its index in Study.streams
    name: heapless::String<{limits::MAX_NAME_LEN}>, // names the output file, the SSE filter,
                                                    // and the post-hoc validation source
    source: StreamSource,                           // inbound: where bytes come from
    sink: Option<StreamSink>,                       // outbound: where a StreamSend step writes
    encoding: StreamEncoding,
    scope: StreamScope,
}

StreamSource   ::= GattNotify { service_uuid: Uuid, characteristic_uuid: Uuid }
                 | PowerFrontEnd { sample_rate_hz: u32 }

StreamSink     ::= GattWrite { service_uuid: Uuid, characteristic_uuid: Uuid,
                               with_response: bool }

StreamEncoding ::= Raw
                 | Text { line_ending: LineEnding }
                 | Samples { layout: SampleLayout, unit: Unit, channel_id: u8 }

SampleLayout   ::= LeF32 | BeF32 | LeI16 | LeU16 | LeI32   // append-only, grows on demand
LineEnding     ::= Lf | CrLf | Cr | None

StreamScope    ::= Study | Step { step_index: u32 }
```

- **Raw UUIDs**, per §4.3's existing raw-not-symbolic stance, sourced from the engineer through `embarch-ui`'s merged action list (live `GattDiscover` plus static `GattConfigExtractor` output, decision 34) — never from a constant in this crate.
- **`sink` is `Option`** because most taps are read-only: a power trace and a PPG waveform have nothing to write back to. A console tap declares both — notify characteristic in, write characteristic out — and that pairing is the engineer's declaration, not something inferred from a service UUID. Declaring it once on the tap, rather than per step, is also better authoring: many `StreamSend` steps, one place that says what "the console" is.
- **`with_response`** distinguishes ATT write-with-response from write-without-response. Which one a characteristic supports is visible in its discovered properties byte (§4.3a) and picking wrong silently fails on some stacks; the UI defaults it from the discovered properties and lets the engineer override.
- **`line_ending`** lives on the encoding so a string authored once behaves identically from the UI, the CLI, or a JSON study file. Shells differ (`\n` vs `\r\n`); this suite does not get to assume.
- **`scope`.** A PPG capture characterizing one step uses `Step { step_index }`, bounded by that step's `timeout_ms` exactly as `GattOperation::StreamCapture` was. A log or console tap uses `Study` — the point of a log is seeing what the DUT printed during the step that failed *and* the reconnect after it.
- **`name` must be unique within a `Study`, and `dev-bench` is reserved** (§6 — Core auto-creates that tap for dev-bench's own firmware log). Both enforced in Core's existing pre-flight validation (§3 decision 18).
- **`encoding` is host-only and never crosses to dev-bench.** Same split `Study.validations` already has (decisions 17/19): dev-bench receives a reduced `StreamArm { id, source, sink, scope }` list, sent as its own message right after `StudyStart`, leaving `steps_crc`'s coverage and the existing `StudyStart` decode path untouched.

### 4.2 The write step

A new `Action` variant — the thing you author when you want dev-bench to type something at the DUT:

```
Action::StreamSend {
    stream_id: u8,                                          // a tap that has a sink
    payload: heapless::Vec<u8, {limits::MAX_PAYLOAD_LEN}>,  // the string, already line-terminated
    expect: Option<StreamExpect>,
}

StreamExpect {
    stream_id: u8,                                      // which tap to watch (usually the same one)
    contains: heapless::Vec<u8, {limits::MAX_EXPECT_LEN}>,
    timeout_ms: u32,
}
```

- **`payload` is bytes, already terminated** with the tap's `line_ending` by whatever authored it (the UI, or the engineer writing the JSON). Firmware stays dumb: it writes exactly these bytes and appends nothing.
- **`expect` is the confirmation**, and it is what makes this a *test* rather than a fire-and-forget write. Dev-bench watches the named tap's inbound bytes for `contains` as a **raw byte-substring match**, from the moment the write completes until `timeout_ms` expires: `Outcome::Pass` on a match, `Outcome::TimedOut` if it never arrives, `Outcome::Fail { reason }` if the write itself failed. No new `Outcome` vocabulary, and it feeds `continue_on_fail` (§3 decision 13) exactly like every other step — which is the whole reason this is a real-time firmware-side check and not a post-hoc one (§3 decision 19: dev-bench can't know a post-hoc result in time to decide whether to continue).
- **A byte-substring search is not an interpretation.** Dev-bench doesn't need to know the payload is text, where a line ends, or what the DUT meant — only whether a given byte sequence appeared. It needs a rolling carry-over buffer of `len(contains) - 1` bytes so a match spanning two notifications isn't missed. That is the entire algorithm, and it keeps decision 35's line intact: the *string* comes from the engineer, the *matching* is mechanical.
- **`expect.stream_id` is separate from the write's `stream_id`** so a study can write to a control characteristic and confirm on the log characteristic. It usually points at the same tap; costing nothing to allow both is better than discovering the restriction later.
- **`expect` matches only what arrives after the write.** Bytes already in flight before the step started don't count, which is what makes a sequence of `StreamSend` steps behave the way an author expects rather than matching a previous command's output.
- Nothing lands in `StepResult` — the transcript is in the stream file, the verdict is the existing `Outcome`. **This design adds no bytes to `StepResult`** (and §4.4 removes two fields from it).
- **Pre-flight validation** (§3 decision 18, extended): `stream_id` in bounds, the write tap has a `sink`, and both taps' `scope` covers the step. Rejected with a `400` at `POST /study`, by name, rather than failing three hops away.

### 4.3 Wire

`DevBenchMessage` variants, replacing `StreamStart`/`StreamChunkBatch`/`StreamEnd`:

- **`StreamOpen { id: u8 }`** — dev-bench→Core, once per tap when it arms.
- **`StreamChunkBatch { id: u8, records: heapless::Vec<StreamRecord, {limits::MAX_BATCH_SAMPLES}> }`**, where **`StreamRecord { rx_utc_ms: u64, outbound: bool, bytes: heapless::Vec<u8, {limits::MAX_PAYLOAD_LEN}> }`** — one record per received notification (or per power-sampler read), payload verbatim, dev-bench's own timestamp (same convention as `Sample.rx_utc_ms`/`GattActivityRecord.rx_utc_ms`). `outbound` is set for the record dev-bench emits for its own `StreamSend` write, so the transcript interleaves both directions at their true times rather than Core guessing placement from step boundaries. One `bool`, and it is the entire cost of an accurate transcript.
- **`StreamClose { id: u8, dropped: u32 }`** — once per tap, carrying the inbound drop count so the host writes an explicit gap marker rather than presenting a lossy capture as complete.
- **`StreamArm { taps: heapless::Vec<ArmedTap, {limits::MAX_STREAMS_PER_STUDY}> }`** — Core→dev-bench, the reduced `{ id, source, sink, scope }` form of §4.1, sent once after `StudyStart`.

**No Core→dev-bench message exists after `StreamArm`.** The link keeps its submit-then-listen model exactly as it is today — the property v3 broke and this version restores.

**This reshapes existing variants rather than appending, which §3 decision 10's append-only discipline normally forbids.** Justified exactly once, and only now: no deployed firmware and no host has ever put a real byte through `StreamChunkBatch`, so there is no compatibility to preserve — only a schema-version bump (4 → 5). A stale dev-bench then fails loudly at the `Hello`/`HelloAck` mismatch check (decision 12) rather than silently misdecoding, and `embarch-umbrella`'s stale-firmware doctor check ([embarch-dev-bench/design.md](embarch-dev-bench/design.md) decision 25) catches it a step earlier. After Milestone 4 this paragraph would not be writable.

### 4.4 Host-side rendering and results

The crate owns each encoding's output format behind its existing `std` feature, per §3 decision 2 (anything every consumer must agree on column-for-column lives in the crate, not reimplemented in Core):

- **`Text`** → UTF-8-lossy, reassembled into lines across record boundaries (a Zephyr log line routinely splits across notifications and carries ANSI escapes), rendered as `<utc_ms> [<step_index>] < <line>` inbound and `… > <line>` outbound. Greppable and `tail`-able, which is how anyone actually reads a log; step correlation from the prefix, direction from the marker.
- **`Samples { layout, unit, channel_id }`** → decode as many complete values as each record holds (trailing partial bytes counted and dropped, not silently absorbed), then the existing `Sample::to_csv_row` (§4.7), unchanged. Decision 22's firmware decode, moved host-side and made a declared parameter instead of a hardcoded guess.
- **`Raw`** → bytes appended verbatim. The escape hatch for a stream nobody has characterized yet — capture first, interpret later, strictly better than refusing to capture until someone can name the format.

Reassembly buffering stays Core-side (`std`, growable, no `no_std` consumer).

`StudyResult` gains **`streams: heapless::Vec<StreamRef, {limits::MAX_STREAMS_PER_STUDY}>`** — `StreamRef { id, name, encoding, records: u32, dropped: u32, truncated_bytes: u64 }` — and `StepResult` **drops `power_samples_ref` and `waveform_ref`**. Net effect on the type two docs carry crash reports against ([embarch-core/decisions.md](embarch-core/decisions.md) decision 24, [embarch-api/design.md](embarch-api/design.md) decision 36): `StepResult` gets *smaller* by two `Option<heapless::String<64>>` × 64 steps; the small addition lands on `StudyResult` once rather than per-step.

`DataChannel` (§4.6) collapses to **`CapturedData | GattActivity | Stream { name }`**, replacing the fixed `PowerSamples`/`SensorWaveform` variants. Post-hoc validation gains something it didn't have: `Contains` over a `Text` stream is the first capture channel where the simplest possible byte check is also the one an engineer wants — §4.6 currently admits no check is authored against `GattActivity` at all. Note the two-tier split this creates, matching decision 19 exactly: **`StreamExpect` is the real-time check that can abort a study; a `PostHocValidation` over the same stream is the after-the-fact one that can't.** Both exist because they answer different questions.

## 5. `embarch-dev-bench` — firmware

- Handle `StreamArm`: for each `GattNotify` source, a targeted `bt_gatt_discover` on that one characteristic (not `GattMonitorAll`'s wildcard walk) plus a subscribe, on the first established connection; for a `PowerFrontEnd` source, start the sampler; for a tap with a `sink`, resolve that characteristic's handle at the same time so a later `StreamSend` needs no discovery round-trip. Emit `StreamOpen`, forward, emit `StreamClose` at the tap's scope boundary.
- Dispatch `Action::StreamSend` like any other step: one GATT write of `payload` to the resolved sink handle, emit an `outbound` record for the transcript, then — if `expect` is present — run the rolling substring match over the named tap's inbound bytes until it hits or `timeout_ms` expires, and report the step's `Outcome`. **No new inbound-serial handling, no concurrency with a running study, no change to the main loop's model.**
- **Delete the planned bytes→`Sample` decode** (decision 22's `ble_bridge_set_stream_handler` little-endian-f32 path). Never implemented; does not get implemented. The handler buffers raw payloads into a `StreamChunkBatch` and nothing else. The log feature arrives by *removing* code that was going to be written — the clearest signal the generalization is the right shape.
- **Static buffers, sized before implementing, not after a crash.** Decision 21 already had to move `serial_protocol.c`/`main.c` off stack scratch onto `static` buffers once real message sizes were known, and [embarch-study-designer/design.md](embarch-study-designer/design.md) §7 still carries the same unresolved warning for `gatt_activity`. The ESP32-C5 build is at **90.87% SRAM** (milestone 9, 2026-08-20) — the tightest constraint here and the first thing to measure. N concurrent taps share one batch buffer pool, not one buffer each; the `expect` matcher needs only its small carry-over window.
- **Overflow: drop, count, report.** Oldest inbound records dropped, counter carried in `StreamClose`, gap marker written by the host. Matches `Sample::to_csv_row`'s "log and skip rather than truncate silently" posture (§4.7) and Core's SSE `event: lagged` frame. One consequence worth stating: a dropped record can cost an `expect` its match, so a `TimedOut` on a busy stream is ambiguous between "never sent" and "dropped." The `dropped` count is what disambiguates it after the fact.

## 6. `embarch-core`, `embarch-api`, `embarch-ui`

**Core.** `study_results/<study_id>/streams/<name>.{log,csv,bin}`, one file per tap, appended incrementally as batches arrive — the durability posture `data.csv` already had (real from the first batch, surviving a crash that writes the study off as failed). Core stamps each `Text` line with the step open at the time, from its own live job state, exactly as it already appends `core_rx_utc_ms` to CSV rows.

- **`GET /study/{study_id}/streams`** → the `StreamRef` list.
- **`GET /study/{study_id}/stream/{name}`** → raw bytes, `Content-Type` by encoding; `404` if no such tap. Bytes, not a path — Core and `embarch-api` aren't guaranteed to share a filesystem (§5.1).
- `/power-data` and `/waveform-data` **stay as thin deprecated aliases** over conventionally-named taps. They're shipped and documented; an alias is three lines.
- The SSE `SampleBatch` event becomes **`StreamData { id, name, records }`** on `GET /study/{study_id}/events` (decision 24's broadcast) — any stream tails live while the study runs, outbound lines included, so watching a `StreamSend` step is watching the command and the response arrive in order.
- **No new write endpoint, and `POST /study/{id}/cancel` is not needed** — v3's dependency, gone with v3.

**The reserved `dev-bench` tap (§1.1's incidental gap, now in scope).** Core auto-creates one `Text` tap per study, named `dev-bench`, fed by the existing `DevBenchMessage::LogLine` handler instead of that handler's current lone `tracing::debug!`. It is not authored, does not appear in `Study.streams`, and does not consume a `MAX_STREAMS_PER_STUDY` slot — but it *does* appear in `StudyResult.streams` and is served by the same `/stream/{name}` endpoint, so dev-bench's own firmware log lands beside the DUT's in the same directory, on the same timeline, instead of in Core's rolling log file where correlating it means matching timestamps across two files. The `tracing::debug!` line stays as well; it costs nothing and Core's own log is still where you look when there is no study. **`dev-bench` becomes a reserved tap name**, rejected by pre-flight validation (§3 decision 18) with a `400` if a `Study` tries to author one.

### 6.1 Retention — the one place this feature breaks the suite's existing posture

Every other artifact this suite writes is small and bounded. A `Text` stream is neither, and it is the first thing here that grows without limit both *within* a run and *across* runs. Those are two independent problems and need two independent bounds; solving only one leaves the other unbounded.

**Within one study — a per-tap byte cap, segment-rotated, keeping the tail.** `<name>.log` is appended until it reaches `EMBARCH_STREAM_MAX_BYTES` (default **32 MiB**), then rolls to `<name>.1.log` and a fresh `<name>.log` starts; at the next roll the old `.1` is unlinked. Two segments, so a tap costs at most 2× the cap and Core only ever appends or unlinks — it never rewrites a file to make room. Reading the stream concatenates segments oldest-first, server-side, so `GET /study/{id}/stream/{name}` is unchanged from the caller's view.

Keeping the **tail** rather than the head is deliberate: a study you are reading a log for usually failed, and it failed at the end. Losing the boot banner is survivable; losing the crash is not.

**Truncation is stated, never silent** — the suite's existing rule everywhere else (`Sample::to_csv_row` logs and skips rather than truncating a row, the SSE surface emits an explicit `event: lagged`, `StreamClose.dropped` counts drops). A roll writes a marker line into the new segment (`… <N> bytes dropped by rotation …`) and increments a `truncated_bytes` counter carried in `StreamRef`, so `events.json` states plainly that a capture is partial. A stream that fits states `truncated_bytes: 0` and is exactly as trustworthy as it was before.

**Across studies — keep the last N result directories, swept at `POST /study`.** `study_results/` has no expiry at all today (§5.1: the in-memory registry dies with Core, the on-disk files outlive everything). Core sweeps oldest-first down to `EMBARCH_STUDY_RESULTS_KEEP` directories (default **50**; `0` disables sweeping entirely) at the moment a new study is accepted — no background timer, no new lifecycle, and the sweep runs exactly when new data is about to be created. The whole `study_results/<id>/` directory goes, not just its streams: `events.json` and the CSVs are the same disk.

Count-based rather than age-based or size-budgeted, for three reasons: it needs no clock (dev-bench's UTC is already the shakiest timing surface here), it is deterministic to reason about, and it is one policy rather than two knobs that can disagree. If 50 studies of 64 MiB each is the wrong bound for a real machine, the cap is the knob to turn — adding a byte budget on top would be a second mechanism to explain.

**A swept study logs its own deletion at `info`** and afterwards `404`s exactly like an unknown `study_id`. Not distinguishing the two is a real (small) loss of fidelity, accepted deliberately: the alternative is a persistent index of things that no longer exist, which is a database in the shape the suite has consistently refused (`embarch-api/design.md` §3.6).

Both knobs are environment variables rather than config-file keys, matching `EMBARCH_TOKEN`/`EMBARCH_DEV_BENCH_PORT`/`EMBARCH_DEV_BENCH_INTERFACE` — Core's own `core.toml` (§3 decisions 11/23) was never actually written and is narrowed to bind/port anyway, so an env var is the existing pattern, not a new one.

**`embarch-api`.** `study_streams` and `study_stream_data { study_id, name }`, MCP tools *and* CLI subcommands both (§3 decision 6's symmetry rule isn't optional). `study_power_data`/`study_waveform_data` stay as aliases.

**`embarch-ui` Study Designer tab** — where authoring actually happens:

- A **Streams** section beside the step table: pick a characteristic from the merged action list the step builder already uses, name it, choose an encoding, choose study-wide or one step, and optionally pair it with a write characteristic. A NUS console log is *two clicks and a name* — characteristic, `Text` — with no NUS knowledge anywhere in this suite, no new firmware feature, and no new `Action`.
- A **`StreamSend` row type** in the step table: choose the tap, type the string, optionally type the expected response and a timeout. That is the whole authoring flow for "send `kernel uptime`, confirm the DUT printed `uptime:`."
- Both persist as presets in decision 35's existing `study-actions.toml`, so a characteristic's format and a repo's useful commands are declared once per firmware repo rather than retyped per study.
- Per-stream live tail panes while a study runs — read-only, since there is nothing to type into.

## 7. Free text, and why it doesn't erode decision 35

Decision 35's registry is deliberately enumerated-values-only: a registered action's payload is "one or more named fields, each with a small enumerated set of engineer-supplied `{label, value}` pairs," with no free-text entry, precisely so nobody uses a value whose meaning nothing recorded. A shell command is free text, so `StreamSend` wants a free-text `ActionField` kind — and that is worth stating carefully rather than slipping in.

**The line decision 35 actually draws is *who authored the bytes*, not *whether they were enumerated*.** Its own text says the point is that "this knowledge only ever comes from the engineer, explicit and unambiguous," and that the failure it exists to prevent is *this suite* inferring what something does and presenting the inference as fact. An engineer typing a command they know into a study they are authoring is that knowledge arriving by the most direct route there is. What stays forbidden is unchanged: a value this suite generates, guesses, defaults, or labels with an invented description. No "suggested commands," no parsing the DUT's source for a shell command table, no help text this crate writes about what a command does.

**And v3's version of this was the actually-risky one, which is why it's withdrawn.** A live console makes a study non-replayable — its transcript depends on what somebody typed while it ran — and `Study` is "entirely static once submitted" (§4.1) for good reasons. Authoring the string up front keeps every one of them: the write is inside `Study.steps`, sealed by `steps_crc` (§3 decision 17), re-runnable, diffable, and reviewable before it ever reaches hardware. The interactive version also dragged in a cancel endpoint, a mid-study Core→dev-bench message, and concurrent inbound serial handling in firmware — all of which disappear here.

## 8. What this retires, and what it leaves alone

| Retired | Replaced by |
|---|---|
| v1 (`LogStart`/`LogChunkBatch`/`LogEnd`, `Study.log_tap`, `device-log.txt`, `/device-log`, `study_log_data`) | `StreamTap { source: GattNotify{…}, encoding: Text }` |
| v3 (`StreamWrite`/`StreamWriteAck`, `POST /study/{id}/stream/{name}`, `study_stream_write`, the console pane, `POST /study/{id}/cancel`, mid-study inbound serial in firmware) | `Action::StreamSend` — authored, sealed, dispatched as an ordinary step |
| `StreamChannel::Power \| SensorWaveform` (§3 decisions 20/21) | `StreamSource` + `StreamEncoding` |
| `StreamChunk { sample }` **and** `StreamChunkBatch { values: Vec<f32>, sample_interval_ms, … }` — both still live, both f32-only, one assuming evenly-spaced timestamps (§1.1) | one `StreamChunkBatch { id, records }` carrying raw bytes and real per-record timestamps |
| `GattOperation::StreamCapture` (§3 decision 21) | a `Step`-scoped `StreamTap`. Removed outright rather than kept as a second overlapping mechanism — the same call §3 decision 22 made when post-hoc validation made `Action::Validate` redundant |
| dev-bench's planned little-endian-`f32` decode ([embarch-dev-bench/design.md](embarch-dev-bench/design.md) decision 22) | `StreamEncoding::Samples { layout, … }`, declared host-side. **Never implemented; now never will be** |
| `DataChannel::PowerSamples \| SensorWaveform` | `DataChannel::Stream { name }` |
| `StepResult.power_samples_ref` / `.waveform_ref` | `StudyResult.streams: Vec<StreamRef>` |
| `data.csv` / `waveform.csv` as special-cased writers | `streams/<name>.csv`; old paths survive as endpoint aliases |

**Left alone deliberately.** `GattMonitorAll`/`gatt_activity` looks foldable — discover, subscribe to everything, capture — but its job is different: bounded reconnaissance whose result belongs *inline* in `events.json` beside the discovered GATT table, answering "what does this DUT even emit?" It is what you run *before* you know which characteristic deserves a tap, and its 32×512 ceiling is a feature for recon and a bug for capture. Re-expressing it as N auto-armed taps is a plausible later simplification, not this change. `serial_log` also stays as it is — dev-bench's link, unrelated hop. **"No cancel endpoint for v1" (§5.1) stays true**, unlike under v3.

## 9. Risks and pre-implementation checks

| Risk | Why it's real | What to do about it |
|---|---|---|
| dev-bench SRAM | Already at 90.87% on ESP32-C5 | Measure the shared batch pool first; shrink `MAX_BATCH_SAMPLES` and flush more often if needed. Static buffers only |
| Link/throughput ceiling | 1 Mbaud serial (decision 25); the DUT's BLE connection interval is the tighter bound in practice | Drives §5's overflow policy. Explicit gap markers, never silent loss |
| A dropped record can cost an `expect` its match | Makes `TimedOut` ambiguous between "never sent" and "dropped" | `StreamClose.dropped` disambiguates after the fact; surface it next to the step's outcome in the UI rather than only in the file |
| Connect/discover flakiness | ~50%, not root-caused (milestone 9 §6) | Out of scope, inherited. A working log tap would itself be a good instrument for root-causing it |
| Schema bump 4 → 5 with reshaped variants | Normally forbidden by decision 10 | Justified only because nothing ever streamed (§4.3); `Hello`/`HelloAck` (decision 12) plus the stale-firmware doctor check fail a lagging dev-bench loudly |
| `expect` timing | Matching bytes that arrived *before* the write would make chained `StreamSend` steps behave unpredictably | §4.2: the match window opens when the write completes, not when the step starts |
| Sweeping deletes results someone wanted | §6.1's keep-last-N runs automatically at `POST /study`, and a swept study is indistinguishable from an unknown one | Default 50 is generous, `EMBARCH_STUDY_RESULTS_KEEP=0` disables it entirely, and every sweep logs at `info`. Anyone treating `study_results/` as an archive should be copying out of it, which was already true before this change |
| Unverified DUT premise | Whether any specific DUT streams its console on subscribe, what it expects written, and what it prints back is **not established here** | By construction it doesn't need to be — the engineer names the characteristics, the command, and the expected response. The first real run against the reference-dut is the validation |

## 10. If accepted: where each piece folds in

Per `DOC-PROTOCOL.md` §5, on acceptance this content is written into the living docs and this file deleted, not left as a parallel source of truth. The stream generalization is a genuine **reversal**, not an addition, so [embarch-decision-reversals.md](embarch-decision-reversals.md) gets a row in the same pass: *"each kind of captured data gets its own channel, and dev-bench decodes payloads into `Sample`s"* → *"one pipeline; dev-bench never interprets a payload; the kind is a declared, engineer-supplied encoding."*

| Doc | Next free number | What lands |
|---|---|---|
| [embarch-study-designer/design.md](embarch-study-designer/design.md) | decisions **36**, **37** | 36: §4.1/§4.3/§4.4 (the pipeline). 37: §4.2's `Action::StreamSend` + `StreamExpect`, and §7's free-text boundary as an amendment to decision 35. §4.3 loses `GattOperation::StreamCapture` and gains `StreamSend`, §4.5 loses two `StepResult` fields and gains `StudyResult.streams`, §4.6's `DataChannel` collapses, new §4.8 for the stream types, §5.1/§5.2/§6 gain the new endpoints/files/tools; schema 4 → 5; `limits` changes: new `MAX_STREAMS_PER_STUDY`/`MAX_EXPECT_LEN`, and `MAX_BATCH_SAMPLES` (already 32) repurposed as the per-batch **record** count rather than sample count |
| [embarch-dev-bench/design.md](embarch-dev-bench/design.md) | decision **28** | §5 above; **decision 22 marked Superseded** — the first `Superseded` entry in either crate's index, worth stating plainly rather than quietly re-editing |
| [embarch-core/decisions.md](embarch-core/decisions.md) | decisions **30**, **31** | 30: §6's stream storage, endpoints, SSE, and the reserved `dev-bench` tap. 31: §6.1's retention policy — segment rotation and the keep-last-N sweep, plus `EMBARCH_STREAM_MAX_BYTES`/`EMBARCH_STUDY_RESULTS_KEEP`, which also want a row in [embarch-user-guide.md](embarch-user-guide.md) since they are the first knobs an operator may actually need to turn. §4's endpoint table, §8's `study.rs` note |
| [embarch-api/design.md](embarch-api/design.md) | decision **39** | §6's tools and subcommands |
| [embarch-ui/design.md](embarch-ui/design.md) | — | the Streams builder section, the `StreamSend` step row, per-stream live tail |
| [embarch-roadmap.md](embarch-roadmap.md) | Milestone **6** | **Sequence before Milestone 4 (Power-Sampling Study), not after** — Milestone 4 is what makes the current specific shape load-bearing, and it needs no hardware this change does |
| [embarch-features.md](embarch-features.md) | — | rows updated once shipped, not before |

## 11. Open questions

Four items in this section were resolved by review on 2026-08-25 and are recorded here as settled rather than deleted, since the reasoning is what a later reader will want:

- ~~**Whether `expect` should support more than `contains`**~~ — **resolved: `contains` only.** A regex or line-anchored match is meaningfully more firmware, and a richer check is already expressible post-hoc over the same stream, which is the cheap way to find out whether the real-time version is ever worth building. Revisit only with a real case that post-hoc validation genuinely can't serve.
- ~~**Retention**~~ — **resolved: specified in §6.1** (per-tap segment rotation keeping the tail, plus a keep-last-N sweep across studies, both env-var-tunable). Opened deliberately rather than deferred, because logs are heavy and this is the first artifact the suite writes that is unbounded in two independent directions.
- ~~**Sequencing against Milestone 4**~~ — **resolved: this goes first.** It needs no PPK2 and no hardware not already validated, and Milestone 4 is precisely what would make the current wire shape load-bearing (§1).
- ~~**Whether dev-bench's own `LogLine` gets a reserved tap**~~ — **resolved: in scope**, §6. Closes the §1.1 gap where dev-bench's firmware log during a study only ever reached Core's rolling log file.

Genuinely still open:

- **`MAX_STREAMS_PER_STUDY`, `MAX_EXPECT_LEN`, the repurposed `MAX_BATCH_SAMPLES`, and dev-bench's buffer pool sizes** — need the real link and real notification rates, same posture as every other hardware-unvalidated constant in these docs. §9's SRAM check is the binding one.
- **Whether `EMBARCH_STREAM_MAX_BYTES`' 32 MiB default and `EMBARCH_STUDY_RESULTS_KEEP`' 50 are the right numbers.** Both are reasoned, neither is measured — nobody has yet watched a real DUT log for a real study's duration. First real capture is what sizes them.
- **Whether `Samples` decoding belongs behind the existing `core-validation` feature** or plainly under `std`. Leaning plainly under `std` — byte-shuffling, not the numerics that motivated a separate feature.
- **Multi-value records for a genuinely multi-lead sensor** — `embarch-study-designer/design.md` §7's existing open item about `Sample`'s grain, unchanged; `SampleLayout` is where it would eventually be expressed.
- **Whether `GattMonitorAll` should later be re-expressed as N auto-armed taps** (§8). Plausible, not now.
