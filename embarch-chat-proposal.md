# Proposal: the owner's own Claude chat, in VS Code

**Status:** draft, 2026-10-22. Shaping notes; becomes a proposal once its open questions are answered. Takes over [`embarch-promptu`](embarch-promptu/design.md)'s place in the suite (decision 6).

## The ask

A Claude Code chat of the owner's own — "its own Claude Code chat basically, with improvements tailored to my needs" — so that the Desk can start, show and answer sessions itself instead of handing off to claude.ai (`embarch-desk` decision 44).

## What is possible (measured 2026-10-22)

**One EmbArch-owned process held a real multi-turn Claude Code conversation on the owner's own login**: `claude -p --input-format stream-json --output-format stream-json`, two user messages fed in over time, one session id throughout, the second answer remembering the first; $0.004 on Haiku with a stripped context. The official SDK expects an API key, so this rides the `claude` CLI.

**The official Claude Code panel is itself a client of that same wire.** Its process on this machine runs `claude --input-format stream-json --output-format stream-json --verbose --permission-prompt-tool=stdio --resume=<id> --setting-sources=user,project,local --permission-mode=auto --replay-user-messages`, one process per open chat. The wire is only partly documented, but it is the one Anthropic's own panel depends on — a change to it breaks theirs too.

**Over it, measured on Haiku for about $0.05 in all:**

| Need | How, on the wire | Result |
|---|---|---|
| Permission prompt | `control_request` `can_use_tool` out (tool, input, description, suggestions, tool use id); `control_response` `allow`/`deny` in | Bash ran after the allow |
| Stop | `control_request` `interrupt` in | Turn ended at once with `[Request interrupted by user]`; the next message was answered |
| Streaming text | `--include-partial-messages` | `stream_event` deltas |
| Close and reopen | process exits; `--resume <id>` later | Same session id, context remembered |
| Mode switch | `control_request` `set_permission_mode` | `plan` set mid-session |
| Name | `control_request` `rename_session`, or `--name` at start | Stored as a `custom-title` line in Claude's own transcript |
| Slash commands | user text `/greet Gabriel` | A project command expanded; `system/init` lists every command the session has |
| Pre-chosen id | `--session-id <uuid>` | The id is known before the process starts |
| Desk visibility | `claude agents --json` | The chat is listed, `kind: interactive` |
| Claude's questions | `can_use_tool` for `AskUserQuestion`, questions and options in its input; `allow` with `answers` added | Claude read the picked option back |

**Memory:** 457 MB resident for a full session with plugins and MCP servers, 242 MB stripped. **A background Bash task dies when its process exits.** Untested: image blocks in a user message.

## Decided so far (2026-10-22)

