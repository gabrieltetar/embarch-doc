# embarch-desk: decisions

**Status:** active, 2026-10-22.

Why it is the way it is. Current truth: [spec.md](spec.md). Unresolved: [open.md](open.md).

**Numbers are permanent identifiers**, unique to this sub-project, never renumbered or reused ([DOC-CONVENTIONS.md](../DOC-CONVENTIONS.md)). 1–21 were shaped with the owner over thirteen rounds of questions on 2026-10-22 and carried in `embarch-desk-proposal.md` until v1 was built the same day; 22 onward were settled while building it.

## What the desk is

### 1 — A work cockpit, not a hardware page
One page for the user's day across clients: the issues on their plate, PRs waiting, Slack mentions, the time running. EmbArch's hardware work is one source inside it (22), not the frame around it. **Why:** the owner was asking a Claude Code session, by hand, to read a Linear issue and to log Harvest time — manual calls the suite could make itself.

### 2 — For any EmbArch user
Connectors are a plug-in point with a setup flow, nothing hardcoded to one person's accounts. **Rejected:** a single-user tool, which would have let tokens and workspace names creep into code.

### 3 — The Dashboard tab becomes Desk, and its content is deleted
Its stat cards, enrolled-boards table and alerts list all rendered from the snapshot Topology already draws better, and the alerts had moved behind *Validate topology* (`embarch-ui` decision 44). Old `#dashboard` links land on the Desk.

### 4, 5 — One card per work item, its tile inside it; cards appear on activity and leave on archive
A card carries the issue's status (a dropdown), PRs with CI, sessions, bench activity, *Open in VS Code*, and its day tiles. Slack collapses to one bar. A card appears when pinned, active within the window, or holding an open tile with time — and **leaves only when the user archives it**, never on issue close or a quiet spell. **Rejected:** tiles as a strip across the top, and three columns.

### 6 — The work item is an EmbArch object, usually one Linear issue
It exists because none of the four services holds the join between an issue, its PRs, its sessions and its time. **It can start without an issue** — a call, a meeting, ad hoc support — and gain one later. **Rejected:** inferring the grouping afresh on every read, and a Linear issue as the only anchor (no home for a meeting).

### 7 — A session with no work item is asked, every prompt, until it answers
Set at birth by a card's launch (25) or a branch naming a card's issue (26); otherwise the hooks put a one-line question in front of the session on every prompt, and the answer goes back through `desk_set_work_item` — an item, an issue key, a new title, or `untracked`. **Rejected:** an "Unsorted" card collecting orphan tiles, and auto-creating an item per repo and branch: asking keeps attribution with the person who knows.

### 8 — A work item finds its repo by session, then PR, then asking
The working directory of a session already on it; else the linked PR's GitHub repo matched to a clone on disk (read from `.git/config`, no git process per directory); else the user picks the folder once.

### 9 — PRs attach by issue key, read-only
Searched as `<KEY> type:pr involves:@me`, then **checked against title and branch on word boundaries**, because search matches `ABC-12` inside `ABC-123`. State and CI (check runs plus the combined status) only; no review list, no merge in v1.

## Time

### 10 — Captured automatically, sent only on ✓
One tile per work item per day: a small square with **✓ (to Harvest) and ✕ (discard) along its bottom edge** — the owner's own picture, kept literally. An unacted tile stays, dated, until the user acts. **✓ on a tile nobody has opened opens it** instead of sending a note and a project the user never saw.

### 11 — Session-open time, idle included, parallel sessions in full
**Over-capture, then cut**, in the owner's words: *"I always rather have agents generate too much content that I have to cut down than the opposite."* **Rejected:** time between prompts, Claude's busy time, last-prompt-wins and splitting overlap — each undercounts, and the tile is where cutting happens.

### 12 — An ignore list keeps untracked work out, the fleet included
Repos and folders on it make no tile and are never asked. EmbArch's own repos go on it — open-source work is not tracked work — and **that excludes the agent fleet with no change to the fleet**, since it only works there. **Rejected:** the fleet declaring itself from `/fleet start` (a change to `embarch-fleet` the list made unnecessary), matching agent names (breaks silently on a rename).

