# embarch-core decisions: Core's wire types

**Status:** active, 2026-11-27 (`tasks/core/194`, EMB-295). Index: [../decisions.md](../decisions.md). Modules: [../interfaces/modules.md](../interfaces/modules.md).

### 164 — What Core serves that a client also reads is defined once, in `crates/embarch-core-wire`

**The problem.** `embarch-core-client` re-declared five of Core's wire families by hand (`StudyEvent`, `HelloAckInfo`, `LoadAnswer`/`LoadSummary`/`LoadSubject`, `LEASE_GATED`), each with its own drift guard, one of which passed silently when this repo was absent.

**Chosen: a crate in this repo, `crates/embarch-core-wire`, a workspace member beside the root package.** The server owns its wire, as `embarch-desk`'s `embarch-user-unit` does (desk decision 94). *Rejected:* `embarch-topology`'s `wire` feature (it carries the bench's hardware facts, not a run's events); a `wire` feature of `embarch-core-client` that Core depends on (Core would build against a client's repo). A wire change is now one edit.

**What it may depend on: `serde`, `serde_json` and `embarch-study-designer`, and nothing else.** `serde` alone cannot hold: a `StudyEvent` carries the study-designer's own wire types (`StepResult`, `Sample`, `GattTranscriptEntry`, `HostStepResult`). `serde_json` is for `PromptPending`'s flatten only. No axum, tokio or hardware crate: it builds alone by `--manifest-path`.

**What lives there.** The five families, plus what `StudyEvent` names: `PendingPrompt`, `SwitchedOn`, `SessionPromptInfo` (with `SessionPhase`, `RunFieldInfo`) and `AnsweredBy`. Core re-exports each from its old module. **Stays in Core:** the prompt slot, the answer body, `outpost_load.rs`'s lane arithmetic, `is_gated`, `LEASE_OPEN` and every handler.

**Owned strings** for what was `&'static str` (`PromptResolved.answer`, `LoadSubject.kind`, `LoadSummary.unit`), so a client can deserialize; same bytes.

**The JSON is byte for byte what it was.** Each family has a test that parses a line captured from Core's serializer before the move and writes the same bytes back: all ten `StudyEvent` variants, `HelloAckInfo`, `LoadAnswer`, and `LEASE_GATED` in order. **`PromptPending` keeps its sorted keys:** its prompt goes through a `serde_json::Value` (renaming `kind` to `prompt_kind`, decision 151), and a `Value`'s keys are alphabetical, `observation` (a study-designer type) included; field order cannot reproduce that, so the crate keeps the round trip.

**An unknown `kind` is not a variant.** The type is strict. A client meeting a variant a newer Core added reports that frame unrecognized with its raw data, as `embarch-core-client`'s frame decoder already does (`StudyStreamItem::Unrecognized`). A `#[serde(other)]` variant would be one Core never sends and would drop the frame's data.

**What the client must keep (`tasks/api/226`):** its frame decoder, `render_hello_ack` and caller-side rendering, and any tolerance of an older Core: the mirrors made six stamps and four hello fields `Option`, the shared types require them, so an older Core's frame becomes `Unrecognized` (the task file lists them).

**Builds from outside are unchanged:** `cargo build --release` still writes `target/release/embarch-core`, the release workflow's version awk still reads `[package]` first, and `deploy-core`'s rsync copies `crates/`. **Not verified:** Windows native and a `cross` aarch64 build.

**Measured:** workspace `build`, `test` and `clippy -D warnings` green; the pins were captured from the pre-move binary, not written from the new types.
