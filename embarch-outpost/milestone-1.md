# embarch-outpost: milestone-1 (roadmap Milestone 7 — MCU Load Tracing)

**Status: Phase A CLOSED 2026-08-25; B–E not started.** Execution plan for [embarch-roadmap.md](../embarch-roadmap.md) Milestone 7. Every decision this implements is already settled — see [design.md](design.md) and the companion decisions listed per phase.

## 1. Why this is phased, and why the phases are ordered this way

Milestone 7 spans seven repos, which is too much for one pass. The ordering is not preference — it is a real dependency chain plus one deliberate exception:

- **Phase A must be first.** `embarch-study-designer`'s types are compiled into `embarch-core`, `embarch-api`, `embarch-ui`, *and* dev-bench firmware. Nothing else can be built against a schema that hasn't landed.
- **Phase C (the outpost module itself) is deliberately out of that chain.** It emits bytes down a UART and depends on nothing in this suite — it can be written and built in parallel with A/B by a separate thread. It is also the only phase whose *validation* needs hardware that does not exist yet (§5).
- **Phase E is last and needs a physical bench**, including a USB-UART bridge nobody has bought yet.

**The timing risk below did not decay: Phase A landed while Milestone 6's firmware was still unflashed**, so decisions 29 and 39 stayed a reshape rather than becoming a migration. Nothing about the ordering below changes; the note is kept because it is still live for Phase B, which is where the reshape actually reaches dev-bench's behavior.

**One timing risk, stated up front because it decays.** [embarch-dev-bench/design.md](../embarch-dev-bench/design.md) §3 decision 29 and [embarch-study-designer/design.md](../embarch-study-designer/design.md) §3 decision 39 reverse wire shapes that are **code-complete and deployed but never flashed or run** (roadmap Milestone 6). That is precisely what made the reversal cheap. If Milestone 6's dev-bench firmware gets flashed and validated before Phase A/B land, the reshape stops being free and becomes a migration. Sequence accordingly, or accept the cost knowingly.

## 2. Phase A — shared types (no hardware, pure Rust) — **CLOSED 2026-08-25**

**Repos:** `embarch-study-designer`, `embarch-topology` (plus the wire-contract half of `embarch-dev-bench`, which the definition of done below requires and §3 does not cover).

1. ~~**Stream taps**~~ — done. [embarch-study-designer/design.md](../embarch-study-designer/design.md) §3 decision 39, §4.8, implemented as `src/streams.rs`. `Study.streams`; `StreamSource`; `StreamEncoding` plus a `SampleLayout` the decision named but did not define (element width/type/byte order only — no scaling, which would be inventing meaning); `StreamScope` (`Steps` inclusive at both ends); `StreamOpen`/`StreamChunkBatch { id, records }`/`StreamClose { id, dropped }`; `StudyResult.streams: Vec<StreamRef>`. Also `validate_taps` and `samples_in`, so Core holds no copy of the tap rules or the sample layout.
2. ~~**Retire what it replaces**~~ — done, all of it: `StreamChannel`, `StreamChunk` **and** the old `Sample`-carrying `StreamChunkBatch`, `DevBenchMessage::GattTranscriptRecord`, `GattOperation::StreamCapture`, `StepResult::power_samples_ref`/`waveform_ref`, plus the now-orphaned `limits::MAX_BATCH_SAMPLES`/`MAX_RESULT_REF_LEN`. Row shapes for `data.csv`/`waveform.csv`/`gatt.csv` are untouched, as required.
3. ~~**Version requirements**~~ — done. `Study.requires` (mandatory, no serde default, so omission fails to deserialize rather than defaulting to `any`; blank is a separate pre-flight failure); `StudyResult.provenance` with `VersionSource::{ReportedByDevBench, ReportedByOutpost, FlashedThisRun, Declared}`. A test asserts host-side-only structurally: two studies differing only in `requires` encode byte-identical `StudyStart`s.
4. ~~**Schema bump**~~ — done, one bump covering both decisions. **It is 7 → 8, not the 5 → 6 both decisions were written against**: decisions 42 and 43 were implemented first and took v6 and v7 in between. Substance unchanged, arithmetic stale; recorded in decision 39 rather than silently corrected.
5. ~~**`SignalLink`**~~ — done. [embarch-topology/design.md](../embarch-topology/design.md) §3 decision 18, implemented as `src/hardware/signal.rs`, stored as a `[[signals]]` table in the existing `enrollment.toml`. Resolution reuses decision 17's `Filter`/`select` via a new `Filter::for_declared_serial` + `no_vid_gate` (off by default, so dev-bench's own path is unchanged); `validate_signal` confirms a `Direct` route's port is enumerable and returns a downcastable `SignalMismatch` when it doesn't.

