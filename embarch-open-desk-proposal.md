# Proposal: an open Desk instead of an open project

**Status:** proposal, 2026-10-22.

Spans `embarch-desk`, `embarch-ui` (its open project, decision 46, and the Desk tab, decision 56), `embarch-api` (its default build target) and the bench (`embarch-ui`'s saved benches, decision 44), which is why it sits at this repo's root ([DOC-PROTOCOL.md](DOC-PROTOCOL.md) §3). Shaped with the owner in five rounds of questions on 2026-10-22.

## Why

**Clients sometimes work in Intercreate's Linear, Slack and GitHub, and sometimes in their own.** One set of connectors cannot say which Linear project or which GitHub org a piece of work belongs to, so agents search everything and the Desk tab mixes every client. **Harvest is always Intercreate's** — it is how the client is billed — and a client's own Slack is not worth connecting.

**And the suite already has one "thing that is open"**: `embarch-ui`'s open project, a firmware repo (decision 46). That is half of a client engagement. A Desk is the whole of it.

## What the owner chose (2026-10-22)

**What a Desk is**

1. **A Desk is one Linear project plus one Harvest project.** The Linear project lives in whichever workspace the client uses, ours or theirs.
2. **It binds** its Linear project; its GitHub org and repos; its firmware repo(s) — what `embarch-ui` calls the open project today; its Harvest project and task, on Intercreate's account; and its saved bench. **Its page shows its firmware repo's saved studies and atlas.**
3. **Slack is not per desk**: Intercreate's workspace only, one feed for all desks.
4. **A desk is created from a form on the Desk tab** — the Linear project (from every connected workspace), the Harvest project and task, the GitHub repos, the firmware repo folder, the saved bench. The first is the owner's current project; a new one is made when a new project starts.

**The open Desk**

5. **One open desk at a time, suite-wide**: every UI tab (the open-project control becomes the open-desk control), the agents' Linear and GitHub tools, `embarch-api`'s default build target, and the bench. Several concurrent desks are a later question.
6. **"No desk" is a state**: the UI opens a bare firmware repo the way it does today — EmbArch's own work, a quick look — with no Linear, no Harvest, nothing tracked.
7. **Who switches it:** the owner from the UI, an agent when told to, the CLI (`embarch-desk open <desk>`), and the question a session asks (8).
8. **A session that starts in another desk's repo asks** whether to switch. **If the answer is "stay", its time still lands on its own desk**: the open desk decides what is shown and where agents and the bench point, not what is tracked.
9. **Opening a desk proposes its saved bench; one click applies it** — the saved-bench behaviour Topology already has (`embarch-ui` decision 44). **If a study, flash or bootload is running, the switch asks each time**, showing what is running.

**Work items and time**

10. **A desk's Harvest project and task are each tile's default, changeable per tile.** Claude stops guessing the project and only drafts the note.
11. **A standalone work item (a call, a meeting) asks which desk it is on** when it is created.

**The Desk tab**

12. **The open desk's cards on top**, plus a strip of other desks' unsent tiles, so nothing waits unseen.
13. **"Today's work" right below the cards: a day list**, with a date picker for other days. **All desks, grouped by desk, the open one first.** Each work item's row carries **links out** (the issue's title opens it in Linear, each PR opens on GitHub with its CI), **what was done** (its lines and note), and **its status and sessions**.

## Shape

### `embarch-desk`

- **Desks** in the state file: name; Linear workspace label, project id and name, and its team; Harvest account, project and task; GitHub repos; firmware repo paths; the saved bench's name. **The open desk** (or none) is one field the desk owns; everything else reads it.
- **Every work item belongs to a desk.** An issue's desk is the one whose Linear project holds it; a standalone item's is chosen at creation (11). Today's cards move to the first desk.
- **Agents' tools take the open desk as their scope**: `linear_my_issues` and `linear_search` within its project, `linear_draft_issue` into it (no team key to guess), PRs searched in its repos. New: `desk_open`, `desk_list_desks`.
- **A session's question (8)** comes from the SessionStart hook when its working directory is under another desk's firmware repo. Its answer goes back through `desk_open` or "stay".
- **Polish drafts the note only** when the tile has its desk's target (10).

### `embarch-ui`

- **The sidebar's open-project control becomes the open-desk control** (decision 46 amended): a desk, or a bare repo for "no desk" (6). Every tab that uses the firmware repo takes the open desk's.
- **The Desk tab**: the desk form (4); cards (12); "Today's work" (13).
- **On switching**: Topology's saved-bench proposal for the desk's bench (9), and the busy question when Core reports a study, flash or bootload running.

### `embarch-api`

- **Its default project follows the open desk's firmware repo**, read from the desk when a call names no project. A call that names one is unchanged.

## Phases

1. **Desks in `embarch-desk`**: the model, the form's routes, scoping the agent tools, the session's question, Harvest defaults. About half a day.
2. **The Desk tab**: the form, the open-desk control on the tab, the cards strip, "Today's work". About half a day.
3. **Suite-wide**: the sidebar control replacing the open project, `embarch-api`'s default, the bench proposal and the busy question. About a day; it touches `embarch-ui` decision 46 and `embarch-api`'s project resolution.
4. **The first desk** — the owner's current project — made from the form.
5. **Fold**: decisions into each sub-project's docs; this file is deleted as it is absorbed.

## Open questions

- **Which desk owns a firmware repo two desks both name?** Assumed: a repo belongs to at most one desk; the form refuses a second.
- **What "Today's work" counts as active**: a work item with time, a line or a session that day — assumed.
- **Several concurrent desks** (5) — deliberately later.