1. **It lives in a VS Code panel** — an extension of EmbArch's own, beside the code.
2. **It replaces the Claude Code panel for the owner's work.** VS Code stays for reading and editing code, and any chat can still open in Claude Code's panel.
3. **The first improvements that pull hardest:** it knows its **work item** (issue, comments, PRs, time) and starts briefed; it carries the owner's **prompt library** as one-click actions; **every thread at a glance**, waiting-on-you first; **bench-aware** — study output, flash results inline; and **atlas integration**.
4. **Tomorrow's workflow does not wait for it**: Start work opens the Claude Code panel (`embarch-desk` decision 43) until this exists.
5. **The extension runs each chat's `claude` process**, one per open chat, with the official panel's own flags; a closed chat comes back with `--resume`. Chats die with the VS Code window; the Desk sees them through `claude agents` and answers through Remote Control or Jump, as it does today (`embarch-desk` decision 44). **Rejected:** the desk service hosting the processes and relaying them to both the panel and the Desk tab — it buys answering in the browser and surviving a window reload for roughly 600–900 lines of Rust in a service whose job is work items and time; and a process per message (`claude -p --resume` each turn, nothing idle) — no idle memory, but every turn pays process and MCP-server startup, and a background task dies when its turn ends.
6. **`embarch-promptu` becomes `embarch-chat`**: one new repo holding the extension and the prompt library, the sub-project count unchanged. promptu's three planned pieces — the permission split, the `CLAUDE.md` fragment, the build→flash→log loop — become library entries. **Rejected:** inside `embarch-desk` (no new repo, and its spec already reserves a v2 chat panel, but firmware prompts would live in the time-tracking service's repo); growing `embarch-ui`'s launcher (one extension to sideload, but it reverses `embarch-ui` decision 3 and puts Claude sessions in the hardware UI's repo); a new `embarch-chat` beside promptu (two planned sub-projects for one concern). Decision 1 already sets aside `embarch-ui` decision 3's "no webview" for this extension; that decision still governs the launcher.
7. **A library entry is a Claude Code command or skill** — a `.md` file with frontmatter, in a plugin. The panel makes buttons of that plugin's own commands from the list `init` sends; the same files work in the terminal, the official panel and the fleet. A command gets its work item by calling `desk_whoami`, so nothing is templated. **Rejected:** panel-only templates with `{{issue}}`-style placeholders (richer filling, usable nowhere else), and a separate button file choosing which commands become buttons (a second file to keep in step, for a filtering the plugin boundary already does).
8. **Day one matches Claude Code's panel on: approve, stop, stream; diffs; @-file mentions.** Permission prompts, the Stop button, streamed text and the mode switch (plan, auto, accept edits) — all measured working above. An Edit or Write shows as a diff in the chat and opens VS Code's own diff editor on a click, built from the tool's input. Typing @ completes a workspace path, with the selected lines when there are some. **Claude's own questions are part of "approve"**: on the wire an `AskUserQuestion` is a permission request (measured above), so the panel draws it as a form with its options and previews; a plan's approval is assumed to arrive the same way, as `ExitPlanMode` [untested]. **Later:** pasted images.
9. **The list shows the open desk's threads, grouped by work item, waiting-on-you first**: every live session in the open desk's repos from `claude agents --json` (0.2 s a call), terminal and Claude Code-panel sessions included, plus the desk's past chats, with an Untracked group last. The fleet stays out through the desk's ignore list. **Rejected:** only the panel's own chats (a terminal session would be invisible), and every live session on the machine in one flat list (the fleet's dozens drown the owner's few).
10. **A chat is on its work item before it starts.** The + on a work item's group starts on that item; the top + opens a picker — the open desk's cards, an issue key, a new title, or untracked. The extension chooses the session id, puts it on the item through the desk's existing `POST /sessions/{sid}/assign` (which creates a session the desk has not seen), then starts `claude --session-id <id>`. **The desk never has to ask, and needs no change.** **Rejected:** binding nothing and letting the hooks ask on every prompt (`embarch-desk` decision 7) — a question the panel can already answer.
11. **The Desk's Start work opens a chat here and sends the prompt.** It follows a `vscode://` link to this extension, which opens a chat on the card's item and sends the read-and-summarize prompt itself — **decision 43's Enter press goes away**, because the extension is what sends the message. **Rejected:** the prompt typed in and waiting for Enter (kept only because nothing could send into Claude Code's panel), and an empty chat on the item.
12. **Nothing new is stored.** The transcript is Claude's own; the desk already maps session to work item; the name is set with `--name` as `ABC-123 · <first line of the first prompt>` and lands as Claude's own title, so the official panel's history and `claude --resume` show the same name. **Rejected:** an index of the extension's own (pins and archive, but a third record to keep in step) and chat records in the desk (a desk change for the same).

13. **The library is two folders: a public plugin and the owner's own commands.** Generic entries ship as a plugin in the public `embarch-chat` repo; **an entry naming a client, a client project or a client internal lives in `~/.claude/commands` and never in a repo**. The panel reads both and makes buttons of both — **amending decision 7**, which said only the plugin's own. **Rejected:** the public plugin only (client-specific prompts typed by hand forever), and the open firmware repo's `.claude/commands` as well (a client team's commands are theirs, not the owner's library).
14. **The library is seeded from the owner's own past prompts, and the owner cuts.** 682 prompts in 145 local transcripts [measured 2026-10-22]; the only exact repeats are one-word replies (done ×20, continue ×15, yes ×12, go ×11, push ×7), so one `claude -p` groups them by intent and drafts candidate entries, each one ✓ or ✕ — over-generate, then cut. About $0.30 on Sonnet [assumed]. Each kept entry lands in the public plugin or the private folder per decision 13. **Rejected:** promptu's three pieces then add-as-you-go (they become entries anyway, decision 6), and starting empty.
15. **Bench results show as cards.** A build, flash, bootload, study or `serial_log` result from `embarch-api` becomes a compact card — pass or fail, board, first error, steps passed, a link into `embarch-ui` — drawn from the tool result already in the stream. **Rejected:** a live bench strip at the top of the panel polled from Core (a second view of what `embarch-ui` already shows), and plain tool output.
16. **Atlas citations become links.** The `atlas-use` skill already cites every hardware fact as `<doc_id> p<N>` or `<board>:<ref>`; the panel makes each a link to that page or to the entry in `embarch-ui`'s Atlas tab. Rendering only. **Rejected:** a hardware pane showing the atlas card for the file being edited (a second surface to keep in step with the Atlas tab), and plain text.

## Open

How the panel talks to `embarch-desk`; where the panel sits in VS Code; what a chat's header shows of its work item; quick replies.
