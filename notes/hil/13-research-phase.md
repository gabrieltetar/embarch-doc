# HIL notes: the research phase, and a bench with no DUT

**Status:** draft, 2026-11-18.

Opened by EMB-213: a contact microphone slid over a textured surface, sampled at audio rate on a Nordic dev kit, seen live, recorded, and its bumps counted. **It is the first research pass of a project**: no custom board exists, dev kits and breakouts are wired together, and the thing being studied is a sensor concept, not firmware. The analog capture itself is [embarch-analog-capture-proposal.md](../../embarch-analog-capture-proposal.md); this note is what that pass asks of the HIL design. **Every answer here is the owner's, 2026-11-18 or 2026-11-19 as marked, unless it sits under Open**; the note's own review is in [10](10-review.md#note-13s-review-2026-11-18).

## Decided

- **No fourth mode.** Purpose separates the modes ([01](01-modes.md#what-separates-them)), and research is a phase of a project, not a purpose. A research question answered by measurement ("does each bump make one distinct event, and does the count match the known one?") is a **Study**; looking at a signal or a register while developing is **Live**. The three modes match the lab's own words: characterisation, verification and debugging. A mode per phase would cut across all three, since research, bring-up and validation each hold Studies and Live sessions, and every rule would then exist twice.
- **A bench holds zero or one DUT**, as it already holds zero or one dev bench. Allowed for a **Study** and for **Live**; **a Test needs a DUT** ([A bench with no DUT](#a-bench-with-no-dut)).
- **The phase changes the bench, never the mode.**
- **The words are "no DUT board"**: in lab usage the DUT is whatever is tested, here the microphone (owner, 2026-11-19). This note's headings keep their words so their links hold.

## Before custom hardware: a dev kit is the DUT

**Wired dev kits are not a DUT-less bench.** The DUT is a role, and a role holds a board type, "a shape a repo builds for" ([embarch-topology storage and roles](../../embarch-topology/spec/storage-and-roles.md)); a dev kit running the engineer's firmware is a DUT like any other. At bring-up the saved bench changes (the custom board replaces the kit, `set_role_board` records the new board type, `validate` reports the new unit) and **a study naming roles and signals runs unchanged on the new bench**, so the same measurement can be repeated before and after the custom board exists. This is the normal start of a project, not an exception, so the guide should say it where it sets a bench up (placement: Open).

## A bench with no DUT

**A bench has no DUT when nothing under test runs firmware**: the subject is a sensor, a transducer or a passive circuit, wired to a bench board's input or to an instrument. EMB-213's first route is one: the microphone wired to the dev bench's own ADC.

| Mode | With no DUT | Why |
|---|---|---|
| Study | **Allowed** | A characterisation of a part is a custom question answered by measurement; every value is `by: bench` or `by: person` |
| Live | **Allowed** | Live already reaches "the DUT and its bench boards"; with no DUT it reaches the bench boards |
| Test | **Refused** when the test is defined, naming the bench | A Test judges a unit's conformance: the runner checks the same unit on every bench ([03](03-test.md#benches)) and charges a fail to what the step addressed ([03](03-test.md#the-verdict)). A part with no hardware ID gives neither anything to hold |

**What changes where a bench holds no DUT**:

- **`validate` and the smoke check skip the DUT** ([02](02-study.md#how-a-study-runs-as-the-procedure-would-say-it) step 2, [03](03-test.md#a-run) item 3): no DUT identity, no DUT image read back. **The skip is never silent**: the audit appendix ([06](06-report-and-publish.md#the-audit-appendix)) reads "Subject: <part> (declared), no DUT board" where the DUT's identity and image would be.
- **Core decides there is no DUT from its own state, never from the study's word** (owner, 2026-11-19), which is what keeps the skip from being a way around the smoke check. The `dut` role holds no probe and no board type, a state only the person's acts (`unenroll_probe`, `set_role_board`) produce ([05](05-live.md#reach-and-permission)); **Core refuses the skip when that role is bound, or when the study names a DUT role or a DUT signal**; the appendix lists every attached probe the bench does not name. A board left wired to the subject with no probe is outside what Core can see ([12](12-prevention.md#what-stays-outside-prevention-and-is-said-so)), so the guide says to unplug the DUT-side kit rather than leave it idle.
- **A bench with no DUT has a declared subject, and the run history is keyed on it** (owner, 2026-11-19). The subject (the part, its fixture) is a person's act like an instrument's calibration, and the report shows it as declared, not read. The history of every run on the same unit ([06](06-report-and-publish.md#the-audit-appendix)) is keyed on the DUT's hardware ID; **with no DUT it is keyed on the declared subject plus the bench boards' IDs**, and the report says "subject declared, not read: its history may be split", since a part with no ID cannot prove it is the same one.
- **Every measurement is `by: bench` or `by: person`**, since there is no DUT to report about itself.
- **The vocabulary**: a bench is "zero or one DUT, zero or one dev bench, and any bench boards and instruments" ([README](README.md#vocabulary)).

## Who samples decides the evidence

**The board that digitises a signal is the one that measured it**, so a research bench's choice of where to wire the sensor is also a choice of evidence ([02](02-study.md#measurements)):

- **A dev kit in the DUT role samples it**: every value is **`by: dut`**, the DUT's own word, from firmware the agent may have written, with the resolution and `U` the study declares.
- **A bench board samples it**: every value is **`by: bench`**, with the smoke check's `bench_image` beside it and the resolution and `U` from that board's own declaration ([02](02-study.md#measurements)). **That is stronger evidence only for a `released` image**: a bench board on a new, `unreleased` build that the agent flashed is no stronger than the DUT's word ([03](03-test.md#a-run), item 3).

**For a question about a sensor, a bench board on a released image is the stronger evidence**; for a question about the DUT's firmware, such as whether its own detector counts right, the DUT is the subject and `by: dut` is the honest label. EMB-213 has both, in that order.

**When one board relays another's samples, `by` follows the tap's declared origin**, a person's act: a relayed payload belongs to the board that produced it, as DUT notifications through the dev bench already do (owner, 2026-11-19). **A value a Study declares for itself** (a `dut` value's resolution and `U`, a declared sample rate, the DUT's block index) is the agent's word, since nothing confirms a Study's definitions: **the report labels it "declared by the study, unconfirmed"**, and Core checks a declared rate against the sample count over its own capture interval ([02](02-study.md#measurements), owner, 2026-11-19). **No bench board streams samples from a general analog input today** (the dev bench has none, [its spec](../../embarch-dev-bench/spec.md) §1); the proposal is where one would be added.

## The detector being researched

**A research pass exists to find a detector, and the HIL design lets no agent-written script compute a reported number** ([02](02-study.md#measurements)): reported numbers come from Core, at step time or through the built-in reducers. What a payload means stays the engineer's ([embarch-study-designer decision 52](../../embarch-study-designer/decisions/payload-meaning.md)), so the suite cannot ship the detector either. **So the count being researched cannot, today, be a measurement in a published report.** Three ways through, not exclusive:

1. **A built-in reducer that counts excursions**: past a declared threshold, with a declared hysteresis and minimum spacing, over one `Samples` series with a declared rate. It is a number-series operation like a percentile and gives the bytes no meaning, so it stays inside decision 52. Its count carries no `U` (a count: none, [02](02-study.md#measurements)); its threshold, hysteresis and spacing are its `method`; a gap inside its window makes it incomplete, and **a loss it cannot place makes the whole series incomplete**. **It needs the proposal's stage B**: stage A records raw bytes, with no series and no rate.
2. **The engineer's own detector**, run offline on the recording. In an agent-driven pass the agent usually writes and runs it, so **its result is tagged `(analysis)`** (owner, 2026-11-19), the fourth tag beside 02's `(derived)`, `(spec)` and `(inference)` ([02](02-study.md#the-report)): **attributed by the token that entered it**, "agent" unless the person adopts it as with a prose block, with **the hashes of the script and of the capture it read** in the audit appendix, and **`verify` reporting it "not recomputed"**. It is never a measurement.
3. **The detector in the DUT's firmware** (EMB-213's last item), its count `by: dut`, with a DUT in the role.

## The known count

**The count the detector is compared with is a `person` measurement**: an observation prompt asking how many ridges the sensor crossed, which the model already has ([02](02-study.md#measurements)). **A fixture's ridge count is a person's act** (owner, 2026-11-19), kept in Core's store like a calibration, **refused with the agent's token** and shown as "declared by <person>". It is new to the model: 02's declared setup terms are uncertainty terms, not values, and a reference value the agent could write would let it set the count its own detector is compared with. In a Study the two counts sit side by side in the report; **a limit on their agreement makes it a Test**, which needs a DUT, so it waits for the detector to run in the DUT.

## Many scans, few reports

**A research session is many short captures, most never cited.** Each is a Study run, logged in Core's run log; publishing is a separate, explicit step ([06](06-report-and-publish.md#publish)), so **an unpublished run is a recorded scan**, and once the proposal's stage B lands the Live Study tab is its live view. **A look that will not be counted or cited stays Live**: Core's capture outside a study ([embarch-core decision 92](../../embarch-core/decisions/signal-capture.md)), with the caveat that its reads are text. **A scan about to be cited is published**, which is when the rule that a cited result has a published receipt ([01](01-modes.md#how-an-agent-picks-a-mode)) is met; an unpublished run is not that receipt. **A scan's captures may be discarded, by either token**: its run-log entry and capture hashes stay, and the history shows "captures discarded" with the scope of the token that discarded them, so a reader sees every discard (owner, 2026-11-19).

## Open

- **The detector**: recommended, the built-in excursion-count reducer (way 1) beside the `(analysis)`-tagged offline count (way 2), with way 3 once the DUT runs it. Its name, contract and fixture go with the reducer crate.
- **Whether Core runs a study with no DUT enrolled today**: `run_study`, `run_host_study` and `validate` against an empty DUT role, to check in embarch-core when the work starts.
- **What a Study run costs per scan**: the lease, the smoke check, and for a host study ending on a prompt the person's go on the card ([02](02-study.md#how-a-study-runs-as-the-procedure-would-say-it)). Unmeasured against a 5 s capture; if it dominates, a research session wants many captures in one run.
- **A Test of a part with no firmware** (a sensor against its datasheet): refused for now; reopened when a premade suite needs one.
- **Where the no-DUT bench and the research pass sit in `suite/hil-guide.md`**: recommended, "Before any hardware" for both benches and the Study section for the detector and the known count ([07](07-procedure-doc.md#an-outline-of-the-guide), items 2 and 4).
