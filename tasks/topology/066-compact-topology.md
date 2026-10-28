# 066 — `decisions/links.md` is in reserve

**State:** done — 2026-10-28, agent/topology/066-compact-topology. Verbatim splits only; nothing deleted. (Earlier state: claimed 13:27, unparked 2026-10-26 by the leg that landed `suite/052`.)
**Dispatch note, 2026-10-28 leg — also pay `tasks/topology/060`'s one remaining file, by a verbatim split only.** `decisions/enrollment.md` is 12,122 / 12,288 B (166 B left), due **2026-11-01**, parked `In flux: yes` on `suite/046` extending decision 41. A verbatim split restates nothing, so that park does not forbid one (`060` says so itself): move decision 41 (or whichever seam `check-decision-refs.py` shows is cleanest) unchanged into its own topic file, fix every inbound link, and close `060` if both files are then out of reserve. **Do not shorten any text in `enrollment.md`** — the flux is real for squeezing. If no clean verbatim seam exists, leave `060` as it is and say why in it.
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

- [x] `links.md` is out of reserve, and nothing was deleted.
- [x] Prefer a verbatim split per DOC-COMPACTION.md §2; state byte counts before and after.

## Result, 2026-10-28

Nothing deleted; every moved paragraph is byte-identical (diffed against the pre-split text).

- `links.md` 12,106 B -> **9,850 B** (limit 12,288). Decisions 37 and 40 moved to the new
  `decisions/links-direct.md` (2,770 B incl. its header). Decisions 18 and 46 stay, because
  `embarch-ui/decisions/topology-tab.md`, `embarch-api/decisions/failure-reporting.md` and
  `embarch-outpost/decisions/capture.md` cite `links.md` by path for them. 37 and 40 had no inbound
  path link; only bare "decision 37" mentions (spec.md, changelog) which resolve by number.
- `enrollment.md` (task `060`'s remaining file) 12,122 B -> **10,395 B**. Decisions 41 and 16 moved to
  the new `decisions/enrollment-bench.md` (2,372 B incl. header). Decision 41 stays in
  `enrollment.md` as a heading plus one-line pointer, because `embarch-core/decisions/roles.md` and
  `embarch-dev-bench/decisions/pd-bench.md` link `enrollment.md` for it; neither doc was edited.
  Not one word of decisions 14, 15, 28, 35 was shortened, so `suite/046`'s flux is untouched.
- `decisions.md` index updated. `check-docs.py` green; no code or source comment cites a moved
  decision's path (the only one, `bin/main.rs` on decision 28, points at a decision that stayed).

**Human question** (can `spec.md` alone answer what someone needs to work on this component today?):
yes for the contract, and nothing in it changed or was deleted by this pass; spec.md names decisions
37 and 46 and 28 by number, and the numbers all still resolve in one hop.
