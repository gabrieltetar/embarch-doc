# Dashboard connectors: working notes

**Status:** draft, 2026-10-22. Shaping notes for reworking `embarch-ui`'s Dashboard tab around external connectors. Not a spec and not yet a proposal: it records the starting point, each question asked and its answer, and what is still open. When the shape settles it becomes a `*-proposal.md` (or folds straight into [embarch-ui/spec](../spec.md)) and this folder is deleted.

## The ask

Remove everything the Dashboard shows today. Replace it with a way to **add connectors — Linear, Harvest, Slack, GitHub — and handle all of them from the dashboard.**

## The shape so far

After twelve rounds of questions. The numbered decisions below are the record; this is the current truth they add up to.

- **A new always-on sub-project, `embarch-desk`,** owns the connectors — Linear, Harvest, Slack, GitHub, each over OAuth with a pasted token as fallback, any number of accounts per service — and the **work item**: an EmbArch object, usually one Linear issue, joining that issue to its PRs, its Claude Code sessions, its bench activity and its time.
- **The Dashboard tab becomes Desk.** Everything it shows today is deleted. In its place, **one card per work item with recent activity**: issue status (movable from the card), PRs with CI state, sessions, bench activity, *open in VS Code with Claude Code prompted*, and **today's time tile inside the card**. Slack mentions and DMs sit on one bar that expands to the feed.
- **Time captures itself and lands only on approval.** A Claude Code plugin's hooks report session-open time to the desk; each session's Claude appends a line to its tile as it works; opening the tile turns the lines into one Harvest note with a guessed project and task; **✓ sends it to Harvest, ✕ discards it.** Over-capture and cut — but fleet sessions never count.
- **Writes:** a status move goes straight through; anything carrying prose is a draft the user approves. Agents manage work items through `embarch-api`, and never approve a tile.
- **v1 ships whole, on one machine.** A Claude chat panel inside the desk is v2.

## Starting point

**What the Dashboard shows now** ([spec/tabs.md](../spec/tabs.md), `embarch-ui/assets/index.html`): three stat cards (boards enrolled, attached probes, open alerts), an enrolled-boards table and a recent-alerts list, all rendered from the one `Snapshot` Core is polled for (`embarch-ui/src/snapshot.rs`). Topology renders from the same snapshot, so removing the Dashboard's cards does not remove the poll. **Every one of those facts is already shown, better, somewhere else**: the boards and probes on Topology's diagram, the alerts behind *Validate topology* (decision 44).

**What already reaches these four services, outside the UI:**

