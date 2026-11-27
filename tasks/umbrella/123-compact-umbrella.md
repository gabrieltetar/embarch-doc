# 123 — compact `embarch-umbrella/decisions/install-core.md`

**State:** done — umbrella/122 split decisions 69 and 70 verbatim into install-core-platforms.md; install-core.md is 5,855 B, out of reserve
**Scope:** umbrella
**Hardware:** none
**Owner:** no
**Compacts:** embarch-umbrella/decisions/install-core.md
**Size debt due:** 2026-12-18
**In flux:** yes
**Must not delete:** decision 61's verification order, 69's step list and deviations, 70's deviations, and 71's rejected alternatives and unverified note.

## What

`decisions/install-core.md` is at 11,774 of 12,288 B (reserve starts at 11,059) after `umbrella/121` added decision 71. Decisions 69 and 70 share one seven-step shape that a compaction can state once.

## Done when

- [ ] The file is out of reserve (`scripts/check-doc-size.py --pressure`) and every `Must not delete:` item survives.
- [ ] The human question is answered in the commit message: can the decisions index row alone say what `install-core` does today?
