# 009 — `validate`'s `confirmed_at_utc_ms` is the enrolment time, and reads as the validation time

**State:** open
**Source:** observed by the supervisor running `tasks/topology/002`, 2026-09-06
**Scope:** topology
**Hardware:** none
**Owner:** no

## What was observed

Two `validate` calls on role `dev-bench`, minutes apart on 2026-09-06, both
returned:

```json
{ "ok": true, "role": "dev-bench", "hardware_id": "6fcddc36cb781b71",
  "confirmed_at_utc_ms": 1788195194573 }
```

`1788195194573` is **2026-08-31 10:53:14 local** — the moment the board was
enrolled, six days earlier. It did not move, because it is `EnrolledBoard`'s
field and `validate` returns the enrolled row on a match, which is documented
behaviour and is not the defect.

The defect is that **the only timestamp in a validation response names something
other than the validation.** A caller reading `ok: true` next to
`confirmed_at_utc_ms` has every reason to read the pair as "confirmed, at this
time"; it means "matches the row recorded at this time". The live check that
just succeeded — the thing the caller asked for — leaves no timestamp at all.

## Why it matters more than a naming nit

This is the field an operator or a doctor check would reach for to answer *how
stale is this?*, and it answers a different question with a plausible number.
The failure mode is silent and in the safe-looking direction: a board unplugged
and replaced an hour ago still shows a `confirmed_at` from whenever it was
enrolled, so a stale answer and a fresh one are indistinguishable in the
response. Nothing in the gate can catch a field that is honest about the wrong
event.

Adjacent, and the reason this is worth doing rather than noting: `tasks/api/032`
already records that the enrolled-board mirror drops `link_port_interface`, so
this response shape has one known fidelity bug already.

## Done when

- [ ] A validation response distinguishes *when the record was made* from *when
      the live check ran* — either by adding the second, or by renaming the field
      so it cannot be read as the second. Whichever is chosen, say why in a
      decision: this is a wire-visible field with consumers.
- [ ] Every consumer of `confirmed_at_utc_ms` is enumerated before it changes
      shape — `embarch-api`'s mirror and MCP `validate` tool, `embarch-umbrella`'s
      doctor, `embarch-ui`'s Topology tab.
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
