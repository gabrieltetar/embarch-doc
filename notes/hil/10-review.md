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
| A requirement's verdict | **Pass when every test that ran passed**; skipped tests listed under it | [03](03-test.md#the-report) |
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

- **G1 critical**: met with gaps; the fold into the proposal and the order are R24 below.
- **G2 adoption**: met with gaps; a suite no longer needs an atlas, and the first hour is not yet written down anywhere.
- **G3 professional**: met with gaps; the vocabulary, the decision rule and the exports match lab practice ([11](11-prior-art.md)); what is new is claimed in [11](11-prior-art.md#what-is-new-in-embarch)'s words and no wider.
- **G4 the LLM-HIL problem**: met for the evidence **against an agent that subverts**, once [the evidence proposal](../../embarch-hil-evidence-proposal.md) is built ([12](12-prevention.md)); **the hardware outside a run rests on authoring and review alone**, by the owner's choice, and the guide says so.
- **G5 open source**: the reducer contract and suites as plain data help; **the dev container is a new step for every adopter**, round 2's adoption lens.
- **G6 clients**: met for the report, signed by Core and checkable by `verify` against a pinned key; the same hardware note as G4.
- **G7 depth**: round 2 planned below.

## Unanswered

### R23 — Smaller points

- **An idle Live lease**: 900 s renewed by the MCP server's timer holds the bench for as long as the session lives. Release after a stated idle time.
- **Instruments in Live**: 05 excludes them, while `instrument_exchange` is an MCP tool today. Procedure-only; say so, or gate it.
- **Several units**: a design-validation campaign runs one plan on three units. One run per unit, and a report over runs, later.
- **The glossary**: HIL test, test suite, test plan, run, resolved run, verdict, measurement. "Test" also names the ledger's tests and unit tests.

### R24 — The proposal and its order

The proposal's order predates round 1. **Recommended:** its one-screen design and its work table take round 1's answers (done in round 1), and **its order puts the file shapes (verdicts, `measurements.json`, `run.json`) before Study publish**, so the Study zip is not reshaped when Test lands.

## Round 2 (2026-11-15)

**Five independent reviewers, one lens each**, on the tree at `1a854154`: evidence integrity, prevention and safety, adoption, lab practice, consistency with the suite. **39 ledger rows, 13 high**, some rows holding two issues the ledger merged by line; the loop's ledger is outside the repo, under `.git/embarch-review/hil-round-2/`. **The owner asked for the round to run without stopping to ask** (2026-11-15), so **every fix below is the reviewer's recommendation, applied and marked "review round 2, recommended" where it stands**, for the owner to confirm or undo.

| Theme | What changed | Now in |
|---|---|---|
| **One source of truth** | Core computes every measurement and keeps the run history; the repo's rows mirror it and lose a disagreement; retention never sweeps an entry, captures only once published | [02](02-study.md#measurements), [03](03-test.md#a-run), [06](06-report-and-publish.md#publish) |
| **`verify`** | Checks Core's signatures against a fingerprint got out of band, recomputes with the crate version the records name, checks every number in the PDF, the labels; says what it cannot recompute | [06](06-report-and-publish.md#verify) |
| **Verdicts** | Core's step outcomes mapped to the six verdicts; a guard band on both sides; runs combine by a severity order; a requirement with no test run is `not verified`; uncertainty on every measurement; calibration checked against the run's date; export mapping that never reads green | [03](03-test.md#the-verdict), [06](06-report-and-publish.md#the-audit-appendix) |
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

## Still unanswered after round 2

- **R23** and **R24**, above.
- **Every "review round 2, recommended"** in the notes, for the owner to confirm or undo.

## Open

- **Round 3**: a verify round of one reviewer on the round-2 fixes, and a full round once the owner has confirmed them.
