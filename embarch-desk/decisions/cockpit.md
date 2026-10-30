# embarch-desk decisions: What the desk is, and its time

**Status:** active, 2026-10-25.

The work cockpit, the work item and its card, and how time is captured and sent.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

## What the desk is

### 1 — A work cockpit, not a hardware page
One page for the user's day across clients: the issues on their plate, PRs waiting, Slack mentions (off the tab since 65), the time running. EmbArch's hardware work is one source inside it (22), not the frame around it. **Why:** the owner was asking a Claude Code session, by hand, to read a Linear issue and to log Harvest time — manual calls the suite could make itself.

### 2 — For any EmbArch user
Connectors are a plug-in point with a setup flow, nothing hardcoded to one person's accounts. **Rejected:** a single-user tool, which would have let tokens and workspace names creep into code.

### 3 — The Dashboard tab becomes Desk, and its content is deleted
Its stat cards, enrolled-boards table and alerts list all rendered from the snapshot Topology already draws better, and the alerts had moved behind *Validate topology* (`embarch-ui` decision 44). Old `#dashboard` links land on the Desk.

### 4, 5 — One card per work item; cards appear on activity and leave on archive
A card carries the issue's status (a dropdown), PRs, sessions, bench activity and *Open in VS Code*. **Its day tiles were inside it until 2026-10-25**; they are in the hand now (57), and the card keeps a chip per waiting day that opens the tile. Slack collapsed to one bar, gone since 65. A card appears when pinned, active within the window, or holding an open tile with time — and **leaves only when the user archives it**, never on issue close or a quiet spell. **Rejected:** three columns. Tiles as a strip across the top were rejected here too, until three days of use reversed it (57).

### 6 — The work item is an EmbArch object, usually one Linear issue
It exists because none of the four services holds the join between an issue, its PRs, its sessions and its time. **It can start without an issue** — a call, a meeting, ad hoc support — and gain one later. **Rejected:** inferring the grouping afresh on every read, and a Linear issue as the only anchor (no home for a meeting).

### 7 — A session with no work item is asked, every prompt, until it answers
Set at birth by a card's launch (25) or a branch naming a card's issue (26); otherwise the hooks put a one-line question in front of the session on every prompt, and the answer goes back through `desk_set_work_item` — an item, an issue key, a new title, or `untracked`. **Rejected:** an "Unsorted" card collecting orphan tiles, and auto-creating an item per repo and branch: asking keeps attribution with the person who knows.

### 8 — A work item finds its repo by session, then PR, then asking
The working directory of a session already on it; else the linked PR's GitHub repo matched to a clone on disk (read from `.git/config`, no git process per directory); else the user picks the folder once.

### 9 — PRs attach by issue key, read-only
Searched as `<KEY> type:pr involves:@me`, then **checked against title and branch on word boundaries**, because search matches `ABC-12` inside `ABC-123`. Their state only — **CI was shown until 2026-10-22, when the owner asked for it gone**, and the desk stopped fetching check runs with it; no review list, no merge in v1.

### 65 — The Desk tab draws no Slack bar; its spot waits for a Promptu section
Decided by the owner on 2026-10-29: the Slack bar and its feed leave the Desk tab, and the place the bar held stays empty for a Promptu section, a later change. **Only the tab changed**: the desk still reads Slack and serves the feed in `GET /view` and the `/slack` routes, which nothing calls now, and the Connectors panel still takes a Slack token. Amends 1, 4–5 and 57; retires `embarch-ui` decision 63, the bar's reply identity.

## Time

### 10 — Captured automatically, sent only on ✓
One tile per work item per day: a card in the hand (57) with **✓ (to Harvest) and ✕ (discard) along its bottom edge** — the owner's own picture, kept literally. An unacted tile stays, dated, until the user acts. **✓ on a tile nobody has opened opens it** instead of sending a note and a project the user never saw.

### 11 — Session-open time, idle included, parallel sessions in full
**Over-capture, then cut**, in the owner's words: *"I always rather have agents generate too much content that I have to cut down than the opposite."* **Rejected:** time between prompts, Claude's busy time, last-prompt-wins and splitting overlap — each undercounts, and the tile is where cutting happens.

### 12 — An ignore list keeps untracked work out, the fleet included
Repos and folders on it make no tile and are never asked. EmbArch's own repos go on it — open-source work is not tracked work — and **that excludes the agent fleet with no change to the fleet**, since it only works there. **Rejected:** the fleet declaring itself from `/fleet start` (a change to `embarch-fleet` the list made unnecessary), matching agent names (breaks silently on a rename).

