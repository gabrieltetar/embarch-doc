# embarch-desk: decisions

**Status:** active, 2026-10-22.

Why it is the way it is. Current truth: [spec.md](spec.md). Unresolved: [open.md](open.md). Reference: [interfaces.md](interfaces.md).

**Numbers are permanent identifiers**, unique to this sub-project, never renumbered or reused ([DOC-CONVENTIONS.md](../DOC-CONVENTIONS.md)). 1–21 were shaped with the owner over thirteen rounds of questions on 2026-10-22 and carried in `embarch-desk-proposal.md` until v1 was built the same day; 22 onward were settled while building it. 46–55 were shaped as `embarch-chat` decisions and moved here when its proposals folded (2026-10-23); each topic file names the old numbers. 56 was settled with the owner on 2026-10-25, with `embarch-chat` decisions 87 and 88; 57 and 58 the same evening, after three days of real use. 62 came from a review of 57 (2026-10-26); 63 the same day, from the owner's report that ✓'s entries carried no issue link. 64 from the owner's report on 2026-10-28 that a tile sent mid-day stopped counting the day's later work.

Cite them as `embarch-desk decision N`.

| Group | Decisions | What it settles |
|---|---|---|
| [decisions/cockpit.md](decisions/cockpit.md) | 1–13, 57, 58, 60, 61 | A work cockpit for any user; the Desk tab, cards and the work item; asking a session for its item; repos and PRs; time captured, sent on ✓, idle included, an ignore list, the note written live and polished once; the hand of waiting tiles, a covered tile closing itself, folding a tile into a later one, hours set by hand only when typed |
| [decisions/agents.md](decisions/agents.md) | 14–21, 29–32, 56, 59 | What each connector does, status moves vs approved prose, pasted tokens, where tokens live; the plugin, `claude -p` stripped, the desk's MCP server, v1 whole; the one access point to Linear and Harvest; the reference index `embarch-chat` mirrors; connector reads that page to a cap and say when it cut |
| [decisions/built.md](decisions/built.md) | 22–28 | Commits and bench activity from PostToolUse, the 8-hour gap, one state file, *Open in VS Code*, branch claims, the systemd service, the UI proxy |
| [decisions/desks.md](decisions/desks.md) | 33–42, 62, 63, 64 | One desk per project, one open; Linear project or team, folders, the switch question, the bench, Harvest defaults, a standalone item's desk, the day list, Harvest's entries joined, earlier days with a waiting tile re-read, ✓'s entry linking its Linear issue, time after a ✓ dealt again as a continuation of the same entry |
| [decisions/sessions.md](decisions/sessions.md) | 43–47 | Start work, live sessions on a card, no always-on window; `embarch-chat`'s mailbox and the Desk's line per chat |
| [decisions/notes.md](decisions/notes.md) | 48–55 | The work item gathers the work's knowledge: the one pull, notes and lines one stream, memory files captured, the one-time import, notes in `state.json` |
