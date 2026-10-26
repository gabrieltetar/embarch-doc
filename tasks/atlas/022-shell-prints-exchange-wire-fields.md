# 022 — `shell` prints what the exchange says happened on the wire

**State:** open
**Source:** embarch-core decision 85 (core task 098); an atlas report said "the command did not run" for a `500` after the command ran. Inbox drop `atlas-shell-prints-exchange-wire-fields.md`, filed 2026-10-26.
**Scope:** atlas
**Hardware:** none
**Owner:** no

## What

Core's `/signals/{name}/exchange` answer now has `written`, `port_lost`, `echo_seen`, `bytes_read` and, when silent, `port_identity` and `core_state` (DHCSR flags). Make the atlas `shell` command read them: `port_lost: true` is reported as "the command ran, the port dropped, here is the first output" and is never retried; a silent reply prints the echo verdict, the port's VID/PID/product and the core state (or why it is unavailable). A `500` from an open or write failure says nothing was written, so a resend is safe there only.

## Why now

On 2026-10 a command that turns the DUT's USB off ran and the exchange answered `500`; the report said it did not run and it was sent twice.

## Done when

- [ ] `shell` prints the new fields; a test feeds a `port_lost` body and asserts the "ran" wording and no retry advice.
- [ ] A silent body prints identity and core state.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10); `changelog.d/` fragment dropped.
