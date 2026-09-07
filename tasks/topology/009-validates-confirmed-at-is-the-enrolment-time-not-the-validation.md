# 009 — `validate`'s `confirmed_at_utc_ms` is the enrolment time, and reads as the validation time

**State:** claimed by agent/topology/009-confirmed-at-is-enrolment-time, 2026-09-07 17:54
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

## Reproduced again, leg 026, and the second role sharpens it

Two `validate` calls seconds apart, 2026-09-06 20:33 local, both `ok: true`:

| role | `confirmed_at_utc_ms` | that instant |
|---|---|---|
| `dut` | `1788723019911` | 2026-09-06 13:30 MDT — earlier the same day |
| `dev-bench` | `1788195194573` | 2026-08-31 10:53 MDT — six days earlier |

Same response shape, same successful live check, **timestamps six days apart.**
So the field does not merely fail to advance — read as a freshness figure it
**ranks two equally-fresh validations against each other**, and the one that
looks stale is the board that has simply not been re-enrolled recently. An
operator or a `doctor` check comparing roles gets a confident ordering that has
nothing to do with when either board was last seen.

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

## Supervisor direction, leg 038 — take the additive arm, not the rename

The "Done when" below offers two arms and **only one of them is yours.**

**Add the second timestamp. Do not rename `confirmed_at_utc_ms`.** A rename is a
wire-schema change across four repos with hand-maintained mirrors, which is
`suite`-scoped work the supervisor executes itself after a Slack announcement
(`../../embarch-fleet/protocol.md` §8) — a `topology` worker cannot land it, and
`check-ownership.py --scope topology` would refuse the other three halves on your
branch anyway. Landing the topology half of a rename alone is the half-landed
wire change this suite names as its worst failure mode.

An additive field is safe by construction: every existing mirror keeps
deserializing, and each consumer picks the new field up when someone gets to it.

So: **enumerate the consumers as a read** — `embarch-api`'s
`crates/embarch-core-client` mirror and its MCP `validate` tool,
`embarch-umbrella`'s doctor, `embarch-ui`'s Topology tab — and for each one,
**file an `inbox/` drop scoped to that repo** saying what it should now show and
why. Do not edit them. If you find a consumer this list does not name, that is
worth more than the field itself; say so.

**If, having read the consumers, you conclude the additive arm is wrong** — that
two timestamps side by side are more confusing than one badly-named one — stop
and write that into this task file rather than renaming. That is a real finding
and it is a `suite` decision, not yours or mine to make on a branch.

## Doc-size reserve for `topology`

`embarch-topology/open.md` — 4322/5120 B, **798 B left**, filed against
`tasks/topology/014-compact-topology.md` (open, not blocked). If your work
spends that reserve or leaves it spent with nothing filed, file
`tasks/topology/<next NNN>-compact-topology.md` in the same commit per
`tasks/README.md`. Nothing else in `topology` is in reserve.

## Done when

- [ ] A validation response distinguishes *when the record was made* from *when
      the live check ran*, **by adding the second** — see the supervisor
      direction above; the rename arm is out of scope for this unit. Say why in
      a decision: this is a wire-visible field with consumers.
- [ ] Every consumer of `confirmed_at_utc_ms` is enumerated before it changes
      shape — `embarch-api`'s mirror and MCP `validate` tool, `embarch-umbrella`'s
      doctor, `embarch-ui`'s Topology tab.
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
