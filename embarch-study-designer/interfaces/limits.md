# embarch-study-designer: capacity limits

**Status:** active, 2026-09-07.

Every bound the crate declares, each marked `[measured <date>]` or `[assumed]`. Why they are fixed-capacity at all, and the two passes that shrank the types: [../decisions/limits.md](../decisions/limits.md). Types: [types.md](types.md).

**Every `[assumed]` value is placeholder-but-concrete**: chosen without hardware to size against, flagged for re-confirmation. **A value proving too small is a version-bumped breaking wire change, like any other field change.**

| Constant | Value | Bounds | Sizing |
|---|---|---|---|
| `MAX_STEPS_PER_STUDY` | 64 | `Study.steps`, `StudyResult.steps` | [assumed] |
| `MAX_STUDY_NAME_LEN` | 64 | `Study.name`, `StudyResult.study_name` | [assumed] |
| `MAX_NAME_LEN` | 32 | `Step.name`, `StepResult.step_name` | [assumed] |
| `MAX_SERVICE_UUIDS` | 4 | `BleAdvertise.service_uuids` | [assumed] |
| `MAX_LOCAL_NAME_LEN` | 26 | `BleAdvertise.local_name` | fits a legacy 31-byte BLE advertising PDU alongside AD-structure/flags overhead — not a round number |
| `MAX_PAYLOAD_LEN` | 512 | `GattOperation::Write.payload`, `StepResult.captured_data`, `ExpectedValue::Equals`/`Contains` | above BLE 5's practical extended-MTU ceiling (247-byte ATT_MTU / 251-byte L2CAP payload), not the legacy 23-byte default, so a single-PDU exchange never truncates |
| `MAX_FAIL_REASON_LEN` | 64 | `Outcome::Fail.reason`, `ContentValidity::Invalid.reason` | [assumed] |
| `MAX_CSV_ROW_LEN` | 96 | `Sample::to_csv_row`'s buffer (§4.7) | fits `rx_utc_ms` (up to 20 ASCII digits for a `u64`), a `MAX_NAME_LEN` step name, a formatted `value`, and separators |
| `MAX_LOG_LINE_LEN` | 128 | `DevBenchMessage::LogLine.text` (`embarch-dev-bench/design.md` §3 decision 7) | [assumed] one free-text log line dev-bench sends instead of raw interleaved bytes on the shared serial line |
| `MAX_FIRMWARE_VERSION_LEN` | 32 | `DevBenchMessage::HelloAck.firmware_version` (`embarch-dev-bench/design.md` §3 decision 18) | [assumed] a single free-form build identifier (e.g. `git describe` output) |
| `MAX_HARDWARE_ID_LEN` | 32 | `DevBenchMessage::HelloAck.hardware_id` (decision 47, `embarch-core/design.md` §3 decision 35) | double the 16 chars both of this suite's JTAG reads produce today; `hwinfo_get_device_id`'s length is a per-SoC driver decision this crate doesn't get to fix |
| `MAX_VERSION_OVERRIDES` | 2 | `Provenance.overrides` (decision 40, §4.5) | the arity of the thing, not a capacity guess: exactly two requirements exist (`dev_bench_version`, `firmware_version`) and an override names one |
| `MAX_STREAMS_PER_STUDY` | 8 | `Study.streams`/`StudyResult.streams` (decision 39, §4.8) | [assumed] deliberately small: a tap is a declared capture channel, not a per-step artifact |
| `MAX_STREAM_NAME_LEN` | 32 | `StreamTap.name`, `StreamRef.name` (§4.8) | [assumed] |
| `MAX_SIGNAL_NAME_LEN` | 32 | `StreamSource::Signal.name` (§4.8) | [assumed] |
| `MAX_STREAM_CHUNK_BYTES` | 512 | `StreamRecord.bytes` (§4.8) | [assumed] no real dev-bench UART throughput number and no real outpost capture exist to size against yet |
| `MAX_STREAM_RECORDS_PER_BATCH` | 4 | `DevBenchMessage::StreamChunkBatch.records` (§4.8) | [assumed] amortizes COBS/postcard framing overhead across a burst |
| `MAX_DISCOVERED_SERVICES` | 8 | `GattServiceInfo` per `StepResult.gatt_services` (decisions 31/32, §4.3a) | decision 57's validated GATT table: `reference-dut-fw` declares 3 services, transcribed from `src/limits.rs:80-84`, whose comment was written 2026-08-23; decision 44's validated-on-hardware discovery found 7 in total once an encrypted link reaches the rest (same DUT as `MAX_MONITOR_TARGETS` below) — with headroom for a DUT this crate hasn't seen yet |
| `MAX_CHARS_PER_SERVICE` | 16 | `GattServiceInfo.characteristics` (§4.3a) | [measured 2026-08-23, superseding a mismatched 2026-08-20 note in this file] that DUT's larger service (Sensor Data Service) declares up to 7 characteristics today (`src/limits.rs:85-88`): 6 unconditional, 1 gated behind `CONFIG_AIR_TEMP_ENABLE` |
| `MAX_MONITOR_TARGETS` | 16 | `Action::GattMonitorSelected`/`GattMonitorSelectedStart.targets` (decision 53) | [measured] against the largest real DUT walked (`reference-dut-fw`: 10 notify/indicate-capable characteristics across two services, 7 services in total once an encrypted link reaches the rest of the table), with headroom. A study wanting more wants `GattMonitorAll` |
| `MAX_RECORD_MAGIC_LEN` | 8 | `RecordFraming::MagicPrefixedCrc32Le.magic` | [assumed] `GWF1` and the WDS spill's magic are four bytes; eight leaves room without letting a "magic" become a header |
| `MAX_BAD_RECORDS_REPORTED` | 32 | `RecordReport.bad_offsets` | [assumed] the *count* of damaged records is never capped, only this list — thirty-two is enough to point at a pattern (a burst of losses, or one per hour), which is what an offset list is for; past that the count is the finding |
| `MAX_DECODERS_PER_STUDY` | = `MAX_STREAMS_PER_STUDY` | `Study.decoders` (decision 52) | the arity of the thing, not a guess: a decoder is reachable only through a tap's `StreamEncoding::Struct`, and there are at most that many taps |
| `MAX_DECODER_NAME_LEN` | 24 | `StructLayout.name` (§4.8a) | [assumed] |
| `MAX_STRUCT_FIELDS` | 12 | `StructLayout.header`/`repeat` (§4.8a) | [assumed] a real notification packet's header is a handful of fields and its repeating element smaller still |
| `MAX_STRUCT_FIELD_NAME_LEN` | 20 | `StructField.name` (§4.8a) | [assumed] becomes a CSV column header |
| `MAX_STRUCT_CSV_ROW_LEN` | 640 | one rendered decoded-struct CSV row's decoded columns, and the header naming them (§4.8a) | bounded by `MAX_STRUCT_FIELDS` × 2 groups × (a name or a rendered scalar), with room for separators — not by `MAX_GATT_CSV_ROW_LEN`, which sizes a row carrying a whole payload rendered twice |
| `MAX_GATT_CSV_ROW_LEN` | 1792 | one rendered `gatt.csv` row (decision 36, §4.3b) | sized to hold a `MAX_PAYLOAD_LEN` payload rendered *twice* (hex, then a printable-ASCII column) alongside two hyphenated UUIDs and the fixed columns — far larger than `MAX_CSV_ROW_LEN` because a GATT transcript row carries a raw payload where a `Sample` row carries one `f32`, and the two file formats are deliberately not sized against the same constant |