### 13 — The note is written live and polished once
**A hook only reports facts; it cannot write a sentence.** So commits become lines by themselves (22), the session's own Claude adds a line at a milestone with no commit, and **opening the tile runs one `claude -p`** that merges the lines into one note and **guesses the Harvest project and task** from the user's assignments and recent entries — no mapping step. **Rejected:** a Stop hook forcing a line every reply (noise, a turn each), the desk summarising transcripts (a call per tile, no live text).

## Writes and connectors

### 14 — What each connector does in v1
Linear: the card's issue and its status. GitHub: PRs with CI. Slack: every @mention and DM in every connected workspace, unread first, the fleet's own pages included, with **replies drafted by Claude and sent only as approved**. Harvest: the tiles. Any number of accounts per service.

### 15 — Status moves go through; prose is approved
An issue's state, ✓ and ✕ happen on the click. A tile's note and a Slack reply are shown in an editable box and sent as the user left them — the reply route takes its text from the request, never from a stored draft.

### 16 — Pasted tokens in v1; OAuth deferred
GitHub reuses the `gh` login; Linear takes a personal API key per workspace; Harvest a personal access token. **Slack has no personal token**, so the user makes an app in their own workspace from the shipped `slack-manifest.json` and pastes its user token — no distribution, no redirect. In a workspace that has the fleet's Slack app, that app can gain the user scopes instead; **its reinstall rotates the fleet's incoming webhook**, which then answers `no_service` while paging nobody, so the alert URL moves in the same sitting and `fleet-slack-doctor.py` runs after. **OAuth was the v1 choice for a few hours and was reversed** because it buys onboarding polish for users who do not exist yet, at the cost of four registrations EmbArch must own and three catches found in the services' docs (2026-10-22, never tried): a distributed Slack app must use HTTPS redirects, Harvest has no PKCE and an undocumented implicit-grant lifetime, and a Linear app must be made public. A pasted token is checked against its service before it is kept.

### 17 — Tokens in `~/.config/embarch-desk/`, owner-only
The treatment Core's token gets ([embarch-token.md](../embarch-token.md)), on the side the desk runs. **Rejected:** beside Core's own token, which on the owner's machine is on the Windows side while the desk runs in WSL — every read would cross the boundary.

## Agents and Claude Code

### 18 — The hooks ship as a Claude Code plugin
Installed once, it covers every repo, versioned with the desk. Every hook runs the same `embarch-desk hook`. **Rejected:** umbrella writing user settings, and per-repo settings (which miss every session outside an EmbArch repo).

### 19 — `claude -p`, stripped to the prompt
Through the user's own install and login: no API key. **Measured 2026-10-22: a bare `claude -p` loaded every plugin, MCP server and memory file — 99,290 tokens of cache creation, $0.20 to say "OK"; with `--tools ""`, `--strict-mcp-config`, `--setting-sources ""` and a replaced system prompt, 493 tokens and $0.0007.** `--bare` would be the obvious flag and fails: it skips the login, and the call ends in `api_error`. `--tools` takes a list and swallows a prompt given after it, so the prompt goes on stdin. `EMBARCH_DESK_INTERNAL=1` on the child makes the desk's own hooks drop it.

### 20 — Agents manage work items through the desk's own MCP server
Shipped in the plugin: look up, set, create, link, add a line. **Amends the proposal, which put these tools in `embarch-api`**: the plugin already ships with the desk, `embarch-api` stays the hardware tool, and bench activity needs no `embarch-api` change (22). Claude Code gives an MCP server no session identity, so the SessionStart hook puts the desk session id in the session's context and every session-scoped tool takes it.

### 21 — v1 ships whole, on one machine
**Rejected:** shipping the time loop or read-only cards first. A Claude chat panel inside the desk is v2.

## Built

