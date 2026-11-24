# 033 — The permissions command names only tools `embarch-api` serves

**State:** open
**Source:** reviewer of `api/178` (2026-11-23): `embarch-api` removed the `instrument_exchange` tool, and `embarch-chat`'s permissions command still lists it
**Issue:** EMB-287
**Scope:** chat
**Hardware:** none
**Owner:** no

## What

`plugin/commands/embarch-permissions.md` writes permission lists into a
project's settings, and it still lists `instrument_exchange` under ask. Its
note on deliberate tools names it too. `embarch-api` removed that tool and its
CLI verb in `api/178` (decision 97 amended): Core refuses the route outside a
run, and a lab supply or load is reached only by a host study's `Instrument`
step, run with `run_host_study`. The suite's agent guide (`suite/agent-guide.md`
§1.1) already says so.

When this is done, the command's lists name no tool that `embarch-api`'s
`src/tools.rs` does not register (read it on `origin/main`), and its prose no
longer mentions `instrument_exchange` as a tool. If the comparison turns up a
tool `tools.rs` registers that the command does not list at all, add it under
ask and name it in the changelog fragment. Moving a tool between allow and ask
is not this unit's job. EMB-269 revises that policy in the agent guide first.

## Why now

A user who runs the command today grants a tool that no longer exists, and the
command's account of how a supply is reached is now wrong.

## Done when

- [ ] The permissions command names no tool that `embarch-api`'s `src/tools.rs` does not register.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10): `embarch-chat`'s npm gate and the doc gate.
- [ ] A `changelog.d/` fragment dropped, and `embarch-doc/embarch-chat/` updated if it describes the command's lists.