**`.eap` protocol manifests** (decisions 58–62). These bound a value dev-bench *executes*, not one it walks past: a `ProtocolDef` rides in `Study.protocols` all the way to the firmware, so every constant below costs real ESP32-C5 SRAM in `struct dev_bench_message`'s union. Sized against the two worked protocols in §4.9 with headroom, deliberately *not* against the generous ceilings the constants above use — dev-bench remains free to cap tighter still with its own internal limit, exactly as `DBM_MAX_STEPS_PER_STUDY` already does at 16 against `MAX_STEPS_PER_STUDY`'s 64 (`embarch-dev-bench/design.md` §3 decision 27). **The SRAM cost has not been measured** — the real number comes from a `west build` ram_report, which is `embarch-dev-bench`'s own scope along with the interpreter itself.

| Constant | Value | Bounds | Sizing |
|---|---|---|---|
| `MAX_PROTOCOLS_PER_STUDY` | 2 | `Study.protocols` (decision 58) | a protocol is only reachable through a `RunProtocol` step, and a study running more than a couple of distinct handshakes is describing two studies |
| `MAX_PROTOCOL_NAME_LEN` | 32 | `ProtocolDef.name` | [assumed] the `protocol <name> { … }` identifier |
| `MAX_SOURCES_PER_PROTOCOL` | 6 | `ProtocolDef.sources` (decision 58) | sized against the real BDS download's three (`ctrl`/`status`/`data`, decision 57) with room for a protocol spanning two services |
| `MAX_SOURCE_NAME_LEN` | 24 | `ProtocolSource.name` | [assumed] the alias a `write`/`frame` refers to |
| `MAX_FRAMES_PER_PROTOCOL` | 8 | `ProtocolDef.frames` | [assumed] only frames a state machine actually reacts to live here; a frame that exists solely to render a capture is a decision-52 `StructLayout` and never reaches dev-bench |
| `MAX_FRAME_NAME_LEN` | 32 | `FrameDef.name` | [assumed] referenced by `on_event <frame>` and by field paths |
| `MAX_FRAME_FIELDS` | 8 | `FrameDef.fields` (decision 59) | the **guard-reachable** scalar reads of one frame, not every field of the real packet — only the ones a `when`, a `remember` or a `write` names |
| `MAX_FRAME_SPANS` | 4 | `FrameDef.spans` | [assumed] a span's *bytes* never reach an expression (decision 60 removed byte-span concatenation outright); only its `len()` does |
| `MAX_EAP_FIELD_NAME_LEN` | = `MAX_STRUCT_FIELD_NAME_LEN` | `ScalarRead.name`/`SpanRead.name` | shares `MAX_STRUCT_FIELD_NAME_LEN`'s size on purpose: the same `.eap` frame can also be lowered into a decision-52 `StructLayout`, and a name that fit one and not the other would be a silent authoring trap |
| `MAX_SELECT_MATCH_LEN` | 8 | `FrameMatch.eq` (decision 59's `select_if`) | sized for a four-byte format magic (`GWF1`, `BSS\x03`) with headroom |
| `MAX_SESSION_VARS` | 6 | `ProtocolDef.session` (decision 60) | [assumed] integers only — the `bytes` session variable the draft carried is gone with `++` |
| `MAX_SESSION_VAR_NAME_LEN` | 24 | `SessionVarDef.name` | [assumed] referenced as `session.<name>` |
| `MAX_STATES_PER_PROTOCOL` | 12 | `ProtocolDef.states` | [assumed] the real BDS download uses six |
| `MAX_STATE_NAME_LEN` | 24 | `StateDef.name`, `ProtocolOutcome.final_state` (decision 62) | [assumed] the one string a protocol run reports back |
| `MAX_EVENT_ARMS_PER_STATE` | 4 | `ActiveState.on_event` | [assumed] distinct frames one state reacts to |
| `MAX_GUARDS_PER_ARM` | 2 | `EventArm.when` | more than one so an author can express a small dispatch without inventing intermediate states; small enough that a real branch stays legible |
| `MAX_REMEMBER_PER_ARM` | 2 | `EventArm.remember` | [assumed] session-variable updates one arm performs before its guards are evaluated |
| `MAX_WRITE_FIELDS` | 6 | `WriteAction.fields` (decision 61) | a control-point write is a one-byte opcode and occasionally an argument; sized for the argument |

Retired constants, kept here because a reader meeting the name in older code needs to know it went and why: ~~`MAX_RESULT_REF_LEN = 64`~~ and the original ~~`MAX_BATCH_SAMPLES`~~ role — `StepResult.power_samples_ref`/`waveform_ref`, retired 2026-08-25 with the fields (decision 39). ~~`MAX_GATT_ACTIVITY_RECORDS = 32`~~ — retired 2026-08-26 with the field it bounded (decision 54); it was what a capped in-memory copy of a streamed capture cost, and §7's stack-safety risk for it went with it. ~~`MAX_STREAM_CHUNK_LEN`~~ — nothing left to bound once `StreamChunk` carried a `Sample` rather than an arbitrary byte buffer. ~~`MAX_VALIDATIONS_PER_STUDY = 64`~~ — retired with post-hoc validation (decision 48).
