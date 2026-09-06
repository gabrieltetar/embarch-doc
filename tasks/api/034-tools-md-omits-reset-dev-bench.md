# `interfaces/tools.md` omits `reset_dev_bench`; add a CLI↔MCP parity test

**State:** open
**Source:** owner's repo survey, 2026-09-06 — `interfaces/tools.md:5`'s own premise is unchecked
**Scope:** api
**Hardware:** none
**Owner:** no

## What

`src/tools.rs:772-790` defines the `reset_dev_bench` MCP tool and `src/main.rs:325` /
`src/cli.rs:91` its `reset-dev-bench` CLI half. `embarch-doc/embarch-api/interfaces/tools.md:40-44`'s
"Dev bench" table lists only the three build/flash tools. The doc's whole premise is "**One table,
because these are two front-ends over one implementation** — not two surfaces to keep in sync"
(`tools.md:5`), and nothing checks it.

Add the missing row, carrying the reason the tool description already gives (flashing halts the
core rather than starting it running). Then add a test that derives the tool list from
`include_str!("../src/tools.rs")` and the subcommand list from `include_str!("../src/main.rs")` and
asserts every tool has a kebab-case subcommand — with the two documented asymmetries (`versions`
CLI-only, `study_watch` reached as `study-status --follow`) as a **named constant with a comment**
pointing at `spec.md` §1, never an inline skip.

## Why now

`spec.md` §1 asserts the CLI is a superset with "`versions` having no tool", and
`suite/studies-guide.md:45` already tells an engineer to run `reset-dev-bench` — a command the
interface reference does not list.

## Done when

- [ ] `interfaces/tools.md`'s Dev bench table lists `reset_dev_bench`.
- [ ] One test fails if a new `#[tool]` gains no matching `Commands::` variant, or vice versa,
      outside the two named exceptions.
- [ ] The exception list is a named constant with a comment, not an inline skip.
- [ ] `tools.md` stays inside its size cap.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false.
