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
| `promptu memory [--json] [--no-used]` | Now with each entry's `used` (the footers of the last 30 days, in prompts the owner sent, that filled a question from it — decision 33) and `used_claude_md`; `--no-used` skips reading the transcripts | §5 |
| `promptu calls <session> [--subagent <id>] [--class <name>] [--json]` | Calls and result characters per thread (main, each subagent with its `meta.json` description) and per class; `--class` lists that class's calls with sizes; `<session>` is a `.jsonl` path or a session id; exit 2 for an unknown session or subagent | §12 |
| `promptu prior <prompt-file> [--projects <dir>] [--json]` | Read-only: the `AskUserQuestion` questions, options and answers of each earlier session whose first user turn is the prompt (text match; a near-match is counted, not listed); exit 2 for an unreadable file or folder | §13 |
| `promptu prep --start` | A desk Start work run: never a `signals.desk: never` pattern, the `default` one when there is no pick; output `start` and `pattern.start_default` | §7.8 |
| `prep` / `next` `filled[]` | A fill a page does not ask carries `ask`, `picked`, `other` and `changed`, so a dialog changes it in place; the change is an answer, `!` in the footer (decision 38) | §7.8 |

## Commands (decision 42, the rewrite)

| Command | What | Contract |
|---|---|---|
| `promptu render <run> …` | Now also rewrites a rough prompt (one model call; a brief, no-pattern, offline or `rewrite = "off"` run is not), writes `log/<run>.json`, and adds `"rewritten"` to its JSON; the footer gains `rewritten=yes` | §8.3, §8.4 |
| `promptu original <run> [--json]` | **The read-back verb** (for `embarch-chat`'s card, EMB-197): stdout is the run's rough prompt exactly as typed, no added newline; `--json` the whole log entry; **exit 0** printed, **exit 2** with one stderr line and nothing on stdout when the run has no log entry or the id is not a run id | §8.5 |
| `promptu stats [--model <name>] [--json]` | p50 and p95 (nearest rank) of the wait after the last question (`wait_ms`) and the rewrite call (`rewrite_ms`) over the logged rewritten runs, overall and per model; exit 0 | §8.6 |

**The log entry** (`log/<run>.json`, contract §8.4): `promptu`, `run`, `date`, `cwd`, `project_key`, `pattern`, `version`, `mode` (`prompt`·`brief`), `original`, `rendered` (what landed in the draft, footer included: the weekly loop's edit baseline), `rewritten`, `rewrite_skipped` (`brief`·`no-pattern`·`offline`·`off`·`failed: …`), `rewrite_model`, `rewrite_effort`, `rewrite_ms`, `wait_ms`.

## Commands (build step 4: `week pack` for run events, `draft`, `status`, `show` and `desk` built; the rest is the contract)

| Command | What | Contract |
|---|---|---|
| `promptu week pack [--week <w>] [--projects <dir>] [--json]` | The week's events into `week/<w>/pack.json`; no model. **Built: all five event kinds**: `run` (footer facts, the owner's edit as a diff), `session` (friction candidates, whether it started with Promptu), `unmatched`, `outcome` (a commit, a subagent's included), `carried` (EMB-274) | §14.4, §14.5 |
| `promptu week draft [--week <w>] [--pack <path>] [--json]` | **Built.** The one model call: the sheet's lines, each pattern line linted and its examples rendered old and new, a question, signal or source change replayed on past prompts; supersedes the open sheet; a failed call writes only `run.json` and exits 1 | §14.4 |
| `promptu week run [--week <w>] [--scheduled] [--json]` | **Built (EMB-277).** `pack` then `draft` under `week/run.lock`; what the timer runs; writes `run.json` (kind, start, end, status, cost), a failed run too; exit 4 when another run is in progress | §14.4 |
| `promptu week status [--json]` | **Built.** Schedule, last run, next run, missed, running, open count (what the chat's card asks); `PROMPTU_NOW` pins the clock | §14.4 |
| `promptu week show [--week <w>] [--json]` | **Built.** The open sheet: `sheet.json`, or `sheet.md` as text | §14.4 |
| `promptu week mark <id>... [--verdict approve\|cut] [--note <t>] [--feel better\|same\|worse]` | A line's or a group's ✓/✕, the sheet's feel | §14.4 |
| `promptu week apply [--week <w>] [--dry-run] [--json]` | Approved pattern lines as commits on a branch, never pushed; memory lines into the memory folder | §14.4 | 
| `promptu week timer [--enabled] [--json]` | **Built (EMB-277).** Prints the systemd user timer and service from `week_schedule`, binary path in `ExecStart`; installs nothing; `--enabled` records the instant in `week/timer.json` | §14.4 |
| `promptu desk --json` | **Built.** The open count and groups for the desk's `GET /promptu` | §9 |

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
| `promptu original <run>`, `log/<run>.json` | `promptu render` (decision 42) | `embarch-chat`'s Promptu card (rollback, EMB-197), the weekly loop (`rendered`), `promptu stats` | §8.4–§8.6 |
| Pattern files (`patterns/*.md`) | the repo; the weekly loop's approved changes (step 4) | `prep`, `lint`, `render` | §7.1 |
| `promptu prep` and `next` JSON | step 2 | the `/promptu` skill, the chat's dialog (step 3) | §7.8, §8.2 |
| `promptu patterns` JSON | step 3 | the chat's Promptu card | §7.9 |
| `promptu render` input and output | step 2 | the skill, the chat | §8 |
| `promptu desk --json` | step 4 | the desk's `GET /promptu`, the chat's card | §9 |
| `sheet.json`, `week/<week>/` | `promptu week draft`, step 4; `mark` and `apply` change it | the Desk section, the chat's card, `/embarch-promptu:review` | §10, §14.1 |

**Step 5 (the linker's kinds, under way):** adds no `promptu` command. Contract §15 fixes the reference entry, the kinds table and three read surfaces: `embarch-atlas refs --json`, `embarch-api --json list-studies` and the desk's `GET /refs` (`projects`, `documents`).

What a later step may change, and what it may not: contract §11.

## Files

| Path | What |
|---|---|
| `~/.config/embarch-promptu/config.toml` | The machine's settings: `memory_hook`; `pass_effort`, `pass_model`, `pass_timeout_s`; `rewrite`, `rewrite_model`, `rewrite_effort`, `rewrite_timeout_s` (decision 42); `week_schedule`, `week_model`, `week_effort`, `week_timeout_s`, `week_checkout`, `week_public_check` (the weekly pass, contract §14.2); `voice_skill`, `memory_claude_md_sections`, and `[embarch]` `desk` / `embarch-api` = `auto` · `on` · `off` (contract §7.6) |
| `~/.local/state/embarch-promptu/` | Runs between `prep` and `render`, each project's last answers, drafts, `log/` (one entry per rendered run, never pruned) and `week/` (one folder per week: pack, run record, sheet, proposed files; contract §7.5, §14.1) |
| `<memory base>/projects/<folder>/memory/` | Claude Code's auto-memory folder, located as contract §1.2 says |
| `plugin/` in the repo | The `embarch-promptu` plugin: `.claude-plugin/plugin.json`, `hooks/hooks.json`, `skills/promptu/SKILL.md`, `skills/review/SKILL.md` (the weekly sheet in the terminal) |
| `patterns/` in the repo | The pattern set, embedded in the binary; `PROMPTU_PATTERNS` reads a folder instead |
