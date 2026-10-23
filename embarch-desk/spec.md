# embarch-desk: spec

**Status:** active, 2026-10-22.

What is true now. Why: [decisions.md](decisions.md). Unresolved: [open.md](open.md).

**Built and running on the owner's machine, with Linear, Harvest, GitHub and Slack connected [measured 2026-10-22] and the first desk open — the owner's current project.** Driven end to end against a scratch desk (29 browser checks) and once through a real headless Claude Code session; the Linear and Harvest reads ran against the real accounts, every write mutation was checked only with invalid ids; no tile has reached Harvest and no draft has been sent.

## 1. What it is

**A work cockpit's backend: the work item, and the connectors that fill it.** A work item is an EmbArch object — usually one Linear issue — that joins the issue to its GitHub PRs, the Claude Code sessions that worked on it, its bench activity and its time ([decision 6](decisions.md)). None of the four services holds that join; the desk does.

**Time captures itself and reaches Harvest only on a ✓.** A Claude Code plugin's hooks report session events; each work item gets one tile per day, and the user sends it (✓) or drops it (✕) from `embarch-ui`'s Desk tab ([decision 10](decisions.md)).

**Desks** (decisions 33–40): one per project — a Linear project or team, a Harvest project and task, GitHub repos, firmware repos, a saved bench — and **one open suite-wide**, published as `~/.local/share/embarch-desk/open-desk.json` for `embarch-api` and `embarch-ui` to read. The UI's open project became the open desk (`embarch-ui` decision 57); calls naming no project build the desk's repo (`embarch-api` decision 85).

**One binary, three roles:** `embarch-desk serve` (the always-on service), `embarch-desk hook` (what every hook runs) and `embarch-desk mcp` (the agent-facing tools). Its UI is `embarch-ui`'s Desk tab, which reaches it through a server-side proxy.

## 2. Invariants

- **Time is session-open time** — a session's first event to its last, idle gaps included — kept as spans per (session, work item, local day). **A gap over 8 hours ends a span** instead of counting ([decision 23](decisions.md)). Activity across midnight splits at midnight. A tile's seconds are the plain sum of its spans: parallel sessions both count in full.
- **A session under an ignored path makes no time and is never asked.** EmbArch's own repos are on the owner's list, which is also what keeps the agent fleet out ([decision 12](decisions.md)).
- **A session with no work item is asked on every prompt until it answers** — a work item, an issue key, a new title, or "untracked" ([decision 7](decisions.md)). Time it ran up while being asked lands on the item it chooses.
- **No agent tool approves, discards, archives, sends a draft or logs time.** ✓, ✕, archive and Send exist only as HTTP routes the Desk tab calls.
- **Prose is never sent unseen.** A tile's note and a Slack reply are drafted by Claude and sent only as the user left them; status moves (an issue's state, ✓, ✕) go straight through ([decision 15](decisions.md)).
- **No token or connector data reaches a repo.** Tokens live in `~/.config/embarch-desk/connectors.toml`, state in `~/.local/share/embarch-desk/`, both owner-only.
- **A hook never fails a session**: no desk, a slow desk or a bad event all exit 0 silently.
- **The open desk scopes what is shown and where agents point, never what is tracked**: a session's time lands on the desk whose repo it is in (36).
- **Switching desks touches no hardware**; the bench is proposed in the UI and loaded on a click (37).

## 3. Interfaces

**HTTP on `127.0.0.1:4891`**, bearer `~/.config/embarch-desk/desk-token` (generated on first run) on every route but `GET /health`:

