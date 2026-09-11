# 037 — `study_schema_mismatch` names an error `code` enum member that does not exist

**State:** open
**Source:** `embarch-core/open.md:9` — the bullet says the value is "reachable by nothing: it names
a member of the error `code` enum that does not exist". Surfaced by leg 076's refill sweep; the
claim is doc-sourced and the code has **not** been read.
**Scope:** core
**Hardware:** none
**Owner:** no

## What

A documented error `code` value, `study_schema_mismatch`, names an enum member `embarch-core` does
not have — so nothing can ever produce it and any client branching on it has dead code.

**Read the code first and settle which is wrong**, then take one of two routes and say which:

- **The member is missing and should exist** — add it, and make it reachable: a caller has to be
  able to produce it, with a test that pins the path. An enum member no code path reaches is the
  same defect one layer down.
- **The name is obsolete** — retire it everywhere it appears (docs, the wire description, any
  client-side match), and record which way it went in a numbered decision.

**Stay inside the enum and the name.** `embarch-core`'s `{code, message, cause}` error *body* is a
deferred cross-repo question and is explicitly not this task's scope — a worker gets one repo
(`../../embarch-fleet/protocol.md` §5), and widening into the body shape is how a bounded fix turns
into a wire change nobody announced.

## Why now

An error code that exists only in documentation is worse than an undocumented one: a client author
writes a handler for it, the handler is never exercised, and the case it was meant to cover falls
through to whatever the default arm does. The suite already carries a named shape for this —
`embarch-decision-reversals.md`'s "a guess indistinguishable from an answer".

## Done when

- [ ] The code repo has been read and this task's body says whether the member was missing or the
      name was obsolete, with the file and line that settles it.
- [ ] Either the member exists **and** a test pins a path that produces it, or the name appears
      nowhere in `embarch-core`'s docs or wire description.
- [ ] `embarch-core/open.md:9`'s bullet is replaced by a numbered decision recording which way it
      went — not merely deleted.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10), including a native Windows build if the
      change reaches `embarch-core`'s Windows-only paths.
- [ ] `changelog.d/` fragment; `status.d/` fragment for anything suite-level this makes false.
