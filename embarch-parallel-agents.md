# EmbArch: parallel agent work

**Status:** active, 2026-09-02. New — nothing has run under it yet; §12 is the list of things to watch on the first batches.

## 1. Why this exists

Every rule in this suite was written for one engineer in one session. [embarch-dev-workflow.md](embarch-dev-workflow.md) §6 says commit straight to `main` and justifies it *by* that assumption — "this suite has one engineer … there is nothing to collide with". [DOC-PROTOCOL.md](DOC-PROTOCOL.md) §5 tells whoever ships a change to update the suite-level status tables in the same pass, which is safe exactly once per moment. Both stop being safe the moment four agents work at once.

So: **one supervisor thread dispatches 4–6 short-lived worker threads, each owning one sub-project, and lands their work itself.** This doc is what replaces the single-session assumption for those threads. It governs background threads only — the owner's own interactive sessions keep working exactly as before, on `main`, under §6 unchanged.

The design principle throughout: **prevent collisions structurally; do not resolve them.** A supervisor that merges two workers' edits to the same table is guessing at two intents it never held. Every rule below exists to make sure that merge never has to happen.

## 2. Roles

Three, and the boundaries between them are the whole design.

**The owner.** Approves nothing routine — the supervisor is a full delegate, and steers by exception, and can start, stop, question or redirect the fleet from Remote Control or **#embarch-fleet** on a phone ([running the fleet](embarch-parallel-agents-ops.md) §3–§5) (§11 is why that is a real risk and what it buys). Four things stay the owner's and cannot be delegated:

- **Amending a standing rule** — this doc, [embarch-dev-workflow.md](embarch-dev-workflow.md) §6, [DOC-PROTOCOL.md](DOC-PROTOCOL.md), [DOC-COMPACTION.md](DOC-COMPACTION.md). A supervisor that can rewrite its own constraints has none. §6 already says its own rule "ends when the repo owner says it ends, and on no other condition"; this is the same property, stated once for the whole class.
- **Anything physical** — plugging in a board, swapping hardware. Unchanged from [embarch-dev-workflow.md](embarch-dev-workflow.md) §5's Tier 3.
- **Anything outside the suite's own repos** — a client firmware repo, a deployed machine, a release.
- **Starting the supervisor.** It does not start itself (§13).

**The supervisor.** Exactly one runs at a time, ever. It refills the queue, dispatches workers, lands their branches in order, owns every shared suite-level file, executes cross-repo passes itself, and writes the digest. It designs suite-wide changes and approves them. It **never** touches hardware and never runs a worker's task itself except where §8 says so.

**A worker.** Takes one task, in one repo, on one branch, ships it with its docs, and exits. It holds no state between tasks — everything it learned is in the docs it wrote or it is gone. That is not a limitation to work around; it is [DOC-PROTOCOL.md](DOC-PROTOCOL.md) §4's discipline with the escape hatch removed.

## 3. The ownership map

Branches are the backstop. **This table is the actual mechanism** — if it is honored, a merge conflict is a bug in the dispatch, not a normal event.

| Path | Worker | Supervisor | Owner |
|---|---|---|---|
| Its own sub-project's code repo | write | write | write |
| Another sub-project's code repo | **never** | write | write |
| `embarch-doc/<its own sub-project>/` | write | write | write |
| `embarch-doc/<another sub-project>/` | **never** | write | write |
| `changelog.d/` (new fragment) | write | write | write |
| `status.d/` (new fragment) | write | write | write |
| [embarch.md](embarch.md), [suite/features.md](suite/features.md), [embarch-roadmap.md](embarch-roadmap.md) | **never** | write | write |
| [embarch-decision-reversals.md](embarch-decision-reversals.md), [embarch-glossary.md](embarch-glossary.md), [embarch-user-guide.md](embarch-user-guide.md) | **never** | write | write |
| `tasks/` | claim + close its own | write | write |
| [DOC-PROTOCOL.md](DOC-PROTOCOL.md), [DOC-COMPACTION.md](DOC-COMPACTION.md), this doc, [embarch-dev-workflow.md](embarch-dev-workflow.md) | **never** | **never** | write |
| `scripts/` | **never** | write | write |
| Hardware (probe, DUT, dev-bench, live Core) | **never** | **never** | write |

The three "never" rows a worker will most want to break are the shared suite-level docs, and [DOC-PROTOCOL.md](DOC-PROTOCOL.md) §5 explicitly tells it to edit them. §9 is the replacement.

## 4. The task queue

