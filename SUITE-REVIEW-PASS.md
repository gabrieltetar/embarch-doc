# embarch-doc: running a suite review pass

**Status:** active, 2026-09-06. A hunt for design flaws and improvement opportunities across **every sub-project at once**, run by hand from the owner's session via `/suite-review`. This file is the method; the agents that execute it are `.claude/agents/embarch-auditor.md` and `.claude/agents/embarch-auditor-dimension.md`, rendered from the framework repo.

## 1. What this is, and why nothing else does it

A **pass** in [DOC-COMPACTION-PASS.md](DOC-COMPACTION-PASS.md)'s sense: an occasional sweep over everything, deliberately not a gate and not a per-change check. Three things already read this suite's work and **none can see what this one looks for:**

- **`scripts/check-docs.py`** is mechanical — sizes, links, decision references, two status tables. It reads *shapes*, never intent.
- **`embarch-reviewer`** reads **one landed diff** against the decisions it must not contradict: one unit, one sub-project, after the fact.
- **The supervisor's refill** ([the protocol](../embarch-fleet/protocol.md) §4) sweeps the roadmap, eight `open.md` files and the reversals follow-ups — **a sweep of what the suite already knows it owes itself.** It cannot generate a finding nobody has written down.

**What none of them sees is the thing that is wrong across two modules and right within each.** A duplicated abstraction, a boundary that leaks, a principle honoured in six places and dropped in the seventh: each passes every check, because **every check is scoped to one repo, one diff, or one file.** That gap is this pass's whole subject.

## 2. The one question

> **Would the suite be simpler if this were different?**

Every dimension below is an aid to asking it well. **A finding that cannot be phrased as an answer to it is not a finding.**

**"Simpler" is a taste word, and that is this charter's known weakness** — an agent can justify nearly anything with it. Two clauses keep it honest, and a hunter skipping either is producing preferences:

- **Simpler for whom**, named: the engineer reading two modules side by side, the agent calling the surface, whoever changes it in six months. Unnamed beneficiary → not a finding.
- **Simpler how much**, counted: one fewer module, concept, place a fact lives, spelling of the same thing, step in a chain. **"Cleaner" and "more idiomatic" are not counts.**

## 3. The bar

> **Would you spend a worker-unit on it?**

Not *is it true* — the pass will find many true and worthless things. A finding clears the bar when the owner would say yes to it announced in the fleet channel: concrete, bounded, worth a quarter of a leg.

**The bar is lower than `embarch-reviewer`'s** ("would you revert a landed commit for it") on purpose, because the two hunt different animals: **a design flaw was never wrong enough to revert — which is why it is still there.** The reviewer's bar applied here returns nothing, every time.

**The run is uncapped** (decided 2026-09-06): a pass is *meant* to generate a lot of work and the queue is meant to hold it. Two consequences are accepted rather than solved:

- **A large drop suppresses refill.** [The protocol](../embarch-fleet/protocol.md) §4 fires refill only when the queue is *below* its low-water mark, so the fleet's own roadmap/`open.md` sweep stops until the findings drain.
- **Rank does not survive into the queue.** §6 step 2 selects by scope diversity, with no ordering rule and no priority field, so drops are worked in effectively arbitrary order. **The ranking lives in the report and nowhere else.**

## 4. The seven dimensions

Six named hunts and one open one. Each hunter reads **the whole corpus** and looks for one thing; that is what preserves the cross-module view a per-sub-project split would destroy (§5).

1. **Standalone-ness.** Can this module be understood, built, tested and reasoned about without its siblings? Where does it reach across a boundary it declares? **Modules here are standalone *to a degree*, not absolutely** — `embarch-study-designer` is compiled into four consumers by design, `embarch-topology` exists to be linked. The finding is *accidental* coupling, never deliberate sharing.
2. **DRY across modules.** The same logic, table, constant or parsing rule living in two repos. **The suite's own precedent is the target shape:** detection logic duplicated across three consumers became `embarch-topology`, a linked crate. The counter-example it already names is the "liftable copy" pattern — mirrored files held equal by a comment and hope.
3. **One philosophy.** [embarch.md](embarch.md) §5's principles, honoured unevenly: *every hardware-facing capability reachable by agent and human alike, converging on the same module, never a privileged path*; *single-engineer scope*; *never present an inference about hardware as fact*. A module that quietly exempts itself is the finding.
4. **Layering and dependency direction.** Who links whom, versus [embarch.md](embarch.md) §4's sketch. A shared crate that grew a dependency on a consumer; a module reaching around its own abstraction; a hop declared out of the runtime path that crept back in — umbrella's *"a working machine keeps working if the `embarch` binary is deleted"* is a testable claim, not a slogan.
5. **Cross-surface consistency.** One concept spelled differently across core / api / ui / umbrella: error taxonomy, config resolution, auth, schema versioning, names against [embarch-glossary.md](embarch-glossary.md). **The mechanical twin of dimension 3** — 3 is a principle, 5 is a spelling. Where both would report one thing, synthesis keeps one.
6. **Deletion candidates.** What could be *removed*: a subsystem a later decision made pointless, a knob nobody uses, a compatibility path for something already shipped. **The strongest shape in the pass**, being the only one whose fix makes the suite smaller — the 2026-08-15 precedent's best item retired four moving parts for one endpoint change.
7. **The newcomer.** *What would an engineer new to this suite get wrong, and be reasonable to?* Missing affordances, misleading names, traps obvious only once known. **Structurally invisible to the other six**, which are consistency-shaped and therefore blind to what is uniformly bad everywhere.

