# embarch-study-designer decisions: Bounded collections and type size

**Status:** active, 2026-09-02.

Every capacity constant, and the three passes that took `Study` from 77 KB to 1 KB.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 15 — Fixed-capacity `heapless` collections, not `alloc`-based `Vec`/`String`, with a concrete constant per field

Decisions 5 and 3 committed the crate to `no_std` and an allocator-free encoding, but neither constrained the crate's own *data types*: as first drafted, `Study.steps: Vec<Step>`, `Step.name: String`, `GattOperation::Write { payload: Vec<u8> }` all require a global heap allocator (`extern crate alloc`) somewhere in whatever links the crate — not something bare-metal C firmware (decision 7) guarantees. Every such field became `heapless::Vec<T, N>` / `heapless::String<N>`, whose `serde` feature pairs with postcard with no allocator anywhere in the chain. That closes the loop decision 3 opened, and forces a concrete ceiling onto every field — which also serves §1's fuzz-testing case directly: a fuzzer now has an explicit bound to generate within instead of being able to build a `Study` no real MCU could hold.

Constants, module `limits`, all `pub const _: usize`:

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

Every `[assumed]` value above is placeholder-but-concrete, the same posture decision 3 accepted for postcard itself: chosen without real dev-bench hardware to size against, flagged for re-confirmation once real nRF54 memory constraints are known. A value proving too small is a version-bumped breaking wire change (decision 12), like any other field change.

### 46 — `Study.steps` is a heap `Vec` on the host and stays `heapless::Vec<Step, MAX_STEPS_PER_STUDY>` on the `no_std` build

The actual fix for a stack overflow tracked since 2026-08-18. `Step`'s largest `Action` variant carries a 512-byte payload, and a `heapless::Vec<Step, 64>` is a 64-slot inline array *regardless of how many steps are populated* — [measured] roughly 38 KB moved on the stack every time a `Study` is passed around, for a real 2-step self-test study. That crashed a debug `embarch-api` serving a live `study_status` call over MCP.

The mitigation that shipped for it (a dedicated 512 MiB-stack runtime thread) works and is why a release build survived, but it is a workaround sized against today's code and optimization level rather than against the type. Behind a `std`/`alloc` feature the field becomes `alloc::vec::Vec<Step>` and the 38 KB collapses to a pointer; the `no_std` FFI build keeps the fixed-capacity form it needs. The crate already feature-gates for `ffi`, so this is an established pattern.

**No schema bump.** `Vec` and `heapless::Vec` serialize identically under both postcard and `serde_json` — a length prefix then elements — so nothing crosses either hop differently and neither constant moves. Stated explicitly because "the type changed" reads like a wire change and is not one.

Two alternatives declined: `heapless::Vec<Box<Step>, 64>` shrinks the container but adds an allocation per step and still needs the same feature gate to be shareable with `no_std`, paying the gate's cost without the simplification. And shrinking `MAX_STEPS_PER_STUDY` 64 → 16, the cheapest possible change, was declined because it reduces a real authoring limit to serve an implementation detail exactly as studies get longer — and dev-bench's own unilateral shrink to 16 is a cautionary tale in the same pass ([embarch-dev-bench/decisions.md](../../embarch-dev-bench/decisions.md) decision 35). That divergence (`DBM_MAX_STEPS_PER_STUDY` 16 here, 64 there, so a 20-step study passes every host check and is rejected on the wire) is dev-bench decision 35's to close; this decision is why the host side has no reason to shrink to meet it.

### 49 — Decision 46's newtype generalised to `Bounded<T, N>` and applied to the result types

Decision 46 fixed `Study.steps` and stopped, on the reasoning that it was the field that had actually crashed something. [Measured 2026-08-25] immediately afterwards, that was far too narrow:

| Type | Before | After |
|---|---:|---:|
| `StudyResult` | 1,293,608 | 9,024 |
| `StepResult` | 20,200 | 696 |
| `DevBenchMessage` | 20,208 | 2,128 |

`StudyResult.steps` was a 64-slot inline array of 20 KB `StepResult`s — **1.29 MB**, in a type Core assembles and `embarch-api` deserializes. `StepResult` was 20 KB because `gatt_activity` inlined 32 × 536-byte records and `gatt_services` 8 × 296, whether or not the step captured any.

**This is the one that matters most, and decision 46 did not address it at all.** `embarch-core`'s `build_runtime` sets a 64 MiB thread stack, and its comment records why: the first real `run_study` POST crashed the **release** Windows service with `STATUS_STACK_OVERFLOW` on `spawn_blocking(run_study_to_completion)` — a `StudyResult` path, not a `Study` one. Decision 46's fix could not have prevented that crash.

`StepList` becomes `pub type StepList = Bounded<Step, MAX_STEPS_PER_STUDY>`, leaving decision 46's call sites unchanged. `captured_data` is deliberately left alone: at 528 bytes it is 0.5% of the old `StepResult` and would touch dozens of byte-level `from_slice`/`extend_from_slice` sites for no meaningful gain — the cut is where the inline arrays are big, not everywhere they exist.

Still no schema bump, now asserted for more than one element type: decision 46 pinned the property with a test comparing postcard bytes against the `heapless` shape for `Step`, and this applies the newtype to three fields with different element types. `gatt_services`' round-trip test now encodes from a `Bounded` and decodes into a plain `heapless::Vec` — the host-encodes/dev-bench-decodes case in miniature, and the first test here to *prove* the two shapes agree rather than assert it in prose. The `no_std` shape is asserted in the opposite direction too: a test requires `size_of::<StepResult>() > 4096` without `alloc`, so "make it smaller" can never be applied to the one build with no allocator to make it smaller with.

---

