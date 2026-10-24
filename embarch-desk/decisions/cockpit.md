# embarch-desk decisions: What the desk is, and its time

**Status:** active, 2026-10-23.

The work cockpit, the work item and its card, and how time is captured and sent.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

## What the desk is

### 1 — A work cockpit, not a hardware page
One page for the user's day across clients: the issues on their plate, PRs waiting, Slack mentions, the time running. EmbArch's hardware work is one source inside it (22), not the frame around it. **Why:** the owner was asking a Claude Code session, by hand, to read a Linear issue and to log Harvest time — manual calls the suite could make itself.

### 2 — For any EmbArch user
Connectors are a plug-in point with a setup flow, nothing hardcoded to one person's accounts. **Rejected:** a single-user tool, which would have let tokens and workspace names creep into code.

### 3 — The Dashboard tab becomes Desk, and its content is deleted
Its stat cards, enrolled-boards table and alerts list all rendered from the snapshot Topology already draws better, and the alerts had moved behind *Validate topology* (`embarch-ui` decision 44). Old `#dashboard` links land on the Desk.

### 4, 5 — One card per work item, its tile inside it; cards appear on activity and leave on archive
A card carries the issue's status (a dropdown), PRs, sessions, bench activity, *Open in VS Code*, and its day tiles. Slack collapses to one bar. A card appears when pinned, active within the window, or holding an open tile with time — and **leaves only when the user archives it**, never on issue close or a quiet spell. **Rejected:** tiles as a strip across the top, and three columns.

### 6 — The work item is an EmbArch object, usually one Linear issue
It exists because none of the four services holds the join between an issue, its PRs, its sessions and its time. **It can start without an issue** — a call, a meeting, ad hoc support — and gain one later. **Rejected:** inferring the grouping afresh on every read, and a Linear issue as the only anchor (no home for a meeting).

### 7 — A session with no work item is asked, every prompt, until it answers
Set at birth by a card's launch (25) or a branch naming a card's issue (26); otherwise the hooks put a one-line question in front of the session on every prompt, and the answer goes back through `desk_set_work_item` — an item, an issue key, a new title, or `untracked`. **Rejected:** an "Unsorted" card collecting orphan tiles, and auto-creating an item per repo and branch: asking keeps attribution with the person who knows.

### 8 — A work item finds its repo by session, then PR, then asking
The working directory of a session already on it; else the linked PR's GitHub repo matched to a clone on disk (read from `.git/config`, no git process per directory); else the user picks the folder once.

### 9 — PRs attach by issue key, read-only
Searched as `<KEY> type:pr involves:@me`, then **checked against title and branch on word boundaries**, because search matches `ABC-12` inside `ABC-123`. Their state only — **CI was shown until 2026-10-22, when the owner asked for it gone**, and the desk stopped fetching check runs with it; no review list, no merge in v1.

## Time

### 10 — Captured automatically, sent only on ✓
One tile per work item per day: a small square with **✓ (to Harvest) and ✕ (discard) along its bottom edge** — the owner's own picture, kept literally. An unacted tile stays, dated, until the user acts. **✓ on a tile nobody has opened opens it** instead of sending a note and a project the user never saw.

### 11 — Session-open time, idle included, parallel sessions in full
**Over-capture, then cut**, in the owner's words: *"I always rather have agents generate too much content that I have to cut down than the opposite."* **Rejected:** time between prompts, Claude's busy time, last-prompt-wins and splitting overlap — each undercounts, and the tile is where cutting happens.

### 12 — An ignore list keeps untracked work out, the fleet included
Repos and folders on it make no tile and are never asked. EmbArch's own repos go on it — open-source work is not tracked work — and **that excludes the agent fleet with no change to the fleet**, since it only works there. **Rejected:** the fleet declaring itself from `/fleet start` (a change to `embarch-fleet` the list made unnecessary), matching agent names (breaks silently on a rename).

### 13 — The note is written live and polished once
**A hook only reports facts; it cannot write a sentence.** So commits become lines by themselves (22), the session's own Claude adds a line at a milestone with no commit, and **opening the tile runs one `claude -p`** that merges the lines into one note and **guesses the Harvest project and task** from the user's assignments and recent entries — no mapping step. **Rejected:** a Stop hook forcing a line every reply (noise, a turn each), the desk summarising transcripts (a call per tile, no live text).
