# HIL notes: the Test mode

**Status:** draft, 2026-11-15.

## What a Test is

**Technical conformance with a verdict.** A **test suite** (USB PD R3.2 is one) holds an exhaustive set of **tests**; the engineer or agent **selects** the tests to run. A suite's tests are **grouped by bench**, so one run can span **one or more benches**, one after another. A suite is **premade** (shipped upstream with the atlas, [04-premade-suites.md](04-premade-suites.md)) or **custom** (written in the firmware repo by the engineer and agent). **A custom suite reuses a premade test by copying it into the firmware repo and editing it freely**; the copy keeps no link back upstream.

## One test

**A test is a study plus verdict rules; there is no new step format.** It carries:

- the **study** it runs, a host study or a dev-bench study;
- the **requirement IDs** it checks, and the **revision range** of the spec it applies to;
- the **bench** it needs, and the **config** of that bench, by name;
- a **run count**, default 1. The verdict is a pass only if every run passes; a flaky behaviour gets a count above 1 in its own test;
- **limits** on the numbers Core parses out of replies.

## The verdict

**Decided by code, never by the agent.** Today's marker outcomes stay (a host study's `until` seen is a pass, `refused_on` a fail, [embarch-core decision 95](../../embarch-core/decisions/host-study.md)), and **declared numeric limits** are added: a voltage, a current or a time within a min and a max. **A person may enter a verdict by hand, and it is recorded as theirs.**

**Core parses the number at step time.** A host-study step declares a pattern and a unit; Core records the number beside the raw reply in `events.json`. This is the "declared numeric parse" the [host-study proposal](../../embarch-host-study-proposal.md) left for later ("What is left", item 2).

## Benches

- **A suite ships each bench as a saved-bench description**: parts, cables and configs, no probe serials. **Selecting a suite copies its benches into the firmware repo's `embarch/topologies/`**, where the project can edit them, which keeps the owner's 2026-11-01 call that saved benches live in the firmware repo ([embarch-ui decision 73](../../embarch-ui/decisions/saved-benches.md)).
- **Setting a bench up is a human step in the Topology view**: open the saved bench, wire it, **Make live**, which applies the declarations and proposes each probe binding ([decision 90](../../embarch-ui/decisions/bench-live.md)).
- **A config change inside one bench is a `Prompt` naming the config**, which host studies already do ([embarch-study-designer decision 88](../../embarch-study-designer/decisions/host-prompt.md); [embarch-ui decision 99](../../embarch-ui/decisions/operator-prompt.md)).
- **The same DUT unit moves from bench to bench.** The runner checks its hardware ID on every bench and refuses a different unit.

## A run

**Core runs it, so a run survives the session that started it.** Core never reads a firmware repo, so **embarch-api resolves the selection** (tests, their studies, benches, limits, from the suite and the test plan) **and sends the resolved run to Core**. Core runs it and keeps the results; embarch-api writes the result rows when it reads them back, as the ledger already does for a study ([embarch-api decision 98](../../embarch-api/decisions/ledger.md)).

1. **Group by bench.** All selected tests for bench A run, then bench B, and so on. **One lease for the whole run, held by the run itself.**
2. **Between benches, an operator prompt** says which saved bench to set up, with what is missing. **Only the person answers a prompt**: in the UI's prompt modal, or by telling the agent, which relays their exact words with `answer_prompt`. **The agent never answers one on its own.**
3. **Before a bench's first test, a smoke check**: the topology the bench needs is live, the DUT's and every board's identity validates, each companion board answers a hello, each instrument answers an identity query. A failing check names the piece and runs no test on that bench.
4. **A failure stops what depends on it.** If step 2 of a bench fails, continuing that bench makes no sense, so cancellation works per bench and per step. **A failure ends its own bench and the run goes on to the next bench; a cancel ends the whole run.** The study in flight always runs its teardown, as host studies already do.
5. **Watching a run.** One `test_status` call answers the current bench, the current test, the verdicts so far, and a waiting prompt with its text, from any session; each study's own events stay available underneath.
6. **Retention.** A Test run's studies count as one unit in Core's retention sweep (`EMBARCH_STUDY_RESULTS_KEEP`, 50 runs), are swept together, and **are never swept while the run is unpublished.**
7. **Sequential only.** Two benches acting at the same moment are out of scope; Core runs one study at a time and a host study cannot drive the dev bench.

## Selecting and rerunning

- **Selection narrows by applicability, then picks.** The runner keeps the tests that apply to the DUT's role and declared features and to the benches that exist, then the engineer or agent picks by test ID or tag.
- **A selection is saved as a test plan** in the firmware repo, to rerun it ("our PD regression set").

## The DUT's inputs

A test may need two kinds of input about the DUT:

- **Capabilities**: its role (source, sink, dual-role), its PDOs, which swaps it supports, and the like. They decide applicability.
- **Hooks**: a named action the DUT must take itself, such as `dut.request_pr_swap` for a swap the DUT initiates. **A hook maps to a DUT shell command or to an operator prompt** ("press the button"); **a hook with no mapping skips its test, and the coverage list says why.**

**The atlas answers first, then the engineer or agent is asked, and every answer is saved in the test plan**, so it is asked once per project rather than once per run. With an atlas, the capabilities come from what it decodes out of the build (a USB PD PDO is already decoded, [atlas design](../../embarch-atlas/design.md#firmware-configuration-against-a-standard)) and from `atlas.toml`'s declared values. **A hook mapping is proposed by the agent and confirmed by the engineer**: the agent finds candidate commands in the firmware's shell (its source, or a live `help`), and the mapping lands in the plan once the engineer says yes.
- **The rerun rule is today's ledger rule**: a test is pending when the DUT image hash differs from its last pass, or it never ran, failed, or its commit was rebased away.

## It grows out of the ledger

**EmbArch Test replaces the hardware test ledger by growing out of it** ([embarch-api decision 98](../../embarch-api/decisions/ledger.md), [tools](../../embarch-api/interfaces/tools-ledger.md)). The ledger's three files and its computed pending view are kept and renamed: **`embarch/tests/` holds the custom suites, the test plans and the results, and `ledger_show`, `ledger_pending` and `ledger_add` become `test_show`, `test_pending` and `test_add`**; `tests.toml`'s `needs` becomes a bench; rows a person entered by hand stay possible. **The ledger is not yet verified on a bench**, so nothing about it is a measurement yet.

## The report

**Published the same way as a Study** ([06-report-and-publish.md](06-report-and-publish.md)), **organised by requirement**: each verdict cites the run behind it. **It always lists every applicable test that did not run, and why** (not selected, bench missing, cancelled, stopped by an earlier failure), so a partial run never reads as full conformance.

## Open

- Nothing left open here as of 2026-11-15.
