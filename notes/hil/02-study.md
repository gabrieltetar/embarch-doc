# HIL notes: the Study mode

**Status:** draft, 2026-11-15.

## What a Study is

**A custom, almost scientific question, answered by measurement on exactly one bench.** A bench here is one DUT, zero or one dev bench, and any companion boards and instruments wired to that setup ([README](README.md#vocabulary)). Two benches in one piece of work make it a Test.

**The runner is not what makes it a Study.** A dev-bench study (`run_study`, the bench plays the DUT's BLE counterpart) and a host study (`run_host_study`, Core drives serial exchanges, instruments and operator prompts itself) are both Studies when what they produce is measurements.

**The worked example is a BLE GATT data-acquisition study**: the bench connects to the DUT, subscribes to its data characteristics, and captures what arrives, so the report can state the rate and the losses. The owner reports this path already runs on hardware; **the report half is what is missing.**

## How a Study runs (as the procedure would say it)

1. **Lease.** `lease_take` with a purpose ([01-modes.md](01-modes.md#the-lease)).
2. **The bench is the one the study expects.** The saved bench is live, and `validate` passes for the DUT and the dev bench.
3. **The firmware is the one the study declares.** The study's build declaration and `--reflash` decide whether anything is built and flashed ([studies guide §2](../../suite/studies-guide.md)); `status`'s `last_images` against the agent's own image says what is on the board now.
4. **Run.** `run_study` or `run_host_study`; `study_watch` or `study_status` until it ends. **Before the study's first step, Core runs a Test's smoke check** on its bench ([03](03-test.md#a-run), item 3): identities, the DUT's image read back, every bench board's image and its `bench_image`. **A host study that holds a prompt or an energising step does not start on the agent's call**: Core registers it, applies the clearance rule to it as it does to `run.json` ([12](12-prevention.md#operator-prompts-by-kind)), and **the person's go on the card**, which shows every prompt with its kind and what the study powers, starts it and pins those kinds; a study with neither starts on the agent's call, as today (review round 3, recommended).
5. **Read the losses before the data.** `list_study_streams`: every tap, its bytes, and **whether it was truncated** ([studies guide §1](../../suite/studies-guide.md)).
6. **Read the measurements, not the captures.** `measurements.json` is small enough for the agent's context; a raw capture is not, and a conclusion drawn from a sample of one is the failure this avoids ([09](09-trust-model.md), F8).
7. **Draft the prose the study asks for**, citing measurements by name, then **publish** ([06-report-and-publish.md](06-report-and-publish.md)).

## Measurements

**A measurement is a named value**: `{name, value, unit, source: {file, rows or bytes}, by, instrument, bench_image, method, resolution, uncertainty}`, where **`method` is how Core produced it** (`parse` with the step's pattern, or the reducer's name and window), **`bench_image` is the producing board's image status** ([03](03-test.md#a-run), item 3) (review round 3, recommended), **`instrument` names the bench board or instrument that produced it** (its identity and, for an instrument, its calibration), **`uncertainty` is `U` with its coverage factor and basis** ([03](03-test.md#the-verdict)), and **`by` says who measured it**: `bench` (EmbArch's bench boards or instruments), `dut` (the DUT reporting about itself, in firmware the agent may have written) or `person` (an observation prompt's answer); the report shows it beside the value ([12](12-prevention.md#what-stays-outside-prevention-and-is-said-so)). **Core fills `by` and `instrument` from what the step addressed**, and `resolution` and `uncertainty` from that instrument's or bench board's own declaration, never from the study, so an agent-written study cannot mark a DUT's word as the bench's (review round 2, recommended). **Where the uncertainty comes from, by producer** (review round 3, recommended): a value read straight from an instrument or bench board takes that source's declared `U`; **a derived measurement takes the `U` its reducer derives from its inputs'**, by a rule each reducer's contract states (an interval between two markers: the two stamps' `U` and the clock's combined by root sum of squares; a mean: its inputs' `U`, not divided, since a systematic error does not average out; a count: none); **a test may add declared setup terms** (a cable's drop, a fixture's offset), each a person's act like an instrument's `U`; **a `dut` measurement takes the resolution and `U` its test declares**, confirmed with the test; and **a `person` measurement** is a choice among the prompt's declared answers, or a number with the unit, resolution and `U` the prompt declares. **Two producers** (owner, review round 1):

- **Core, at step time**: a host-study step's declared numeric parse ([03-test.md](03-test.md#the-verdict)).
- **Core, after each test or study ends**: **derived measurements**, declared by name in the study, over its captures, from **a fixed set of built-in reducers**: count, rate, min, max, mean, a percentile, the interval between two markers, the value at a marker. Rust, deterministic, versioned. No agent-written script computes a reported number.

**The reducers and the verdict rules are one crate** (owner, review round 1), in `embarch-study-designer`'s host-only half: **Core links it to judge each test as it ends**, so a verdict resting on a derived measurement can still end its test, skip what `requires` it, or stop the run; **embarch-api links it for `verify`**, so a zip is rechecked by the code that judged it. One implementation, the way `embarch-topology` is the one implementation of hardware access ([embarch.md](../../embarch.md) §4). **Each reducer has a stated contract** (its inputs, its output unit, how it reports incomplete input) and a fixture of its own, so a contributor adds one as a small reviewable change, and the guide's reducer list is generated from the crate. **A contributor builds and tests a reducer in the crate alone** (`cargo test` against its fixtures, no Core installed); it reaches a bench with the next Core release, and **the crate's version is written into every signed record and `measurements.json`, so `verify` judges a zip with the version that produced it**, or says it cannot (review round 2, recommended).

Both land in **`measurements.json`**, the one file that **limits** act on ([03](03-test.md#one-test)), **`report.typ`** reads, **prose** cites, the audit appendix traces through each `source`, and **`verify`** recomputes ([06](06-report-and-publish.md#verify)). A measurement over a truncated capture, or across a dropped-record gap, says so, and a verdict resting on it is inconclusive.

## The report

**Its shape is free, and decided by the study itself.** Each study carries its own `report.typ`, a Typst source that reads the run's `measurements.json` and files, and draws its own plots. embarch-api compiles it at publish time. The lab-report shape (question, method, setup, results, analysis, limits, conclusion) is the shape the guide recommends and the example uses, and nothing enforces it.

**The run's files are the numeric oracle** (owner, review round 1), the atlas's rule carried over (`embarch-atlas` repo, `DESIGN.md`, "Principles" 2). **Every number in the prose and in `report.typ`'s text equals a measurement it cites, or carries a tag**: `(derived)`, `(spec)` or `(inference)`. Publish goes ahead and **lists in the audit appendix every untagged number that matches no measurement**, so a number the agent typed from memory is visible to whoever reads the report. Made precise (review round 2, recommended):

- **The match**: **a number in prose cites the measurement it states, by name** (`#m("rate")` in Typst, `[rate]` in a prose file), and matches when it equals that measurement's value rounded to the significant digits written, in its unit or one the crate converts (mV and V, ms and s); **a number that cites nothing but equals some measurement is listed as "unbound"**, since a value of the same size can be a coincidence (review round 2, recommended).
- **A tag is shown in the report beside its number**, and the appendix lists every tagged number too, so an agent cannot hide a number behind a tag unseen.
- **`report.typ`'s numeric literals** that reach the page (a hardcoded array plotted, a number in its markup) are listed as "hardcoded" in the appendix, and **`verify` rescans the `report.typ` in the zip for them** rather than trusting the list; **a plot takes its series from a signed file, by name, through EmbArch's plot helper**, and one drawn any other way is listed as unverified (review round 2, recommended).
- **It is checked on the rendered PDF, by `verify`**, not only by the embarch-api that published it, which the agent can reach: every number in the PDF's text matches a signed measurement, is listed in the appendix, or is in an exempt context (a page number, a date, a hash, an ID, an axis tick of a plot drawn by EmbArch's plot helper) ([06](06-report-and-publish.md#verify)).

**Who writes each prose section is decided by the study**, and **the report says who wrote each block** (owner, review round 1): `agent (<model id>)` or a person's name; a person may adopt an agent's block, which then reads "agent, reviewed by <name>". The appendix lists every block and its author. **A person's name on a block, and an adoption, is a person's act**, made on the card with the person's token like a confirmation; a block or adoption entered with the agent's token reads "agent", whatever name it carries (review round 2, recommended).

**A Study with no `report.typ` still publishes**: the audit appendix plus a data section listing each capture with its row count and each measurement, so a Study is never unpublishable.

**embarch-api always appends a fixed audit appendix** that the study cannot leave out ([06-report-and-publish.md](06-report-and-publish.md#the-audit-appendix)).

## Where its files live

**Both study kinds are saved in the firmware repo's `embarch/studies/<slug>/`**: the study file, its `report.typ`, and the prose files the agent writes, side by side. A dev-bench study is saved under `embarch/studies/` by the Study Designer today ([embarch-ui spec](../../embarch-ui/spec.md)); **a host study is not saved in a repo at all** ([embarch-ui decision 96](../../embarch-ui/decisions/bench-configs.md)), so this is new for host studies. **It removes a premise of decision 96**, which never refuses renaming or deleting a bench config because no saved host study can name one: once host studies and tests are saved, **renaming or deleting a config a saved study or test names is refused, naming them**, as the Study Designer already refuses a destructive edit that would break a saved dev-bench study (review round 2, recommended).

**The prose the agent writes for a run is one file per run in the study's folder** (`embarch/studies/<slug>/runs/<run id>`), which `report.typ` includes by the run's ID, so a republish renders the same words. **A test's study lives with its test**, in `embarch/tests/<suite>/<test id>/`, and **a Test run's prose in `embarch/tests/runs/<run id>/`**, one file per requirement section the report has (review round 2, recommended).

## Open

- **Which plots Typst can draw offline.** Plot packages are normally fetched from the Typst package registry; a binary that must work offline has to vendor the ones it supports. To measure when the work starts; the prior-art survey ([09](09-trust-model.md#open)) looks at it.
- **Whether the reducer set covers the first studies.** Fixed by the BLE GATT example: rate and loss over a capture.
- **The Study Designer UI** gains host-study rows later ([host-study proposal](../../embarch-host-study-proposal.md), "What is left" item 3); nothing in the Study mode waits on it.