**Definition of done — met.** `cargo build`/`test`/`clippy --all-targets -- -D warnings` clean in both crates and in all four consumers (`embarch-core`, `embarch-api`, `embarch-ui`, `embarch-umbrella`), across `embarch-study-designer`'s whole feature matrix and its `thumbv8m.main-none-eabi` staticlib cross-compile, and at `embarch-topology`'s default/`hardware`/`bin` feature sets. Every new wire record pinned **in both languages**: literal COBS frames in `embarch-dev-bench`'s ztest suite (28/28 pass on `native_sim`) against identical pre-COBS bodies in the Rust crate.

**Three things Phase A settled that the decisions had left implicit**, all written up in [embarch-study-designer/design.md](../embarch-study-designer/design.md) §3 decision 39: `StudyStart` carries `streams` (appended after `steps_crc`, so dev-bench's C decoder sees a trailing byte rather than a reshuffle); `SampleLayout`'s variant set; and reuse of the retired stream trio's discriminants rather than leaving holes postcard cannot express.

**Four things deliberately left for later, each recorded where it belongs rather than here:**

- `steps_crc` still seals `steps` alone, so taps ride outside the integrity seal — `embarch-study-designer/design.md` §7.
- `Step.power_sample` now overlaps a `PowerFrontEnd` tap; not resolved by implementation order — same §7.
- No CLI or HTTP surface to declare a `SignalLink` from, and no durable `alerts.jsonl` record for a `SignalMismatch` — `embarch-topology/design.md` §5.
- `embarch-core` was adapted mechanically, not redesigned: it still writes the three fixed CSV paths (chosen from the tap's declared encoding/source) rather than `streams/`, and logs rather than discards a `Raw`/`Text`/`OutpostTrace` tap's bytes. `streams/` is Phase B.

## 3. Phase B — hosts

**Repos:** `embarch-core`, `embarch-api`, `embarch-dev-bench`.

1. **Core** — [embarch-core/design.md](../embarch-core/design.md) §3 decisions 30, 31. `streams/` under `study_results/<id>/` replacing the three fixed CSV paths; **raw bytes always written before any decode is attempted**; a `Signal` tap with a `Direct` route opens a third serial port (resolved via `embarch_topology`'s `SignalLink`, taking neither `hw_lock` nor `study_lock`); manifest storage bound by the study's own flash and verified by build ID; retention (`EMBARCH_STREAM_MAX_BYTES`, `EMBARCH_STUDY_RESULTS_KEEP`); `GET /study/{id}/stream/{name}` with the three old routes kept as aliases for one release; `POST /signals`; the `POST /study` version gate (dev-bench checked for real, `409` naming both strings, no step run).
2. **api** — [embarch-api/design.md](../embarch-api/design.md) §3 decisions 39, 40. Manifest pickup from the build and transport to Core; `study_stream_data`/`list_study_streams` with the three old tools as aliases; `run_study --reflash none|dev-bench|dut|both` (default `none`) and `--allow-version-mismatch` (recorded in the result, never silent). **`embarch-api` must never run `git checkout`** — reflash builds the tree as it stands and then verifies; a wrong tree fails naming both revisions.
3. **dev-bench** — [embarch-dev-bench/design.md](../embarch-dev-bench/design.md) §3 decision 29(a). Delete payload interpretation: the `f32` grouping loop, trailing-partial handling, `sample_interval_ms` derivation, `unit`/`channel_id` defaults. Forward `{ rx_utc_ms, bytes }`. Add the reserved `dev-bench` tap for its own `LogLine`. This phase is **net-negative firmware** — if it is getting bigger, something has been misread.

**Definition of done:** all three build/test/lint clean, including a native Windows build of Core (this suite's real deployment target). Not deployed to the live service in this phase.

## 4. Phase C — the outpost module (parallelisable with A/B)

**Repo:** `embarch-outpost` (empty; clone as a sibling of `embarch-doc`).

Everything here is [design.md](design.md) §3 decisions 1–9 and §5. Build order that keeps it testable throughout:

1. `zephyr/module.yml`, `CMakeLists.txt`, `Kconfig` — the full symbol table in §5.3.
2. Record ring + drain thread + `uart_tx()` on `DT_CHOSEN(embarch_outpost_uart)`. Overflow = drop, count, **emit a gap record** (Zephyr counts drops but never puts them on the wire — that gap is ours to close).
3. `TRACING_USER` hooks: thread switch in/out, ISR enter/exit, idle, thread create/name-set. ISR identity via `__get_IPSR() - 16` behind `EMBARCH_OUTPOST_ISR_IDENTIFY`, emitted on **both** enter and exit.
4. `OUTPOST_EVT` + the marker registration list; an unregistered ID must be a **build error**.
5. Records: `{ cycles: u32 (absolute), kind: u8, a: u32, b: u32 }`; postcard + COBS on drain; periodic header record carrying build ID, `sys_clock_hw_cycles_per_sec()` **read at runtime** (the Kconfig is legitimately 0 on some targets), record-layout version.
6. **Manifest generator** — post-link CMake step emitting `outpost-manifest.json`: marker IDs, `_k_thread_obj_*` → names, `_sw_isr_table[]` index → handler names, cycle rate, build ID.

**Definition of done:** builds for `native_sim` and for the reference-dut's real board; a `native_sim` run produces a decodable stream; the manifest generator resolves real thread and ISR names out of a real ELF. Overhead measured — a build with the outpost compiled out vs. in, same study — since a trace that changes the timing it reports is the failure mode this whole design is arranged around.

## 5. Phase D — UI, and Phase E — hardware bring-up

**D** ([embarch-ui/design.md](../embarch-ui/design.md) §3 decisions 10, 11): signal-route rows in the Topology tab with the diagram drawing a `Direct` signal **around** the dev-bench node; the post-hoc Trace view (gaps drawn as gaps; a build-ID mismatch **not rendered at all**); `requires` fields prefilled from live bench state; reflash in the run dialog; `Declared` provenance rendered visibly weaker than verified.

**E** needs hardware that does not exist yet: a USB-UART bridge (which will be the **third** VID-matching serial device on this bench — [embarch-topology/design.md](../embarch-topology/design.md) §3 decision 17's ambiguity, one candidate louder), a chosen UART/pin on the reference-dut board, and a wire. First real capture is what sizes every Kconfig default in §5.3, none of which is measured.

## 6. Definition of done (milestone)

- [x] Phase A: schema **8** lands (not 6 — see §2), all consumers green, wire records pinned in both languages — **closed 2026-08-25**
- [ ] Phase B: Core/api/dev-bench green; dev-bench firmware is net smaller
- [ ] Phase C: outpost builds for real hardware; manifest resolves real thread + ISR names; overhead measured
- [ ] Phase D: routing declarable in the UI; a trace renders with honest gaps
- [ ] Phase E: a real study captures a real trace from the real reference-dut DUT over the bypass route
- [ ] `embarch-doc` updated per [DOC-PROTOCOL.md](../DOC-PROTOCOL.md) §4/§5 as each phase closes — including the pre-close staleness grep
