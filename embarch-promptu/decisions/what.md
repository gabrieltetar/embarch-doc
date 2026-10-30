# embarch-promptu decisions: What Promptu is

**Status:** active, 2026-10-30.

What Promptu is and owns, what it stands beside, and how it ships. Moved verbatim from `decisions.md` on 2026-10-30, when step 3's fork answers took it past its 25 KB cap ([DOC-COMPACTION.md](../../DOC-COMPACTION.md) §2).

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 1 — Its own sub-project again, as a plugin plus a CLI
Decided by the owner on 2026-10-29, so Promptu can be used without `embarch-chat`. **This reverses `embarch-chat` decision 6**, where `embarch-promptu` became `embarch-chat`. It ships as one Claude Code plugin, `embarch-promptu@embarch`, and a `promptu` CLI that prints its data as JSON; it works in the terminal and in Claude Code's panel, and `embarch-chat` finds it installed and draws its menus. Promptu owns two things: memory organisation and prompt patterns. `embarch-chat` keeps the 📚 library and the 💡 assistant. **Rejected:** staying inside `embarch-chat`, which tied both to one UI.

### 29 — Promptu works with or without the rest of EmbArch
Decided by the owner on 2026-10-29. Promptu stands alone: the binary and the plugin need nothing else from the suite, and the README and spec describe standalone use first, EmbArch as the optional integration. **Detection is automatic with a config override**: the `/promptu` skill checks which EmbArch parts its session has, the desk (`desk_work_item`) and the bench tools (`embarch-api`), and passes them as `prep --have`; an `[embarch]` table in Promptu's `config.toml` forces each to `on` or `off`, `auto` by default. **What needs a missing part is hidden and a generic fallback stays**: a pattern marks such a question or option `requires: desk`, `requires: embarch-api`, or `requires: item` (the desk **and** a work item passed to the run, for anything that reads or writes the item); without it, it is not shown, filled or rendered, the model's catalogue leaves it out, and no text fill may equal a hidden label; a hidden recommendation gives way to the first option that shows (bench-session's "flash through EmbArch" gives way to "the project's own tooling"), and lint checks every `requires` and that each question keeps 2–4 options without EmbArch. **Install alone** with `cargo install --git …` or a release binary in `~/.local/bin`; inside the suite the binary stays in `~/.local/share/embarch/bin`. **Rejected:** requiring the desk for `/promptu`, and per-user pattern variants.

### 2 — Rust, one binary
Like `embarch-desk`: the hook runs on every file write in every session, and a Rust hook call costs about a millisecond [measured 2026-10-29]. **Rejected:** TypeScript (shares code with the chat, pays Node's start on every write), Python (fastest to write, tens of milliseconds a call [assumed]).

### 3 — Five build steps, each usable alone; built by agents under a contract
1 memory · 2 `/promptu` in the terminal · 3 Start work, the chat's dialog and rail · 4 the weekly loop and the Desk section · 5 the 💡 linker's new kinds. Background agents build each step in their own worktree, the contract (`docs/contract.md`) first, then three independent review rounds; nothing is installed before review passes. **A design fork goes to the owner's ranked list (`docs/forks.md`) and runs on its most reversible default; an agent never decides one.**

### 20 — The `embarch` marketplace moves to `embarch-umbrella`
Decided by the owner on 2026-10-29 (fork F3): the suite's `embarch` marketplace, until then a file in `embarch-desk`'s repo, moves to `embarch-umbrella` and lists every suite plugin, so this plugin keeps the id `embarch-promptu@embarch`. **Moved and re-registered 2026-10-29:** `embarch-umbrella/.claude-plugin/marketplace.json` lists `embarch-desk`, `embarch-promptu` and `embarch-chat`, each a `git-subdir` source (`url` + `path: plugin`). A `github` source with `path`, tried first, installed the whole repo as the plugin, so the plugin's manifest, hooks and MCP config were not found [measured on Claude Code 2.1.287]. `embarch-desk`'s file is gone. **Rejected:** a second entry in `embarch-desk`'s file (a suite list in one plugin's repo), a marketplace in this repo named `embarch` (clashes with the desk's) or named after it (changes the decided id).
