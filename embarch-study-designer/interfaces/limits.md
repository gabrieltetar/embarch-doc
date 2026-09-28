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
| `MAX_CSV_ROW_LEN` | 96 | `Sample::to_csv_row`'s buffer (`decoders.md`) | fits `rx_utc_ms` (up to 20 ASCII digits for a `u64`), a `MAX_NAME_LEN` step name, a formatted `value`, and separators |
| `MAX_LOG_LINE_LEN` | 128 | `DevBenchMessage::LogLine.text` (`embarch-dev-bench` decision 7) | [assumed] one free-text log line dev-bench sends instead of raw interleaved bytes on the shared serial line |
| `MAX_FIRMWARE_VERSION_LEN` | 32 | `DevBenchMessage::HelloAck.firmware_version` (`embarch-dev-bench` decision 18) | [assumed] a single free-form build identifier (e.g. `git describe` output) |
| `MAX_HARDWARE_ID_LEN` | 32 | `DevBenchMessage::HelloAck.hardware_id` (decision 47, `embarch-core` decision 35) | double the 16 chars both of this suite's JTAG reads produce today; `hwinfo_get_device_id`'s length is a per-SoC driver decision this crate doesn't get to fix |
| `MAX_VERSION_OVERRIDES` | 2 | `Provenance.overrides` (decision 40) | the arity of the thing, not a capacity guess: exactly two requirements exist (`dev_bench_version`, `firmware_version`) and an override names one |
| `MAX_STREAMS_PER_STUDY` | 8 | `Study.streams`/`StudyResult.streams` (decision 39) | [assumed] deliberately small: a tap is a declared capture channel, not a per-step artifact |
| `MAX_STREAM_NAME_LEN` | 32 | `StreamTap.name` (`taps.md`), `StreamRef.name` (`result-types.md`) | [assumed] |
| `MAX_SIGNAL_NAME_LEN` | 32 | `StreamSource::Signal.name` (`taps.md`) | [assumed] |
| `MAX_STREAM_CHUNK_BYTES` | 512 | `StreamRecord.bytes` | [assumed] no real dev-bench UART throughput number and no real outpost capture exist to size against yet |
| `MAX_STREAM_RECORDS_PER_BATCH` | 4 | `DevBenchMessage::StreamChunkBatch.records` | [assumed] amortizes COBS/postcard framing overhead across a burst |
| `MAX_DISCOVERED_SERVICES` | 8 | `GattServiceInfo` per `StepResult.gatt_services` (decisions 31/32) | decision 57's validated GATT table: `reference-dut-fw` declares 3 services, transcribed from `src/limits.rs:80-84`, whose comment was written 2026-08-23; decision 44's validated-on-hardware discovery found 7 in total once an encrypted link reaches the rest (same DUT as `MAX_MONITOR_TARGETS` below) — with headroom for a DUT this crate hasn't seen yet |
| `MAX_CHARS_PER_SERVICE` | 16 | `GattServiceInfo.characteristics` (`gatt-types.md`) | [measured 2026-08-23, superseding a mismatched 2026-08-20 note in this file] that DUT's larger service (Sensor Data Service) declares up to 7 characteristics today (`src/limits.rs:85-88`): 6 unconditional, 1 gated behind `CONFIG_AIR_TEMP_ENABLE` |
| `MAX_MONITOR_TARGETS` | 16 | `Action::GattMonitorSelected`/`GattMonitorSelectedStart.targets` (decision 53) | [measured] against the largest real DUT walked (`reference-dut-fw`: 10 notify/indicate-capable characteristics across two services, 7 services in total once an encrypted link reaches the rest of the table), with headroom. A study wanting more wants `GattMonitorAll` |
| `MAX_RECORD_MAGIC_LEN` | 8 | `RecordFraming::MagicPrefixedCrc32Le.magic` | [assumed] `GWF1` and the WDS spill's magic are four bytes; eight leaves room without letting a "magic" become a header |
| `MAX_BAD_RECORDS_REPORTED` | 32 | `RecordReport.bad_offsets` | [assumed] the *count* of damaged records is never capped, only this list — thirty-two is enough to point at a pattern (a burst of losses, or one per hour), which is what an offset list is for; past that the count is the finding |
| `MAX_DECODERS_PER_STUDY` | = `MAX_STREAMS_PER_STUDY` | `Study.decoders` (decision 52) | the arity of the thing, not a guess: a decoder is reachable only through a tap's `StreamEncoding::Struct`, and there are at most that many taps |
| `MAX_DECODER_NAME_LEN` | 24 | `StructLayout.name` (`decoders.md`) | [assumed] |
| `MAX_STRUCT_FIELDS` | 12 | `StructLayout.header`/`repeat` (`decoders.md`) | [assumed] a real notification packet's header is a handful of fields and its repeating element smaller still |
| `MAX_STRUCT_FIELD_NAME_LEN` | 20 | `StructField.name` (`decoders.md`) | [assumed] becomes a CSV column header |
| `MAX_STRUCT_CSV_ROW_LEN` | 640 | one rendered decoded-struct CSV row's decoded columns, and the header naming them (`decoders.md`) | bounded by `MAX_STRUCT_FIELDS` × 2 groups × (a name or a rendered scalar), with room for separators — not by `MAX_GATT_CSV_ROW_LEN`, which sizes a row carrying a whole payload rendered twice |
| `MAX_GATT_CSV_ROW_LEN` | 1792 | one rendered `gatt.csv` row (decision 36) | sized to hold a `MAX_PAYLOAD_LEN` payload rendered *twice* (hex, then a printable-ASCII column) alongside two hyphenated UUIDs and the fixed columns — far larger than `MAX_CSV_ROW_LEN` because a GATT transcript row carries a raw payload where a `Sample` row carries one `f32`, and the two file formats are deliberately not sized against the same constant |
| `MAX_BUILD_ID_LEN` | 128 | `OutpostHeader.outpost_version`, `OutpostHeader.build_id` | mirrors `CONFIG_EMBARCH_OUTPOST_BUILD_ID_MAX`'s Kconfig range max (confirmed 128, not drifted) — derived, not measured/assumed |