### 22 — Commits and bench activity are read from PostToolUse, not reported by their tools
A `Bash` call whose command contains `git commit`, followed by a HEAD the session has not seen, becomes one tile line with the commit's subject. An `mcp__…embarch-api__` build, flash, bootload, reset or study call becomes bench activity, failed when its response says `isError`. Lines and bench seen before the session has a work item are held and move onto it when it gets one.

### 23 — A gap over 8 hours ends a span
Idle gaps count (11), so a three-hour lunch is session time — but a VS Code window left open overnight is not a night of work. 8 hours is a guess that separates the two; activity that runs across midnight splits at midnight instead.

### 24 — One JSON state file, flushed every two seconds
Owned by the one process that serves it, rewritten atomically, with acted-on tiles moving to `history/YYYY-MM.jsonl` after a week. Hooks fire on every tool call, so writes mark the state dirty and a flusher persists it. **Rejected:** SQLite — queries for free, one compiled C dependency for kilobytes a day.

### 25 — *Open in VS Code* is two links and a claim
The card records "the next session in this repo is this item" for 10 minutes, then the browser follows a `vscode://vscode-remote/wsl+<distro>/<path>` link (plain `vscode://file` off WSL) and, four seconds later, `vscode://anthropic.claude-code/open?prompt=…`, which pre-fills the Claude Code panel (documented as never auto-submitted). The first session starting in that repo takes the claim. **Rejected:** the desk spawning `code` itself — under a systemd service there is no VS Code CLI environment to reach.

### 26 — A branch naming a card's issue claims the session
`user/abc-123-…` puts a session on the card that already carries `ABC-123`. It never creates a card; an unknown key still asks (7).

### 27 — A systemd user service beside Claude Code
On the owner's machine that is WSL, not a Windows service beside Core: it runs `claude -p` and resolves repo paths locally, and the browser reaches it through `embarch-ui`. The unit carries the installing shell's `PATH`, because a user service starts without the user's own bins and the desk runs `claude`, `gh`, `git` and `wslpath`. **Rejected:** a Windows service (every polish call and path crosses the boundary; deploys need UAC), hosting inside `embarch-ui` (sessions lost while the UI is closed), a spool file ingested later (no live tiles).

### 28 — The browser reaches the desk only through `embarch-ui`
`/api/desk/{*rest}` is forwarded with the desk token added server-side. The token never enters the page, so no other site open in the browser can make the desk post to Slack or Harvest as the user.

## The one access point

### 29 — Agents reach Linear and Harvest only through the desk, with curated tools
Decided 2026-10-22, the day v1 landed: two access points meant two logins per service, two sources of truth for time, and `harvest:day` logging the same day the tiles capture. The desk's MCP server gained the handful agents use — `linear_get_issue` (description and latest comments), `linear_my_issues`, `linear_search`, `linear_set_status`, `linear_draft_comment`, `linear_draft_issue`, `harvest_entries`, `harvest_projects` — on the desk's own tokens. **Rejected:** the desk as a gateway re-exposing the official servers' whole tool sets (an MCP client with their auth inside the desk), and re-implementing everything they offer.

### 30 — Agents write under the tab's rules
A status move goes through. A comment or a new issue is a **draft** on the Desk tab, sent only by the user's Send, as they leave it; a new issue drafted from a standalone card attaches to it once sent. **No tool logs time**: a session's time is already on its tile, and what it did goes in as a line. **Rejected:** agents writing directly through the desk, and read-only agents.

### 31 — The desk replaces `harvest:day` and `harvest:track`
`harvest:day` drafted entries from the day's sessions — what the tiles now do — so using both double-logged. `harvest:track`'s live timer for work away from Claude became the desk's manual timer: one at a time, a session of its own, its time landing on the item's tile; ticked whenever the view is read, so the 8-hour gap rule (23) never ends a running timer. The plugin carrying both skills is disabled on the owner's machine.

### 32 — A hard switch, as each service is covered
Each hosted connector goes the moment the desk covers its account: on 2026-10-22 the Harvest one and the owner's company Linear workspace's. **A connector is not removed before its account is connected to the desk** — the client's Linear workspace stayed until its key is added, or agents would have lost it. **Rejected:** denying writes first and removing later, and a week of both side by side.

