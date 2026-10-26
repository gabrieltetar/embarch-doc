# 001 — A message the CLI sends Claude is never an owner bubble

**State:** claimed by agent/chat/001-cli-turns-are-not-the-owners, 2026-10-25 23:14
**Source:** owner, 2026-10-25 — a background agent's `<task-notification>` showed in a chat as a raw-XML message the owner appeared to have sent; wire shape recorded the same day on CLI 2.1.287
**Scope:** chat
**Hardware:** none
**Owner:** no

## Dispatch note, 2026-10-25 leg

The fleet's first `chat` unit, so the worktree setup is new: `.worktrees/embarch-chat/` holds a
symlink `embarch-doc` → the main `embarch-doc` checkout, so the `../embarch-doc/scripts/...`
paths in this repo's `CLAUDE.md` resolve from your code worktree. Run `npm ci` there first; a
fresh worktree has no `node_modules`. No `embarch-chat` doc is in its size reserve. This task
lands **before** `tasks/chat/002` (both edit `foldUser`); 002 is not dispatched this leg.
If `check-docs.py` is red only on `embarch-study-designer/open.md`, that is pre-existing on `main`
and being paid by `study-designer/026` in parallel — not yours; everything else must be green.

## What

A `user` line whose `origin.kind` is anything but `"human"` never becomes a user entry. Today `foldUser` (`src/wire/reducer.ts`) drops only `isSynthetic`, `isMeta`, a compaction summary and a subagent's lines, so this one gets through: when a background task ends while a turn is still running tools, the CLI replays its notification as `type: "user"`, `isReplay: true`, `origin: {kind: "task-notification", producer: "session-task"}`, with content a `<task-notification>` XML string (`task-id`, `tool-use-id`, `output-file`, `status`, `summary`, `note`, `result`) and no `isMeta`. Instead:

- **`task-notification`** becomes a one-line row where Claude took it, worded like the CLI's own line: `Agent "<summary>" completed` (or `failed`, `stopped`), and a shell task's summary as it comes. The row links to its tool card by `<tool-use-id>`; a click scrolls to the card and opens it. The card already flips to completed from the `system` `task_notification` event (`task_notification` case in `foldSystem`), so the row says when Claude saw it and the card holds the detail.
- **A turn the CLI starts on its own** gets the same row ahead of the reply. This happens when a task ends while Claude is idle: `system` `task_notification`, then `init` and an assistant reply, with no user line between. A reply never appears with nothing above it.
- **`peer` without `handback`** (another session's message, content `Another Claude session sent a message:` followed by `<agent-message from=…>`), where it reaches the panel, becomes a collapsed `Message from <name>` row that expands to the text. A hand-back (`origin.handback: true`) is `chat-agent-card-shows-the-hand-back`'s.
- **One predicate**, shared with `humanPrompt` in `src/assistant/history.ts`, which already applies this rule to the assistant's prefix match. Not a second copy. A line with no `origin` falls back to `turnOrigin` as `humanPrompt` does.
- **Such a line is never the owner's.** It is never matched to a pending message by the `mine` lookup, never editable, and never a rewind point.
- **On reload**, the transcript records a notification taken mid-turn as `type: "attachment"`, `attachment.type: "queued_command"`, with the XML in `attachment.prompt`. That is ignored today; the same row comes back from it.

## Why now

The owner asked for it on 2026-10-25, after a real session showed the notification as a bubble he had not sent. That notification also pointed to a report the panel never showed, which is the other task. This is the fleet's first `chat` task: the repo got its remote (`gabrieltetar/embarch-chat`) the same day for exactly this.

## Done when

- [ ] Two scenarios in `test/record.mjs`, recorded in a scratch folder with neutral prompts and run through `sanitize.mjs`:
  - **Mid-turn:** a background Agent ends while the turn still runs a foreground tool, which produces the replay line.
  - **Idle:** it ends after the turn's `result`, which produces the self-started turn.
  - **What worked on 2026-10-25:** Haiku, `--tools Agent,Bash`, the prompt `Use the Agent tool with run_in_background: true (subagent_type general-purpose) to have a subagent reply with exactly the word PING`, then a foreground tool. A standalone `sleep 45` is refused by the CLI, so use a ticking loop like the `sendnow` scenario's.
- [ ] Wire test on the mid-turn fixture: one row linked to the Agent card, and no user entry.
- [ ] Wire test on the idle fixture: a row ahead of the reply.
- [ ] Reducer test: a `peer` line without `handback` gives a collapsed message row. An `origin.kind: "human"` line, and one with no `origin`, still give a user entry, so the owner's own messages do not regress.
- [ ] Reload test: a `queued_command` attachment gives the same row.
- [ ] Webview e2e (`npm run test:webview`): the row renders, there is no bubble, and a click opens the card.
- [ ] Gate green (`../../embarch-fleet/gate.md`, which has an npm bullet since 2026-10-25; this repo has no `cargo`):
  - `npm ci` in the worktree, then `npm run build`, `npm run typecheck`, `npm test` and `npm run test:webview`.
  - `python3 ../embarch-doc/scripts/check-client-names.py --repo .`
  - `check-docs.py`
  - `check-ownership.py --scope chat`
  - The desk tests skip without `EMBARCH_DESK_BIN`, and that is fine here.
- [ ] Decision in `embarch-chat/decisions/timeline.md`, `spec.md` updated, `changelog.d/` fragment with scope `chat`.