**`.eap` protocol manifest constants** (decisions 58–62, `MAX_PROTOCOLS_PER_STUDY` through `MAX_WRITE_FIELDS`) moved to [eap-limits.md](eap-limits.md) — a self-contained group of eighteen rows nothing outside protocol work reads, split rather than folded into [eap.md](eap.md) itself since that file had no headroom left for them. Same posture as every constant here: `[measured]`/`[assumed]` per row, placeholder-but-concrete unless marked otherwise.

## Advisory dev-bench capacities

**Advisory, never a gate, and nothing here branches on them** — mirrors of caps in `embarch-dev-bench`'s own headers (paths below are under `embarch-dev-bench/app/src/`), served so an authoring host can *warn*. Why: [../decisions/limits.md](../decisions/limits.md) decision 76.

| Constant | Value | Mirrors | Why the bench is tighter |
|---|---|---|---|
| `DEV_BENCH_MAX_STEPS_PER_STUDY` | 16 | `DBM_MAX_STEPS_PER_STUDY` (`serial_protocol.h:54`), embarch-dev-bench decision 27 | `struct dbm_step`'s action union at this crate's 64 slots does not fit that board's RAM |
| `DEV_BENCH_MAX_EVENT_ARMS_PER_STATE` | 2 | `EAP_MAX_EVENT_ARMS_PER_STATE` (`eap.h:90`), embarch-dev-bench decision 41 | an arm is the heaviest thing a state holds, multiplied by states, by protocols, and again by two static `struct dev_bench_message` copies |
| `DEV_BENCH_MAX_PROTOCOLS_WIRE_LEN` | 3072 | `DBM_MAX_PROTOCOLS_WIRE_LEN` (`serial_protocol.h:113-129`), embarch-dev-bench decision 41 | **mirrors no crate constant at all**: the count caps multiply into ~7.4 KB for one `ProtocolDef`, against 398 bytes for the real BDS manifest. Measured by `crc::protocols_wire_len`, which encodes the **whole field, length prefix included** |

Retired constants, kept here because a reader meeting the name in older code needs to know it went and why: ~~`MAX_RESULT_REF_LEN = 64`~~ and the original ~~`MAX_BATCH_SAMPLES`~~ role — `StepResult.power_samples_ref`/`waveform_ref`, retired 2026-08-25 with the fields (decision 39). ~~`MAX_GATT_ACTIVITY_RECORDS = 32`~~ — retired 2026-08-26 with the field it bounded (decision 54); it was what a capped in-memory copy of a streamed capture cost, and the stack-safety risk it carried went with it. ~~`MAX_STREAM_CHUNK_LEN`~~ — nothing left to bound once `StreamChunk` carried a `Sample` rather than an arbitrary byte buffer. ~~`MAX_VALIDATIONS_PER_STUDY = 64`~~ — retired with post-hoc validation (decision 48).
