# 156 — `spec.md` states the main-clone build as a known defect, not an invariant

**State:** done — closed at the split, by reconcile: the source no longer says the thing
**Source:** EMB-182, filed by the `api/154` reviewer
**Issue:** EMB-182
**Scope:** api
**Hardware:** none
**Owner:** no

## What

The `api/154` worker's doc branch added an `embarch-api/spec.md` Invariants
bullet saying a build runs the tree its config's `source_path` names, "never
the session's working directory", and a changelog fragment filing it as
decided. That is the defect EMB-181 exists to fix, written as a rule the fix
would have to overturn. The bullet and the history line should present it as
current behaviour pending EMB-181.

## Why now

A spec invariant is what the next reader treats as design.

## Done when

- [x] The spec bullet and the history line present the `source_path`-only behaviour as the known EMB-181 defect, not as a settled invariant.

## What shipped

Nothing for a worker to do. The supervisor reworded both in `api/154`'s own
fold (`e9120d26`), before that unit's doc half reached `main`, so `main` never
carried the invariant wording: the bullet now opens "Known defect, not a design
rule" and says EMB-181's fix replaces it, and the `history/api.md` line says
"a known defect, bug EMB-181, not fixed here". The pinning test's name and doc
comment still describe today's behaviour; `api/155` (EMB-181) replaces that
test with the fix.
