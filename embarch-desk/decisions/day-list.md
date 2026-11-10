# embarch-desk decisions: The day list and Harvest defaults

**Status:** active, 2026-11-10.

A tile's default Harvest target, the Desk tab's cards and today's work, and what Harvest already holds joining the day, split out of [desks.md](desks.md) (2026-11-10, verbatim; decisions 38, 40, 41).

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 38 — A tile defaults to its desk's Harvest target
Every tile starts on its desk's project and task, changeable per tile; with a desk target, polish drafts only the note and fetches no Harvest lists. **Rejected:** a target fixed per desk, and a fixed project with a guessed task.

### 40 — The Desk tab: the UI's desk's cards, then today's work
Cards for the UI's desk only, every desk's unsent tiles in the hand above them (57; a strip of other desks' tiles until 2026-10-25), and **"Today's work" below** — every work item with time, a line, bench activity or a session that day, grouped by desk with the open one first, each row linking out to Linear and GitHub with its lines, note, status and sessions; a date picker reads other days. **Rejected:** a Harvest-style week grid, and a separate tab.

### 41 — What Harvest already holds joins the day, and a tile proposes only the gap
The first evening of real use showed the day list empty beside six hours already in Harvest: it read only the desk's own tiles. **Each day's Harvest entries are fetched** (today every two minutes, any other day when it is read, and a day with a waiting tile every ten minutes and at ✓, 62) **and merged into the work item whose issue their note names**; an entry naming an issue with no card **makes the card**, dated by the entry so an old day read back does not look like today's work; an entry naming none is its own row under the desk billing its Harvest project. **A tile proposes only the time Harvest doesn't already hold** for its item that day, the entry its own ✓ made aside. **The user can edit an entry's hours and note, or delete it, from the list**; deleting one a tile made reopens that tile. **Rejected:** a separate "already in Harvest" block per desk (two lists for one day), read-only entries, and keeping the full captured time on the tile. Silently dropping a tile Harvest already covers was rejected too, until a 0h00 tile asking for ✓ or ✕ reversed it (57).
