# 046 — Compact embarch-core/decisions/auth.md

**State:** blocked — `In flux: yes`, so nothing here is dispatchable yet.
**Size debt due:** 2026-09-26 (two weeks out; re-check `api.rs`'s auth-sweep
churn rate then and either compact or extend).
**Source:** `scripts/check-doc-size.py`, run by task `core/045` (2026-09-12):
`embarch-core/decisions/auth.md` at 11356/12288 B (92.4%, 932 B left), no debt
filed.
**Scope:** core
**Hardware:** none
**Owner:** no

## What

**Compacts:** `embarch-core/decisions/auth.md`

Shorten `decisions/auth.md` (`DOC-COMPACTION.md`/`DOC-COMPACTION-PASS.md`)
without deleting a decision number or a distinct finding. The file crossed
90% of its reserve when decision 60 (the route-wiring cross-check, the other
half of decision 42's sweep) landed.

**In flux:** yes. Decisions 42 and 46 both concern `build_router`'s own
route-registration scan, and decision 60 is a third mechanism reading the
same source text a different way; the next new HTTP route or the next gap
found in this sweep family is likely to land here again rather than
somewhere quieter.

**Must not delete:** decision 42's derivation rationale and its "residual is
one-sided" scan limitation; decision 46's cross-repo `include_str!` failure
mode and why `DOCUMENTED_ROUTE_COUNT` is a pinned literal instead; decision
53's directory-vs-file ACL distinction and the instruction not to narrow the
directory; decision 60's mutation-verification result and its stated "not
covered" limits (a route the scan's text pattern misses; a handler whose own
`// route:` comment is simply wrong).

## Why now

`check-doc-size.py` names this file with no filed debt; per protocol §5 item
5, that failure must be filed rather than left silent.

## Done when

- [ ] `embarch-core/decisions/auth.md` back under reserve (under 90% of
      12288 B), same decision numbers still resolving.
- [ ] `scripts/check-doc-size.py` clean.
- [ ] Gate green.
