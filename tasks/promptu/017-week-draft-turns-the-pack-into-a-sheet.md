# 017 — `promptu week draft` turns the week's pack into a ✓/✕ sheet

**State:** done — week draft built: fake-claude sheet, lint-checked proposed patterns, failed lines, no tools; forks W13-W15
**Source:** decisions 14 and 30 (`decisions/learning.md`); `embarch-promptu` `docs/contract.md` §10, the sheet (written by `promptu/011`)
**Issue:** EMB-276
**Scope:** promptu
**Hardware:** none
**Owner:** no

## What

Decision 14's weekly sheet needs one model call that turns the week's pack
into proposals. When this is done, `promptu week draft` makes that call and
writes the sheet:

- **The call**: a stripped `claude -p` like the pass's, with the drafter's
  model (Opus in decision 14) and its time limit as config keys. No tools and
  no MCP servers, as the pass runs.
- **The rules it drafts by**, from decision 14: every event becomes a
  proposal; identical proposals stack into one line with a count; a specific,
  stable fact becomes a memory entry with its kind, domain and index line,
  never a pattern change; an event that needs no change still gets a line,
  marked cut, with the reason.
- **What Promptu writes from the reply**: `sheet.json` (contract §10),
  `sheet.md`, and a proposed copy of each pattern a line changes.
- **Checks on each proposed pattern**: `promptu lint`, and its examples
  rendered with the old and the new file, side by side in the week folder.

Where to start: `src/pass.rs` (`Call`, `argv`, `call_model`: the stripped call,
its environment, and `PROMPTU_CLAUDE` for tests), `src/rewrite.rs` (the most
recent model call built on it), `src/lint.rs` `lint`, and `tests/prompts.rs`
(the fake `claude` the tests use).

Build the pack fixture by hand in the contract's shapes. `promptu/016` adds
event kinds to the pack; read any it has landed on `origin/main` when you start,
and do not depend on the rest.

## Why now

The owner reviews this sheet every Wednesday (decision 14), and users without
the Desk read the Markdown sheet (decision 30). `week apply` (EMB-279), `week
run` (EMB-277) and the replay check (EMB-281) all wait on it.

**Burndown leg: no new numbered decision.** Where the contract leaves a choice
open, record it as a fork in `docs/forks.md` on a default. If the work needs a
new decision, stop and say so in this file and in your report.

## Done when

- [x] With a fake `claude`, a fixture pack yields a `sheet.json` that matches
      contract §10, a `sheet.md`, and the proposed files.
- [x] A proposed pattern that fails lint, or a line naming an unknown pattern
      or question, stays on the sheet with status `failed` and its error.
- [x] A failed or timed-out call writes no sheet and exits non-zero with one
      line on stderr.
- [x] The call runs with no tools and no MCP servers, as the pass does.
- [x] Gate green (`../../embarch-fleet/gate.md`), with `cargo test
      --all-targets` and `cargo clippy --all-targets -- -D warnings`.
- [x] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment
      dropped.

## Done

Built in `embarch-promptu`: `src/draft.rs`, `src/draft_system.md`, `tests/draft.rs`, config keys `week_model` (default `opus`), `week_effort`, `week_timeout_s`. Contract §14.4 and forks W13 (reply shape; a missing target or failed lint stays `failed`, a broken line is dropped), W14 (a `no-change` line starts cut), W15 (carrying earlier lines waits for the pack's `carried` events). No new numbered decision.

**Not built, by design:** `check.replay` is `[]` (EMB-281); carried lines and the friction `numbers` wait for EMB-274; `week_checkout`/`apply` are EMB-279. **Not tested:** the timeout path of `week draft` itself (`week_timeout_s` cannot go below 60 s); it is `pass::call_model`'s, covered by `tests/prompts.rs`. **Unmeasured:** a real Opus reply; the drafter's system prompt is untried against a model. No hardware-verification debt. `016` had not landed; the pack fixture is hand-built from `run` events.
