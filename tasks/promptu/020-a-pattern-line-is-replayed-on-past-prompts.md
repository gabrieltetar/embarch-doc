# 020 — A pattern line that changes a question, a signal or a source is replayed on past prompts

**State:** open
**Source:** decisions 14 and 47 (`decisions/learning.md`); `embarch-promptu` `docs/contract.md`'s sheet lines; the sheet `week draft` writes (`promptu/017`)
**Issue:** EMB-281
**Scope:** promptu
**Hardware:** none
**Owner:** no

## What

Decision 47 tests a proposed pattern by re-rendering its examples and
replaying 3 to 5 real past prompts, old pattern against new, before the owner
approves it. `week draft` checks a proposed pattern with `promptu lint` and
writes example renders, and replays nothing. When this is done:

- For a pattern line that changes a question, a signal or a source, the pass
  runs on three to five past rough prompts of that pattern (the log's
  `original`), once with the old pattern file and once with the new, and the
  two results are written side by side in the week folder and linked from the
  line.
- A template-only change renders without a model, so it gets no replay.
- A setting caps the replay's cost per week, and a line the cap stopped says so.
- Past prompts are read from the log only; nothing leaves the state folder.

Where to start: `src/pass.rs` `call_model` (the pass), `src/state.rs`
`all_logs` (past rough prompts), `src/pattern.rs` `Set::from_dir` (loading a
pattern set from a folder, as `PROMPTU_PATTERNS` does), and `src/draft.rs`
(where a sheet's pattern lines are written). Tests use a fake `claude`, as
`promptu/017`'s do.

## Why now

`week draft` landed as `promptu/017`; the owner reads a replay before he
approves a pattern line.

**Burndown leg: no new numbered decision.** Amend decision 47 in place if it
changes. Where the contract leaves a choice open (which past prompts are
picked, the cap's default), record it as a fork in `docs/forks.md` on a
default. If the work needs a new decision, stop and say so in this file and in
your report.

## Done when

- [ ] With a fake `claude`, a question change yields a side-by-side file per replayed prompt; a template-only change yields none.
- [ ] The cap stops the replay and says so on the line.
- [ ] Past prompts are read from the log only; nothing leaves the state folder.
- [ ] Gate green (`../../embarch-fleet/gate.md`), with `cargo test --all-targets` and `cargo clippy --all-targets -- -D warnings`.
- [ ] `spec.md`/`decisions.md`/`interfaces.md` updated where they change, `changelog.d/` fragment dropped.
