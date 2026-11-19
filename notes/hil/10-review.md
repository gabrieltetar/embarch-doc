# HIL notes: review rounds

**Status:** draft, 2026-11-15.

Each round reviews the notes and [the two proposals](../../embarch-hil-proposal.md) against [the goals](00-goals.md). **An answered finding folds into the note it is about and leaves this file**; what stays is what is unanswered, each round's outcome, and its line per goal.

## Round 1 (2026-11-15)

**23 findings, then 6 more from a second pass (R25 to R30); the owner answered all but R23 and R24 in the same session.** Where each answer landed:

| Finding | Answer | Now in |
|---|---|---|
| Six verdicts; a failure charged by what the step addressed | Taken | [03](03-test.md#the-verdict) |
| A fail ends its test, an error its bench; `requires`; `stop_on_fail` | Taken; replaces "a failure ends its bench" | [03](03-test.md#a-run) |
| Measurements, from Core and from built-in reducers | Taken (reducers only, no script) | [02](02-study.md#measurements) |
| Numbers in prose checked against measurements; authorship per block | Taken (listed, not refused) | [02](02-study.md#the-report) |
| Verdict-deciding inputs confirmed by the engineer; capability provenance; `derived_from` | Taken | [03](03-test.md#the-duts-inputs) |
| A runtime safe envelope | **Declined**: safety is an authoring concern | [03](03-test.md#benches) |
| A premade suite runs without an atlas | Taken; replaces "suites live on the atlas's records" | [04](04-premade-suites.md#decided) |
| Every run listed; publishes never overwritten; the manifest hash outside the zip | Taken | [06](06-report-and-publish.md#publish) |
| `verify <zip>` | Taken | [06](06-report-and-publish.md#verify) |
| Manual verdicts through the CLI and UI only | **Declined**: MCP stays | [03](03-test.md#the-verdict) |
| The image read back before each bench; the dirty tree recorded | Taken | [03](03-test.md#a-run), [06](06-report-and-publish.md#the-audit-appendix) |
| `embarch/` split into definitions and outputs | **Deferred**: untracked until EmbArch is published and used by others | [03](03-test.md#it-grows-out-of-the-ledger) |
| A precondition per test, a reset by default | Taken | [03](03-test.md#one-test) |
| `run.json`, templates, the preview | Taken | [03](03-test.md#selecting-and-rerunning) |
| Resolution per source, the decision rule, instrument identity | Taken | [03](03-test.md#the-verdict), [06](06-report-and-publish.md#the-audit-appendix) |
| The standard's coverage; the no-certification sentence | Taken | [03](03-test.md#the-report) |
| A list of DUT shell commands that ask, in Live | **Declined**: all stay free | [05](05-live.md#reach-and-permission) |
| `via: live` on a measured atlas fact | Taken | [05](05-live.md#writing-a-finding-back) |
| A long run resumed; the host kept awake | Taken | [03](03-test.md#a-run) |
| Never edit a test to pass; a fix is a new run | Taken | [07](07-procedure-doc.md#an-outline-of-the-guide) |
| Premade tests validated against injected faults | Taken, a later phase | [04](04-premade-suites.md#decided) |
| The claim's two sentences open the guide and the proposal | Taken | [09](09-trust-model.md#the-claim) |
| Reducers and verdict rules as one crate, linked by Core and embarch-api | Taken | [02](02-study.md#measurements) |
| A requirement's verdict | **Pass when every test that ran passed**; skipped tests listed under it (narrowed 2026-11-19: a test skipped for a gap makes it `not verified`) | [03](03-test.md#the-report) |
| A contract and a fixture per reducer | Taken | [02](02-study.md#measurements) |
| A confirmation recorded with its surface | Taken | [03](03-test.md#the-duts-inputs) |
| `publish <run id>` for a Study and a Test | Taken | [06](06-report-and-publish.md#publish) |
| Confirmations in the UI only, the CLI where there is no UI | Taken | [03](03-test.md#the-duts-inputs) |
| A confirmation binds a hash and is kept by Core | Taken | [03](03-test.md#the-duts-inputs) |
| Prevention, not only detection, against a subverting agent | **Taken, widened: "plan for prevention"** | [12](12-prevention.md) |
| Prompts declare a kind; Core refuses a relayed answer to an observation or a clearance | Taken | [12](12-prevention.md#operator-prompts-by-kind) |
| No hardware call but the run's own while a run is in flight, Live reads included | Taken (the owner's own proposal) | [12](12-prevention.md#what-stays-outside-prevention-and-is-said-so) |
| Each measurement marked `bench`, `dut` or `person` | **Mark only**: any test may rest on any source | [02](02-study.md#measurements) |
| Core as the root of trust, under its own OS account | Taken | [12](12-prevention.md#the-root-of-trust-core-under-its-own-account) |
| A result inside a guard band | **inconclusive**, reason "guard band" | [03](03-test.md#the-verdict) |
| JUnit XML and OCP T&V exports; the VIF as a capability source; the Typst stack with lilaq | Taken | [06](06-report-and-publish.md), [03](03-test.md#the-duts-inputs) |
| A newcomer's first run in the guide | **Not taken**: not the BLE fixture ("EmbArch isn't" BLE-specific), and no generic one picked | |

**The goals, after round 1** (the reviewer's reading, [00](00-goals.md)):

- **G1 critical**: met with gaps; the fold into the proposal and the order were R24, answered in the owner's confirmation pass below.
- **G2 adoption**: met with gaps; a suite no longer needs an atlas, and the first hour is not yet written down anywhere.
- **G3 professional**: met with gaps; the vocabulary, the decision rule and the exports match lab practice ([11](11-prior-art.md)); what is new is claimed in [11](11-prior-art.md#what-is-new-in-embarch)'s words and no wider.
- **G4 the LLM-HIL problem**: met for the evidence **against an agent that subverts**, once [the evidence proposal](../../embarch-hil-evidence-proposal.md) is built ([12](12-prevention.md)); **the hardware outside a run rests on authoring and review alone**, by the owner's choice, and the guide says so.
- **G5 open source**: the reducer contract and suites as plain data help; **the dev container is a new step for every adopter**, round 2's adoption lens.
- **G6 clients**: met for the report, signed by Core and checkable by `verify` against a pinned key; the same hardware note as G4.
- **G7 depth**: round 2 planned below.

## Round 2 (2026-11-15)

**Five independent reviewers, one lens each**, on the tree at `1a854154`: evidence integrity, prevention and safety, adoption, lab practice, consistency with the suite. **39 ledger rows, 13 high**, some rows holding two issues the ledger merged by line; the loop's ledger is outside the repo, under `.git/embarch-review/hil-round-2/`. **The owner asked for the round to run without stopping to ask** (2026-11-15), so **every fix below is the reviewer's recommendation, applied and marked "review round 2, recommended" where it stands**, for the owner to confirm or undo.

| Theme | What changed | Now in |
|---|---|---|
| **One source of truth** | Core computes every measurement and keeps the run history; the repo's rows mirror it and lose a disagreement; retention never sweeps an entry, captures only once published | [02](02-study.md#measurements), [03](03-test.md#a-run), [06](06-report-and-publish.md#publish) |
| **`verify`** | Checks Core's signatures against a fingerprint got out of band, recomputes with the crate version the records name, checks every number in the PDF, the labels; says what it cannot recompute | [06](06-report-and-publish.md#verify) |
| **Verdicts** | Core's step outcomes mapped to the six verdicts; a guard band on both sides; runs combine by a severity order; a requirement with no test run is `not verified`; uncertainty on every measurement; calibration checked against the run's date; export mapping in which only a pass maps to a passing outcome | [03](03-test.md#the-verdict), [06](06-report-and-publish.md#the-audit-appendix) |
| **What is confirmed** | A custom test whole, by its hash, prompt kinds included; a premade one by its suite version; Core re-expands `run.json`; a measured capability runs first and the rest `requires` it | [03](03-test.md#the-duts-inputs) |
| **A person's acts** | "Relayed" decided by the token's scope, amending Core decision 105; identity routes in the person's scope; the card escapes the agent's strings and needs Core's nonce; a touch per observation or clearance; the first passkey in the elevated install; the go bound and used once; notes, adoptions and calibration dates attributed by scope | [12](12-prevention.md), [03](03-test.md#a-run) |
| **The boundary** | The repo's host-executed files read-only; the firewall out of the agent's reach; the report says what Core saw, not where the agent ran; the boundary holds only while the agent's code runs inside it | [12](12-prevention.md#a-persons-act-what-a-ui-card-can-prove-and-what-it-cannot) |
| **Safety at authoring** | A clearance prompt required between a handling prompt and an energising step, checked at definition; the card shows what Core switched on; bench boards' images read back | [12](12-prevention.md#operator-prompts-by-kind), [03](03-test.md#a-run) |
| **Observed and claimed** | Core's record separates what it observed from the build's commit and dirty state | [06](06-report-and-publish.md#the-audit-appendix) |
| **Adoption** | Unattested and attested said plainly; vocabulary rewritten; a reducer's contributor path and version; `unvalidated` premade tests; a suite version beside its commit | [12](12-prevention.md#the-root-of-trust-core-under-its-own-account), [README](README.md#vocabulary), [02](02-study.md#measurements), [04](04-premade-suites.md#decided) |
| **Consistency** | The lease handed to a run at the go; the person's setup calls admitted between benches; a run's study and prose paths; §1.1's full list; decision 96's premise; the false "a Test run holds its own lease today"; the proposals aligned | [03](03-test.md), [05](05-live.md), [07](07-procedure-doc.md), [02](02-study.md#where-its-files-live), the proposals |

**Not changed**: the part of one row asking the guide to lead with a cheapest first result, since the owner declined a walkthrough in round 1; and **a requirement passing with tests skipped for a gap**, the owner's rule, which the practice reviewer rated high for a client reading it: kept, and raised for the owner under [03](03-test.md#open)'s Open.

**The goals, after round 2** (the reviewer's reading):

- **G2, G5**: closer; the unattested path needs nothing the owner's setup has, and a contributor's reducer and test have a path. The container remains a new step for an attested report.
- **G3**: the verdict model now matches lab practice to the reviewers' reading (decision rule, guard band, uncertainty, severity order, statement of conformity).
- **G4, G6**: no high finding is left unanswered on paper; **every one rests on [the evidence proposal](../../embarch-hil-evidence-proposal.md) being built as written**, and the round-2 additions are the owner's to confirm.

### Round 2's verification round

**Three reviewers on the fix diff** (evidence, prevention, consistency): **27 findings, none high.** Fixed the same way, marked "review round 2, recommended": attested decided by a key from Core's elevated install, not by a mark; the label carries the engineer's statement of where the agent runs, and with no container the passkey; uncertainty, calibration and bootload ports among the person's declarations; later passkeys need an existing one; the nonce only the person's token obtains; the agent's own clone in the container and its definition outside the repo, instead of a list of read-only paths; the container's hardening listed; Core's own copy of the premade suites; a relayed manual verdict never rolls up; the run history keyed on the chip's hardware ID; `bench_image` on every measurement; a prose number bound to the measurement it cites; `verify` rescanning `report.typ`; the clearance rule checked by Core at re-expansion, an unclassifiable step counting as energising; the cancel always admitted; the deploy described as it is; the lease returned to the session; the proposals aligned. **Left for the owner**: Core switching outputs off before a handling prompt at run time, a runtime safety rule against the round-1 answer ([12](12-prevention.md#open)).

### Round 2's final round

**Two reviewers on the verification fixes** (one on integrity and prevention, one on consistency, lab practice and adoption), the loop's last round by its cap: **10 findings, none high.** Fixed the same way, marked "review round 2, recommended": a manual verdict is an entry in Core's run log, made through a route that records the token's scope; `bench_image` shown beside each value it touches and in the appendix, and a verdict resting on an unreleased or unverified bench board says so; bench firmware compared with the hashes the installed EmbArch release ships, so a custom test and a Study have a reference; a unit whose hardware ID read-out protection blocks is keyed on the probe's enrolment and the declared serial, and its reports say its history may be split; definitions the agent writes reach Core through embarch-api and fill the person's `embarch/` from Core's copies, since a fetch from the agent's clone carries no `embarch/`; the identity tools leaving the MCP surface, stated in the Live note, the procedure note and both proposals; one acceptance rule for both decision rules, 2 × max(w, `U`); the export rule restored to "no verdict but pass maps to a passing outcome"; the evidence proposal's amended UI decision corrected to 90; the round-2 markers added where they were missing. **The loop stops here**: its round cap, and no high finding in its last two rounds.

## Round 3 (2026-11-15)

**The owner asked the review to go on without stopping**, so round 3 read the whole design with round 2's recommendations taken as the current design, not as decisions. **Five reviewers** (evidence integrity, prevention and safety, lab practice, consistency, adoption): **about 50 findings, 7 high**, each fixed on the reviewer's recommendation and marked "review round 3, recommended".

| Theme | What changed | Now in |
|---|---|---|
| **What Core signs** | A signed record per Test run (the selection as expanded at the go, every test's status, its resume); `report-data.json`, every non-prose claim of the report, written and signed by Core at publish; the unit's segment of the run log in the zip; a log that starts anew says so; Core's signature covers what it produced, and embarch-api's files rest on `verify` | [03](03-test.md#a-run), [06](06-report-and-publish.md#publish) |
| **`verify`** | Verdicts against `report-data.json`; every selected test accounted for; citations rescanned in the sources; the PDF's other claims diffed; both exports regenerated; both log segments' chains checked | [06](06-report-and-publish.md#verify) |
| **Prevention** | An attested Core only from a signed release; firmware taken as bytes, never from a path; the call log a file of its own, failing closed; the passkey as the whole person's scope where the agent is not contained; the container statement a person's act in Core's store; an agent-flashed bench board named as such; a host study with a prompt takes the person's go and the clearance check; an action prompt's measurement must feed a limit or an `until` | [12](12-prevention.md), [02](02-study.md#how-a-study-runs-as-the-procedure-would-say-it) |
| **The boundary** | The person's `embarch/` mounted read-only into the clone under a container-owned layer; the writer of the person's `embarch/` confined; publish runs with the agent's embarch-api, so a zip is trusted through `verify`; `report.typ` compiled with a confined root | [12](12-prevention.md#a-persons-act-what-a-ui-card-can-prove-and-what-it-cannot), [06](06-report-and-publish.md#publish) |
| **Lab practice** | The standard and revision named; uncertainty per producer, derived measurements included; a premade test's default rule a guard band with w = `U`, simple acceptance's risk stated; per-verdict counts beside every combined verdict; calibration bound to the serial and certificate, checked per measurement; qualifiers kept in both exports; the person's name declared in Core | [02](02-study.md#measurements), [03](03-test.md#the-verdict), [06](06-report-and-publish.md#the-audit-appendix) |
| **Flows** | `run_test` prepares, the go starts and takes the preparing session's lease; the smoke check before a Study; `test_add` through Core's route; the CLI covers Make live; a contributor's dev Core reads a suite checkout | [03](03-test.md), [02](02-study.md), [12](12-prevention.md#the-root-of-trust-core-under-its-own-account) |
| **Adoption and consistency** | The PD partner's boards named; the example suite before the PD suite; Live's lease, `validate` and `reset_dev_bench` free; "saved bench", "live bench", "Test run" in chat; the live log a mirror of Core's call log; the proposals aligned (own clone, decision 96, embarch.md §5, Study publish's prerequisites, the manifest hash in Core's log); missing round-2 markers added | [04](04-premade-suites.md), [05](05-live.md), [README](README.md), both proposals |

### Round 3's delta round

**Three reviewers on the fix diff** (evidence, prevention, consistency): **18 findings, 2 high.** Fixed the same way: a source install never opens an attested store; the call log's fail-closed rule always admits teardown, an output switched off and a cancel, with a quota that refuses the agent's calls first; the staging folder follows no link; a registered passkey binds whatever the container statement says; an action prompt's measurement is `by: bench` and can fail; every compile of a zip's sources is confined; `report-data.json` carries the audit appendix's claims, the notes and prose adoption go through Core, the atlas's count is a labelled input; the flasher's scope is in the signed record and the call log a chain of its own; `verify` rebuilds the PDF and checks the publish's own entry against Core; an atlas fact re-verifies its zip on use; a host study takes a go when it holds a prompt; the CLI's Make live and the signed release have owners in the proposals.

### Round 3's third round

**Two reviewers on that fix diff**: **9 findings, 1 high.** Fixed the same way: a source install runs Core under the engineer's own account, so the OS keeps it out of the attested store; the fail-closed exception is a cancel and Core's own safe-off, built from the declarations, with a reserved tail and the person's recovery; the call log's head and the run's range in each signed record, its segment in the zip; `verify` check 9 compares rendered pages and admits only images drawn from the data or signed captures, and reports a Typst version it lacks as not rebuilt; the atlas's fingerprint comes from Core or the read-only mount; a host study's go is named among the person's acts, bound to the study's hash and prompt kinds; the notes' and prose's text hashes in Core's record; the revision number in `report-data.json`; a Core route for a publish's entry and the log head.

### Round 3's fourth round

**Two reviewers on that fix diff**: **9 findings, none high.** Fixed the same way: the owner's development loop stated, `deploy-core` installing a development Core in the logon session beside the stopped service, with its own store, tokens and hash check, so development never turns the attested install unattested; the safe-off covering every declared output and the teardown logged to the reserved tail; the atlas's fingerprint only from the read-only mount, never a Core's own answer; check 9's image test made mechanical (a closed list of Typst calls, numerals as text) with the Typst version and fonts pinned; check 8 split per chain; the two segments named alike everywhere; 01's runner note and the proposal's identity-tool pointer corrected.

### Round 3's fifth round

**Two reviewers on that fix diff**: **6 findings, none high.** Fixed the same way: a study's teardown, which the agent wrote, runs only while it can be logged, the safe-off in its place otherwise; which Core answers is shown on every act, the token pair picked by Core's own status, and a service start logs the time it was stopped and resets each board's last flasher to unknown; the fingerprint written to `embarch/core-fingerprint` by the elevated install; check 9 requires every text-layer glyph to be visible in the render; leftover wording aligned.

### Round 3's sixth round, the loop's last

**Two reviewers on that fix diff**: **6 findings, none high.** Fixed the same way: embarch-api and embarch-ui send the service's token pair only to a Core that signs a fresh challenge with the key whose fingerprint the elevated install recorded; `core-fingerprint` is out of the agent's reach only in the container topology, and elsewhere a fact resting on it says "fingerprint not protected here"; a repo registered later gets the file through an elevated step; check 9's visibility test made mechanical (render with and without each glyph run, a stated contrast and a minimum size); the dev workflow §4a and umbrella decision 32 amendments stated as to do once accepted. **The loop stops here, at its round cap**: six rounds, the high findings falling 7, 2, 1, 0, 0, 0; the last round's fixes are unreviewed.

## Note 13's review (2026-11-18)

**Two reviewers on [13](13-research-phase.md) and the analog-capture proposal** (facts and consistency; the trust model, lab practice and adoption against the goals): **29 findings, 9 high.** **The factual ones are fixed**: a bench study already holds a `Raw` capture open through a step's delay, with `record_checks`, so the proposal's first stage needs no suite change; Live keeps Core's capture outside a study; an odd-length read misaligns samples with no newline in it; 02's bench sentence; the evidence row's stage A; the tags 02 has; a fixture value is not in the model. **The trust-model ones went to the owner. Confirmed 2026-11-19 and folded into [13](13-research-phase.md)**: Core decides there is no DUT from its own state; a declared subject keys the run history; an `(analysis)` tag; a fixture value as a person's act. **Still recommendations under [13](13-research-phase.md#open)**, marked "note 13 review, recommended": discarding unpublished scans' captures, `by` for a relayed sample, a Study's own declarations labelled unconfirmed, and "no DUT board".

| Goal | Line |
|---|---|
| G1 | Met with named gaps: the subject's declaration, which the run history rests on, is Open |
| G2 | Met with named gaps: stage A now runs with no suite change; the per-scan cost is unmeasured |
| G3 | Met with named gaps: "no DUT" against lab usage and the retention of unpublished scans are Open |
| G4 | Met with named gaps: the four holes closed by the owner's answers of 2026-11-19, whose wording no reviewer has read yet; a Study's own declarations are still unlabelled (Open) |
| G5 | Met: the excursion counter is a reducer a contributor adds to the crate |
| G6 | Met with named gaps: the sensor answer on the DUT route is development evidence, and the proposal says so |
| G7 | Met: the bench definition reopened, its consequences carried into 02, 03 and the README |

## The owner's confirmation pass (2026-11-19)

**The owner went through every "review round 2, recommended" and "review round 3, recommended", theme by theme, then note 13's four and R23 and R24.** A marker the owner confirmed now reads "review round N, owner 2026-11-19"; where an answer changed or deferred something, the note says so in place.

| Theme | Answer |
|---|---|
| Core as the one source of truth; what Core signs, `report-data.json` included; the signed run record and resume | Confirmed |
| `verify` | **Checks 0 to 8 confirmed; check 9, the PDF rebuilt and compared page by page in pixels, cut**: the PDF is checked on its text layer, and what an image in it shows rests on embarch-api ([06](06-report-and-publish.md#verify)) |
| Verdicts | Confirmed, and **a test skipped for a gap makes its requirement `not verified`**: only a not-applicable or not-selected skip sits under a pass, which narrows the round-1 rule ([03](03-test.md#the-report)) |
| Uncertainty and the decision rule; bench-board readback and `bench_image`; the numeric-oracle rules | Confirmed |
| What is confirmed; prepare, go and lease; the refusals during a run | Confirmed |
| Prompts and safety at definition | Confirmed; **outputs switched off at run time before a handling prompt: declined**, since a "plug the cable now" prompt needs the DUT powered ([12](12-prevention.md#operator-prompts-by-kind)) |
| Who the report says did what | Confirmed |
| Identity as the person's act | **On an attested Core only**: on an unattested one the identity routes, an instrument's declarations and the setup calls between benches stay on MCP with the agent's token, labelled as the agent's; every other person's act keeps the person's surface ([12](12-prevention.md#the-root-of-trust-core-under-its-own-account)) |
| The card and the passkey | The card confirmed; **the passkey's details wait for its own phase**, marked so ([12](12-prevention.md#open)) |
| Unattested and attested | Confirmed |
| Core's install and the development loop | Confirmed, landing with the attested phase, and **changed**: the two Cores never run at once on one bench, since the shared port is the lock that keeps a development Core off the bench during attested work, and **the engineer's account may stop and start the service without elevation**; new, so round 4 reads it ([12](12-prevention.md#the-root-of-trust-core-under-its-own-account)) |
| The call log failing closed; firmware taken as bytes | Confirmed |
| The agent's container | The hardening and the firewall confirmed; **the agent's own clone and the `embarch/` flow are decided in the standalone pass**, marked so ([12](12-prevention.md#open)) |
| Exports and publish; files and suites; Live | Confirmed |
| R23, the smaller points | All four taken: the Live lease released after a stated idle time ([01](01-modes.md#the-lease)); Core refuses `instrument_exchange` outside a run ([05](05-live.md#reach-and-permission)); several units as later work ([03](03-test.md#open)); the guide opens with a glossary ([07](07-procedure-doc.md#an-outline-of-the-guide)) |
| R24, the order | Taken: the file shapes are fixed as a doc before Study publish ([the proposal](../../embarch-hil-proposal.md#order)) |
| Note 13's four | "No DUT board", `by` following a relayed tap's declared origin, and a Study's own declarations labelled unconfirmed: confirmed. **A scan's captures may be discarded by either token**, the discard and its token's scope kept in the history ([13](13-research-phase.md#many-scans-few-reports)) |

**The order and who builds it** (owner, 2026-11-19): **the first milestone is an unattested Study publish**: the file shapes, the shared crate, Core signing its records and keeping its run log under the engineer's own account, then publish and `verify` on the BLE GATT study. **Core's own account and the `deploy-core` change come later**, as the attested phase. **HIL runs alongside the atlas rework**, and only Live's write-back waits on it. **The fleet writes the code that needs no hardware; interactive sessions do every bench run** ([the proposal](../../embarch-hil-proposal.md#order)).

## Still unanswered

- **The passkey's details**, until its phase, and **the agent's own clone and the `embarch/` flow**, until the standalone pass ([12](12-prevention.md#open)).
- **Switching between the Cores without elevation**: the owner's answer of 2026-11-19, not yet read by a reviewer.

## Open

- **Round 4**: a full round on the design as confirmed, with **the five lenses plus buildability** (whether each piece can be built and tested in its own repo, and what is heavier than a first version needs), reading note 13 and the 2026-11-19 changes with the rest. **Its findings go to the owner before anything is folded**, and nothing lands marked "recommended" again (owner, 2026-11-19).
