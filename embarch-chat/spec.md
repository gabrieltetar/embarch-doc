# embarch-chat: spec

**Status:** active, 2026-10-30. **Decisions 94–99 built, review round 1's findings fixed, not installed; 67 retired** (`embarch-promptu` build step 3). Shipped and deployed on the owner's machine from a local `.vsix` — decisions 1–49, with `embarch-desk` d9a8efc, `embarch-ui` 2e73649 and the desk's chat setting on. **Decisions 50–85 installed 2026-10-23 21:58** (embarch-chat b6996cc), after three independent review rounds. **Decisions 86–88 installed 2026-10-25 17:08** (embarch-chat d998b2f), after three review rounds, live after the owner's window reload, with `embarch-desk` 9d43fe4 and `embarch-ui` ab1b9f8 deployed the same minute. **Decisions 89–91 installed 2026-10-26 12:42** (embarch-chat 0f8d613), and 91's wider column **13:11** (0067fcf), each live after the owner's window reload. **92–93 installed 14:43** (c973aec). The repo has a public GitHub remote, and `main` is pushed.

What is true now. Why: [decisions.md](decisions.md). Unresolved: [open.md](open.md). Settings, commands, keys, the `claude` command line and the desk calls: [interfaces.md](interfaces.md). Constants: [spec/constants.md](spec/constants.md).

## 1. What it is

**The owner's own Claude Code chat, as a VS Code extension beside the code**, replacing Claude Code's panel for his work (decisions 1, 2). **Every chat is bound to a desk work item before it starts**, and the thread list shows every thread of the window's desk by work item, waiting-on-you first (9, 10). It carries the prompt library — what `embarch-promptu` was planned to be (6) — a Haiku assistant at the input, bench cards, atlas links, and `embarch-ui`'s launcher (29).

## 2. How it works

- **One `claude` per open chat**, run by the extension host over Claude Code's own stream-json wire with the official panel's flags (5): permission prompts, questions and plans arrive as requests and are answered as forms; the panel declares its own autosave hook, dialogs and, when on, a diagnostics MCP server in `initialize` (61, 65, 66). The `claude` on `PATH` (30).
- **A chat is an editor tab**, what it opens goes beside it, and `chatLocation` = `sidebar` restores the sidebar (92). **A file link opens the file Claude meant** (93).
- **A chat belongs to the window that started it.** A thread another window or a terminal runs is read-only, opened from its transcript, with Jump (31). A past chat resumes here only when `claude agents` lists nothing running it.
- **A process closes 5 minutes after its last input or reply** unless a background task runs, it waits on the owner, or a Remote Control bridge the owner turned on; the next message resumes it (41, 83). **A reload** — the window back within 90 s — brings back the chats on screen with their drafts, queued messages, mode and effort; an interrupted step continues only on a click (63).
- **The desk is reached from the Node side only** (20): the list polls `GET /view`, each window polls the desk's mailbox for its folders, and Start work and Open chat land through it (11). The chat's header is its card in two lines (18).
- **The library** is two folders: this repo's `plugin/` (a Claude Code plugin: `/embarch-permissions`, `/embarch-claude-md`, the `build-flash-verify` skill) and `~/.claude/commands` for anything naming a client, as 📚 buttons by `category:` (13, 38, 39).
- **The Haiku assistant**, for the chat on screen only: ghost text, 💡 cards that edit the draft, reply chips, a name for each new chat — one stripped, unsaved `claude -p` per call (19, 24–27, 34, 36, 37). The 💡 and 📚 menus go by keyboard as IntelliSense does, and a preview never moves the menu under the pointer (86).
- **Promptu** (decisions 94–98, the `embarch-promptu` CLI): a rail on the left edge holds Usage (99) at the top, Memory, Promptu, the 📚 and the 💡 at the bottom. At a task start, or on Start work (11), Enter runs `promptu prep` and a dialog over the chat asks what is missing; the prompt lands in the draft, never sent. The Memory menu draws `promptu memory --json`; the 💡 keeps references and context handling (97).
- **The desk's reference index is mirrored** from `GET /refs` (88): the cards call carries the issues and PRs the draft matches locally, so a vague "the widget PR" becomes the PR itself, and a key or PR in Claude's prose the index knows is a link.
- **A step names what it touched** — the connector's glyph, then the issue, PR, channel, card, board or study as a link — and a folded run lists them (87). **Bench results become cards** from the `embarch-api` tool result already in the stream, and **atlas citations become links** into the repo's `embarch/atlas` (15, 16).
- **What the CLI sends Claude is not the owner's** (89): a `user` line whose `origin.kind` is not `human` is no bubble — a background task's end is a one-line row (`Agent "…" completed`) that opens its card, one that ends while idle gets its row ahead of the turn the CLI starts, another session's message folds to `Message from <name>`; a reload brings the same rows back from the transcript's `queued_command`.
- **A background agent's card shows its report** (90): the hand-back the CLI sends Claude, else the subagent's last reply, under a collapsed "Report"; never the launch reply. The hand-back is not yet seen on the wire.

## 3. Invariants

- **The webview never holds the desk token**, and the desk client calls loopback only (20, 48).
- **Nothing a workspace controls redirects the panel**: every setting is machine-scoped, and an untrusted workspace does not run it (48).
- **Only the owner's own pick untracks a chat**; a resume never sends `untracked` (48).
- **A chat is on its work item before `claude` starts** (10).
- **Nothing new is stored**: the transcript is Claude's, session → item the desk's, a name Claude's own `rename_session` or `custom-title` (12, 75).
- **Nothing reruns by itself**: after a reload, an interrupted step reruns only on Continue (63).
- **Promptu never sends and never blocks sending**: its prompt goes to the draft; a failure is one line and the draft as typed (96).
- **A card only edits the draft**, previewed in place, never acting outside it (36, 37); nothing typed answers a card that arrived mid-typing (55). **The pointer only previews**: Enter and Tab pick a row only the keys reached, and that row's preview is what shows (86).
- **A reference in the draft is written from the desk's index, never from Haiku's text**, and references are matched locally: nothing on a keystroke reaches the network (88).
- **A link taken from outside** — a tool's output, a command, the desk's index — **opens only as https to its connector's own host**; the Desk's and the bench's are built from `embarch-ui`'s address. **A `gh` step's PR is linked only in the repo the step or its output names** (87).
- **A line of the CLI's is never the owner's**: not matched to a pending message, edited or rewound to (89).
- **Effort is the chat's own**, never written to the owner's settings (82).
- **A link opens once, through the extension**: http(s) in the browser, a path beside the chat (92, 93); any other URI is shown, not opened.

## 4. Constants

Idle close, the column, timings, caps and the tested `claude` range: [spec/constants.md](spec/constants.md).

## 5. What it deliberately does not do

- **No Marketplace listing**: an internal `.vsix`, sideloaded by `./reinstall.sh`, which a VS Code server update drops silently.
- **No hosting outside the window**: no desk-side or daemon process runs chats, and no window takes over another's (5, 31).
- **No toasts**: waits are a count, unread a dot that joins no count (35, 80).
- **No store of its own** — no chat index, no bookmarks (12, 84).
- **No client-named library entry in a repo** (13).
- **No automatic rerun** of an interrupted step (63).

## 6. Pointers

The repo: `../embarch-chat` (local, no remote); its README covers building, testing and installing. The desk side — the mailbox, the Desk's line per chat, the work item's notes: [embarch-desk](../embarch-desk/spec.md), routes in its [interfaces.md](../embarch-desk/interfaces.md). The launcher's own history: `embarch-ui` decisions 3 and 28.
