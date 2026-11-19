# HIL notes: the research phase, and a bench with no DUT

**Status:** draft, 2026-11-18.

Opened by EMB-213: a contact microphone slid over a textured surface, sampled at audio rate on a Nordic dev kit, seen live, recorded, and its bumps counted. **It is the first research pass of a project**: no custom board exists, dev kits and breakouts are wired together, and the thing being studied is a sensor concept, not firmware. The analog capture itself is [embarch-analog-capture-proposal.md](../../embarch-analog-capture-proposal.md); this note is what that pass asks of the HIL design. **Every answer here is the owner's, 2026-11-18, unless it sits under Open.**

## Decided

- **No fourth mode.** Purpose separates the modes ([01](01-modes.md#what-separates-them)), and research is a phase of a project, not a purpose. A research question answered by measurement ("does each bump make one distinct event, and does the count match the known one?") is a **Study**; looking at a signal or a register while developing is **Live**. The three modes match the lab's own words: characterisation, verification and debugging. A mode per phase would cut across all three, since research, bring-up and validation each hold Studies and Live sessions, and every rule would then exist twice.
- **A bench holds zero or one DUT**, as it already holds zero or one dev bench. Allowed for a **Study** and for **Live**; **a Test needs a DUT** ([A bench with no DUT](#a-bench-with-no-dut)).
- **The phase changes the bench, never the mode.**

## Before custom hardware: a dev kit is the DUT

**Wired dev kits are not a DUT-less bench.** The DUT is a role, and a role holds a board type, "a shape a repo builds for" ([embarch-topology storage and roles](../../embarch-topology/spec/storage-and-roles.md)); a dev kit running the engineer's firmware is a DUT like any other. At bring-up the saved bench changes (the custom board replaces the kit, `set_role_board` records the new board type, `validate` reports the new unit) and **a study naming roles and signals runs unchanged on the new bench**, so the same measurement can be repeated before and after the custom board exists. The guide says so in its "Before any hardware" section ([07](07-procedure-doc.md#an-outline-of-the-guide), item 2), because it is the normal start of a project and not an exception.

## A bench with no DUT

**A bench has no DUT when nothing under test runs firmware**: the subject is a sensor, a transducer or a passive circuit, wired to a bench board's input or to an instrument. EMB-213's first route is one: the microphone wired to the dev bench's own ADC, nothing running on the DUT-side kit.

| Mode | With no DUT | Why |
|---|---|---|
| Study | **Allowed** | A characterisation of a part is a custom question answered by measurement; every value is `by: bench` |
| Live | **Allowed** | Live already reaches "the DUT and its bench boards"; with no DUT it reaches the bench boards |
| Test | **Refused** when the test is defined, naming the bench | A Test judges a unit's conformance: the runner checks the same unit on every bench and charges a fail to it ([03](03-test.md#benches)). A part with no hardware ID gives neither anything to check |

**What changes where a bench holds no DUT**:

- **`validate` and the smoke check skip the DUT** ([02](02-study.md#how-a-study-runs-as-the-procedure-would-say-it) step 2, [03](03-test.md#a-run) item 3): no DUT identity, no DUT image read back. **The skip is never silent**: the report's audit appendix states "no DUT on this bench" where the DUT's identity and image would be.
- **Every measurement is `by: bench` or `by: person`**, since there is no DUT to report about itself.
- **The vocabulary**: a bench is "zero or one DUT, zero or one dev bench, and any bench boards and instruments" ([README](README.md#vocabulary)).

## Who samples decides the evidence

**The board that digitises a signal is the one that measured it**, so a research bench's choice of where to wire the sensor is also a choice of evidence ([02](02-study.md#measurements)):

- **A dev kit in the DUT role samples it**: every value is **`by: dut`**, the DUT's own word, from firmware the agent may have written, with the resolution and `U` the study declares.
- **A bench board samples it**: every value is **`by: bench`**, from EmbArch's own bench firmware, with the smoke check's `bench_image` beside it and the resolution and `U` from that board's characterisation ([06](06-report-and-publish.md#the-audit-appendix)).

**For a question about a sensor, the bench reading it is the stronger evidence**; for a question about the DUT's firmware, such as whether its own detector counts right, the DUT is the subject and `by: dut` is the honest label. EMB-213 has both, in that order. **No bench board has an analog input today** ([embarch-dev-bench spec](../../embarch-dev-bench/spec.md) §1); the proposal is where one is added.

## The detector being researched

**A research pass exists to find a detector, and the HIL design lets no agent-written script compute a reported number** ([02](02-study.md#measurements)): reported numbers come from Core, at step time or through the built-in reducers. What a payload means stays the engineer's ([embarch-study-designer decision 52](../../embarch-study-designer/decisions/payload-meaning.md)), so the suite cannot ship the detector either. **So the count being researched cannot, today, be a measurement in a published report.** Three ways through, not exclusive:

1. **A built-in reducer that counts excursions**: past a declared threshold, with a declared hysteresis and minimum spacing, over one `Samples` series. It is a number-series operation like a percentile and gives the bytes no meaning, so it stays inside decision 52. Its count carries no `U` (a count: none, [02](02-study.md#measurements)); its threshold, hysteresis and spacing are its `method`, and a dropped-record gap inside its window makes it incomplete, as every reducer reports.
2. **The engineer's own detector**, run offline on the recording, with its result labelled as the engineer's analysis: in a report it is a tagged number, listed in the audit appendix ([02](02-study.md#the-report)), never a measurement.
3. **The detector in the DUT's firmware** (EMB-213's last item), its count `by: dut`, with a DUT in the role.

## The known count

**The count the detector is compared with is a `person` measurement or a declared fact**: an observation prompt asking how many ridges the sensor crossed, or the fixture's ridge count declared with the bench. Both exist in the model already ([02](02-study.md#measurements)). In a Study the two counts sit side by side in the report; **a limit on their agreement makes it a Test**, which needs a DUT, so it waits for the detector to run in the DUT.

## Many scans, few reports

**A research session is many short captures, most never cited.** Each is a Study run, logged in Core's run log; publishing is a separate, explicit step ([06](06-report-and-publish.md#publish)), so **an unpublished run is a recorded scan** and the Live Study tab is its live view. **Live stays instant reads and actions**: a capture is never a Live call, since Live reaches instruments only through a Study or a Test ([05](05-live.md#reach-and-permission)). The rule that a result about to be cited is redone as a Study ([05](05-live.md#when-live-is-not-enough)) is already met: the scan was one.

## Open

- **The detector**: recommended, the built-in excursion-count reducer (way 1) beside the labelled engineer's analysis (way 2), with way 3 once the DUT runs it. Its name, its contract and its fixture go with the reducer crate.
- **What names the subject of a bench with no DUT**: recommended, a declared subject (the part, its fixture), entered as a person's act like an instrument's calibration, and shown in the report as declared, not verified.
- **Whether Core runs a study with no DUT enrolled today**: `run_study`, `run_host_study` and `validate` against an empty DUT role, to check in embarch-core when the work starts. The docs read here do not say.
- **What a Study run costs per scan** (the lease, the smoke check) against a 5 s capture: unmeasured. If it dominates, a research session wants many captures in one run.
- **A Test of a part with no firmware** (a sensor against its datasheet): refused for now; reopened when a premade suite needs one.
- **Where the no-DUT bench and the research pass sit in `suite/hil-guide.md`**: recommended, "Before any hardware" for both benches and the Study section for the detector and the known count ([07](07-procedure-doc.md#an-outline-of-the-guide), items 2 and 4).
