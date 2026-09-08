# `POST /validate`'s JSON body never picks up `validated_at_utc_ms`

**State:** claimed
**Source:** `tasks/topology/009` (embarch-doc), topology decision 26
**Scope:** core
**Hardware:** none

## Supervisor direction (leg 042)

**This is not a wire-schema bump and does not take the §8 announcement route,
and the reasoning matters more than the conclusion.** `ops.md` §4 parks "any
change that bumps a wire schema version". This adds a field and changes
nothing that exists: `ok`, `role`, `hardware_id` and `confirmed_at_utc_ms`
keep their names, types and meanings, so every one of the four hand-maintained
mirrors keeps deserializing untouched, and `embarch-core/interfaces/topology.md`
already documents this response as open-ended rather than a closed schema
(`topology/009`'s reviewer checked exactly that). **If you find that
characterisation is wrong** — the response is declared closed somewhere, or a
mirror uses `deny_unknown_fields`, or there is a version constant to move —
**stop and write it into this task file rather than proceeding.** That would
make this a `suite` unit that a `core` worker may not land.

**Do not rename or re-meaning `confirmed_at_utc_ms`.** The previous leg closed
that arm deliberately: it is wire-visible across four repos and is `suite`
work. Both timestamps ship side by side.

**Keep `validate_serial`/`validate_role` callable.** Topology deliberately
left the old signatures intact and added `_timed` variants; your job is to
switch Core's `POST /validate` handler to the `_timed` variant, not to remove
anything.

**Record the addition as an `embarch-core` decision.** `decisions/surfaces.md`
is the likely home (5,809/12,288 B — plenty of room) unless the file layout
says otherwise; the decision should say the field is additive, that four repos
mirror this shape by hand, and that the three consumers are already filed
(`tasks/api/045`, `tasks/umbrella/041`, `tasks/ui/020`, all blocked on this
task).

**Doc-size reserve for `core`:** `embarch-core/open.md` is at 4,478/5,120 B —
**642 bytes left**, and its compaction task `tasks/core/022-compact-core.md` is
**blocked on `In flux: yes`**. Prefer not to write `open.md` at all. If your
work genuinely needs an open question recorded there, compact that file as
part of this unit, carrying `tasks/core/022`'s `Must not delete:` list and
closing only `open.md`'s item on it. Every other `embarch-core` doc has room.

**Hardware:** none, and do not touch the live Core, the bench, or any board.
This is a handler change plus host tests.

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
