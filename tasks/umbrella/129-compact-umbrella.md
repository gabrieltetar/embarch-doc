# 129 — compact `embarch-umbrella/decisions/reporting.md`

**State:** claimed by agent/umbrella/129-compact-umbrella, 2026-11-27 04:31
**Scope:** umbrella
**Hardware:** none
**Owner:** no
**Compacts:** embarch-umbrella/decisions/reporting.md
**Size debt due:** 2026-12-18
**In flux:** no
**Must not delete:** decision 39's two placements (`detail` and the `path` field), the "resolved, not assumed" paragraph amended by task 126, and every `[measured ...]` line.

## What

`decisions/reporting.md` is at 11,503 of 12,288 B (785 B left) after `umbrella/126` rewrote decision 39's `%ProgramData%` caveat. Decision 39's "verified live" paragraph predates that rewrite and can lose its sentence about the caveat not being exercised once folded into the amended paragraph. Reporting is not moving: check 16's resolver seam is settled.

**At dispatch:** two umbrella files are in reserve. `decisions/reporting.md` (864 B left) is this task's. `open.md` (567 B left) is parked under `umbrella/127` (`In flux: yes`): leave it alone. Decisions 67, 72 and 62 are over their own limits: do not grow them.

## Done when

- [ ] The file is out of reserve (`scripts/check-doc-size.py --pressure`) and every `Must not delete:` item survives.
