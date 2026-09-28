# 118 — Decision 59's "`SignalLink`'s own mirror" is stale after decision 72 retired it

**State:** claimed by agent/api/118-decision-59-signallink-mirror, 2026-09-28 16:32
**Dispatch note (supervisor, 2026-09-28):** reconciled before dispatch — still true:
`crates/embarch-core-client/src/client.rs:432` imports `SignalLink` from `embarch-topology`, so it
is an alias, and `hardware-selection.md:23` still says "`SignalLink`'s own mirror". Two more places
to read while you are there, and fix only if they make the same stale claim: the same file's line
55 ("the same day this route's mirror was written"), and `client.rs:882`'s code comment pointing at
"`SignalLink`'s own doc comment above for the same constraint" — if that doc comment no longer
exists or no longer states the constraint, the pointer is the same defect in source. Decision 59's
file is 9,124 B, clear of reserve. **In reserve in `api` and not yours**:
`decisions/failure-reporting.md` (710 B left, `111`), `spec.md` (858 B, `083`), `open.md` (665 B,
`113`) — all blocked; push none further in. Correcting a decision's stale parenthetical is an
amendment in place, not a new decision number.
**Source:** embarch-api/decisions/hardware-selection.md decision 59 (2026-09-11) vs
embarch-api/decisions/client-crate.md decision 72 (2026-09-12) — found while
reviewing api/117 (merge a942c23f), which only touched decisions.md's index and
did not create this gap.
**Scope:** api
**Hardware:** none
**Owner:** no

## What

`hardware-selection.md` decision 59 says (present tense):

> not `embarch_topology::hardware`'s comparison type — the two are never checked
> against each other (this crate cannot link the `hardware` feature, the same
> constraint `SignalLink`'s own mirror lives under)

Decision 72 (`client-crate.md`, landed one day later) retired the seven
hand-written mirror types — `SignalLink` named among them — and replaced them
with type aliases to the real `embarch-topology` types (`default-features =
false, features = ["software", "wire"]`): "So the copies are gone... the old
`*Response` spellings survive as **aliases**." Decision 72 draws its own line
between a "mirror" (an independent hand-copy that can silently drift — the
`EnrolledBoardResponse` incident it describes) and an "alias" (compiler-enforced
identity, cannot drift). `SignalLink` is now the latter, not the former.

Decision 59's text was never revised after decision 72 landed, so it still
tells a reader that `SignalLink` has "its own mirror" — the exact drift-prone
thing decision 72 exists to have eliminated.

## Why now

Not urgent, not tied to any hardware failure, but it is exactly the kind of
authoritative-looking claim a future worker or reviewer would treat as current
fact when reasoning about `hardware-selection.md` or deciding whether a new
type needs the same "can't link `hardware`, so mirror it" treatment.

## Done when

- [ ] `hardware-selection.md` decision 59's parenthetical is reworded to reflect
      that `SignalLink` is now a type alias (decision 72), not an independent
      mirror — or the sentence is rewritten to make its point without leaning on
      `SignalLink`'s current shape.
- [ ] A pass over the same paragraph confirms no other type named there was
      also among decision 72's retired seven.
