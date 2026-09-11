# 037 — `study_schema_mismatch` names an error `code` enum member that does not exist

**State:** done — leg 077, 2026-09-10, `agent/core/037-study-schema-mismatch-code`
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

- [x] The code repo has been read and this task's body says whether the member was missing or the
      name was obsolete, with the file and line that settles it.
- [x] Either the member exists **and** a test pins a path that produces it, or the name appears
      nowhere in `embarch-core`'s docs or wire description.
- [x] `embarch-core/open.md:9`'s bullet is replaced by a numbered decision recording which way it
      went — not merely deleted.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10), including a native Windows build if the
      change reaches `embarch-core`'s Windows-only paths.
- [x] `changelog.d/` fragment; `status.d/` fragment for anything suite-level this makes false.

## Outcome

**The doc claim was false, and the truth is stranger than "one enum member missing".**
`embarch-core` has **no `code` enum at all** — not one missing a member, one that does not exist
in the code. Verified by `grep -rn "enum.*Code\|ErrorCode" --include='*.rs' .` and
`grep -n "code" src/api.rs` across the whole code worktree: no error-code enum type anywhere in
`embarch-core/src/`. `embarch-core/decisions/surfaces.md` decision 12 is the record of why — the
`{code, message, cause}` error body (the only place a `code` enum could live) was **designed and
deliberately not built**, cross-repo and deferred, with its own trigger condition. `study_schema_mismatch`
was never a member of a real enum; it was a name typed into decision 12's prose for a
*hypothetical future* enum, then left there with nothing to reconcile it against.

**Route taken: the name is obsolete.** There is no member to make reachable without building the
whole deferred `{code, message, cause}` body — explicitly out of this task's scope (a `{code,
message, cause}` shape is a cross-repo wire contract, §5 of the protocol gives a worker one repo).
Retired the name everywhere it appeared in `embarch-core`'s docs: `embarch-core/decisions/surfaces.md`
(the sentence in decision 12 that proposed it) and `embarch-core/open.md:9` (the bullet this task
was filed from). Recorded as decision 55 in `embarch-core/decisions/surfaces.md`, appended to the
same file the name originated in, with a forward note that the name is not owed a seat in the enum
by prior mention if it is ever built.

Confirmed `study_schema_mismatch` never appeared in `embarch-core`'s code (`src/`), tests, or wire
description (`interfaces.md`) — only in the two doc locations above, both now retired. No wire
change, no client-side match existed to retire.

**Doc-size reserve spent:** decision 55 pushed `embarch-core/decisions/surfaces.md` to
11,937/12,288 B (351 B left, in reserve). Filed `tasks/core/038-compact-core.md`, `blocked` on
`In flux: yes` — decision 12 and the new decision 55 are both still-moving design questions, so a
compaction pass now risks cutting a claim before it settles.

No code diff in `embarch-core`; `cargo build`, `cargo test`, `cargo clippy --all-targets -- -D
warnings` all pass unchanged (doc-only change, no Windows-only path touched). `check-docs.py`,
`check-client-names.py --repo <code worktree>`, and `check-ownership.py` (both repos) all green.
