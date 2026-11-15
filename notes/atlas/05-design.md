# Atlas notes: the design plane

**Status:** draft, 2026-11-15.

## What it is

**What people decided the product should be**, as opposed to what the schematic and the firmware are. Today the atlas reads one design source, a PRD, into `requirement` records; a notes file is read as it is, and a "PRD → code trace" is listed as deliberately not built (`embarch-atlas` repo, `DESIGN.md`, "Kinds" and "Not yet built").

## Sources, and what may be cited

| Source | Read through | Version key | Citable |
|---|---|---|---|
| Linear issues | The desk, live | Issue key and `updatedAt` | **Yes** |
| GitHub PR discussions | The desk, live | Repo, PR number and `updatedAt` | **Yes** |
| Commit messages | git | Commit | **Yes** |
| Documents in the sources folder: PRD, architecture and design PDFs, meeting-notes files | `inventory`, as today | sha256 | **Yes** |
| Slack | The desk, once it has a Slack connector | None | **Never** |

**Slack is a finder, not a source.** Design information found in Slack that no Linear issue holds becomes **a Linear issue draft through the desk** (`linear_draft_issue`), pre-filled with what the thread states and the entities it names. It waits for the owner's Send on the Desk tab, as every desk draft does, and once sent it is citable. Chosen over a question row in `missing.md` and over both. **Slack reaches the atlas through a desk Slack connector**, scoped to the channels the engineer picks; chosen over a session snapshot, files dropped by hand, and leaving Slack for later.

## Read live through the desk

**The atlas reads Linear and GitHub through the desk's local API at question time; there is no snapshot.** The desk is already the agents' one access point to Linear, holds the tokens, and indexes every issue in its scope and every PR in its repos ([embarch-desk spec](../../embarch-desk/spec.md)), so the atlas needs no credentials of its own. **Live reads stay cacheable**: a claim, and a check that reads it, are keyed on the source and its `updatedAt`, so they are redone only when that source changes. Chosen over an atlas-written snapshot in the sources folder and over a snapshot written by a session.

**The desk does not serve the text yet.** `GET /refs` gives each issue's key, title, state and URL and each PR's repo, number, title, state, branch and issue keys; `GET /items/{id}/brief` gives a work item's description head and latest comments, capped at 16,000 characters ([desk routes](../../embarch-desk/interfaces/chat-routes.md)). Neither gives an issue's or a PR's full text, its comments and its `updatedAt` for an arbitrary key. That route is desk work.

## Which issues belong to a repo's design plane

**An LLM picks them, and asks the engineer when it is not sure.** It runs on demand, when a session asks a design question. Mention matching (below) runs over every source in the desk's index regardless, since it is free.

## Mentions: deterministic and free

A design source **mentions** an entity when the entity's name appears in it as a whole token: a net or one of its aliases, a board-qualified refdes, an MPN, a devicetree node name or label, a Kconfig symbol, an MCU pin, a requirement ID. The match runs over issue titles, bodies and comments, PR threads, commit messages and design documents' text layers, and records the entity, the source, the place and the quoted line, `prov: deterministic`. **This is what lets a design-against-hardware check run with no LLM at all** ([09](09-interactions.md#worked-example-a-bus-left-unconnected)).

## Claims: an LLM, on demand

**When a session asks, an LLM reads a mentioned passage and writes claims**: the entity, what the passage states about it (connects to, a value with its unit, a direction, a purpose, must or must not), the quote and the cite. The atlas's rules carry over unchanged: every number must be in the quote, a failing claim is kept and marked, and a claim is frozen on its source's version key.

## Open

- **The desk route**: an issue's or PR's full text, comments and `updatedAt`, served from the desk's cache. And the Slack connector, with its channel scope.
- **Where the scope answers are kept.** Recommended: beside the engineer's other answers (`inventory/answers.toml`), so no issue's membership is asked twice.
- **The claim record's fields, and superseding.** Recommended: a later statement in the same issue or thread supersedes an earlier one; two sources that disagree are kept as a `conflict` (principle 4).
- **Names that differ in spelling** between prose and the netlist (a bus named once in prose, split into per-side nets in the schematic). A prefix match finds more and is noisier; measured on the first fixture before it is chosen.
- **The `desk unreachable` answer.** Recommended: the design plane answers that the desk is not running, listed under Not run, never counted as a pass.
- **Whether the PRD stays its own kind** or becomes one design source among the others.
- **A `design <entity>` lookup**: mentions and claims about the entity, newest first, with cites.
- **Meeting notes kept in a shared drive.** Today a file dropped in the sources folder; a desk connector for the drive is later.
