# embarch-desk decisions: Connectors and agents

**Status:** active, 2026-10-23.

What each connector does, how tokens are held, how agents and Claude Code reach the desk, the desk as the one access point to Linear and Harvest, and the reference index it holds for `embarch-chat`.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

## Writes and connectors

### 14 — What each connector does in v1
Linear: the card's issue and its status. GitHub: PRs and their state. Slack: every @mention and DM in every connected workspace, unread first, the fleet's own pages included, with **replies drafted by Claude and sent only as approved**. Harvest: the tiles. Any number of accounts per service.

### 15 — Status moves go through; prose is approved
An issue's state, ✓ and ✕ happen on the click. A tile's note and a Slack reply are shown in an editable box and sent as the user left them — the reply route takes its text from the request, never from a stored draft.

### 16 — Pasted tokens in v1; OAuth deferred
GitHub reuses the `gh` login; Linear takes a personal API key per workspace; Harvest a personal access token. **Slack has no personal token**, so the user makes an app in their own workspace from the shipped `slack-manifest.json` and pastes its user token — no distribution, no redirect. In a workspace that has the fleet's Slack app, that app can gain the user scopes instead; **its reinstall rotates the fleet's incoming webhook**, which then answers `no_service` while paging nobody, so the alert URL moves in the same sitting and `fleet-slack-doctor.py` runs after. **OAuth was the v1 choice for a few hours and was reversed** because it buys onboarding polish for users who do not exist yet, at the cost of four registrations EmbArch must own and three catches found in the services' docs (2026-10-22, never tried): a distributed Slack app must use HTTPS redirects, Harvest has no PKCE and an undocumented implicit-grant lifetime, and a Linear app must be made public. A pasted token is checked against its service before it is kept.

### 17 — Tokens in `~/.config/embarch-desk/`, owner-only
The treatment Core's token gets ([embarch-token.md](../../embarch-token.md)), on the side the desk runs. **Rejected:** beside Core's own token, which on the owner's machine is on the Windows side while the desk runs in WSL — every read would cross the boundary.

## Agents and Claude Code

### 18 — The hooks ship as a Claude Code plugin
Installed once, it covers every repo, versioned with the desk. Every hook runs the same `embarch-desk hook`. **Rejected:** umbrella writing user settings, and per-repo settings (which miss every session outside an EmbArch repo).

### 19 — `claude -p`, stripped to the prompt
Through the user's own install and login: no API key. **Measured 2026-10-22: a bare `claude -p` loaded every plugin, MCP server and memory file — 99,290 tokens of cache creation, $0.20 to say "OK"; with `--tools ""`, `--strict-mcp-config`, `--setting-sources ""` and a replaced system prompt, 493 tokens and $0.0007.** `--bare` would be the obvious flag and fails: it skips the login, and the call ends in `api_error`. `--tools` takes a list and swallows a prompt given after it, so the prompt goes on stdin. `EMBARCH_DESK_INTERNAL=1` on the child makes the desk's own hooks drop it.

### 20 — Agents manage work items through the desk's own MCP server
Shipped in the plugin: look up, set, create, link, add a line. **Amends the proposal, which put these tools in `embarch-api`**: the plugin already ships with the desk, `embarch-api` stays the hardware tool, and bench activity needs no `embarch-api` change (22). Claude Code gives an MCP server no session identity, so the SessionStart hook puts the desk session id in the session's context and every session-scoped tool takes it.

### 21 — v1 ships whole, on one machine
**Rejected:** shipping the time loop or read-only cards first. A Claude chat panel inside the desk was v2; it became `embarch-chat`, a VS Code extension that runs its own `claude` processes (`embarch-chat` decisions 1, 5), with the desk's side in 46–55.

## The one access point

### 29 — Agents reach Linear and Harvest only through the desk, with curated tools
Decided 2026-10-22, the day v1 landed: two access points meant two logins per service, two sources of truth for time, and `harvest:day` logging the same day the tiles capture. The desk's MCP server gained the handful agents use — `linear_get_issue` (description and latest comments), `linear_my_issues`, `linear_search`, `linear_set_status`, `linear_draft_comment`, `linear_draft_issue`, `harvest_entries`, `harvest_projects` — on the desk's own tokens. **Rejected:** the desk as a gateway re-exposing the official servers' whole tool sets (an MCP client with their auth inside the desk), and re-implementing everything they offer.

### 30 — Agents write under the tab's rules
A status move goes through. A comment or a new issue is a **draft** on the Desk tab, sent only by the user's Send, as they leave it; a new issue drafted from a standalone card attaches to it once sent. **No tool logs time**: a session's time is already on its tile, and what it did goes in as a line. **Rejected:** agents writing directly through the desk, and read-only agents.

### 31 — The desk replaces `harvest:day` and `harvest:track`
`harvest:day` drafted entries from the day's sessions — what the tiles now do — so using both double-logged. `harvest:track`'s live timer for work away from Claude became the desk's manual timer: one at a time, a session of its own, its time landing on the item's tile; ticked whenever the view is read, so the 8-hour gap rule (23) never ends a running timer. The plugin carrying both skills is disabled on the owner's machine.

### 32 — A hard switch, as each service is covered
Each hosted connector goes the moment the desk covers its account: on 2026-10-22 the Harvest one and the owner's company Linear workspace's. **A connector is not removed before its account is connected to the desk** — the client's Linear workspace stayed until its key is added, or agents would have lost it. **Rejected:** denying writes first and removing later, and a week of both side by side.

### 56 — The desk holds each desk's reference index, for `embarch-chat`
Every issue in a desk's Linear scope and every PR in its GitHub repos — key or number, title, state, link — so the chat can turn a vague "the widget PR" in a draft into the PR itself and make a key in its timeline a link (`embarch-chat` decisions 87, 88). **The desk holds it because it is the one access point** (29): the chat has no Linear or GitHub token of its own. **A request never waits on the network**: the index's own task refreshes a desk at most every 5 minutes, at once after `POST /sync` and within 30 s of an edit to that desk, and `GET /refs` answers from memory, so the chat's match on a keystroke is local [measured 2026-10-25 on the owner's first desk, from a scratch desk: 178 issues and 48 PRs, 35 KB; a GET 2 ms; a refresh 1.9 s]. **Scope:** the desk's Linear project or team in every state — Done, Canceled and archived too (69 of the 178), since a reference to old finished work is the point, the archived ones kept pending the owner's call ([open.md](../open.md)); trashed ones not — the 1,000 most recently updated issues, and the 300 most recently updated PRs per repo, each with the issue keys in its title or branch whose team the index knows, so `UTF-8` is no issue. **Kept in `refs.json`** beside `state.json`, written only when the index changes: a restart serves the last one at once, and a polling window never rewrites the state file. `synced_ms`, and `/view`'s `refs_ms`, move only when a refresh changed the index, as a card's `notes_ms` does; a part whose fetch failed keeps its rows while its scope is unchanged. **Its own task, beside the sync loop**: inline, a refresh waiting out its timeouts on a lossy network held up timer catch-up, claim and mail expiry, the Slack feed and `POST /sync`. **Rejected:** a resolve route the chat calls per card (Linear and GitHub on the cards' path), Haiku calling the desk's tools, the cards alone (a card holds only its own item's PRs, and a Done issue never on a card was invisible), the refresh inline in the sync loop.
