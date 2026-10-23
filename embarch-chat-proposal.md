# Proposal: the owner's own Claude chat, in VS Code

**Status:** draft, 2026-10-22. Shaping notes; becomes a proposal once its open questions are answered. Takes over [`embarch-promptu`](embarch-promptu/design.md)'s place in the suite (decision 6).

## The ask

A Claude Code chat of the owner's own — "its own Claude Code chat basically, with improvements tailored to my needs" — so that the Desk can start, show and answer sessions itself instead of handing off to claude.ai (`embarch-desk` decision 44).

## What is possible (measured 2026-10-22)

**An EmbArch-owned process can hold a multi-turn Claude Code session on the owner's own login, over the wire the official Claude Code panel itself uses.** That panel's process here runs `claude --input-format stream-json --output-format stream-json --verbose --permission-prompt-tool=stdio --resume=<id> --setting-sources=user,project,local --permission-mode=auto --replay-user-messages`, one per open chat. The wire is only partly documented, but Anthropic's own panel depends on it. The official SDK expects an API key, so this rides the `claude` CLI. Measured over it on Haiku, about $0.06 in all:

| Need | On the wire | Result |
|---|---|---|
| Permission prompt | `can_use_tool` control request out; `allow`/`deny` control response in | Bash ran after the allow |
| Claude's question | the same, for `AskUserQuestion`; `allow` with `answers` added | Claude read the pick back |
| Stop | `interrupt` control request | Turn ended at once; the next message was answered |
| Streaming | `--include-partial-messages` | `stream_event` deltas |
| Reopen | `--resume <id>` after the process exits | Context remembered |
| Mode, name | `set_permission_mode`; `rename_session` or `--name` | `plan` mid-session; a `custom-title` line in Claude's transcript |
| Commands | user text `/greet world` | Expanded; `system/init` lists every command |
| Pre-chosen id | `--session-id <uuid>` | Known before the process starts |
| Desk visibility | `claude agents --json`, 0.2 s | Listed, `kind: interactive` |
| Next-prompt guess | `--prompt-suggestions` | A `prompt_suggestion` after the turn ("go ahead") |

**Memory:** 457 MB resident for a full session, 242 MB stripped; a background Bash task dies with its process. **Haiku thinks by default here**, 5–9 s for a one-line completion; with `--max-thinking-tokens 0` a stripped one-shot `claude -p` takes 1.2 s of API time, 1.85 s wall, $0.0016. Untested: image blocks.

## Decided (2026-10-22)

