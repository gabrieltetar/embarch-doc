# embarch-desk: routes added for embarch-chat

**Status:** active, 2026-10-23. Split out of [../interfaces.md](../interfaces.md) on 2026-11-09, verbatim, when that file reached its reserve line. The caller's-desk rule (77) that follows this table stays in [../interfaces.md](../interfaces.md).

### Added for `embarch-chat`

Every route takes the desk's bearer token. Additions only; nothing above changed shape. `?desk=` takes a desk's id or its name. What the extension calls, and when: [embarch-chat's interfaces](../../embarch-chat/interfaces.md).

| Route | What |
|---|---|
| `POST /sessions/{sid}/assign` | Gains `"client": "embarch-chat"`, marking a session the panel runs; `/view` reports it. **A resume sends the mark alone**: the desk records it, then answers 400 for the missing item, so the panel reads `client` back from `GET /sessions/{sid}` rather than trusting the status ([open.md](../open.md)) |
| `POST /sessions/{sid}/line` | `{"text","kind"}`, kind `done` (the default), `finding`, `decision`, `handoff` or `todo` → `{"tile","note_id"}`, or `{"held":true}` when the session has no item yet (it lands once assigned); 404 for a session the desk never saw. The route behind `desk_add_line`, and `embarch-chat`'s Keep (`embarch-chat` decision 84) |
| `POST /mailbox` | `{"kind":"focus","session_id","folder"}` → `{"id"}`, or `{"kind":"open","folder"}` → `{"id","folder_uri"}`: the matching window starts an untracked chat with no prompt (70), and a second open before it is taken replaces the first. An entry expires after 10 min, as a launch claim does. **A `start` entry is written only by Start work, server-side** (46); `end` and `unfinished` only by the desk (83), and the route refuses all three |
| `GET /mailbox?folder=<absolute path>` | `{"entries":[…]}`, the pending entries for that folder. An `end` is `{id, kind, folder, item_id, issue_key, outcome: done\|canceled, created_ms, expires_ms, taken_ms}`; an `unfinished` adds `blockers: [{repo, reason}]`. Neither expires on the 10-minute clock (83); a window shows a folder while it polls for it, and the desk removes the folder once the polls have stopped for 180 s (84) |
| `POST /items/{id}/finish` | Re-runs the close-out checks for the item's issue (Done or Canceled) and posts a fresh `end` or `unfinished` for its folder; `{"ended":true}` or `{"ended":false,"blockers":[{repo,reason}]}`; 409 when the issue is open or has no folder here, 404 for no such item (83) |
| `GET /view`, per card; `work_item` of `GET /sessions/{sid}` | `close_out`: `{outcome: done\|canceled, blockers: [{repo, reason}], removal: {state: waiting\|removed\|left, why}\|null}` once the desk closed the issue out, else null; the Work tab's Finish button reads it (83), `removal` says what became of the folder (84) |
| `POST /mailbox/{id}/take` | The entry, once; `409` after |
| `POST /items/{id}/start` | With the chat setting on, leaves a `start` entry for the worktree and answers without the Claude Code prompt link (43) |
| `POST /items/{id}/repos` | `{"repo"}` → `{worktree, branch, how, warnings}`. On a suite desk, gives that clone a worktree on the card's branch, replacing its symlink in the issue's folder; `409` on a desk with no suite, before Start work, or for a name that is not a clone in the root (70) |
| `GET`/`PUT /settings` | `{"chat_panel": bool, "promptu": bool}`. `chat_panel`, **off by default**: Start work opens Claude Code's panel unless it is on (`embarch-chat` decision 4). `promptu`, **on by default**: with the chat setting off, Start work types `/promptu …` when Promptu is installed (67). A PUT changes only the fields it names |
| `GET /items/{id}/brief` | The pull (48): issue (title, state, description head, latest comments), PRs, sessions, notes (each memory note's newest state, the latest lines), bench — newest first, capped at 16,000 characters |
| `GET /items/{id}/notes` | Every note, newest first (53) |
| `GET /view`, per session | `state` (`busy`, `waiting`, `idle`, `ended`), `waiting_for`, `last_ms`, `cwd`, `client`; `folder_uri` and `session_uri`, on a card's rows and in `sessions` (71), and `folder_missing` (true when `cwd` is set but no longer a directory; `folder_uri` is then null); **a card keeps its ended `embarch-chat` sessions**, so Open chat can resume one (47) |
| `GET /view?desk=<id>` | The named desk's cards instead of the UI's desk's, for a window on another desk (`embarch-chat` decision 9); 404 for a desk that does not exist |
| `GET /view`, per card | `notes_ms`, **when the item's notes last changed** — a note held before its session had an item lands with its older time, so the newest note's own time would not move — and a client reads `/notes` only when it moves |
| `GET /refs`, `GET /refs?desk=<id or name>` | The desk's reference index (56), from memory: `{"desk_id","synced_ms","issues":[{"key","title","state","url"}],"prs":[{"repo","number","title","state","draft","url","branch","keys"}]}`. Issues newest update first, `state` Linear's own name; PRs by repo in the desk's order, newest first, `state` `open`, `closed` or `merged`, `keys` the issue keys of a known team in the title or branch. The UI's desk's without `?desk=`; with none selected, an empty index and `desk_id` null; 404 for a desk that does not exist. `synced_ms` is when a refresh last **changed** it, null before the first |
| `GET /view` | `refs_ms`: the viewed desk's `synced_ms`, and a client re-reads `/refs` only when it moves (56) |
| `POST /sync` | Also makes every desk's reference index due and wakes its task, without waiting on it (56) |
