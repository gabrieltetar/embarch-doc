# embarch-study-designer: milestone 3 — Study Designer

**Status:** draft, 2026-07-27. Execution plan for [embarch-roadmap.md](../embarch-roadmap.md)'s Milestone 3. Unlike milestones 1–2 ([embarch-core/milestone-2.md](../embarch-core/milestone-2.md), [embarch-api/milestone-2.md](../embarch-api/milestone-2.md)), this milestone is **design-only** — `embarch-dev-bench` doesn't physically exist yet, so there's no hardware to validate against. See [design.md](design.md) for the durable architecture record this plan resolves questions into.

## 1. Goal, restated

Get `embarch-study-designer`'s design (`design.md`) to a state with no major unresolved unknowns, so a future code-executing milestone can start implementation directly — a shared, `no_std` Rust crate defining the data types for BLE-interaction-plus-power-profiling studies, compiled independently by `embarch-core`, `embarch-api`, and dev-bench firmware.

## 2. Scope for this milestone

- **Design and documentation only.** No code for `embarch-study-designer`, `embarch-dev-bench`, or any change to `embarch-core`/`embarch-api`'s actual source. An empty repo was created for `embarch-study-designer` mid-milestone ([gabrieltetar/embarch-study-designer](https://github.com/gabrieltetar/embarch-study-designer), `design.md` §3 decision 8) to resolve where it lives — it stays empty (no code pushed) for the remainder of this milestone.
- **Board/DUT:** none specifically — this milestone is architecture, not board-specific validation.
- Out of scope: the physical `embarch-dev-bench` design itself (BLE radio choice, power-sampling hardware, form factor) — that stays a separate, later effort (`design.md` §7).

## 3. Steps

### 3.1 Nail down the concrete `Study`/`Step`/`Action` data model — resolved

Resolved `design.md` §4 from conceptual categories into field-level `Study`/`Step`/`Action`/`PowerSampleWindow`/`StudyResult`/`StepResult` types. Fuzzing's parameter-variation use case is explicitly *not* a type-level construct — a fuzzer generates many concrete `Study` values externally and submits each one, keeping the wire types simple.

### 3.2 Decide dev-bench firmware's runtime/language — resolved

Resolved `design.md` §7's biggest open question: **C**, with `embarch-study-designer` linked in via a cross-compiled `no_std` FFI staticlib (`cbindgen`-generated header), not native embedded Rust or a Zephyr+Rust module (`design.md` §3 decision 7). Driven by the nRF54 family splitting on Rust viability (nRF54L15 plausible via `zephyr-lang-rust`, nRF54H20's multi-core `sysbuild` build unproven for it) and Zephyr's BLE host staying a C API either way. "Each component compiles it in" (§3 decision 1) is now: literal Cargo dependency for `embarch-core`/`embarch-api`, FFI staticlib for dev-bench firmware.

### 3.3 Decide (or spike) the Core↔dev-bench binary wire format — resolved

