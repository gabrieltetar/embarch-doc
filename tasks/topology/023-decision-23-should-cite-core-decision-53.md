# `embarch-topology` decision 23 should cite `embarch-core` decision 53 rather than flag the phrasing to its owner

**State:** claimed — leg 062, 2026-09-09
**Source:** `tasks/core/031`, worker on `agent/core/031-shared-dir-decision` — that unit authored `embarch-core` decision 53, closing the gap `embarch-topology/decisions/storage.md` decision 23 pointed at
**Scope:** topology
**Hardware:** none

## What

`embarch-topology/decisions/storage.md` decision 23 says, of `embarch-token.md`'s directory-vs-file
ACL phrasing: "that phrasing is embarch-core's to tighten, not this crate's — flagged to its owner
rather than edited across the boundary." `embarch-core` decision 53 (new, this unit) now states the
directory's permissiveness is deliberate and names the topology-side dependency explicitly.
`embarch-token.md` itself already cites decision 53 at the point decision 23 quotes.

## Why now

Decision 23's own sentence is now stale — the thing it deferred to "its owner" has been done — and
the whole point of authoring core's decision 53 was to make the invariant discoverable and cited
from both sides, not just core's.

## Done when

- [ ] `embarch-topology/decisions/storage.md` decision 23 cites `embarch-core` decision 53 (e.g.
      "now stated as `embarch-core` decision 53") in place of, or alongside, "flagged to its owner
      rather than edited across the boundary."
- [ ] No behavioural claim in decision 23 changes — this is a citation update, not new reasoning.
- [ ] Gate green.
