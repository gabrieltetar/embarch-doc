# desk: history

**Status:** active, 2026-10-26. Assembled from `changelog.d/` fragments by `scripts/build_changelog.py`; newest window first. Capped at 20 KB: over that, whole windows roll off the end, oldest first — never the newest, so a single over-cap window stays and says so — into [archive/](archive/).

## 2026-10

### Added
- One desk per project, one open suite-wide: Linear and GitHub scope, the day list, the desk form (decisions 33-40).
- The day list merges what Harvest already holds; tiles propose only the gap; entries editable from the desk (decision 41).
- `GET /refs` serves each desk's reference index - its Linear scope's issues, archived too, and its repos' PRs - on its own task; `/view` carries `refs_ms` (decision 56). Deployed 2026-10-25.
- desk 64: an approved tile whose sessions ran on comes back as a + continuation; its ✓ adds the time since to the same Harvest entry.
- embarch-chat's side moved in as decisions 46-55: the mailbox, a line per session with Open chat, the work item's notes; routes now in interfaces.md.
- embarch-desk v1: work items, Linear/Harvest/GitHub/Slack on tokens, Claude Code plugin, self-tracking time tiles. [spec](../embarch-desk/spec.md)

### Changed
- Decisions split by topic into decisions/; spec section 3 moved whole to interfaces.md.
- Waiting tiles left the work cards for the hand, a row of cards under the Slack bar for every desk; a covered tile closes itself; a tile folds into a later one (decisions 57, 58).

### Fixed
- A tile's ✓ creates its Harvest entry with an `external_reference` to the item's Linear issue, in the shape Linear's own Harvest integration writes, so the two link each other (decision 63).
- `embarch-desk service install` quotes the unit's PATH and binary path, so a WSL PATH with `/mnt/c/Program Files` is no longer cut at the first space.
- The desk re-reads Harvest every ten minutes for earlier days with a waiting tile, and ✓ re-reads the tile's day first (embarch-desk decision 62).
- Tile hours: a typed override is the only one that counts as set by hand; PATCH "hours": null returns a tile to computed hours (desk decision 61).
- A fold into an earlier or invalid day is refused, a tile id must carry a real date, and ✓ with no note sends the folded lines (desk 60).
- Harvest entries and assigned Linear issues now read every page up to a cap (2,000 / 500) and flag `truncated` ([desk decision 59](../embarch-desk/decisions/agents.md)).

### Decided
- Agents reach Linear and Harvest only through embarch-desk: curated tools, drafts sent from the Desk tab, a manual timer (decisions 29-32).
