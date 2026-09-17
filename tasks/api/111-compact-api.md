# 111 — `embarch-api/decisions/failure-reporting.md` is in reserve after decision 76

**State:** blocked
**Source:** `api/110`'s decision 76 (the `validate` `not_attached` lead wording) pushed this file
past its reserve band; `DOC-COMPACTION.md` §2
**Scope:** api
**Hardware:** none
**Owner:** no

**Compacts:** embarch-api/decisions/failure-reporting.md
**Size debt due:** 2026-09-27
**In flux:** yes — `validate`'s `kind`/`reason` split has taken three amendments this month alone
(71, 73, now 76) and `embarch-core`'s own classifier for the condition changed again the same
morning this decision landed (`tasks/core/077`). A compaction pass run now risks shortening prose
the next such amendment will need to build on within days.
Unparked once a unit lands here without adding a new amendment to decisions 71/73/76, or once the
file is judged safe to split (its own natural seam: decision 57/67, the parity-rule entries, versus
71/73/76, the `validate` `kind`-classification thread).
**Must not delete:**
- Decision 71's own text describing the three-layer fix (wire shape, `is_not_attached()`
  predicate, two call sites) — the only record of why the client-side inference was rejected.
- Decision 73's "Against leaving it" paragraph — the concrete hazard (`fix_it_url` inviting
  re-enrolment on an unclassifiable response) that justified the `"unknown"` value.
- Decision 76's three named alternatives and why each was rejected — the second supervisor note on
  `api/110` asked for this explicitly, and it is the only place the reasoning behind the chosen
  wording is recorded.

## Why now

`python3 scripts/check-doc-size.py` names `embarch-api/decisions/failure-reporting.md` at
11578/12288 B (94.2%, 710 B left) — inside the last 10% reserve band (`RESERVE_FLOOR` = 1200 B),
crossed by `api/110`'s decision 76 addition.

## Done when

- [ ] `embarch-api/decisions/failure-reporting.md` is back under its reserve band, its "must not
      delete" facts intact — a split along the seam above is one honest way to do it, not the only
      one.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `changelog.d/` fragment.
