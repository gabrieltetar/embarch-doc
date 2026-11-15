# HIL notes: premade test suites and the atlas

**Status:** draft, 2026-11-15.

## The idea

**EmbArch ships premade test suites for standards** (USB PD R3.2 first), and the engineer and agent add **custom suites** for one project's own context. The owner is reworking the atlas and **will draft that rework as its own notes folder, and start there**; this file records only what the HIL side needs from it.

**Why this fits the atlas:** a standard binds a *role* (a PD source, a sink), not a part, and the atlas already models it that way ([atlas design](../../embarch-atlas/design.md#standards-and-specifications)). A requirement record there already carries a static `fw_check`, which compares the firmware's configuration with the standard ([same doc](../../embarch-atlas/design.md#firmware-configuration-against-a-standard)). **A premade test is the dynamic check of the same requirement**, so it lives on the same record: one requirement, three things (the requirement, its static configuration check, its hardware test).

## Decided

- **Premade suites live in the atlas, on the requirement records.** Two commits are in play and must not be confused: **an atlas built for a board is pinned to the firmware's commit**, while **the shared suite is EmbArch's own, upstream, at an EmbArch commit.**
- **One suite per standard; each test states the revision range it applies to.** A project says which revision it tests against.
- **A project pins a premade suite by the EmbArch git commit of the shared suite**, named in the test plan; the report states that commit beside the firmware's. **When the installed EmbArch is at another commit, the installed suite runs with a warning**, and the report records both commits.
- **A suite ships IDs only, no spec text.** The spec is copyrighted and the upstream repo is public; any wording a reader sees comes from the engineer's own copy of the spec, distilled locally as the atlas already does.
- **Test procedures are written by EmbArch from the requirement**, never copied from an official compliance test document, and **no compliance test ID appears anywhere**, not even as a cross-reference.
- **Bench binding by convention.** A premade test names signals, boards and instruments by conventional names, and **the suite ships its benches as saved-bench descriptions** that use those names ([03-test.md](03-test.md#benches)). A study naming a signal, never a cable, is today's rule ([studies guide §4](../../suite/studies-guide.md)).
- **The bench boards' command sets are already EmbArch's.** The dev bench, the PD partner and every other bench app are EmbArch firmware in `embarch-dev-bench`, which defines their commands ([pd-bench README](../../../embarch-dev-bench/pd-bench/README.md)), so a premade test and the commands it sends change in the same suite.
- **Mostly black-box, with named DUT hooks.** A premade test drives EmbArch's own partner bench and instruments, the way a conformance lab does. **Where the DUT must act itself** (a swap the DUT initiates), **the test calls a named hook**, which the project maps to a shell command or an operator prompt, or leaves unmapped and the test is skipped with the reason ([03-test.md](03-test.md#the-duts-inputs)). Anything else DUT-specific is a custom test.

## What the HIL side needs from the atlas rework

The Test runner reads these; their shape is the rework's call.

1. **A requirement ID** that is stable across revisions of one standard.
2. **A test record** on a requirement: the study it runs, its verdict rules (limits on parsed numbers), its revision range, its bench and config by name, its run count, the hooks it calls.
3. **The suite's bench descriptions**, in the saved-bench file shape ([embarch-ui decision 73](../../embarch-ui/decisions/saved-benches.md)), with no probe serials.
4. **Applicability**: which tests apply to a role and a set of capabilities. The atlas's `applies` lookup already answers what a role must support ([protocol records](../../embarch-atlas/design.md#protocol-records)).
5. **The capabilities the atlas can decode from a build**, so the runner asks the engineer only for the rest.

## Open

- **Which hook names the first suite needs.** To be drafted with the first suite, not ahead of it.
