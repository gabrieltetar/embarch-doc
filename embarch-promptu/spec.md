# embarch-promptu: spec

**Status:** active, 2026-10-29. In progress: build step 1 of 5 (memory) passed its three review rounds, is pushed, and is installed on the owner's machine in warn mode — the `promptu` binary in `~/.local/share/embarch/bin/`, the plugin from the `embarch` marketplace in `embarch-umbrella` (decision 20). Build step 2 (the terminal pass, `/promptu`) passed its three review rounds and is committed locally in `embarch-promptu`, not pushed or installed. Steps 3–5 are designed ([decisions.md](decisions.md)) and not started.

What is true now. Why: [decisions.md](decisions.md). Unresolved: [open.md](open.md). Reference: [interfaces.md](interfaces.md), and the repo's own [docs/contract.md](../../embarch-promptu/docs/contract.md), the interface every build step shares.

## 1. What it is

**Promptu turns a rough prompt into a good one, and keeps Claude Code's memory organised** (decision 1). It is a Claude Code plugin, `embarch-promptu`, plus a small Rust CLI, `promptu`, that prints its data as JSON. **It works on its own** in any Claude Code setup, installed with `cargo install --git …` or as a release binary in `~/.local/bin` (decision 29); **the rest of EmbArch is an optional integration**: with the desk, a work item becomes a source; with the bench tools, bench sessions can flash through them; from step 3, `embarch-chat`'s rail draws its menus. Without them, what needs them is hidden and the generic rest stays. The repo is `embarch-promptu`: public, MIT.

## 2. What exists: build step 1, memory

- **The labels** (decision 4). Each auto-memory topic file carries `kind` (`preference` · `rule` · `trap` · `reference` · `status`) beside Claude Code's own `type`, which must match it; a `status` carries `review-by` at most 90 days ahead, a `reference` carries `source`. Its `MEMORY.md` line sits under a `## <domain>` header in 150 characters or less. The rule telling Claude so is in the owner's global `CLAUDE.md`.
- **`promptu hook`** (decisions 5–7), run by the plugin's PreToolUse and PostToolUse hooks. A Write, Edit or MultiEdit into an auto-memory folder is checked as the file the write would leave, on what the write touches: T1–T7 on a topic file, I1–I5 on the index, and O1 (orphaned topic files) after an index write. **Warn mode** is the default: the write goes ahead and Claude is told what to fix. **Block mode** refuses a write with an error (exit 2); `off` checks nothing. Set in `~/.config/embarch-promptu/config.toml`.
- **`promptu memory [--json]`** (decision 8): the memory that loads in a folder, by scope (user, auto, project), then domain, then kind, each entry with its 6-hex memory id, age and stale flags.
- **`promptu memory check [<path>...]`**: the same checks on files as they stand.
- **The plugin** `embarch-promptu` 0.1.0, the two hooks, installed from the `embarch` marketplace (decision 20).

## 2b. What exists: build step 2, the terminal pass (committed, not installed)

