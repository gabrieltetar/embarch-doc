# `embarch-token.md` should cite `embarch-core` decision 53 for the directory-vs-file ACL split

**State:** open
**Source:** `tasks/core/031`, worker on `agent/core/031-shared-dir-decision` — that unit authored
`embarch-core` decision 53, stating that `%ProgramData%\embarch` keeping its default ACL (only the
token *file* is locked down) is deliberate
**Scope:** suite
**Hardware:** none

## What

`embarch-token.md`'s "The auto-generated token file" section says: "this doc does not assert what
that default concretely grants on any given machine, only that Core never restricts it. That
permissiveness is what `embarch-topology` decision 23 relies on..." It should say Core deliberately
never restricts it, and cite `embarch-core` decision 53 (new), the same way it already cites
`embarch-topology` decision 23 in the next clause.

`embarch-token.md` is suite-level (`DOC-PROTOCOL.md` §5) and outside the `core` sub-project's
ownership row, so `tasks/core/031`'s worker could not make this one-clause edit itself.

## Why now

Decision 53 exists specifically to make this invariant discoverable and citable from both sides of
the cross-repo dependency. Leaving `embarch-token.md` uncited means a reader following the doc's own
trail from the ACL fact to "why" lands nowhere, even though the answer now exists.

## Done when

- [ ] `embarch-token.md`'s directory-ACL sentence cites `embarch-core` decision 53 (e.g. "...only
      that Core deliberately never restricts it (`embarch-core` decision 53)").
- [ ] No other wording in that section changes.
- [ ] Gate green.
