# embarch-desk: spec

**Status:** active, 2026-10-22.

What is true now. Why: [decisions.md](decisions.md). Unresolved: [open.md](open.md). Every route, tool, connector and command: [interfaces.md](interfaces.md).

**Built and running on the owner's machine, with Linear, Harvest, GitHub and Slack connected [measured 2026-10-22] and the first desk open — the owner's current project.** Driven end to end against a scratch desk (29 browser checks) and once through a real headless Claude Code session; the Linear and Harvest reads ran against the real accounts, every write mutation was checked only with invalid ids; no tile has reached Harvest and no draft has been sent. **`embarch-chat`'s side** — the mailbox, a line per session, the work item's notes — is deployed since 2026-10-23 (d9a8efc). **The reference index (56) is deployed** since 2026-10-25 17:07 (9d43fe4), live on the open desk with 178 issues and 48 PRs [measured 2026-10-25]. **The hand and folding (57, 58) are deployed** since 2026-10-25 18:33 (desk 880d970, `embarch-ui` aa5ffda); the first fold joined an earlier day's 1h46 to the day's tile on the owner's desk. **59–62 are deployed** since 2026-10-26 13:47 (32c51e3), with the service unit now quoting its PATH, so the service sees the Windows folders with a space in them. **63 is deployed** since 2026-10-26 14:24 (9b93637). **64 is deployed** since 2026-10-28 13:19 (e367298).

## 1. What it is

**A work cockpit's backend: the work item, and the connectors that fill it.** A work item is an EmbArch object — usually one Linear issue — that joins the issue to its GitHub PRs, the Claude Code sessions that worked on it, its bench activity and its time ([decision 6](decisions.md)). None of the four services holds that join; the desk does.

**Time captures itself and reaches Harvest only on a ✓.** A Claude Code plugin's hooks report session events; each work item gets one tile per day, and the user sends it (✓) or drops it (✕) from the hand, a row of cards at the head of the Desk tab holding every desk's waiting tiles ([decisions 10, 57](decisions.md)). An earlier tile can fold into a later one of its item, sent as one entry (58). The entry links the item's Linear issue, as Linear's own Harvest integration does (63).

**Desks** (decisions 33–40): one per project — a Linear project or team, a Harvest project and task, GitHub repos, firmware repos, a saved bench — and **one open suite-wide**, published as `~/.local/share/embarch-desk/open-desk.json` for `embarch-api` and `embarch-ui` to read. The UI's open project became the open desk (`embarch-ui` decision 57); calls naming no project build the desk's repo (`embarch-api` decision 85).

**The work item gathers the work's knowledge** (decisions 48–55): sessions write notes unasked, a tile line being a note of kind `done`; the hook turns every memory file a session writes into a note on its item; `desk_work_item` returns the whole brief, and a day's notes are what the tile's note summarises. **For `embarch-chat`** (46, 47) the desk is a mailbox each VS Code window polls, and the Desk shows each session as one line with Open chat or Jump. It also holds each desk's **reference index** (56) — every issue in its Linear scope, archived included, and every PR in its repos — which the chat mirrors from `GET /refs`.

**One binary, three roles:** `embarch-desk serve` (the always-on service), `embarch-desk hook` (what every hook runs) and `embarch-desk mcp` (the agent-facing tools). Its UI is `embarch-ui`'s Desk tab, which reaches it through a server-side proxy.

## 2. Invariants

