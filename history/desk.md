# desk: history

**Status:** active, 2026-10-26. Assembled from `changelog.d/` fragments by `scripts/build_changelog.py`; newest window first. Capped at 20 KB: over that, whole windows roll off the end, oldest first — never the newest, so a single over-cap window stays and says so — into [archive/](archive/).

## 2026-10

### Fixed
- A fold into an earlier or invalid day is refused, a tile id must carry a real date, and ✓ with no note sends the folded lines (desk 60).
- Harvest entries and assigned Linear issues now read every page up to a cap (2,000 / 500) and flag `truncated` ([desk decision 59](../embarch-desk/decisions/agents.md)).
