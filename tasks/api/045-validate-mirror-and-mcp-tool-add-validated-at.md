# `validate`'s response mirror and MCP tool should show `validated_at_utc_ms` when Core sends it

**State:** open — unblocked by leg 042 when `tasks/core/026` landed
(`embarch-core` `b0bf60d`, decision 50). `POST /validate` now serves
`validated_at_utc_ms`, so both mirrors in this repo have something real to
carry. This is now the head of the chain: `tasks/umbrella/041` and
`tasks/ui/020` are blocked on *this* task where they read Core through
`embarch-api`'s mirror.
**Source:** `tasks/topology/009` (embarch-doc), topology decision 26
**Scope:** api
**Hardware:** none
**Blocked on:** `tasks/core/026-validate-handler-wires-validated-at.md`. Core's
`POST /validate` handler is what assembles the wire body; until it calls the
`_timed` variant the field is on no wire and there is nothing here to mirror.
Unparks the moment `core/026` lands.

## What

`embarch-topology` decision 26 adds a second `validate` timestamp,
`validated_at_utc_ms` — when the live hardware-ID check ran — additive
alongside the existing `confirmed_at_utc_ms`, which is enrolment time and does
not move on a successful re-check. Once `embarch-core`'s `POST /validate`
picks the new field up (a separate inbox drop, `core-validate-handler-wires-
validated-at.md`), this repo has two hand-maintained mirrors of that response
shape to update: `crates/embarch-core-client`'s response struct, and the MCP
`validate` tool's output.

**This is additive, and nothing here is urgent on its own** — the existing
field name and shape are unchanged, so both mirrors keep deserializing with no
edit at all. This drop exists so the new field is enumerated as a consumer
before anyone reaches for `confirmed_at_utc_ms` expecting it to answer "how
stale is this check," which is exactly the defect `topology/009` observed.

## Why now

Not urgent — filed so the fix is visible once Core sends the field, per the
`topology/009` supervisor direction to enumerate every consumer of this
response shape before it changes.

## Done when

- [ ] `crates/embarch-core-client`'s `validate` response type gains
      `validated_at_utc_ms` once Core's own response carries it.
- [ ] The MCP `validate` tool surfaces it (both timestamps, distinctly
      labelled — not one replacing the other).
