# 007 — Promptu rewrites the rough prompt and keeps the original in its log

**State:** done on agent/promptu/007-rewrite-the-rough-prompt-and-log-the-original, 2026-11-17; pushed, not merged
**Source:** EMB-196, the build of `embarch-promptu` decision 42 (owner, 2026-11-17)
**Issue:** EMB-196
**Scope:** promptu
**Hardware:** none
**Owner:** no

## What

Today the pass picks a pattern, the dialog asks what is missing, and `render`
puts the rough prompt verbatim under Goal with the answers in the other five
sections (decision 9). A pasted brief keeps its text and gets only its gaps
answered (decision 24). Nothing is stored beyond the footer and the last answers
(decisions 13 and 27). The weekly loop compares the owner's edits against that
rendered prompt (decision 14).

Decision 42 (`decisions/patterns.md`) changes that. Build it:

- After the last question, Promptu writes a better prompt from the rough text,
  the answers and the plan, and that rewrite is what lands in the draft.
- The original rough prompt is kept in Promptu's log, one entry per run, beside
  the last answers in the state folder, and **one CLI verb prints it for a given
  run**. `embarch-chat`'s card (EMB-197, the next unit) calls that verb to
  restore the draft, so state its name, arguments, output and exit codes in
  `interfaces.md`.
- A pasted brief (`mode=brief`) is not rewritten: decision 24 stands for it.
- The weekly loop's edit signal compares the owner's edits against the rewrite.
- The footer says the prompt was rewritten, so a reader of the draft can tell.

Where to look: `src/run.rs` (rendering), `src/pass.rs` and `src/pass_system.md`
(what the pass returns), `src/state.rs` (the state folder), `src/footer.rs`, and
`embarch-doc/embarch-promptu/interfaces.md`.

**Which model rewrites and the wait after the last question are open in
decision 42, and stay the owner's.** Make the model a setting with a sensible
default, and record the model and the wait for each run where the build can
report them (the log entry is the natural place). Measuring p50 and p95 over at
least ten real prompts needs real `/promptu` runs, which this unit cannot make:
leave a command or a log query that computes both, and write the measurement
here as owed, owner-side.

**Burndown leg: no new numbered decision.** Decision 42 is the decision; record
the verb, the log's shape and the footer wording in `spec.md` and
`interfaces.md`. A design fork decision 42 does not settle is filed with
`scripts/fleet-linear.py file --from decision`, and you take the narrower
reading. Decisions 9 and 24 are amended by 42 already; if their text still
reads as current, add the "amended by 42" pointer, nothing more.

**What you may change.** Only `embarch-promptu` and `embarch-doc/embarch-promptu/`.

**Doc reserve.** Nothing of `embarch-promptu`'s is in reserve.

## Why now

The owner moved it to Fleet Ready with EMB-197, which depends on its CLI verb.

## Done when

- [x] A rough prompt run through the pass lands in the draft rewritten, and a pasted brief lands with its text unchanged; tests cover both.
- [x] Each run's original is in Promptu's log, and one CLI verb prints it for a given run; the verb is in `interfaces.md`.
- [x] The weekly loop's edit input is the diff between the rewrite and what was sent.
- [x] Each run records which model rewrote and the wait after the last question, and a command prints p50 and p95 over the logged runs; the real-prompt measurement is written here as owed.
- [x] Gate green (`../../embarch-fleet/gate.md`); `changelog.d/` fragment dropped.

## Built

- `embarch-promptu` `src/rewrite.rs` (call, cleaning, p50/p95), `src/rewrite_system.md`, `prep::render` (the rewrite, never fatal), `state::LogEntry` (`log/<run>.json`, never pruned), config keys `rewrite`, `rewrite_model` (default `sonnet`), `rewrite_effort` (`low`), `rewrite_timeout_s` (30).
- Verbs: **`promptu original <run> [--json]`** (stdout = the original as typed, exit 0; exit 2 for no entry), **`promptu stats [--model] [--json]`**. Contract §8.4–§8.6; `interfaces.md` states the read-back verb for EMB-197.
- Footer: `rewritten=yes`, last field, after `mode` and `way`. A brief, a run with no pattern, an offline run and `rewrite = "off"` are not rewritten; a failed call leaves the structured render with his words under Goal and the reason in the log (`rewrite_skipped`).
- Weekly loop (step 4, not built): its edit baseline is the log's `rendered`, the text that landed (the rewrite when there is one). Nothing in the repo reads edits yet, so the done-when is met as the contract the loop will read, not as running code.
- Tests (`tests/prompts.rs`): a rough prompt lands rewritten with its original in the log and read back by the verb; a brief lands unchanged with no second call; a failed rewrite falls back; unknown run exits 2; `stats` p50/p95. The shared scratch config sets `rewrite = "off"` so the earlier tests still pin the verbatim render.
- No design fork needed filing; the narrower reading taken: the log entry is written at `render` (a run never rendered has none), and `wait_ms` is the `render` command's own duration.

## Owed, owner-side (hardware: none)

- **The ten-real-prompt measurement.** This unit could not run real `/promptu` sessions. Run at least ten real prompts through the plugin, then `promptu stats` (add `--model <name>` per candidate; change `rewrite_model` in `config.toml` to compare). Pick the model and the acceptable wait after the last question from the p50 and p95 it prints, then record the pick as an amendment to decision 42. Keep the numbers outside the public repos (`embarch-promptu` CLAUDE.md).
- **Not installed or run against the real Sonnet.** The fake `claude` pins the call's shape; the real model's rewrite quality is unseen.
- The chat card (EMB-197) is unbuilt: it must call `promptu original <run>` to roll back.
- No `features.d/` row: `features.d/README.md` lists no `promptu` scope, so none was written.
