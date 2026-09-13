# embarch-study-designer decisions: What a study declares about what it runs against

**Status:** active, 2026-09-02.

Firmware versions, and how each is verified. The GATT table a study declares
split out 2026-09-13, verbatim, to [declared-gatt.md](declared-gatt.md) — it is
designed-never-built and shares no code or citation with 40 or 74.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 40 — A study declares the firmware versions it is meant to run against; reflashing is the operator's per-run choice

It closed a gap wider than the one it was raised for: **a result could not say what it ran against.** Two runs of the same study against two different builds produced results **indistinguishable after the fact** — the same silent-mislabelling class decisions 39 and 35 exist to prevent, **sitting unnoticed in the middle of the thing the whole suite produces.**

Two free-form strings matching the shape the bench already reports. **Host-side only — they never cross the wire to dev-bench**, which has no use for a requirement it cannot check about itself. **A test asserts that structurally rather than by inspection:** two studies differing only here must encode byte-identical dispatch messages and the same seal.

**Both fields are mandatory, and `any` is an explicit legal value.** "I don't care which build" is legitimate — a bench self-test involves no DUT at all — **but it has to be *said*, not achieved by leaving a field out.** There is no serde default, so an omitted requirement **fails to deserialize rather than quietly becoming `any`**, and a *blank* one is a separate explicit pre-flight failure — **because the failure this decision exists to prevent is precisely the one where nobody thought about it.**

**Reflash is a run parameter, not a study field**, the same split decision 39 draws for signal routes: **a study describes what the experiment *is*, and how a particular run is set up to satisfy it is the operator's call.** Baking it in would mean a saved study **that reflashes a board every time you re-read its results.** So the override and the flashed version cross as **query parameters** — literally run parameters — which also **leaves the study body byte-identical, so both seals and every fixture on disk are untouched.** Query rather than a header for the same reason the override is recorded rather than honoured silently: **it shows up in Core's request log and in a command an engineer types by hand.**

**On a mismatch with no reflash requested, the study is rejected before any step runs**, naming both strings. **Not a warning that proceeds: a result attributed to the wrong firmware is worse than no result**, which is this decision's whole premise. An explicit override is available and **recorded in the result** rather than silently honoured.

**The verification asymmetry is the load-bearing limitation and cannot be designed away.** The bench *self-reports* its version, so a bench requirement is genuinely **checked**. **The DUT reports nothing at all** — Core flashes it through a debug probe with no readback path — so a DUT requirement is verifiable only when the outpost is compiled in, whose header carries a build ID, **or the run just flashed it.** A result therefore records not just the versions but **how each was established**: reported by the bench, reported by the outpost, flashed this run, or merely declared. **A result quietly presenting a declared string as a verified one would be the same defect in a new place.**

**A consequence this decision did not anticipate, and the most useful thing its implementation produced:** supplying the flashed version is also **what makes the DUT requirement *checkable*.** That sentence in the asymmetry above had no implementation anywhere, and it is now Core's gate rejecting on the DUT half too. What the flashed string *is*, stated because the asymmetry does not go away: **it is derived from the tree that was built, not from the board.** So flashed-this-run is **stronger than declared, where nobody checked at all, and weaker than a bench self-report, which is a measurement** — exactly the ordering the provenance type exists to express.

The comparison rule and the is-this-verified decision both live in this crate, **so Core's gate holds no second copy and no UI re-derives which variants count.**

**The human surface was the first thing that ever stated a real requirement:** the Study Designer had been submitting "any" unconditionally — **honestly, since it had no fields to say anything else in.** Both fields are now prefilled from live bench state, `any` is a visible checkbox rather than an empty field that happens to validate, and **a blank field is refused rather than quietly promoted, which is the distinction this decision rests on.**

### 74 — `firmware_version` keeps its name on both surfaces, and every reader is told whose build it is

**One field name covers two different boards' builds, in the one flow that reads both.** `HelloAck.firmware_version` is the **bench's** (embarch-dev-bench decision 18); `Requirements.firmware_version` and `Provenance.firmware_version` are the **DUT's**. Both consumers do the crossing by hand — `embarch-api`'s reflash gate and `embarch-core`'s study start each assign `hello.firmware_version` into a **`dev_bench_version`** — so the correspondence is bench→`dev_bench_version`, and the identically named field is the other board.

**This had already produced a wrong message, and that half is fixed rather than documented.** `embarch-core`'s `clamp_version` warned *"dev-bench reported a firmware_version longer than N bytes"* for all four values that reach it, including the DUT's `flashed_firmware_version`, which `embarch-api` supplies out of band and which no bench ever reported. It now takes a `VersionSubject` — the enum decision 40 already introduced for exactly this distinction — so the message names the board and the compiler makes every call site say which one it means.

**The names themselves stay, and the argument is not the same for all three.** Renaming `HelloAck.firmware_version` to `dev_bench_version` is **rejected on cost**: that field is on the wire, so the rename is a schema bump that reflashes every bench and redeploys Core in the same sitting ([embarch-dev-workflow](../../embarch-dev-workflow.md) §4a), against a defect whose damage is a misleading log line and a mis-authored study. Renaming only the host-side pair is worse than either — it breaks every saved study and every `StudyResult` on disk while *leaving* the wire field that invites the confusion.

**The third surface is a genuinely open question and this decision does not close it.** `embarch-core`'s `GET /dev-bench/hello` serves that value as `firmware_version` over **HTTP**, where a rename costs no reflash — and `embarch-core` decision 47 did exactly this rename, for exactly this defect class, on this exact route: `hardware_id` became `self_reported_hardware_id` because a caller comparing it against `/probes/enrolled`'s `hardware_id` got a near-miss rather than a category error. That precedent points the other way from this decision, and it is not dismissed here — **it is filed as `tasks/suite/036`** rather than taken, because it changes a served field on Core's surface and the announcement window this unit ran under covered the `clamp_version` fix and the doc comments, not an API rename.

**So the ambiguity is named where a caller reads it**, which is the same posture decision 40 takes toward the verification asymmetry it also could not design away: the doc comments on all three fields now say whose build the value is and which field on the other surface it corresponds to.

**The failure this closes is silent, which is why naming it is worth a decision rather than a comment.** A caller that reads `/dev-bench/hello`'s `firmware_version` and writes it into `requires.firmware_version` has pinned a DUT requirement to the bench's build — and `embarch-core` only *compares* `requires.firmware_version` when a `flashed_firmware_version` is supplied, so in the normal no-reflash case the wrong value is accepted and recorded as `Declared`. **That is precisely the mislabelling `Provenance`'s source fields exist to prevent**, reached by a route those fields cannot see: the source is honestly `Declared`, and what was declared is a fact about the wrong board.

**Reversal condition.** The next wire-schema bump this crate takes for another reason is when the rename becomes free. If one lands and `HelloAck.firmware_version` is still called that, this decision was kept past its cost argument.
