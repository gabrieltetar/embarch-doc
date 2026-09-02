# embarch-study-designer: milestone 9 — Study Designer: Feature-Branch Iteration

**Status:** done, 2026-08-20 (this crate's own half — see §6). Execution plan for [embarch-roadmap.md](../embarch-roadmap.md)'s Milestone 3 ("Study Designer: Feature-Branch Iteration" — filed on disk as `milestone-9`, continuing past Milestone 2's `milestone-8` set). Companion to [embarch-dev-bench/milestone-9.md](../embarch-dev-bench/milestone-9.md) (dispatching the new `Action`s on real firmware), [embarch-core/milestone-9.md](../embarch-core/milestone-9.md) (concurrent DUT-flash + dev-bench-study validation), and [embarch-api/milestone-9.md](../embarch-api/milestone-9.md) (driving the whole chain against the real reference-dut DUT). See [design.md](design.md) §3 decisions 31/32/33 for the durable decisions this doc closes out.

## 1. Goal, restated

`design.md` §3 decisions 31 (`Action::GattDiscover`), 32 (`Action::GattMonitorAll`), and 33 (the GATT-config extraction tool) are all design-only as of the design-questions pass that opened this milestone — no code exists yet. This milestone is what actually writes it: the two new `Action` variants and their `StepResult` fields (`gatt_services`/`gatt_activity`, §4.3a/§4.5), the schema-version bump (3 → 4), and the `GattConfigExtractor` trait plus its one concrete `ZephyrBleDefExtractor` implementation — the crate's own half of Milestone 3, ahead of `embarch-dev-bench` ever dispatching either new `Action` for real.

## 2. Scope for this milestone

- **New types, no removal.** `GattCharacteristicInfo`/`GattServiceInfo`/`GattActivityRecord` (§4.3a) are additive; `Action` grows two variants; `StepResult` grows two fields. Every existing `Action`/`StepResult` consumer (dev-bench's `BleAdvertise` dispatch, Core's `events.json` writer) is unaffected by construction — `serde`'s default handling of new optional fields and new enum variants means old data still deserializes, matching this crate's existing append-only discipline (§3 decision 10).
- **`GattConfigExtractor` is a `std`-only tool, not `no_std` core.** Lives in a new `tools/` directory, built as a separate Cargo binary target behind a new `gatt-extract` feature — never linked by dev-bench firmware or gated behind `#![no_std]`, since it runs on whatever machine authors a `Study`, not on the MCU.
- **`ZephyrBleDefExtractor` targets exactly one firmware's real source layout** (`reference-dut-fw`'s `lib/ble/ble_def.h`/`lib/ble/ble.c`), confirmed against the checked-out repo, not guessed against a generic Zephyr BLE peripheral convention. A second firmware's own extractor is out of scope — the trait exists so that's additive later, not a redesign.
- **Out of scope:** extending the FFI decode surface (`essd_study_decode_full`) to cover the two new `Action`s, or `BleConnect`/`DataExchange` — that's `embarch-dev-bench/milestone-9.md`'s job, consuming whatever this doc produces. Any actual GATT discovery/subscription logic against a real BLE stack — that's `ble_bridge_real.c`, also `embarch-dev-bench`'s job.

## 3. Steps

### 3.1 Implement `GattCharacteristicInfo`/`GattServiceInfo`/`GattActivityRecord` and the new `limits` constants

`MAX_DISCOVERED_SERVICES = 8`, `MAX_CHARS_PER_SERVICE = 16`, `MAX_GATT_ACTIVITY_RECORDS = 32` (§3 decision 15's update). `properties: u8` carried raw, not a bitflags newtype (decision 31's own rationale) — a plain field, no new dependency.

### 3.2 Add `Action::GattDiscover` and `Action::GattMonitorAll`, and the matching `StepResult` fields

Both variants are field-less (§4.3) — all of their behavior lives on the dev-bench side; this crate's job is just the wire shape. `StepResult` gains `gatt_services: Option<Vec<GattServiceInfo, MAX_DISCOVERED_SERVICES>>` and `gatt_activity: Option<Vec<GattActivityRecord, MAX_GATT_ACTIVITY_RECORDS>>` (§4.5). Bump `STUDY_DESIGNER_SCHEMA_VERSION` 3 → 4 (§3 decision 32).

### 3.3 Add `DataChannel::GattActivity`

Additive, for future `PostHocValidation` authoring against `gatt_activity` (§4.6) — not consumed by any check this milestone writes, per the DoD decided in this milestone's design pass (data landing in storage, not a content assertion).

### 3.4 Round-trip tests: encode/decode every new type and variant through postcard, matching this crate's existing `serde` test discipline

Confirm `GattServiceInfo`/`GattActivityRecord` round-trip through both postcard (the Core↔dev-bench wire format) and `serde_json` (the `embarch-api`/`events.json` path, §3 decision 3's format-agnostic stance) — same coverage pattern as every prior wire-shape addition to this crate (decisions 24/25/27's own implementation passes).

### 3.5 Define the `GattConfigExtractor` trait

`fn extract(&self, repo_root: &Path) -> Result<heapless::Vec<GattServiceInfo, {limits::MAX_DISCOVERED_SERVICES}>, ExtractError>` — `ExtractError` names the specific failure (file not found, macro not found, unparseable properties expression) rather than a raw I/O error, matching this crate's existing "name the specific failure" discipline (§3 decisions 18/23).

### 3.6 Implement `ZephyrBleDefExtractor`

Text-scan (not a full C parser) `lib/ble/ble_def.h` for `#define ..._UUID_VAL \ BT_UUID_128_ENCODE(...)` macros, resolving each to a 128-bit UUID; text-scan `lib/ble/ble.c` for `BT_GATT_SERVICE_DEFINE(...)` blocks, matching each `BT_GATT_PRIMARY_SERVICE(&x)`/`BT_GATT_CHARACTERISTIC(&x, PROPS, ...)` call back to the macro that defined `x`'s UUID, and parsing `PROPS` (a `BT_GATT_CHRC_READ | BT_GATT_CHRC_NOTIFY | ...`-shaped expression) into the raw properties byte (§3 decision 31). Confirm against the real, current `reference-dut-fw` checkout — real service/characteristic UUIDs and properties, not a synthetic fixture — since the whole point is a tool a Study author can actually run.

### 3.7 CLI wrapper for the extraction tool

A minimal binary (`cargo run --features gatt-extract --bin extract-gatt-config -- --repo <path>`) emitting the extracted `Vec<GattServiceInfo>` as JSON to stdout — the authoring-time convenience this decision exists to provide.

### 3.8 Fold resolved decisions back into `design.md`

Per `DOC-PROTOCOL.md` §5: update decisions 31/32/33's status from "not yet implemented" to real, once §3.1–3.7 land and pass `cargo test`/`clippy --all-features -D warnings`.

## 4. Definition of done

- [x] `GattCharacteristicInfo`/`GattServiceInfo`/`GattActivityRecord` implemented with the new `limits` constants (§3.1).
- [x] `Action::GattDiscover`/`Action::GattMonitorAll` and the matching `StepResult` fields implemented; `STUDY_DESIGNER_SCHEMA_VERSION` bumped to 4 (§3.2).
- [x] `DataChannel::GattActivity` added (§3.3).
- [x] Round-trip tests pass for every new type/variant, both postcard and `serde_json` (§3.4).
- [x] `GattConfigExtractor` trait defined (§3.5).
- [x] `ZephyrBleDefExtractor` implemented and confirmed against the real, current `reference-dut-fw` checkout — real UUIDs/properties extracted, spot-checked by hand against `ble_def.h`/`ble.c` (§3.6).
- [x] CLI wrapper runs and emits valid JSON (§3.7).
- [x] `cargo build`/`cargo test`/`cargo clippy --all-features --all-targets -D warnings` all clean.
- [x] `design.md` updated to reflect real implementation, not design-only, per `DOC-PROTOCOL.md` §5 (§3.8).

## 5. Open questions / risks carried into execution

- **`gatt_activity`'s worst-case `StepResult` size and dev-bench's static-vs-stack allocation** — this crate's own wire-shape work doesn't touch dev-bench's C allocation strategy at all; flagged here only because `design.md` §3 decision 32 calls it out as a risk `embarch-dev-bench/milestone-9.md` needs to address from the outset, not rediscover.
- **`ZephyrBleDefExtractor`'s text-scanning approach is inherently heuristic** — a macro renamed, reformatted across multiple lines in an unexpected way, or a properties expression using a symbol this scanner doesn't recognize could silently under-extract rather than error loudly. Worth a defensive posture in §3.6 (fail loudly on an unrecognized `BT_GATT_CHRC_*` token rather than silently treating it as zero properties) — an implementation-time call, not pre-decided here.
- **Whether `MAX_DISCOVERED_SERVICES = 8`/`MAX_CHARS_PER_SERVICE = 16` are actually sufficient** — sized against `reference-dut-fw` (**3 services, largest at 8 characteristics — corrected 2026-08-26 by `design.md` §3 decision 57**; this line said 2, because the extraction it was sized against had never opened `lib/bds/bds.c`) with headroom; not yet validated against what `GattDiscover` reports live once §3.6's extraction and `embarch-dev-bench/milestone-9.md`'s live discovery can be diffed against each other.
