# embarch-desk decisions: Desks

**Status:** active, 2026-10-23.

One desk per project, each session on its own and the UI on the one it shows; what a desk binds, who selects the UI's, the day list, and a desk's standing notes.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

Shaped in five rounds of questions on 2026-10-22 as `embarch-open-desk-proposal.md` and built the same evening; the proposal is folded here and deleted.

### 33 — One desk per project; each session works on its own
Clients sometimes work in Intercreate's Linear and GitHub, sometimes in their own; **Harvest is always Intercreate's**. A desk binds its Linear scope (34), its Harvest project and task, its GitHub repos, its firmware repos (35) and a saved bench. **Each session works on its own desk** (77), which scopes its agents' Linear calls and `embarch-api`'s default build (`embarch-api` decision 85); **the UI's desk only picks what the UI shows** (`embarch-ui` decision 57). **"No desk" is a state**: unscoped for a session, every desk's cards for the UI. Every desk is published as `desks.json` beside the state.

### 34 — A desk follows one Linear project, or a whole team
The proposal said one Linear project. **The first real client's team held four**, two in progress, so a desk can bind a team instead and cover all of them. Scoping filters `my_issues` and search on the project when one is named, else on the team; a new issue drafted with no team goes into the desk's team and project.

### 35 — A desk's firmware repos are its folders; the first is what opens
The first is the repo every tab opens. The rest only say which sessions are the desk's — a project folder holding the main clone, per-feature worktrees and its manifest repo is named whole. **A folder belongs to at most one desk**; the form refuses a second claim.

### 36 — A session in a desk the UI does not show stays its own desk's
**Its time, notes, Linear scope and default build are its own desk's**, whatever the UI shows. The SessionStart question offering to switch the open desk (`desk_open` on a yes) went with the one open desk (77).

### 37 — Who selects the UI's desk, and the bench
**Only the user, in the UI**: its desk list, a desk saved new, or no desk; no agent, CLI or session moves it (77), and a repo picked by hand keeps it. **Selecting touches no hardware**: the UI proposes the desk's saved bench and loads it on a click, naming a running study first (`embarch-ui` decision 57). **Core serves one bench, by design**: a bench takes most of the machine's ports.

### 38 — A tile defaults to its desk's Harvest target
Every tile starts on its desk's project and task, changeable per tile; with a desk target, polish drafts only the note and fetches no Harvest lists. **Rejected:** a target fixed per desk, and a fixed project with a guessed task.

### 39 — A standalone item names its desk when it is made
Once any desk exists, a work item with no issue needs one (or `none`) — the tab's picker defaults to the UI's desk, and an agent tool without one gets an error listing the desks to ask about. An issue's item takes the desk holding its Linear scope. **The first desk ever made adopts every item that had none**, the cards from before desks existed.

### 40 — The Desk tab: the UI's desk's cards, then today's work
Cards for the UI's desk only, every desk's unsent tiles in the hand above them (57; a strip of other desks' tiles until 2026-10-25), and **"Today's work" below** — every work item with time, a line, bench activity or a session that day, grouped by desk with the open one first, each row linking out to Linear and GitHub with its lines, note, status and sessions; a date picker reads other days. **Rejected:** a Harvest-style week grid, and a separate tab.

### 41 — What Harvest already holds joins the day, and a tile proposes only the gap
The first evening of real use showed the day list empty beside six hours already in Harvest: it read only the desk's own tiles. **Each day's Harvest entries are fetched** (today every two minutes, any other day when it is read, and a day with a waiting tile every ten minutes and at ✓, 62) **and merged into the work item whose issue their note names**; an entry naming an issue with no card **makes the card**, dated by the entry so an old day read back does not look like today's work; an entry naming none is its own row under the desk billing its Harvest project. **A tile proposes only the time Harvest doesn't already hold** for its item that day, the entry its own ✓ made aside. **The user can edit an entry's hours and note, or delete it, from the list**; deleting one a tile made reopens that tile. **Rejected:** a separate "already in Harvest" block per desk (two lists for one day), read-only entries, and keeping the full captured time on the tile. Silently dropping a tile Harvest already covers was rejected too, until a 0h00 tile asking for ✓ or ✕ reversed it (57).

### 42 — A card with no repo of its own opens its desk's
A card made from an issue key or a Harvest entry has no session yet to learn its repo from (8), so "Open in VS Code" takes the desk's first firmware repo instead of asking.

### 62, 63, 64 — Day tiles, re-read and sent: moved
Moved verbatim to [tiles-after-send.md](tiles-after-send.md): 62 (a waiting tile's earlier day is re-read in the background and again at ✓), 63 (✓'s entry links its item's Linear issue) and 64 (time after a ✓ comes back as a continuation of the same entry).

### 74 — A desk keeps standing notes, and every session in its repos hears them at its start
Some rules hold for a whole desk, not one item: "in repo X, only app Y on board Z matters", "file F is another engineer's; report, never branch". A line is an item's and feeds Harvest, and a session told such a rule forgets it by its next start. **A desk keeps standing notes**, one rule each. **Every SessionStart (startup, resume, clear, compact) appends its desk's notes**, an agent's marked: follow them, ask on a conflict, copy them into no memory or item note. The desk is resolved at the hook, its folder's else its item's, and kept: `GET /sessions/{sid}`, `desk_work_item` and an agent's note follow it. An untracked session hears them, a hidden or path-ignored one nothing. **They count as heard**: 500 characters a note, a line break counting 3, blank lines dropped, and 4,000 for the desk's whole list, markers and marks included; past either a write is refused with 400, never cut. **Never a tile line, never Harvest**: kept beside the desks, outside `Desk` (the form rebuilds it, `desks.json` publishes it) and an item's notes (the polish reads them). **Agents write them directly** with `desk_add_desk_note` when the user says always, never, from now on or in this repo, or agrees when asked: the owner's call, 2026-11-05. The user edits and deletes them on the Desk tab. **Rejected:** a scope field on `desk_add_line`; storing them in `Desk`; a repo's `CLAUDE.md` (public, or the client's); `CLAUDE.local.md` (missing from new worktrees); Claude Code memory (captured as item notes, 52, which feed Harvest); an uncapped injection; a propose-and-accept step.

### 77 — Each session works on its own desk; the UI's desk only picks the cards
**One desk open suite-wide (33) broke once sessions for two clients ran at once**: a switch made for one client's session moved every other session's Linear scope and default build, and the suite kept losing the selected desk. **A session's desk is resolved as 74 resolves it for notes**: its folder's, else its work item's, else none, which is unscoped, never the UI's. Claude Code gives every MCP server, hook and shell it starts the session's id (`CLAUDE_CODE_SESSION_ID`) and folder; the desk's client sends both as headers and the service resolves them per call, and `embarch-api` asks `GET /desks` the same way, else reads `desks.json` by folder. **A key no workspace has says why** (EMB-9): its team bound to another desk names that desk and its folder; a team no connected workspace has says so, naming no desk. **A call naming no session works on the UI's desk**, which only the user moves (37) and the state keeps across restarts. **Rejected:** a `session_id` parameter on each Linear tool (an agent can forget it); the folder alone (loses the work item's desk); falling back to the UI's desk; one Core serving several benches (37). EMB-94, the owner's call, 2026-11-09.
