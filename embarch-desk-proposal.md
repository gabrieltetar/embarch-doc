# Proposal: embarch-desk — work items, connectors and time that tracks itself

**Status:** proposal, 2026-10-22.

Adds a sub-project, `embarch-desk`, and touches `embarch-ui` (its Dashboard tab becomes **Desk**), `embarch-api` (work-item tools for agents) and `embarch-umbrella` (installs the service and the plugin), which is why it sits at this repo's root ([DOC-PROTOCOL.md](DOC-PROTOCOL.md) §3). Shaped over thirteen rounds of questions with the owner; the round-by-round record is in git.

## Why

**Today the owner asks a Claude Code session, by hand, to read a Linear issue and to log time in Harvest.** Linear, Harvest, GitHub and Slack each hold one end of a link — the issue, the time entry, the PR, the thread — and **none of them holds the join**, so every session rebuilds it from scratch and every day's timesheet is reconstructed after the fact.

**The Dashboard tab carries nothing of its own.** Its stat cards, enrolled-boards table and alerts list ([embarch-ui spec/tabs.md](embarch-ui/spec/tabs.md)) all render from the snapshot Topology already draws better, and the alerts moved behind *Validate topology* ([embarch-ui](embarch-ui/decisions.md) decision 44).

## What the owner chose (2026-10-22)

**The desk**

1. **A work cockpit**: one page for the user's day across clients. EmbArch's hardware work is one source inside it, not the frame around it.
2. **Any EmbArch user**, not one person: connectors are a plug-in point with a setup flow, nothing hardcoded, documented in the [user guide](suite/user-guide.md).
3. **The Dashboard tab becomes Desk**, and everything it shows today is deleted.
4. **One card per work item, its time tile inside it.** The card carries the issue's status (a dropdown), its PRs with CI state, its session count, its bench activity, today's tile, and **open in VS Code with a Claude Code session already prompted** with the issue, PR and work-item id. **Slack collapses to one bar** of mention and DM counts that expands to the feed.
5. **Cards appear on recent activity** — a session, PR or tile in the last N days, plus anything pinned — and **leave only when the user archives them**.

**Work items**

6. **The work item is an EmbArch object, and the reason the sub-project exists**: it joins a Linear issue to its PRs, Claude Code sessions, bench activity and time. **Usually one Linear issue; it can start without one** (a call, a meeting, ad hoc support) and gain an issue later.
7. **A session knows its work item from the desk's store**: set at launch from a card, or **asked in the session** — "which work item is this?" — **on every prompt until answered**.
8. **A work item finds its repo by**: the working directory of a session already on it, else its PR's GitHub repo matched to a clone on disk, else the user picks a folder once.
9. **PRs attach by the issue key** in branch or title. **Bench activity attaches too** — a build, flash or study run through `embarch-api` from a session lands on that session's work item ("3 flashes, 1 study, pass"). Neither is a time source.

**Time**

10. **Captured automatically, sent only on approval.** Each work item gets **one tile per day**, a small square with a **green ✓ that sends it to Harvest and a red ✕ that discards it**. An unacted tile stays, dated, until the user acts. Nothing expires and nothing is sent on its own.
11. **The only time source in v1 is Claude Code sessions, measured as session-open time** — start to last activity, **idle gaps included**. Parallel sessions on two items both count in full. **Over-capture, then cut**: in the owner's words, *"I always rather have agents generate too much content that I have to cut down than the opposite."*
12. **An ignore list of repos and folders is never tracked**: no tile, no question. EmbArch's own repos go on it — open-source work is not tracked work — **and that excludes the agent fleet**, which only ever works there, with no change to the fleet.
13. **The note is written live and polished once.** A hook turns **every commit message into a line** on the tile; the session's Claude adds a line at **each milestone with no commit** (an investigation's finding, a flash or study result). **Opening the tile runs one `claude -p` call** that merges the lines into one Harvest note in the user's voice and **guesses the Harvest project and task** — inferred from names and past entries, corrected on the tile, no mapping step.

**Connectors and auth**

14. **Linear**: the card's issue status, movable. **GitHub**: PRs with CI state on their cards. **Slack**: every @mention and DM in every connected workspace, unread first — the fleet's own pages included — with **replies drafted by Claude and approved by the user**. **Harvest**: the tiles. Any number of accounts per service.
15. **Writes:** a status move goes straight through (issue status, timer, mark read). **Anything carrying prose is a draft the user approves first.**
16. **Pasted tokens in v1, one per account; OAuth deferred to v2.** GitHub reuses the user's `gh` login, or takes a personal access token; Linear takes a personal API key per workspace; Harvest a personal access token, which covers every account the user has. **Slack has no personal token**, so EmbArch ships a manifest: the user creates a Slack app in their own workspace from it, installs it, and pastes its user token — no distribution and no redirect, because the app never leaves that workspace. **EmbArch owns no app registration.** Chosen 2026-10-22 over OAuth in v1, the same day — see [OAuth, deferred](#oauth-deferred-to-v2).
17. **Tokens live in a file beside Core's**, owner-only, following [embarch-token.md](embarch-token.md)'s lifecycle.

**Agents and Claude Code**

