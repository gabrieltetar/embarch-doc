# 178 — The instrument_exchange tool and CLI verb are gone; run_host_study names the Instrument step

**State:** done — tool, CLI verb and client call removed; docs amended
**Source:** notes/hil/05-live.md — "Reach and permission": an instrument is reached only through a Study or a Test
**Issue:** EMB-257
**Scope:** api
**Hardware:** none
**Owner:** no

## What

Core now refuses `POST /instruments/{name}/exchange` to every caller, `409`,
naming a host study's `Instrument` step as the way in (`embarch-core` decision
104, amended by `tasks/core/142`). So `embarch-api`'s `instrument_exchange` MCP
tool and its `instrument-exchange` subcommand can only fail, and the tool's text
("Send one SCPI command to a declared bench instrument … Refused 409 while a
study holds the bench") describes behaviour that no longer exists. When this is
done:

- `src/tools.rs` registers no `instrument_exchange`, and the CLI has no
  `instrument-exchange` (`src/main.rs`'s `Commands::InstrumentExchange`,
  `src/cli.rs`, `src/instrument.rs`). Remove what only they used, including the
  client crate's call if nothing else uses it; say in the report what you kept
  and why.
- `declare_instrument`, `list_instruments`, `remove_instrument` and
  `run_host_study` stay. `run_host_study`'s description says an instrument is
  reached by an `Instrument` step.
- Any permission list, tool count or tool table in the repo that names the tool
  is updated with it.

## Why now

The owner chose this on 2026-11-23: Core keeps the route and refuses it outside
a run, and the tool and the CLI verb go. Core's half landed as `tasks/core/142`.

**Burndown leg: no new numbered decision.** Amend decision 97
(`decisions/instruments.md`) in place. If any suite-level doc names the tool
(`suite/agent-guide.md` does), that is a `status.d/` fragment for the
supervisor, never your edit; if the pinned HIL guide copy in this repo changes,
the fragment carries the exact replacement text, because the drift guard
compares the two.

## Done when

- [x] `tools.rs` registers no `instrument_exchange`, and the CLI has no
      `instrument-exchange`.
- [x] `run_host_study`'s description names the `Instrument` step as the way to
      an instrument.
- [x] `interfaces/tools-instruments.md`, `interfaces/tools.md` and decision 97
      are amended.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment
      dropped, `status.d/` fragment for anything suite-level it made false.
