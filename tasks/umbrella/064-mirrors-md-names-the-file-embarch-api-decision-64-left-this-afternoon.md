# 064 — `mirrors.md` names the file `embarch-api` decision 64 moved out of this afternoon

**State:** open
**Source:** created by `tasks/api/086`, which split `embarch-api/decisions/shape.md` and moved
decisions 53 and 64 verbatim into a new `embarch-api/decisions/config-retirement.md`. The `api`
worker found this reference, correctly judged it out of its own scope, and said so; filed by the
leg of 2026-09-13 17:4x as that unit landed.
**Scope:** umbrella
**Hardware:** none — one parenthesis in one decision body.
**Owner:** no

## What

`embarch-umbrella/decisions/mirrors.md`, in decision 16's **Amended 2026-09-10** paragraph, reads:

> `artifact_path_for_core` … was an umbrella-only field `embarch-api`'s own decision 64
> (`embarch-api/decisions/shape.md`) tolerated by name specifically *because* `init.rs` still
> scaffolded it and check 9 still read it.

**Decision 64 is no longer in `shape.md`.** It is in `embarch-api/decisions/config-retirement.md`
as of 2026-09-13. The reference is a backticked path rather than a markdown link, so
`check-links.py` cannot see it and nothing failed.

Repoint it, and **read decision 64's body while you are there** rather than only fixing the path.
Four consecutive units this week found the same shape — a citation whose *filename* was repaired
while the *sentence around it* had also gone false — so check that the "tolerated by name because
`init.rs` still scaffolded it and check 9 still read it" clause is still an accurate account of
what decision 64 now says, given that its first "Ends when" clause has fired.

## Why now

It is one line, it was created by a landing this afternoon, and the same paragraph already carries
a `**Superseded by the 2026-09-13 amendment above**` note — so a reader following the path lands in
a file that no longer holds the decision, in the one paragraph most likely to be read by someone
reconstructing what changed that day.

## Done when

- [ ] `embarch-umbrella/decisions/mirrors.md` names `embarch-api/decisions/config-retirement.md`,
      and the surrounding claim has been checked against decision 64's current body rather than
      assumed.
- [ ] A sweep of `embarch-umbrella/**` for any other backticked `embarch-api/decisions/shape.md`
      path — the same split may have stranded more than one.
- [ ] Gate green (`../../../embarch-fleet/protocol.md` §10).
- [ ] `changelog.d/umbrella-*` fragment.