### 13 — The note is written live and polished once
**A hook only reports facts; it cannot write a sentence.** So commits become lines by themselves (22), the session's own Claude adds a line at a milestone with no commit, and **opening the tile runs one `claude -p`** that merges the lines into one note and **guesses the Harvest project and task** from the user's assignments and recent entries — no mapping step. **Rejected:** a Stop hook forcing a line every reply (noise, a turn each), the desk summarising transcripts (a call per tile, no live text).

### 57 — The hand: every waiting tile as a card at the head of the desk, and a covered tile closes itself
Decided with the owner on 2026-10-25, three days into real use: *"I regret the decision of having them inside the work card"* — the time to send was scattered across cards further down the page, and a desk switch hid the rest behind a strip. **The tiles leave the cards for one row at the head of the desk** (under the Slack bar until 65), **picked like cards in a game's draft**: upright cards, the item's key and title, the hours large, the day, a live dot while a session still counts, ✓ ✕ along the bottom. **Every desk's tiles are in it**, this desk's first, then oldest first, another desk's tagged with its name; the strip of other desks' unsent tiles (40) is gone. An archived card's tiles stay out. A card is dealt in once, lifts under the pointer, flies to a "Sent today" count on ✓ and drops on ✕.

**A tile Harvest already covers closes itself**: when the entries naming its issue that day hold at least the time it captured, and nobody set its hours by hand, it is out of the hand and does not keep its card on the desk. It is computed, never stored, so deleting those entries opens it again. The first such tile sat at 0h00 with ✓ and ✕, a question with no answer. This reverses 41's rejection of dropping a covered tile. **Rejected:** a fanned, overlapping hand (past five cards the numbers hide until hovered), a hand flanked by Harvest and discard piles to drag onto (drag on a trackpad, and twice the build), the open desk's tiles only, a covered tile kept greyed with only ✕.

### 58 — A tile folds into a later one of its item
A work item started late one day and carried on two days later left two tiles for one stretch of work; the owner wanted one entry. **`POST /tiles/{id}/fold` with `{"into": <date>}`** moves an open tile's time and lines into the same item's open tile on that date, and one Harvest entry dated that day carries both; the tile dialog offers *Fold into <day>* when a later tile of the item is in the hand. **What moves is what the tile proposed** — its own hours if the user set them, else the gap Harvest's entries that day left (41) — so no hour is sent twice; it freezes as the folded tile's `final_seconds`. The target shows the folded lines and the polish summarises them. **A folded tile goes to history with its target, never before**, since its seconds are part of the target's until the target freezes its own. There is no unfold. **Rejected:** re-dating the earlier day's spans (rewrites what happened), freezing the target's hours by hand (stops a live tile counting), discarding the earlier tile.

### 60 — A fold goes only to a later real day, and a folded row reports what it carried
Review of 58 found three server gaps. **`fold_tile` refuses (400, nothing changes) an `into` that is not a real `YYYY-MM-DD` or is not later than the source**; the UI offered only later tiles, but the desk is the one access point and the one entry is dated the later day, so an earlier target would date work before it happened. **Every tile route refuses a tile id whose date part is not a real day**, so `PATCH /tiles/{item@anything}` no longer creates a record on a non-date. **✓ on a tile with no written note falls back to the lines the dialog shows** (its own plus the folded tiles', oldest first), not its own alone. **A folded tile's row reports the hours it carried**, the gap frozen at the fold (58), as `hours`, `computed_hours` and `captured_hours`; `logged_hours` stays that day's Harvest. Before, the frozen gap was read as captured time and that day's Harvest hours came off it a second time: 3 h captured and 0.5 h logged carried 2.5 h and reported 2.0. **Rejected:** reporting the day's own captured time on a folded row (it would show hours the target now owns), hours 0 for a folded row (loses what it moved).

### 61 — A tile's hours are "set by hand" only when a person typed them
Review of 57 found one field, `hours_override`, written by three events: ✓ stored what it sent, the Desk tab's dialog PATCHed its prefilled hours on every Save, Polish, Add line and ✓, and nothing could clear it. A tile whose ✓'d entry was deleted reopened proposing the deleted entry's hours and could never close as covered; merely opening a tile froze its hours against later session time. **Now `hours_override` is only what a person typed.** ✓ keeps what it sent as `sent_hours`, which an approved tile reports and which is cleared when the entry goes and the tile reopens (it then proposes the current gap, and closes as covered once Harvest covers it again). **`PATCH /tiles/{id}` with `"hours": null` clears the override**; absent leaves it, a number sets it. A typed override survives a reopen. Tiles already stuck from before keep their stale override until cleared with null. The UI sends hours only when its field changed, and offers a way back to computed (inbox drop to `embarch-ui`). **Rejected:** clearing the override on any reopen (loses a person's choice), deriving "typed" by comparing the PATCHed hours with the computed ones (a person who types the computed number is still choosing).