| Service | Reaches the owner today through | Notes |
|---|---|---|
| Linear | Two Linear MCP servers in Claude Code, one per workspace (the owner's company and a client) | So one connector type already needs **more than one account** |
| Harvest | Harvest MCP server; the `harvest:day` and `harvest:track` skills | `harvest:day` already joins a day's work to **one entry per Linear issue** |
| Slack | claude.ai Slack connector; the fleet's own `scripts/fleet-*.py` bot | #embarch-fleet is the fleet's command channel — [remote surfaces](../../embarch-remote-surfaces.md) |
| GitHub | `gh` CLI | All EmbArch repos are public; client repos are not |

**Constraint from the start: this repo is public.** Connector *data* — issue titles, Slack messages, client names, hours — never lands in any EmbArch repo, and these notes name no client.

## Decisions so far

**Round 1, 2026-10-22.**

1. **Purpose: a work cockpit.** One page for the owner's day across clients — issues on their plate, PRs waiting, Slack mentions, the running timer. EmbArch's hardware work is one source inside it, not the frame around it.
2. **Users: any EmbArch user.** A generic, public feature of the suite. Connectors are a plug-in point with a setup flow; nothing is hardcoded to one person's accounts, and the user guide documents it.
3. **Plumbing: a new sub-project** owns the tokens and the sync. The UI and `embarch-api` both read from it, so an agent sees the same data the dashboard does.
4. **Depth: not settled, but the answer reframed the whole idea** — see below.

**The reframe: a *work item*, and automation instead of manual calls.** Today the owner tells a Claude Code session to read a Linear issue and to track time in Harvest — each one a manual call. EmbArch should do that to some degree by itself. That wants a concept of **work item** spanning a Linear issue, its Harvest entries and its GitHub PRs — and **Claude Code (and possibly VS Code) belong in the dashboard too**, as sources of activity rather than only as consumers.

**Round 2, 2026-10-22.**

5. **A work item is a Linear issue** plus everything linked to it — its PRs, its Harvest entries, the Claude Code sessions that worked on it. Matches `harvest:day`'s one-entry-per-issue rule. Work with no issue still needs a home (open below).
6. **Time is captured automatically, and lands only on approval.** The dashboard shows each ongoing entry as a **small square tile with a green ✓ and a red ✕ along its bottom edge**: ✓ adds it to the real Harvest timesheet, ✕ discards it. Capture is automatic; the timesheet is not.
7. **Claude Code and VS Code, v1:** sessions show as activity on the work item they touched (and feed the time tiles); a work item can **launch a Claude Code session** seeded with the issue, PR and repo; a work item **opens its repo and branch in VS Code**. **A chat panel inside the dashboard is v2.**
8. **Writes: status moves go straight through** — move an issue's status, start or stop a timer, mark a notification read. **Anything carrying prose** — a comment, a Slack reply, a time entry's note — **is a draft approved first.** The time tile in 6 is that rule's approval surface for Harvest.

**Round 3, 2026-10-22.**

9. **v1 watches one signal: Claude Code sessions.** VS Code focus, git/GitHub activity, Slack threads and bench runs are not time sources in v1.
10. **One tile per work item per day**, growing as the day goes — one tile becomes one Harvest entry.
11. **Issue → Harvest project and task is inferred**, from names and past entries, and corrected on the tile. No mapping step at setup.
12. **Claude drafts the tile's note**, from what the sessions did, in the user's voice, editable on the tile before ✓. **How is 36.**

**Round 4, 2026-10-22.**

13. **Working time is session-open time**: from a session's start to its last activity, idle or not. It overcounts on purpose, and the tile is where it gets trimmed.
14. **Parallel sessions on two issues both count in full.** No splitting, no last-prompt-wins; the user trims on the tile. (A session's minutes are only ever on one tile, so this is a choice about overlap, not about double-counting one session.)
15. **A session knows its issue because EmbArch's work-item store says so** — see 17.
16. **Claude is called as `claude -p`, headless**, through the user's own Claude Code install and login. No API key to configure; Claude Code becomes a prerequisite of `embarch-desk`.

**Round 5, 2026-10-22.**

17. **The work item is a new EmbArch backend object, and the reason the sub-project exists.** It is what ties a Linear issue to its sessions, PRs, Slack threads and time tiles — the services each hold one end of a link and none of them holds the join. So the session→issue link lives in EmbArch's work-item store, not inferred afresh on each read.
18. **Over-capture, then cut — the governing principle.** In the owner's words: *"I always rather have agents generate too much content that I have to cut down than the opposite."* So **agent sessions** (fleet workers, supervisors, subagents) **make tiles too**, as do sessions EmbArch did not launch. Decisions 13 and 14 were already this principle; the tile's ✕ is what makes it affordable. **Amended by 40: fleet sessions are excluded.**
19. **Slack, v1: a mentions-and-DMs feed, and draft replies** (Claude drafts, the user approves — decision 8). Threads are not attached to work items in v1.
20. **GitHub, v1: PRs attach to their work item**, by the issue key in branch or title, with state and CI status. No review-request list and no merge or approve buttons in v1.

**Round 6, 2026-10-22.**

21. **The sub-project is `embarch-desk`.**
22. **A work item can exist without a Linear issue** — a client call, a meeting, ad hoc support starts as a standalone work item and gains an issue later. Its tiles still reach Harvest. This amends 5: a work item is *usually* an issue, and is always an EmbArch object (17).
23. **`embarch-desk` is an always-on service**, installed and started the way Core is (umbrella sets it up). Claude Code hooks post session events to it over HTTP, so tiles are live. Rejected: a hook-written spool file ingested later (survives the service being down, but no live tiles), and hosting it inside `embarch-ui` (sessions lost whenever the UI is closed).
24. **The cockpit lists work items with recent activity** — a session, PR or tile in the last N days — plus anything pinned. Not every open assigned issue.

**Round 7, 2026-10-22.**

25. **The tab is renamed: Dashboard becomes Desk** in `embarch-ui`, matching the sub-project.
26. **Layout: one card per work item, its tile inside it.** The card carries the issue's status, its PRs with CI state, its session count, its bench activity (32), the day's tile with ✓/✕, and the launch buttons (Claude Code, VS Code). Standalone work items (22) are cards too. **Slack collapses to one bar** — mention and DM counts — that expands to the feed. Rejected: a strip of tiles across the top with work items below, and three side-by-side columns.
27. **Agents manage work items through `embarch-api`'s MCP tools** — look up what they are on, create a work item, link an issue or PR, switch a session to another item, add to a tile's draft note. **No agent ever approves a tile**: ✓ is the human's alone.
28. **An unacted tile stays until the user acts on it**, marked with its date. Nothing expires and nothing is sent by itself.

**Round 8, 2026-10-22.**

29. **Auth: OAuth from v1 for all four connectors, with paste-a-token as the fallback on every one** — see [What OAuth would take](#what-oauth-would-take). No hosted server.
30. **Tokens live in a file beside Core's token**, owner-only permissions, following [embarch-token.md](../../embarch-token.md)'s lifecycle. Plain text at rest, as Core's is. Rejected: the OS credential store (encrypted at rest, but one more dependency per platform).
31. **v1 ships whole**, in one milestone: everything decided above. Rejected: the time loop first, or read-only cards first.
32. **Bench activity attaches to the work item, v1** — a build, flash or study run through `embarch-api` from a session lands on that session's work item as activity ("3 flashes, 1 study, pass"). **Not a time source** (9).

**Round 9, 2026-10-22.**

33. **The hooks ship as a Claude Code plugin** — `embarch-desk`'s plugin carries the session hooks and the agent-facing skills; installed once, it covers every repo, versioned with the suite. Rejected: umbrella writing user-level settings, and per-repo settings (which miss every session outside an EmbArch repo).
34. **"Launch Claude Code" opens the repo in VS Code with a Claude Code session already prompted** with the issue, its PR and the work-item id. Rejected: a terminal `claude`, and a background agent working the issue alone.
35. **A work item finds its local repo by, in order:** the working directory of a session already on it; else the linked PR's GitHub repo matched to a clone found on disk; else the user picks the folder once.

**Round 10, 2026-10-22.**

36. **The note is written live by the sessions, and polished once.** A hook only reports facts — time, repo, branch, tools run; it is a shell command, not a model, and cannot write a sentence. So **each session's own Claude appends a line to its tile through `embarch-api`** as it finishes a piece of work (27), at no extra cost. **When the user opens the tile, one `claude -p` call merges every session's lines into one Harvest note** in the user's voice and guesses the Harvest project and task (11). Rejected: raw lines with no polish (reads like a changelog), and the desk summarizing transcripts itself (a call per tile, no live text).
37. **A card leaves the desk only when the user archives it.** Not on issue close, not after a quiet spell. Decision 24's activity window decides which cards *appear*, not which go.
38. **One machine, v1.** `embarch-desk` and its store live on the machine with the bench; a laptop's sessions elsewhere are not seen.

**Round 11, 2026-10-22.**

39. **Every user signs in as themselves; EmbArch ships the registered apps.** One app registration per service, shipped with the suite; each user's token is theirs alone. Rejected: bring-your-own registrations, which cost each user about what pasting tokens does. Who owns the four registrations: 43.
40. **Fleet work is never tracked.** Listener, supervisor, worker, reviewer and every other fleet session makes no tile, on any work item. **This amends 18**: over-capture still governs the sessions a person works in — a subagent's time is already inside its parent session's — but the fleet's own sessions are not the user's time.
41. **A session with no work item in sight asks.** The plugin has Claude ask "which work item is this?" on the session's first prompt — pick a card, name an issue, or start a standalone item. Rejected: an "Unsorted" card collecting orphan tiles, and auto-creating a standalone item per repo and branch.
42. **The card's Linear action in v1 is a status move**, from a dropdown — a status move, so it goes straight through (8). No in-desk comments, no description reader, no issue creation from a standalone item in v1.

**Round 12, 2026-10-22.**

43. **The four app registrations belong to the personal account that owns the public EmbArch repos.** Least setup, and tied to the project's owner rather than to an employer. Rejected: a new EmbArch identity across four services, and the company's workspaces.
44. **The Slack feed is every @mention and DM in every connected workspace**, unread first. No picked channels, no unanswered-only filter.

## What OAuth would take

Asked in round 7 instead of picking an auth model. Researched 2026-10-22 from each service's docs; **nothing here has been tried**.

**The shape is the same for all four: EmbArch's maintainer registers one app per service, once, and ships its client ID — never a secret, since a secret inside a public binary is not one.** The always-on `embarch-desk` service (23) already listens on localhost, so the redirect lands on one route of it. Then: store the token, refresh it, and offer "re-connect" when a refresh fails.

| Service | Flow for a desktop app | Secret needed | The catch |
|---|---|---|---|
| GitHub | **Device flow**: the user types a short code at github.com | No | None found — it is how `gh` itself logs in. Or reuse an existing `gh` login and skip OAuth entirely |
| Linear | Authorization code **with PKCE**, localhost redirect | No — `client_secret` optional under PKCE; refresh with `client_id` alone | A workspace can require admin approval of third-party apps ([docs](https://linear.app/docs/third-party-application-approvals)); whether the app must also be marked public to install in other workspaces is unchecked |
| Slack | Authorization code **with PKCE**; a localhost redirect counts as a desktop redirect *only* on a PKCE-enabled app ([docs](https://docs.slack.dev/authentication/using-pkce)) | No | **Enabling PKCE is one-way.** Desktop redirects get **user scopes only, no bot scopes** — which suits a feed and replies sent as the user. **Refresh tokens expire after 30 days.** Installing in other workspaces needs the app's public distribution turned on (from memory, unchecked) |
| Harvest | **No PKCE.** Implicit grant (token returned directly, no secret; documented for browser apps) or authorization code (needs the secret) ([docs](https://help.getharvest.com/api-v2/authentication-api/authentication/authentication/)) | Only for authorization code | **The weak one.** Implicit grant returns no refresh token, so the user re-connects whenever the token expires (lifetime unchecked). The only alternative is a hosted relay holding the secret — a server EmbArch would have to run |

**Accepted in round 8 (decision 29):** OAuth from v1 for all four, no server anywhere — device flow for GitHub, PKCE for Linear and Slack, implicit grant for Harvest — **and keep paste-a-token as the fallback on every connector**, which is also the way in for a workspace whose admins block third-party apps.

## Open questions

Not yet asked, or surfaced by an answer. Ranked by how much each one moves the design.

1. **How does the plugin tell a fleet session from a person's (40)?** The fleet's agents have known definitions and run in the listener window; whether a hook's payload carries enough to tell is unchecked. And do fleet sessions show on a card as *activity* at all, or are they invisible to the desk?
2. **Where `embarch-desk` runs on a split machine.** Core is a Windows service, while Claude Code sessions here run in WSL and the browser on Windows. The desk must be reachable from the hooks, the UI, `embarch-api` and the OAuth redirect at once — Core already solves the same reachability, so start from [embarch-token.md](../../embarch-token.md) and umbrella's topology.
3. **What session-open time is, exactly (13).** Which hook events count as activity, what bounds a session left open overnight, and whether a session crossing midnight splits across two days' tiles.
4. **The agent-facing surface (27, 36):** the `embarch-api` MCP tools for work items and tile lines, and what the plugin's skill tells a session to do — how often it appends a line, and how it asks for a work item (41) without nagging.
5. **Before registering any app (43):** Harvest's implicit-grant token lifetime, whether a Linear app must be marked public to install in other workspaces, and Slack's distribution step.

Smaller: the activity window N for which cards appear (24); how a card shows which account it came from when two Linear workspaces are connected; whether the fleet bot's own posts reach the Slack feed (44) and need filtering.

## Next

Promote these notes to `embarch-desk-proposal.md` at the root (the proposal tier, [DOC-PROTOCOL.md](../../DOC-PROTOCOL.md) §3) once the five questions above are answered, add it to [embarch.md](../../embarch.md) §6, and delete this folder.
