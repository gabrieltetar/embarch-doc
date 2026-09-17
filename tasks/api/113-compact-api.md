# 113 — `embarch-api/open.md` is in reserve after task 109's `build_dir_name` bullet

**State:** blocked
**Source:** `api/109`'s new Structural-limits bullet (`build_dir_name` names only the default
combination) put this file into its reserve band; `DOC-COMPACTION.md` §2
**Scope:** api
**Hardware:** none
**Owner:** no

**Compacts:** embarch-api/open.md
**Size debt due:** 2026-10-01
**In flux:** yes — `open.md` is this sub-project's live "known wrong / unfinished" ledger and one
of its most frequently touched files (nine of the last fifteen `api` units landed a bullet here,
most recently `api/090`/`092` and `api/086`); a compaction pass run now risks shortening prose the
next such unit will need to revise within days. Unparked once a unit lands here without adding or
retiring a bullet, or once a natural seam appears (e.g. "Known wrong / unfinished" vs "Structural
limits" vs "Settled-deferred" splitting into their own files the way `decisions/*.md` already does
by topic).
**Must not delete:**
- Every bullet's citation back to the decision or task that is its source of truth — several
  bullets exist only because a prior compaction pass lost the citation once already (`api/060`'s
  "trim 84 B of connective filler, file debt unpaid" line is the standing warning against doing
  that again).
- The `build_dir_name` bullet's own two clauses: what it does name (the default combination) and
  what it does not (a non-default snippet/`extra_args` build, which needs `target.json` instead) —
  losing either turns a scoped, honest limit into either an overclaim or a non-answer.
- The "decision corpus runs narrow across `api`" bullet under Settled-deferred — it is the standing
  warning against filing a decision in whichever file has room instead of the one whose topic it
  is (leg 015's mistake, cited there by name).

## Why now

`python3 scripts/check-doc-size.py` names `embarch-api/open.md` at 4381/5120 B (85.6%, 739 B left)
— inside the last 10% reserve band, crossed by `api/109`'s Structural-limits addition.

## Done when

- [ ] `embarch-api/open.md` is back under its reserve band, its "must not delete" facts intact —
      a topical split (mirroring how `decisions/*.md` is organized) is one honest way to do it, not
      the only one.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `changelog.d/` fragment.
