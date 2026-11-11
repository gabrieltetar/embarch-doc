# embarch-chat: spec

**Status:** active, 2026-11-01. **Decisions 94–100 installed** (67 retired): measured 2026-11-05, the installed `dist/extension.js` is md5-identical to the clone's, built 2026-11-04 02:10 after `2b04ff5`; install time unrecorded. Decision 100 is not recorded as reviewed. Deployed from a local `.vsix`: decisions 1–49 (with `embarch-desk` d9a8efc, `embarch-ui` 2e73649, the desk's chat setting on) and **50–85 on 2026-10-23** (embarch-chat b6996cc). **Decisions 86–88 installed 2026-10-25** (embarch-chat d998b2f, with `embarch-desk` 9d43fe4 and `embarch-ui` ab1b9f8), **89–91 2026-10-26** (0f8d613; 91's column 0067fcf), **92–93** the same day (c973aec); 50–88 each after three review rounds. The repo has a public GitHub remote, and `main` is pushed.

What is true now. Why: [decisions.md](decisions.md). Unresolved: [open.md](open.md). Settings, commands, keys, the `claude` command line and the desk calls: [interfaces.md](interfaces.md). Constants: [spec/constants.md](spec/constants.md). The input's library, assistant and Promptu: [spec/input.md](spec/input.md).

## 1. What it is

**The owner's own Claude Code chat, as a VS Code extension beside the code**, replacing Claude Code's panel for his work (decisions 1, 2). **Every chat is bound to a desk work item before it starts**, and the thread list shows every thread of the window's desk by work item, waiting-on-you first (9, 10). It carries the prompt library — what `embarch-promptu` was planned to be (6) — a Haiku assistant at the input, bench cards, atlas links, and `embarch-ui`'s launcher (29).

## 2. How it works

- **One `claude` per open chat**, run by the extension host over Claude Code's own stream-json wire with the official panel's flags (5): permission prompts, questions and plans arrive as requests and are answered as forms; the panel declares its own autosave hook, dialogs and, when on, a diagnostics MCP server in `initialize` (61, 65, 66). The `claude` on `PATH` (30).
- **A chat is an editor tab**, what it opens goes beside it, and `chatLocation` = `sidebar` restores the sidebar (92). **A file link opens the file Claude meant** (93).
- **A chat belongs to the window that started it.** A thread another window or a terminal runs is read-only, opened from its transcript, with Jump (31). A past chat resumes here only when `claude agents` lists nothing running it.
- **A process closes 5 minutes after its last input or reply** unless a background task runs, it waits on the owner, or a Remote Control bridge holds it — one the owner turned on, or one the CLI started by itself while the chat is open, so an open chat stays reachable from the phone; the next message resumes it (41, 83, 100). **A reload** — the window back within 90 s — brings back the chats on screen with their drafts, queued messages, mode and effort; an interrupted step continues only on a click (63).
- **The desk is reached from the Node side only** (20): the list polls `GET /view`, each window polls the desk's mailbox for its folders, and Start work and Open chat land through it (11). The chat's header is its card in two lines (18).
- **An issue that is Done or Canceled ends its chat** (104): the desk's `end` entry puts `Chat has ended because the issue is done` (or `canceled`) over the chat with one Close window button, closes the input for good and survives a reload, after a running turn; an `unfinished` lists its blockers over the live chat with Finish. Nothing closes without a click.
- **The library, the Haiku assistant, Promptu and the desk's reference index** (what the chat offers at the input): [spec/input.md](spec/input.md).
- **A step names what it touched** — the connector's glyph, then the issue, PR, channel, card, board or study as a link — and a folded run lists them (87). **Bench results become cards** from the `embarch-api` tool result already in the stream, and **atlas citations become links** into the repo's `embarch/atlas` (15, 16).
- **What the CLI sends Claude is not the owner's** (89): a `user` line whose `origin.kind` is not `human` is no bubble — a background task's end is a one-line row (`Agent "…" completed`) that opens its card, one that ends while idle gets its row ahead of the turn the CLI starts, another session's message folds to `Message from <name>`; a reload brings the same rows back from the transcript's `queued_command`.
- **An agent can hand its chat to a fresh session** (103): `handoff(prompt)`, a tool of the panel's own MCP server, shows a card with the prompt editable and Continue or Stay (`embarchChat.handoff`: `card`, `immediate`, `off`). Continue starts a new session on the same work item in the same panel, in the chat's mode, model and effort, the old history above a divider; Stay answers the tool and the agent carries on.
- **A background agent's card shows its report** (90): the hand-back the CLI sends Claude, else the subagent's last reply, under a collapsed "Report"; never the launch reply. The hand-back is not yet seen on the wire.

## 3. Invariants

- **The webview never holds the desk token**, and the desk client calls loopback only (20, 48).
- **Nothing a workspace controls redirects the panel**: every setting is machine-scoped, and an untrusted workspace does not run it (48).
- **A chat keeps the login it was created under**; a window's login and desk come from machine settings by folder, and its picker moves only the login (101).
- **A due login is refreshed by one process alone**: a chat's process waits for its warm-up and Haiku starts nothing meanwhile; a turn the CLI's refresh lock still ended goes again once (105).
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
