# 016 — A session whose folder no longer exists says so, and carries no folder link

**State:** open
**Source:** Linear issue EMB-76, filed by a session
**Issue:** EMB-76
**Scope:** desk
**Hardware:** none
**Owner:** no

## What

A session row in the desk's view (`GET /view`, `view_sessions`) and in the session list carries a field saying its folder is missing when its `cwd` is non-empty and no longer exists on disk, and no `folder_uri` then. A row whose folder exists is unchanged.

Today both rows build `folder_uri` from the session's `cwd` whenever it is non-empty, without checking the folder exists. A client that opens that link (Go to chat, Jump) opens a VS Code window on a missing folder, and a chat panel there fails to resume.

## Why now

A chat whose landing deleted its own folder could not be reached, and nothing on the row said why.

## Where to look

- `src/server.rs` — the two row builders that set `"folder_uri": (!s.cwd.is_empty()).then(...)`, one in the session list and one in `view_sessions`
- `src/uri.rs` `folder_uri`
- `embarch-doc/embarch-desk/interfaces.md` — the `/view` and session-list rows
- `embarch-desk` decision 71 — the session list carries the links

## Dispatch notes

- **Only the desk's half is this task.** The issue's second item, the Work tab showing it on the row instead of Go to chat, is in a repo the fleet does not work; leave it. `embarch-ui/assets/desk.js` and `embarch-chat` read `folder_uri` already and hide their buttons when it is absent; do not edit them. If either needs to show the new field, say so in your report rather than filing it yourself.
- **Burndown is on: no new numbered decision.** Amending decision 71 in place to say when a row carries `folder_uri` is fine. If you find the change needs a new decision, write its proposed text under `## Owed decision` in this file and the supervisor files it.
- A missing folder is a cheap `Path::exists` per row per view; say in your report if you find a reason it is not.
- No `embarch-desk` doc in `embarch-doc` is in reserve at the split (`spec.md` 8,441 B, `interfaces.md` 11,124 B; check `scripts/check-doc-size.py` before you grow either).

## Done when

- [ ] With a session's `cwd` deleted, its rows in the view and the session list say the folder is missing and carry no `folder_uri`; a test covers it.
- [ ] A row whose folder exists is unchanged.
- [ ] `interfaces.md` states the field; decision 71 says when a row carries the link.
- [ ] Gate green (`../../embarch-fleet/gate.md`, the Rust bullet); `changelog.d/` fragment dropped.
