# embarch-api: lease tools

**Status:** active, 2026-11-04. The client half of `embarch-core` decision 93's bench lease; why it is shaped this way: [decisions](../decisions/lease.md) 90, 101. See [tools.md](tools.md) for the one-table premise.

| Tool / subcommand | Params | Behaviour |
|---|---|---|
| `lease_take` | `holder?`, `purpose?`, `ttl_s?` | Core `POST /lease`. Core releases a lease after 30 minutes with no hardware call. Holds **both boards**; every other session's hardware call is refused `409` naming holder, purpose and expiry. `ttl_s` 1 to 14400; default 900 (MCP, renewed by a timer), 3600 (CLI, nothing renews). Returns the token **once**, with `token_env`; the CLI prints the `export` line. Refused with Core's text verbatim if another lease is live |
| `lease_renew` | `ttl_s?` | Core `PUT /lease`, with the token this process sends. The MCP server already renews on a timer; use it to change the TTL. `404` text when none is live, `409` when the token is not the live one |
| `lease_release` | — | Core `DELETE /lease`; the process forgets the token |
| `lease_show` | — | Core `GET /lease` (`404` text names an idle release: "released after 30 min with no hardware call"): holder, purpose, start, expiry, never the token; `lease: null` when none. `this_process_sends_a_token` says whether this process sends one; `this_process_requires_a_lease` whether `EMBARCH_REQUIRE_LEASE` is on. Never refused by a lease |

**Sending the token.** `X-Embarch-Lease` is attached to every Core request from, in order, the token this process took, then `EMBARCH_LEASE_TOKEN`. An `embarch-api` CLI call or an `embarch-atlas` live call (a subprocess of the CLI) sends it when that variable is in its environment, with no argument. A token taken by an MCP tool is in the server only until exported there.

**`status` also returns** `lease` (the live lease or `null`) and `last_images`: per chip `chip`, `probe_serial?`, `path`, `sha256?`, `flashed_at`, `lease_holder?` for the last image Core flashed or bootloaded since it started. Compare `sha256` with your own image before reflashing. **An absent chip means unknown, not nothing flashed.** An older Core gives `null` and `[]`.

**`status` also returns** `mode` (`service` or `development`) and `keyid` (the sealing key's fingerprint); `null` from a Core that predates them, which is unknown, not `service` (decision 139).

**A refused hardware call** (any tool or subcommand, including `validate`, `run_study`, `dev_bench_hello`) returns Core's `409` text unchanged: `bench leased by '<holder>' for '<purpose>' (started …, expires …); …`.

**A session made to hold the lease.** With `EMBARCH_REQUIRE_LEASE` in its environment (anything but empty or `0`), both front-ends ask `GET /lease` before a hardware route. With none live, the call fails without reaching the route: `no bench lease is live, and this session must hold one for hardware (EMBARCH_REQUIRE_LEASE is set): …`. A token left over from a dead lease does not help. With one live, the call goes on and Core decides by the token. Open routes, `lease_take` among them, are never affected. The routes are `lease_gate::LEASE_GATED`, a copy of Core's table.

**A lease Core released for idleness** (30 minutes with no hardware call), or one that expired or was lost with a Core restart: the renew answers `404` with Core's reason. The process then sends no token (`EMBARCH_LEASE_TOKEN` included), `lease_show` reports `this_process_sends_a_token: false`, and the next hardware call fails before reaching Core with that reason and "take it again with `lease_take`" (`lease-take`), with or without `EMBARCH_REQUIRE_LEASE`. `lease_take` clears it.
