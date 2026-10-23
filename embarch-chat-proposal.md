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

**Memory:** 457 MB resident for a full session with plugins and MCP servers, 242 MB stripped. **A background Bash task dies when its process exits.** Untested: image blocks in a user message.

## Decided so far (2026-10-22)

1. **It lives in a VS Code panel** — an extension of EmbArch's own, beside the code.
2. **It replaces the Claude Code panel for the owner's work.** VS Code stays for reading and editing code, and any chat can still open in Claude Code's panel.
3. **The first improvements that pull hardest:** it knows its **work item** (issue, comments, PRs, time) and starts briefed; it carries the owner's **prompt library** as one-click actions; **every thread at a glance**, waiting-on-you first; **bench-aware** — study output, flash results inline; and **atlas integration**.
4. **Tomorrow's workflow does not wait for it**: Start work opens the Claude Code panel (`embarch-desk` decision 43) until this exists.
5. **The extension runs each chat's `claude` process**, one per open chat, with the official panel's own flags; a closed chat comes back with `--resume`. Chats die with the VS Code window; the Desk sees them through `claude agents` and answers through Remote Control or Jump, as it does today (`embarch-desk` decision 44). **Rejected:** the desk service hosting the processes and relaying them to both the panel and the Desk tab — it buys answering in the browser and surviving a window reload for roughly 600–900 lines of Rust in a service whose job is work items and time; and a process per message (`claude -p --resume` each turn, nothing idle) — no idle memory, but every turn pays process and MCP-server startup, and a background task dies when its turn ends.
6. **`embarch-promptu` becomes `embarch-chat`**: one new repo holding the extension and the prompt library, the sub-project count unchanged. promptu's three planned pieces — the permission split, the `CLAUDE.md` fragment, the build→flash→log loop — become library entries. **Rejected:** inside `embarch-desk` (no new repo, and its spec already reserves a v2 chat panel, but firmware prompts would live in the time-tracking service's repo); growing `embarch-ui`'s launcher (one extension to sideload, but it reverses `embarch-ui` decision 3 and puts Claude sessions in the hardware UI's repo); a new `embarch-chat` beside promptu (two planned sub-projects for one concern). Decision 1 already sets aside `embarch-ui` decision 3's "no webview" for this extension; that decision still governs the launcher.
7. **A library entry is a Claude Code command or skill** — a `.md` file with frontmatter, in a plugin. The panel makes buttons of that plugin's own commands from the list `init` sends; the same files work in the terminal, the official panel and the fleet. A command gets its work item by calling `desk_whoami`, so nothing is templated. **Rejected:** panel-only templates with `{{issue}}`-style placeholders (richer filling, usable nowhere else), and a separate button file choosing which commands become buttons (a second file to keep in step, for a filtering the plugin boundary already does).
8. **Day one matches Claude Code's panel on: approve, stop, stream; diffs; @-file mentions.** Permission prompts, the Stop button, streamed text and the mode switch (plan, auto, accept edits) — all measured working above. An Edit or Write shows as a diff in the chat and opens VS Code's own diff editor on a click, built from the tool's input. Typing @ completes a workspace path, with the selected lines when there are some. **Later:** pasted images.

## Open

How chats are stored and named; which threads the list shows; how the panel talks to `embarch-desk`, and how a chat started here joins its card and time tile; where the library's files live (public repo or private); how the bench and the atlas show inline.
