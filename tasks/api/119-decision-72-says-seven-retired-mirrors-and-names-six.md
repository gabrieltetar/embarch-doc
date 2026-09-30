# 119 — Decision 72 says "seven" retired mirrors and names six

**State:** claimed by agent/api/119-decision-72-mirror-count, 2026-09-29 21:31
**Source:** the `api/118` reviewer, 2026-09-28, reading decision 72 while checking decision 59's
amendment against it. Pre-existing — decision 72 was authored at `c62cc870` (2026-09-12) and
`api/118` did not touch it. Filed by the supervisor at `api/118`'s fold.
**Scope:** api
**Hardware:** none
**Owner:** no

## What

`embarch-api/decisions/client-crate.md` says "seven" three times — line 26 ("seven hand-written
mirrors of topology types"), decision 72's heading ("The seven mirrored `embarch-topology` types
are retired"), and its first sentence ("Decisions 37/38 accepted seven hand-written copies of
…") — and that sentence then names **six**: `EnrolledBoard`, `Alert`, `DetectedPort`,
`SignalLink`, `Route`, `SignalDirection`. The source agrees with six:
`crates/embarch-core-client/src/client.rs`'s block comment above the
`pub use embarch_topology::hardware::{...}` re-export (around lines 408–432) opens "Until
2026-09-12 the six types below were hand-written copies".

Either a seventh type was retired and the list dropped it (a `*Response` spelling, or a type that
is now an alias under another name), or the count was wrong when written. Settle which from
`git show c62cc870` and the pre-retirement `client.rs`, then make the count and the list agree in
all three places. `api/117` and `api/118` both cited "decision 72's retired seven" on the strength
of the heading, so check those two task outcomes (now in `history/api.md`) still read true.

## Why now

A decision whose count and list disagree is one a later reader resolves by guessing, and two
tasks in a row have already repeated the count.

## Done when

- [ ] The count and the named list in decision 72 agree, with the source (git) for which is right.
- [ ] Line 26's "seven" agrees too.
- [ ] If a seventh type existed, `client.rs`'s "six" comment is corrected to match (comment only —
      `embarch-core-client` is path-depended on by `embarch-ui`).
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10), `changelog.d/` fragment.
