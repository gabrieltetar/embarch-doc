# embarch-fleet: what is true now

**Status:** active, 2026-09-05. Shipped and in daily use — ten legs run, and the relay, the pump and the per-unit merge gate are all live.

The suite's own work is done in parallel by background agents, and this is the machine that runs them. A **supervisor** keeps four to six short-lived **workers** in flight, one repo each, on branches; it runs the gate itself, lands each unit, and writes the log. A **leg** is one supervisor's whole life — four units, then it dies and hands off to a successor through nothing but a written log entry.

**This is a sub-project whose docs live in another repo, and that is the design.** [`embarch-fleet`](../../embarch-fleet/README.md) holds the rules, the scripts that enforce them, and the agent definitions that carry them, because **a supervisor that can edit its own constraints has none** — a leg never checks that repo out, so there is no path from a leg's diff to a rule it runs under. An earlier attempt enforced the same thing with a denylist of filenames inside this repo and it broke: the risk register was §12 of the protocol until a size cap split it into its own file, and reserved content stopped being reserved purely by moving. Nothing noticed for a day.

So this directory is **one file on purpose**. `decisions.md`, `open.md` and `interfaces.md` are deliberately absent rather than missing: they exist as [protocol.md](../../embarch-fleet/protocol.md), [open.md](../../embarch-fleet/open.md) and [risks.md](../../embarch-fleet/risks.md) in the framework repo, and a second copy here would be a second source of truth about the rules an agent is running under — the one place in this suite where drift is not merely untidy.

## Invariants

- **Ownership is enforced, not described.** [protocol.md](../../embarch-fleet/protocol.md) §3 maps every path to who may write it, and `scripts/check-ownership.py` is what makes it true — of a worker's branch, and of the supervisor's own commits. `suite` and `fleet` are refused as worker scopes outright.
- **The claim commit is the interlock.** A task is claimed on this repo's `main`, one commit per task, pushed before the branch is cut. Two supervisors cannot claim the same task because one of them loses a race in git.
- **Nothing waits for everything.** A leg is a rolling wave: a finished worker's branches land, its fragments fold, its log entry is written and a new task starts in the freed slot at once.
- **A leg holds no authority over a standing rule.** Amending one is the owner's, from the owner's own window, and `check-ownership.py --supervisor` is what stops it happening any other way — including when the leg is right.
- **The log is the review surface**, and under full delegate it is the only one. One entry per unit, in the same commit as the fold; a unit that lands unlogged has failed.
- **Closing VS Code stops the fleet.** That is the kill switch, by design.

## Three windows

| Window | What it is | Hands |
|---|---|---|
| **Listener** | Armed with `/fleet start`. Reads **#embarch-fleet**, spawns agents, and reads exactly one thing itself — the dispatchable count, because the heartbeat needs a predicate | None. It never does work |
| **Legs** | One `embarch-supervisor` at a time, four units each, spawned by the listener while the pump latch is on. Each leg's death spawns the next until `fleet stop` | Everything except a standing rule |
| **The owner's** | An ordinary session. Standing rules, `scripts/`, `.claude/`, hardware, and drops into `inbox/` | Everything |

**There is no route from Slack to a standing rule**, for anyone, the owner included: the listener cannot write those paths and neither can any agent it spawns. The answer to a rule change asked for in the channel is "open your own window".

## What lives where

The **queue** stays in this repo — `tasks/`, `inbox/`, `status.d/`, `changelog.d/` — because the claim commit on this repo's `main` is the interlock, and the queue is a view of docs that live here. The framework repo ships their *protocol*; this repo holds their *contents*.

`supervisor-log.md` runs the other way: it is the fleet's own output, so it lives in the framework repo even though a leg writes it. That makes a unit's fold two commits in two repos, which reopens a window the protocol closed by making it one — so `scripts/fold-commit.py` commits both or neither.

**This repo's `.claude/`, its four protocol READMEs and its `scripts/` fleet shims are generated**, rendered from `embarch-fleet/templates/` by `install.py`. Edit the template, never the copy; `install.py --check` is a check in [`scripts/check-docs.py`](../scripts/check-docs.py) and is what catches the difference. **Nothing wires that into CI and nothing should**: CI checks out one repo and has no framework beside it to diff against, so the local wrapper — which every worker and every fold runs — is the guard.

**The denylist the fleet checks against lives outside every repo.** `check-client-names.py` (2026-09-05) refuses a client's name in a tracked file's contents or path or in a branch's commit messages, reading its names from the fleet's state directory, and it never prints what it matched. It is the ninth check in the wrapper for this repo, and the merge gate runs it again per code repo — the wrapper reaches 1.19 MB of the suite's 5.9 MB, and the 2026-09-04 leak it exists to prevent a repeat of was mostly on the other side.

## What it deliberately does not do

- **It does not approve anything routine.** The supervisor is a full delegate; review is after the fact, in the log.
- **It does not touch hardware.** No worker flashes a board, ever. A task needing one is `verify-only` at most, and leaves a debt.
- **It does not run in the owner's checkout.** A leg works in its own worktree; two actors in one working tree swept the owner's fragments into a fold twice.
- **It is not a general agent runner.** A leg executes queued task files against the ownership map. Work that arrives any other way — a Slack message that is not a `fleet` command — is outside the protocol by design, and [the risks](../../embarch-fleet/risks.md) says so.

## Pointers out

[README.md](../../embarch-fleet/README.md) is the entry point and says what each file is. Then [protocol.md](../../embarch-fleet/protocol.md) for the design, [ops.md](../../embarch-fleet/ops.md) for running it, [risks.md](../../embarch-fleet/risks.md) for what each choice traded away — in that order. [DEVELOPING.md](../../embarch-fleet/DEVELOPING.md) is how to change any of it. The queue's own protocols are [tasks/README.md](../tasks/README.md) and [inbox/README.md](../inbox/README.md), generated from the same templates.
