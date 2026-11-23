# 095 — Atlas live tools work under a lease the same session holds

**State:** done
**Source:** Fleet Ready issue, a session running read-only bus and GPIO checks under a lease taken through embarch-api's MCP
**Issue:** EMB-233
**Scope:** atlas
**Hardware:** verify-only
**Owner:** no

## What

A session that took the bench lease with embarch-api's `lease_take` then got a
`409` naming its own lease from atlas's `shell` tool, so it had to give up the
atlas's read-only shell for the rest of the lease. The atlas live tools
(`shell`, and through the same Core calls `reg_read`, `live_stacks`,
`core_state`) reach Core by running the `embarch-api` CLI (`call_api` in
`live.py`), which reads `EMBARCH_LEASE_TOKEN` from its environment; the atlas
MCP server's environment was fixed when it started, so `lease_take`'s advice to
export the token cannot reach it. When this is done a session holding the lease
can use the atlas live tools without releasing it, and a `409` lease refusal is
reported as "did not run", since Core sent nothing. How the token reaches
`call_api` (for example an optional tool argument the agent copies from
`lease_take`'s result, passed to the CLI's environment and never logged) is the
worker's to decide and record; it stays inside `embarch-atlas` and changes no
`embarch-api` behaviour.

## Why now

Under a lease the atlas's read-only checks were unusable, and the refusal's
"may have run" told the agent a command might have reached the board when it
had not.

## Where

- `embarch-atlas/src/embarch_atlas/live.py`: `Console.exchange` and its
  `_NOT_WRITTEN` test, `shell_status` (which turns the refusal into "may have
  run"), and `call_api`.
- The atlas MCP tool definitions that call them.

## Done when

- [x] With a lease token supplied, the live tools pass it to the `embarch-api`
      CLI they run; a test shows it reaches the CLI's environment and no log
      or answer prints it.
- [x] A `409` lease refusal makes `shell` say the command did not run; a test
      covers it.
- [x] Hardware-verification debt written into this file: with the lease held
      through the embarch-api MCP, atlas `shell device list` in the same
      session returns the device list (a live Core and a board, which a worker
      does not touch).
- [x] Gate green (`../../embarch-fleet/gate.md`, the Python bullet).
- [x] `DESIGN.md` and `embarch-doc/embarch-atlas/design.md` updated where they
      describe the live tools, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false.

## Outcome

**Decision.** Every live MCP tool (`shell`, `shell_run`, `reg_read`, `reg_read_clear`, `reg_read_bank`, `live_stacks`,
`core_state`) takes an optional `lease_token` argument, the value `lease_take` returned. `live.lease(token)` holds it in a
context variable for that call; `call_api` passes it as `EMBARCH_LEASE_TOKEN` in the CLI child's environment only (never
argv), and every CLI failure text is scrubbed of it. Nothing stores or logs it. The atlas CLI's own `live` verbs inherit
the shell's variable and need no argument. `_NOT_WRITTEN` now also matches `409` and `lease`, so a lease refusal is "did
not run" (exit 1) and the next console is not tried. The refusal's exact wording is assumed (tests use two plausible
texts), not measured against a live Core. Tests: tests/test_live.py (token in env and not argv, released after the block,
blank ignored, scrubbed from a failure, `shell_read` passes it and prints none, 409 reads as did not run).

## Hardware-verification debt

With the lease taken through the embarch-api MCP (`lease_take`), in the same session call atlas `shell` with
`command: "device list"` and `lease_token` set to the token. Expect the device list, not a 409. Also confirm what text
Core's 409 carries for a wrong or missing token and that it still matches `409|lease` (a live Core and a board; a worker
touches neither).
