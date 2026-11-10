# embarch-promptu spec: build steps 2 and 3 (not installed)

**Status:** active, 2026-11-10.

Split verbatim from [../spec.md](../spec.md) §2b and §2c on 2026-11-10, under [DOC-COMPACTION.md](../../DOC-COMPACTION.md) §2: `spec.md` was in reserve (9,563 of 10,240 B). The text is unchanged. Current truth: [../spec.md](../spec.md). Why: [../decisions.md](../decisions.md).

## 2b. What exists: build step 2, the terminal pass (committed, not installed)

- **`/promptu <rough prompt>`**, a skill in the plugin (0.2.0), run only when typed (decision 12): `promptu prep`, each page through AskUserQuestion and `promptu next`, `promptu render`, then "send as is / edit / cancel" before any work.
- **EmbArch parts** (decision 29): the skill passes the parts its session has (`--have desk,embarch-api`), and `[embarch]` in `config.toml` can force each on or off. A question or option marked `requires:` a missing part is hidden; a generic fallback stays.
- **`promptu prep`** (decision 9): gathers the sources with no model (the checkout, the project's `MEMORY.md` with each line's memory id, the global `CLAUDE.md` bullets, last time's answers in this project (27), a desk work item passed as a file (26)), runs **one stripped `claude -p` on Sonnet at effort medium** (decision 22), drops every fill whose quote is not in its source (decision 10), and plans the questions: required ones unanswered, costliest gap first; the always-asked; the optional ones the pass marked relevant. A weak pick opens a chip row; a failed or slow pass falls back to a keyword pick. A pasted brief asks only its gaps (decision 24).
- **`promptu next`** records a page of answers and re-plans; **`promptu render`** writes the six-section prompt with the owner's words verbatim under Goal, stated assumptions for what Esc left open, and the footer (decision 13). It keeps each pattern's last answers per project and the draft under `~/.local/state/embarch-promptu/`.
- **Planning for high context** (decision 41): the pass also judges whether the work will outgrow one context window, from the text and, when `prep --context-usage <percent>` gives it (the chat does), how full the chat already is. A big task gets one line in Who does it, `Context plan, <way>: <how> Why: <why>`, naming parallel workers, a handoff, scheduled compactions or a split into tasks; the footer carries `way=<name>`. A small task gets nothing, and the Goal stays verbatim. Contract §7.10; the tests pin one render per way and one for the small task.
- **The patterns**: 11 and 2 fragments in the repo's `patterns/`, embedded in the binary (decisions 11, 23). **`promptu lint`** checks them against the schema and AskUserQuestion's limits and renders every example; the tests pin each render.

## 2c. Build step 3 (built, not installed)

- **The CLI** (decisions 32–33): `promptu patterns`, "where it's used" in `promptu memory`, `prep --start`, the skill's `--item`.
- **`embarch-chat`** (its 94–98): a rail: Memory, Promptu, Library, Suggestions; at a task start Enter runs the pass in a dialog, the prompt lands in the draft, unsent; Start work runs it on the issue; Memory menu.
- **`embarch-desk`** (its 67): chat setting off, Start work types `/promptu --item <wNN> Work on KEY — title`.
