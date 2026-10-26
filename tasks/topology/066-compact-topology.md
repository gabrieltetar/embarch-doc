# 066 — `decisions/links.md` is in reserve

**State:** blocked — until `tasks/suite/052` (filed from topology/062's drop `suite-direct-route-declared-interface`) lands, because it amends decision 46 in this same file. A verbatim split needs no unpark.
**Source:** `scripts/check-doc-size.py`'s reserve floor, hit by `tasks/topology/062` adding decision 46 (10,046 -> 12,121 / 12,288 B, 167 B left), 2026-10-26
**Scope:** topology
**Hardware:** none
**Owner:** no
**Compacts:** embarch-topology/decisions/links.md
**In flux:** yes — decision 46 is expected to be amended when a direct route gains a declared interface (cross-repo drop `suite-direct-route-declared-interface`); compacting before that states something about to be wrong.
**Size debt due:** 2026-11-26
**Must not delete:** decision 46's three qualifiers (dev-bench's link keeps its guess; two serial-less ports are refused, with the cost it names; the declared interface is deliberately not done and why), and decisions 37's and 40's statements of what Core's exchange wait keys on.

## What

`links.md` holds decisions 18, 37, 40 and 46. Decision 18 is the longest; a verbatim split (e.g. 46 into its own `decisions/links-ambiguity.md`) is the likely seam.

## Why now

Within the last 10% of its cap with no debt filed.

## Done when

- [ ] `links.md` is out of reserve, or the task says why not and what was deleted.
- [ ] Prefer a verbatim split per DOC-COMPACTION.md §2; state byte counts before and after.
