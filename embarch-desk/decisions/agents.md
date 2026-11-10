# embarch-desk decisions: Connectors and agents

**Status:** active, 2026-10-23.

What each connector does, how tokens are held, how agents and Claude Code reach the desk, the desk as the one access point to Linear and Harvest, and the reference index it holds for `embarch-chat`.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

## Writes and connectors

### 14 — What each connector does in v1
Linear: the card's issue and its status. GitHub: PRs and their state. Harvest: the tiles. Any number of accounts per service. Slack was a fourth, every @mention and DM with replies drafted by Claude, until 66.

### 15 — Status moves go through; prose is approved
An issue's state, ✓ and ✕ happen on the click. A tile's note is shown in an editable box and sent as the user left it; so was a Slack reply, until 66.

### 16 — Pasted tokens in v1; OAuth deferred
GitHub reuses the `gh` login; Linear takes a personal API key per workspace; Harvest a personal access token. **OAuth was the v1 choice for a few hours and was reversed** because it buys onboarding polish for users who do not exist yet, at the cost of four registrations EmbArch must own and three catches found in the services' docs (2026-10-22, never tried): a distributed Slack app must use HTTPS redirects, Harvest has no PKCE and an undocumented implicit-grant lifetime, and a Linear app must be made public. A pasted token is checked against its service before it is kept.

### 17 — Tokens in `~/.config/embarch-desk/`, owner-only
The treatment Core's token gets ([embarch-token.md](../../embarch-token.md)), on the side the desk runs. **Rejected:** beside Core's own token, which on the owner's machine is on the Windows side while the desk runs in WSL — every read would cross the boundary.

### 66 — No Slack connector
Decided by the owner on 2026-10-29, the same day as 65: with the Desk tab drawing no Slack bar, the desk's Slack side goes too — the feed poll, `slack` in `GET /view`, `POST /slack/draft` and `/slack/reply`, the `slack` connector kind and its status check, and `slack-manifest.json`. Nothing else in the suite read any of it; the Claude Code Slack connector that `embarch-chat` links is separate and untouched. **A `[[slack]]` table already in `connectors.toml` still loads**: no kind reads it, a save writes it back unchanged rather than deleting a token nobody asked to delete, and `connect`/`disconnect` refuse `slack`, so it is removed by hand. Amends 14–16.

### 68 — Linear through its MCP server, for a workspace that gives no key
Decided by the owner on 2026-10-31: a guest in a client's Linear workspace cannot make a personal API key. **Such a workspace signs in through Linear's hosted MCP server** (`connect linear <label> --mcp`, or *Sign in through Linear MCP* under Connectors), and each Linear operation of that account goes through the server's tools, answered in the GraphQL side's shapes. **EmbArch still owns no registration**, 16's objection: the server does dynamic client registration, so the desk registers a public PKCE client per sign-in, and the browser comes back to `GET /oauth/linear/callback` — the one route without the bearer, acting only on a state the desk handed out, once, within 10 minutes. [measured 2026-10-31, a probe on the owner's guest account] The token works on the MCP endpoint, **Linear's GraphQL API refuses it (401)**, it lasts 86,100 s and a refresh gives another; the desk renews it 5 minutes early, or once on a 401. **Not 29's gateway**: no tool is re-exposed. **Rejected:** reading Claude Code's own login to that server; an OAuth app EmbArch registers; asking the client for a member seat. Amends 16; refines 29.

## Agents and Claude Code

### 18 — The hooks ship as a Claude Code plugin
Installed once, it covers every repo, versioned with the desk. Every hook runs the same `embarch-desk hook`. **Rejected:** umbrella writing user settings, and per-repo settings (which miss every session outside an EmbArch repo).

### 19 — `claude -p`, stripped to the prompt
Through the user's own install and login: no API key. **Measured 2026-10-22: a bare `claude -p` loaded every plugin, MCP server and memory file — 99,290 tokens of cache creation, $0.20 to say "OK"; with `--tools ""`, `--strict-mcp-config`, `--setting-sources ""` and a replaced system prompt, 493 tokens and $0.0007.** `--bare` would be the obvious flag and fails: it skips the login, and the call ends in `api_error`. `--tools` takes a list and swallows a prompt given after it, so the prompt goes on stdin. `EMBARCH_DESK_INTERNAL=1` on the child makes the desk's own hooks drop it.

### 20 — Agents manage work items through the desk's own MCP server
Shipped in the plugin: look up, set, create, link, add a line. **Amends the proposal, which put these tools in `embarch-api`**: the plugin already ships with the desk, `embarch-api` stays the hardware tool, and bench activity needs no `embarch-api` change (22). Claude Code gives an MCP server no session identity, so the SessionStart hook puts the desk session id in the session's context and every session-scoped tool takes it.

### 21 — v1 ships whole, on one machine
**Rejected:** shipping the time loop or read-only cards first. A Claude chat panel inside the desk was v2; it became `embarch-chat`, a VS Code extension that runs its own `claude` processes (`embarch-chat` decisions 1, 5), with the desk's side in 46–55.
