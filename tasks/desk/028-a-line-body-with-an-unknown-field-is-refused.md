# 028 — A line body the desk cannot honour is refused, and a session can take back its own line

**State:** claimed by agent/desk/028-a-line-body-with-an-unknown-field-is-refused, 2026-11-12 19:33
**Source:** EMB-141, found adding a todo for another item from a session, 2026-11-10
**Issue:** EMB-141
**Scope:** desk
**Hardware:** none
**Owner:** no

## What

`POST /sessions/{sid}/line` with `{"item":"w608","kind":"todo","text":"…"}`
against a deployed desk built before the `item` field (45d38e0, EMB-82) returned
`{"note_id":"n686","tile":"w575@…"}`: the line landed on the session's own item,
not on `w608`. `LineBody` ignores fields it does not know, so nothing told the
caller its target was dropped, and no route removes one line from a tile, so the
agent could not undo it; only the owner can, on the Desk tab.

Today's source has `item`, so this exact call now works. What is still true is
the class: **any field a desk does not know is dropped silently**, and the next
field added will misfile the same way against an older desk.

Two changes:

1. **Refuse what cannot be honoured.** A line body carrying a field the desk
   does not know is a 400 naming the field, and nothing is written.
   `#[serde(deny_unknown_fields)]` on `LineBody` (`src/server.rs`) is the
   obvious route; check whether the 400 names the field in the shape the desk's
   other refusals use, and whether the same holds for `tile_line`'s body.
   **Before you refuse anything, grep the suite read-only for every caller of
   these routes** (`embarch-chat/src/desk/client.ts` sends `text` and `kind`;
   look for hooks, scripts and other clients too). A caller that sends a field
   the desk does not know is **not yours to change**: file it with
   `scripts/fleet-linear.py file --from worker --project <its repo>` and name it
   here.
2. **Take back a line.** An agent can remove a line its own session wrote, by
   note id, through the API and an MCP tool (`src/mcp.rs`). Only a line that
   session wrote, and only while its tile is unsent; say what a sent tile's
   line answers. This is a new route and a new tool, so it is a decision: write
   it in the `decisions/` file of its subject (`notes.md` or `sessions.md`,
   whichever holds the line routes' decisions), with the reason, and update
   `spec.md` and `interfaces.md`.

**What you may change.** Only `embarch-desk` and `embarch-doc/embarch-desk/`.
**Never deploy, restart or rebuild the installed desk**: the fix reaches the
running desk only when the owner deploys it, and that is a debt for this file.

## Why now

A misfiled line sits on the wrong tile, which is time and notes attributed to
the wrong work item, and today the agent that made the mistake cannot see it
happened or undo it.

## Done when

- [x] A line body with a field the desk does not know is refused with a 400
      that names the field, and nothing is written.
- [x] An agent can remove a line its own session wrote, by note id, through the
      API and an MCP tool, and cannot remove another session's.
- [x] Tests cover both.
- [x] The callers grep is recorded here, with any issue it filed.
- [x] Gate green (`../../embarch-fleet/gate.md`), and a deploy debt written here.

## Result

- Decision 85 (`embarch-desk/decisions/notes.md`). Unknown field: collected by `#[serde(flatten)]` on `LineBody` and refused in `LineBody::note` as a 400 naming each field (axum's `deny_unknown_fields` would answer 422). Covers `tile_line` too. Take-back: `DELETE /sessions/{sid}/line/{nid}` and MCP `desk_remove_line`; 403 another's, 404 unknown, 400 on a sent tile.
- **Callers grep** (2026-11-12, read-only over embarch-chat, embarch-ui, embarch-api, embarch-fleet, embarch-doc/scripts, the plugin and hooks): `embarch-chat/src/desk/client.ts` sends `text`, `kind`; `embarch-ui/assets/desk.js` and `tests/browser/drive_desk.py` send `text`, `kind`; the desk's own MCP tool sends `text`, `kind`, `item`. No caller sends an unknown field; **no issue filed**.
- Gate: cargo build, test (260), clippy green; doc gates below.

## Deploy debt

The installed desk is untouched. Until the owner deploys this build, a running desk still drops unknown fields and has no `desk_remove_line`. After deploy, verify on the live desk: POST `/sessions/<sid>/line` with `{"text":"x","bogus":1}` answers 400 naming `bogus`; `desk_add_line` then `desk_remove_line` removes it from the tile. The plugin's MCP server restarts with the binary, so open chats need a new session to see the tool.
