# Proposal: running hardware-in-the-loop from an agent — Study, Test and Live

**Status:** proposal, 2026-11-15.

Spans `embarch-atlas`, `embarch-study-designer`, `embarch-core`, `embarch-api`, `embarch-ui`, `embarch-umbrella` and this repo, which is why it sits at the root ([DOC-PROTOCOL.md](DOC-PROTOCOL.md) §3). **One procedure tells an agent how to run hardware-in-the-loop, in three modes.** The research and every answer behind it are in [notes/hil/](notes/hil/README.md), gathered with the owner on 2026-11-15; this file keeps the design and the work, and links to the notes for the reasons.

## The three modes

| Mode | Purpose | Benches | Output |
|---|---|---|---|
| **Study** | A custom, almost scientific question, answered by measurement | Exactly one | A published report |
| **Test** | Technical conformance: selected tests of a suite such as USB PD R3.2 | One or more, one after another | A verdict per test, coverage, a published report |
| **Live** | An instant read or action during development | The DUT and its bench boards | An answer, a live-log line, a fact written back to the atlas |

**A bench** is one DUT, zero or one dev bench, and any companion boards and instruments, described as a saved bench and bound to real probes by Make live ([vocabulary](notes/hil/README.md#vocabulary)). **Purpose separates the modes**, and a spec named in a request makes it a Test ([how an agent picks](notes/hil/01-modes.md#how-an-agent-picks-a-mode)). **Interactive sessions only**: the fleet stays off hardware. **Every mode holds the bench lease**; a Test run holds its own, and a Study run will too once Core can hold one for a run.

## The design in one screen

- **Study** ([notes](notes/hil/02-study.md)): either runner. Saved in the firmware repo's `embarch/studies/<slug>/` with its own `report.typ`, free in shape; every number in the report comes from the run's files.
- **Test** ([notes](notes/hil/03-test.md)): **a test is a study plus verdict rules** (requirement IDs, revision range, bench and config, run count, numeric limits). **Core runs a resolved Test**, so it survives the session: embarch-api resolves the selection and sends it, since Core never reads a firmware repo. Tests group by bench, an operator prompt sits between benches, a smoke check runs before each one, and **a failure ends its bench and the run goes on to the next.** **Verdicts are decided by code**: Core parses numbers at step time, and a person may enter a verdict as theirs. **The agent never decides a verdict and never answers a prompt.** **EmbArch Test grows out of the hardware test ledger** and replaces it.
- **Premade suites** ([notes](notes/hil/04-premade-suites.md)): shipped upstream **in the atlas, on its requirement records**, IDs only and no compliance test ID, procedures written from the requirement, one suite per standard with revision ranges per test. Mostly black-box, with **named DUT hooks** mapped per project to a shell command or an operator prompt. **DUT inputs come from the atlas first, then from the engineer or agent, and are saved in the test plan.**
- **Live** ([notes](notes/hil/05-live.md)): reads, resets and any shell command on the DUT or a bench board are free. Flashing and reads that change state ask. **The atlas is optional**: with one, reads come decoded and a finding is written back as a `measured` fact with its receipt. Every call goes in `embarch/live/`. **A result about to be cited is redone as a Study or a Test.**
- **Publish** ([notes](notes/hil/06-report-and-publish.md)): an explicit step producing **one zip** (PDF report, study files, every capture, operator notes, hash manifest) in a configured local folder. **embarch-api renders the PDF with Typst built in**, and appends **an audit appendix no study can leave out.**
- **The procedure itself** ([notes](notes/hil/07-procedure-doc.md)): `suite/hil-guide.md`, plus a thin `embarch-hil` skill shipped with embarch-api.

## The work, by sub-project

What exists and what does not: [notes/hil/08-existing-pieces.md](notes/hil/08-existing-pieces.md).

| Sub-project | Work |
|---|---|
| `embarch-atlas` | **The rework, drafted first in its own notes by the owner.** HIL needs from it: requirement IDs stable across revisions, a test record on a requirement, suite bench descriptions, applicability, the capabilities it decodes from a build, and a write-back verb for a live finding ([the list](notes/hil/04-premade-suites.md#what-the-hil-side-needs-from-the-atlas-rework)) |
| `embarch-study-designer` | Suite and test types: a study plus verdict rules, revision range, bench and config, run count, hooks. A declared numeric parse on a host step |
| `embarch-core` | The number parsed at step time. **A Test route**: a resolved run, grouped by bench, prompts between benches, the smoke check, the same-DUT check, failure per bench, cancel. **A lease held by a run.** Retention that keeps a run's studies together |
| `embarch-api` | `study_publish`: Typst, the PDF, the zip, the audit appendix. Test selection and resolution, `run_test`, run status. **The ledger grown into Test**: `embarch/tests/`, `test_show`, `test_pending`, `test_add`, with test plans holding DUT inputs and hook mappings. The live-log writer. The `hil` skill |
| `embarch-ui` | Host studies saved in `embarch/studies/`. A suite's benches copied into `embarch/topologies/`. A Test run view, later |
| `embarch-umbrella` | `embarch init` installs the `embarch-hil` skill beside the MCP server |
| `embarch-doc` | `suite/hil-guide.md`. [agent-guide.md](suite/agent-guide.md) §1.1: `reset`, `signal_exchange` and `shell_run` move to allow |

## Order

1. **The atlas rework**, in its own notes (the owner's call: start there).
2. **Study publish**, on the BLE GATT data-acquisition path, which already runs on hardware; Tests reuse the same publish.
3. **Recommended:** Live: the guide's Live section, the live log, the permission lists, then the write-back once the atlas has its verb.
4. **Recommended:** Test: the numeric parse and a first host study on the real PD bench (the [host-study proposal](embarch-host-study-proposal.md)'s own first item), then the Core route and a custom suite, then the first premade suite.
5. `suite/hil-guide.md` grows a section per mode as each lands, rather than waiting for all three.

## Open questions

The full lists close each note; the ones that block a phase:

- **The order of Live and Test** after Study publish (above).
- **The inventory of what exists** ([08](notes/hil/08-existing-pieces.md)) was taken from the docs; each row a phase relies on is checked against its repo when that phase starts.

**Fold:** each phase moves its part into the owning sub-project's docs as it is accepted and deletes it here; the notes go with it. This file is deleted once nothing in it is still proposed.
