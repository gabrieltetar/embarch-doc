# embarch-study-designer decisions: What a study declares about what it runs against

**Status:** active, 2026-09-02.

Firmware versions and the GATT table, and how each is verified.

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

### 45 — A study declares the GATT table it was authored against, and live discovery is what checks it

Three sources of GATT knowledge existed here, built at three different times, and **nothing ever joined them**: vendor identities, static extraction, and the engineer-authored registry. A study could reference any and declared none, **so nothing could answer the question this milestone actually got stuck on — *is the service this study writes to even present on the build under test?* A whole session ran without that being answerable, because the DUT's GATT table had never once been seen.**

An optional declaration carrying a source and the services, **reusing the same types a live discovery fills in rather than a parallel shape, so comparing the two is a comparison and not a translation.** The source is one of: resolved vendor identities, an extraction against a real checkout **recording *which* checkout**, or hand-authored. Host-side only, **and dev-bench continues to interpret nothing.**

**Live discovery wins, and the difference is reported rather than tolerated.** When a discovery step runs in a study that declared a table, Core reconciles the two and records **what was declared-but-absent, present-but-undeclared, or present with different properties.** A declared service missing from the DUT is **not a study failure by default — it is the single most useful line in the result**, and exactly the fact nobody could produce for a whole session: the config symbol was set, **but was the service actually registered?**

**This is the durable form of decision 35's rule.** That decision said engineer-supplied knowledge must come from the engineer; **this one says where in the study it goes, so an agent authoring one has a field to put it in rather than a temptation to infer it.**