## 5. Shape of a run

**Seven hunters in parallel, then one synthesis.** Each holds the whole doc corpus (~950 KB, ~240k tokens) and hunts one dimension; the synthesizer dedupes, ranks and writes.

**Not one agent per sub-project**, the cheaper split and the wrong one: a per-module reader **structurally cannot see "these two modules duplicate each other"** — dimension 2, the second thing this pass exists to find.

**Docs first, code on demand.** A hunter reads docs to *form* a suspicion and opens code only to **confirm or kill a specific one**; the ~80k lines fit no context, and reading them speculatively turns a run into a survey. **A finding whose claim is about code behaviour must be code-confirmed before it is dropped.** One about design coherence need not be.

## 6. Procedure

**Preflight, and the first is not optional:**

- **The pump must be stopped.** A leg's tree is up to three units stale and *nothing errors* — `embarch-reviewer` names this as its central hazard. Check `../.fleet/pump` and the tick file's age; if the fleet is live, stop it and say so before starting.
- **Working tree clean and pulled**, in every repo the pass will read.
- **Read the queue first**, every open `tasks/**` file. **A finding already queued is not dropped again** — the report names the task covering it. Not a ledger, and no contradiction with §8's accepted churn, which is about findings *you declined*.
- **Run the read-only tools rather than re-deriving them**: `scripts/check-duplication.py` (a DRY signal that already exists), `collect-open-questions.py`, `queue-status.py`.

**Then:** fan out seven hunters → synthesize → write the report → write the drops.

**A drop is a complete task file** in [inbox/README.md](inbox/README.md)'s format — no number, `Hardware:` an honest claim about *the fix*, a `Done when` checking the property rather than an implementation. **It carries the flaw plus one proposed direction**, leaving the worker room to design within its own sub-project ([the protocol](../embarch-fleet/protocol.md) §5.4). **A finding spanning two or more sub-projects is `Scope: suite`** — §8 there makes it the supervisor's own, never dispatched. The fleet already draws that line; this pass uses it rather than inventing one.

**The report is uncommitted**, `.claude/suite-review-<yyyy-mm-dd>.md`, as its 2026-08-15 ancestor was: regenerable, so durability buys nothing and a stale findings file reads as current truth to whoever opens it next.

## 7. The gate

**Mechanical: none, and that is honest** — the pass writes only to `inbox/` and an ignored file, so `check-docs.py` has nothing to say about it. What replaces a gate is the report's shape: every finding names its beneficiary, its count (§2), the files it rests on, and whether it was code-confirmed.

**Human, one question, asked honestly:**

> **Of what this run dropped, how much would you have wanted done anyway?**

**Mostly yes → the pass is working. Mostly no → the bar drifted**, and the next run's instruction is to raise it, not to find more.

## 8. What this pass deliberately does not solve

- **Churn.** Run N+1 re-finds what you declined in run N. Accepted (2026-09-06); the alternatives were a declined-findings ledger — a second place design rationale lives, which [DOC-PROTOCOL.md](DOC-PROTOCOL.md) §3 treats as the characteristic failure — or an obligation to record every declined finding in a `decisions.md`. **The free mitigation should still be used: a finding contradicting a rejection already recorded in a `decisions.md` is not a finding, and if the rejection is not written down, *that* is the finding.**
- **Ordering.** §3.
- **The fleet's own rules.** In scope to *read*, never to file: `check-ownership.py` refuses `fleet` as a worker scope and `tasks/fleet/` is reserved, so a finding there **cannot become a queue task at all.** It goes in the report's owner-only section and never into `inbox/` — which is what keeps *"a supervisor that can edit its own constraints has none"* true rather than nearly true. Same for every path in `fleet.toml`'s `reserved` list.

## 9. Failure modes

- **Surveying instead of choosing.** A report listing everything true is the 2026-08-15 outcome: ~60 findings, several genuinely valuable, never run again. The bar (§3) is the whole defence.
- **Re-proposing a rejected alternative.** [embarch-decision-reversals.md](embarch-decision-reversals.md) is largely a record of this happening. A hunter that has not read the relevant "why not" clauses is generating them.
- **Mistaking a decision for a flaw.** Single-engineer scope, no `rustfmt` gate, umbrella out of the runtime path, the dev-bench bypass — deliberate, documented, and all look like flaws from outside.
- **Reading a stale tree.** §6's first preflight. **The staleness is invisible**: the file is there, it parses, it is merely a version old.
- **Inventing a DUT or firmware fact.** [embarch.md](embarch.md) §5 — every hardware-specific meaning is engineer-declared. A hunter that infers one has produced a false finding with a real-looking citation.
- **Two hunters, one finding.** Dimensions 3 and 5 overlap by construction. A run that drops both spellings skipped synthesis.

## 10. What the pass must never do

- **Never write outside `inbox/` and the ignored report.** Not a doc, not a task file, not code. Same rule as `embarch-reviewer`, same reason: nothing mechanical stops it, this instruction does.
- **Never touch hardware.** No build, no flash, no study, no board. It reads.
- **Never file a finding about the fleet's own rules or any reserved path.** §8.
- **Never let a hunter drop its own findings.** They go to synthesis first, or the dedupe and the ranking do not exist.