1. **It lives in a VS Code panel** — an extension of EmbArch's own, beside the code.
2. **It replaces the Claude Code panel for the owner's work.** VS Code stays for reading and editing code, and any chat can still open in Claude Code's panel.
3. **The first improvements that pull hardest:** it knows its **work item** (issue, comments, PRs, time) and starts briefed; it carries the owner's **prompt library** as one-click actions; **every thread at a glance**, waiting-on-you first; **bench-aware**; **atlas integration**.
4. **Tomorrow's workflow does not wait for it**: Start work opens the Claude Code panel (`embarch-desk` decision 43) until this exists.
5. **The extension runs each chat's `claude` process**, one per open chat, with the official panel's flags; a closed chat comes back with `--resume`. Chats die with the window; the Desk sees them through `claude agents` and answers through Remote Control or Jump, as today (`embarch-desk` decision 44). **Rejected:** the desk service hosting them (answering in the browser and surviving a reload, for roughly 600–900 lines of Rust in a work-item service), and a process per message (no idle memory, but startup every turn and background tasks killed at its end).
6. **`embarch-promptu` becomes `embarch-chat`**: one new repo for the extension and the library, the sub-project count unchanged; promptu's three planned pieces (the permission split, the `CLAUDE.md` fragment, the build→flash→log loop) become library entries. Decision 1 sets `embarch-ui` decision 3's "no webview" aside for this extension only. **Rejected:** inside `embarch-desk` (no new repo, but firmware prompts in the time-tracking service's repo), growing `embarch-ui`'s launcher (Claude sessions in the hardware UI's repo), and a new sub-project beside promptu (two for one concern).
7. **A library entry is a Claude Code command or skill**, a `.md` file with frontmatter: the same file works in the terminal, the official panel and the fleet, and gets its work item from `desk_whoami`, so nothing is templated. **Rejected:** panel-only templates with `{{issue}}` placeholders (usable nowhere else), and a button file choosing which commands show (a second file to keep in step).
8. **Day one matches Claude Code's panel on approve, stop and stream; diffs; @-file mentions.** Permission prompts, Stop, streamed text, the mode switch (plan, auto, accept edits). **Claude's own questions count as approve** — on the wire they are permission requests — so they show as forms with their options and previews; a plan's approval is assumed to arrive the same way, as `ExitPlanMode` [untested]. An Edit or Write shows as a diff and opens VS Code's diff editor on a click. @ completes a workspace path, with the selected lines. **Later:** pasted images.
9. **The thread list is the open desk's threads, by work item, waiting-on-you first**: every live session in the desk's repos from `claude agents` — terminal and Claude Code-panel ones too — plus the desk's past chats, Untracked last; the fleet stays out through the desk's ignore list. **Rejected:** only the panel's own chats, and every session on the machine (the fleet's dozens drown the owner's few).
10. **A chat is on its work item before it starts.** The + on a group starts on that item; the top + picks one (a card, an issue key, a new title, untracked). The extension chooses the session id, assigns it with the desk's existing `POST /sessions/{sid}/assign` (which creates a session the desk has not seen) and starts `claude --session-id`: the desk never asks and needs no change. **Rejected:** letting the hooks ask on every prompt (`embarch-desk` decision 7).
11. **Start work on the Desk opens a chat here and sends the prompt**, through a `vscode://` link the extension handles — **`embarch-desk` decision 43's Enter press goes away**. **Rejected:** the prompt typed in and waiting, and an empty chat.
12. **Nothing new is stored.** The transcript is Claude's; session → item is the desk's; the name, set with `--name` as `ABC-123 · <first line of the first prompt>`, is Claude's own title, so the official panel's history and `claude --resume` agree. **Rejected:** an index of the extension's own, and chat records in the desk.
13. **The library is two folders**: generic entries in a plugin in the public `embarch-chat` repo; **an entry naming a client, a client project or a client internal in `~/.claude/commands`, never in a repo**. Both become buttons, amending decision 7's "the plugin's own". **Rejected:** the public plugin only, and the open firmware repo's commands too (the client team's, not the owner's).
14. **The library is seeded from the owner's past prompts, and the owner cuts.** 682 prompts in 145 local transcripts [measured]; the only exact repeats are one-word replies (done ×20, continue ×15, yes ×12, go ×11, push ×7), so one `claude -p` groups them by intent and drafts entries, each ✓ or ✕; about $0.30 on Sonnet [assumed]. **Rejected:** promptu's three then add-as-you-go, and starting empty.
15. **Bench results show as cards**: a build, flash, bootload, study or `serial_log` result from `embarch-api` becomes pass or fail, board, first error, steps passed and a link into `embarch-ui`, drawn from the tool result already in the stream. **Rejected:** a live bench strip polled from Core (a second `embarch-ui`), and plain output.
16. **Atlas citations become links**: `atlas-use` cites every hardware fact as `<doc_id> p<N>` or `<board>:<ref>`, and each opens that page or the entry in `embarch-ui`'s Atlas tab. **Rejected:** a hardware pane for the open file (a second Atlas tab), and plain text.
17. **The list sits left, the chat right**: the list behind its own activity-bar icon, the chat in the secondary sidebar where Claude Code's panel is (its `package.json` contributes there), any chat also openable as an editor tab. **Rejected:** both stacked on the right (the list folds away), and every chat a tab (chats compete with code).
18. **A chat's header is its card in two lines**: key, title, status dropdown, PRs with their state, today's time, a link to the Desk card. **Rejected:** key and title alone, and the full card folded in.
19. **Quick replies follow the moment** — the owner's most-sent messages are one word (14) — **and the Haiku assistant drafts them** (24–27). **Rejected:** a fixed row of chips; none; the CLI's `--prompt-suggestions` guess alone or with two hand rules (one guess, blind to the draft); a hand-written table of situations.
20. **The extension's Node side calls the desk directly** on `127.0.0.1:4891` with the token file; **the webview never holds the token** (`embarch-desk` decision 28 — a webview is a page). The list polls `claude agents` and `GET /view` every 3 s while visible; the panel's own chats update from their streams. **Rejected:** `embarch-ui`'s proxy (no work items while the UI is down), and an SSE route in the desk (a desk change to save 3 s).
21. **The webview is Preact bundled with esbuild**, in VS Code's theme variables: one event stream feeding a constantly changing UI renders better from state than by hand-patched DOM. About 4 KB. **Rejected:** plain DOM (`embarch-ui` decision 2's posture), and React (about 140 KB).
22. **A new chat starts in auto mode on the owner's default model**, as the official panel does here and Start work's worktrees do (`embarch-desk` decision 43); both switch per chat. **Rejected:** ask mode, and a mode and model per desk.
23. **It ships whole**, one build of every decision, as the desk's v1 did (`embarch-desk` decision 21). **Rejected:** the library first (usable in Claude Code's panel at once) and the panel first.

### The Haiku assistant

24. **While the owner writes, Haiku offers ghost text and cards.** The completion shows in grey and Tab takes it; **cards above the input suggest or warn about the prompt**. **Rejected:** a one-line note under the box (became the cards), and a tighten-the-draft button.
25. **When Claude's turn ends, it drafts two to four replies as chips**, the CLI's own guess among them. **Rejected:** a checklist of what Claude asked, ticked as the draft answers it, and a one-line digest of the reply in the thread list.
26. **It runs on a pause**: 700 ms after typing stops, and after each turn; the next keystroke cancels a stale call. Each is one stripped `claude -p` with thinking off, returning whatever applies — completion, cards, chips — in about 1.9 s for $0.002–0.004, so $1–2 a day at ~500 calls [estimate]. It runs under `EMBARCH_DESK_INTERNAL=1`, so the desk ignores it. **Rejected:** after turns only, and only on a key.
27. **It sees the draft, Claude's last reply, the work item's card and the library's entry names** — 1–3K tokens. **Rejected:** the whole transcript (tens of thousands of tokens a call, about 10× the cost), and the draft and last reply only.

## Open

Which cards may appear above the input; whether `embarch-ui`'s launcher stays a separate extension or moves into `embarch-chat`'s.
