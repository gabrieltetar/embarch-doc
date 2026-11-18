# 010 — A shell write into a memory index gets checked, or told to use Edit

**State:** done (claimed by agent/promptu/010-shell-writes-to-a-memory-index-get-checked, 2026-11-17 18:34)
**Source:** EMB-187, an audit finding: a memory index line added by a shell script skipped Promptu's memory checks and came out over the length limit
**Issue:** EMB-187
**Scope:** promptu
**Hardware:** none
**Owner:** no

## What

Promptu's memory hook (`src/hook.rs`, registered in `plugin/hooks/hooks.json`)
matches `Write|Edit|MultiEdit` only. A session that adds an index line to an
auto-memory `MEMORY.md` with a Bash command — read the file, splice a line
after an anchor, write it back — gets none of the index checks (line length,
domain header, one line per file), and nothing tells it so.

Close that route. Two directions are acceptable, and the smaller one that meets
the `Done when` is preferred:

- **A Bash hook rule**: on a Bash command that writes into an auto-memory
  folder, either run the same index findings on the file after the command
  (PostToolUse), or warn before it runs and name the Edit tool as the checked
  path (PreToolUse). Reuse `claude::memory_target` to decide what is an
  auto-memory folder; do not write a second copy of that rule.
- **A CLI verb** that adds an index line under a `## <domain>` header and runs
  the same checks.

A Bash command is free text, so detection will be a heuristic. Keep false
positives cheap: a warning that names Edit is fine, a refusal of a Bash command
that only reads the memory folder is not.

**No new numbered decision** (burndown). `decisions/patterns.md` is parked in
reserve (below), so this unit must not add to it in any case. Record the
behaviour in `spec.md` and `docs/contract.md` where the hook is described. A
real design fork goes to `scripts/fleet-linear.py file --from decision`.

**What you may change.** Only `embarch-promptu` and `embarch-doc/embarch-promptu/`.

**Doc reserve.** `embarch-promptu/decisions/patterns.md` is 11,138 of 12,288 B
(1,150 B left), filed against `tasks/promptu/008`, blocked. Leave that file
alone.

## Why now

The owner moved EMB-187 to Fleet Ready; the index checks are the reason the
memory hook exists, and this route skips all of them.

## Done when

- [x] A shell write into an auto-memory `MEMORY.md` gets the same index findings as an Edit, or a warning naming Edit.
- [x] A Bash command that only reads the memory folder gets nothing.
- [x] Tests cover both.
- [x] Gate green (`../../embarch-fleet/gate.md`); `changelog.d/` fragment dropped.

## Done

PreToolUse on Bash warns (any mode, never refuses) and names Edit when the command names a memory-folder `MEMORY.md` and looks like a write; reads get nothing. Reuses `claude::memory_target`. Spec and `docs/contract.md` §3.3a updated; no new decision. Limit: a script that builds the path at run time, or never names the index, is not seen. Hardware debt: none. A real session has not run this hook on Bash; the plugin needs the owner's reinstall for the new matcher.
