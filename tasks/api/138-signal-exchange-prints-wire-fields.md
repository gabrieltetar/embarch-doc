# 138 — Print the new `/signals/{name}/exchange` fields in the MCP `signal_exchange` text and the CLI

**State:** open
**Source:** embarch-core decision 85 (core task 098) — the exchange answer gained fields the api drops. Inbox drop `api-signal-exchange-prints-wire-fields.md`, filed 2026-10-26.
**Scope:** api
**Hardware:** none
**Owner:** no

## What

`POST /signals/{name}/exchange` now also returns `bytes_read`, `echo_seen`, `written`, `port_lost`, and, only when no byte came back, `port_identity` ({vendor_id, product_id, product, serial_number}) and `core_state` ({dhcsr, s_halt, s_sleep, s_lockup, s_reset_st, s_retire_st, unavailable?}). Add them to `embarch-core-client`'s response type (additive, defaulted so an older Core still parses) and make the MCP `signal_exchange` text and the CLI print them: a `port_lost` reply says the command ran, an empty reply names the echo/identity/core state. Do not tell the caller to resend a command whose reply says `written: true`.

## Why now

Core 098 stopped answering `500` for a command that ran; the api is the only reader of that answer, and an agent seeing only `text: ""` still cannot tell the failure modes apart.

## Done when

- [ ] `ExchangeResponse` in the client carries the new fields with serde defaults; a test parses an old-shape body and a new one.
- [ ] MCP text and CLI print `port_lost`, `echo_seen`, and the silent-case identity and core state.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10); `spec.md`/`decisions.md` updated, `changelog.d/` fragment dropped.