`tasks/<sub-project>/NNN-slug.md`, committed to `main` in this repo. Format and the claim protocol: [tasks/README.md](tasks/README.md).

A queue that lives in git rather than in the supervisor's head buys three things worth the extra doc kind: two supervisor runs cannot dispatch the same task, a task survives the thread that was working it, and the reason a task exists is written down next to it instead of being re-derived from the roadmap every batch.

**The supervisor refills the queue itself** at the start of each batch, from [embarch-roadmap.md](embarch-roadmap.md)'s Now/Next, every sub-project's `open.md`, and [embarch-decision-reversals.md](embarch-decision-reversals.md)'s unaddressed follow-ups. No one hand-writes a backlog. The queue is therefore a *view* of the docs, which is only true as long as closing a task also updates the doc the task came from — §5's contract.

## 5. The worker contract

A worker is handed exactly one task file and this contract. It must:

1. **Work in two worktrees, on one branch name.** Almost every task changes both its code repo *and* `embarch-doc/<sub-project>/`, so a worker gets a branch called `agent/<sub-project>/<NNN-slug>` in **both** repos, and the supervisor lands both together (§10). This is not bookkeeping: a shipped change whose docs sit on an unmerged branch is exactly the drift [DOC-PROTOCOL.md](DOC-PROTOCOL.md) §5 exists to prevent. Six workers branching `embarch-doc` at once is safe *because* of §3 — their paths are disjoint by construction. Both worktrees live under `embarch/.worktrees/<repo>/<NNN-slug>/`, **outside every repo tree**, and the supervisor creates and deletes them (§6). Not inside `.claude/worktrees/`: a checkout of a repo placed inside that repo is what made a naive source scan find six GATT service blocks instead of three (`embarch-study-designer` decision 57), and putting agent worktrees there would re-create that class of bug on purpose.
2. **Stay inside its ownership row** (§3). If the task turns out to need another repo, it stops and reports that — it does not reach across. A task that needed two repos was mis-filed, and §8 owns the fix.
3. **Never touch hardware** (§7).
4. **Design freely within its own sub-project.** A new `decisions.md` entry scoped to one sub-project needs nobody's approval — that was the owner's call and it stands. Number it per [DOC-PROTOCOL.md](DOC-PROTOCOL.md) §7.2; numbers are permanent.
5. **Update its own four files** — `spec.md`, `decisions.md`, `open.md`, `interfaces.md` — per [DOC-PROTOCOL.md](DOC-PROTOCOL.md) §4–5. Edit the body; never append.
6. **Drop a `changelog.d/` fragment**, and a `status.d/` fragment for every suite-level fact its change made false (§9). It does not edit the suite-level docs.
7. **Pass the gate** (§10) before it says it is done — including `scripts/check-ownership.py --scope <sub-project>`, the mechanical form of rule 2. Green, or it reports red and does not claim otherwise.
8. **Close its task file** and push its branch. It does not merge.

A worker that cannot finish writes what it found into the task file and exits. A half-done branch left with an honest note is worth more than a finished-looking one.

## 6. The supervisor's batch

One batch is five phases, in order. Phases 3 and 4 interleave — a worker's branch can land while others are still running, and should, because a branch that waits gets stale.

0. **Recover.** A previous batch may have been killed outright — closing VS Code is the owner's kill switch and is expected to be used ([running the fleet](embarch-parallel-agents-ops.md) §3). Abort any in-progress merge or rebase, reclaim every stale claim, and delete dead worktrees **before** anything else. The exact rule and what a kill can leave behind: [running the fleet](embarch-parallel-agents-ops.md) §3.
1. **Refill.** Sweep the roadmap, every `open.md`, and the reversals follow-ups; write any new task files. Reconcile: a task whose source doc no longer says the thing is closed, not dispatched.
2. **Select and set up.** Ask `scripts/usage-budget.py --suggest` how wide this wave may be ([running the fleet](embarch-parallel-agents-ops.md) §2); it, not the cap, sets the number. Pick at most one task per sub-project from `Hardware: none`/`verify-only` tasks. For each: create both worktrees under `embarch/.worktrees/`, create the branch in both repos, write the brief. **If nothing is dispatchable** — the queue is empty, or holds only `Hardware: required` or `blocked` tasks — the batch ends here: say so, list what is waiting on the owner, and do not invent work to fill the wave.
3. **Dispatch.** Launch the workers in parallel as background agents. Do not block on the first one. Re-check the budget ([running the fleet](embarch-parallel-agents-ops.md) §2) before each subsequent wave, never only at the start of the batch.
4. **Land.** As each worker reports, run the gate (§10) independently — do not trust the worker's word for green — then merge both of its branches in the order §10 fixes. Rebase the rest onto the new `main`. **Record every merge commit's SHA**: under §6 there is no merge commit and no branch name left afterwards, so the SHA is the only handle a revert has (§11). Delete a worker's worktrees once its branches have landed or been abandoned.
5. **Fold and report.** Consume every `status.d/` fragment into the shared suite-level docs, run `build_changelog.py`, commit that as the supervisor's own single serialized change, then write the digest (§11).

