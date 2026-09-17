# 081 — `open.md` still says the per-lane spans route is decided but not yet built

**State:** open
**Filed by:** leg 138's refill sweep, 2026-09-17, reconciling `embarch-core/open.md` against what
landed an hour earlier in the same leg. Not a worker's report and not a reviewer finding — the
supervisor read the open-questions index and found a bullet the queue had already overtaken.
**Source:** `embarch-core/open.md`, the bullet beginning *"A sibling route serving decoded per-lane
spans (decision 64)"*.
**Scope:** core
**Hardware:** none — one bullet of prose in one file, and reading two decisions to confirm what
replaced it.
**Owner:** no

## What

`embarch-core/open.md` currently reads:

> **A sibling route serving decoded per-lane spans** (decision 64) — decided yes, not yet built.
> `outpost_load.rs` and `embarch-ui/src/trace.rs` keep independently building the same timeline
> until it ships. Filed as `tasks/core/076`; it is a wire-schema bump the supervisor announces
> before landing.

**Every clause of that is now false or spent.** `tasks/core/076` landed 2026-09-17 (code `ef60321`
in `embarch-core`, doc `e0d54e6`, fold `9e36bf6`): the route is
`GET /study/{id}/stream/{name}/load/spans`, its shape and reasoning are `embarch-core` decision 65
in `decisions/stream-index.md`, and the announcement window it refers to closed with no objection
before the work was dispatched.

Resolve the bullet rather than editing it into a smaller true sentence, **unless something is
genuinely still open** — and one thing may be. The bullet's substantive claim was about
*duplication*: `outpost_load.rs` and `embarch-ui/src/trace.rs` both building the same timeline.
`core/076` closed `embarch-core`'s half by making the structure servable; whether `embarch-ui` has
actually stopped rebuilding it is `tasks/ui/065`'s business, dispatched in the same leg as this
filing and possibly still in flight when you read this. **So: check `embarch-ui/src/trace.rs` on
`main` before you write.** If it still decodes for itself, the honest replacement is a narrower
bullet that says the route exists and names what has not yet consumed it; if `ui/065` has landed,
the bullet goes entirely. Either way the current text must not survive, because it tells a reader
the route does not exist.

**Do not touch `embarch-ui`** — read it, cite it, and stop there.

## Why now

`open.md` is what a supervisor's refill sweep reads to decide what is worth doing, so a stale
bullet there does not merely misinform: it can put a task back in the queue for work that already
shipped. This one specifically names a task number (`tasks/core/076`) that no longer exists on
disk, which is the shape of staleness that survives longest because nothing resolves the reference.

## Done when

- [ ] `embarch-core/open.md`'s decision-64 bullet either states what is genuinely still open, in
      terms of what `main` actually contains on the day you write it, or is removed.
- [ ] Whatever you write cites `embarch-core` decision 65 (`decisions/stream-index.md`) for the
      route that now exists, not decision 64 alone.
- [ ] No claim about `embarch-ui` that you have not read out of `embarch-ui/src/trace.rs` on `main`.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `changelog.d/` fragment if anything a user could notice changed; a pure open-question
      reconciliation usually does not warrant one — say which you concluded.
