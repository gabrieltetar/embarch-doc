# 090 — `embarch-api/decisions/tests.md` is in reserve after decision 74

**State:** open
**Source:** `api/088`'s decision 74 (the smoke harness's real timeout bound) pushed this file into
its reserve band; `DOC-BUDGET.md` §2. **Filed by its worker as `089` and renumbered to `090` by the
supervisor at landing**: the leg had already issued `tasks/api/089` in a refill commit this worker's
branch was cut before, so two files claimed one number. Nothing about the debt changed.
**Scope:** api
**Hardware:** none
**Owner:** no

**Compacts:** embarch-api/decisions/tests.md
**Size debt due:** 2026-09-27
**In flux:** no — this is a decision log (append-only, permanent entries, `DOC-CONVENTIONS.md`),
not a currently-"live" surface the way `spec.md` is. This leg's own edit (decision 74) was the only
touch this file had; nothing here suggests an imminent second one. A split is actionable now.
**Must not delete:**
- Every decision entry (30, 46, 54, 56, 74) verbatim — a decision number is a permanent identifier
  and this file is its only home; `decisions.md`'s index must keep pointing at wherever each number
  ends up.
- Decision 56's three amendment-style asides embedded in its own entry (the `members` failing
  silently, the `embarch-ui` isolation test, the deleted sub-crate lockfile) — each pins a
  measured, non-obvious finding, not restatable prose.
- Decision 54's "Amended 2026-09-06" paragraph — it corrects what the entry above it originally
  claimed and would misread as the original claim if detached from it.

## Why now

`python3 scripts/check-doc-size.py --pressure` names `embarch-api/decisions/tests.md` at
12201/12288 B (99.3%, 87 B left) — inside the last 10% reserve band, crossed by `api/088`'s decision
74 entry.

## Why a split, not a squeeze

`DOC-COMPACTION-PASS.md` calls a split the default remedy. This file has a natural seam by mission:
decisions 30 and 74 are both about the **named smoke-harness tier itself** (what it covers, and the
bound its one Core call actually runs under); decisions 46, 54, 56 are about the **mocked
unit-test infrastructure** underneath it (the `lib` target, the bearer sweep, workspace membership).
Splitting along that line moves entries verbatim rather than shortening any of the five arguments
above to make room for a sixth.

## Done when

- [ ] `embarch-api/decisions/tests.md` is back under its reserve band — a mission split (the
      smoke-harness tier vs. the mocked unit-test infrastructure, per above) is one honest way,
      not the only one.
- [ ] `decisions.md`'s index table still points at whichever file each of 30, 46, 54, 56, 74 ends
      up in.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `changelog.d/` fragment.
