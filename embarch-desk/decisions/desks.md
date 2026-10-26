# embarch-desk decisions: Desks

**Status:** active, 2026-10-23.

One desk per project and one open suite-wide; what a desk binds, who switches it, and the day list.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

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
Cards for the open desk only, every desk's unsent tiles in the hand above them (57; a strip of other desks' tiles until 2026-10-25), and **"Today's work" below** — every work item with time, a line, bench activity or a session that day, grouped by desk with the open one first, each row linking out to Linear and GitHub with its lines, note, status and sessions; a date picker reads other days. **Rejected:** a Harvest-style week grid, and a separate tab.

### 41 — What Harvest already holds joins the day, and a tile proposes only the gap
The first evening of real use showed the day list empty beside six hours already in Harvest: it read only the desk's own tiles. **Each day's Harvest entries are fetched** (today every two minutes, any other day when it is read) **and merged into the work item whose issue their note names**; an entry naming an issue with no card **makes the card**, dated by the entry so an old day read back does not look like today's work; an entry naming none is its own row under the desk billing its Harvest project. **A tile proposes only the time Harvest doesn't already hold** for its item that day, the entry its own ✓ made aside. **The user can edit an entry's hours and note, or delete it, from the list**; deleting one a tile made reopens that tile. **Rejected:** a separate "already in Harvest" block per desk (two lists for one day), read-only entries, and keeping the full captured time on the tile. Silently dropping a tile Harvest already covers was rejected too, until a 0h00 tile asking for ✓ or ✕ reversed it (57).

### 42 — A card with no repo of its own opens its desk's
A card made from an issue key or a Harvest entry has no session yet to learn its repo from (8), so "Open in VS Code" takes the desk's first firmware repo instead of asking.
