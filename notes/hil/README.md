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

## Vocabulary

These words mean exactly this in every file here.

- **Bench**: one DUT, zero or one dev bench, and any number of companion boards (a USB PD partner, ...) and instruments (an electronic load, a supply). Described as a **saved bench** (parts, cables, configs) in the firmware repo's `embarch/topologies/` ([embarch-ui decision 73](../../embarch-ui/decisions/saved-benches.md)). The description does not change with the probes and ports; **Make live** binds the real ones by live enrolment ([decision 90](../../embarch-ui/decisions/bench-live.md)).
- **Study**: a custom, almost scientific question answered by measurement, on **exactly one bench**. Either runner: a dev-bench study or a host study.
- **Test**: technical conformance with a verdict. A **test suite** (USB PD R3.2 is one) holds **tests**; a run selects some of them; the tests are grouped by bench; a run spans **one or more benches**.
- **Live**: an instant read or action on the DUT or a bench board, during a development session.
- **Premade suite**: a test suite shipped with EmbArch as plain data, runnable without an atlas. **Custom suite**: one the engineer and agent write in the firmware repo.
- **Measurement**: a named value with a unit, a resolution and the file and rows it came from, computed by Core at step time or by embarch-api's built-in reducers after the run ([02](02-study.md#measurements)).
- **Verdict**: one of pass, fail, error, inconclusive, skipped, cancelled, decided by code ([03](03-test.md#the-verdict)).
- **Resolved run** (`run.json`): a Test selection with every test expanded and every input substituted, hashed, the unit of reproducibility ([03](03-test.md#selecting-and-rerunning)).
- **Publish**: turning a finished run into one zip holding a PDF report and every file behind it.
