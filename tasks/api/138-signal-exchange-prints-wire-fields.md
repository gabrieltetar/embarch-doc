# 138 — Print the new `/signals/{name}/exchange` fields in the MCP `signal_exchange` text and the CLI

**State:** claimed by agent/api/138-signal-exchange-prints-wire-fields, 2026-10-26 01:20
**Source:** embarch-core decision 85 (core task 098) — the exchange answer gained fields the api drops. Inbox drop `api-signal-exchange-prints-wire-fields.md`, filed 2026-10-26.
**Scope:** api
**Hardware:** none
**Owner:** no

## Dispatch note, 2026-10-26

- **Read Core's side first:** `embarch-doc/embarch-core/decisions/signal-exchange.md` decision 85
  (and 79 as amended) is the contract for every field named below; the Rust type is in
  `embarch-core` (read-only for you; the main checkout is `/home/gabriel/Github/embarch/embarch-core`).
  `api/123` (landed an hour ago) gave `signal-exchange` exit codes 3/4/5 in decision 82
  (`decisions/failure-reporting.md`); keep those codes coherent with `port_lost` (decide and record
  whether a `port_lost` reply changes the exit code, and say why).
- **Shared crate.** `embarch-core-client` is path-depended on by `embarch-ui` and `embarch-umbrella`.
  Keep the change additive with `#[serde(default)]`; grep those two repos for any struct-literal
  construction of the response type and say in your report what you found (you may not edit them).
- **Doc reserve:** nothing in `embarch-api/` is in reserve, but `decisions/client-crate.md` is
  10,941 B (reserve line 11,059 B, 118 B away) and `decisions/zephyr.md` 10,812 B. If your work
  pushes either into reserve, file `tasks/api/<next NNN>-compact-api.md` in the same commit
  (`scripts/check-task-numbers.py --next api`), per `tasks/README.md`'s compaction shape.

## What

`POST /signals/{name}/exchange` now also returns `bytes_read`, `echo_seen`, `written`, `port_lost`, and, only when no byte came back, `port_identity` ({vendor_id, product_id, product, serial_number}) and `core_state` ({dhcsr, s_halt, s_sleep, s_lockup, s_reset_st, s_retire_st, unavailable?}). Add them to `embarch-core-client`'s response type (additive, defaulted so an older Core still parses) and make the MCP `signal_exchange` text and the CLI print them: a `port_lost` reply says the command ran, an empty reply names the echo/identity/core state. Do not tell the caller to resend a command whose reply says `written: true`.

## Why now

Core 098 stopped answering `500` for a command that ran; the api is the only reader of that answer, and an agent seeing only `text: ""` still cannot tell the failure modes apart.

## Done when

- [x] `ExchangeResponse` in the client carries the new fields with serde defaults; a test parses an old-shape body and a new one.
- [x] MCP text and CLI print `port_lost`, `echo_seen`, and the silent-case identity and core state.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10); `spec.md`/`decisions.md` updated, `changelog.d/` fragment dropped.

## Result, 2026-10-26

Decision 82 amended (`decisions/failure-reporting.md`): `port_lost` exits 5, silent stays 4. No struct-literal construction of `SignalExchangeResponse` in `embarch-ui` or `embarch-umbrella` (grep of `*.rs`, none at all). Not verified against a real Core. `decisions/client-crate.md` untouched, still 118 B from reserve.