Phase 5 being one commit by one actor is what makes the shared tables conflict-free. It is the only phase that must not be parallelized.

## 7. Hardware: workers never touch it

There is one probe, one `hw_lock`, one study in flight (rejected with `409`, deliberately no queue), one live Core, and one DUT + dev-bench pair (`embarch-topology` decision 10). Four workers cannot share that, and Core's `409` is not a coordination mechanism — it is a refusal an agent will misread as a bug in its own change.

So: **workers are host-side only.** Build, `cargo test`, `clippy --all-targets -- -D warnings`, host unit tests, docs, design. Anything needing a board — a flash, a study, a serial log, a deploy — is not a task. A worker that discovers its change can only be verified on hardware writes that into the task file as a **hardware-verification debt** and ships the host-side half; the supervisor collects those into the digest, and they are worked in the owner's own session.

The supervisor does not touch hardware either. It is unattended by design, and [embarch-dev-workflow.md](embarch-dev-workflow.md) §5's Tier 2/3 autonomy was granted to a session the owner was sitting in front of.

This is a real cap on what parallelism buys here: most of what currently blocks this suite is hardware-gated. The threads are for the large remainder that is not.

## 8. Cross-repo changes: the supervisor does them itself

A schema change touching five repos must land as one sequenced pass, shared crate first, each repo's `main` compiling on its own ([embarch-dev-workflow.md](embarch-dev-workflow.md) §6). One-thread-per-repo structurally cannot do that: a half-landed wire change is the worst failure mode this suite has.

So a task that spans sub-projects is **never dispatched to a worker.** The supervisor executes it itself, in one session, sequenced — after designing it, which under the full-delegate model it may do without asking. Workers stay single-repo, always.

Practically this means the supervisor's own hands do the riskiest work in the suite while unattended. So it **announces before it starts**: a Slack DM naming what it is about to do, the task parked rather than begun, the rest of the batch running normally, and a reply from the owner able to cancel it right up until the batch ends ([running the fleet](embarch-parallel-agents-ops.md) §4). That is a veto that costs the batch nothing, which is why it is this rather than a delay. §12 says what to watch anyway.

## 9. Shared suite-level docs: `status.d/` fragments

[DOC-PROTOCOL.md](DOC-PROTOCOL.md) §5 requires the suite-level facts to move in the same pass as the change. With one engineer that is a rule against drift. With four workers it is a rule that puts four agents into [embarch.md](embarch.md) §3's table at once.

The fix is the one this repo already proved with `changelog.d/`: **one file per pending edit, no shared file touched.** A worker writes `status.d/<scope>-<slug>.md` naming the target doc and the fact that changed; the supervisor folds every fragment in phase 5 and deletes them. Format: [status.d/README.md](status.d/README.md).

The rule DOC-PROTOCOL §5 was protecting is unchanged — the suite-level docs still must not disagree with a sub-project's — it just now takes two actors and one batch instead of one actor and one commit. The window in which they *can* disagree is the length of a batch, and closing it is phase 5's whole job. **A batch that ends with unfolded fragments in `status.d/` has failed**, whatever else it landed.

## 10. The merge gate and merge order

The gate, run by the worker and then **re-run independently by the supervisor** on the merge result — not on the branch:

- `cargo build`, `cargo test`, `cargo clippy --all-targets -- -D warnings` in the touched repo, plus a native Windows build where `embarch-core` is involved ([embarch-dev-workflow.md](embarch-dev-workflow.md) §4).
- All six `embarch-doc` checks: `check-links.py`, `check-staleness.py`, `check-decision-refs.py`, `check-doc-conventions.py`, `check-doc-size.py`, `build_changelog.py --check`.
- **`check-ownership.py --scope <sub-project>`** on both branches — the mechanical form of §3. Without it §3 is prose nothing reads: a worker's edit to [embarch.md](embarch.md)'s status table is *plausible by construction*, so `check-staleness.py` (which only flags a row disagreeing with a sub-project doc) passes it, and the collision §9 exists to prevent happens anyway.

