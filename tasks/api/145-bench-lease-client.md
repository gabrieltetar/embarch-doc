# 145 — The bench lease client: the MCP server and CLI take, renew and send the lease token

**State:** done 2026-10-26 (branch agent/api/145-bench-lease-client)
**Source:** `tasks/core/099` (embarch-core decision 93, `embarch-core/decisions/lease.md`): Core now serves `/lease`; with none live every route behaves as before, so nothing breaks until a session takes one. Field use on a USB PD charger board, 2026-10-08 to 2026-10-20: two Claude sessions shared one DUT and one bench board through a `mkdir` lock directory because no lease existed. Filed from `inbox/api-bench-lease-client.md` by the 2026-10-26 leg.
**Scope:** api
**Hardware:** verify-only — every box below is testable against a scripted Core (the client's existing mock pattern); the run against an installed Core with two real sessions is the hardware-verification debt. Reclassified from the drop's `none` on filing.
**Owner:** no

## Supervisor note, 2026-10-26 leg

`embarch-atlas` reaches Core only by running the `embarch-api` CLI as a subprocess (`embarch-atlas/src/embarch_atlas/live.py:85-99`, `subprocess.run`), so an environment variable that `embarch-api` reads on every Core call reaches atlas's live calls with **no change to `embarch-atlas`**. That makes the env-var arm of "pick one" below the one that satisfies the third `Done when` box without leaving this scope. You may still pick the per-process arm, but then the atlas box needs a cross-repo drop, and decision text must say why.

**Doc reserve in your scope (dispatch, 2026-10-26 06:31):** `embarch-api/decisions/client-crate.md` 11,581 / 12,288 B (707 B left, filed `api/140`, open) and `embarch-api/open.md` 4,034 / 5,120 B (1,086 B left, filed `api/144`, open). Put the lease decision in a new topic file under `embarch-api/decisions/` (indexed in `decisions.md`) rather than growing `client-crate.md`; both debts are already filed, so you owe no new compaction task unless you push a third file into reserve. `embarch-core-client` is a shared crate (`embarch-ui` path-depends on it): keep its changes additive (new optional fields, new calls), and say in your report exactly which public items you added.

## What

Core's lease: `POST /lease {holder, purpose?, ttl_s}` returns `201` `{token, holder, purpose, started_at, expires_at, ttl_s}` (ttl 1..=14400 s; `409` naming the holder if one is live); `PUT /lease {ttl_s?}` renews and `DELETE /lease` releases (`204`), both with the token in the `X-Embarch-Lease` header; `GET /lease` returns the view without the token or `404`. While one is live, every hardware route without that header is `409` with a plain-text body naming holder, purpose, start and expiry. It covers the whole bench (both boards). `GET /status` gains two additive fields, `lease` (view or `null`) and `last_images` (per chip: `chip, probe_serial?, path, sha256?, flashed_at, lease_holder?`; absent means unknown); `embarch-core-client`'s decoding of `/status` must keep ignoring unknown fields or add these as optional.

Build the client half: MCP tools and CLI subcommands to take, renew, release and show the lease, and a way for every other call to send the token. **The token must reach `embarch-atlas`'s live calls and subagents without each remembering a rule**, so carry it in an environment variable (for example `EMBARCH_LEASE_TOKEN`) that `embarch-api` reads on every Core call and sends as `X-Embarch-Lease`, or a per-process lease the MCP server takes on its own at first hardware call and renews while the process lives. Pick one and record why. A `409` from Core should surface the refusal text verbatim, so a session sees who holds the bench and until when. Renewing must not depend on a model remembering to: renew on a timer inside the MCP server, or take short TTLs and renew on each call.

## Why now

Without this the lease exists and no session can use it; the lock-directory stopgap (62 holds, 80 reflashes after taking it) stays in force.

## Done when

- [x] The MCP server and CLI can take, renew, release and show a lease, and send the token on every Core call.
- [x] A session that did not take the lease gets Core's `409` text through the tool, naming the holder.
- [x] The token reaches a second process (an `embarch-atlas` live call) with no per-call argument.
- [x] `last_images` is exposed where a session can compare `sha256` with its own image before reflashing.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped.

## Done

Decision 90 (`embarch-api/decisions/lease.md`): the env-var arm. `CoreClient::dispatch` sends `X-Embarch-Lease` from the process's own lease, else `EMBARCH_LEASE_TOKEN`, on every call; the MCP server spawns `lease_keepalive` (renews at a third of the TTL); a lease `409` becomes `LeaseHeldError` with Core's text verbatim, ahead of the three other `409` meanings (`validate`, `post_study`, `dev_bench_hello`). Tools `lease_take`/`lease_renew`/`lease_release`/`lease_show` and CLI twins; `status` returns `lease` and `last_images`. Tests: `tests/lease_client.rs` (11, mock Core, including the real binary with the variable set and a refusal on stderr), the bearer sweep extended with the four `/lease` routes.

Atlas: no change to `embarch-atlas`; its live calls inherit the variable if it is in the environment they are launched with. A token taken through an MCP tool is not exported anywhere automatically (recorded in `open.md`).

## Hardware-verification debt

Run on a real installed Core with the new client and two sessions: (1) session A `lease-take`, export the token, `status` shows `lease`; (2) session B `reset` or `flash` gets the `409` text naming A; (3) A's MCP server stays leased past its TTL with no manual renew (use `ttl_s` 30 and wait 60 s); (4) an `embarch-atlas` live call with the variable exported succeeds while B is refused; (5) after a flash `status.last_images` shows the image's `sha256`. Needs embarch-core at or after 5063c0b deployed (it is not).
