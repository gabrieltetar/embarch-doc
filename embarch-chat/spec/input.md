# embarch-chat spec: the input and the library

**Status:** active, 2026-11-10.

Split verbatim from [../spec.md](../spec.md) §2 on 2026-11-10, under [DOC-COMPACTION.md](../../DOC-COMPACTION.md) §2: `spec.md` had 867 bytes before its reserve. These four bullets (the library, the Haiku assistant, Promptu, the desk's reference index) are what the chat offers at the input; they are unchanged. Current truth: [../spec.md](../spec.md). Why: [../decisions.md](../decisions.md).

- **The library** is two folders: this repo's `plugin/` (a Claude Code plugin: `/embarch-permissions`, `/embarch-claude-md`, the `build-flash-verify` skill) and `~/.claude/commands` for anything naming a client, as 📚 buttons by `category:` (13, 38, 39).
- **The Haiku assistant**, for the chat on screen only: ghost text, 💡 cards that edit the draft, reply chips, a name for each new chat — one stripped, unsaved `claude -p` per call (19, 24–27, 34, 36, 37). The 💡 and 📚 menus go by keyboard as IntelliSense does, and a preview never moves the menu under the pointer (86).
- **Promptu** (decisions 94–98, the `embarch-promptu` CLI): a rail on the left edge holds Usage (99) at the top, Memory, Promptu, Library, Suggestions and the 💬 side question (57) at the bottom, each a one-colour SVG. At a task start, or on Start work (11), Enter runs `promptu prep` and a dialog over the chat asks what is missing; the prompt lands in the draft, never sent. When it is Promptu's rewrite (`render` says `rewritten`; EMB-197), "Restore my original prompt" shows under the draft: one click, no question, the draft is `promptu original <run> --json`'s original, verbatim, Ctrl+Z undoes it; it is gone once restored, sent or cleared, and never shows for a brief, an offline or a rewrite-off run. The Memory menu draws `promptu memory --json`, and with three machine settings (`embarchChat.memoryPass.*`: stamp file, interval in days, command) it carries a periodic-pass line (last date, due) that starts a chat with the command, the icon dotted while due (98). **The card shows the weekly pass in one line** from `promptu week status --json` (95): last run, next run, a run in progress or missed, the waiting sheet's open count, one line on an error; the ✨ is dotted while a sheet waits or a run was missed; a `promptu` without the verb shows neither. A click on it opens the waiting sheet in a new chat (`/embarch-promptu:review` typed, unsent), else runs `promptu week run`, never twice at once (95). The 💡 keeps references only (97).
- **A gear at the rail's foot holds the mode, the model and its effort, Remote Control and MCP** (107): shown on a chat before its first message, the input's row the box and Send; one short `claude` per login and folder, sent no message, fills it before the chat's own runs (108).
- **The desk's reference index is mirrored** from `GET /refs` (88): the cards call carries the issues and PRs the draft matches locally, so a vague "the widget PR" becomes the PR itself, and a key or PR in Claude's prose the index knows is a link.

## Invariants of the input

Moved verbatim from [../spec.md](../spec.md) §3 on 2026-11-17.

- **Promptu never sends and never blocks sending**: its prompt goes to the draft; a failure is one line and the draft as typed (96).
- **A card only edits the draft**, previewed in place, never acting outside it (36, 37); nothing typed answers a card that arrived mid-typing (55). **The pointer only previews**: Enter and Tab pick a row only the keys reached, and that row's preview is what shows (86).
- **A reference in the draft is written from the desk's index, never from Haiku's text**, and references are matched locally: nothing on a keystroke reaches the network (88).
