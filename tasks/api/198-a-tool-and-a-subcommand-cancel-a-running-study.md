# 198 — A tool and a subcommand cancel a running study

**State:** open
**Source:** EMB-487 — no tool or button cancels a running study (the api half; the UI button is `ui/122`)
**Issue:** EMB-487
**Scope:** api
**Hardware:** none
**Owner:** no

## What

Core's `POST /study/{id}/cancel` now stops a device study as well as a host
study (Core decision 128, which sends `StudyStop{Cancel}` to the dev bench),
and during a Test run it is the one study route the run lock admits (Core
decisions 135 and 137). No embarch-api client calls it: there is no cancel tool
or subcommand. When this is done, `cancel_study` (MCP) and `cancel-study <id>`
(CLI) share one implementation, take the lease token as every gated call does,
and report the study's end as Core records it. Anyone who started the wrong
study, or a session that must end before its cap without its Done prompt, can
then stop it.

## Where to look

- `src/tools.rs`, `src/main.rs` (the MCP and CLI twins, and the parity test)
- `src/host_study.rs` — the host-study prompt relay, the nearest neighbour
- `crates/embarch-core-client/` — the client crate; `lease_gate.rs` already
  lists the route
- `embarch-doc/embarch-core/decisions/stopping-a-study.md` (128) for what Core
  answers

## Where the doc goes

`interfaces/tools-host-study.md` (1,377 B) or the interface file the tool fits
best, and `interfaces/tools.md`'s index. A decision only if you choose
something a reader would need; **do not grow decisions 90 (`lease.md`, 504 B
over its per-decision limit), 98 (`ledger.md`, 15 B left) or 134
(`test-plans.md`, 490 B over)**. If your work pushes any file into reserve, file
`tasks/api/<NNN>-compact-api.md` in the same commit per `tasks/README.md`.

## Done when

- [ ] The tool and the subcommand cancel a study against a mock Core, and the
      parity test passes.
- [ ] A cancel of an unknown or ended study reports Core's refusal.
- [ ] Gate green.
