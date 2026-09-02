# embarch-study-designer decisions: Things this crate deliberately does not have

**Status:** active, 2026-09-02.

Removals, and two tombstones.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 22 — `Action::Validate` is removed

Its job — checking a prior step's captured data against an expected value — moved to the Core-side post-hoc mechanism (decision 19), which was itself later removed outright (decision 48). Keeping both would have meant two overlapping validation systems. dev-bench firmware has had no validation-related code path since.

### 48 — Post-hoc validation is removed outright — the whole notion, not a field

`Study.validations`, `StudyResult.validations`, `PostHocValidation`, `PostHocCheck`, `ExpectedValue`, `SignalCheck`, `ValidationSource`, `DataChannel`, `ContentValidity`, `ValidationResult`, `signal.rs`'s evaluation logic and the `core-validation` Cargo feature are all gone. Decision 19's post-hoc half and decision 28 are retired with it; decision 19's real-time `Outcome` half is untouched and is what every study has always actually used.

**It was never once used.** That is the decision, and everything else is detail. `embarch-core`'s `events.json` writer wrote a hardcoded `"validations":[]` — not "empty because this run had none" but a literal string in the source, because Core never evaluated a validation in its life. Decision 28's `validate_on_abort` field was designed and never added to `Study` at all. The `SignalCheck` variant set was described in its own §7 bullet as an "illustrative placeholder", and its `FftPeakNear` was implemented as a naive O(n²) DFT against synthetic signals, because no real signal ever reached it. The one thing that would have made any of it real — power and sensor hardware producing data worth checking — was deferred to the Later bucket earlier the same day.

**What it cost to keep, [measured 2026-08-25].** `ExpectedValue` inlines two `MAX_PAYLOAD_LEN` buffers, so `PostHocValidation` is 576 bytes; times 64 gives a **36,872-byte inline array** in `Study`. After decision 46 fixed `steps` — the field that actually crashed a debug `embarch-api` — `validations` was **97% of what remained**. `Study` was 77,368 bytes at the start of that pass, 37,960 after decision 46, and **1,088** after this. Decision 46 got a 2× reduction; removing this got a further 35×.

Host v10 → v11, `DEV_BENCH_WIRE_SCHEMA_VERSION` untouched at 9. None of it ever crossed the dev-bench wire (decision 17 said so from the start, and it held), so dev-bench needed no reflash and its C decoder no change — only three stale comments. **This is the second bump to move the host constant alone, and the cleanest evidence yet for decision 12's split**: under the old single constant, deleting a type dev-bench cannot observe would have charged a firmware reflash. A removal is exactly as breaking as an addition on the api↔Core hop, which is why it bumps at all.

**Not "deferred", and not left as a stub.** The alternative on the table was to keep the types and stop growing them. Declined: a subsystem that is fully typed, partly implemented, wired into two repos' call sites, and has never run is worse than no subsystem — it reads as a feature to everyone who meets it, and it was already misleading readers. `embarch-api`'s own MCP tool description advertised `validations` in the study schema to every agent that ever called `run_study`. If post-hoc checks are wanted when real captured data exists to check, they should be designed against that data.

Done **on a branch**, unlike the rest of that pass, at the repo owner's explicit direction — [embarch-dev-workflow.md](../../embarch-dev-workflow.md) §6's standing carve-out for real, risky or exploratory work, not an exception to the no-branches rule.

### 54 — `StepResult.gatt_activity` retired outright — the capture is the file, and it was never the field

The repo owner's call, raised as "can we get free of the 32 cap?" while designing decisions 52/53: `MAX_GATT_ACTIVITY_RECORDS` was 32 records per step, and even a characteristic that notifies rarely exceeds that in a study of any length.

**The answer is that the cap should not be raised, because the field should not exist.** It held a bounded, in-memory copy of something unbounded and streamed: the tap pipeline (decision 39) already writes every record incrementally to a file as it arrives. Keeping the capped copy alongside it meant a study could *look* like it had captured everything while holding 32 of several thousand records — the "nothing captured, no error" family of failure this suite has now been opened by from four directions (decisions 34, 36, 53, and this one). `GattActivityRecord`, `MAX_GATT_ACTIVITY_RECORDS`, and the whole `ble_gatt_activity_record` path in dev-bench went with it.

**What replaces it is not nothing.** Every study with a monitor step now gets a `GattTranscript` tap declared for it automatically ([embarch-ui/design.md](../../embarch-ui/design.md) decision 15) — uncapped, both directions, written to `streams/gatt.csv` as it arrives. Before that pass the Study Designer authored no GATT tap at all, so `gatt_activity`'s first 32 records were genuinely the only inline record a UI-authored study produced; retiring the field without that half would have removed the answer along with the wrong one.

**[Measured, not asserted]:** dev-bench's `sram0_0_seg` on the ESP32-C5 goes **90.87% → 81.12%** — about 37 KB — on a board whose SRAM had already overflowed twice in this suite's history. `DBM_MAX_RAW_LEN` shrinks with it, and `StudyStart` becomes that firmware's largest message again for the first time since v4.

Wire v13 → v14, host v15 → v16. The removal is mid-struct in a message dev-bench hand-encodes, which is what makes this unambiguously a wire bump: an encoder that kept writing even the `None` byte would put `security_level` one byte late and Core would read the activity byte as a security level. Both `StepResult` vectors are re-pinned one COBS code byte shorter, and the populated-`security_level` one is where that shows up as a wrong *value* rather than only a wrong length — the same class of drift the retired `power_samples_ref`/`waveform_ref` bytes caused for a whole schema version before v9 caught them.

### 19 — Two-tier validation: real-time `Outcome` plus a Core-side post-hoc content check

**Retired 2026-08-25** (decision 48). The post-hoc half — `Study.validations`, `PostHocValidation`/`PostHocCheck`/`ValidationSource`/`DataChannel`/`ContentValidity`/`ValidationResult`, and the `core-validation` feature that evaluated them — is gone.

Two things it established that outlived it: **the real-time half stands** and is what dev-bench reports per step (`Outcome`, §4.5) and what `continue_on_fail` gates; and **`validations` never crossed the dev-bench wire**, which decision 17 asserted from the start, which held, and which is what let decision 48's removal cost a host bump and no reflash. Its own late amendment — a stream-fed check names the *tap*, not a `DataChannel`, because a capture belongs to a tap whose scope may outlive any step — was the **first change decision 12's constant split actually spared dev-bench**, and the concrete argument for having made that split.

One rule from its implementation survives it and now lives in decision 18: **naming a tap the study doesn't declare is a `POST /study` pre-flight failure**. Nothing in the type system stops an author naming a tap that isn't there, and the failure it would otherwise produce is a check that silently never runs.

### 28 — Opt-in post-hoc validation over an aborted study's completed steps

**Retired 2026-08-25** with post-hoc validation itself (decision 48). It proposed `Study.validate_on_abort: bool`, defaulting to `false`, so a fuzzer could learn whether data a step *did* capture before a later step aborted the study was itself valid.

Kept as a tombstone because it is **evidence for decision 48 rather than a loss to it**: this refinement was designed, recorded, and the field was **never actually added to `Study`** — so it spent months as a decision describing behavior no code had. That is the failure mode decision 48 names when it declines to leave a subsystem "deferred" rather than removed.

