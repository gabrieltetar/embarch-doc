# embarch-promptu: interfaces

**Status:** active, 2026-10-29.

An index. **The reference is the repo's [docs/contract.md](../../embarch-promptu/docs/contract.md)**, which every build step codes against; this file says what exists and where the contract defines it, and does not restate it. Current truth: [spec.md](spec.md). Why: [decisions.md](decisions.md).

## Commands (build step 1)

| Command | What | Contract |
|---|---|---|
| `promptu hook` | Reads Claude Code's hook JSON on stdin; checks a memory write; answers by mode | §3 |
| `promptu memory [--json]` | The memory that loads in the current folder: scope → domain → kind, ids, ages, stale flags | §5 |
| `promptu memory check [<path>...] [--json]` | The T and I checks on files as they stand; exit 1 on an error, 2 on a bad path | §4 |

## Commands (build step 2)

| Command | What | Contract |
|---|---|---|
| `promptu prep [--have <parts>] [--pattern <id>\|none] [--rec] [--desk <file>] [--offline]` | The rough prompt on stdin: picks the pattern, fills what the sources say, plans the dialog pages; `--have` names the EmbArch parts the session has | §7.8 |
| `promptu next <run>` | A page of answers on stdin; prints the pages left | §8.2 |
| `promptu render <run> [--rest recommended\|assume] [--text]` | The prompt and its footer | §8.3 |
| `promptu lint [<path>...] [--json] [--show] [--have <parts>]` | Pattern files against the schema and AskUserQuestion's limits; renders every example, with or without EmbArch | §7.7 |
| `/promptu [--item <wNN>] [pattern=<id>] [--rec] <rough prompt>` | The plugin's skill: runs the three commands and the dialogs, then "send as is / edit"; `--item` (step 3) is the desk's Start work: `prep --start` with that work item | §7.8, §8 |

## Commands (build step 3)

| Command | What | Contract |
|---|---|---|
| `promptu patterns [--json]` | The task patterns, name order: name, version, summary, description, `signals.desk`; for the chat's Promptu card | §7.9 |
| `promptu memory [--json] [--no-used]` | Now with each entry's `used` (the footers of the last 30 days that filled a question from it) and `used_claude_md`; `--no-used` skips reading the transcripts | §5 |
| `promptu prep --start` | A desk Start work run: never a `signals.desk: never` pattern, the `default` one when there is no pick; output `start` and `pattern.start_default` | §7.8 |

## The hook

- **Registered** by the plugin's `hooks/hooks.json` on PreToolUse and PostToolUse, matcher `Write|Edit|MultiEdit`, command `promptu hook` found on `PATH`, timeout 5 s (contract §3.1).
- **Answers:** nothing, or exit 0 with `{"hookSpecificOutput":{"hookEventName":…,"additionalContext":…}}`, or, in block mode on an error, exit 2 with the reason on stderr. Never a `permissionDecision`, never a `systemMessage` (§3.5).
- **Checks** T1–T7 (topic file), I1–I5 (index), O1 (orphans, PostToolUse); ids are permanent (§3.4).
- **Configuration:** `memory_hook = "warn" | "block" | "off"` in `~/.config/embarch-promptu/config.toml`; `PROMPTU_MEMORY_HOOK` overrides; `PROMPTU_CONFIG_DIR` moves the folder (§3.7). `PROMPTU_TODAY` pins the date for tests (§0).

## Shared with later steps

| Interface | Written by | Read by | Contract |
|---|---|---|---|
| Memory labels (`kind`, `type`, `review-by`, `source`, domains) | Claude, under the `CLAUDE.md` rule | the hook, the inventory | §2 |
| The footer, `— promptu <pattern>@<version> …`, and the 6-hex memory id | `promptu render` (step 2) | the memory menu's "used", the weekly loop | §6 |
| Pattern files (`patterns/*.md`) | the repo; the weekly loop's approved changes (step 4) | `prep`, `lint`, `render` | §7.1 |
| `promptu prep` and `next` JSON | step 2 | the `/promptu` skill, the chat's dialog (step 3) | §7.8, §8.2 |
| `promptu patterns` JSON | step 3 | the chat's Promptu card | §7.9 |
| `promptu render` input and output | step 2 | the skill, the chat | §8 |
| `promptu desk --json` | step 4 | the desk's `GET /promptu` | §9, sketch |
| `sheet.json` | the weekly drafter, step 4 | the Desk section | §10, sketch |

What a later step may change, and what it may not: contract §11.

## Files

| Path | What |
|---|---|
| `~/.config/embarch-promptu/config.toml` | The machine's settings: `memory_hook`; `pass_effort`, `pass_model`, `pass_timeout_s`, `voice_skill`, `memory_claude_md_sections`, and `[embarch]` `desk` / `embarch-api` = `auto` · `on` · `off` (contract §7.6) |
| `~/.local/state/embarch-promptu/` | Runs between `prep` and `render`, each project's last answers, drafts (contract §7.5) |
| `<memory base>/projects/<folder>/memory/` | Claude Code's auto-memory folder, located as contract §1.2 says |
| `plugin/` in the repo | The `embarch-promptu` plugin: `.claude-plugin/plugin.json`, `hooks/hooks.json`, `skills/promptu/SKILL.md` |
| `patterns/` in the repo | The pattern set, embedded in the binary; `PROMPTU_PATTERNS` reads a folder instead |
