# 029 — `spec.md` says Core's `POST /validate` "does not yet expose" `validated_at_utc_ms`; it does

**State:** open
**Source:** refill sweep, leg 087, 2026-09-11. `embarch-topology/spec.md` and
`decisions/validate-timing.md`, checked against `embarch-core/src/api.rs` and against
`embarch-core/interfaces/topology.md`, which already records the field as landed.
**Scope:** topology
**Hardware:** none — the evidence is Core's handler and its own interface doc, both readable.
**Owner:** no

## What

`embarch-topology/spec.md` still says *"`embarch-core`'s `POST /validate` does not yet expose it"*
about `validated_at_utc_ms`, and `decisions/validate-timing.md` carries the matching forward-looking
clause — *"the new field only reaches the wire once its own `/validate` handler switches to
`validate_role_timed`"*. **That switch happened.** `embarch-core/src/api.rs` calls
`embarch_topology::hardware::validate_role_timed`, declares `validated_at_utc_ms: u64` on
`ValidateOkResponse`, and populates it from `validation.validated_at_utc_ms`.
`embarch-core/interfaces/topology.md` already says so, citing `embarch-core` decision 50.

Retire both stale clauses against that evidence. **The decision's clause is a condition that fired,
not a sentence to delete**: write it as satisfied, naming `embarch-core` decision 50, so the
sequencing stays readable rather than looking as though the field was always on the wire.

## Why now

This is a precondition that came true and told nobody. A reader of `embarch-topology` is currently
told a field they can use today is unavailable, which is the shape of staleness that costs somebody
an afternoon building around an absence — and it is a disagreement between two sub-projects' docs,
so no single-repo check can see it.

## Done when

- [ ] `spec.md`'s "does not yet expose it" sentence is gone, replaced by what is true now with a
      citation to `embarch-core` decision 50.
- [ ] `decisions/validate-timing.md`'s forward-looking clause reads as a fired condition, not as a
      pending one, and does not claim more than Core's handler actually does.
- [ ] Nothing in this crate's code changes — this is a documentation correction; if you find the
      code *also* disagrees, stop and say so in the task file rather than widening the unit.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10). `changelog.d/` fragment.
