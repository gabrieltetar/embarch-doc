# embarch-promptu: spec

**Status:** active, 2026-10-29. In progress: build step 1 of 5 (memory) is built and tested, committed locally in its repo, not reviewed and not installed; steps 2–5 are designed ([decisions.md](decisions.md)) and not started.

What is true now. Why: [decisions.md](decisions.md). Unresolved: [open.md](open.md). Reference: [interfaces.md](interfaces.md), and the repo's own [docs/contract.md](../../embarch-promptu/docs/contract.md), the interface every build step shares.

## 1. What it is

**Promptu keeps Claude Code's memory organised, and from build step 2 turns a rough prompt into a good one** (decision 1). It is a Claude Code plugin, `embarch-promptu`, plus a small Rust CLI, `promptu`, that prints its data as JSON, so it works in the terminal, in Claude Code's panel and, from step 3, in `embarch-chat`'s rail, without needing `embarch-chat`. The repo is `embarch-promptu`: public, MIT, local commits only, no push yet.

## 2. What exists: build step 1, memory

- **The labels** (decision 4). Each auto-memory topic file carries `kind` (`preference` · `rule` · `trap` · `reference` · `status`) beside Claude Code's own `type`, which must match it; a `status` carries `review-by` at most 90 days ahead, a `reference` carries `source`. Its `MEMORY.md` line sits under a `## <domain>` header in 150 characters or less. The rule telling Claude so is live in the owner's global `CLAUDE.md` since 2026-10-29, and the owner relabelled three projects' memories the same evening.
- **`promptu hook`** (decisions 5–7), run by the plugin's PreToolUse and PostToolUse hooks. A Write, Edit or MultiEdit into an auto-memory folder is checked as the file the write would leave, on what the write touches: T1–T7 on a topic file, I1–I5 on the index, and O1 (orphaned topic files) after an index write. **Warn mode** is the default: the write goes ahead and Claude is told what to fix. **Block mode** refuses a write with an error (exit 2); `off` checks nothing. Set in `~/.config/embarch-promptu/config.toml`.
- **`promptu memory [--json]`** (decision 8): the memory that loads in a folder, by scope (user, auto, project), then domain, then kind, each entry with its 6-hex memory id, age and stale flags.
- **`promptu memory check [<path>...]`**: the same checks on files as they stand; exit 1 on an error.
- **The plugin** `embarch-promptu` 0.1.0 with the two hooks. It validates and installs into a scratch Claude Code config; it is installed nowhere for real, and where it will be listed is open.

## 3. Invariants

- **No model call and no network** in the hook, the checks or the inventory.
- **The hook fails open**: bad input, an unreadable file, an edit that would not apply, a panic, all exit 0 with nothing printed. It never answers with a `permissionDecision`, so Claude Code's own permission flow is untouched.
- **It checks only what a write touches**: a topic file's labels whenever the file is written; an index line only when the write adds or changes it, so a legacy long line never blocks an unrelated write.
- **A field counts at either level**, the top level or under `metadata:`: on a Write into a memory folder Claude Code moves every key but `name` and `description` under `metadata:` and restamps `node_type`, `originSessionId` and `modified` [measured 2026-10-29, Claude Code 2.1.287]. T7 (a dropped field) ignores the level and those three.
- **The memory folder is found as Claude Code finds it**: keyed on the main checkout, so a linked worktree shares it, with Claude Code's folder-name rule and its overrides; a `source:` path resolves against the checkout the folder's name encodes.
- **Frontmatter is read as Claude Code reads it**, with its lenient second pass, so a file Claude Code accepts is never called broken.
- **Public repo**: fixtures and examples are invented; nothing from the owner's memory or transcripts.

## 4. Constants

| Constant | Value |
|---|---|
| Hook call, release build, through `sh -c` as Claude Code runs it | p50 0.9–1.0 ms, p95 under 1.4 ms [measured 2026-10-29, WSL2, 300 calls per case] |
| Hook timeout in `hooks.json` | 5 s |
| Index line limit | 150 characters |
| `review-by` horizon | after today, at most 90 days |
| Memory id | first 6 hex digits of the SHA-1 of the topic file's name |
| Copies of the owner's memory after relabelling, `memory check` | the relabelled projects: 0 errors; the three not relabelled: 41 errors in 18 files [measured 2026-10-29] |

## 5. What it deliberately does not do

- **Write or move a memory.** Claude writes memories freely; the hook only checks (decision 5).
- **See a shell write** into a memory folder (`>`, `sed -i`, `mv`): only Write, Edit and MultiEdit pass through it.
- **Cover subagent memory** or the personal memory folder: auto memory only.
- **Show startup cost** in the inventory (decision 8).
- **Install itself**, or decide a design fork: those wait for the owner (`docs/forks.md` in the repo).

## 6. Pointers

- The repo: [README](../../embarch-promptu/README.md), [docs/contract.md](../../embarch-promptu/docs/contract.md), [docs/forks.md](../../embarch-promptu/docs/forks.md).
- `embarch-chat` decision 6, which this sub-project's revival amends; `embarch-desk` decisions 65 and 66, the Desk spot step 4 fills.
