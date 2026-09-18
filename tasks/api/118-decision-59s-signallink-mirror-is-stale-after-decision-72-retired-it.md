# 118 — Decision 59's "`SignalLink`'s own mirror" is stale after decision 72 retired it

**State:** open
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
