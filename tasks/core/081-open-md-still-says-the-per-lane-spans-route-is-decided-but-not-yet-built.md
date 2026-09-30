# 081 — `open.md` still says the per-lane spans route is decided but not yet built

**State:** done — worker 2026-09-29. `embarch-core/open.md`'s decision-64 bullet removed
(doc `e9064972`); no `embarch-core` code change needed. `embarch-ui/src/trace.rs` on `main`
still decodes the CSV for itself, but decision 66 (already landed, from a landed
`tasks/ui/065`) already established that split as permanent — not a gap `tasks/core/076`'s
route is still closing — so the honest resolution was deletion, not a narrower bullet.
**Filed by:** leg 138's refill sweep, 2026-09-17, reconciling `embarch-core/open.md` against what
landed an hour earlier in the same leg. Not a worker's report and not a reviewer finding — the
supervisor read the open-questions index and found a bullet the queue had already overtaken.
**Source:** `embarch-core/open.md`, the bullet beginning *"A sibling route serving decoded per-lane
spans (decision 64)"*.
**Scope:** core
**Hardware:** none — one bullet of prose in one file, and reading two decisions to confirm what
replaced it.
**Owner:** no
**Reserve (core):** `embarch-core/decisions/surfaces.md` 709 B left (parked, tasks/core/091) — do not add to it.

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

- [x] `embarch-core/open.md`'s decision-64 bullet either states what is genuinely still open, in
      terms of what `main` actually contains on the day you write it, or is removed. — Removed:
      decision 66 (already on `main`, from a landed `tasks/ui/065`) already found the
      `outpost_load.rs`/`trace.rs` split permanent, so there was no true "still open" sentence
      left to write.
- [x] Whatever you write cites `embarch-core` decision 65 (`decisions/stream-index.md`) for the
      route that now exists, not decision 64 alone. — N/A by the deletion path: nothing in
      `open.md` names a decision anymore because nothing is open. Decisions 64/65/66 read to
      confirm this are cited in the commit message and above.
- [x] No claim about `embarch-ui` that you have not read out of `embarch-ui/src/trace.rs` on `main`.
      — Read directly (`grep` over `src/trace.rs`); it still self-decodes, but that fact does not
      make the bullet true, since decision 66 already closed the question of whether it ever will.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10). — `check-docs.py` 11/11 pass,
      `check-client-names.py --repo` (core worktree) clean, `check-ownership.py --scope core` and
      `--code-repo` both OK.
- [x] `changelog.d/` fragment if anything a user could notice changed; a pure open-question
      reconciliation usually does not warrant one — say which you concluded. — Concluded: no
      fragment. Nothing user-facing changed; the route this bullet described already shipped in
      `tasks/core/076` and the duplication it flagged was already settled permanent by decision 66.
