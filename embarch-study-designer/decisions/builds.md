# embarch-study-designer decisions: What a study builds

**Status:** active, 2026-09-28.

Split out of [declares.md](declares.md) 2026-09-28, verbatim. That file's own
header is about firmware versions and how each is verified — a version string
compared after the fact. This is a different thing wearing the same field:
what a study builds, and what it refuses to run against — a selection resolved
before the run, and a mode read off the wire.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 77 — A study can declare the firmware it builds for itself, and the outpost mode it needs the DUT to be in

Decision 40 names a gap it could not close: **the DUT reports nothing.** dev-bench self-reports over `HelloAck`; Core flashes the DUT through a probe with no readback path, so `firmware_version` is verifiable only when the run just flashed it. That asymmetry was called one that "cannot be designed away".

**It can, for a DUT with an outpost compiled in, and the mechanism was already on the wire.** The header frame carries a `build_id` *and* a `flags` byte saying which hook families the running firmware has. `Requirements` gains two host-only `Option` fields against it: **`build: Option<BuildSpec>`**, the DUT firmware this study builds and flashes before it runs — field-for-field the selection `embarch-firmware-build`'s `resolve::Selection` already takes, because the resolver is the one thing that knows what a selection means and a second set of axes would need a translation layer whose only job is to lose information — and **`outpost: Option<OutpostModeRequirement>`**, two `u8` masks over that flags byte.

**A declaration, resolved every time, with no pinned `build_id`** — the write-ahead staleness pattern `embarch-topology` decision 3 exists to eliminate, which a later `west build`, a moved tree or a pruned build root falsifies silently. **It names no project either**, which keeps a study portable: which `[[projects]]` entry is the DUT is a property of the bench, as `reflash::dut_project` already treats it.

***Two masks rather than one, because a flag's clear state can be the requirement.*** `TRACE_SELF` is the standing case: clear means the trace deliberately omits the outpost's own drain thread and UART interrupt, so a study reasoning about unaccounted-for intervals needs it **off**, and a single "required" mask cannot ask for that. A bit in neither mask is genuinely not cared about — the third state, and the common one.

**Validation lives here so Core and an authoring UI hold no second copy.** A blank axis is refused where an absent one is fine: the resolver fills an absent axis from the project's `default_target`, while a blank one is the nobody-filled-this-in case decision 40 already refuses for a version. `snippets` mixing the reserved `"none"` literal with real names is refused here as well as at build time (`embarch-api` decision 21's ambiguity, caught at save time). A bit required both set and clear is refused: no firmware satisfies it, so it is a typo. **Snippet order is stored, never normalised** (reversals row 114) — west applies `-S` in order, so two orderings are two images.

**`outpost_requirement_is_satisfiable` is separate, being the one rule needing a field outside `requires`.** The flags byte arrives in an outpost capture's header, so a mode declared without that tap has no subject — refused at submit, which is the difference between "you forgot the tap" while authoring and a DUT sitting reset waiting for a frame nobody asked for.

**`HOST_TYPE_SCHEMA_VERSION` moves to 19; the wire number stays at 15** — `requires` never crosses to dev-bench (decisions 17/39/40). It moves even though both fields default to `None`, because a Core too old to run the pre-flight would otherwise accept a study carrying a build spec and run it unchecked. The new `limits.rs` caps are sized against a real target repo — thirteen snippets, longest name 17 characters; board strings of 26 and 30 — each roughly double the measured case.
