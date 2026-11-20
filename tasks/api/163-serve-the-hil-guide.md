# 163 — `embarch-api guide hil <mode>` serves the HIL guide embedded at build, and an `embarch-hil` skill points at it

**State:** done — resumed after the 14:39 claim's worker died with its leg; its trees were verified and one test fixed
**Source:** Fleet Ready issue: the HIL guide has to reach an agent on any machine, not only one with an `embarch-doc` checkout. `notes/hil/14-implementation-plan.md`, unit M1.12, and its Open item "Where `suite/hil-guide.md` is embedded from"; `notes/hil/07-procedure-doc.md`, "Its form" (review round 4, owner 2026-11-20).
**Issue:** EMB-227
**Scope:** api
**Hardware:** none
**Owner:** no

## What

- **`embarch-api guide hil <mode>`**, a subcommand, prints the HIL guide's section for one mode (`live`, `study`, `test`), and with no mode the "which mode" part. The text is embedded in the binary at build, so it is the guide that matches the tools it describes, and it needs no `embarch-doc` on disk. An unknown mode exits non-zero and lists the modes.
- **An `embarch-hil` skill shipped in the `embarch-api` repo**: it loads when a task needs hardware, holds the "which mode" table (`notes/hil/01-modes.md`, "How an agent picks a mode"), and points at `embarch-api guide hil <mode>` for each mode. The precedent for the shape is `embarch-atlas`'s `skills/atlas-use/SKILL.md`.

## Why now

The plan marks M1.12 as needing nothing, and the owner moved it to Fleet Ready with M1.1 and M1.4.

## Dispatch notes

- **The guide's text does not exist yet.** `suite/hil-guide.md` is M1.13, written interactively after `publish` and `verify` land. So this unit ships the mechanism and a skeleton: a section per mode, each saying plainly that it is not written yet and naming where the design is (`embarch-hil-proposal.md`). Do not write the procedure itself, and do not invent one from the notes.
- **Where the embedded text comes from is this unit's decision** (the plan leaves it to the unit): a pinned copy in this repo kept in step with `suite/hil-guide.md`, or a build-time read of a pinned `embarch-doc`. Say in the decision how a guide edit reaches the binary, and what catches the two drifting apart. A build that reads a sibling repo by relative path breaks a worktree build and a published crate, so weigh that.
- **Installing the skill is `embarch-umbrella`'s** (`embarch init`, per `embarch-hil-proposal.md`'s table) and is out of scope; say in `open.md` that it is owed.
- Decisions within 256 B of their limit: `ledger#98` (15 B), `bench-exchange#89`, `failure-reporting#67`. You should not need them.

## Done when

- [x] `embarch-api guide hil study|test|live` prints that mode's section, and a test runs the built command from a directory with no `embarch-doc` reachable.
- [x] The `embarch-hil` skill exists in this repo and every pointer in it names a command that resolves.
- [x] A decision records where the embedded text comes from and how a guide edit reaches the binary.
- [x] `spec.md`, `decisions.md`, `open.md` and the CLI interface doc updated; `changelog.d/` fragment dropped.
- [x] Gate green (`../../embarch-fleet/gate.md`; `check-ownership.py --scope api` on both branches).

## Outcome

Built and verified on resume: the dead worker's code was sound; the only defect was `cli.rs`'s subcommand-count tripwire and `tests/json_surface.rs` not knowing `guide` (fixed), and three comments citing decision 99 instead of 108. Embedded text is a pinned copy `guide/hil-guide.md` (decision 108), drift-tested where `embarch-doc` is reachable. Skill install by `embarch init` is owed by `embarch-umbrella` (in `open.md`). No hardware debt.