- **A tile proposes only what Harvest doesn't already hold** for its item that day (41), and **one with nothing left to propose closes itself** unless a person typed its hours (`null` clears them; ✓'s own hours never count, 61) — computed, so it opens again if the entries go (57).
- **Time after a ✓ comes back** as a continuation of its entry (64).
- **A folded tile carries only what it proposed**, and goes to history with its target, never before (58). A fold goes only to a later real day; a folded row reports the hours it carried, and ✓ without a note sends the folded lines too (60).
- **Time is session-open time** — a session's first event to its last, idle gaps included — kept as spans per (session, work item, local day). **A gap over 8 hours ends a span** instead of counting ([decision 23](decisions.md)). Activity across midnight splits at midnight. A tile's seconds are the plain sum of its spans: parallel sessions both count in full.
- **A session under an ignored path makes no time and is never asked.** EmbArch's own repos are on the owner's list, which is also what keeps the agent fleet out ([decision 12](decisions.md)).
- **A session with no work item is asked on every prompt until it answers** — a work item, an issue key, a new title, or "untracked" ([decision 7](decisions.md)). Time it ran up while being asked lands on the item it chooses.
- **No agent tool approves, discards, archives, sends a draft or logs time.** ✓, ✕, archive and Send exist only as HTTP routes the Desk tab calls.
- **Prose is never sent unseen.** A tile's note and a Slack reply are drafted by Claude and sent only as the user left them; status moves (an issue's state, ✓, ✕) go straight through ([decision 15](decisions.md)).
- **No token or connector data reaches a repo.** Tokens live in `~/.config/embarch-desk/connectors.toml`, state in `~/.local/share/embarch-desk/`, both owner-only.
- **A hook never fails a session**: no desk, a slow desk or a bad event all exit 0 silently.
- **The open desk scopes what is shown and where agents point, never what is tracked**: a session's time lands on the desk whose repo it is in (36).
- **Switching desks touches no hardware**; the bench is proposed in the UI and loaded on a click (37).
- **The session decides a note's item, never the file's name** (52); a note held before the session has an item lands once it gets one.
- **A `start` mailbox entry is written only by Start work, server-side** (46): no caller supplies a prompt that a window would run in auto mode.
- **`GET /refs` answers from memory**: only the index's own task fetches, so no request waits on Linear or GitHub (56).

## 3. Interfaces

**HTTP on `127.0.0.1:4891`**, bearer `~/.config/embarch-desk/desk-token` (generated on first run) on every route but `GET /health`; the plugin's hooks, `desk` skill and MCP server — agents' one access point to Linear and Harvest ([decision 29](decisions.md)); connectors on pasted tokens; a CLI. The reference, `embarch-chat`'s additions included: [interfaces.md](interfaces.md).

## 4. Constants

| Constant | Value |
|---|---|
| Port | 4891, `EMBARCH_DESK_PORT` |
| Gap that ends a span | 8 h [assumed] |
| Launch claim window | 10 min |
| Cards shown | the open desk's (all, with none open): pinned, active within 7 days (`EMBARCH_DESK_WINDOW_DAYS`), or holding an open tile with time |
| Refresh | connectors 5 min, issues 3 min, PRs 5 min, Slack 2 min, Slack window 3 days |
| Harvest entries | today every 2 min; a day with a waiting tile 10 min [chosen] and again at ✓ (62) |
| Reference index | 1,000 issues; 300 PRs per repo; each desk every 5 min, by its own task's pass every 30 s (56) |
| Harvest entries read | 2,000 per account per call, paged by 100; `truncated` when cut [chosen] (59) |
| Assigned issues read | 500 per workspace, paged by 50; `truncated` when cut [chosen] (59) |
| Acted-on tiles archived to `history/YYYY-MM.jsonl` | after 7 days |
| Least time after a ✓ dealt as a continuation | 5 min [chosen] (64) |
| Brief | 16,000 characters, about 4K tokens (48) |
| Mailbox entry life | 10 min, as a launch claim (46) |
| Memory note versions kept | 20 per file (52) |
| Notes, worst case | 8.2 MB of state, 20 ms a write [measured 2026-10-23] (55) |
| Polish model | `sonnet`, `EMBARCH_DESK_MODEL` |
| `claude -p` cost, stripped | $0.0007 for a trivial prompt [measured 2026-10-22], against $0.20 unstripped ([decision 19](decisions.md)) |

## 5. What it deliberately does not do

- **No OAuth in v1** — tokens only ([decision 16](decisions.md)); EmbArch owns no app registration.
- **No time source but Claude Code sessions and the manual timer** — not VS Code focus, git, Slack or the bench.
- **No in-desk Linear comments, issue creation, PR review or merge** (v2), **and no Claude chat panel of its own**: that is `embarch-chat`, a VS Code extension running its own `claude` processes (`embarch-chat` decision 5).
- **No second machine**: one desk service, one state file, the machine with the bench.
- **No two desks open at once** (33) — later.
- **No archive or approve for agents.**

## 6. Pointers

The repo: [gabrieltetar/embarch-desk](https://github.com/gabrieltetar/embarch-desk), checked out as `../embarch-desk`. The tab: [embarch-ui](../embarch-ui/spec.md) Desk. The chat: [embarch-chat](../embarch-chat/spec.md). The browser drive: `embarch-ui/tests/browser/drive_desk.py`.