| Route | What |
|---|---|
| `POST /hook` | A hook's stdin JSON verbatim; returns `{context}` for SessionStart/UserPromptSubmit |
| `GET /view` | Cards (visible work items with tiles, PRs, sessions, bench), Slack feed, connector status, ignore list |
| `POST /items`, `/items/{id}/pin`, `/archive`, `/link`, `/status`, `/launch`; `GET /items/{id}/states` | Create from issue key or title; pin; archive; link issue or repo; move Linear status; open in VS Code |
| `GET /sessions/{sid}`, `POST /sessions/{sid}/assign`, `/line` | What a session is on; put it on an item (or untrack it); add a milestone line |
| `PATCH /tiles/{item@date}`; `POST …/line`, `/polish`, `/approve`, `/discard` | Edit note, hours, Harvest target; Claude drafts note and target; ✓ to Harvest; ✕ |
| `GET /harvest/targets`; `POST /slack/draft`, `/slack/reply` | Projects and tasks; a drafted reply; send an approved one |
| `GET/POST /connectors`, `DELETE /connectors/{kind}/{label}`; `GET/PUT /ignore`; `POST /sync` | Accounts (labels only, never tokens); the ignore list; refresh now |
| `GET /linear/issue/{key}`, `/linear/mine`; `POST /linear/search`, `/linear/status`; `POST /harvest/entries` | What the agent tools call |
| `POST /drafts`, `PATCH /drafts/{id}`, `POST /drafts/{id}/send`, `/discard`; `POST /timer/start`, `/timer/stop` | Agents' comment and issue drafts, sent only from the tab; the manual timer |
| `GET/POST /desks`, `DELETE /desks/{id}`; `GET/POST /open`; `GET /day/{date}`; `GET /linear/projects`, `/github/repos` | Desks and the open one (`none` closes it); a day's work grouped by desk; the form's choices |

**The plugin** (`plugin/` in the repo, marketplace `embarch` at its root): hooks on SessionStart, UserPromptSubmit, PostToolUse, Stop and SessionEnd, all running `embarch-desk hook`; a `desk` skill; and an MCP server `embarch-desk mcp` that is **agents' one access point to Linear and Harvest** ([decision 29](decisions.md)) — work items (`desk_whoami`, `desk_set_work_item`, `desk_add_line`, `desk_list_items`, `desk_create_item`, `desk_link`), Linear (`linear_get_issue`, `linear_my_issues`, `linear_search`, `linear_set_status`, `linear_draft_comment`, `linear_draft_issue`), Harvest read-only (`harvest_entries`, `harvest_projects`) the manual timer (`desk_timer_start`, `desk_timer_stop`), and desks (`desk_list_desks`, `desk_open` — only when the user says so). **A commit becomes a tile line** when a PostToolUse `Bash` command contains `git commit` and HEAD is new; **an `embarch-api` build, flash, bootload, reset or study call becomes bench activity** ([decision 22](decisions.md)).

**Connectors** (pasted tokens, [decision 16](decisions.md)): Linear personal API key per workspace (GraphQL); Harvest personal access token (REST v2, every account it reaches); GitHub token or the user's `gh` login (REST; PR search `<KEY> type:pr involves:@me`, then check runs); Slack user token from an app made from `slack-manifest.json`.

**CLI:** `serve`, `hook`, `mcp`, `service install|uninstall|status` (a systemd user unit), `connect <kind> <label>` (token on stdin), `disconnect`, `ignore list|add|remove`, `desks`, `open <desk|none>`, `status`.

## 4. Constants

| Constant | Value |
|---|---|
| Port | 4891, `EMBARCH_DESK_PORT` |
| Gap that ends a span | 8 h [assumed] |
| Launch claim window | 10 min |
| Cards shown | the open desk's (all, with none open): pinned, active within 7 days (`EMBARCH_DESK_WINDOW_DAYS`), or holding an open tile with time |
| Refresh | connectors 5 min, issues 3 min, PRs 5 min, Slack 2 min, Slack window 3 days |
| Acted-on tiles archived to `history/YYYY-MM.jsonl` | after 7 days |
| Polish model | `sonnet`, `EMBARCH_DESK_MODEL` |
| `claude -p` cost, stripped | $0.0007 for a trivial prompt [measured 2026-10-22], against $0.20 unstripped ([decision 19](decisions.md)) |

## 5. What it deliberately does not do

- **No OAuth in v1** — tokens only ([decision 16](decisions.md)); EmbArch owns no app registration.
- **No time source but Claude Code sessions and the manual timer** — not VS Code focus, git, Slack or the bench.
- **No in-desk Linear comments, issue creation, PR review or merge, and no Claude chat panel** (v2).
- **No second machine**: one desk service, one state file, the machine with the bench.
- **No two desks open at once** (33) — later.
- **No archive or approve for agents.**

## 6. Pointers

The repo: [gabrieltetar/embarch-desk](https://github.com/gabrieltetar/embarch-desk), checked out as `../embarch-desk`. The tab: [embarch-ui](../embarch-ui/spec.md) Desk. The browser drive: `embarch-ui/tests/browser/drive_desk.py`.