That is [embarch-dev-workflow.md](embarch-dev-workflow.md) §6's existing standard, unchanged, applied per branch instead of per commit. Nothing here licenses a lower bar because an agent wrote it.

**The gate is mechanical and catches broken, not wrong.** The one judgement the supervisor adds: it reads the diff before merging when the change touches a shared crate (`embarch-study-designer`, `embarch-topology`), a wire type, or retires a decision — the three places where passing and correct diverge most expensively. Everything else merges on green.

**Merge order** is shared crates first, then consumers, then `embarch-doc` — the same sequencing §6 already fixes for a cross-repo pass, applied to a batch of independent ones. Within a tier, order by branch age, oldest first, so nothing sits.

## 11. The digest

Canon is a doc; Slack is the ping.

Each batch prepends one entry to [supervisor-log.md](supervisor-log.md), newest first: what it **decided**, what merged, what blocked and why, and every hardware-verification debt it collected. What *shipped* is already recorded by the workers' own `changelog.d` fragments and assembled into `history/<scope>.md` — the digest does not restate it. When the log passes 25 KB the oldest batches roll into `history/archive/`, matching what `build_changelog.py` already does for a history file. Then a short Slack message to the owner pointing at it.

**This is the review surface, and under full delegate it is the only one.** It is read after the fact, so it must be honest about what was decided and not just what was shipped — a suite-wide design the supervisor approved on the owner's behalf is the single most important line it will ever write, and it belongs at the top of the entry, not buried under the merge list.

## 12. Known risks, stated rather than designed away

- **Nothing reads a diff for intent before it lands, most of the time.** Full delegate plus a mechanical gate plus 4–6 parallel branches means `main` across eight repos moves on green alone. §10's shared-crate/wire-type/retirement carve-out is the mitigation, and it is deliberately narrow. Watch for the first change that passes every check and contradicts a locked-in decision — that is this design's characteristic failure, and it will not announce itself.
- **The supervisor executes cross-repo passes unattended.** §8's reasoning is sound and its blast radius is still the largest in the suite. The announce-and-park DM ([running the fleet](embarch-parallel-agents-ops.md) §4) narrows the window rather than closing it: an owner who does not read the DM within the batch gets the change anyway, which is what full delegation means.
- **A worker's design authority is scoped by repo, not by consequence.** A one-repo change can be less reversible than a two-repo rename — a wire encoding, a retired decision, a deleted doc. The owner chose scope as the boundary because it is mechanically checkable; the cases where it is the wrong boundary will show up in [embarch-decision-reversals.md](embarch-decision-reversals.md), which is where to look for evidence this needs revisiting.
- **The queue is a view of the docs and can drift from them.** Refill reconciles in one direction only.
- **Worktrees are already load-bearing elsewhere and bit this suite once.** A naive repo-wide source scan finds `.claude/worktrees/` copies and silently over-extracts (`embarch-study-designer` decision 57). Any new tool that walks a repo must honor ignore files; more worktrees make that failure more likely, not less.
- **`status.d/` can be skipped silently.** A worker that ships without a fragment leaves a suite-level doc stale and nothing fails. `check-ownership.py` proves a worker did not edit a shared doc; nothing proves it *should* have asked to. `check-staleness.py` catches part of it, heuristically, and only for two tables.
- **Work can start from Slack outside the protocol.** A message in #embarch-fleet that is not a `fleet` command is acted on as an ordinary session turn ([running the fleet](embarch-parallel-agents-ops.md) §5.2) — no task file, no ownership map, no gate. Chosen deliberately for the reach it buys; it means the three mechanisms §3 and §10 exist to enforce have a documented way around them, bounded only by who sent the message.
- **A worker's two branches can land apart.** The code lands, the doc branch fails its gate, and the suite ships an undocumented change — the failure §5.1's pairing is meant to prevent, and which only the supervisor's discipline actually prevents.
- **The usage budget is calibrated against nothing.** [running the fleet](embarch-parallel-agents-ops.md) §2's thresholds and its taper are guesses until several batches have run.
- **`git add -A` in the main checkout sweeps up whatever else is mid-edit.** Workers are safe — they are in worktrees (§5.1) — but the supervisor's phase-5 fold happens in the main checkout, so an owner committing everything while a batch is folding can land a half-written suite-level doc under an unrelated message. Observed twice on 2026-09-02, while this very doc was being written. Cheap habit: `git add <paths>`, not `-A`, in `embarch-doc` while a batch is running.

## 13. Running it

Starting a batch, sizing it against the real usage limits, watching it from a phone, and stopping it: [running the fleet](embarch-parallel-agents-ops.md).
