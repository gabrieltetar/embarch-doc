# 138 — `embarch-core/open.md` still owes `verify` check 8, which has landed

**State:** done
**Source:** `embarch-core/open.md` — "The run log's tail is anchored only from a publish on … Remains for M1.11: `verify` check 8 comparing the recorded head."; `embarch-api/interfaces/publish.md` check 8 row and `embarch-api/decisions/verify.md` decisions 118 to 121 (landed 2026-11-22, `tasks/api/170`). Filed by the supervisor during a refill sweep, 2026-11-23.
**Scope:** core
**Hardware:** none
**Owner:** no

## Dispatch notes

- Docs only: no `embarch-core` code changes, so no code branch is expected. If you find a code comment in `embarch-core` that makes the same stale claim, say so in your result rather than editing it.
- `embarch-api`'s `verify` (M1.11 in `notes/hil/14-implementation-plan.md`) landed with `tasks/api/170` and `tasks/api/171`. Its check 8 recomputes every hash, `prev` and `seq` and requires the chain to end at the manifest's signed head and length; the publish's own `published` entry, and any later revision, are stated as not checkable offline. Read check 8's row in `embarch-api/interfaces/publish.md` and decision 121 in `embarch-api/decisions/verify.md` before rewording anything. Do not edit `embarch-api`'s docs; they are another scope.
- No new decision is expected. Near their per-decision limit in `embarch-core`: `signing#110` (already over by 2,486 B), `lease#93` (182 B left), `run-log#111` (201 B left). If a decision text has to change, say why in your result before spending those bytes.

## What

`embarch-core/open.md`'s run-log-tail bullet says what is true now: a publish records the head it ended at, `verify` check 8 checks a zip's segment against the manifest's signed head, and what still cannot be detected offline (a tail cut after the last publish, the publish's own entry). Read the rest of `embarch-core/open.md` and its `open/*.md` files for any other line that `embarch-api`'s verify decisions (118 to 125) have made false, and correct those too.

## Why now

The bullet names M1.11 as remaining after M1.11 landed, so a reader of `embarch-core/open.md` would plan work that is done.

## Done when

- [x] The run-log-tail bullet no longer says check 8 is owed, and states what check 8 does and does not cover, citing `embarch-api`'s decision by number.
- [x] Any other line in `embarch-core/open.md` or `embarch-core/open/*.md` that the verify decisions made false is corrected, or the result says none was found.
- [x] Gate green (`../../embarch-fleet/gate.md`), `changelog.d/` fragment dropped, `status.d/` fragment for anything suite-level it made false.
