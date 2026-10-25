# embarch-desk: interfaces

**Status:** active, 2026-10-23. Moved out of [spec.md](spec.md) §3 when `embarch-chat`'s routes would have taken it past its size cap ([DOC-COMPACTION.md](../DOC-COMPACTION.md) §3) — a reference section, moved whole, not cut. Why: [decisions.md](decisions.md).

## HTTP

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
| `GET/POST /desks`, `DELETE /desks/{id}`; `GET/POST /open`; `GET /day/{date}`; `GET /linear/projects`, `/github/repos` | Desks and the open one (`none` closes it); a day's work grouped by desk, Harvest's entries merged in (41); the form's choices |
| `PATCH`/`DELETE /harvest/entry/{account}/{id}` | The user's edit or delete of an entry already in Harvest, from the day list |
| `GET /pickup`; `POST /items/{id}/start` | The user's open issues in the desk with no card; Start work (43) |

### Added for `embarch-chat`

Every route takes the desk's bearer token. Additions only; nothing above changed shape. `?desk=` takes a desk's id or its name. What the extension calls, and when: [embarch-chat's interfaces](../embarch-chat/interfaces.md).

| Route | What |
|---|---|
| `POST /sessions/{sid}/assign` | Gains `"client": "embarch-chat"`, marking a session the panel runs; `/view` reports it. **A resume sends the mark alone**: the desk records it, then answers 400 for the missing item, so the panel reads `client` back from `GET /sessions/{sid}` rather than trusting the status ([open.md](open.md)) |
| `POST /sessions/{sid}/line` | `{"text","kind"}`, kind `done` (the default), `finding`, `decision`, `handoff` or `todo` → `{"tile","note_id"}`, or `{"held":true}` when the session has no item yet (it lands once assigned); 404 for a session the desk never saw. The route behind `desk_add_line`, and `embarch-chat`'s Keep (`embarch-chat` decision 84) |
| `POST /mailbox` | `{"kind":"focus","session_id","folder"}` → `{"id"}`; an entry expires after 10 min, as a launch claim does. **A `start` entry is written only by Start work, server-side** (46) |
| `GET /mailbox?folder=<absolute path>` | `{"entries":[…]}`, the pending entries for that folder |
| `POST /mailbox/{id}/take` | The entry, once; `409` after |
| `POST /items/{id}/start` | With the chat setting on, leaves a `start` entry for the worktree and answers without the Claude Code prompt link (43) |
| `GET`/`PUT /settings` | `{"chat_panel": bool}`, **off by default**: Start work opens Claude Code's panel unless it is on (`embarch-chat` decision 4) |
| `GET /items/{id}/brief` | The pull (48): issue (title, state, description head, latest comments), PRs, sessions, notes (each memory note's newest state, the latest lines), bench — newest first, capped at 16,000 characters |
| `GET /items/{id}/notes` | Every note, newest first (53) |
| `GET /view`, per session | `state` (`busy`, `waiting`, `idle`, `ended`), `waiting_for`, `last_ms`, `cwd`, `client`; **a card keeps its ended `embarch-chat` sessions**, so Open chat can resume one (47) |
| `GET /view?desk=<id>` | The named desk's cards instead of the open desk's, for a window on another desk (`embarch-chat` decision 9); 404 for a desk that does not exist |
| `GET /view`, per card | `notes_ms`, **when the item's notes last changed** — a note held before its session had an item lands with its older time, so the newest note's own time would not move — and a client reads `/notes` only when it moves |
| `GET /refs`, `GET /refs?desk=<id or name>` | The desk's reference index (56), from memory: `{"desk_id","synced_ms","issues":[{"key","title","state","url"}],"prs":[{"repo","number","title","state","draft","url","branch","keys"}]}`. Issues newest update first, `state` Linear's own name; PRs by repo in the desk's order, newest first, `state` `open`, `closed` or `merged`, `keys` the issue keys of a known team in the title or branch. The open desk's without `?desk=`; with none open, an empty index and `desk_id` null; 404 for a desk that does not exist. `synced_ms` is when a refresh last **changed** it, null before the first |
| `GET /view` | `refs_ms`: the viewed desk's `synced_ms`, and a client re-reads `/refs` only when it moves (56) |
| `POST /sync` | Also makes every desk's reference index due and wakes its task, without waiting on it (56) |

## The plugin

**The plugin** (`plugin/` in the repo, marketplace `embarch` at its root): hooks on SessionStart, UserPromptSubmit, PostToolUse, Notification, Stop and SessionEnd, all running `embarch-desk hook`; a `desk` skill; and an MCP server `embarch-desk mcp` that is **agents' one access point to Linear and Harvest** ([decision 29](decisions.md)) — work items (`desk_whoami`, `desk_work_item`, `desk_set_work_item`, `desk_add_line`, `desk_list_items`, `desk_create_item`, `desk_link`), Linear (`linear_get_issue`, `linear_my_issues`, `linear_search`, `linear_set_status`, `linear_draft_comment`, `linear_draft_issue`), Harvest read-only (`harvest_entries`, `harvest_projects`) the manual timer (`desk_timer_start`, `desk_timer_stop`), and desks (`desk_list_desks`, `desk_open` — only when the user says so). **A commit becomes a tile line** when a PostToolUse `Bash` command contains `git commit` and HEAD is new; **an `embarch-api` build, flash, bootload, reset or study call becomes bench activity** ([decision 22](decisions.md)).

**Notes** (48–55). A note is `{id, ts_ms, session_id, kind, text, source_path}`; kind `memory` is a captured memory file, one per `source_path`, its versions kept. `desk_work_item` returns the brief for the calling session's item, and the SessionStart brief names it as the way to everything about the item; `desk_add_line` takes a `kind`. **Capture** (52): a PostToolUse `Write`, `Edit` or `MultiEdit` whose `file_path` is under `~/.claude/projects/*/memory/` and is not `MEMORY.md` files the file's text after the write on the session's item — held until the session has one, as lines are. **Import** (54): once, on the first start that has notes. **Harvest** (50): the polish reads that day's notes of every kind.

## Connectors and CLI

**Connectors** (pasted tokens, [decision 16](decisions.md)): Linear personal API key per workspace (GraphQL); Harvest personal access token (REST v2, every account it reaches); GitHub token or the user's `gh` login (REST; PR search by key, within the desk's repos when it names some); Slack user token from an app made from `slack-manifest.json`.

**CLI:** `serve`, `hook`, `mcp`, `service install|uninstall|status` (a systemd user unit), `connect <kind> <label>` (token on stdin), `disconnect`, `ignore list|add|remove`, `desks`, `open <desk|none>`, `status`.
