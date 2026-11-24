# 023 — A plugin skill walks the weekly sheet in the terminal for a user without the Desk

**State:** done — plugin/skills/review (typed /embarch-promptu:review), plugin 0.4.0, contract, README, fork W21, decision 30 amended
**Source:** decisions 29 and 30 (`decisions/learning.md`); `embarch-promptu` `docs/contract.md` §10 and §14.4; `week show`, `week mark` and `week apply` (`promptu/014`, `promptu/019`)
**Issue:** EMB-280
**Scope:** promptu
**Hardware:** none
**Owner:** no

## What

Decision 30 promises a skill that walks the weekly ✓/✕ sheet in the terminal
when the Desk is not there. When this is done, the plugin carries it:

- **A plugin skill, run only when typed** (`disable-model-invocation: true`).
  It reads `promptu week show --json`, puts each group's lines on
  `AskUserQuestion` pages (✓ or ✕, and a note), records each answer with
  `promptu week mark`, asks the feel line (`better`, `same`, `worse`), then
  runs `promptu week apply` and shows what applied and what failed.
- **Its name, as the contract fixes it.** Decision 30 calls it
  `/promptu:review`, but the plugin is `embarch-promptu`. Pick the name the
  plugin actually exposes, write it into the contract, and amend decision 30
  in place.
- **Its `allowed-tools` lists only the `promptu week` commands it runs.** A
  missing binary or a failing command is one line, and the skill stops
  without changing anything.
- **The plugin's version is bumped** and its description names the skill.
- **`README.md`** says how to review a sheet without EmbArch.

Where to start: `plugin/skills/promptu/SKILL.md` (the existing skill's
frontmatter, `allowed-tools` and fail-open rule),
`plugin/.claude-plugin/plugin.json`, and `README.md`.

## Why now

`week mark` and `week apply` landed as `promptu/019`, so the skill has
commands to call. EMB-85's chat card may open this skill on a waiting sheet.

**Burndown leg: no new numbered decision.** Amend decision 30 in place. Where
the contract leaves a choice open, record it as a fork in `docs/forks.md` on a
default. If the work needs a new decision, stop and say so in this file and in
your report.

**Doc size:** `embarch-promptu/spec.md` is in reserve (9,074 of 10,240 B),
filed as `tasks/promptu/022`, blocked. Keep any `spec.md` edit to a few words;
if you must add more, move the long status paragraph to `spec/` verbatim in
this unit, carrying `promptu/022`'s `Must not delete:` list, and say so.

## Done when

- [x] The skill's `allowed-tools` lists only the `promptu week` commands it runs.
- [x] A missing binary or a failing command is one line, and the skill stops without changing anything.
- [x] The plugin's version is bumped and its description names the skill.
- [x] The README says how to review a sheet without EmbArch.
- [x] Gate green (`../../embarch-fleet/gate.md`), with `cargo test --all-targets` and `cargo clippy --all-targets -- -D warnings`.
- [x] `spec.md`/`decisions.md`/`interfaces.md` updated where they change, `changelog.d/` fragment dropped.
