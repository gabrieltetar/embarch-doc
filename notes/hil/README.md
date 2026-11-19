# notes/hil: running hardware-in-the-loop from an agent

The research behind [embarch-hil-proposal.md](../../embarch-hil-proposal.md): one procedure telling an agent how to run hardware-in-the-loop (HIL) in three modes. Gathered in an interview with the owner on 2026-11-15. **Every answer recorded in these files is the owner's, 2026-11-15, unless it sits under Open.**

## Files

| File | Subtopic |
|---|---|
| [00-goals.md](00-goals.md) | **The goals every review is held to**, in the owner's words, and what each asks of a review |
| [01-modes.md](01-modes.md) | The three modes, what separates them, how an agent picks one, who may run them, the lease |
| [02-study.md](02-study.md) | A Study: one bench, a measurement, a report |
| [03-test.md](03-test.md) | A Test: suites, benches, the Core-run sequence, verdicts, the ledger it grows out of |
| [04-premade-suites.md](04-premade-suites.md) | Test suites shipped with EmbArch, runnable without an atlas, and what HIL takes from the atlas when there is one |
| [05-live.md](05-live.md) | Live access: instant reads and actions on the DUT and bench boards, and writing findings back |
| [06-report-and-publish.md](06-report-and-publish.md) | The report and the published zip, shared by Study and Test |
| [07-procedure-doc.md](07-procedure-doc.md) | The deliverable: a suite guide plus a thin skill, and the gaps in today's agent docs it closes |
| [08-existing-pieces.md](08-existing-pieces.md) | What already exists that each mode reuses, and what is missing |
| [09-trust-model.md](09-trust-model.md) | What the mechanisms must add up to: the agent outside the evidence chain, and which layer enforces each guarantee |
| [10-review.md](10-review.md) | Review rounds: what is still unanswered, and each round's line per goal |
| [11-prior-art.md](11-prior-art.md) | What exists before EmbArch claims anything as new: agent-driven HIL, evidence against fabricated numbers, approval integrity, classical HIL frameworks, formats |
| [12-prevention.md](12-prevention.md) | Prevention against an agent that deliberately subverts the trust model: Core as the root of trust, signed records, a person's acts by passkey |
| [13-research-phase.md](13-research-phase.md) | **A project's first research pass**: no fourth mode, a dev kit as the DUT before custom hardware, a bench with no DUT, who samples decides `by`, and the detector being researched |

## Vocabulary

These words mean exactly this in every file here. Where one word names two things, the second is written out in full (review round 2).

- **Bench**: zero or one DUT (none only for a Study or Live, [13](13-research-phase.md#a-bench-with-no-dut), owner, 2026-11-18), zero or one dev bench, and any number of **bench boards** (the dev bench, a USB PD partner, ...) and **instruments** (an electronic load, a supply). Described as a **saved bench** (parts, cables, configs) in the firmware repo's `embarch/topologies/` ([embarch-ui decision 73](../../embarch-ui/decisions/saved-benches.md)). The description does not change with the probes and ports; **Make live** binds the real ones by live enrolment ([decision 90](../../embarch-ui/decisions/bench-live.md)). **The bench lease** is Core's lock on all of it; **`by: bench`** on a measurement means a bench board or an instrument measured it. Never "bench" alone for one board; **"saved bench" for the description and "live bench" for the bound one** wherever the difference matters (review round 3, recommended).
- **Study** (the mode): a custom, almost scientific question answered by measurement, on **exactly one bench**. Either runner: a dev-bench study or a host study. **A study** (the file) is the steps a runner executes; a test runs one, so "a test's study" is the file, not the mode.
- **Test** (the mode, capitalised): technical conformance with a verdict, as pre-compliance evidence. A **test suite** (USB PD R3.2 is one) holds **tests** (lower case: one test); a Test run selects some of them; the tests are grouped by bench; a run spans **one or more benches**. The hardware test ledger's "tests" become these ([03](03-test.md#it-grows-out-of-the-ledger)); a firmware's unit tests are never called tests here without "unit". **Where capitals cannot carry the difference** (chat, tool names, file names), the mode is "Test mode" or "a Test run" and one test is "a test"; the `test_*` tools act on tests and test plans, `run_test` prepares a Test run (review round 3, recommended).
- **Run**: one execution, of a study or of a Test selection, with an id in Core's run log. A Test run holds one study run per test and per pass of its run count.
- **Live** (the mode): an instant read or action on the DUT or a bench board, during a development session. Not Make live, which is the UI's step binding a saved bench to real probes.
- **Premade suite**: a test suite shipped with EmbArch as plain data, runnable without an atlas. **Custom suite**: one the engineer and agent write in the firmware repo.
- **Measurement**: a named value with a unit, a resolution, an uncertainty, who measured it and the file and rows it came from, computed by Core, at step time or through the shared crate's built-in reducers as each test or study ends ([02](02-study.md#measurements)).
- **Verdict**: one of pass, fail, error, inconclusive, skipped, cancelled, decided by code ([03](03-test.md#the-verdict)); a requirement may also be **not verified**.
- **Resolved run** (`run.json`): a Test selection with every test expanded and every input substituted, hashed, the unit of reproducibility ([03](03-test.md#selecting-and-rerunning)).
- **A person's act**: an act only the person may make (a confirmation, the go, an observation or clearance answer, a manual verdict, an identity declaration, a no-DUT bench's subject or a fixture's reference value ([13](13-research-phase.md), owner, 2026-11-19)), made with the person's token ([12](12-prevention.md)).
- **Attested**, **unattested**: whether a run's records were signed by a Core under its own account ([12](12-prevention.md#the-root-of-trust-core-under-its-own-account)).
- **Publish**: turning a finished run into one zip holding a PDF report and every file behind it.
