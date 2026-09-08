# `POST /validate`'s JSON body never picks up `validated_at_utc_ms`

**State:** open
**Source:** `tasks/topology/009` (embarch-doc), topology decision 26
**Scope:** core
**Hardware:** none

## What

`embarch-topology` decision 26 (2026-09-07) adds `validate_serial_timed`/
`validate_role_timed`, returning a new `Validation { board: EnrolledBoard,
validated_at_utc_ms: u64 }` alongside the unchanged `validate_serial`/
`validate_role` — additive, so nothing broke. `embarch-core`'s own
`POST /validate` handler is the piece that actually assembles the wire
response (`{ ok, role, hardware_id, confirmed_at_utc_ms }`) from an
`EnrolledBoard`, and it is a **direct in-process caller** of these functions
(topology is linked live, not called over the wire) — so it is the one place
that has to switch to the `_timed` variant and add `validated_at_utc_ms` to
that JSON body before the new field means anything to any consumer.

This is the consumer the supervisor's own enumeration for `tasks/topology/009`
did not name (it listed `embarch-api`'s core-client mirror and MCP tool,
`embarch-umbrella`'s doctor, `embarch-ui`'s Topology tab) — worth flagging on
its own, since without this half none of those four ever see the field.

## Why now

The observed defect (`tasks/topology/009`): two `validate` calls minutes or
days apart both return the same `confirmed_at_utc_ms`, which is enrolment
time, not the live check's — a caller reading it as freshness gets a
plausible, wrong answer, silently, in the safe-looking direction.

## Done when

- [ ] `POST /validate`'s handler calls `validate_role_timed`/
      `validate_serial_timed` and adds `validated_at_utc_ms` to the response
      body, alongside the unchanged `confirmed_at_utc_ms`.
- [ ] A decision records the wire-schema addition (this is `suite`-visible —
      four repos share this response shape by hand-maintained mirror), and
      `embarch-api`, `embarch-umbrella`, `embarch-ui` each pick it up in their
      own time since every existing mirror keeps deserializing regardless.