## Desks

Shaped in five rounds of questions on 2026-10-22 as `embarch-open-desk-proposal.md` and built the same evening; the proposal is folded here and deleted.

### 33 — One desk per project, one open suite-wide
Clients sometimes work in Intercreate's Linear and GitHub, sometimes in their own; **Harvest is always Intercreate's**, and a client's own Slack is never connected (Slack stays one feed for every desk). A desk binds its Linear scope (34), its Harvest project and task, its GitHub repos, its firmware repos (35) and a saved bench, and **one is open across the whole suite** — the UI (`embarch-ui` decision 57), the agents' Linear and GitHub scope, `embarch-api`'s default build (`embarch-api` decision 85). **"No desk" is a state**: a bare repo, nothing scoped. The open desk is published as `open-desk.json` beside the state, so the other processes read a file rather than this service. Several open at once is later.

### 34 — A desk follows one Linear project, or a whole team
The proposal said one Linear project. **The first real client's team held four**, two in progress, so a desk can bind a team instead and cover all of them. Scoping filters `my_issues` and search on the project when one is named, else on the team; a new issue drafted with no team goes into the desk's team and project.

### 35 — A desk's firmware repos are its folders; the first is what opens
The first is the repo every tab opens. The rest only say which sessions are the desk's — a project folder holding the main clone, per-feature worktrees and its manifest repo is named whole. **A folder belongs to at most one desk**; the form refuses a second claim.

### 36 — A session in another desk's repo is asked once, and stays its own desk's
The SessionStart hook tells the session the open desk is not its own and asks it to put the question to the user once (`desk_open` if yes). **Either way its time lands on its own desk**: the open desk decides what is shown and where agents and the bench point, not what is tracked.

### 37 — Who switches, and the bench
The user from the UI, an agent when told to (`desk_open`), the CLI (`embarch-desk open`), and the session's question. **Switching touches no hardware**: the UI proposes the desk's saved bench and loads it on a click, naming a running study first (`embarch-ui` decision 57).

### 38 — A tile defaults to its desk's Harvest target
Every tile starts on its desk's project and task, changeable per tile; with a desk target, polish drafts only the note and fetches no Harvest lists. **Rejected:** a target fixed per desk, and a fixed project with a guessed task.

### 39 — A standalone item names its desk when it is made
Once any desk exists, a work item with no issue needs one (or `none`) — the tab's picker defaults to the open desk, and an agent tool without one gets an error listing the desks to ask about. An issue's item takes the desk holding its Linear scope. **The first desk ever made adopts every item that had none**, the cards from before desks existed.

### 40 — The Desk tab: the open desk's cards, then today's work
Cards for the open desk only, a strip of other desks' unsent tiles, and **"Today's work" below** — every work item with time, a line, bench activity or a session that day, grouped by desk with the open one first, each row linking out to Linear and GitHub with its lines, note, status and sessions; a date picker reads other days. **Rejected:** a Harvest-style week grid, and a separate tab.

### 41 — What Harvest already holds joins the day, and a tile proposes only the gap
The first evening of real use showed the day list empty beside six hours already in Harvest: it read only the desk's own tiles. **Each day's Harvest entries are fetched** (today every two minutes, any other day when it is read) **and merged into the work item whose issue their note names**; an entry naming an issue with no card **makes the card**, dated by the entry so an old day read back does not look like today's work; an entry naming none is its own row under the desk billing its Harvest project. **A tile proposes only the time Harvest doesn't already hold** for its item that day, the entry its own ✓ made aside. **The user can edit an entry's hours and note, or delete it, from the list**; deleting one a tile made reopens that tile. **Rejected:** a separate "already in Harvest" block per desk (two lists for one day), read-only entries, keeping the full captured time on the tile, and silently dropping a tile Harvest already covers.

### 42 — A card with no repo of its own opens its desk's
A card made from an issue key or a Harvest entry has no session yet to learn its repo from (8), so "Open in VS Code" takes the desk's first firmware repo instead of asking.

