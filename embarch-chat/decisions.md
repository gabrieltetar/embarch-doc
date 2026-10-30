# embarch-chat: decisions

**Status:** active, 2026-10-30.

Why the chat is shaped this way. Current truth: [spec.md](spec.md). Unresolved: [open.md](open.md). Reference: [interfaces.md](interfaces.md).

Decision numbers are permanent and address this sub-project, not a file. Cite them as `embarch-chat decision N`. 1–49 were shaped with the owner in rounds of questions from 2026-10-22 and carried in three proposals at this repo's root until the fold of 2026-10-23; 50–85 were settled porting Claude Code's own panel the same day; 86–89 on 2026-10-25, with `embarch-desk` decision 56 and `embarch-ui` decision 58. 90–93 on 2026-10-26; 94–98, with 11 reversed and 28 retired, on 2026-10-30, for `embarch-promptu`'s build step 3. The code cites them by number.

| Group | Decisions | What it settles |
|---|---|---|
| [decisions/shape.md](decisions/shape.md) | 1, 2, 3, 4, 6, 23, 29, 17, 92, 21, 52, 53, 91, 94, 54 | A VS Code panel replacing Claude Code's, what `embarch-promptu` became until the owner revived it, the launcher moved in, shipped whole; the layout, a chat as a tab, Preact, the typeface, the palette, the column, the rail, the mark |
| [decisions/sessions.md](decisions/sessions.md) | 5, 31, 35, 80, 41, 30, 22, 12, 75, 48, 63 | One `claude` per chat owned by its window, foreign threads read-only, waiting and unread, the idle close, which `claude`, nothing new stored, names, what a workspace cannot change, what a reload restores |
| [decisions/desk.md](decisions/desk.md) | 9, 10, 11, 18, 20, 84; 32, 33, 40, 42–47, 49 moved | The window's desk's threads, a chat on its item before it starts, Start work into a chat and its Promptu pass, the header, reaching the desk, Keep; the desk's side, now `embarch-desk` decisions 46–55 |
| [decisions/timeline.md](decisions/timeline.md) | 8, 50, 87, 51, 89, 90, 76, 79, 62, 93 | Day-one parity, steps and folded runs, what a step touched as a link, turns, what the CLI sends Claude as a row, a background agent's report, compactions, answered questions, tool output in a tab, file links |
| [decisions/readouts.md](decisions/readouts.md) | 68, 69, 67, 74, 85, 15, 16 | Time, the cache line, the usage banner, copy and export, long chats, bench cards, atlas links |
| [decisions/input.md](decisions/input.md) | 55, 56, 57, 58, 59, 86, 60, 72 | Cards while typing, pastes and images, `/btw`, a terminal's output, the keys, a preview that never moves the menu and the menus by keyboard, the selection, a message sent mid-turn |
| [decisions/cli.md](decisions/cli.md) | 66, 61, 65, 64, 77, 78, 70, 71, 73, 81, 82, 83 | `initialize` and the CLI's requests, autosave, diagnostics, per-change diffs, plans, Always allow, background tasks, rewind and fork, MCP, effort, Remote Control |
| [decisions/library.md](decisions/library.md) | 7, 13, 14, 38, 39 | An entry is a command or skill, two folders, seeded from past prompts, the 📚 and 💡, promptu's install pieces |
| [decisions/assistant.md](decisions/assistant.md) | 19, 24, 28 (retired), 36, 97, 37, 88, 25, 26, 34, 27 | Haiku's quick replies, ghost text and cards, what it left to Promptu, the desk's reference index in cards and prose, three waves, the chat on screen only, what it sees |
| [decisions/promptu.md](decisions/promptu.md) | 95, 96, 98 | `embarch-promptu` in the chat: the icon and its card, the pass and its dialog at a task start and on Start work, the Memory menu |
