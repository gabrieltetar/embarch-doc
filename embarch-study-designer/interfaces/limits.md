# embarch-study-designer: capacity limits

**Status:** active, 2026-09-02.

Every bound the crate declares, each marked `[measured <date>]` or `[assumed]`. Why they are fixed-capacity at all, and the two passes that shrank the types: [../decisions/limits.md](../decisions/limits.md). Types: [types.md](types.md).

**Every `[assumed]` value is placeholder-but-concrete**: chosen without hardware to size against, flagged for re-confirmation. **A value proving too small is a version-bumped breaking wire change, like any other field change.**

| Constant | Value | Bounds | Sizing |
|---|---|---|---|
| `MAX_STEPS_PER_STUDY` | 64 | `Study.steps`, `StudyResult.steps` | [assumed] |
| `MAX_STUDY_NAME_LEN` | 64 | `Study.name`, `StudyResult.study_name` | [assumed] |
| `MAX_NAME_LEN` | 32 | `Step.name`, `StepResult.step_name` | [assumed] |
| `MAX_SERVICE_UUIDS` | 4 | `BleAdvertise.service_uuids` | [assumed] |
| `MAX_LOCAL_NAME_LEN` | 26 | `BleAdvertise.local_name` | fits a legacy 31-byte BLE advertising PDU alongside AD-structure/flags overhead — not a round number |
| `MAX_PAYLOAD_LEN` | 512 | `GattOperation::Write.payload`, `StepResult.captured_data` | above BLE 5's practical extended-MTU ceiling (247-byte ATT_MTU / 251-byte L2CAP payload), not the legacy 23-byte default, so a single-PDU exchange never truncates |
| `MAX_FAIL_REASON_LEN` | 64 | `Outcome::Fail.reason` | [assumed] |
| `MAX_DISCOVERED_SERVICES` | 8 | `GattServiceInfo` per `StepResult.gatt_services` (§4.3a) | [measured 2026-08-26] the real DUT declares 3 services and a live `GattDiscover` over an L4 link reports 7 — see decision 57 |
| `MAX_CHARS_PER_SERVICE` | 16 | `GattServiceInfo.characteristics` (§4.3a) | [measured 2026-08-20] that DUT's largest is the Device Management Service at 8 characteristics |
| `MAX_MONITOR_TARGETS` | 16 | `GattMonitorSelected*.targets` (decision 53) | [measured] against the largest real DUT walked (`reference-dut-fw`: 10 notify/indicate-capable characteristics, 7 services over an encrypted link), with headroom. A study wanting more wants `GattMonitorAll` |
| `MAX_STREAMS_PER_STUDY` | 8 | `Study.streams` (§4.8) | [assumed] |
| `MAX_STREAM_NAME_LEN` | 32 | `StreamTap.name` | [assumed] |
| `MAX_SIGNAL_NAME_LEN` | 32 | `StreamSource::Signal.name` | [assumed] |
| `MAX_STREAM_CHUNK_BYTES` | 512 | one stream record's bytes | [assumed] |
| `MAX_STREAM_RECORDS_PER_BATCH` | 4 | `StreamChunkBatch` | [assumed] |
| `MAX_BATCH_SAMPLES` | 32 | `StreamChunkBatch.values` (decision 25) | [assumed] keeps one batched frame comfortably inside a UART receive buffer at 1 Mbaud |
| `MAX_DECODERS_PER_STUDY` | = `MAX_STREAMS_PER_STUDY` | `Study.decoders` (decision 52) | the arity of the thing, not a guess: a decoder is reachable only through a tap's `StreamEncoding::Struct` |
| `MAX_DECODER_NAME_LEN` | 24 | `StructLayout.name` | [assumed] |
| `MAX_STRUCT_FIELDS` | 12 | `StructLayout` fields | [assumed] |
| `MAX_STRUCT_FIELD_NAME_LEN` | 20 | `StructField.name` | [assumed] |
| `MAX_STRUCT_CSV_ROW_LEN` | 640 | a rendered struct row | [assumed] |
| `MAX_CSV_ROW_LEN` | 96 | `Sample::to_csv_row`'s buffer (§4.7) | fits `rx_utc_ms` (up to 20 ASCII digits for a `u64`), a `MAX_NAME_LEN` step name, a formatted `value`, `unit`/`channel_id` (decision 27), and separators |
| `MAX_HARDWARE_ID_LEN` | 32 | `HelloAck.hardware_id` (decision 47) | double the 16 chars both of this suite's JTAG reads produce; `hwinfo`'s length is a per-SoC driver decision this crate does not get to fix |
| `MAX_DECLARED_SERVICES` | — | `DeclaredGatt.services` (decision 45) | [assumed] |

Retired constants, kept here because a reader meeting the name in older code needs to know it went and why: ~~`MAX_RESULT_REF_LEN = 64`~~ and the original ~~`MAX_BATCH_SAMPLES`~~ role — `StepResult.power_samples_ref`/`waveform_ref`, retired 2026-08-25 with the fields (decision 39). ~~`MAX_GATT_ACTIVITY_RECORDS = 32`~~ — retired 2026-08-26 with the field it bounded (decision 54); it was what a capped in-memory copy of a streamed capture cost, and §7's stack-safety risk for it went with it. ~~`MAX_STREAM_CHUNK_LEN`~~ — nothing left to bound once `StreamChunk` carried a `Sample` rather than an arbitrary byte buffer. ~~`MAX_VALIDATIONS_PER_STUDY = 64`~~ — retired with post-hoc validation (decision 48).
