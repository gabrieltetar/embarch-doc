# Proposal: running hardware-in-the-loop from an agent — Study, Test and Live

**Status:** proposal, 2026-11-15.

Spans `embarch-atlas`, `embarch-study-designer`, `embarch-core`, `embarch-api`, `embarch-dev-bench`, `embarch-ui`, `embarch-umbrella` and this repo, which is why it sits at the root ([DOC-PROTOCOL.md](DOC-PROTOCOL.md) §3). **One procedure tells an agent how to run hardware-in-the-loop, in three modes.** The research and every answer behind it are in [notes/hil/](notes/hil/README.md), gathered with the owner on 2026-11-15 and reviewed in round 1 the same day ([10-review.md](notes/hil/10-review.md)); this file keeps the design and the work, and links to the notes for the reasons.

## The three modes

| Mode | Purpose | Benches | Output |
|---|---|---|---|
| **Study** | A custom, almost scientific question, answered by measurement | Exactly one | A published report |
| **Test** | Technical conformance: selected tests of a suite such as USB PD R3.2 | One or more, one after another | A verdict per test, coverage, a published report |
| **Live** | An instant read or action during development | The DUT and its bench boards | An answer, a live-log line, a fact written back to the atlas |

**A bench** is zero or one DUT (none only for a Study or Live, [13](notes/hil/13-research-phase.md)), zero or one dev bench, and any companion boards and instruments, described as a saved bench and bound to real probes by Make live ([vocabulary](notes/hil/README.md#vocabulary)). **Purpose separates the modes**, and a spec named in a request makes it a Test ([how an agent picks](notes/hil/01-modes.md#how-an-agent-picks-a-mode)). **Interactive sessions only**: the fleet stays off hardware. **Every mode holds the bench lease**; a Test run holds its own, and a Study run will too once Core can hold one for a run.

## What it is held to

**The goals** are the owner's, in [notes/hil/00-goals.md](notes/hil/00-goals.md); every review is judged against them. **The trust model** ([09](notes/hil/09-trust-model.md)) is what they add up to, in two sentences:

- **No number, verdict or identity in a published report depends on the agent having told the truth; every sentence the agent wrote is labelled as its own.**
- **The agent does to the hardware only what the engineer allowed**: a study or a test written in a file the engineer can read before it runs, and previewed before a Test starts, or a Live action on the free list; every call is logged.

**The agent is outside the evidence chain**, and **[embarch-hil-evidence-proposal.md](embarch-hil-evidence-proposal.md) holds that against an agent that deliberately subverts it**: Core under its own account signs every record, the agent runs in a dev container, and the person's acts are made where it cannot reach. Every measurement, verdict and identity in a published report is produced by versioned code from the run's files or attested by a named person; the agent plans, authors, operates and interprets, and every sentence it wrote is labelled as its own. **Hardware safety is an authoring concern**: what a study or test puts on the DUT is reviewed when it is written, and a Test shows it before the go; no envelope is enforced at run time.

## The design in one screen

- **Study** ([notes](notes/hil/02-study.md)): either runner. Saved in the firmware repo's `embarch/studies/<slug>/` with its own `report.typ`, free in shape. **Measurements are named values** with a unit, a resolution, an uncertainty, who measured them and their source rows, **all computed by Core**, at step time or through **the shared crate's built-in reducers** as each test ends, in one `measurements.json` that limits, the report, the prose and the agent all read. **The run's files are the numeric oracle**: a number in prose or in the PDF that matches no measurement is listed in the appendix, `verify` rechecks it on the PDF, and each prose block names its author.
- **Test** ([notes](notes/hil/03-test.md)): **a test is a study plus verdict rules** (requirement IDs, revision range, bench and config, a precondition defaulting to a reset before every test, `requires`, run count, limits on measurements wider than their uncertainty; a guard band on either side of a limit reads inconclusive; verdicts combine by a stated severity order). **Six verdicts, decided by code**: pass, fail, error, inconclusive, skipped, cancelled; a failure is charged by what the step addressed, so a lost bench port is an error, not a DUT fail. **A fail ends its test, an error its bench.** **Core runs `run.json`**, the resolved run, hashed, so a run survives the session; the engineer sees a preview and gives the go. A smoke check before each bench **reads the DUT's and every bench board's image back through the probe**. **Every input that decides a verdict is proposed by the agent and confirmed by the engineer**, a custom test as a whole by its hash, each capability with its provenance. **The agent never decides a verdict and never answers a prompt on its own**; it may relay the person's answer to a setup or action prompt, never to an observation or a clearance. A long run resumes as a new run of the pending rest. **EmbArch Test grows out of the hardware test ledger** and replaces it.
- **Premade suites** ([notes](notes/hil/04-premade-suites.md)): **plain data shipped with EmbArch, runnable with no atlas**; an atlas adds requirement text and decoded capabilities. IDs only and no compliance test ID, procedures written from the requirement, one suite per standard with revision ranges per test, templates expanded at resolution. Mostly black-box, with **named DUT hooks**. **Each premade test ships evidence that it can fail**, against faults the PD partner injects.
- **Live** ([notes](notes/hil/05-live.md)): reads, resets and any shell command on the DUT or a bench board are free. Flashing and reads that change state ask. **The atlas is optional**: with one, reads come decoded and a finding is written back as a `measured` fact with its receipt and `via: live`, answered as development evidence. Every call goes in `embarch/live/`. **A result about to be cited is redone as a Study or a Test.**
- **Publish** ([notes](notes/hil/06-report-and-publish.md)): an explicit step producing **one zip** (PDF, study files, `run.json`, `measurements.json`, every capture raw and rendered, operator notes, hash manifest) in a configured local folder; **never overwritten**, a republish is `-r2`. **The report lists every run of the test on that image**, published or not; a Test's counts the standard's coverage and says it is not a certification. **embarch-api renders the PDF with Typst built in** and appends **an audit appendix no study can leave out.** **`embarch-api verify <zip>`** recomputes every measurement and verdict from the raw captures, so a reader checks the report without trusting the agent or the machine.
- **The procedure itself** ([notes](notes/hil/07-procedure-doc.md)): `suite/hil-guide.md`, opening with the trust model and naming every procedure-only rule, plus a thin `embarch-hil` skill shipped with embarch-api.

## The work, by sub-project

What exists and what does not: [notes/hil/08-existing-pieces.md](notes/hil/08-existing-pieces.md).

| Sub-project | Work |
|---|---|
| `embarch-atlas` | **The rework: [embarch-atlas-planes-proposal.md](embarch-atlas-planes-proposal.md)**, research in [notes/atlas/](notes/atlas/README.md). HIL takes from it, when present: requirement IDs stable across revisions, the join from a suite's test to its requirement record, applicability from the standard, the capabilities it decodes from a build, the unit a run ran on, and a write-back verb with `via` ([the list](notes/hil/04-premade-suites.md#what-the-hil-side-needs-from-the-atlas-rework)) |
| `embarch-study-designer` | Suite and test types: a study plus verdict rules, revision range, bench and config, precondition, `requires`, run count, hooks, `derived_from`. Declared measurements: a numeric parse on a host step, derived measurements by reducer, a resolution per source. **The reducers and the verdict rules, one crate** in the host-only half, linked by Core and embarch-api |
| `embarch-core` | The number parsed at step time; each test judged as it ends, through the shared crate. **A Test route** running `run.json`: grouped by bench, prompts between benches, the smoke check with the image readback and `*IDN?`, the same-DUT check, preconditions, the six verdicts with failures charged by what a step addressed, a fail ending its test and an error its bench, `stop_on_fail`, cancel. **A lease held by a run.** Retention that keeps a run's captures together, never sweeps them before the run is published, and never sweeps its run-log entry. An interrupted run's verdicts kept; the host kept awake under a run |
| `embarch-api` | Resolution into `run.json` with the definitions it came from. `publish`: Typst, the PDF, the zip, revisions, the audit appendix, the numeric-oracle listing, authorship. **`verify`.** Test selection, resolution into `run.json`, the preview, `run_test`, run status, resume. **The ledger grown into Test**: `embarch/tests/`, `test_show`, `test_pending`, `test_add`, with test plans holding confirmed DUT inputs and hook mappings with their provenance, every run listed, the rows a mirror of Core's run log, which holds each manifest hash. The live-log writer. **A CLI verb making a saved bench live**, as the UI's Make live does, with the person's token, so a Test needs no UI. The `hil` skill |
| `embarch-dev-bench` | Each bench board's idle command, for the default precondition. The PD partner's fault-injection commands, for validating premade tests; its Source_Capabilities capture, for a measured capability |
| `embarch-ui` | Host studies saved in `embarch/studies/`. A suite's benches copied into `embarch/topologies/`. **[Decision 96](embarch-ui/decisions/bench-configs.md) amended**: renaming or deleting a config a saved study or test names is refused ([02](notes/hil/02-study.md#where-its-files-live)). A Test run view, later |
| `embarch-umbrella` | `embarch init` installs the `embarch-hil` skill beside the MCP server |
| `embarch-doc` | `suite/hil-guide.md`. [agent-guide.md](suite/agent-guide.md) §1.1: `reset`, `signal_exchange`, `mem_read`, `core_state`, `bench_exchange`, `validate`, `reset_dev_bench` and the three lease tools move to allow; the atlas's tools get a list of their own; the identity tools leave it and the MCP surface, becoming the person's ([the evidence proposal](embarch-hil-evidence-proposal.md)) |

## Order

1. **The atlas rework**, in [its own proposal](embarch-atlas-planes-proposal.md) (the owner's call: start there).
2. **Study publish**, on the BLE GATT data-acquisition path, which already runs on hardware; Tests reuse the same publish. **It needs, before it lands**: the shared crate's reducers linked by Core, and Core's signed records and run log, the [evidence proposal](embarch-hil-evidence-proposal.md)'s steps 1 and 2 (scoped tokens, Core's own account and store, then signing), so the first published zip is already signed and verifiable.
3. **Live**: the guide's Live section, the live log, the permission lists, then the write-back once the atlas has its verb.
4. **Test**: the numeric parse and a first host study on the real PD bench (the [host-study proposal](embarch-host-study-proposal.md)'s own first item), then the Core route and a custom suite, then the first premade suite.
5. `suite/hil-guide.md` grows a section per mode as each lands, rather than waiting for all three, and splits into one file per mode if it outgrows the studies guide (about 23 KB).

## Open questions

The full lists close each note; what is left is measured later or is the atlas rework's call. The ones that touch every phase:

- **The inventory of what exists** ([08](notes/hil/08-existing-pieces.md)) was taken from the docs; each row a phase relies on is checked against its repo when that phase starts.
- **The order** ([10-review.md](notes/hil/10-review.md) R24). Recommended: the file shapes (verdicts, `measurements.json`, `run.json`) fixed as a doc before Study publish, so the Study zip is not reshaped when Test lands.

**Fold:** each phase moves its part into the owning sub-project's docs as it is accepted and deletes it here; the notes go with it. This file is deleted once nothing in it is still proposed.
