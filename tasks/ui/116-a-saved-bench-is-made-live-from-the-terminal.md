# 116 — A saved bench is made live from the terminal

**State:** open
**Source:** HIL implementation plan (`notes/hil/14-implementation-plan.md`, Test phase): "the CLI does the same in the person's terminal, so a Test needs no UI" (`notes/hil/03-test.md`, "Benches")
**Issue:** EMB-386
**Scope:** ui
**Hardware:** none
**Owner:** no

## What

Make live is `api_make_live` in the UI server
(`embarch-ui/src/bench/live.rs`), reached only from the Topology tab. A Test
needs no UI, so the person must be able to make a saved bench live from a
terminal.

When this is done the UI binary has a subcommand, in the plan's recommended
shape (kept by the owner, `14-implementation-plan.md` line 64):

    embarch-ui bench make-live <slug> [--config <name>] [--bind <role>=<serial>...]

run in the person's terminal: the saved bench's declarations applied with the
person's token, each proposed probe binding printed, the ones given with
`--bind` applied, and the live record written as the tab writes it. It calls
**the same functions the route calls** (`api_make_live`'s body factored so the
route and the subcommand share it, `take_machine` likewise), so the two cannot
disagree. Subcommands go in `src/main.rs` beside the binary's existing ones.

Docs, in `embarch-doc/embarch-ui/`: amend decision 90
(`decisions/bench-live.md`) in place to say Make live has a terminal form and
that it shares the route's code; `spec.md` and the interface doc that lists the
binary's subcommands, if one does.

## Why now

An engineer with no browser open, and the setup prompt between benches in a
Test, both need it. EMB-386.

**Burndown leg: no new numbered decision.** Amend decision 90 in place; if the
change seems to need a new decision, stop and say so in this file.

**Doc-size reserve (dispatch note):** no `embarch-ui` file is in reserve.
Decisions near their per-decision limit (`check-doc-size.py --pressure`):
launcher#28 22 B, tab-folders#100 113 B, topology-tab#10 141 B,
topology-tab#43 207 B, plus several pinned ones. Do not grow those.

## Done when

- [ ] Against a fake Core, the subcommand on a fixture bench sends the same
      declarations the route sends, with the person's token.
- [ ] A binding not given is printed as proposed and not applied.
- [ ] The live record the tab reads shows the bench live.
- [ ] Gate green (`../../embarch-fleet/gate.md`).
- [ ] Decision 90 amended; `spec.md` updated; `changelog.d/` fragment dropped.
