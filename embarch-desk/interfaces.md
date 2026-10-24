# embarch-desk: interfaces

**Status:** active, 2026-10-23. Moved out of [spec.md](spec.md) §3 because `embarch-chat`'s routes would take it past its size cap ([DOC-COMPACTION.md](../DOC-COMPACTION.md) §3) — a reference section, moved whole, not cut. Why: [decisions.md](decisions.md).

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


## The plugin

**The plugin** (`plugin/` in the repo, marketplace `embarch` at its root): hooks on SessionStart, UserPromptSubmit, PostToolUse, Notification, Stop and SessionEnd, all running `embarch-desk hook`; a `desk` skill; and an MCP server `embarch-desk mcp` that is **agents' one access point to Linear and Harvest** ([decision 29](decisions.md)) — work items (`desk_whoami`, `desk_set_work_item`, `desk_add_line`, `desk_list_items`, `desk_create_item`, `desk_link`), Linear (`linear_get_issue`, `linear_my_issues`, `linear_search`, `linear_set_status`, `linear_draft_comment`, `linear_draft_issue`), Harvest read-only (`harvest_entries`, `harvest_projects`) the manual timer (`desk_timer_start`, `desk_timer_stop`), and desks (`desk_list_desks`, `desk_open` — only when the user says so). **A commit becomes a tile line** when a PostToolUse `Bash` command contains `git commit` and HEAD is new; **an `embarch-api` build, flash, bootload, reset or study call becomes bench activity** ([decision 22](decisions.md)).


## Connectors and CLI

**Connectors** (pasted tokens, [decision 16](decisions.md)): Linear personal API key per workspace (GraphQL); Harvest personal access token (REST v2, every account it reaches); GitHub token or the user's `gh` login (REST; PR search by key, within the desk's repos when it names some); Slack user token from an app made from `slack-manifest.json`.

**CLI:** `serve`, `hook`, `mcp`, `service install|uninstall|status` (a systemd user unit), `connect <kind> <label>` (token on stdin), `disconnect`, `ignore list|add|remove`, `desks`, `open <desk|none>`, `status`.
