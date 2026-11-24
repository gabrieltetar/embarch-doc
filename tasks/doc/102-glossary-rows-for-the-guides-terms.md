# 102 — Glossary rows for the guides' terms, and a current Study entry

**State:** claimed by agent/doc/102-glossary-rows-for-the-guides-terms, 2026-11-24 13:51
**Source:** EMB-317 — the glossary has none of the terms the guides use, and its Study entry says a study runs "through dev-bench"
**Issue:** EMB-317
**Scope:** doc
**Hardware:** none
**Owner:** no

## What

`embarch-glossary.md` has 30 terms and none of these, which the guides use:
bench lease, host study, instrument, bench board, role, enrolment, bootload,
ledger, publish, saved bench and live bench. Its Study entry says a study runs
"through dev-bench", but `run_host_study` runs one on Core's own host runner
with no dev bench.

When this is done, each listed term has a link-only glossary row pointing at
the doc that owns it (find the owning `spec.md`, `interfaces/` or decision for
each; do not define a term the owning doc does not), and the Study row says a
study runs on the dev bench or on Core's own host runner. `suite/studies-guide.md`
§1 points at the glossary's Study row rather than restating it.

**How it lands:** the glossary and the guides are not writable by a `doc`
worker, so deliver the exact edits as a quoted edit set in a `status.d/`
fragment (old text, new text, per file), as `doc/101` did; the supervisor
applies them at the fold. Keep the rows terse: the glossary is 8,199 B and
1,024 B of headroom above its reserve line is the budget.

**Not in this task:** `suite/hil-guide.md`'s "Words" section, which the api
binary embeds as a pinned copy; pointing it at the glossary is `api/190`, after
this lands.

## Why now

EMB-317, from the 2026-11-23 suite audit.

**Burndown leg: no new numbered decision.**

## Done when

- [ ] Every listed term has a glossary row naming its owning doc, in the
      quoted edit set.
- [ ] The Study row covers both runners; studies-guide §1 links to it.
- [ ] `python3 scripts/check-docs.py` green on the branch, `changelog.d/`
      fragment dropped.