18. **Hooks and skills ship as a Claude Code plugin**, installed once for every repo.
19. **Claude is called as `claude -p`** through the user's own install and login: no API key, and Claude Code becomes a prerequisite.
20. **Agents manage work items through `embarch-api`'s MCP tools** — look up, create, link an issue or PR, switch a session, add a tile line. **No agent ever approves a tile.**

**Scope**

21. **v1 ships whole, on one machine.** A Claude chat panel inside the desk is v2.

## Shape

### `embarch-desk`, the new sub-project

- **An always-on service beside Claude Code** — on a machine like the owner's, a systemd user service in WSL, not a Windows service beside Core. It runs `claude -p` and resolves repo paths locally; the Windows browser reaches it as it reaches `embarch-ui`. Umbrella installs and starts it.
- **One HTTP surface for three callers**: the plugin's hooks, `embarch-ui` and `embarch-api`.
- **The store** — work items, links, tiles, lines, the ignore list, archived cards — **lives outside every repo**. Connector data (issue titles, messages, client names, hours) never reaches an EmbArch repo; they are public.
- **Sync** pulls the issues, PRs and mentions the cards show; a write is one of the two kinds in 15.

### The Claude Code plugin

- **Hooks**: report session start and activity to the desk with the working directory; turn a commit into a tile line; check the ignore list; ask for the work item until answered.
- **Skill**: when to add a milestone line, and which `embarch-api` tools manage work items.

### `embarch-api`

- **Work-item MCP tools** (20), and **bench activity reported to the desk** against the calling session's work item (9).

### `embarch-ui`

- **The Dashboard panel's content is deleted** and the tab renamed **Desk**; the Core snapshot stays, since Topology renders from it.
- Cards, tiles and the Slack bar render from the desk's HTTP surface, not from Core.

### OAuth, deferred to v2

**OAuth was the v1 choice for a few hours, and was reversed because it buys onboarding polish for users who do not exist yet**, at the cost of four registrations EmbArch must own and the per-service catches below. If it comes back, it is **one registration per service, shipping only its client ID** — a secret inside a public binary is not one. Researched 2026-10-22 from each service's docs; **none of it has been tried**.

| Service | Desktop flow | The catch |
|---|---|---|
| GitHub | Device flow, a short code typed at github.com | None found — it is how `gh` logs in |
| Linear | Authorization code with PKCE, localhost redirect, no secret; refresh with `client_id` alone ([docs](https://linear.app/developers/oauth-2-0-authentication)) | The app's distribution must be **public** to install outside its own workspace ([manifests](https://linear.app/developers/oauth-app-manifests)); a workspace can require admin approval ([docs](https://linear.app/docs/third-party-application-approvals)) |
| Slack | Authorization code with PKCE; localhost counts as a desktop redirect only on a PKCE app ([docs](https://docs.slack.dev/authentication/using-pkce)) | Enabling PKCE is one-way; user scopes only; refresh tokens expire after 30 days. **A distributed app must use HTTPS redirects** ([docs](https://docs.slack.dev/app-management/distribution/)) |
| Harvest | **No PKCE**: implicit grant, no secret, no refresh token ([docs](https://help.getharvest.com/api-v2/authentication-api/authentication/authentication/)) | **Lifetime undocumented** for v2 implicit tokens — v1's lasted 18 hours. A personal access token, the fallback, is steadier |

## Rejected, and why

- **Hosting the desk inside `embarch-ui`**: sessions would be lost whenever the UI is closed. **A hook-written spool ingested later**: survives downtime, but no live tiles. **A Windows service beside Core**: every `claude -p` call and repo path crosses the WSL boundary, and Windows-service deploys need UAC.
- **Time between prompts, or last-prompt-wins across parallel sessions**: both undercount, against 11.
- **A fleet-arming hook to exclude the fleet**: the ignore list (12) already does it with no change to the fleet.
- **OAuth in v1** (16): four registrations to own, Slack's HTTPS rule for distributed apps, and Harvest's undocumented implicit-grant lifetime, for polish no second user needs yet. **The OS credential store**: one more dependency per platform.
- **An "Unsorted" card for sessions without a work item**, or auto-creating one per repo and branch: asking in the session (7) keeps attribution with the person who knows.

## Order of work

1. **v1, one milestone**: `embarch-desk`, the plugin, the `embarch-api` tools, the Desk tab, umbrella's install step.
2. **Fold**: acceptance creates `embarch-desk/` here and its repo; decisions move into the four files of each sub-project touched, and this file is deleted as it is absorbed.

## Open questions

- **A managed Slack workspace may require admin approval to install any app**, the user's own included. Where it does, that workspace has no Slack feed until an admin approves.
- **If OAuth returns in v2**: does Slack's PKCE localhost redirect survive distribution (its docs state the HTTPS rule and the localhost rule and never reconcile them), and what is Harvest's real implicit-grant `expires_in`? A probe script for both was written and never run.
- **How `embarch-api` knows the calling session**, and so the work item a build or flash belongs to (9). Its MCP server is spawned per session, but what identifies that session to it is unchecked.
- **Session-open time in hook terms**: which events bound a session, and a session crossing local midnight splitting across two days' tiles.
- **The store's format and the MCP tool list.** Defaults taken without asking: N = 7 days (5), and a chip naming the account on a card when two workspaces of one service are connected.