- **`/promptu <rough prompt>`**, a skill in the plugin (0.2.0), run only when typed (decision 12): `promptu prep`, each page through AskUserQuestion and `promptu next`, `promptu render`, then "send as is / edit / cancel" before any work.
- **EmbArch parts** (decision 29): the skill passes the parts its session has (`--have desk,embarch-api`), and `[embarch]` in `config.toml` can force each on or off. A question or option marked `requires:` a missing part is hidden; a generic fallback stays.
- **`promptu prep`** (decision 9): gathers the sources with no model (the checkout, the project's `MEMORY.md` with each line's memory id, the global `CLAUDE.md` bullets, last time's answers in this project (27), a desk work item passed as a file (26)), runs **one stripped `claude -p` on Sonnet at effort medium** (decision 22), drops every fill whose quote is not in its source (decision 10), and plans the questions: required ones unanswered, costliest gap first; the always-asked; the optional ones the pass marked relevant. A weak pick opens a chip row; a failed or slow pass falls back to a keyword pick. A pasted brief asks only its gaps (decision 24).
- **`promptu next`** records a page of answers and re-plans; **`promptu render`** writes the six-section prompt with the owner's words verbatim under Goal, stated assumptions for what Esc left open, and the footer (decision 13). It keeps each pattern's last answers per project and the draft under `~/.local/state/embarch-promptu/`.
- **The patterns**: 11 and 2 fragments in the repo's `patterns/`, embedded in the binary (decisions 11, 23). **`promptu lint`** checks them against the schema and AskUserQuestion's limits and renders every example; the tests pin each render.

## 3. Invariants

- **No model call and no network** in the hook, the checks or the inventory. The pass is the only model call, and `lint`, `next` and `render` are model-free and deterministic.
- **Render, don't rewrite** (decision 9): the rough prompt reaches the rendered prompt verbatim, under Goal or, for a brief, as the whole of its start; no model rephrases it.
- **A fill stands only on evidence** (decision 10): its quote, folded for case, quotes and whitespace, is in the source it names, the source is one the question takes, and an always-asked question is pre-selected only from the prompt.
- **Nothing runs before the owner says so**: the skill shows the prompt and waits for "send as is" or "edit".
- **Promptu never blocks the task**: a missing binary or a failing command is one line, and Claude works on the rough prompt as typed; `prep` and `render` degrade rather than fail (contract §7.8, §8.3).
- **Works without EmbArch** (decision 29): with no EmbArch part, no page shows EmbArch text and every page still has 2–4 options [tested on every pattern].
- **The hook fails open**: bad input, an unreadable file, an edit that would not apply, a panic, all exit 0 with nothing printed. It never answers with a `permissionDecision`, so Claude Code's own permission flow is untouched.
- **It checks only what a write touches**: a topic file's labels whenever the file is written; an index line only when the write adds or changes it, so a legacy long line never blocks an unrelated write.
- **A field counts at either level**, the top level or under `metadata:`: on a Write into a memory folder Claude Code moves every key but `name` and `description` under `metadata:` and restamps `node_type`, `originSessionId` and `modified` [measured 2026-10-29, Claude Code 2.1.287]. T7 (a dropped field) ignores the level and those three (decision 18).
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
| The pass, Sonnet 5.5 at effort medium | wall p50 3.9 s, p95 7.3 s; 18 of 20 picks right; about $0.02 a run [measured 2026-10-29, 23 of the owner's prompts]; timeout 15 s |
| `promptu render` / `prep` without the model, release build | p50 3.1 ms / 7.2 ms; the hook unchanged at p50 0.66 ms [measured 2026-10-29, WSL2] |
| A dialog page | at most 4 questions: 3 plus "Rest" while more remain |

## 5. What it deliberately does not do

- **Write or move a memory.** Claude writes memories freely; the hook only checks (decision 5).
- **See a shell write** into a memory folder (`>`, `sed -i`, `mv`): only Write, Edit and MultiEdit pass through it.
- **Cover subagent memory** or the personal memory folder: auto memory only.
- **Show startup cost** in the inventory (decision 8).
- **Install itself**, or decide a design fork: those wait for the owner (`docs/forks.md` in the repo; F1–F4 answered as decisions 18–21, S1–S3 as 22–24).
- **Touch a reply inside a running task** (decision 16): `/promptu` runs only when typed.
- **Rewrite the rough prompt or store a run log**: the footer is the record (decision 13); the state folder keeps the last answers and the draft only.

## 6. Pointers

- The repo: [README](../../embarch-promptu/README.md), [docs/contract.md](../../embarch-promptu/docs/contract.md), [docs/forks.md](../../embarch-promptu/docs/forks.md).
- `embarch-chat` decision 6, which this sub-project's revival amends; `embarch-desk` decisions 65 and 66, the Desk spot step 4 fills.
