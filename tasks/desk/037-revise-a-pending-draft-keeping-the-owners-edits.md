# 037 — Revise a pending draft without mixing the agent's revision into the owner's edits

**State:** claimed by agent/desk/037-revise-a-pending-draft-keeping-the-owners-edits, 2026-11-18 03:18
**Source:** Fleet Ready issue: an agent revising its own pending draft after the owner had edited it patched the draft and its untouched baseline copy with a throwaway script, so the learning diff stayed limited to the owner's edits.
**Issue:** EMB-165
**Scope:** desk
**Hardware:** none
**Owner:** no

## What

A pending desk draft (`linear_draft_comment`, `linear_draft_edit` and their kin) holds one body today. When a session drafts outgoing text, the owner edits it on the Desk tab, and the session is then asked for a change, the session has to apply its revision without overwriting the owner's edits, and the text used afterwards to learn from the owner's edits must contain only the owner's changes, never the agent's revisions.

Make the desk keep the two apart: store the agent's version of a pending draft beside the current body (each agent revision a new agent version, each owner edit through the existing `PATCH /drafts/{id}` changing only the body), give the draft tools a revise call that applies one change (replace a named section, or append) to both the agent version and the owner's current body without disturbing the owner's other edits, and expose the last agent version so that, after Send, the diff between it and the sent text is the owner's edits alone. A revision that cannot be applied without touching an owner edit is refused with what collided, never merged silently. The exact shape is the worker's call within `embarch-desk`.

## Why now

The owner moved the issue to Fleet Ready. The issue's own Direction prefers a draft history in the desk over a CLI verb beside a skill, and the desk is where the owner already edits and sends drafts.

## Dispatch notes

- **Burndown: no new numbered decision.** Document the tools and the stored fields in `spec.md`/`interfaces.md`. If the design genuinely needs one (for example, whether the desk now records owner edits as a history), implement the part that does not, say so in this file, and the supervisor files it.
- **`interfaces.md` is in reserve: 14,133 of 15,360 B, 1,227 B left**, filed against `tasks/desk/036-compact-desk.md`, `blocked` on `In flux: yes`. **Compact it as part of this unit**: move the MCP agent-tool inventory (the plugin paragraph's tool list) into a sibling file under `interfaces/` verbatim, as `interfaces/cli.md` was split off, leaving a link and the index row current. Carry 036's **Must not delete:** — the route and MCP tool lists and their decision/EMB citations. Then add this unit's tools to the moved list. Do not edit 036; the supervisor closes it at the fold.
- The `gabriel-voice` skill that keeps the local `.orig.md` baseline today is not in the suite; do not look for it or edit it. The desk side is the whole of this task.
- No other file of this sub-project is in reserve.

## Done when

- [x] A session applies a revision to a pending draft through a desk tool, without writing a script, and the owner's earlier edits survive it.
- [x] After Send, the desk can give the last agent version, and its diff against the sent text contains only the owner's changes.
- [x] A revision that would overwrite an owner edit is refused and says what collided.
- [x] `scripts/check-doc-size.py --pressure` no longer lists `embarch-desk/interfaces.md`; the moved text is byte-identical in its new file.
- [x] Tests cover the cases above; gate green (`../../embarch-fleet/gate.md`); `spec.md`/`interfaces.md` updated, `changelog.d/` fragment dropped, `features.d/desk-<NNN>-*` row if it is a user-visible feature.

## Done

- Desk: `src/draftedit.rs` (section and append revision, owner-only diff), `Draft.agent_body`, `POST /drafts/{id}/revise`, `GET /drafts/{id}`, MCP `desk_revise_draft` and `desk_get_draft`, skill line. A draft made before this unit has no `agent_body`; its body at first revision stands in for it.
- Docs: `interfaces.md` split (tool inventory verbatim to `interfaces/mcp-tools.md`, now 12,549 of 15,360 B, out of reserve; closing 036 is the supervisor's); `spec.md` went into reserve by 147 B and is filed as `tasks/desk/038-compact-desk.md`.
- **No decision filed (burndown).** Open for the supervisor: whether the desk should record owner edits as a history rather than one agent version plus the current body, and whether `github_replies` drafts (one body per thread) should get per-reply revision. Both left out; a `github_replies` revise is a 400.
- Direct-write desks send at creation, so there is nothing to revise there.
- The Desk tab (embarch-ui) does not show `agent_body` or the diff; that is a UI task.
- One `cargo test` run in several failed once with 1 of 292 (not reproduced in six further runs, nor identified; the output was not captured).
