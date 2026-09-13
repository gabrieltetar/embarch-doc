# 064 — `mirrors.md` names the file `embarch-api` decision 64 moved out of this afternoon

**State:** claimed by agent/umbrella/064-mirrors-repoint, 2026-09-13 17:47
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

## Widened at dispatch, 2026-09-13 — verify the whole file while you have it open

*Added by the leg of 2026-09-13 17:47. The repoint above is one parenthesis, which is not a unit;
this is the rest of it, and it is the same class of work on the same file.*

`mirrors.md` carries **five** decision citations of its own, and it is the suite's cross-repo mirror
doc — the one place where a citation points *out* of `embarch-umbrella` by construction, so a wrong
one is both more likely and more expensive than elsewhere. Check all five against the cited
decision's **current body in the repo it actually lives in**, not against this file's summary of it,
and not against the number alone.

Two things this week's citation units keep finding, in this order of yield:

1. **The sentence, not the number.** Four consecutive units found a citation whose *filename* was
   correct-able while the claim wrapped around it had independently gone false. The number
   resolving is not evidence the sentence holds. `embarch-umbrella` decision 16's own *"upstream
   decisions 53/13"* phrasing is the kind of thing to re-derive rather than trust.
2. **Cross-repo numbers collide.** A bare `decision N` in this file may resolve against
   `embarch-umbrella`'s own index when it meant `embarch-api`'s. Where a citation crosses a repo
   boundary, say which repo — `<repo> decision N` is the form `embarch-api` decision 57 fixed on.

**Report the count honestly**: how many held, how many were wrong, and for each fix whether it was a
number or a sentence. "Five checked, five held" is a good outcome and a useful one to record; do not
manufacture findings to justify the pass.

**Out of scope, deliberately:** `embarch-umbrella/src/doctor.rs` carries roughly 120 more bare
citations. That is not a twenty-minute pass and is filed separately — do not start it here.

## Done when

- [ ] `embarch-umbrella/decisions/mirrors.md` names `embarch-api/decisions/config-retirement.md`,
      and the surrounding claim has been checked against decision 64's current body rather than
      assumed.
- [ ] A sweep of `embarch-umbrella/**` for any other backticked `embarch-api/decisions/shape.md`
      path — the same split may have stranded more than one.
- [ ] All five of `mirrors.md`'s own decision citations verified against the cited body in its own
      repo, with the held/wrong count reported and each fix classified as number or sentence.
- [ ] Gate green (`../../../embarch-fleet/protocol.md` §10).
- [ ] `changelog.d/umbrella-*` fragment.
