# 033 — The permissions command writes the agent guide's lists, for both MCP servers

**State:** open
**Source:** reviewer of `api/178` (2026-11-23): `embarch-api` removed the `instrument_exchange` tool, and `embarch-chat`'s permissions command still lists it. Widened at the split of a second issue the same day: `doc/099` revised the agent guide's lists, and the command's copy now disagrees with them.
**Issue:** EMB-287
**Issue:** EMB-291
**Scope:** chat
**Hardware:** none
**Owner:** no

## What

`plugin/commands/embarch-permissions.md` writes permission lists into a
project's settings. Its copy of those lists is dated 2026-10-29, and the
suite's agent guide (`suite/agent-guide.md` §1.1) was revised on 2026-11-23
(`doc/099`). Read §1.1 on `origin/main`: it is the source, and this command is
a copy of it.

When this is done, the command writes exactly §1.1's allow and ask lists, for
both MCP servers:

- **`embarch-api`.** Ten tools moved from ask to allow because the bench lease
  gates them and Core refuses them during a run: `reset`, `reset_dev_bench`,
  `signal_exchange`, `mem_read`, `core_state`, `bench_exchange`, `validate`,
  `lease_take`, `lease_renew`, `lease_release`. `build_each`, `bundle`,
  `call_log` and `study_measurements` are allow, and `publish` is ask. The
  command's step 1 sends tools "in neither list" to ask, so check that no tool
  §1.1 places lands there by default.
- **The atlas's server.** The command writes no block for
  `mcp__embarch-atlas__*` today. Add one, with §1.1's allow and ask lists.
- **`instrument_exchange` is gone.** `embarch-api` removed the tool and its CLI
  verb in `api/178`. A lab supply or load is reached only by a host study's
  `Instrument` step, run with `run_host_study`. No list and no prose names it
  as a tool.

Cross-check the `embarch-api` lists against `src/tools.rs` on `origin/main`
(the guide counts 58 tools), and the atlas lists against the atlas's
`src/embarch_atlas/mcp_server.py`. If §1.1 and the code disagree, follow §1.1
and say so in your report: the guide is the supervisor's, so a fix to it is a
`status.d/` fragment, never an edit.

## Why now

A user who runs the command today grants a tool that no longer exists, and gets
a prompt on every Live reset and read that the guide says should be free.

**Burndown leg: no new numbered decision.** If a decision needs amending, amend
it in place. If the work needs a new decision, stop and say so in this file and
in your report.

## Done when

- [ ] Every tool in the command's allow and ask lists sits in the same list in §1.1, for both servers.
- [ ] The command writes a block for `mcp__embarch-atlas__*`.
- [ ] No list and no prose names `instrument_exchange` as a tool.
- [ ] Gate green (`../../embarch-fleet/gate.md`): `embarch-chat`'s npm gate and the doc gate.
- [ ] A `changelog.d/` fragment dropped, and `embarch-doc/embarch-chat/` updated if it describes the command's lists.
