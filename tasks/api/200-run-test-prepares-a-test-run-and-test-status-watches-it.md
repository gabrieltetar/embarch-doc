# 200 — `run_test` prepares a Test run and `test_status` watches it

**State:** claimed by agent/api/200-run-test-prepares-a-test-run-and-test-status-watches-it, 2026-11-25 12:33
**Source:** EMB-377 — an agent cannot prepare a Test run or watch one
**Issue:** EMB-377
**Scope:** api
**Hardware:** none
**Owner:** no

## What

The agent selects tests, resolves them into the resolved run file, shows the
preview, and waits for the engineer's go. No tool takes a test selection today.
The design: "`run_test` prepares a run and never starts one: embarch-api sends
`run.json` and its definitions to Core with the agent's token"; "the agent may
show the same preview in the chat as a convenience"; "one `test_status` call
answers the current bench, the current test, the verdicts so far, and a waiting
prompt with its text, from any session" (`notes/hil/03-test.md`, "Selecting and
rerunning" and "A run", item 6).

- **`run_test`** (MCP tool and CLI twin): takes a plan, or a suite and test ids
  or tags; resolves through `embarch-study-designer`'s `expand` with the plan's
  DUT inputs and the benches the project has; sends `run.json` and its
  definitions to Core's `POST /test-runs`; returns the run id and Core's card
  data as the preview: tests per bench, prompts with their kinds, what will be
  powered, unconfirmed inputs, the duration bound. It says the engineer gives the
  go on the card or in the terminal, and **calls no go**.
- **`test_status`**: `GET /test-runs/{id}` (core decision 136), with each study's
  own status underneath on request.
- **`answer_prompt`** stays the relay for setup and action prompts. For a Test
  run's prompt it shows the kind; an observation's or a clearance's `403` (core
  decision 138) says the person answers it on the card or in the terminal. A
  setup prompt (core decision 139) is one the agent may relay.
- A spec named with no plan lists the applicable tests and asks, as
  `notes/hil/01-modes.md` says.

Every Core call goes through `embarch-core-client`'s one funnel; add client
methods for `POST /test-runs` and `GET /test-runs/{id}` if they are missing.
That crate is shared with `embarch-ui`, so additive methods only.

## Where to look

- `embarch-api/src/tools.rs`, `src/cli.rs`, `src/host_study.rs`
- `embarch-api/crates/embarch-core-client/src/client.rs`
- `embarch-core/interfaces/test-runs.md` (the routes, the card, `waiting_prompt`)
- `embarch-api/interfaces/tools-host-study.md`; `embarch-api/decisions/host-study.md` (99)
- `embarch-api/decisions/test-plans.md` (134: `test_propose` never confirms)

## Where the doc goes

`interfaces/` gives both tools; the subcommand count and the parity test move
with them. **Decision 134 is 490 B over its entry limit and decision 90 (lease)
504 B over** (`check-doc-size.py --pressure`): put this unit's design in a new
decision rather than growing either. No `embarch-api` file is in reserve at
filing. If your work pushes one in, file `tasks/api/<NNN>-compact-api.md` in the
same commit per `tasks/README.md`.

## Done when

- [ ] Against a fake Core, `run_test` on a fixture plan sends the `run.json` the
      crate gives and returns the preview with an unconfirmed input listed.
- [ ] No code path in the MCP server or the agent's CLI calls the go.
- [ ] `test_status` returns the current bench, test, verdicts so far and a
      waiting prompt.
- [ ] `interfaces/` gives both tools.
- [ ] Gate green, the client crate included.
