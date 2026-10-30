# embarch-promptu: interfaces

**Status:** active, 2026-10-29.

An index. **The reference is the repo's [docs/contract.md](../../embarch-promptu/docs/contract.md)**, which every build step codes against; this file says what exists and where the contract defines it, and does not restate it. Current truth: [spec.md](spec.md). Why: [decisions.md](decisions.md).

## Commands (build step 1)

| Command | What | Contract |
|---|---|---|
| `promptu hook` | Reads Claude Code's hook JSON on stdin; checks a memory write; answers by mode | §3 |
| `promptu memory [--json]` | The memory that loads in the current folder: scope → domain → kind, ids, ages, stale flags | §5 |
| `promptu memory check [<path>...] [--json]` | The T and I checks on files as they stand; exit 1 on an error, 2 on a bad path | §4 |

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
| `promptu prep` JSON | step 2 | the `/promptu` skill, the chat's dialog | §7, sketch |
| `promptu render` input and output | step 2 | the skill, the chat | §8, sketch |
| `promptu desk --json` | step 4 | the desk's `GET /promptu` | §9, sketch |
| `sheet.json` | the weekly drafter, step 4 | the Desk section | §10, sketch |

What a later step may change, and what it may not: contract §11.

## Files

| Path | What |
|---|---|
| `~/.config/embarch-promptu/config.toml` | The machine's settings; step 1 reads `memory_hook` |
| `<memory base>/projects/<folder>/memory/` | Claude Code's auto-memory folder, located as contract §1.2 says |
| `plugin/` in the repo | The `embarch-promptu` plugin: `.claude-plugin/plugin.json`, `hooks/hooks.json` |
