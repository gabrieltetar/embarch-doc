# embarch-desk: decisions

**Status:** active, 2026-10-22.

Why it is the way it is. Current truth: [spec.md](spec.md). Unresolved: [open.md](open.md). Reference: [interfaces.md](interfaces.md).

**Numbers are permanent identifiers**, unique to this sub-project, never renumbered or reused ([DOC-CONVENTIONS.md](../DOC-CONVENTIONS.md)). 1–21 were shaped with the owner over thirteen rounds of questions on 2026-10-22 and carried in `embarch-desk-proposal.md` until v1 was built the same day; 22 onward were settled while building it.

Cite them as `embarch-desk decision N`.

| Group | Decisions | What it settles |
|---|---|---|
| [decisions/cockpit.md](decisions/cockpit.md) | 1–13 | A work cockpit for any user; the Desk tab, cards and the work item; asking a session for its item; repos and PRs; time captured, sent on ✓, idle included, an ignore list, the note written live and polished once |
| [decisions/agents.md](decisions/agents.md) | 14–21, 29–32 | What each connector does, status moves vs approved prose, pasted tokens, where tokens live; the plugin, `claude -p` stripped, the desk's MCP server, v1 whole; the one access point to Linear and Harvest |
| [decisions/built.md](decisions/built.md) | 22–28 | Commits and bench activity from PostToolUse, the 8-hour gap, one state file, *Open in VS Code*, branch claims, the systemd service, the UI proxy |
| [decisions/desks.md](decisions/desks.md) | 33–42 | One desk per project, one open; Linear project or team, folders, the switch question, the bench, Harvest defaults, a standalone item's desk, the day list, Harvest's entries joined |
| [decisions/sessions.md](decisions/sessions.md) | 43–45 | Start work, live sessions on a card, no always-on window |
