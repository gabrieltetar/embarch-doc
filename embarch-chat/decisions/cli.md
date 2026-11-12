# embarch-chat decisions: Answering the CLI

**Status:** active, 2026-11-01.

What the panel declares in `initialize`, how it answers the CLI's requests — permissions, plans, rules, dialogs, elicitations — and the controls it drives: background tasks, rewind and fork, MCP servers, effort, Remote Control, and the short claude that answers before a chat's own.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 66 — The CLI's other requests get an answer

The chat's first line to the CLI is `initialize`, declaring the auto-mode fallback and refusal-fallback dialogs (without it the CLI never sends them); both are cards with Claude Code's words and buttons. An MCP elicitation, which the CLI sends any stdio permission client and then waits on with no timeout [measured: 20 s, no line], is a form or link card (Accept / Decline / × cancels). Any other request is refused at once with a timeline line, so none can hang a turn unseen. **Rejected:** dropping every subtype but `can_use_tool` (the old hang), Claude Code's decline-every-elicitation, a toast for the auto-mode wait (35 stands).

### 61 — An open file's unsaved changes are saved before Claude reads, edits or writes it

As Claude Code's own panel does: a PreToolUse hook declared in `initialize`, which the tool waits on for at most 5 s and which always answers continue, so a failed save never blocks it. It saves only a document under the chat's folder or a workspace folder: the hook runs before the permission check, so a Read the owner refuses must not save a file elsewhere. `embarchChat.autosave`, machine scope, on. **Rejected:** saving every editor on send (touches files Claude never reads, misses edits made mid-turn).

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

8's "later" half. A ↶ on each message, `/rewind` and Esc twice offer: fork the conversation into a new chat on the same item (the CLI's own `--resume --fork-session --resume-session-at`, the message back in the draft, named "<name> (fork)", assigned through the existing desk route), rewind the files Claude changed (`rewind_files`, which needs every chat started with `CLAUDE_CODE_ENABLE_SDK_FILE_CHECKPOINTING=true`; its dry run shown, done only on the owner's click, never mid-turn or while a background task runs; at Rewind a fresh dry run is compared with the one shown, and a different list is shown again rather than acted on), or both [measured]. The host takes a rewind or fork only for an owner message of the chat it serves. **Rejected:** the CLI's in-place `rewind_conversation`, writing the fork's transcript ourselves, a file rewind without confirmation, a desk route for forks.

### 81 — The settings menu's MCP is Claude Code's `/mcp`

A section of the settings menu (107; a pill left of the box until EMB-164). Each server with its state and error, and Reconnect, Disable and Enable for this chat's process; `/mcp` opens it. Reconnect starts the server again [measured: new pid], so a rebuilt `embarch-api` binary is picked up without ending the chat. The window's own server (65) lists with no actions — the CLI refuses to reconnect it. **Rejected:** ending the chat to pick up a rebuild, the CLI's text `/mcp`.

### 82 — Effort is per chat, beside the model, as in Claude Code's model pill

The levels the model takes, and the Ultracode switch where the CLI offers it, under the model in the settings menu (107). It is the chat's own flag settings, sent whole [measured: the CLI replaces the layer, it does not merge] and carried into a resumed process by `--settings`; never written to the owner's settings. **Rejected:** Claude Code's save to user settings.

### 83 — `/remote-control` bridges a chat to claude.ai/code

The settings menu's switch (107) shows connecting, on (with the session's link) or failed until dismissed, and while it is on the process outlives the idle close (41) [measured: link in 0.25 s, works before the first message, prompts still asked in the panel; on the phone 2026-11-11, by the owner]. A bridge the panel starts at startup for Claude Code's `remoteControlAtStartup` (100) shows the same, and Claude Code's disclosure once, as a note, when its default rather than the owner's setting turned it on; it holds the process only while the chat is open. **Rejected:** an always-shown pill, closing the process under a live bridge.

### 100 — The panel bridges each chat at startup, and an open chat keeps it, so the phone reaches it

With `remoteControlAtStartup` on, the panel bridges each chat's process to claude.ai/code as it starts, as Claude Code's own panel does: when `initialize` answers `remote_control_auto_enable` true and `remote_control_available` not false, and either `remote_control_auto_on_by_default` false (the owner's setting) or `ide_rc_auto_enable_gate` true, it sends `remote_control` itself. **The CLI starts no bridge for a host** [measured 2026-11-11 on 2.1.287 and 2.1.322: no `bridge_state` at startup or after a message]; the panel first waited for one, and no chat reached the phone ([reversals](../../embarch-decision-reversals.md) row 117, EMB-162). The bridge holds the process while the chat is open — a tab, shown or not, or with `chatLocation` = `sidebar` the sidebar's chat — and a chat whose tab closes goes at its idle close (41) as before, checked again within 30 s. Asked for by the owner on 2026-11-01, to reach his open chats from Claude Code on his phone. About 300 MB a held process [measured: 294 and 341 MB]. A bridge the owner turns off stays off for the chat's later processes, and one turned on starts again with them; before the first message the menu's switch sets it for the chat (108). A chat whose process already closed, or one brought back by a reload (63), is reachable again only after its next message [measured 2026-11-11: connected 1.6 s after the first message]. **Rejected:** a longer `idleMinutes` (holds every chat, open or not), holding every bridged chat (83's reason: a closed chat would keep its process for good), Claude Code's server mode `claude remote-control` (its sessions are not chats: no work item, not in the panel).

### 108 — One short claude per login and folder fills a chat's settings before its first message

A chat's process starts on its first message (41), so until then its effort levels, its MCP servers and whether Remote Control starts with it were unknown. The host starts one `claude` with the panel's flags per login and folder as the window starts, and again for a chat created over a minute after the last answer; it sends `initialize`, then `mcp_status` each second while a server is connecting (at most 15 s), and closes it. **It is sent no message: no tokens, no transcript, no bridge** [measured 2026-11-11]. `--settings` `disableAllHooks` and `EMBARCH_DESK_INTERNAL` keep the owner's hooks and the desk out, and a due login waits on its warm-up (105). The models and Remote Control come at once, the servers after [measured 2026-11-12 on the owner's login: 0.6 s and 2.6 s, 16 models, 21 servers]. A chat this window runs takes the answers until its own process's `initialize` replaces them. Before the first message, the Remote Control switch (107) changes only what the start does: off, the chat bridges nothing; on, it bridges though Claude Code's setting would not (100). `embarchChat.startupProbe` turns the probe off. **Rejected:** starting the chat's own process when it opens (300–450 MB a chat, and an empty session on the phone for each); the last chat's answers alone (a fresh window shows nothing).
