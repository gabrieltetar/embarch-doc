# embarch-study-designer: locked-in design decisions

**Status:** active, 2026-08-31.

Extracted from [design.md](design.md) §3 on 2026-08-31, per [DOC-PROTOCOL.md](../DOC-PROTOCOL.md) §3's threshold (a decisions section past 40 entries or ~120 KB), and compacted in the same pass per [DOC-COMPACTION.md](../DOC-COMPACTION.md). Section references without a file name (§4.7, §5.2, §7) are [design.md](design.md)'s.

**Decision numbers are permanent identifiers** ([DOC-PROTOCOL.md](../DOC-PROTOCOL.md) §7.2–7.4). They are unique within this sub-project, never renumbered and never reused; groups below are topical, so numbers run out of order inside them by design. Nothing addresses a decision by its file or section, which is what let this extraction happen without touching a single one of the references pointing here.

---

## Crate shape and boundaries

### 1 — Separable crate, not embedded in `embarch-api`

`embarch-core`, `embarch-api`, and dev-bench firmware each compile it in independently — a Cargo dependency for the first two, a cross-compiled FFI staticlib for the third (decision 7). Chosen explicitly over embedding study logic inside `embarch-api`: dev-bench firmware is a different binary in a different language and needs the identical types, which is impossible if they live only in `embarch-api`'s crate.

### 2 — Data types plus the narrow set of tools needed to use them identically everywhere — not a protocol or transport

The crate defines `serde`-derived types (§4) *and* the small number of type-adjacent helpers every consumer needs one implementation of, so `embarch-core`/`embarch-api`/dev-bench never reimplement the same logic and drift: CRC sealing (`steps_crc`, decision 17) and `Sample`'s canonical row-rendering (§4.7, since §5.2's CSV rework). It deliberately hardcodes no wire format and no transport — different hops need different formats (decision 3), and baking one in forces a lossy re-encode at whichever hop doesn't match.

The line: anything every consumer must agree on byte-for-byte or column-for-column belongs in the crate; anything hop-specific (the socket, the HTTP client) stays out.

### 5 — `#![no_std]`, not std-everywhere

Dev-bench firmware may be bare-metal and its runtime was undecided when this was locked (§7). A `no_std` crate keeps every option open (bare-metal Rust, an RTOS, a hosted environment via a `std` shim); a `std`-only crate forecloses the bare-metal case outright. `embarch-core`/`embarch-api` run hosted and simply use the `no_std`-compatible types.

### 7 — Dev-bench firmware is C, bridged via an FFI staticlib — not native Rust, not a Zephyr+Rust module

Resolved over native embedded Rust and `zephyr-lang-rust` because the nRF54 family splits sharply by variant: nRF54L15 (single Cortex-M33) has a workable Rust path via existing `zephyr-lang-rust` samples on comparable Nordic parts, but nRF54H20's mandatory multi-core `sysbuild` build isn't a proven fit for that project's west-module/CMake integration. Either way Zephyr's BLE host stays a C API reached through generated bindings, so the BLE-heavy parts wouldn't be idiomatic Rust regardless. Going C sidesteps the split.

This crate cross-compiles as a `#![no_std]` staticlib for the target ABI, exposing `extern "C"` functions to build/serialize/deserialize `Study`/`Step`; `cbindgen` generates the C header from the Rust source so it cannot drift by hand. The `postcard` encode/decode logic (decision 3) stays inside the compiled Rust — C calls into it rather than re-implementing the wire format, which is what stops this becoming the three-independent-definitions problem decision 1 exists to avoid.

### 8 — A sibling-repo path dependency, not a published crate and not a git reference

`embarch-core` and `embarch-api` consume it as `embarch-study-designer = { path = "../embarch-study-designer" }`. Not a registry package: that means version-bump-and-republish overhead while the type model (§4) still changes across all three consumers, all of whom track head. Originally specified as a *git* dependency and implemented as a plain path instead once Milestone 2 needed it wired for real — edits are picked up by the next `cargo build` in either consumer with no commit/push/re-vendor step, and a path is exactly what [DOC-PROTOCOL.md](../DOC-PROTOCOL.md) §2's sibling layout already assumes. A git dependency stays available if a consumer's checkout is ever not a true sibling (a CI runner, a machine without all four repos cloned side by side); no real workflow needs it yet.

