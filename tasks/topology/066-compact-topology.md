# 066 — `decisions/links.md` is in reserve

**State:** open — unparked 2026-10-26 by the leg that landed `suite/052`, which amended decision 46 in place (the "Deliberately not done" paragraph replaced by an "Amended 2026-10-26" one of about the same length; 12,121 to 12,106 B, still in reserve).
**Source:** `scripts/check-doc-size.py`'s reserve floor, hit by `tasks/topology/062` adding decision 46 (10,046 -> 12,121 / 12,288 B, 167 B left), 2026-10-26
**Scope:** topology
**Hardware:** none
**Owner:** no
**Compacts:** embarch-topology/decisions/links.md
**In flux:** no — the amendment it waited for landed with `suite/052`; nothing else in decisions 18, 37, 40 or 46 is mid-change.
**Size debt due:** 2026-11-26
**Must not delete:** decision 46's three qualifiers (dev-bench's link keeps its guess; two serial-less ports are refused, with the cost it names; the 2026-10-26 amendment: a direct route's optional `interface`, absent-means-refused, and old rows unchanged), and decisions 37's and 40's statements of what Core's exchange wait keys on.

## What

`links.md` holds decisions 18, 37, 40 and 46. Decision 18 is the longest; a verbatim split (e.g. 46 into its own `decisions/links-ambiguity.md`) is the likely seam.

## Why now

Within the last 10% of its cap with no debt filed.

## Done when

- [ ] `links.md` is out of reserve, or the task says why not and what was deleted.
- [ ] Prefer a verbatim split per DOC-COMPACTION.md §2; state byte counts before and after.