Resolved: **`postcard` locked in** (`design.md` §3 decision 3), framed with **COBS** and versioned via an append-only top-level enum rather than a manual version byte (§3 decision 10) — postcard has neither framing nor a self-describing schema on its own, so both gaps needed an explicit answer. Locked without a real-hardware spike (dev-bench doesn't exist yet); flagged for re-confirmation once real nRF54 hardware exists, same posture as §3.2.

### 3.4 Decide Core's new endpoint surface/naming — resolved

Resolved: async, job-based (`design.md` §3 decision 9) rather than a single blocking call — `POST /study` returns a `study_id` immediately, `GET /study/{id}` polls status/result, `GET /study/{id}/power-data` streams the power-sample CSV as bytes (not a local path, avoiding `/flash`'s artifact-transfer-gap class of bug). Full shape in `design.md` §5.1. `embarch-core/design.md` §4/§2/§8 updated to match, ahead of implementation.

### 3.5 Decide study-result/telemetry storage — resolved

Resolved: splits by data shape rather than one combined file or a database (`design.md` §3 decision 11) — a small `events.json` (per-step pass/fail, captured BLE data) plus a separate `data.csv` (power time-series), under `study_results/<study_id>/` on Core's local disk. Full layout in `design.md` §5.2.

### 3.6 Decide build/compile-integration mechanics — partially resolved

Repo layout resolved: a standalone sibling repo, [gabrieltetar/embarch-study-designer](https://github.com/gabrieltetar/embarch-study-designer) (created empty), consumed via a git dependency (`design.md` §3 decision 8). **Still open** and carried forward (`design.md` §7): the nRF54 cross-compilation target triple/toolchain/linker setup for the `no_std` FFI staticlib, and how `cbindgen` header generation plus the staticlib build get wired into dev-bench firmware's Zephyr/CMake build — both blocked on real dev-bench hardware existing to validate against, unlike the other items above.

### 3.7 Decide the crate's own allocation model and resource bounds — resolved

A design review pass surfaced a gap §3.1's field-level types didn't actually close: `Study.steps: Vec<Step>`, `Step.name: String`, `GattOperation::Write { payload: Vec<u8> }`, and similar fields all require a global heap allocator (`extern crate alloc`) wherever this crate is linked — something dev-bench firmware (bare-metal C, §3.2) isn't guaranteed to provide, even though decisions 3/5 already committed the *encoding* (postcard) and the crate itself to `no_std`/no-allocator. Resolved: every such field switches to fixed-capacity `heapless::Vec<T, N>`/`heapless::String<N>` (`design.md` §3 decision 15), closing the allocator question end to end rather than just at the encoding layer, and forcing concrete max-size constants (a new `limits` module — max steps per study, max name/payload lengths, etc.) onto fields that were previously unbounded. Those constants double as an explicit ceiling for the fuzz-testing use case (§1) to generate within. Placeholder-but-concrete, same posture as §3.3's postcard lock-in: chosen without real dev-bench hardware to size against, flagged for re-confirmation once real nRF54 memory constraints are known.

### 3.8 Resolve embarch-api's tool/subcommand naming — resolved

§3.7 of the previous fold-back step (renumbered §3.9 below) had left this open: `design.md` §6 named `run_study`/`study_status` only as illustrative examples of the two-call shape async execution implies, not as locked names. Resolved: those two names are now the final MCP tool/CLI subcommand surface (`design.md` §6, new table) — `run_study` takes a `study` param (MCP) or `--study-file <path>` (CLI, since `Study`'s nesting rules out per-field flags), with no `project` param since a study isn't tied to one of `embarch-api`'s configured projects; `study_status` takes `study_id`. Also decided: no `build_and_flash`-style blocking "wait until done" wrapper for v1, matching the suite's minimal-viable posture. A tool name for Core's `GET /study/{id}/power-data` remains unresolved — small enough to leave for whichever milestone implements this surface in code, rather than blocking this closure on it.

### 3.9 Fold resolved decisions back into `design.md` — done

`design.md`'s body was edited directly as each of §3.1–3.8 resolved (§4, §5, §6, §3 decisions 9–11, 15, §7), with dated §8 changelog bullets. `embarch-core/design.md` was also updated (§4.1/§2 architecture diagram, §8 module layout, §11 changelog) since §3.4's endpoint surface is now concrete enough to record there, per `design.md` §5. `embarch-api/design.md` is now updated too (§5, §5a, §13 changelog), per §3.8's resolution.

### 3.10 Mid-study disconnect/Core-crash recovery and wire-integrity — resolved

A fourth design review pass (`design.md` §8, 2026-07-29) surfaced two gaps that survived §3.1–3.9 untouched: nothing said what happens to a study or a connection if Core itself dies mid-run, and neither COBS framing nor postcard nor plain HTTP/JSON actually detect payload corruption (only COBS's resync, which isn't the same thing). Resolved: a Core crash/restart mid-study is treated as an unrecoverable, catastrophic failure for that specific study (in-memory job registry lost, no `StudyResult` written, a later poll 404s) — but the *connection* itself recovers, since `Hello` now doubles as a hard reset (`design.md` §3 decision 12, amended): dev-bench unconditionally aborts whatever it's running on any `Hello`, rather than Core waiting out dev-bench's own step timeouts (new §3 decision 16). Separately, a `steps_crc: u32` CRC-32 seal on `Study.steps` — computed once by whoever submits a `Study`, checked independently at both the API↔Core hop and the Core↔dev-bench hop — closes the corruption-detection gap (new §3 decision 17).

### 3.11 Core as pre-flight validator — resolved

Previously nothing validated a submitted `Study`'s structural well-formedness before relaying it to dev-bench — an out-of-range cross-reference or an over-capacity field would only surface as whatever dev-bench's bare-metal C, or a raw `serde` error, happened to do with it. Resolved: Core checks every `limits`-module capacity and every `Study.validations` `step_index` bound before generating a `study_id` or touching the serial link, rejecting with a `400` naming the offending field rather than a raw deserialize error — material given `--study-file` (`design.md` §6) means a human is often hand-writing the JSON directly (new §3 decision 18).

### 3.12 Two-tier validation model, replacing `Action::Validate` — resolved

The original `Validate` `Action` (`design.md` §4.3) conflated two different questions into one on-device mechanism: "did this step's action mechanically succeed" and "was the data it captured actually correct." Resolved by splitting them: the existing device-observed `Outcome` (real-time, gates `continue_on_fail`) stays as the first; a new, Core-only, post-hoc mechanism — `Study.validations`/`StudyResult.validations` (`PostHocValidation`, `ValidationSource`, `PostHocCheck`, `SignalCheck`, `ContentValidity`, `ValidationResult`, new `design.md` §4.6) — answers the second, evaluated only if/when a study reaches `"completed"` status. `Action::Validate` itself is removed (new §3 decision 22); `ValidationSource`'s step-index correlation (§3 decision 14) is rewritten to drop its earlier-index-only ordering constraint, since post-hoc evaluation only ever happens after the whole study has finished. `PostHocCheck` covers both simple byte-level checks (`ExpectedValue`, unchanged in shape) and a new, richer `SignalCheck` enum for power/sensor-waveform data that byte equality can't express — its actual evaluation logic lives behind a new `core-validation` Cargo feature that only Core's build enables, keeping dev-bench firmware and `embarch-api` free of the `std`/`alloc`/floating-point/FFT dependencies that logic needs (new §3 decision 19).

### 3.13 Dev-bench→Core streaming mechanism for power/sensor-waveform data — resolved

Power sampling was previously modeled as a single bulk transfer once a `PowerSampleWindow` closed; there was no mechanism at all for a continuous sensor-waveform capture (e.g. PPG). Resolved: a new streaming sub-protocol (`StreamStart`/`StreamChunk`/`StreamEnd` `DevBenchMessage` variants, channel-tagged via `StreamChannel::Power`/`SensorWaveform` to allow concurrent streams per step) delivers both kinds of continuous data (new §3 decision 20); sensor-waveform capture itself is a new `GattOperation::StreamCapture` variant, bound implicitly by the step's own `timeout_ms` like `PowerSampleWindow` already is, rather than a parallel step-level field (new §3 decision 21). Core writes both `data.csv` and a new `waveform.csv` incrementally as chunks arrive rather than buffering until the study ends, so raw capture data can survive even the crash scenario in §3.10. A new `GET /study/{id}/waveform-data` endpoint mirrors `/power-data` (`design.md` §5.1).

### 3.14 Fold resolved decisions back into `design.md` (second round) — done

`design.md`'s body was edited directly as each of §3.10–3.13 resolved (§2, §3 decisions 12–22, §4.2/§4.3/§4.5/new §4.6, §5.1, §5.2, §6, §7), with a dated §8 changelog bullet (2026-07-29).

## 4. Definition of done

- `design.md` §7 has no open item left for: dev-bench firmware runtime/language, the Core↔dev-bench binary format, Core's new endpoint surface, study-result storage, or the Cargo-dependency repo-layout half of build/compile-integration mechanics. **Met**, except the cross-compilation-toolchain/`cbindgen`-build-wiring half of build/compile-integration mechanics, which stays open pending real dev-bench hardware (§3.6) — carried into a future milestone rather than blocking this one, since it's validation-gated the same way the wire-format/firmware-language decisions already accepted being.
- `design.md` §4 has real field-level type definitions, not just conceptual categories, and those types don't silently assume a heap allocator dev-bench firmware may not have. **Met** (§3.1, §3.7).
- `embarch-api`'s future tool/subcommand names and param shapes for running a study are locked in, not left as illustrative placeholders. **Met** (§3.8).
- A future milestone could plausibly start writing `embarch-study-designer`'s actual `Cargo.toml`/`lib.rs` directly from `design.md`, without first needing another round of architecture decisions. **Met** for the crate's own types; the FFI staticlib's *build* still needs the toolchain/wiring decision above before dev-bench firmware's side of that can start.
- The design accounts for what happens when Core itself fails mid-study (not just dev-bench/the DUT), detects wire corruption beyond COBS's resync, pre-validates a submitted `Study`'s structure, and models both "did the action succeed" and "was the data correct" as distinct mechanisms rather than one overloaded `Validate` step. **Met** (§3.10–§3.13).

## 5. Open questions / risks carried into execution

- **The nRF54 cross-compilation toolchain and `cbindgen`/Zephyr-CMake build wiring (§3.6)** remains open, blocked on real dev-bench hardware — the one item this milestone didn't close.
- The physical `embarch-dev-bench` hardware doesn't exist, so every "resolved" decision validated only against a stand-in target rather than the real bench (§3.2's C/FFI-staticlib call, §3.3's postcard/COBS lock-in, §3.7's `heapless` size constants, §3.13's stream-chunk sizing, and §3.6's still-open toolchain question) should be treated as re-confirm-once-real-hardware-exists, not unquestionable just because it's in `design.md`.
- `data.csv`/`waveform.csv`'s (§3.5, §3.13) exact column schemas depend on dev-bench's eventual power-sampling and sensor hardware — placeholder-level until `embarch-dev-bench/design.md` stops being a placeholder.
- A tool/subcommand name for Core's `GET /study/{id}/power-data` (§3.8) remains unresolved — small enough to leave for whichever milestone implements `embarch-api`'s side of this surface in code; the new `GET /study/{id}/waveform-data` (§3.13) carries the same open item.
- `SignalCheck`'s real variant set and the DSP/statistics implementation behind Core's `core-validation` feature (§3.12), and the exact CRC crate for §3.10's `steps_crc`, are both placeholder-but-concrete — small, not blocked on hardware, just not yet chosen.

## 6. Changelog

- 2026-07-27 — Initial draft, scoping Milestone 3 as design-only work to close `design.md`'s open questions.
- 2026-07-27 — Closed §3.2 (dev-bench firmware runtime/language): C firmware, `embarch-study-designer` linked via FFI staticlib. Folded into `design.md` §3 decision 7 and §8's changelog; updated §5's risk register accordingly.
- 2026-07-28 — Added §3.6 (build/compile-integration mechanics) as a new step, surfaced from a gap in `design.md` §3 decisions 1/7 that didn't cover repo layout, cross-compilation toolchain, or `cbindgen`/build-system wiring. Renumbered the fold-back step to §3.7 and updated §4/§5 references accordingly.
- 2026-07-28 — Closed §3.1, §3.3, §3.4, §3.5, and the repo-layout half of §3.6: concrete `Study`/`Step`/`Action` types (§3.1); postcard locked in with COBS framing/append-only-enum versioning, no real-hardware spike (§3.3); async job-based `/study` endpoint surface (§3.4); `events.json`+`data.csv` result storage (§3.5); standalone sibling repo created at [gabrieltetar/embarch-study-designer](https://github.com/gabrieltetar/embarch-study-designer) (§3.6). Folded all of it into `design.md` (§4, §5, §3 decisions 9–11, §7, §8) and into `embarch-core/design.md` (§2, §4, §8, §11) per §3.7. Updated §2's scope note (repo now exists, stays empty), §4's definition of done, and §5's risk register: only the nRF54 cross-compilation toolchain / `cbindgen`-build-wiring half of §3.6 remains open, blocked on real dev-bench hardware.
- 2026-07-28 — Added and closed two new steps found during a further design review pass: §3.7 (the crate's own allocation model) — switched every §4 field from `alloc`-based `Vec`/`String` to fixed-capacity `heapless` collections plus a new `limits` module of max-size constants (`design.md` §3 decision 15), since decisions 3/5's `no_std`/no-allocator framing hadn't previously covered the crate's own types, only postcard's encoding. §3.8 (`embarch-api` tool/subcommand naming) — locked in `run_study`/`study_status` as final names/param shapes (`design.md` §6), previously only illustrative; decided against a `build_and_flash`-style blocking wrapper for v1. Renumbered the fold-back step from §3.7 to §3.9 and folded both new resolutions into `design.md` (§4, §6, §3 decision 15, §8) and `embarch-api/design.md` (§5, §5a, §13). Updated §4's definition of done and §5's risk register accordingly.
- 2026-07-29 — Added and closed four more steps from a fourth `design.md` review pass, none blocked on real hardware: §3.10 (mid-study Core-crash recovery + a CRC-sealed integrity check on `Study.steps`, new §3 decisions 16/17), §3.11 (Core as pre-flight structural validator, new §3 decision 18), §3.12 (two-tier validation model replacing `Action::Validate` — device-observed `Outcome` vs. a new Core-only, post-hoc `Study.validations` mechanism with a `core-validation` Cargo feature gating the actual signal-processing code, new §3 decision 19, rewritten §3 decision 14, `Action::Validate` removed per new §3 decision 22), and §3.13 (a dev-bench→Core streaming sub-protocol for power/sensor-waveform data plus a new `GattOperation::StreamCapture` variant, new §3 decisions 20/21). Added §3.14 as the new fold-back step (mirroring §3.9) and folded all four resolutions into `design.md` (§2, §3 decisions 12–22, §4.2/§4.3/§4.5, new §4.6, §5.1, §5.2, §6, §7, §8). Updated §4's definition of done and §5's risk register accordingly.