The repo is [gabrieltetar/embarch-study-designer](https://github.com/gabrieltetar/embarch-study-designer), standalone rather than a workspace member of an existing repo — three independently-versioned consumers (two Cargo dependents, one FFI/C consumer) is the case a shared standalone crate is for.

### 23 — The FFI boundary is panic-safe by construction: `panic = "abort"` plus explicit status codes, not `catch_unwind`

A Rust panic unwinding across `extern "C"` into C firmware is undefined behavior, and decision 7 left it unaddressed. Resolved with `panic = "abort"` in `[profile.release]` — the natural fit for a `no_std` bare-metal target with no unwinding runtime (decision 5) — rather than wrapping every exported body in `std::panic::catch_unwind`, which needs `std` and is unavailable here. Every exported function returns an integer status (`0` = success, negative = a documented reason: buffer-too-small, capacity-exceeded, malformed input) plus out-parameters, so no Rust `Result` or panic ever reaches the C caller. Same philosophy as decision 18 applies at the HTTP boundary: name the specific failure, never let a raw internal error surface.

---

## Bounded collections and type size

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

Two alternatives declined: `heapless::Vec<Box<Step>, 64>` shrinks the container but adds an allocation per step and still needs the same feature gate to be shareable with `no_std`, paying the gate's cost without the simplification. And shrinking `MAX_STEPS_PER_STUDY` 64 → 16, the cheapest possible change, was declined because it reduces a real authoring limit to serve an implementation detail exactly as studies get longer — and dev-bench's own unilateral shrink to 16 is a cautionary tale in the same pass ([embarch-dev-bench/decisions.md](../embarch-dev-bench/decisions.md) decision 35). That divergence (`DBM_MAX_STEPS_PER_STUDY` 16 here, 64 there, so a 20-step study passes every host check and is rejected on the wire) is dev-bench decision 35's to close; this decision is why the host side has no reason to shrink to meet it.

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

## Serialization, framing, and the link

### 3 — Format-agnostic at the type level; two formats chosen per hop

`embarch-api` ↔ `embarch-core` stays JSON, matching every existing Core endpoint (`embarch-core/decisions.md` §4) — no reason to break that convention for a hop that isn't resource-constrained. `embarch-core` ↔ `embarch-dev-bench` uses **`postcard`** (pairs naturally with `serde` + `no_std`, no allocator required). Locked without real dev-bench hardware to spike against; a stand-in `no_std`/no-alloc round-trip check is treated as sufficient, flagged for re-confirmation once real nRF54 hardware exists — the same posture as decision 7's firmware-language call. Framing is layered on top: decision 10.

### 4 — Transport for the Core↔dev-bench hop is serial (UART or USB CDC)

Chosen over HTTP because dev-bench is a resource-constrained MCU wired directly to whatever machine runs `embarch-core`. Mirrors Core's existing DUT serial-log pattern (`serialport`, `embarch-core/decisions.md` §5) rather than requiring dev-bench to carry a network stack.

### 10 — COBS-framed postcard, versioned by an append-only top-level enum — not a length prefix or a version byte

postcard has no framing and no self-describing schema. COBS (Consistent Overhead Byte Stuffing) wraps each encoded message in a self-terminating frame that resyncs after a dropped or corrupted byte — chosen over a fixed length-prefix header, which desyncs the reader on any single corrupted length field until a resync heuristic kicks in, a real risk on a physical UART. The `cobs` crate is `no_std` with no allocator, matching decision 5.

Versioning rides on making every message a variant of one top-level `serde` enum (`DevBenchMessage`): postcard's varint enum discriminant gives wire compatibility across additions for free **provided variants are only ever appended, never reordered or removed** — the discipline this decision commits to instead of a hand-rolled version byte. Every later variant follows it (decisions 20, 24, 36, 39), and every `Action` discriminant is likewise append-only: `GattMonitorStart`/`GattMonitorStop` at 5 and 6 (decision 36), `BleSecurity` at 7 (decision 44), `BleUnbond` at 8 (decision 50), `GattMonitorSelected`/`GattMonitorSelectedStart` at 9 and 10 (decision 53).

The one exception, and why it was safe: decision 39 **reuses** discriminants 2, 3 and 4 from the stream triple it retired, because postcard encodes by declaration index and leaving holes would need placeholder variants existing only to be un-constructible. The `Hello`/`HelloAck` handshake refusing a version mismatch outright is what makes reuse safe — and no dev-bench firmware carrying the old shapes had ever been flashed.

### 24 — `Study` crosses in one message; per-step results stream back

Closed the largest gap the 2026-08-15 design review found: `embarch-core/decisions.md` §4 said Core "begins relaying `Study.steps`", but no wire message carried a `Study` at all, and whether steps crossed one at a time or as a vector was unspecified — a real gap, since decision 17's `steps_crc` is computed over the whole vector at once.

`StudyStart { steps, steps_crc }` (Core→dev-bench, once, immediately after the `Hello`/`HelloAck` handshake) carries the whole vector in one postcard message. Whole-vector rather than per-step because it keeps decision 17's CRC check atomic: a per-step transfer needs either a running CRC accumulated message-by-message or per-message CRCs plus a final reconciliation, for a payload already small and bounded (`MAX_STEPS_PER_STUDY = 64`, each `Step` itself bounded by decision 15) and therefore cheap to send in one frame. `StudyDone { completed: bool }` comes back once, after the last step dev-bench actually ran.

Per-step *results* stream incrementally instead, mirroring `StreamChunk`'s reasoning (decision 20): `StepResult { step_index, result }` is sent as each step completes, so Core writes `events.json`'s per-step entries progressively and decision 16's host-side watchdog can key off individual arrivals rather than one final blob.

`StudyStart` has grown by appending only, never inserting, so dev-bench's hand-written C decoder sees one unconsumed trailing field instead of a re-shuffled sequence: `streams` and `streams_crc` after `steps_crc` (decision 39), `dev_bench_log_level` after those (decision 51), `protocols` and `protocols_crc` after that (decision 58).

### 25 — The UART link budget is stated, and stream chunks batch

Closed review item 3: a COBS+postcard single-`Sample` `StreamChunk` (decision 20) is [measured] roughly 10–14 bytes on the wire, and the power-profiling rate this crate serves (10–100 kHz per §1) needs far more throughput than one frame per sample delivers at any reasonable baud.

- **The Core↔dev-bench UART runs at 1 Mbaud** — [assumed] the practical ceiling for both the nRF54L15's UART peripheral and the on-board J-Link VCOM bridge it crosses ([embarch-dev-bench/decisions.md](../embarch-dev-bench/decisions.md) decision 6) without exotic clocking. Stated here because nothing in either doc previously named a rate.
- **Batching:** one base timestamp plus a fixed sample interval (both known at `StreamStart` time, from `PowerSampleWindow.sample_rate_hz`) means every sample after the first carries only its value. `unit`/`channel_id` (decision 27) ride once per batch, not once per sample, since a capture window doesn't change units mid-stream. Core reconstructs each `rx_utc_ms` as `base_utc_ms + i * sample_interval_ms`.

Superseded in shape by decision 39, which collapsed `StreamChunk` and `StreamChunkBatch` — both of which were still live and still handled by Core in separate match arms, a duplication *this* decision was believed to have removed — into one `StreamChunkBatch` carrying `{ rx_utc_ms, bytes }` records rather than `Sample`s. The link budget and the batching rationale above are unchanged by that.

---

## Schema versioning, handshake, and clocks

### 12 — Two hand-bumped schema constants, checked at both connection points

`embarch-core` and `embarch-api` track this crate at head (decision 8) but deploy independently — nothing stops one running a build ahead of the other, and a drifted `Study`/`StudyResult` shape would fail however `serde` happens to fail rather than with a clear error. Bumped only when a wire-relevant type changes, independent of `Cargo.toml`'s own semver.

- **`DEV_BENCH_WIRE_SCHEMA_VERSION`** — checked at `Hello`/`HelloAck`, bumped only by a change to something dev-bench itself parses or emits. This is the number whose movement costs a firmware reflash and a decision 36 both-languages re-pinning pass.
- **`HOST_TYPE_SCHEMA_VERSION`** — checked at `GET /status`, bumped by any change to a type crossing the `embarch-api`↔`embarch-core` hop. A strict superset: every dev-bench wire change plus host-side-only ones.

**Both are mismatch *detectors*, not compatibility *negotiators*** — no fallback to an older wire format, matching the suite's minimal-viable posture (no config hot-reload, single shared token) rather than building version-negotiation machinery nothing needs. A `SchemaVersionMismatch` is downcastable like `StudyConflictError`.

**Why one constant became two, 2026-08-25.** `schema_version.rs` listed `crate::validation` among the modules that bump the single constant. That was half right, and the wrong half mattered: `validations` never reached dev-bench at all (decisions 17, 19), so no change to it could drift a dev-bench decoder — but `Study` *including* `validations` did cross the api→Core hop as JSON, whose only drift check was that same constant. Dropping validation from the trigger list would have created a real undetected failure between two processes this suite genuinely deploys separately ([embarch-dev-workflow.md](../embarch-dev-workflow.md)); so the constant split instead. `STUDY_DESIGNER_SCHEMA_VERSION` was removed outright rather than kept as an alias, so every call site had to choose which hop it meant — an alias would have let the ambiguity survive.

**Neither constant was renumbered, and that was a decision.** Both continue the single constant's sequence from v8; `schema_version.rs`'s rewritten history says which side each past bump would have belonged to rather than recounting them. Renumbering would make every version string already logged, pinned in a C test, or written into a doc ambiguous about which scheme counted it — the same harm as [embarch-decision-reversals.md](../embarch-decision-reversals.md) row 18's stale bump number, with a wider blast radius.

**A compile-time assertion holds the invariant:** `HOST_TYPE_SCHEMA_VERSION >= DEV_BENCH_WIRE_SCHEMA_VERSION`. The host constant's triggers are a strict superset so it can never trail, and a wire bump that forgot to move the host one would otherwise leave the api↔Core hop talking across a difference it exists to refuse. Compile-time rather than a test, because the build carrying the bug is not necessarily one anybody ran the suite against.

Three things implementation settled:

- **The api↔Core half had never been built.** This decision described `/status` carrying a version since 2026-07-28; `embarch-core/decisions.md` §4 recorded (2026-08-23) that `status_handler` returned `{status, probes}` and nothing else. So "update the field and the comparison" was *adding* both. `embarch-api`'s comparison lives in `embarch-core-client`'s `post_study`, not at each caller: the CLI and the MCP tool both submit through that one method, and a drift detector only one of them runs is not a detector.
- **A Core that serves no version is a mismatch, not a pass.** `StatusResponse.study_designer_schema_version` is `Option<u32>` purely so such a response still parses and the drift can be named; `None` is refused. The operational consequence was real and not hidden: the then-live Core served no such field, so `embarch-api` refused to submit until it was redeployed. That is the detector working — but it makes Core-first the deployment order for such a pass.
- **The FFI's `essd_schema_version` returns the wire constant**, and there is deliberately no FFI surface for the host one; dev-bench is not a party to that hop. Separately, `study_ffi_stub.c` — the by-hand mirror `native_sim` uses in place of the real staticlib — was found **stale at v4, four bumps behind**, because nothing compares it against the crate by construction. Corrected; the gap in what `native_sim` can prove is unchanged by fixing the number and is recorded in `embarch-dev-bench/decisions.md`.

**`Hello` also does two other jobs.** It is a **hard reset**: receiving one unconditionally tells dev-bench to abort any in-progress `Study` and clear its execution state before replying, which is what lets Core recover a usable connection after its own crash (decision 16) with no separate abort message and no waiting out dev-bench's step timeouts. And it **carries `host_utc_ms: u64`**: dev-bench has no other clock source, so this is its only way to learn wall-clock time at all, seeding/resyncing its UTC offset on every connection and reconnection. That is what makes `Sample.rx_utc_ms` (§4.7) a real UTC timestamp rather than dev-bench-uptime-relative. Best-effort periodic resync, not NTP-style discipline — acceptable drift between resyncs is an open item (§7).

### 30 — Core records its own arrival time on every incoming message

`Sample.rx_utc_ms` is stamped by dev-bench's free-running clock, corrected only when a `Hello` arrives (decision 12) — for a long study with no reconnect, that clock free-runs with no way to correct for it after the fact. Resolved without adding a second resync trigger (decision 12 deliberately ties resync to connection establishment, not a periodic timer): Core timestamps its own receipt of every timing-relevant `DevBenchMessage` using its own wall clock and records it alongside as an additive `core_rx_utc_ms` column, changing `Sample`'s wire shape not at all. This doesn't correct drift in real time; it gives post-hoc analysis the raw material to detect and account for it, which a resync-on-`Hello`-only design otherwise cannot surface.

### 47 — `HelloAck` carries dev-bench's own `hardware_id`

Wire v9 → v10, host v11 → v12. *(Written as host 10 → 11; decision 48 landed first and took 11, so this re-derived to 12 — [embarch-decision-reversals.md](../embarch-decision-reversals.md) row 18's protocol working as intended, as decisions 44/45's reserved bump also had to.)*

The wire half of [embarch-core/decisions.md](../embarch-core/decisions.md) decision 35 and the answer to [embarch-topology/design.md](../embarch-topology/design.md) §5's UART-and-JTAG-are-different-USB-devices gap, which that doc had correctly described as needing a firmware protocol change it could not make unilaterally. One field on the handshake frame that already carries `schema_version` and `firmware_version`, both of which Core already checks at exactly this moment — so the comparison lands in an existing gate rather than adding one. Dev-bench reads its own chip ID and reports it; Core compares against the identity `hardware::validate_role` just verified over JTAG and refuses the link on a mismatch.

Both constants move per decision 12's rule: the wire one because a message dev-bench encodes changed shape, the host one because its triggers are a superset and the compile-time assertion refuses to let it trail.

**An empty `hardware_id` is a real value, not an absent field**, and both sides test it: a board whose Zephyr build has no `hwinfo` driver reports `""`, which still writes its length prefix and leaves the frame walkable. Core's comparison is where "no ID" acquires meaning — the encoder's job is only to carry it faithfully.

Decision 36's both-languages pinning applied in full, and the interesting part is that **`HelloAck` had never been pinned at all** — like `StepResult`, it predates that rule. `WIRE_HELLO_ACK` here and `test_hello_ack_encodes_to_the_pinned_wire_bytes` in dev-bench's ztest suite now hold the same 30 bytes from both sides. They agreed on the first run.

---

## Integrity seals and pre-flight validation

### 17 — CRC-sealed integrity checks, verified independently at both hops

Neither existing safeguard covers payload corruption: COBS (decision 10) provides frame resync after a dropped byte, not corruption *detection*; postcard has no checksum; and the api↔Core hop is plain JSON over HTTP with no equivalent check at all.

`Study` carries a `steps_crc: u32` over `steps` specifically — not `name`. Computed via a crate-exported `steps_crc()` (CRC-32/ISO-HDLC, the `crc` crate, one element streamed through the digest at a time), checked **twice**: Core recomputes over what it deserialized from the HTTP body and rejects with `400` before generating a `study_id` (alongside decision 18's structural checks), then dev-bench recomputes over what it decoded before running any step and rejects the study outright on mismatch rather than running with possibly-corrupted step data.

**Three sibling seals, not one widened seal.** `streams_crc` joined it in `crc.rs` beside `steps_crc` — same algorithm, same one-element-at-a-time digest, its own `StreamTapTooLargeError` (decision 39) — and `protocols_crc` after that (decision 58), each carried on the wire **immediately after the one contiguous span it covers**, so dev-bench's hand-written C digests one run of bytes per seal and a mismatch names which of the three is corrupt.

Widening `steps_crc` instead was considered and rejected on a corrected fact. The recorded objection had been that widening would "silently invalidate every saved study's sealed value" — it would not, because `embarch-api` recomputes and overwrites on every submit (decision 26), so no stored value is ever trusted. The real cost is structural: `steps_crc` sits *between* `steps` and `streams` on the wire, so the C side would have to digest two non-contiguous spans, or `StudyStart`'s field order would have to be reshuffled — a reshape where an append will do.

**What is deliberately outside every seal:** `Study.decoders` (decision 52) and `Study.dev_bench_log_level` (decision 51), because how the host renders a captured byte and how loud the bench is change neither what dev-bench executes nor what it captures. Re-rendering a capture with a corrected layout, or re-running at a louder log level, **must leave it the same study by every check that matters** — otherwise debugging a failure would require altering the artifact under investigation. `requires` (decision 40) and `gatt` (decision 45) are outside because they are host-side only and never cross that wire at all.

Two implementation findings:

- **dev-bench's decoder did *not* already walk the `streams` span, so adding `streams_crc` was net-positive firmware, not net-negative.** The expectation was "one varint read and one CRC call over a span the decoder already walks". It walked no such span — decision 39's Phase A appended `streams` *after* `steps_crc` precisely so C could stop there and see one unconsumed trailing byte, which is what it did. Checking the seal at that hop therefore required teaching C to walk a `StreamTap`: a ~120-line `pc_skip_stream_tap` covering every `StreamSource`/`StreamEncoding`/`StreamScope` variant, since postcard carries no per-variant length. [Measured on `native_sim`: 25,660 → 26,314 bytes of text, +654.] The decision stands as written — a seal computed at one hop and taken on trust at the other is not "checked independently at both hops" — and the walker is not wasted, since taps have to be decoded to be opened anyway. What was wrong is only the estimate.
- **`Study.streams_crc` is `#[serde(default)]`, and the default is *correct* rather than merely permissive.** Saved studies (decision 38) are JSON deserialized straight back into `Study`, so a mandatory field would make every one unloadable. A study authored before taps existed has no taps, and `0` is the genuine CRC-32/ISO-HDLC of zero bytes (init and xorout are both `0xFFFF_FFFF` and cancel), not a sentinel. The sharp edge: an empty tap list validates against a decoder that never computed the CRC at all — which is why the both-languages pin deliberately carries three real taps.
- **The FFI decode surface still checks `steps_crc` only.** `essd_study_decode_and_verify`'s single `out_crc_matches` bool and `essd_study_decode_full`'s single `CrcMismatch` status cannot say which of three seals failed; folding them in would quietly destroy the property the sibling seals exist to provide, and widening the C ABI would extend a surface §7 records as having no caller anywhere. Left as-is with the reason written at the call site. The real Core↔dev-bench check is dev-bench's own C decoder, which computes all of them.
- **dev-bench aborts the study on a seal mismatch**, naming which seal failed in its own log line, even for seals covering things that firmware version could not yet act on. Computing a seal and ignoring it would leave a study whose declarations arrived corrupt running to completion and reporting captures that are silently missing or wrong.

### 18 — Core validates a submitted `Study` structurally, before generating a `study_id` or touching the serial link

Every `limits` capacity (decision 15) within bounds, every referenced index in-bounds, `Requirements` present and non-blank (decision 40), and every named tap actually declared (`embarch-core`'s `validate_study`/`validate_taps`, decision 19's implementation note). Each failure produces a `400` naming the offending field and limit rather than a raw `serde` deserialize error — which matters because §6's `--study-file` path means a human is often hand-writing the JSON.

### 26 — `steps_crc` is filled in by whoever *submits* a study, not required of whoever *authors* one

Review item 4: decision 17 requires a correct CRC on submission, which makes a hand-authored `Study` JSON file unusable without a human computing a CRC by hand — squarely against decision 6's symmetric-access principle. Resolved without touching the check: `embarch-api`'s `run_study` tool / `run-study` CLI computes `steps_crc` via this crate's exported function and overwrites whatever value (including a missing or zero one) was in the submitted JSON, immediately before `POST /study`. A caller that already computed a correct value — a fuzzing driver generating studies programmatically — is unaffected, since the recomputation is idempotent.

The crate also ships a generated `study.schema.json` for `Study` (via `schemars`), so a human hand-authoring a `--study-file` gets editor/CI validation before ever submitting, independent of the CRC question.

---

## Study structure and step semantics

### 13 — Per-step, not per-study, fail-continuation: `Step.continue_on_fail: bool`

A study's steps mix "must pass or the rest is meaningless" checks (a `BleConnect` — nothing downstream works without a connection) with "record and move on" ones (a `DataExchange` that is informational for a fuzzing run rather than fatal to it). A single study-wide switch can't express that mix; a per-step bool can. Defaults to `false` (abort immediately on this step's `Fail`/`TimedOut`), matching typical test-runner semantics; an author opts a specific step into `true` only where continuing past its failure is useful.

This is also the knob for "attempt it but don't insist" wherever that comes up — decision 44 declined to add a second flag for exactly that reason.

### 14 — Correlation by array position (`step_index: u32`), not by `Step.name`

`Step.name` stays purely a human-readable label — useful when a person reads `events.json` (§5.2) — and nothing in the wire types uses it to locate a step. `Study.steps` is already order-significant (§4.1), so a step's position is already a unique, stable-within-that-study identifier; reusing it costs no new field and sidesteps the ambiguity a name lookup would have if an author (or a fuzzer generating steps) gave two steps the same name.

Encoded as `u32`, not `usize`: `usize`'s width isn't fixed across the architectures this wire format actually crosses (a 64-bit host vs. a 32-bit nRF54 MCU, decision 7), and postcard would encode a mismatched-width `usize` inconsistently between them.

### 42 — `Step.delay_before_ms` — the "when" half of authoring a stimulus

Steps run strictly in sequence, so until this the only expressible timing was "immediately after the previous step finished". That isn't enough to author a stimulus: letting a DUT settle after a connect, or waiting inside an open `GattMonitorStart` window before writing so the transcript visibly separates unsolicited traffic from the response, both need a delay that isn't a side effect of some other step's `timeout_ms`.

Deliberately **not folded into `timeout_ms`**: this is time spent before the action starts, so it doesn't consume the action's budget, and `Outcome::TimedOut` keeps meaning "the action took too long" rather than "the delay was too long". It also **replaced a workaround** — the UI's capture template previously held the run open with a `GattMonitorAll` step, which re-subscribes inside an already-open window; a delay on the `GattMonitorStop` step does that job without a second action.

Declared and encoded **last**, on purpose: postcard is field-order-sensitive with no field names on the wire and dev-bench hand-decodes `Step` in C, so appending gave that decoder one extra trailing varint read instead of a reshuffled sequence. Wire v5 → v6 — appending is still a wire break in both directions, and the handshake refusing the mismatch outright is the point. Covered by `steps_crc`, so the timing an engineer authored is inside the integrity seal.

### 51 — `Study.dev_bench_log_level` — how loud the bench should be is a property of the run

[embarch-dev-bench/decisions.md](../embarch-dev-bench/decisions.md) decision 38 made dev-bench's `CONFIG_LOG` output reach Core, and made it reach Core *always*, because the only knob was a compile-time Kconfig level. This is the type change that moves the knob to the study. `DevBenchLogLevel { Off, Error, Warn, Info, Debug }`, fieldless so postcard encodes a single varint discriminant, appended to `Study` and — after `streams_crc`, never inserted — to `StudyStart`. Wire v12 → v13, host v14 → v15: dev-bench parses the field and acts on it.

Three shape decisions, each with a plausible alternative:

- **On `Study`, not a submission-time override.** A `POST /study` query parameter would have avoided touching this crate at all, but would then need threading through `embarch-api`'s MCP tool, its CLI and the UI's submit path separately, and a saved study could not carry it. On `Study` it works through every path that already exists, and `#[serde(default)]` means every study file authored before the field still loads at `Warn` — which is what those studies effectively already ran at, so the default is *correct* rather than merely permissive.
- **A scalar, not a property of the reserved `DevBenchLog` tap.** That tap looks like the more idiomatic home (capture is declared, not implicit — decision 39), but it is synthesized by Core, never crosses the dev-bench hop (§4.8), and a `StreamScope` window would drop precisely the lines emitted *between* steps.
- **Outside both seals, deliberately** — decision 17's rule.

`Warn` is the default rather than `Off`, and the asymmetry is the point: an `<err>`/`<wrn>` line is rare by construction and is exactly what someone needs to read about the run that just failed. `Off` exists for the study that genuinely needs a clear link and accepts being blind, including to the fatal-error dump. `DevBenchLogLevel::zephyr_level()` lives here rather than in the firmware so the discriminant→severity mapping has one home; the C side reads the same numbers as `DBM_LOG_LEVEL_*`, which is why no translation table exists there — small, but this project has already had two hand-mirrored constants go stale (`embarch-dev-bench/app/CMakeLists.txt`'s own note on `STUDY_FFI_STUB_SCHEMA_VERSION`).

---

## Execution and failure model

### 9 — Async, job-based execution for the Core↔dev-bench-bridging HTTP surface, not a blocking call like `/flash`

A study's BLE steps (advertise, wait for a connection) can legitimately take unbounded time, unlike Core's existing bounded operations — a synchronous call would need an unreasonably long client-side timeout or risk truncating a study mid-run. Core accepts a `Study`, returns a `study_id` immediately, and reports progress via polling. Endpoint shapes in §5.1; this decision covers the *shape* of the interaction, a property of the whole study-execution flow rather than of Core's implementation.

### 16 — A crash mid-study on either side is catastrophic for that study, and dev-bench's needs a host-side watchdog to be detected at all

Each `Step.timeout_ms` self-bounds any single hung action, so dev-bench is never stuck past a step's own budget — but that says nothing about the *study* if Core disappears (crash, unplugged, restarted). That study is written off: Core's in-memory job registry doesn't survive a restart and Core is what persists `events.json`/`data.csv`, so a study in flight when Core dies never gets a `StudyResult`, and a caller polling that `study_id` afterwards gets `404`, indistinguishable from an id that never existed. Raw data already streamed to disk may still be sitting there — a partial diagnostic artifact, not a completed result — since decision 20 writes incrementally.

**A dev-bench crash or hang is symmetrically catastrophic and cannot use the same detection.** `Step.timeout_ms` is enforced *by dev-bench*; if dev-bench is what hung, nothing device-side is left to report `TimedOut`. So Core enforces its own watchdog: it expects a `StepResult` for the in-flight step within `timeout_ms` plus a small fixed grace margin [assumed], and treats that margin lapsing — or the serial connection dropping — as an immediate `"failed"` outcome, the same terminal state a device-reported `Fail` produces, just detected by Core.

Recovering the *connection* in either direction is decision 12's `Hello`-as-hard-reset: when Core reconnects, dev-bench aborts whatever it was still running and both sides start clean.

### 29 — The fuzz-testing loop is documented, not changed

Review item 40 flagged that a 64-step ceiling, no queue, and a `409 Conflict` on concurrent submission make a fuzzing driver look like an awkward N-round-trip loop against a rejection. Examined and left as-is deliberately: raising the ceiling doesn't help a fuzzer exploring many *distinct* short studies rather than one long one (§4.1 already frames a `Study` as fuzzing's *output*, one concrete value per run), and a queue is real new machinery — persistence, ordering, partial-failure semantics — this suite has avoided everywhere else (`embarch-api/decisions.md` §3.6's no-database stance).

The intended shape, stated explicitly: a fuzzing driver runs entirely client-side, generating one `Study` at a time, submitting it, polling `GET /study/{id}` to a terminal status, then generating the next. **The poll loop *is* the intended backpressure mechanism**, not a workaround for a missing one.

---

## Streams: one generic capture pipeline

### 11 — Result storage splits by data shape: a JSON events file plus CSV data files, not one file and not a database

Per-step pass/fail and captured BLE data go in a small, human-readable `events.json`; time-series samples — potentially large and high-rate — go in separate CSV files referenced from it rather than embedded. So the common case (did this study pass) never requires parsing a large series, while the small side still follows the suite's no-database principle (`embarch-api/decisions.md` §3.6). Full layout in §5.2. Decision 39 replaced the fixed `data.csv`/`waveform.csv`/`gatt.csv` set with `streams/<tap name>`; the split itself is unchanged, and is the same reasoning that keeps decision 36's inline summary separate from its streamed transcript.

### 20 — A streaming sub-protocol from dev-bench to Core, replacing discrete end-of-window sampling

A capture can run for the length of a step, producing far more data than fits in one bounded message. `StreamStart`/`StreamChunk`/`StreamEnd` variants (append-only per decision 10) open a channel, carry records, and close it; chunks in between carry no channel tag of their own, since Core tracks which channel is open from the last matching `StreamStart` — keeping per-chunk overhead minimal on a UART link. More than one channel can be open concurrently (a power window overlapping a waveform capture), so `Start` and `End` both carry the tag to disambiguate.

Originally each chunk carried a `Sample` directly rather than arbitrary raw sensor bytes, so a chunk was self-contained and hardware-agnostic at the wire level, with translating a raw ADC reading into a `Sample` being dev-bench's own job before the value reached the wire. That is what kept Core's CSV writing free of hardware-specific decoding — the same property decision 39 preserves by moving *meaning* into a declared encoding rather than back into the node.

**Core writes each incoming record to disk incrementally**, appending as it arrives rather than buffering the whole capture until the study finishes, so raw capture data survives even a Core crash that writes off the study itself (decision 16).

### 21 — Sensor-waveform capture is a `GattOperation` variant, not a step-level field

`StreamCapture` joined `Read`/`Write`/`Notify`/`Indicate`/`Subscribe` (§4.3) — a continuous capture of whatever the characteristic streams (a PPG waveform, say). No separate duration field, matching `PowerSampleWindow`'s reasoning: it runs for exactly as long as the step's own `timeout_ms`/completion allows, so a capture can't silently outlive or fall short of the step characterizing it. Folded into decision 39's tap model as `StreamSource::GattNotify`.

### 27 — `Sample` carries `unit` and `channel_id`

Resolving an ambiguity `StreamChannel`'s two variants already implied but never settled: `Sample { rx_utc_ms, value }` was one shape shared by power and arbitrary waveform data, with nothing on the wire saying what `value` meant or which of several concurrent channels on the same step it came from — a real gap the moment a capture needs more than one bare scalar (current *and* voltage sampled together, a multi-lead sensor). Added ahead of real hardware forcing the question, to avoid stacking a second breaking wire change on the one hardware validation will likely already require.

`unit: Unit` is a small append-only enum (`Milliamps`, `Volts`, `Milliwatts`, `Raw`); `channel_id: u8` disambiguates concurrent streams on the same channel (`0` for the common single-channel case). Both thread through `Sample::to_csv_row`/`csv_header` as trailing columns, and both ride once per batch rather than once per sample (decision 25).

### 39 — One generic inbound stream pipeline; the write direction explicitly not accepted

[embarch-stream-pipeline-proposal.md](../embarch-stream-pipeline-proposal.md)'s read direction, accepted 2026-08-25. Opened by [embarch-outpost](../embarch-outpost/design.md), whose DUT-side debug UART needs its bytes captured for a study's duration and which would otherwise have become **the fourth** near-identical capture pipeline here, after power, sensor waveform, and (as of the day before) the GATT transcript. Four pipelines differing only in what the bytes mean is the point at which the pattern has to be named rather than repeated again.

`Study` gains one top-level field beside `steps`: `streams: heapless::Vec<StreamTap, MAX_STREAMS_PER_STUDY>` (§4.8). A tap declares four things and nothing else — **where the bytes come from, how long the tap lives, how to render what arrives, and what to call the output.** Every bespoke channel becomes a declared `StreamSource`; every bespoke row shape becomes a declared `StreamEncoding`.

| Was | Becomes |
|---|---|
| `StreamChannel::Power` + `StreamChunk`/`StreamChunkBatch` (decisions 20/25) | `StreamSource::PowerFrontEnd { sample_hz }` + `StreamEncoding::Samples { .. }` |
| `GattOperation::StreamCapture` → `StreamChannel::SensorWaveform` (decision 21) | `StreamSource::GattNotify { service_uuid, characteristic_uuid }` + `StreamEncoding::Samples { .. }` |
| `DevBenchMessage::GattTranscriptRecord` → `gatt.csv` (decision 36) | `StreamSource::GattTranscript` + `StreamEncoding::GattTranscript` |
| `DevBenchMessage::LogLine`, which reached only Core's rolling log and never a study's results | `StreamSource::DevBenchLog`, a reserved tap — closing a real asymmetry rather than inventing a feature |
| *(did not exist)* | **`StreamSource::Signal { name }`** — a signal Core reads itself, resolved to a carrier by [embarch-topology](../embarch-topology/design.md) decision 18. The outpost's tap |
| *(did not exist)* | **`StreamEncoding::OutpostTrace`** — decoded against a build-time manifest ([embarch-outpost/design.md](../embarch-outpost/design.md) decision 9). Shipped as `OutpostTrace { manifest_crc }` and corrected to a unit variant at v11/v13 |

**`StreamSource::Signal { name }` is the one genuinely new idea, and it is what makes the outpost expressible at all.** Every other source is dev-bench-mediated: dev-bench receives the bytes and forwards them. The outpost's bytes reach Core over a wire that **bypasses dev-bench entirely** today and are intended to go through it later — so the tap names the *signal* and topology's declared route decides the carrier. The identical saved study (decision 38) then runs unchanged across that migration, across a differently-enumerating USB bridge, and against a Core on another machine. A source variant naming the concrete port or pin would have re-authored every saved study the day the bench was rewired.

**The write direction is explicitly not accepted.** `Action::StreamSend`, `StreamExpect`, and the shell-interaction case stay in the proposal, unadopted: the outpost is TX-only and needs nothing from them, and adopting a step type nothing yet sends would build a capability nothing needs. The proposal file survives with its status narrowed rather than deleted. (Decision 58 later closed this direction by a different route — an authored state machine, not a generic write step.)

Wire changes were real and were not minimised: the stream variants collapsed to one `StreamOpen`/`StreamChunkBatch`/`StreamClose` triple carrying `{ rx_utc_ms, bytes }` records rather than `Sample`s, `GattTranscriptRecord` was retired as a variant, and `StreamChunk`/`StreamChunkBatch` finally became one. Every new record shape gets decision 36's both-languages pinning.

**`Step.power_sample` is retired; a `PowerFrontEnd` tap is the only way to author power capture.** This decision's own retire list omitted `PowerSampleWindow`, and it was settled against what the code did rather than what the types allowed: `power_sample` was already **fully vestigial** — `embarch-core` never read it (a capture's rate comes from the tap's `sample_hz`), dev-bench's C encoder wrote that `Option` byte as `None` unconditionally and its decoder read-and-discarded it, and `study_builder::build_study` always emitted `None`. Retiring it deleted a second way of saying something only one way had ever said, and Milestone 4 — which has never run — then arrives to exactly one way to author a power capture instead of two.

**The cost of doing this when it was done, stated plainly.** It reversed a decision one day old (decision 36), re-bumped a schema that had just been bumped, and edited dev-bench firmware that was code-complete and deployed to a live Core. The offsetting fact is the one the proposal argued for itself: **no real byte had ever crossed the streaming path** — Milestone 4 (power) had never run and Milestone 6's firmware had never been flashed, verified rather than assumed at the time: `embarch-dev-bench`'s Phase A edits were committed (`d5dc6d8`, over `9515e0e`) but the newest `build-artifacts/` binary was still `zephyr-dc4cc07-current.bin` from six days earlier, so it had **still never been flashed**. Nothing was load-bearing on a real bench yet, and that stops being true the moment either runs. This was the last cheap moment and it was taken deliberately.

**On bump arithmetic.** The bump landed at 7 → 8, not the 5 → 6 written when the decision was made: decisions 42 and 43 were implemented first and took v6 and v7. Nothing about the substance moved — still one bump, still covering this decision and decision 40 — only the arithmetic. Recorded rather than silently corrected, since "one bump per pass" is exactly the kind of rule a stale number quietly turns into two. The amendment adding `streams_crc` then landed at 8 → 9, re-derived rather than copied.

**A Phase A leftover found on the same wire**, while walking the C encoder against the Rust type: dev-bench was still writing two `Option` bytes for `StepResult`'s retired `power_samples_ref`/`waveform_ref`. Both were retired at v8; the C encoder and decoder kept writing and skipping them, so every `StepResult` dev-bench sent carried two bytes Rust did not expect — on the message it sends most. Both suites stayed green because each agreed with itself: `StepResult` predates decision 36's rule, which applied to *new* records, so it had never been pinned. Fixed, and `StepResult` is now pinned in both languages so the gap cannot reopen. **That pairing has now found a real discrepancy the first time it ran for a given record, twice.**

### 52 — An engineer-declared payload layout: `StreamEncoding::Struct`, `Study.decoders`, and a per-repo `study-structs.toml`

Opened by the session that opened decisions 53 and 54, authoring the first study that captures one specific characteristic rather than everything: a `GattNotify` tap could only be `Raw`, producing a `.bin` and no CSV at all, or `Samples`, which can say "packed `i16`s, one column" and nothing else. A real notification is a small header followed by a packed sample array, and neither describes it.

`decoder.rs` adds `ScalarType` (18 widths/byte-orders, no scale and no unit — the same line `SampleLayout` draws), `StructField { name, ty }`, and `StructLayout { name, header, repeat }`. `header` is read once at offset 0; `repeat`, when non-empty, is read as many times as fits, producing **one CSV row per repetition** with the header's values denormalized onto each. That repetition is the whole reason the type exists rather than a flat field list: a notification carrying a sequence number and twenty samples is one record and twenty rows, and rendering it as one row with twenty columns makes it unanalyzable by every tool that reads a CSV.

**The layout lives in the firmware repo, is referenced by name, and is resolved into the study at build time.** `embarch/study-structs.toml`, sibling to `study-actions.toml` and `embarch.toml`, for decision 35's reason: it is engineer-authored knowledge about *this* DUT. Resolution happens when the study is built, so the submitted `Study` carries the layout rather than a name — **Core cannot read that repo**, and a study naming a layout it didn't carry would render nothing on any machine but the author's, and would render *differently* after an unrelated edit to the file. `StructRegistry` is a plain-`String` mirror of the wire type on purpose: a hand-edited TOML's mistakes (`u24le`, a name one character too long) become a named `RegistryError` rather than a `toml` error pointing at a `heapless::String` capacity.

**What crosses the wire is an index, not the layout.** `StreamEncoding::Struct { decoder: u8 }` indexes `Study.decoders`, which is **host-only**. A tap's encoding *does* cross on `StudyStart`, where dev-bench has to walk past it to reach `scope`; a variable-length struct definition there would cost a nested walker in hand-written C for a value dev-bench must never act on, and would put what a payload *means* back inside the node decision 39 took it away from. The index costs that decoder one `u8` read.

**A payload that doesn't fit the layout still gets a row** — decoded columns empty, `payload_hex` and `decode_note` carrying the bytes and the reason. Never a dropped record and never a forced decode: the raw `.bin` is on disk before any decode is attempted, so a wrong layout costs a rendering that can be redone rather than a capture that cannot, and a record that arrived must be visibly *present and undecoded* rather than absent and indistinguishable from a notification that never came. Two smaller rules fall out and are asserted rather than assumed: `DecodeError`'s rendered text contains no comma and no quote (this crate refuses to produce a CSV value that would break the column shape rather than quoting it — `csv_escape_ok`'s own rule), and an empty repetition list produces **zero rows and no error**, because a DUT sending a header with nothing after it is a real thing and a row invented for it would be invented data.

**Integers render as integers.** `SampleLayout` can only produce `f32`, and a `u64` sample counter round-tripped through one loses its low bits — a plausible, wrong number, which is the failure this crate keeps refusing to produce.

### 55 — A `StreamSource::GattNotify` tap actually produces records, and dev-bench keeps the one thing it needs to route them

The variant had existed since decision 39 and was **decoded but dead**: dev-bench opened and closed the tap and never sent a record on it, which `main.c`'s own comment said out loud. So "give this characteristic its own file" was expressible in the type model and impossible in practice.

**Routing, not subscribing.** A GattNotify tap does not arm its own subscription; it routes what a monitor step already subscribed. dev-bench's transcript sink is the one place every captured notification passes through, so one entry now fans out to the declared transcript tap *and* to every open GattNotify tap whose characteristic matches — the transcript getting the postcard-encoded `GattTranscriptEntry` it always did, the tap getting **the raw ATT value and nothing around it**, because Core decodes those bytes against a layout describing the DUT's packet rather than a dev-bench record wrapping it. One notification landing in two files is not duplication: the transcript is the complete story of the connection, the tap is one characteristic's data with a declared layout, and neither is optional given the other.

The alternative — a tap arming its own subscription when it opens — was rejected: it needs new lazy-subscribe machinery in firmware (a `WholeStudy` tap opens before the `BleConnect` step, so there is no connection to subscribe on yet), and it would give one characteristic two independent subscribers to reconcile. Routing costs a UUID comparison in a callback that already runs.

**The cost is [measured] 16 bytes per tap in `struct dbm_stream_tap`, and it is addressing rather than meaning.** dev-bench now keeps a GattNotify tap's `characteristic_uuid`, having previously skipped those 32 bytes outright. `encoding` stays deliberately unkept — what a payload means is exactly the knowledge decision 39 took away from this node — but *which characteristic's notifications go to which tap id* is routing, precisely like `source_tag`, and this node has to know it because this node sends the record. The service UUID is still skipped: a notification identifies itself by characteristic, and a second array per tap would be static RAM for a comparison nothing makes.

**The failure this leaves reachable, and where it is caught.** A tap naming a characteristic no step subscribes to captures nothing, passes, and looks fine. Refused at authoring time by `embarch-ui`, which has both the steps and the taps in hand — not at run time, where it is an empty file after a run that cost hardware time.

---

## GATT: discovery, monitoring, and naming

### 31 — `Action::GattDiscover` — walk a connected DUT's entire GATT table

Motivated by [embarch-roadmap.md](../embarch-roadmap.md) Milestone 3: a study author pointed at an unfamiliar DUT has no way to ask "what's actually on this device" before authoring a `DataExchange` step against it. After a preceding `BleConnect`, this step walks every primary service and, per service, every characteristic (Zephyr's ordinary wildcard `bt_gatt_discover` with no target UUID — a superset of the single-service discovery `ble_bridge_real.c` already does per `DataExchange` call), reporting the table in `StepResult.gatt_services` (§4.3a) and acting on it no further: no subscribe, no capture. Bound by the step's own `timeout_ms`, no separate duration field, matching every other Action.

Properties are carried as the **raw ATT characteristic-properties byte** (bit 0 = broadcast … bit 5 = indicate, per the Bluetooth Core Spec's own characteristic-declaration encoding), not a crate-invented bitflag enum — consistent with this crate's "UUIDs are raw, not symbolic" stance on `DataExchange` (§4.3).

### 32 — `Action::GattMonitorAll` — discover, subscribe to everything notify/indicate-capable, capture for the rest of the step

**Deliberately not built on a prior `GattDiscover`'s result.** Considered and rejected: a design where this consumes a previous step's output so discovery happens once per connection. Rejected because every other `Action` here is self-contained within its own step — `DataExchange` re-resolves its own service/characteristic on every call — and threading one step's discovered table into a later step's input would be new wire-level state-passing this crate has never needed, for a capability (an unfamiliar-firmware smoke test, not a steady-state high-frequency operation) where re-running discovery is cheap.

So it runs its own internal discovery, subscribes to every characteristic whose discovered properties include Notify or Indicate, and captures until `timeout_ms` expires. `characteristic_index` in a captured record indexes into `gatt_services` **flattened in service-then-characteristic order** (service 0's characteristics first, then service 1's) — stated because it is the one place dev-bench's encoder and every consumer must agree on that flattening.

**Overflow behavior:** if real traffic filled the inline record cap before `timeout_ms` elapsed, dev-bench stopped capturing further records for that step and reported what it had — not a `Fail`/`TimedOut` — matching `Sample::to_csv_row`'s "log and skip rather than corrupt" precedent (§4.7) rather than silently wrapping or truncating a record's payload. That cap is gone with decision 54; the tap pipeline it was replaced by is uncapped.

The stack-safety risk this decision carried at the time — a `StepResult` variant substantially larger than `StudyStart`'s own worst case, which had already forced static rather than stack-allocated scratch buffers in [embarch-dev-bench/decisions.md](../embarch-dev-bench/decisions.md) decision 21 — was tracked as an implementation risk in dev-bench milestone 9 rather than re-litigated here, and went away with the field (decision 54).

`GattMonitorAll` is kept unchanged by both later monitor decisions (36, 53): pointing an unfamiliar DUT at "subscribe to everything and see what it does" is still the first thing anyone does, and still the simpler thing to author.

### 33 — A GATT-config extraction tool ships in this crate: a generic `GattConfigExtractor` trait, one concrete implementation

Distinct from decisions 31/32, which answer the same question live over BLE against whatever is running. A study author working against a specific firmware repo usually has it checked out already, and its GATT table is *source*, not a runtime mystery — extracting it statically means a `DataExchange` step can be authored with real UUIDs before dev-bench connects to anything, and gives a second independent source to diff against a live result (catching, say, a service compiled out of a specific build).

The trait's output reuses §4.3a's own `GattServiceInfo`/`GattCharacteristicInfo`, so a static extraction and a live `GattDiscover` result are comparable without a translation step. One implementation ships: `ZephyrBleDefExtractor`, scoped narrowly to one firmware's actual conventions — confirmed against real source (`ble_def.h`'s `..._UUID_VAL` macros, `ble.c`'s `BT_GATT_SERVICE_DEFINE`/`BT_GATT_PRIMARY_SERVICE`/`BT_GATT_CHARACTERISTIC` calls) rather than guessed against a generic Zephyr peripheral layout. It lives in `tools/`, a `std`-only binary behind a `gatt-extract` feature, not the `no_std` core — an authoring-time tool, never something dev-bench or Core links. Deliberately generic at the trait boundary and narrow at the implementation, per the repo owner's explicit call: a second firmware project's extractor is a new `impl GattConfigExtractor`, not a redesign of the trait or the output shape.

**Byte-for-byte comparability is now weaker than this decision claimed** — see decision 57: services come back in a stable but *non-handle* order, so a caller comparing static against live should compare them as **sets**.

### 36 — `GattMonitorStart`/`GattMonitorStop` — a capture window that outlives its own step — plus a streamed transcript

Opened by a gap found trying to author the first real stimulate-and-capture study: **it was not expressible.** Steps run strictly in sequence, and `GattMonitorAll` (decision 32) unsubscribes everything it armed when its own step ends, so a `DataExchange` write that stimulates the DUT and a monitor step that captures the response can never overlap. Write first and the response arrives after the capture step is over; capture first and the write never happens during it. **Every ordering loses, silently, producing an empty capture and a `Pass`** — the same "nothing captured, no error" failure decision 34 was opened by, from a different direction.

Two field-less variants at discriminants 5 and 6: `GattMonitorStart {}` runs the same wildcard discovery and subscribe-to-everything walk, then **returns immediately, leaving every subscription armed**, so every following step runs inside a live capture window; `GattMonitorStop {}` unsubscribes and reports the window's results. A `Stop` with no open window is a no-op `Pass`, not a `Fail`, and a study ending without one gets its window closed implicitly by dev-bench's dispatch loop, so an abort mid-study cannot leave subscriptions armed into the next one.

**The second half, and the reason this is one decision rather than two:** a window spanning steps immediately outgrows a per-step inline record list, which was capped and recorded *inbound notifications only* — nothing about what dev-bench itself sent, which is precisely the half a stimulate-and-capture transcript needs to be readable. So this decision also added a **streamed GATT transcript**, emitted as each GATT event happens and appended by Core incrementally. Because one entry is streamed per message, only a single entry ever has to fit in dev-bench's message buffer — which is what lifts the cap: the transcript is bounded by the study's own duration, nothing else.

The transcript was deliberately **its own message variant rather than a third `StreamChannel`** carried by decision 20/25's chunks: those carried a `Sample` — one `f32` plus a unit, with no room for a raw byte payload, a direction, or a pair of UUIDs. **Partially superseded by decision 39 one day later, knowingly, with the collision flagged before the call was made:** the dedicated variant folded into the generic pipeline, while `gatt.csv`, its columns, `GattTranscriptEntry`/`GattDirection`/`GattEventKind`, and the entire streamed/uncapped/both-directions/incremental behavior survive unchanged as a declared *encoding* over a generic tap. **The reasoning here was not wrong** — `Sample` genuinely had no room for those things, which is exactly why a third parallel pipeline looked like the only option. It was an argument against the shape the chunks had, not against a generic pipeline as such, and decision 39's tap model was designed around that specific objection.

**Where the inline summary and the transcript disagree, and why that's intended:** the summary counted only what a single step received, capped; the transcript records everything, both directions, across every step. A reader comparing them sees different numbers. (The inline half was retired outright by decision 54.)

**The both-languages wire contract, and the rule this decision introduced.** dev-bench hand-writes its postcard encoding in C (`serial_protocol.c`), and nothing in either side's own test suite would notice the two drifting — a reordered field or a `u8` written as a varint decodes into plausible-looking garbage, not an error. So the exact bytes of a new record are pinned **twice**: as a literal COBS frame in dev-bench's ztest suite, and as the identical pre-COBS body in this crate's own `gatt_transcript_record_decodes_dev_bench_firmwares_own_hand_written_encoding`, which asserts postcard decodes them to the matching value *and* re-encodes to the same bytes. Changing the shape must break both. **This pairing found a real discrepancy the first time it ran** — and has now done so again for `StepResult` (decision 39) and been applied retroactively to `HelloAck` (decision 47), both of which predate the rule because it applied to *new* records only.

### 41 — A built-in table of vendor-defined GATT service identities (`vendor.rs`)

Decision 35's registry is per-repo and engineer-authored because what a *custom* characteristic's bytes mean is knowledge only that repo's engineers have. A vendor-defined service is the opposite kind of fact: Nordic's UART Service has the same UUIDs on every device that implements it, published in Zephyr's own `nus.h`/`nus/inst.h`. Requiring every engineer to transcribe `6e400002-b5a3-f393-e0a9-e50e24dcca9e` into their own `study-actions.toml` to write to a service the stack itself defines is pure error surface. So those identities ship as constants (`VendorService`/`VendorCharacteristic`, `NORDIC_UART_SERVICE`, `vendor::ALL`, `vendor::find_characteristic`), surfaced as `MergedAction::Vendor` and authored as `RowAction::Vendor { service, characteristic, operation, payload }` — picked by **id** (`"nordic-uart"`, `"rx"`), never by typing a UUID.

**Identity only. No semantics, ever.** This is decision 35's rule applied to a table that would be far more tempting to over-fill. It records *where* to write — which service, which characteristic, which operations the vendor declares there — and records nothing whatsoever about *what* to write: no command vocabulary, no line terminator, no "send `help` to list commands". Whatever sits behind a given DUT's NUS endpoint — a Zephyr shell, an application protocol, a bootloader, nothing at all — is that DUT's business, supplied per study as literal bytes exactly as `RowAction::Raw` does.

**An entry is a conditional, not a claim**: *if* a device exposes this vendor service, these are its UUIDs. `GattDiscover` against real hardware remains the only thing that answers "does this DUT actually have it?" — and that distinction is written down rather than assumed because the first DUT this was pointed at turned out not to expose NUS at all.

`VendorCharacteristic::properties` is included because it is part of the vendor's own declaration and decides whether a chosen operation is even legal: `build_study` refuses a `Write` against NUS TX (Notify-only) rather than letting it fail mid-study as an opaque ATT error. It remains the vendor's claim, not a measurement — `MergedAction::Vendor` carries a separate `discovered_properties`, and where the two disagree **live discovery wins and the disagreement is itself the finding**.

**No schema bump:** a vendor row resolves into an ordinary `Action::DataExchange` carrying plain UUIDs before anything is encoded, so dev-bench never learns the table exists — pinned by a test asserting a `Vendor` row and the equivalent `Raw` row build the byte-identical `Action`.

### 53 — `GattMonitorSelected`/`GattMonitorSelectedStart` — subscribe to the characteristics the study names

Raised by the repo owner authoring a real study: `GattMonitorAll` was the only monitor available and it is all-or-nothing. Subscribing to every notify-capable characteristic on a DUT that streams a high-rate waveform floods the serial link with traffic nobody asked for and buries the two characteristics the study is about.

Two variants at discriminants **9 and 10**, each carrying `Bounded<GattTarget, MAX_MONITOR_TARGETS>`; `GattTarget { service_uuid, characteristic_uuid }` is new in `gatt.rs`. **New variants beside the old rather than a `targets` field on the existing pair** — the repo owner's call. `GattMonitorStop` is reused unchanged: a window is a window regardless of how many characteristics it armed, and a second stop action would be two names for one thing.

**These are the first `Action` variants ever to carry a sequence, and that is a real cost, not a footnote.** Every monitor action before them was field-less, so dev-bench's hand-written C decoder walked them by tag alone; one that kept doing so would read the target-count varint as the next step's name length and decode the rest of the study into nonsense that still parses. `tests/firmware_test_vectors.rs`'s v14 vector pins exactly that shape — two targets, then a field-less `GattMonitorStop` whose tag has to land where the encoder put it.

**An empty target list is refused, not promoted to "everything"**, in the builder and in the UI: "monitor these" with nothing named is the not-thought-about case, and quietly subscribing to the whole table is the flood this action exists to avoid. Symmetrically, on hardware **a named target that isn't on the DUT, or that can neither notify nor indicate, fails the step naming it** rather than being skipped — the log-and-skip rule the unfiltered walk uses is right precisely because nothing there was named, and a study that names a characteristic has said it expects one.

### 56 — A characteristic gets a name: the vendor's, or the C identifier the firmware declared it under

Raised by the repo owner one decision after 53/55 gave a study something to name characteristics *for*: "the option show up as numbers." They did. Every picker asking "which characteristic?" labelled its options with the head of a 128-bit UUID, because a UUID was the only thing this crate could tell a UI about a discovered characteristic. On the DUT this suite is built against that means choosing between `00000002` … `00000008`, which differ in one hex digit and are in service-definition order, not in any order a human is thinking in.

**A UUID is the correct identity and a poor label.** Nothing about identity changes: the UUID is still what a checkbox's value carries, what crosses the wire, and what every tooltip shows.

Two name sources, neither a guess:

- **The vendor table.** A vendor-published characteristic already carries the vendor's own name; `VendorCharacteristic` gains a `short_name` (`"NUS TX"`) beside its full `name`, because a picker's label has room for a few characters and the place to decide the short form of a vendor's sentence is the table holding both. New `vendor::find_by_uuid` is the lookup direction the table never had: `find_characteristic` resolves a selection made *by name*, this resolves one something else found *by UUID*.
- **The firmware's own source.** `gatt_extract` always had the declaring C identifier in hand — it resolves `&sds_hrm_rrm_char_uuid` to 16 bytes to build the table at all — and **dropped it on the floor**. Keeping it costs one `push` and covers everything custom, which on a real DUT is nearly everything: [measured] 15 of the reference-dut's characteristics, named without asking its engineers for anything, because they already wrote the names down.

Vendor wins where both apply: source is one repo's spelling of a thing the vendor has already named.

**A label, never semantics** — the same line `vendor.rs` and `registry.rs` both hold, and the one this decision could most easily have crossed. `sds_hrm_rrm` says what the firmware's authors call this characteristic. It says nothing about what its bytes mean, when it notifies, or what writing to it does; that stays with `registry` (decision 35) and `decoder` (decision 52). So the shortening is mechanical and reversible — `label_from_symbol` trims the suffix naming a *variable* rather than a characteristic (`_char_uuid`, `_uuid`) and does nothing else. No title-casing, no `_` → ` `, and emphatically **no expanding `hrm`/`sds`/`rrm` into words**: every one of those is this crate deciding what a firmware team's abbreviation stands for, being wrong about it occasionally, and being trusted anyway. `GattName` carries its `source` and the untrimmed `origin` beside the label so a UI renders provenance rather than presenting a vendor's published name and a local variable's spelling identically.

**A name is optional and its absence is ordinary.** A live-only characteristic on a repo with no configured extractor has no name, and the picker shows the UUID head exactly as everything did before. Nothing fails, and nothing is invented to fill the gap.

**Services get names too, by exactly this mechanism** (amended the same session). `parse_gatt_services` was throwing away the *service*'s declaring identifier (`sds_service_uuid`) for the same reason and for the same length of time. `GattNameBook` gains `with_service_symbols`/`service()`, `vendor.rs` gains `find_service_by_uuid`, and `label_from_service_symbol` trims `_uuid` and **keeps** `_service`: `bds_service` is a heading, `bds` would be this crate deciding what the abbreviation stands for. Two maps rather than one, because a service UUID resolves against the vendor table's *services* and a merged map would have to guess which lookup a UUID wanted. `CharacteristicSymbol` accordingly became `GattSymbol { uuid, identifier, kind }` — one `symbols` list covering both, since a name lookup is keyed by UUID and a service UUID never collides with a characteristic's.

**Why not a `name` field on `GattCharacteristicInfo`.** That type is the `no_std`, wire-comparable shape a *live* `GattDiscover` fills in from an ATT response, and an ATT response carries no names. A source-only field on it would be a field hardware can never populate, and would break the comparability between static extraction and live discovery that decision 33 exists to provide. So names ride beside the table: `extract_labeled` returns `ExtractedGatt { services, symbols }` and `extract` becomes a provided method over it — one text-scan produces both halves, where an extractor asked for the table and then the names would read and re-parse the same files twice to answer one request.

### 57 — The GATT extraction scans the repo, not two files it was told about

Raised by the repo owner as a question rather than a bug report: "maybe the gatt discovery check can be project wide?" It could, and it had to. `ZephyrBleDefExtractor` hardcoded two paths — `lib/ble/ble_def.h` and `lib/ble/ble.c` — and `reference-dut-fw` has three `BT_GATT_SERVICE_DEFINE` blocks. The third is `lib/bds/bds.c`'s `sensor_bds` (Batch Data Service: `bds_ctrl_char_uuid`, `bds_status_char_uuid`, `bds_data_char_uuid`). Everything the scanner needed was already parseable and already in files it could read — the UUID macros are in the very header it opens (`ble_def.h:141-147`) — it was simply never handed the file. **A third of this DUT's GATT table had been missing for as long as the extractor had existed, and nothing anywhere could have said so.**

That is the actual finding, and it is worse than the missing service: `gatt_extract.rs`'s own doc comment opened by claiming it "fails loudly … rather than silently under-extracting". A bounded read of two named files *cannot* fail loudly about a third file, because it has no idea the file exists. **The loudness was real for everything inside its scope and vacuous about its scope.**

**What decides the scope now: the firmware repo's own ignore files, not a list this crate maintains.** The walk takes every `.c`/`.h` under `repo_root`, honoring `.gitignore`/`.ignore`/`.git/info/exclude`/global gitignore and skipping hidden directories (ripgrep's `ignore` crate, `gatt-extract`-gated like `regex`). `require_git(false)`, so a `.gitignore` still applies in an exported tree with no `.git` — an extractor that quietly widened its scan whenever pointed at a tarball would be the same silent failure in a different costume.

**The measurement is the argument.** [Measured 2026-08-26] on the real checked-out DUT, a naive `**/*.{c,h}` glob reads **1663** files and finds `BT_GATT_SERVICE_DEFINE` **six** times, because `.claude/worktrees/` holds two entire extra copies of the repo. Six services fit under `MAX_DISCOVERED_SERVICES = 8` with room to spare, so the naive walk would have emitted **three duplicated services without a word** — the same silent wrongness, merely inverted from under- to over-extraction. Honoring the repo's ignore files reads **218** files and finds the three real services.

**One hard block on top of that, at the repo owner's call: any directory named `embarch`** (`SCAN_BLOCKED_DIR_NAMES`), at any depth, whatever the repo's ignore files say. That directory is EmbArch's own per-engineer build config, which `embarch-core` plants *inside* the firmware repo being worked on — [measured] 917 `.c`/`.h` files of Zephyr build output on this DUT. It is gitignored there, but it is this suite that put it there, so this suite does not get to depend on the firmware repo having remembered. Never the walk root itself: pointing the extractor at a directory that happens to be named `embarch` is a deliberate act, not the accident the block is for. What it pruned is reported (`ScanReport::blocked_dirs`), because a hard block is exactly the kind of rule that stays invisible until it excludes something it shouldn't have.

**The loudness moves to the point of use.** Under a two-file read, every declaration scanned was a declaration in use, so raising on an unresolvable one was free. Under a repo-wide walk it is not: a malformed `#define X_UUID_VAL` in some third-party corner nothing references must not be able to blank the whole GATT table. So an unresolvable macro or variable is now *recorded as* unresolvable and raises only if a `BT_GATT_SERVICE_DEFINE` actually reaches for it. Failing loudly about things that affect the answer is the property worth keeping; failing loudly about everything a wide walk happens to see is how a defensive posture turns into a broken tool.

**Two failure modes a wide walk creates, both named rather than absorbed.** `ExtractError::DuplicateService(Uuid)` — two blocks resolving to one service UUID, i.e. a duplicated or vendored tree the ignore files didn't catch, caught even in a future repo that tracks one. `ExtractError::AmbiguousSymbol(String)` — one name carrying two different values in two files, reported instead of resolved by whichever file the walk read last. Alongside them, C `static`s are file-scoped, so a `&var` inside a service block resolves against **its own file first** and only then repo-wide: two files each declaring `static struct bt_uuid_128 service_uuid` is ordinary C and must not cross-resolve. And `ExtractError::NoSourceFilesFound` — a walk that reaches a real directory and comes back with no C at all would otherwise return an empty table, a plausible-looking answer to a question nobody asked.

**The caps are reached, not bypassed**, and there are now tests that say so: nine services hits `CapacityExceeded("MAX_DISCOVERED_SERVICES")` and seventeen characteristics in one block hits `CapacityExceeded("MAX_CHARS_PER_SERVICE")`. A repo-wide walk is precisely what makes finding nine services plausible, so the assertion stopped being theoretical.

**`ExtractedGatt.scan: ScanReport` — the extractor reports what it scanned:** files read, which ones contributed and what each contributed, what the hard block pruned, and what wasn't valid UTF-8. This is the half that kills the failure mode rather than patching this instance of it — a bounded read cannot report that it is incomplete, and a walk that reports nothing is one commit away from being incomplete again. Against the real DUT it prints three contributing files out of 218 read, so "it never opened the file I expected" is something an engineer can see rather than infer from a table that came back plausible.

**Order became a real question and is answered narrowly.** Services come back in sorted repo-relative path order, then source order within a file. That is *stable*, and deliberately **not** a claim about ATT handle order: within one file, source order was a fair proxy for the order a live `GattDiscover` walks the table, but across files the handle order is decided by the linker's section ordering, a build fact this scanner cannot read out of source and does not guess. Decision 33's byte-for-byte comparability is therefore weaker than it was — compare the two as **sets**. Flagged rather than papered over; nothing in the suite compares them positionally today.

**What deliberately did not change.** The text-scan still doesn't evaluate preprocessor conditionals (milestone-9.md §3.6), so a Kconfig-gated characteristic is still reported unconditionally — this decision widens *which files* are read and touches nothing about how a file is understood. `ZephyrBleDefExtractor` keeps its name even though the two files it was named for are gone from it: `static_extractor = "zephyr-ble-def"` is a value in real `embarch-ui` configs, and the remaining project-specific assumption — that a 128-bit UUID reaches a `bt_uuid_128` through a `#define <NAME>_UUID_VAL` — is real enough to keep the narrow name honest.

Three alternatives rejected: **a configured file/glob list per project** (`embarch.toml`, or `embarch-ui`'s `[study_designer]`) — explicit and auditable, and silently incomplete in exactly the way the two-file read was the moment someone adds a file, which is the bug. **An exclude-glob knob on top of the walk**, for now — it is the escape hatch if a *tracked* vendored copy ever trips `DuplicateService`, and the error names the two files when that happens, which is a better time to design the knob than in advance of any repo needing one. **Shelling out to `git ls-files`** — same file set with no new dependency, but it needs the git binary and a real checkout, and an extractor that returns nothing when pointed at an export is the silent failure again.

[Validated 2026-08-26] against the real checked-out `reference-dut-fw`: **3 services and 18 characteristics, up from 2 and 15**, all 18 named, plus the three service names decision 56 adds.

---

## BLE link control

### 43 — `Action::BleConnect.target_name` — naming the DUT instead of taking whichever advertises first

`target_address: None` was documented as "the common case", on the assumption that a bench has one advertiser. **It does not.** Found live on the first real stimulate-and-capture run: consecutive runs of the *same* study connected to visibly different peripherals — one saw a GATT table with a `0x1910` service, the next an entirely different table carrying two Apple 128-bit services, neither of them the DUT — and every study then failed with `"service not found on DUT"`, which is true and completely misleading. The service wasn't on the device dev-bench happened to reach.

`target_address` remains the precise filter but can't be authored ahead of time for a DUT advertising a resolvable private address, and nobody knows their DUT's MAC by heart. A name is what an engineer actually knows (`CONFIG_BT_DEVICE_NAME`). Both may be set; both must then match. Matched **exactly**, and against the advertised Local Name only — never the GAP Device Name characteristic (`0x2A00`), which would require connecting first, i.e. the very thing this exists to avoid. A blank or whitespace name means "no filter", not "match the empty name", so an untouched UI field can't become a filter nothing satisfies.

**A failed name match reports what *was* on the air** (`"no name match; on air: 'GABRIEL', …"`) rather than a bare `TimedOut`, because "nothing called X appeared, but these did" is the answer to the only question anyone asks at that point — and it immediately proved its worth: the DUT's real advertised name turned out not to be its configured `CONFIG_BT_DEVICE_NAME` at all. Wire v6 → v7, same append-don't-insert discipline as v6.

### 44 — `Action::BleSecurity { level }` — elevating the link is a step an engineer authors

The DUT this milestone was built for **requires an encrypted, MITM-authenticated link (Zephyr `BT_SECURITY_L4`) before it will tolerate GATT service discovery.** That is the engineer's answer to a direct question, per decision 35's no-inference rule — not something read off behavior. And the level has to be *authorable*, not pinned to what one DUT happens to need: the same requirement stated as "L4 always" would be wrong for the next DUT.

`BleSecurityLevel` is `L1`/`L2`/`L3`/`L4`, one-to-one onto Zephyr's `BT_SECURITY_L1..L4` — no security, encrypted-unauthenticated, encrypted-authenticated, LE Secure Connections authenticated with a 128-bit key. A study says which it needs; nothing in the suite defaults it, and `L1` is the honest way to say "this DUT needs none" rather than omitting the step and hoping.

**Why its own `Action` rather than a `require_security` field on `BleConnect`** — considered, and rejected on the ambiguity it would preserve. A `BleSecurity` step gets its own `StepResult` row with its own `Outcome` and error text, so *"connected, then failed to pair"* is distinguishable from *"couldn't connect"* and from *"discovery failed"*. Not hypothetical: this milestone lost a session to a deterministic `"disconnected during service discovery"` (4 of 4 attempts), which is what a failed elevation looks like when nothing in the pipeline can name elevation as a thing that happens. A separate step also composes with `delay_before_ms` (decision 42) and lets a study elevate at a point of its own choosing, or not at all.

**Semantics:** request at least `level` and wait for the link's security to actually change — or for the connection to drop — within the step's own `timeout_ms`. A link **already** at or above `level` is a `Pass`, not an error, since a peripheral that initiates its own elevation on connect (this DUT does, after a 200 ms delay of its own) can win the race. The **achieved** level is reported back, so a study that asked for L4 and got L2 fails loudly at the step that asked instead of proceeding into a discovery the DUT will refuse.

**What it deliberately does not carry:** a pairing method, a passkey, an IO capability, or anything about bonding. Same identity-only discipline decision 41 states for the vendor table — how dev-bench answers a pairing exchange is dev-bench's design ([embarch-dev-bench/decisions.md](../embarch-dev-bench/decisions.md) decision 34), and whether a bond survives the run is decision 11 there. A study says *what security the link must reach*, and nothing about how.

Appended at discriminant 7. Wire v11 → v12 / host v13 → v14, **re-derived at implementation time** rather than using the 8 → 9 this decision originally reserved: decision 39's amendment shipped first and took v9. That is [embarch-decision-reversals.md](../embarch-decision-reversals.md) row 18's protocol working as intended rather than a number being corrected.

Three things implementation had to settle:

- **Where the achieved level is reported.** This decision said "reported back" without saying where, and there was nowhere: `StepResult` had no field. It gets `security_level: Option<BleSecurityLevel>`, appended (§4.5), populated on **every** step, not only a security step. That is a strictly larger claim than this decision made, and it is the one that pays: `"disconnected during service discovery"` at L1 and the same failure at L4 are different findings, and until this field existed a result could not tell them apart. `None` means there was no connection to ask about, never that nobody looked.
- **What "fails loudly" is, mechanically.** The step `Fail`s when the reached level is lower than asked. No separate "request it but don't insist" flag: `continue_on_fail` (decision 13) is already exactly that knob, and adding a second would be two ways to say one thing.
- **`L1` really is authorable, and the first implementation got that wrong.** It refused `L1` as "a level to report, not one to elevate to" — which reads sensibly and contradicts this decision's own text. Corrected before commit; the refusal is gone from the builder, the firmware and the UI dropdown, and an `L1` step passes under the same already-at-or-above rule as every other level rather than by a special case. Recorded because the failure is instructive: **the design was already written and the implementation invented a stricter rule than the design asked for**, which is the same shape as ignoring it.

[Validated on hardware 2026-08-26] against `the client S11 B9C3`: `connect` `Pass` at L1, `BleSecurity { level: L4 }` `Pass` reporting **L4**, then `GattDiscover` `Pass` returning **7 services**. Discovery of that table had never once succeeded before this pass. Three runs of the same study, identical results. dev-bench's own log names the pairing method that actually ran — `LE SC Numeric Comparison (authenticated)` — rather than leaving it inferred.

### 50 — `Action::BleUnbond {}` — dropping the bond is a step

Decision 44 gave a study a way to *reach* a security level and no way to get back, and [embarch-dev-bench/decisions.md](../embarch-dev-bench/decisions.md) decision 11 clears bonds only between studies. So the only way to author a second pairing exchange was to end the study — which is not the same experiment: a bond re-established inside one run exercises the reconnect path, and one re-established across two runs exercises the bench's reset. "Pair, do work, drop the bond, pair again" is a real test.

Field-less, appended at discriminant 8 alongside decision 44's variant, one wire bump for the pair — `BleUnbond` is only reachable once something can establish a bond, so shipping decision 44 alone would have shipped half a feature at two reflashes' cost.

**It drops the link, and that is stated rather than mitigated.** Zephyr's `bt_unpair` disconnects a peer whose keys it clears. dev-bench does not choose that and does not work around it: a link whose keys just went away is not a link. So a study that unbonds mid-run needs its own `BleConnect` afterwards — which is what "pair again" meant. `StepResult.security_level` is `None` for the step, correctly: by the time it returns there is no connection to ask about.

**Why an action rather than a lifecycle setting**, having considered the alternative: decision 44's own argument. A step gets its own `Outcome` row, composes with `delay_before_ms`, and lets the author choose the moment. A `clear_bonds_between_steps` flag on `Study` could not express "here, and not there". The companion half — bonds cleared at *study end* rather than only on the next `Hello` — is dev-bench's ([embarch-dev-bench/decisions.md](../embarch-dev-bench/decisions.md) decision 37).

---

## What a study declares about what it runs against

### 40 — A study declares the firmware versions it is meant to run against; reflashing is the operator's per-run choice

Prompted directly, and it closed a gap wider than the one it was raised for: **a `StudyResult` could not say what it ran against.** Two runs of the same study against two different builds produced results indistinguishable after the fact — the same silent-mislabelling class decisions 39 and 35 both exist to prevent, sitting unnoticed in the middle of the thing the whole suite produces.

`Study.requires: Requirements { dev_bench_version, firmware_version }` — two free-form strings, matching `HelloAck.firmware_version`'s shape ([embarch-dev-bench/decisions.md](../embarch-dev-bench/decisions.md) decision 18: whatever the build embeds, typically `git describe --always --dirty --abbrev=8`). **Host-side only — it never crosses the wire to dev-bench**, which has no use for a requirement it cannot check about itself, and `steps_crc` seals what dev-bench actually executes, unchanged. A test asserts that structurally rather than by inspection: two studies differing only in `requires` must encode byte-identical `StudyStart` messages and the same `steps_crc`.

**Both fields are mandatory, and `any` is an explicit legal value.** "I don't care which build" is a legitimate answer — a dev-bench self-test involves no DUT at all — but it has to be *said*, not achieved by leaving a field out. `Requirements` has no `serde` default, so an omitted `requires` fails to deserialize rather than quietly becoming `any`, and a *blank* one is a separate explicit pre-flight failure (`Requirements::validate`). Because the failure this decision exists to prevent is precisely the one where nobody thought about it.

**Reflash is a run parameter, not a study field**, the same split decision 39 draws for signal routes: a `Study` describes *what the experiment is*, and how a particular run is set up to satisfy it is the operator's call at run time. Baking it in would mean a saved study (decision 38) that reflashes a board every time you re-read its results. The override and the flashed version therefore cross as **`POST /study` query parameters** — `?allow_version_mismatch=1` and `?flashed_firmware_version=<string>` — because a parameter of the *request* is literally a run parameter, and because that leaves the `Study` body byte-identical, so both seals and every fixture on disk are untouched. Query rather than a header, for the same reason the override is recorded rather than honoured silently: a query parameter shows up in Core's request log and in a `curl` an engineer types by hand.

**On a mismatch with no reflash requested, the study is rejected before any step runs**, naming both strings — the same shape `doctor` check 13 already fails in. Not a warning that proceeds: a result attributed to the wrong firmware is worse than no result, which is this decision's whole premise. An explicit override is available and is **recorded in the result** (`Provenance.overrides`, host v10; the flashed version needed no new field — `firmware_version` carries what was flashed and `firmware_source` becomes `FlashedThisRun`) rather than silently honoured.

**The verification asymmetry, which is the load-bearing limitation and cannot be designed away.** dev-bench *self-reports* its version over `HelloAck`, so a dev-bench requirement is genuinely **checked**. The DUT reports nothing at all: Core flashes it through a debug probe with no readback path. So a `firmware_version` requirement is only verifiable when either the outpost is compiled in (its header record carries a build ID, [embarch-outpost/design.md](../embarch-outpost/design.md) decision 9) or **the run just flashed it**. `StudyResult` therefore records not just the versions but **how each was established** — `ReportedByDevBench`, `ReportedByOutpost`, `FlashedThisRun`, or `Declared` (asserted, unverified). A result quietly presenting a declared string as a verified one would be the same defect in a new place.

**A consequence this decision did not anticipate, and the most useful thing its implementation produced:** supplying the flashed version is also what makes `requires.firmware_version` *checkable*. The asymmetry above said a DUT requirement is verifiable "when the run just flashed it" — that sentence had no implementation anywhere, and it is now Core's gate rejecting on the DUT half, not only the bench's. What the flashed string *is*, stated because the asymmetry does not go away: `embarch-api` derives it from the *tree it built*, via a project-declared `version_command` defaulting to `git describe --always --dirty --abbrev=8` — not from the board. Nothing reads a version back off a DUT. `FlashedThisRun` is therefore stronger than `Declared` (nobody checked that at all) and weaker than `ReportedByDevBench` (a measurement), which is exactly the ordering `VersionSource` exists to express.

`requirement_satisfied(required, actual)` lives in this crate so Core's version gate holds no second copy of the comparison rule, and `VersionSource::is_verified` decides whether a version renders as verified so no UI re-derives which variants count.

**The human surface landed 2026-08-26** ([embarch-ui/design.md](../embarch-ui/design.md) decision 11), and it is the first thing that ever stated a real requirement: the Study Designer had been submitting `Requirements::any()` unconditionally — honestly, since it had no fields to say anything else in. Both fields are now prefilled from live bench state, `any` is a visible checkbox rather than an empty field that happens to validate, and a blank field is **refused rather than quietly promoted to `any`**, which is the distinction this decision rests on.

### 45 — A study declares the GATT table it was authored against, and live discovery is what checks it

Three sources of GATT knowledge existed in this crate, built at three different times, and **nothing ever joined them**: `vendor.rs`'s vendor identities (decision 41), `gatt_extract.rs`'s static extraction (decision 33), and the engineer-authored registry (decision 35). A `Study` could reference any of them and declared none, so nothing could answer the question this milestone actually got stuck on — *is the service this study writes to even present on the build under test?* A whole session ran without that being answerable, because the DUT's GATT table had never once been seen.

`Study.gatt: Option<DeclaredGatt>` — `{ source: GattSource, services }`, reusing §4.3a's `GattServiceInfo`/`GattCharacteristicInfo` rather than a parallel shape, so a declaration and a live discovery result are literally the same type and comparing them is a comparison, not a translation. `GattSource` is `Vendor { ids }` (resolved from `vendor::ALL`), `Extracted { repo, revision }` (produced by `extract-gatt-config` against a real checkout, recording *which* checkout), or `Authored` (typed in). Host-side only, like `requires` — it never crosses the wire, and dev-bench continues to interpret nothing.

**Live discovery wins, and the difference is reported rather than tolerated.** `vendor.rs` already stated this rule for the vendor half; generalised here. When a `GattDiscover`/`GattMonitorStart` step runs in a study that declared a table, Core reconciles the two and records what was declared-but-absent, present-but-undeclared, or present with different properties. A declared service missing from the DUT is **not a study failure by default** — it is the single most useful line in the result, and it is exactly the fact (`CONFIG_BT_ZEPHYR_NUS=y` was set, but was the service actually registered?) that nobody could produce for a whole session.

This is the durable form of decision 35's rule. That decision said engineer-supplied knowledge must come from the engineer; this one says **where in the study it goes**, so an agent authoring a study has a field to put it in rather than a temptation to infer it.

---

## Protocol manifests (`.eap`)

### 58 — A protocol manifest an engineer writes and the tool never infers: `embarch/protocols/*.eap`

Opened by the repo owner with a design draft written against a real firmware's BLE stack rather than against this suite's own code, closing two things at once: decision 39's write direction, rejected at the time as premature because nothing in the model had conditional logic, branching or multi-step state; and milestone 11 §3.8's real-hardware step, blocked since 2026-08-24 on "user-supplied DUT protocol knowledge" with no mechanism for a user to supply any.

A per-repo `<firmware-repo>/embarch/protocols/<name>.eap` ("EmbArch Protocol") holds one or more named `protocol { … }` blocks: characteristic aliases, frame shapes, session variables, and a state machine. It sits beside `study-actions.toml` (decision 35) and `study-structs.toml` (decision 52), for the reason those two are there — it is engineer-authored knowledge about *this* DUT, and it belongs in the repo that knows it. A protocol block is **self-contained**: it declares its own characteristic aliases rather than referencing a `Study`'s taps, so one `.eap` protocol is a portable unit any study can invoke without first being wired up to match.

**Resolved into the submitted `Study` at build time**, as `Study.protocols`, referenced by a `u8` index from `Action::RunProtocol` the way `StreamEncoding::Struct { decoder }` indexes `Study.decoders`. Decision 52 had already settled the same question for payload layouts one day earlier and for an independent reason: **Core cannot read the firmware repo.** A study naming a manifest rather than carrying it would render on its author's machine and nowhere else, and would behave *differently* after an unrelated edit to that file.

**The draft bound a manifest by a CRC over its text, and that is the one thing here that changed.** It was proposed as the same integrity pattern `steps_crc`/`streams_crc` use, citing `StreamEncoding::OutpostTrace { manifest_crc }` as precedent. That precedent had been **reversed the day before** ([embarch-decision-reversals.md](../embarch-decision-reversals.md) row 37) and is now a unit variant. Half of why does not apply here — the outpost's manifest is generated from a linked image, so no CRC of it exists at compile time, whereas an `.eap` file is authored and does exist. The other half applies exactly: it is the write-ahead staleness pattern [embarch-topology/design.md](../embarch-topology/design.md) decision 3 exists to eliminate, and a saved study's pinned CRC would go stale on the author's next edit.

**Where it parts company with `decoders`, and why that costs a third seal.** `Study.decoders` is host-only and sealed by neither CRC, because a layout only decides how the host *renders* a byte already captured. A protocol is the opposite: dev-bench **executes** it (decision 60), so it crosses the wire like `steps` and gets a seal like `steps`. `protocols_crc` is a **sibling** rather than a widening, per decision 17's structural rule.

**Amended 2026-08-26, one field short.** As first shipped, this resolved a manifest into `Study.protocols` and sealed it — and stopped at the host. `StudyStart` carried no `protocols` at all, so the field existed everywhere except on the one hop that had to execute it, and `Action::RunProtocol` named an index into something dev-bench had never been sent. `StudyStart` now carries `protocols` and `protocols_crc`, **appended after `dev_bench_log_level`** rather than inserted beside `streams_crc`: postcard is positional and this wire's rule is that a new field goes on the end, so the diff a human checks is a suffix. Decision 17's structural rule — each seal immediately after the one contiguous span it covers — is a property of the *pair*, not of where the pair sits, and holds either way. [embarch-decision-reversals.md](../embarch-decision-reversals.md) row 68; the executor is [embarch-dev-bench/decisions.md](../embarch-dev-bench/decisions.md) decision 41.

**Syntax is a small purpose-built text grammar, not TOML/YAML/JSON.** The grammar is inherently recursive — frames select on magic bytes, records repeat other records, fields parametrize how later fields are read — and that nests far more legibly as text than as table-of-tables TOML. It stays pure data: the parser produces an AST with no code, no `eval`, and nothing executable beyond the fixed primitive set decision 59 admits. Full grammar in §4.9.

### 59 — A fixed, closed set of decode primitives, split by what a running state machine can reach

The primitive set was checked against a real, currently-shipping protocol (the the client S11 reference-dut's SDS/DMS/BDS services) that exercises every awkward case this kind of description has to survive: magic-byte format versioning with no version handshake, self-describing descriptor tables that parametrize how later bytes are read, delta+zigzag+variable-bit-packed payload columns, CRC32-validated records, and a real flow-controlled state machine. **Every primitive exists because that protocol needed it; none were added speculatively.**

Sized/endian integers; `fixed(scale, unit)`; byte spans; `select_if` magic-byte dispatch; `repeat[count_from: <field>]` for descriptor-table-parametrized parsing; `bitpack[count_from:] width_from: … delta zigzag seed:` for the compression primitive underlying every batch format checked against; and `crc32` with a per-frame `skip|error|retry` policy.

**Deliberately no plugin trait and no escape hatch**, unlike decision 33's `GattConfigExtractor`, which extends per firmware because UUID extraction genuinely varies per build system. Byte codecs do not vary that way — every format this suite has seen (`BSS\x00`…`BSS\x03`, `PPG1`…`PPG8`, `GWF1`) is the same handful of primitives recomposed. A future firmware needing a primitive this list lacks is a real decision to extend the list, not a silent per-firmware workaround.

**The split, which is this decision's real content and was not in the draft.** With dev-bench as the executor (decision 60), every primitive the wire carries is C the bench has to run, and every future addition costs a firmware reflash and a decision 36 re-pinning pass. So the grammar divides by **what a running state machine can reach**:

- **Crossing the wire:** `select_if` predicates, integer scalar reads at fixed offsets, byte-span *lengths*, write templates, and the expression set — everything a `when`, a `remember` or a `write` can name.
- **Staying host-side**, parsed from the same file and applied at render time over the raw bytes the tap already wrote: `repeat`, `bitpack`, `crc32`, and `fixed`.

**The line is not a compromise, it is where the consumers are.** No guard in either worked protocol references a bit-packed column — guards read headers (`progress.total`, `chunk.bps`) — and with `ProtocolOutcome` reporting only a state name (decision 62), dev-bench has **no consumer at all** for a bit-unpacked value. Putting one in hand-written C would buy a capability nothing uses, on a board this project has had to shrink things to fit three times, and would make the whole grammar reflash-costing rather than just the small half of it.

**Two things the grammar does not have, both refusals rather than omissions.** The draft's `crc32 ieee seed: <literal>` loses its seed parameter: CRC-32/ISO-HDLC — init `0xFFFFFFFF`, reflected in and out, final XOR `0xFFFFFFFF` — already *is* what that spelling names and is bit for bit Zephyr's `crc32_ieee`, so a configurable seed would mean constructing a custom algorithm per frame, i.e. the second CRC implementation the draft's own constraints asked not to exist. `policy` stays, because it genuinely varies per frame. And **`crc16` is refused by name**: Zephyr ships several mutually incompatible CRC-16s (ANSI, CCITT, ITU, each with its own seed and reflection), the design named none, and neither worked protocol uses one. Guessing which would be the inference this suite refuses everywhere else; implementing all four would be four primitives with no caller, the shape [embarch-core/decisions.md](../embarch-core/decisions.md) decision 30 already records as a mistake worth not repeating. One line to add the day a real frame names a variant.

### 60 — `Action::RunProtocol` — stateful sequencing, executed by dev-bench

`{ protocol: u8, entry_state: u8 }` hands the link to a declared state machine for the length of one step. Named states, `on_enter` writes, `on_event <frame>` transitions with `remember`/`when`/`otherwise`, `on_timeout … retry N`, and terminal states mapping to the existing `Outcome`. It spans steps the way `GattMonitorStart`/`GattMonitorStop` (decision 36) does, but where that pair opens a time window this one runs a machine — which is what decision 39's rejected `StreamSend`/`StreamExpect` was reaching for and could not express. The executor shipped the same day ([embarch-dev-bench/decisions.md](../embarch-dev-bench/decisions.md) decision 41).

**Where the loop closes was the hard question, and the first answer was wrong.** The draft asserted both that `RunProtocol` "crosses the postcard wire to dev-bench like every other `Action`" *and* that the interpreter is `std`-only and host-side. Those are incompatible: something has to close decode → decide → write. Two arguments were made for Core closing it and **both were mistaken, recorded because the correction is the reasoning**:

- *"The board is at 98.5% of `sram0_0_seg`."* Real but stale — the pre-decision-54 number. Deleting `gatt_activity` took the ESP32-C5 to **81.12%**, and reversals row 60 found another ~10.5 KB was a mis-sized inbound buffer. There is room.
- *"Core in the loop is too slow."* At 1 Mbaud a Core↔bench round trip is single-digit milliseconds against a BLE connection interval of 7.5–30 ms that already dominates a chunked download — perhaps 1.1–1.6× on the pump loop, against a stall watchdog measured in seconds. Not the objection it was presented as.

What actually decides it is the third consideration: **under Core-side execution nothing new crosses the wire, but Core would have to send something mid-study for the first time** — the proposal's own unbuilt "v3" tier — and under bench-side execution the manifest crosses but the lifecycle does not change. The repo owner chose bench-side, which keeps `main.c`'s receive-then-run model and Core's silence after `StudyStart` exactly as they are. **The cost is stated rather than hidden:** what a payload *means* now reaches the bench, which is the knowledge decision 39 took away from it and decisions 52 and 55 each restated — `struct dbm_stream_tap` drops `encoding` for precisely this reason. Decision 59's split keeps that cost to the smallest set of primitives a machine can actually reach, and the mid-study write tier stays unbuilt, which is the compensating simplification.

**Nothing here can transition on a write's own ATT response**, whether or not it is `with_response`, and that is deliberate. On the DUT this was designed against, a control-point write's response confirms only that the write was *accepted*; the authoritative answer arrives later as an independent notification on a different characteristic. A machine that could branch on the ack would be branching on the wrong fact and would look correct doing it. `with_response` selects the ATT operation and nothing else.

**The expression evaluator**, which the draft flagged as open and did not resolve. A small fixed set, and the architecture made it smaller than the draft's:

| In | Why it is there |
|---|---|
| Integer literals (`i64`, decimal or `0x`) | The only literal a guard needs |
| `session.<var>` | A run's own carried state |
| `<frame>.<field>` | A scalar of the frame that triggered this event |
| `len(<frame>.<span>)` | The only way a byte span's contents affect anything |
| `+` (saturating) | A flow-controlled pump loop must accumulate a count and there is no other way to say it |
| `== != < <= > >=` | One comparison per guard, checkable at a glance |

Out, each for a stated reason: **`++` (byte-span concatenation)** — the draft's `buffer = buffer ++ chunk.payload` accumulated an entire download in a session variable to compare its length against a total. On the bench there is nowhere to put those bytes and nowhere they are needed: the chunks are already streaming out on their own tap as they arrive, so `received = received + len(chunk.payload)` says the same thing in eight bytes of state. Session variables are therefore **integers only**. **`-`, `*`, `/`, `%`** — no worked protocol needs one, and each is a permanent widening. **`&&`, `||`, `!`** — `a && b` is two states and `!a` is swapping `when` and `otherwise`; neither omission costs an author a protocol they could otherwise write. **Nesting and parentheses** — an expression is `operand [+ operand]` and a guard is `operand cmp operand`, one level. **Any function but `len()`**, and any user-defined one at all.

Addition **saturates** rather than wrapping: a wrapping counter is a plausible wrong number, the failure this crate keeps refusing, and a saturated one stops a guard passing, which the step timeout catches and reports. An operand that cannot resolve — a field a truncated notification did not carry — makes a guard **false**, never true, and makes a write **not happen** rather than happen with a zero substituted in.

**One finding came out of writing the tests rather than the design**, and it is in §4.9's worked example for that reason. An `on_event` arm with no `otherwise` consumes the frame, applies its `remember`s, and stays in the state *without re-entering it* — no `on_enter` re-send, timeout still running from the original entry. `otherwise: goto <this state>` is a different thing: it re-enters, which re-sends the flow-control ack and restarts the stall watchdog. A pump loop needs the second, and the first draft of the fixture wrote the first — it consumed every chunk correctly, acked none of them, and stalled at the watchdog. Both behaviors are real and the author says which.

### 61 — A write is built from the same typed vocabulary as a decode

Inside a `RunProtocol` block, a `write`'s payload is assembled from decision 59's primitives, each field taking a literal, a `session.*` variable, or a field of the frame that triggered the current event. Required for anything like a live epoch in a time-sync write, or the echo-back-the-last-seen-length pattern where a client must reply with exactly the length it was notified — a payload computed purely from constants expresses neither.

It **replaces literal-only writes only inside a `RunProtocol` block.** Decision 35's registered actions are enumerated-values-only by design, precisely so nobody uses a value whose meaning nothing recorded, and they are untouched.

### 62 — A protocol run reports the state it stopped in, and nothing it could lie about

Decoded fields are addressable by name everywhere inside a manifest — in guards, in `remember`, and in a `write` (decision 61) — which is what makes the state machine expressible at all. **`ProtocolOutcome` is `{ final_state, outcome }`** and nothing more.

Two things the draft wanted here are not built, both because a decision made days earlier already answered them:

- The draft had `StepResult` carrying a bounded `heapless::Vec` of every decoded field a run saw, addressable by path. That is the exact shape decision 54 retired `StepResult.gatt_activity` for, one week earlier and on measurement: a bounded in-memory copy of something unbounded and streamed lets a result *look* complete while holding a fraction of what arrived. Decoded values reach a reader the way every other captured byte does — through the tap the study declared, rendered host-side. So `ProtocolOutcome` carries the one thing the tap file structurally cannot say. Whether that state was terminal is not stored either — it is a lookup in the `ProtocolDef` the `Study` already carries, and a stored copy could disagree with it.
- The draft had decoded output reaching `Study.validations`. **There is no such field**: decision 48 removed post-hoc validation outright. Its terminal states are the assertion instead — a manifest declares `outcome: pass|fail` where the protocol knowledge lives, and a study passes or fails on which one it reaches. §7's standing position on the rest is unchanged: checks over real capture data get designed against that data, and a real `RunProtocol` run is the first thing that will produce any.

**Where a `ProtocolOutcome` lands, confirmed rather than assumed.** `EventsJsonWriter` hand-writes only the *envelope* — `study_name`, the `steps` array's brackets, `provenance`, `streams` — and serializes each `StepResult` through serde, so this field reaches `events.json` automatically and a test asserts it does. It reaches `GET /study/{id}` with it (`result` is that file read back as a `Value`) and rides the `StepCompleted` SSE event, which carries the whole `StepResult`. `streams/index.json` deliberately says nothing about it: that file describes declared capture channels, and a protocol run is not one — it writes through whatever taps the study already declared.

**`StreamEncoding::GattDecoded` is not added either.** The draft proposed it as a passive-capture counterpart mirroring `OutpostTrace { manifest_crc }` — a precedent that no longer exists (decision 58) — and it would have been a second rendering path for GATT notifications one day after decision 52 shipped the first. Instead an `.eap` frame flat enough to be one **lowers into decision 52's own `StructLayout`**, so a frame an engineer already described for a state machine does not have to be described again in TOML to also be rendered. One rendering mechanism, two front ends. A frame the layout cannot express — a `count_from` repeat, a bitpack, a trailing CRC — gets **no layout rather than an approximate one**, decision 52's own rule: the raw `.bin` is on disk either way, so a missing rendering can be redone and a wrong one silently misreads every row.

---

## Authoring surfaces

### 6 — Symmetric human/agent access

Follows the suite-wide principle already established for Core/API (`embarch.md` §5: every hardware-facing capability is reachable both by an agent and directly by a human, converging on the same underlying modules). Concretely, study-running code means new MCP tools *and* CLI subcommands (§6) — not one without the other, matching `build`/`flash`'s existing pattern. Decision 26 exists because decision 17's CRC requirement would otherwise have broken the human half of this.

### 34 — A Study Designer UI: an interactive, table-based `Study` builder

**Implemented 2026-08-24** (milestone 11): `src/study_builder.rs` (table rows → `Study`) and `tools/study_designer_ui.rs` (the `axum` server, since retired — see below), live-smoke-tested against the real `reference-dut-fw` repo.

Motivated by a real gap Milestone 3's own closing session hit directly: a real `GattMonitorAll` run against the reference-dut DUT came back with an **empty `gatt_activity`** — nothing was captured because nothing in that `Study` ever *wrote* anything, and there was no way for whoever authored it to know what to write, since that is DUT-specific knowledge no generic discovery can produce. Closing that gap needed two things: a real authoring UI (this decision) and a place for that DUT-specific knowledge to live (decision 35).

**Shape:** the main surface is a table where each row is a `Step` — an `Action` from a dropdown, its parameters filled in, `timeout_ms`, `continue_on_fail`. Rows can be added, removed and reordered, and **sequencing is expressed purely by row order**, not a separate precondition field, matching how `Study.steps` already works (§4.1; no state passes between steps, per decision 32's self-contained-action stance).

**The action list a row can pick from is merged from three sources, not one:** this crate's built-in `Action` variants; live `GattDiscover` results, when a DUT happens to be connected; and `GattConfigExtractor`'s static output (decision 33) — the same dual-source cross-check decision 33 established, now feeding one UI instead of being two things a human diffs by hand.

**Scope: author, run, and watch — read-only outside the authoring table.** It can submit the `Study` it just built and poll each step's live result, because a human shouldn't need a second tool to try what they built. It does **not** build or flash anything — provisioning the DUT/dev-bench (`build_and_flash`/`build_and_flash_dev_bench`) stays a separate `embarch-api` step, done before the "run" button means anything.

**This crate's own `tools/study_designer_ui.rs` binary is retired** (2026-08-24, milestone 1 §4.9). `embarch-ui`'s Study Designer tab is the successor: the same merged action list, the same table model, the same registry, but calling `registry`/`merged_actions`/`study_builder` in-process rather than running a second local web server, and submitting via `embarch-core-client` over HTTP+Bearer rather than shelling out to `embarch-api`'s CLI — which is the "left to implementation" question this decision deliberately deferred, resolved by `embarch-ui` rather than here. `src/study_builder.rs`, `src/registry.rs` and `src/merged_actions.rs` are entirely unaffected; only the binary that wrapped them in a server is gone.

### 35 — A user-authored custom-action registry: names and enumerated parameter choices only, never a semantic description

This is the actual fix for what motivated decision 34. Closing Milestone 3, an attempt to figure out what a custom GATT write "does" by reading the DUT firmware's own source and asserting a conclusion from it **was flagged directly as destructive to the dev process** — reading code and inferring behavior from it isn't the same as knowing it, and presenting that inference as fact is worse than not answering at all. The fix isn't a smarter inference; it is removing inference from the loop entirely: this knowledge only ever comes from the engineer, explicit and unambiguous, through a registry the UI reads and writes.

**What the engineer provides — mechanical, not documentary:** for a detected characteristic they want to use, a freely-chosen `name` (shown in the dropdown), which characteristic it targets, its `operation` (read/write/subscribe/notify/indicate), and — for a write — its payload described as one or more named fields, each with a small enumerated set of engineer-supplied `{label, value}` pairs. Building a step against a registered action means clicking a name and clicking a value; nothing is typed as raw hex, and **nothing describes *why* a value does what it does — there is deliberately no "what this does" field at all**, since that would be this crate inventing a place to write down another guess.

A value's bytes are **the engineer's own literal bytes, never a numeric type this crate encodes itself** (which would require assuming a width and endianness nobody here is in a position to know). `ActionRegistry`/`RegisteredAction`/`ActionField`/`ActionFieldValue` in `src/registry.rs`, **implemented 2026-08-24** and confirmed round-tripping against the real `reference-dut-fw` repo; the correction that a value's bytes are the engineer's literal bytes, and why, is milestone 11 §3.1's own account.

**Persisted in the firmware repo's own `embarch/` folder** as `study-actions.toml`, sibling to `embarch.toml` — it travels with the firmware, is versioned in that repo's git history, and is shared across engineers the same way `embarch.toml` already is; not a catalog this tool owns separately, and not re-entered per `Study`.

**The durable principle, stated plainly since it generalizes past this one crate:** *no EmbArch component should ever present an inference about what a specific piece of hardware or firmware does — derived from reading its source, its comments, or any other heuristic — as established fact.* Where that knowledge is needed, the answer is a pipeline for the engineer who actually knows to supply it explicitly, built once, generically, for any project. This registry is that pipeline for "what does this GATT action do", not a one-off for `reference-dut-fw`. Decisions 41, 45, 52, 56 and 58 are each that rule applied somewhere else.

### 37 — A free-text payload path alongside the registry: `RowAction::Raw`

Decision 35's registry is the right home for a *named, reusable* action, but it was the only way to send a payload at all, which makes a one-off — an ad-hoc shell command, a value being tried once to see what happens — require editing `study-actions.toml` first. `RowAction::Raw { service_uuid, characteristic_uuid, operation, payload }` (§4.3c) takes a UUID pair typed directly and a payload supplied as literal bytes.

**This does not weaken decision 35.** That rule forbids two specific things: this crate inventing a *semantic description* of what an action does, and this crate *encoding a number into bytes* on an engineer's behalf. `Raw`'s payload is already bytes when it reaches this crate — parsed client-side by the same parser the registration form uses, from either UTF-8 text with explicit escapes or hex tokens — so nothing here interprets or encodes anything. The registry remains how an action gets *named and re-used*; this is how one gets *sent before it has a name*.

`Uuid::parse` arrives alongside it, accepting the hyphenated 128-bit form, 32 bare hex digits, or the 16-bit shorthand expanded against the Bluetooth SIG Base UUID. That expansion is a Core Spec fact — a 16-bit UUID *means* that 128-bit value by definition — not an inference about any particular DUT, so it doesn't cross decision 35's line either.

### 38 — A saved-study library at `<firmware-repo>/embarch/studies/*.json`

Until this, a `Study` authored in the UI existed only as long as the browser tab did; re-running one meant rebuilding the table by hand. Saved studies live beside `study-actions.toml`, same per-repo convention, so a study travels with the firmware it was written against and is versionable with it.

**The file *is* a `Study`** — `embarch-api run-study --study-file <path>` re-runs it directly, with no conversion step. The authoring rows ride along in one extra key, `_embarch_ui_rows`, which `Study`'s own deserializer ignores (no `deny_unknown_fields` anywhere in this crate). That single-file choice is what makes a saved study both re-runnable from the CLI *and* re-loadable into an editable table; a sidecar file would have made one of the two lossy or the pair separable. A `Study` JSON dropped into that directory by hand or by an agent is still listed and still runnable — it just has no rows to load back, and the UI says so rather than offering a Load that would silently produce an empty table.

This is also what makes decision 39's `StreamSource::Signal` and decision 40's reflash-is-a-run-parameter rules load-bearing: a saved study has to survive a rewired bench and has to not reflash a board every time someone re-reads its results.

---

## Things this crate deliberately does not have

Removals are decisions in their own right and keep their numbers. Two entries here are **retired** — their content is history rather than a description of the crate — and are kept as tombstones per [DOC-PROTOCOL.md](../DOC-PROTOCOL.md) §7.4, so a reference landing on them finds an explanation rather than a gap.

### 22 — `Action::Validate` is removed

Its job — checking a prior step's captured data against an expected value — moved to the Core-side post-hoc mechanism (decision 19), which was itself later removed outright (decision 48). Keeping both would have meant two overlapping validation systems. dev-bench firmware has had no validation-related code path since.

### 48 — Post-hoc validation is removed outright — the whole notion, not a field

`Study.validations`, `StudyResult.validations`, `PostHocValidation`, `PostHocCheck`, `ExpectedValue`, `SignalCheck`, `ValidationSource`, `DataChannel`, `ContentValidity`, `ValidationResult`, `signal.rs`'s evaluation logic and the `core-validation` Cargo feature are all gone. Decision 19's post-hoc half and decision 28 are retired with it; decision 19's real-time `Outcome` half is untouched and is what every study has always actually used.

**It was never once used.** That is the decision, and everything else is detail. `embarch-core`'s `events.json` writer wrote a hardcoded `"validations":[]` — not "empty because this run had none" but a literal string in the source, because Core never evaluated a validation in its life. Decision 28's `validate_on_abort` field was designed and never added to `Study` at all. The `SignalCheck` variant set was described in its own §7 bullet as an "illustrative placeholder", and its `FftPeakNear` was implemented as a naive O(n²) DFT against synthetic signals, because no real signal ever reached it. The one thing that would have made any of it real — power and sensor hardware producing data worth checking — was deferred to the Later bucket earlier the same day.

**What it cost to keep, [measured 2026-08-25].** `ExpectedValue` inlines two `MAX_PAYLOAD_LEN` buffers, so `PostHocValidation` is 576 bytes; times 64 gives a **36,872-byte inline array** in `Study`. After decision 46 fixed `steps` — the field that actually crashed a debug `embarch-api` — `validations` was **97% of what remained**. `Study` was 77,368 bytes at the start of that pass, 37,960 after decision 46, and **1,088** after this. Decision 46 got a 2× reduction; removing this got a further 35×.

Host v10 → v11, `DEV_BENCH_WIRE_SCHEMA_VERSION` untouched at 9. None of it ever crossed the dev-bench wire (decision 17 said so from the start, and it held), so dev-bench needed no reflash and its C decoder no change — only three stale comments. **This is the second bump to move the host constant alone, and the cleanest evidence yet for decision 12's split**: under the old single constant, deleting a type dev-bench cannot observe would have charged a firmware reflash. A removal is exactly as breaking as an addition on the api↔Core hop, which is why it bumps at all.

**Not "deferred", and not left as a stub.** The alternative on the table was to keep the types and stop growing them. Declined: a subsystem that is fully typed, partly implemented, wired into two repos' call sites, and has never run is worse than no subsystem — it reads as a feature to everyone who meets it, and it was already misleading readers. `embarch-api`'s own MCP tool description advertised `validations` in the study schema to every agent that ever called `run_study`. If post-hoc checks are wanted when real captured data exists to check, they should be designed against that data.

Done **on a branch**, unlike the rest of that pass, at the repo owner's explicit direction — [embarch-dev-workflow.md](../embarch-dev-workflow.md) §6's standing carve-out for real, risky or exploratory work, not an exception to the no-branches rule.

### 54 — `StepResult.gatt_activity` retired outright — the capture is the file, and it was never the field

The repo owner's call, raised as "can we get free of the 32 cap?" while designing decisions 52/53: `MAX_GATT_ACTIVITY_RECORDS` was 32 records per step, and even a characteristic that notifies rarely exceeds that in a study of any length.

**The answer is that the cap should not be raised, because the field should not exist.** It held a bounded, in-memory copy of something unbounded and streamed: the tap pipeline (decision 39) already writes every record incrementally to a file as it arrives. Keeping the capped copy alongside it meant a study could *look* like it had captured everything while holding 32 of several thousand records — the "nothing captured, no error" family of failure this suite has now been opened by from four directions (decisions 34, 36, 53, and this one). `GattActivityRecord`, `MAX_GATT_ACTIVITY_RECORDS`, and the whole `ble_gatt_activity_record` path in dev-bench went with it.

**What replaces it is not nothing.** Every study with a monitor step now gets a `GattTranscript` tap declared for it automatically ([embarch-ui/design.md](../embarch-ui/design.md) decision 15) — uncapped, both directions, written to `streams/gatt.csv` as it arrives. Before that pass the Study Designer authored no GATT tap at all, so `gatt_activity`'s first 32 records were genuinely the only inline record a UI-authored study produced; retiring the field without that half would have removed the answer along with the wrong one.

**[Measured, not asserted]:** dev-bench's `sram0_0_seg` on the ESP32-C5 goes **90.87% → 81.12%** — about 37 KB — on a board whose SRAM had already overflowed twice in this suite's history. `DBM_MAX_RAW_LEN` shrinks with it, and `StudyStart` becomes that firmware's largest message again for the first time since v4.

Wire v13 → v14, host v15 → v16. The removal is mid-struct in a message dev-bench hand-encodes, which is what makes this unambiguously a wire bump: an encoder that kept writing even the `None` byte would put `security_level` one byte late and Core would read the activity byte as a security level. Both `StepResult` vectors are re-pinned one COBS code byte shorter, and the populated-`security_level` one is where that shows up as a wrong *value* rather than only a wrong length — the same class of drift the retired `power_samples_ref`/`waveform_ref` bytes caused for a whole schema version before v9 caught them.

### 19 — Two-tier validation: real-time `Outcome` plus a Core-side post-hoc content check

**Retired 2026-08-25** (decision 48). The post-hoc half — `Study.validations`, `PostHocValidation`/`PostHocCheck`/`ValidationSource`/`DataChannel`/`ContentValidity`/`ValidationResult`, and the `core-validation` feature that evaluated them — is gone.

Two things it established that outlived it: **the real-time half stands** and is what dev-bench reports per step (`Outcome`, §4.5) and what `continue_on_fail` gates; and **`validations` never crossed the dev-bench wire**, which decision 17 asserted from the start, which held, and which is what let decision 48's removal cost a host bump and no reflash. Its own late amendment — a stream-fed check names the *tap*, not a `DataChannel`, because a capture belongs to a tap whose scope may outlive any step — was the **first change decision 12's constant split actually spared dev-bench**, and the concrete argument for having made that split.

One rule from its implementation survives it and now lives in decision 18: **naming a tap the study doesn't declare is a `POST /study` pre-flight failure**. Nothing in the type system stops an author naming a tap that isn't there, and the failure it would otherwise produce is a check that silently never runs.

### 28 — Opt-in post-hoc validation over an aborted study's completed steps

**Retired 2026-08-25** with post-hoc validation itself (decision 48). It proposed `Study.validate_on_abort: bool`, defaulting to `false`, so a fuzzer could learn whether data a step *did* capture before a later step aborted the study was itself valid.

Kept as a tombstone because it is **evidence for decision 48 rather than a loss to it**: this refinement was designed, recorded, and the field was **never actually added to `Study`** — so it spent months as a decision describing behavior no code had. That is the failure mode decision 48 names when it declines to leave a subsystem "deferred" rather than removed.
