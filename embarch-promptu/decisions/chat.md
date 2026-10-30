# embarch-promptu decisions: The chat and the desk

**Status:** active, 2026-10-30.

Promptu in `embarch-chat` and on desk Start work: step 3, and the owner's answers to its forks. Moved verbatim from `decisions.md` on 2026-10-30, when step 3's fork answers took it past its 25 KB cap ([DOC-COMPACTION.md](../../DOC-COMPACTION.md) §2).

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 16 — Start work runs the pass on the issue; the rail; the linker
From step 3, desk Start work runs the pass on the issue itself and leaves the improved start prompt in the draft, replacing today's read-and-summarize starter. `embarch-chat` gains a left rail, folded like VS Code's activity bar, holding Memory, Promptu, 📚 and 💡. The 💡 becomes the reference linker, gaining datasheet and spec sections through the atlas, instruments, captures and traces, Linear projects and docs, branches and worktrees, Kconfig symbols and devicetree nodes; Promptu owns missing context and improvement. **A reply inside a running task is never touched.**

### 17 — The owner's `CLAUDE.md` carries the rules
The memory rule went live on 2026-10-29, worded as 19 says. With step 2 come rules on design forks (interactive work waits for his pick), asking, web research in his own wording, and ignoring the footer. **Rejected:** "take the recommendation and proceed" as a standing rule.

### 19 — The memory rule says "in its frontmatter", not "at the top level"
Decided by the owner on 2026-10-29 (fork F2): the global `CLAUDE.md` rule tells Claude to add `kind:` "in its frontmatter (Claude Code may move it under `metadata:`)", since Claude Code moves it there on the next Write (18). The hook's T2 message says the same. **Rejected:** keeping "at the top level", which a file Claude wrote by the rule stops matching after one write.

### 32 — Start work takes the desk's default pattern, never a `never` one
Built in step 3 from 16 and the pattern field `signals.desk` (11): `promptu prep --start` marks a desk Start work run, which the chat sends for its own Start work and the skill's `--item` for the panel's. A pick that is missing, unknown or a `signals.desk: never` pattern becomes the `default` one, `implement-issue`; offline, so does the keyword pick; a `possible` pick (a bug, a bench validation, a review) stands. A replaced pick opens the chip row with the default recommended, so one Enter confirms it — the owner's pick, 37. **Rejected:** forcing `--pattern implement-issue`, which would turn every bug into an implementation.

### 33 — Where a memory is used: the prompts the owner sent
Built in step 3 for the memory menu (8), from the footer as the only record (13). A use is a fill from the entry in a footer of the last 30 days in this project's transcripts, found in **the owner's own sent message** — the chat's route — once per transcript; never in Claude's own text. **Amended by the owner on 2026-10-30 (fork P3 = b): sent prompts only**; `promptu render`'s JSON in a tool result, the terminal skill's shown prompt, no longer counts (it also closed review finding F3). A `memory.claude-md` fill names the global `CLAUDE.md` as a file. A removed worktree's runs are lost (fork P15, open). **Rejected:** a run log of Promptu's own (13); the terminal's shown prompt as a use, which counted runs cancelled at "send as is".

### 34 — Start work without a Promptu prompt: in the draft when Promptu is absent, sent when the pass fails
Decided by the owner on 2026-10-30 (forks P1 = a, P2 = b), for `embarch-chat` decision 96. With Promptu off on its card or not installed, Start work's read-and-summarize starter waits in the draft, unsent. With Promptu on but its pass failing or skipped (Esc), the starter is sent, as chat decision 11 sent it, and one line says so. The two differ on purpose: a pass that ran owes the owner a start. **Rejected:** the draft for both (P2 = a); sending for both (P1 = b).

### 35 — The Promptu icon: an indicator with a card, its switches the extension's, no key
Decided by the owner on 2026-10-30 (forks P4 = a, P10, P11 = a), for `embarch-chat` decision 95. A pattern forced on the card lights the icon for the next prompt, a reply included, once. There is no key for the pass: the indicator and its card instead. The card's switches live in the extension's own state for every window, never the owner's settings. **Rejected:** a forced pick waiting for the next task start; Ctrl+Shift+Enter on any draft; VS Code settings or per-chat switches.

### 36 — What is installed: the binary the desk finds, the bench tools the chat's CLI lists
Decided by the owner on 2026-10-30 (forks P5 = a, P6 = a). The desk counts Promptu as installed when the `promptu` binary is an executable in `~/.local/share/embarch/bin/` or on its service's `PATH` (`embarch-desk` decision 67). The chat passes `--have embarch-api` when its CLI's MCP list has the server, or before the CLI starts when the binary is on `PATH`. **Rejected:** reading Claude Code's plugin list or MCP configuration; a setting instead of detection.

### 37 — Start work's chip row when its default replaced the pick
Decided by the owner on 2026-10-30 (fork P7 = a), for 32. When `--start` took the default because the pick was missing, a `never` one or offline, the dialog opens on the chip row, the default recommended: one Enter takes it, and it is the only place to switch pattern. **Rejected:** the default taken silently.

### 38 — The dialog: Esc keeps what the owner gave; a pre-filled answer is changed in place
Decided by the owner on 2026-10-30 (forks P8 = a, P13 = b), for `embarch-chat` decision 96. Esc keeps the pages answered and the questions touched on the page on screen; the rest become stated assumptions. **A pre-filled answer is editable in place**: `prep` and `next` give each fill a page does not ask its question as a page shows it, what it holds and whether it changed (contract §7.8 `filled`); a change is an answer to its id, and the footer marks it `!`, as the footer grammar already defined. Built the same day. **Rejected:** Esc keeping only answered pages, as the terminal does; pre-filled answers read-only.

### 39 — The handoff card keeps the "Fresh chat with this handoff" chip
Decided by the owner on 2026-10-30 (fork P9 = a), for `embarch-chat` decisions 36 and 97. The prompt the handoff pattern writes still marks its message as a handoff request, so the turn that answers it offers a fresh chat with the brief. **Rejected:** leaving it to the pattern's `save_to`.

### 40 — The rail's icons are emoji at the bottom, beside the input
Decided by the owner on 2026-10-30 (fork P14 = a), for `embarch-chat` decision 94: 🧠 Memory, ✨ Promptu, 📚 and 💡, at the bottom of the rail beside the input they work on. The Usage icon's place (chat 99) is open, fork P16. **Rejected:** the top, as VS Code's activity bar; codicons.
