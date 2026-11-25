# HIL notes: premade test suites and the atlas

**Status:** draft, 2026-11-15.

## The idea

**EmbArch ships premade test suites for standards** (USB PD R3.2 first), and the engineer and agent add **custom suites** for one project's own context. The owner is reworking the atlas, **drafted in [notes/atlas/](../atlas/README.md), and starts there**; this file records what the HIL side needs from it, and [notes/atlas/11-hil.md](../atlas/11-hil.md) says where each need lands.

**Why this fits the atlas:** a standard binds a *role* (a PD source, a sink), not a part, and the atlas already models it that way ([atlas design](../../embarch-atlas/design.md#standards-and-specifications)). A requirement record there already carries a static `fw_check`, which compares the firmware's configuration with the standard ([same doc](../../embarch-atlas/design.md#firmware-configuration-against-a-standard)). **A premade test is the dynamic check of the same requirement**, joined to it by requirement ID: one requirement, three things (the requirement, its static configuration check, its hardware test).

## Decided

- **A premade suite runs on a project with no atlas** (owner, review round 1; *replaces "premade suites live in the atlas, on the requirement records"*). **A suite is plain data shipped with EmbArch**: its tests, the requirement IDs each checks, revision ranges, the applicability conditions over a DUT's role and capabilities, and its benches. With no atlas, the report cites requirement IDs only and the engineer supplies the capabilities. **With an atlas, the atlas joins the suite**: requirement text from the engineer's own distillation, capabilities decoded from the build. The reason: requirement records for a standard exist only where the engineer has distilled their own copy of the spec, a heavy first step to ask of someone who wants to try one test.
- **Two commits are in play and must not be confused**: **an atlas built for a board is pinned to the firmware's commit**, while **the shared suite is EmbArch's own, upstream, at an EmbArch commit.**
- **One suite per standard; each test states the revision range it applies to.** A project says which revision it tests against.
- **A project pins a premade suite by the EmbArch git commit of the shared suite**, named in the test plan; the report states that commit beside the firmware's. **A suite also carries a version**, which a release install has where it has no checkout: the plan names both, and the version is what a release compares (review round 2, owner 2026-11-19). **When the installed EmbArch is at another commit, the installed suite runs with a warning**, and the report records both commits; to run the pinned suite instead, the engineer confirms that suite version once, by its manifest hash, and the elevated install can add a signed suite version without a full Core update ([03](03-test.md#the-duts-inputs), review round 4, owner 2026-11-20).
- **A suite ships IDs only, no spec text.** The spec is copyrighted and the upstream repo is public; any wording a reader sees comes from the engineer's own copy of the spec, distilled locally as the atlas already does.
- **Test procedures are written by EmbArch from the requirement**, never copied from an official compliance test document, and **no compliance test ID appears anywhere**, not even as a cross-reference.
- **Bench binding by convention.** A premade test names signals, boards and instruments by conventional names, and **the suite ships its benches as saved-bench descriptions** that use those names ([03-test.md](03-test.md#benches)). A study naming a signal, never a cable, is today's rule ([trace guide](../../suite/trace-guide.md)).
- **The bench boards' command sets are already EmbArch's.** The dev bench, the PD partner and every other bench app are EmbArch firmware in `embarch-dev-bench`, which defines their commands (`embarch-dev-bench` repo, `pd-bench/README.md`; [its decisions](../../embarch-dev-bench/decisions/pd-bench.md)), so a premade test and the commands it sends change in the same suite. **The PD partner is off-the-shelf hardware**: a NUCLEO-G0B1RE with an X-NUCLEO-SNK1M1 (sink) or an X-NUCLEO-DRP1M1 (dual role), flashed with the `pd-bench` app built from `embarch-dev-bench` ([decision 49](../../embarch-dev-bench/decisions/pd-bench.md)); **the guide names them as what a first PD Test needs to buy** (review round 3, owner 2026-11-19).
- **Mostly black-box, with named DUT hooks.** A premade test drives EmbArch's own partner bench and instruments, the way a conformance lab does. **Where the DUT must act itself** (a swap the DUT initiates), **the test calls a named hook**, which the project maps to a shell command or an operator prompt, or leaves unmapped and the test is skipped with the reason ([03-test.md](03-test.md#the-duts-inputs)). Anything else DUT-specific is a custom test.
- **A premade test is a template**, expanded at resolution with the DUT's inputs ([03](03-test.md#selecting-and-rerunning)).
- **Every premade test ships evidence that it can fail** (owner, review round 1; a later phase than the first suite): **a pass on a reference DUT, and a fail as expected against a deliberate fault the PD partner injects** (a late message, a wrong voltage, a refused swap). EmbArch owns the partner's firmware, so each fault is one of its own commands. A test that has only ever passed proves nothing about the test, and for an open-source suite this is the answer to "why trust your tests". **Until it has that evidence a premade test is `unvalidated`, and the report says so beside its verdict**, so a contributor without a PD partner can still add a test, and the validation lands later on a bench that has one (review round 2, owner 2026-11-19).
- **A small example suite any DUT with a shell can run ships with the Test route, before the first premade PD suite**, as a template for contributors and so a first Test needs no EmbArch bench hardware; it is not the walkthrough the owner declined (review rounds 2 and 3, owner 2026-11-19).

## What the HIL side needs from the atlas rework

The Test runner reads these when an atlas is present; their shape is the rework's call. **None of them is needed to run a suite.**

1. **A requirement ID** that is stable across revisions of one standard, matching the IDs the suite cites.
2. **The join from a suite's test to its requirement record**, so the report quotes the engineer's own distilled text and the static `fw_check` sits beside the dynamic test.
3. **Applicability from the standard**: the atlas's `applies` lookup already answers what a role must support ([protocol records](../../embarch-atlas/design.md#protocol-records)), and the report's count of the standard's applicable requirements comes from it ([03](03-test.md#the-report)).
4. **The capabilities the atlas can decode from a build**, so the engineer is asked only for the rest; each one marked `decoded`.
5. **The hardware a run ran on** (the unit, its board revision and reworks), which [notes/atlas/11-hil.md](../atlas/11-hil.md) already adds.

## Open

- **Which hook names the first suite needs.** To be drafted with the first suite, not ahead of it.
- **The suite's file format and where it ships**: in `embarch-api`'s repo, or a repo of its own. Recommended: a repo of its own, `embarch-suites`, so a suite's commit pins the suite alone and contributors to a standard's suite need not touch the API.
- **The fault-injection commands the PD partner needs**, listed with the first validated test. **How a contributor adds a bench app** for a standard the PD partner does not cover is answered: it goes into `embarch-dev-bench`, its image's hash into the next release, and until then it reads `unreleased` by design; a Core in the engineer's own account takes the hash list from a checkout ([03](03-test.md#a-run), item 3, review round 4, owner 2026-11-20). What its commands look like stays open.
