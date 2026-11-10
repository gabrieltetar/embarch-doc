# desk: history

**Status:** active, 2026-10-26. Assembled from `changelog.d/` fragments by `scripts/build_changelog.py`; newest window first. Capped at 20 KB: over that, whole windows roll off the end, oldest first — never the newest, so a single over-cap window stays and says so — into [archive/](archive/).

## 2026-11

### Added
- The desk flags a folder whose Claude login lacks `embarch-api` and tells its session the `claude mcp add` command; it never writes `.claude.json` ([82](../embarch-desk/decisions/desks.md)).
- embarch-desk reads an issue's images and files: `linear_get_issue` lists them under `files`, `linear_get_file` fetches one it lists (EMB-14, decision 81).
- Start work in a west workspace sets ZEPHYR_MODULES in the worktree's local settings, so a build there reads the worktree's module files, not the main clone's (embarch-desk 80).
- embarch-desk gains linear_list_issues, which lists a team's issues in a named state in any connected workspace; agents never fall back to Claude's Linear connector (decision 79).
- embarch-desk: desk_add_line takes an optional item (issue key or item id) to note a different work item than the session's own; an unknown one errors and writes nothing (decision 78).

### Changed
- embarch-desk decisions 38, 40 and 41 moved verbatim from decisions/desks.md to decisions/day-list.md; desks.md is out of reserve.
- Desk decisions 79 and 81 moved verbatim from decisions/access-point.md to decisions/linear-reads.md; no wording changed.
- Desk: a session row in /view and the session list says its folder is missing (folder_missing) and carries no folder_uri when its cwd is gone.
- desk: `/linear/mine` and `/linear/open` answer `scope` as `team <KEY>` on a team-bound desk, as `/linear/search` does.
- A `linear_search` word query's answer names the project or team it searched, for a team-bound desk too ([interfaces](../embarch-desk/interfaces.md)).
- The desk skill, the server instructions and both no-item tool replies take a connected team's key from the prompt or a handoff before asking, as the start hook does (decision 7).
- Desk decisions 29-32, 56, 59 split out of agents.md into decisions/access-point.md; no wording changed.
- Desk: a session on no work item takes an issue key from its opening prompt or a handoff before asking ([decision 7](../embarch-desk/decisions/cockpit.md)).
- An issue key no workspace has now says why: its team's desk and folder, or that no connected workspace has the team (embarch-desk decision 77).
- `linear_get_issue` returns comments_total and a note when comments were cut, and a `skip` parameter reads older ones, on both account types (desk decision 59).
- embarch-desk docs split: the hand (57-76) and day-tile decisions (62-64) to topic files, chat routes to interfaces/, spec constants continued; nothing reworded.
- embarch-desk spec.md: status paragraph's per-decision deploy history folded into one line; out of reserve.

### Fixed
- A desk-note start that resolves no desk is no desk for every reader; the start block's cards come from that desk; a shrinking edit on a full desk is accepted (EMB-48).
- Pick up now lists an open issue whose card the view window has hidden, and Add card on it puts the card back on the board.
- Start work links the main clone's untracked embarch/, CLAUDE.local.md and .mcp.json into the new worktree, so the session loads the atlas and MCP servers.
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
- Harvest entries and assigned Linear issues now read every page up to a cap (2,000 / 500) and flag `truncated` ([desk decision 59](../embarch-desk/decisions.md)).

### Decided
- Agents reach Linear and Harvest only through embarch-desk: curated tools, drafts sent from the Desk tab, a manual timer (decisions 29-32).
