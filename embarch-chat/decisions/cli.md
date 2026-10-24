# embarch-chat decisions: Answering the CLI

**Status:** active, 2026-10-23.

What the panel declares in `initialize`, how it answers the CLI's requests — permissions, plans, rules, dialogs, elicitations — and the controls it drives: background tasks, rewind and fork, MCP servers, effort, Remote Control.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 66 — The CLI's other requests get an answer

The chat's first line to the CLI is `initialize`, declaring the auto-mode fallback and refusal-fallback dialogs (without it the CLI never sends them); both are cards with Claude Code's words and buttons. An MCP elicitation, which the CLI sends any stdio permission client and then waits on with no timeout [measured: 20 s, no line], is a form or link card (Accept / Decline / × cancels). Any other request is refused at once with a timeline line, so none can hang a turn unseen. **Rejected:** dropping every subtype but `can_use_tool` (the old hang), Claude Code's decline-every-elicitation, a toast for the auto-mode wait (35 stands).

### 61 — An open file's unsaved changes are saved before Claude reads, edits or writes it

As Claude Code's own panel does: a PreToolUse hook declared in `initialize`, which the tool waits on for at most 5 s and which always answers continue, so a failed save never blocks it. `embarchChat.autosave`, machine scope, on. **Rejected:** saving every editor on send (touches files Claude never reads, misses edits made mid-turn).

### 65 — With `embarchChat.diagnosticsTool` on, Claude can call `getDiagnostics`

Machine scope, off by default — the owner's standing rule is that Claude ignores IDE diagnostics unless asked. An MCP server declared in `initialize` and spoken over the chat's own stdio: no process, port or lock file; about 150 tokens of tool definition per chat while on. **Rejected:** the IDE lock-file WebSocket server (every terminal `claude` in the folder would take the window as its IDE), a stdio server via `--mcp-config` (a process per chat with no access to VS Code's diagnostics).

### 64 — In ask mode a pending Edit or Write is taken change by change in its diff tab

CodeLens Reject per change, Accept/Reject in the title bar, and the permission is answered with only the kept changes. The CLI is not told a change was dropped — the permission answer has no field for it. **Rejected:** Claude Code's comment-thread bars (heavier for the same choice), a freely editable proposed side (can produce an Edit the CLI cannot apply).

### 77 — A plan's first answer is "Yes, and use auto mode"

The mode is set, then the plan allowed; a model that refuses auto gets accept-edits and a note [measured]. Then "manually approve edits" and "keep planning". "Open to comment" opens the plan as a read-only Markdown tab taking VS Code comments on its lines; with any comment the plan can only go back, the comments sent in Claude Code's words. **Rejected:** Claude Code's webview preview with text selection, an editable plan document, approving with comments attached.

### 78 — Always allow lists every suggestion the CLI made, and saves rules where the owner picks

Each one droppable, saved to the place the owner picks among Claude Code's four (project, all projects, local, session); the card starts at the owner's last pick, else the most lasting place the CLI named, and the host accepts nothing outside the four. A rule saved to a file is also given to the session: CLI 2.1.287 writes a project rule and still asks again in the session that saved it [measured]. **Rejected:** Claude Code's single button, which also applies a mode change it does not show [measured], remembering per workspace.

### 70 — A Bash call or a subagent running in the foreground offers "Run in background"

Under its row and on its folded run's header (50); it goes on as a background task and the turn continues, by `background_tasks` with its tool_use_id as Claude Code's panel asks. The CLI never registers an MCP call as a foreground task, so an `embarch-api` flash cannot move [measured]. **Rejected:** Stop as the only choice, a button on every running step.

### 71 — The status line opens the background tasks

Each shell, Monitor or subagent with its output tail (read every second while it runs) or its progress, and a Stop that ends only it; Stop on the turn ends only the turn [measured]. 41 is unchanged. **Rejected:** a count with no output or Stop, a full agent map with transcripts.

### 73 — Rewind and fork from any of the owner's messages, as Claude Code's panel does it

8's "later" half. A ↶ on each message, `/rewind` and Esc twice offer: fork the conversation into a new chat on the same item (the CLI's own `--resume --fork-session --resume-session-at`, the message back in the draft, named "<name> (fork)", assigned through the existing desk route), rewind the files Claude changed (`rewind_files`, which needs every chat started with `CLAUDE_CODE_ENABLE_SDK_FILE_CHECKPOINTING=true`; its dry run shown, done only on the owner's click, never mid-turn), or both [measured]. **Rejected:** the CLI's in-place `rewind_conversation`, writing the fork's transcript ourselves, a file rewind without confirmation, a desk route for forks.

### 81 — The MCP pill is Claude Code's `/mcp`

Each server with its state and error, and Reconnect, Disable and Enable for this chat's process; `/mcp` opens it. Reconnect starts the server again [measured: new pid], so a rebuilt `embarch-api` binary is picked up without ending the chat. The window's own server (65) lists with no actions — the CLI refuses to reconnect it. **Rejected:** ending the chat to pick up a rebuild, the CLI's text `/mcp`.

### 82 — Effort is per chat, in Claude Code's model pill

The levels the model takes, and the Ultracode switch where the CLI offers it. It is the chat's own flag settings, sent whole [measured: the CLI replaces the layer, it does not merge] and carried into a resumed process by `--settings`; never written to the owner's settings. **Rejected:** Claude Code's save to user settings.

### 83 — `/remote-control` bridges a chat to claude.ai/code

A footer pill shows connecting, on (opens the session) or failed until dismissed, and while it is on the process outlives the idle close (41) [measured: link in 0.25 s, works before the first message, prompts still asked in the panel; the phone side not yet seen]. **Rejected:** an always-shown pill, closing the process under a live bridge.
