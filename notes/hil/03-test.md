# HIL notes: the Test mode

**Status:** draft, 2026-11-15.

## What a Test is

**Technical conformance with a verdict.** A **test suite** (USB PD R3.2 is one) holds an exhaustive set of **tests**; the engineer or agent **selects** the tests to run. A suite's tests are **grouped by bench**, so one run can span **one or more benches**, one after another. A suite is **premade** (shipped with EmbArch, [04-premade-suites.md](04-premade-suites.md)) or **custom** (written in the firmware repo by the engineer and agent). **A custom suite reuses a premade test by copying it into the firmware repo and editing it freely**, and **the copy keeps `derived_from: <test id>@<suite commit>`**, so the report shows every verdict-deciding field it changed ("limit widened from 4.75–5.25 V to 4.5–5.5 V"); a copy with a loosened limit never reads as the premade test.

## One test

**A test is a study plus verdict rules; there is no new step format.** It carries:

- the **study** it runs, a host study or a dev-bench study;
- the **requirement IDs** it checks, and the **revision range** of the spec it applies to;
- the **bench** it needs, and the **config** of that bench, by name;
- a **precondition**, the state it starts from: `reset`, `power_cycle`, `detach` or `none`. **The default is a DUT reset plus each bench board's idle command, before every test**, so one test's leftovers (a PPS contract kept alive, a swapped role) are never the next one's start, and reordering tests cannot change their results. LabGrid's strategies are the precedent ([09](09-trust-model.md#prior-art));
- **`requires`**: other tests it depends on, so a failed or skipped one skips it, with that reason;
- a **run count**, default 1. The verdict is a pass only if every run passes; a flaky behaviour gets a count above 1 in its own test;
- **limits** on its **measurements** ([02-study.md](02-study.md#measurements)), each limit no tighter than what measures it can resolve.

## The verdict

**Decided by code, never by the agent**, and one of six:

| Verdict | Means |
|---|---|
| **pass** | Every limit held, on every run, on complete evidence |
| **fail** | The DUT broke a limit or a marker rule |
| **error** | The setup could not judge the DUT: a bench board, an instrument or a port failed, or the smoke check did |
| **inconclusive** | The evidence the verdict rests on is incomplete: a truncated capture, a truncated reply, a gap across the measured window, a number that did not parse. **Or a result inside a limit's guard band**, between its acceptance limit and its tolerance limit, with the reason "guard band" (owner, review round 1) |
| **skipped** | Not run, with the reason: not applicable, hook unmapped, bench missing, not selected, a `requires` not met, stopped by an error |
| **cancelled** | The run was cancelled |

**A step's failure is charged by what it addressed.** A step on a DUT signal, or a limit on a DUT measurement, can fail the DUT; a step on a bench board or an instrument that fails is an **error**, so a cable that falls out never reads as a DUT failing conformance. Today a lost port is `Fail` whatever it addressed ([embarch-core decision 95](../../embarch-core/decisions/host-study.md)), so this is new in Core. Today's marker outcomes stay underneath (a host study's `until` seen passes the step, `refused_on` fails it), and **declared numeric limits** are added on top. **A person may enter a verdict by hand, and it is recorded as theirs**, through any surface the ledger has today, MCP included (owner, review round 1).

**Core parses the number at step time.** A host-study step declares a pattern and a unit; Core records the number beside the raw reply in `events.json`. This is the "declared numeric parse" the [host-study proposal](../../embarch-host-study-proposal.md) left for later ("What is left", item 2). Numbers computed over a capture after the run are embarch-api's ([02-study.md](02-study.md#measurements)).

**A limit is checked against what can measure it.** Each measurement source declares its resolution, and **a test whose limit is tighter than its source can resolve is refused when the test is defined.** A host stamp through a USB serial bridge is not a sub-millisecond clock (inferred, not measured), so a PD timing requirement is measured on the bench board's own clock. **The report states its decision rule**, simple acceptance or a guard band, as ISO/IEC 17025 asks of a statement of conformity; **a limit carries its uncertainty**, and under a guard band its acceptance limit is the tolerance limit less a stated multiple of it (ILAC-G8; [11](11-prior-art.md#classical-hil-frameworks-formats-and-report-tooling)).

## Benches

- **A suite ships each bench as a saved-bench description**: parts, cables and configs, no probe serials. **Selecting a suite copies its benches into the firmware repo's `embarch/topologies/`**, where the project can edit them, which keeps the owner's 2026-11-01 call that saved benches live in the firmware repo ([embarch-ui decision 73](../../embarch-ui/decisions/saved-benches.md)).
- **Setting a bench up is a human step in the Topology view**: open the saved bench, wire it, **Make live**, which applies the declarations and proposes each probe binding ([decision 90](../../embarch-ui/decisions/bench-live.md)).
- **A config change inside one bench is a `Prompt` naming the config**, which host studies already do ([embarch-study-designer decision 88](../../embarch-study-designer/decisions/host-prompt.md); [embarch-ui decision 99](../../embarch-ui/decisions/operator-prompt.md)).
- **The same DUT unit moves from bench to bench.** The runner checks its hardware ID on every bench and refuses a different unit.
- **Hardware safety is an authoring concern, not a runtime limit** (owner, review round 1): no envelope is enforced at execution. What a test puts on the DUT (a VBUS level, a load current) is reviewed against the DUT's ratings when the test is written and confirmed, and the run preview shows it again before the start ([Selecting and rerunning](#selecting-and-rerunning)).

## A run

**Core runs it, so a run survives the session that started it.** Core never reads a firmware repo, so **embarch-api resolves the selection** into one file, **`run.json`**, and sends it to Core. Core runs it and keeps the results; embarch-api writes the result rows when it reads them back, as the ledger already does for a study ([embarch-api decision 98](../../embarch-api/decisions/ledger.md)).

1. **Group by bench.** All selected tests for bench A run, then bench B, and so on. **One lease for the whole run, held by the run itself.**
2. **Between benches, an operator prompt** says which saved bench to set up, with what is missing. **Only the person answers a prompt**: in the UI's prompt modal, or by telling the agent, which relays their exact words with `answer_prompt`. **The agent never answers one on its own.** **A prompt declares its kind**, `setup`, `action`, `observation` or `clearance`, and **Core refuses a relayed answer to an observation or a clearance**, whose answer is itself evidence or a person's safety; an action prompt names the measurement that confirms the action (owner, review round 1; [12](12-prevention.md#operator-prompts-by-kind)).
3. **Before a bench's first test, a smoke check**: the topology the bench needs is live, the DUT's and every board's identity validates, each companion board answers a hello, each instrument answers an identity query (its `*IDN?` reply goes in the report), and **the DUT's image is read back through the probe**, its load segments' SHA-256 compared with the artifact's. The report then says "verified by readback", or "a claim" with the reason when read-out protection blocks the read. A failing check names the piece, runs no test on that bench, and is an **error** for each of them.
4. **Nothing else touches the bench while a test runs**: Core refuses every hardware call that is not the run's own, Live reads included ([12](12-prevention.md#what-stays-outside-prevention-and-is-said-so)).
5. **What a failure stops.** A failed **step** ends its **test**, with the study's teardown, as host studies already do. **A fail ends only its own test**: the bench goes on to its next test, which starts from its own precondition. **An error ends its bench**, because the setup is no longer trustworthy, and the run goes on to the next bench. **A cancel ends the whole run.** **`stop_on_fail`**, a run option off by default, ends the run at the first fail, for a debugging session. *Replaces the owner's first answer, "a failure ends its own bench" (owner, review round 1).*
6. **Watching a run.** One `test_status` call answers the current bench, the current test, the verdicts so far, and a waiting prompt with its text, from any session; each study's own events stay available underneath.
7. **Retention.** A Test run's studies count as one unit in Core's retention sweep (`EMBARCH_STUDY_RESULTS_KEEP`, 50 runs), are swept together, and **are never swept while the run is unpublished, nor once it is published.**
8. **Sequential only.** Two benches acting at the same moment are out of scope; Core runs one study at a time and a host study cannot drive the dev bench.
9. **A long run survives a restart as far as it got.** A Core restart leaves the run `interrupted`, its verdicts so far kept. **Resuming is a new run of the pending remainder**, linked to the first, with the image read back again. **Core keeps the host awake while a run holds the lease** (the need on Windows is inferred, not measured).

## Selecting and rerunning

- **Selection narrows by applicability, then picks.** The runner keeps the tests that apply to the DUT's role and capabilities and to the benches that exist, then the engineer or agent picks by test ID or tag.
- **A selection is saved as a test plan** in the firmware repo, to rerun it ("our PD regression set").
- **`run.json` is the resolved run**: every test expanded to a concrete study, the DUT's inputs substituted, limits, benches, configs, preconditions, the suite's commit, the plan's hash, and each capability with its provenance. **A premade test is a template**, expanded here: one pass per PDO the DUT advertises, say. `run.json` is hashed, kept by Core, carried in the zip, and is what `verify` recomputes against ([06](06-report-and-publish.md#verify)).
- **A preview before the start.** The agent shows the engineer the tests per bench, the prompts the person will see, what will be powered and at what level, and an upper bound on the duration from the timeouts. **The engineer's go starts the run.**
- **The rerun rule is today's ledger rule**: a test is pending when the DUT image hash differs from its last pass, or it never ran, failed, or its commit was rebased away.

## The DUT's inputs

A test may need two kinds of input about the DUT:

- **Capabilities**: its role (source, sink, dual-role), its PDOs, which swaps it supports, and the like. They decide applicability.
- **Hooks**: a named action the DUT must take itself, such as `dut.request_pr_swap` for a swap the DUT initiates. **A hook maps to a DUT shell command or to an operator prompt** ("press the button"); **a hook with no mapping skips its test, and the coverage list says why.**

**Every input that decides a verdict needs the engineer's confirmation** (owner, review round 1): capabilities, hook mappings, limits, run counts, the revision tested against. **The agent proposes; a proposal is not used until the engineer confirms it**, and **a confirmation is made in the UI only, or the CLI where there is no UI** (owner, review round 1). **It binds the hash of exactly what was confirmed and is kept by Core**, outside the firmware repo the agent can edit (owner, review round 1): an input edited after its confirmation is unconfirmed again, and the preview says so. Who confirmed what, when and through which surface is shown in the appendix. How Core makes this hold against an agent that tries to forge one: [12-prevention.md](12-prevention.md). Otherwise an agent that read the source and decided "this DUT cannot PR_Swap" would drop the swap tests as not applicable, and the coverage would still look complete.

**Each capability carries its provenance**, listed in the report:

| Provenance | Where it comes from |
|---|---|
| `measured` | Read off the wire: the PD partner captures the DUT's Source_Capabilities |
| `decoded` | The atlas, from the build (a USB PD PDO is already decoded, [atlas design](../../embarch-atlas/design.md#firmware-configuration-against-a-standard)), or `atlas.toml`'s declared values |
| `confirmed` | Proposed by the agent, confirmed by the engineer |
| `declared` | Typed by the engineer, or read from the DUT's **VIF** (Vendor Info File, the XML a PD compliance tool takes; Zephyr's `scripts/generate_usb_vif` builds one from the devicetree) (owner, review round 1) |

**Where a capability can be measured, a declared or decoded value is checked against the measured one**, which is a test in its own right. Every answer is saved in the test plan, so it is asked once per project, not once per run. **A hook mapping is proposed by the agent** from the firmware's shell (its source, or a live `help`) and lands in the plan once the engineer says yes.

## It grows out of the ledger

**EmbArch Test replaces the hardware test ledger by growing out of it** ([embarch-api decision 98](../../embarch-api/decisions/ledger.md), [tools](../../embarch-api/interfaces/tools-ledger.md)). The ledger's three files and its computed pending view are kept and renamed: **`embarch/tests/` holds the custom suites, the test plans and the results, and `ledger_show`, `ledger_pending` and `ledger_add` become `test_show`, `test_pending` and `test_add`**; `tests.toml`'s `needs` becomes a bench; rows a person entered by hand stay possible. **`embarch/` stays untracked** until EmbArch is published and other engineers use it (owner, review round 1), so the report pins each definition file by its hash ([06](06-report-and-publish.md#the-audit-appendix)). **The ledger is not yet verified on a bench**, so nothing about it is a measurement yet.

## The report

**Published the same way as a Study** ([06-report-and-publish.md](06-report-and-publish.md)), **organised by requirement**: each verdict cites the run behind it. **A requirement passes when every one of its tests that ran passed** (owner, review round 1); its skipped tests do not block the pass and are listed under it with their reasons, and any other verdict of a test is the requirement's.

- **It lists every applicable test that did not run, and why**, from the skip reasons above, so a partial run never reads as full conformance.
- **It counts the standard, not only the selection**: the standard's requirements applicable to this role (with an atlas), those the suite has a test for, those selected, run and passed.
- **It lists every run of each test on the same DUT image**, published or not, with its verdict, from the ledger's append-only rows: a pass after four failures shows the four failures.
- **It carries a fixed sentence: pre-compliance evidence, not a certification by any standards body.**

## Open

- **An authoring rule for prompts that ask a person to handle the bench.** Recommended for the guide's authoring section, following the owner's "safety at authoring": such a prompt is preceded, in the test as written, by the steps that turn every output off, and its text says the outputs are off.
- **How a step declares what it addresses**, for charging a failure: derived from its target (a DUT signal, a bench board, an instrument) or written in the step. Recommended: derived, so no study is rewritten.
