# 021 — The weekly sheet opens with decision 15's numbers, a control beside each, and the owner's feel line

**State:** done — five numbers, control, null, feel line and read-only sheet.md built; spec.md out of reserve
**Source:** decision 15 (`decisions/learning.md`); `embarch-promptu` `docs/contract.md` §10 (`numbers`, `feel`) and §14.5 (the pack's records); the session events `week pack` writes (`promptu/016`); `week draft`'s `numbers()` (`src/draft.rs`, `promptu/017`)
**Issue:** EMB-278
**Scope:** promptu
**Hardware:** none
**Owner:** no

## What

Decision 15 says each weekly sheet reports whether Promptu works. `week draft`
computes three of its checks today (`fills_kept`, `patterns_kept`,
`questions_per_run`) and leaves the two friction checks out, because the
session events did not exist yet; `promptu/016` added them. When this is done:

- **All five checks are on the sheet**, each computed from the week's pack as
  contract §10 names them: `friction_per_prompt` (corrections per prompt,
  target at or below 0.10), `redirects_per_task` (redirected messages per task
  start, target down about 30% on the baseline), `fills_kept` (at least 0.90),
  `patterns_kept` (at least 0.85) and `questions_per_run` (falling). Where the
  drafter judges a candidate redirect (fork W2), count the ones it keeps; if
  the draft does not record a judgement per candidate, count the candidates
  and record that as a fork on a default.
- **A control beside the friction checks**: the same figure for the week's
  sessions not started with Promptu (a session event's `promptu: false`), in
  a new field on the number. The contract allows a new field (§11, "may
  grow"); name it in §10.
- **A check with no data that week is listed with a null value, not zero and
  not left out.** Contract §10 says "left out" today; amend that sentence to
  match and say so in your report.
- **`feel`** (`better`, `same`, `worse` or null) is shown on the sheet, empty
  until the owner sets it. If `week mark --feel` does not exist yet, the line
  still shows; setting it is `promptu/019`'s, or note in your report where it
  landed.
- **`sheet.md` opens with the numbers**, above the first group, marked
  read-only.

Where to start: `numbers()` and `sheet_md()` in `src/draft.rs`, the session
events in `src/weeksession.rs`, and `docs/contract.md` §10.

## Why now

The owner judges after four weeks whether Promptu works (decision 15), and
the sheet is where he reads it. The friction numbers were waiting on the
session events, which landed as `promptu/016`.

**Burndown leg: no new numbered decision.** Amend decision 15 in place if it
changes. Where the contract leaves a choice open, record it as a fork in
`docs/forks.md` on a default. If the work needs a new decision, stop and say
so in this file and in your report.

**Doc size, a dispatch note (supervisor):** `embarch-promptu/spec.md` is in
reserve (9,147 of 10,240 B, out of reserve at 9,039 B or less), filed as
`tasks/promptu/022`, `blocked` on `In flux: yes`. You are the unit making that
flux, so **bring `spec.md` out of reserve in this unit**: move its long status
paragraph to a file under `embarch-promptu/spec/` verbatim, leaving a one-line
summary and a link, then make your own status edit there. Carry
`promptu/022`'s `Must not delete:` (the step-by-step build status and its EMB
references). Say in your report what moved; I close `promptu/022` at the fold.
No other promptu file is in reserve.

## Done when

- [x] Each of the five checks has a fixture pack with a known answer, and a test.
- [x] The two friction checks carry a control figure from non-Promptu sessions, with a test.
- [x] A check with no data that week is null, not zero, and the contract says so.
- [x] `sheet.md` opens with the numbers and the feel line, marked read-only.
- [x] Gate green (`../../embarch-fleet/gate.md`), with `cargo test --all-targets` and `cargo clippy --all-targets -- -D warnings`.
- [x] `spec.md`/`decisions.md`/`interfaces.md` updated where they change, `changelog.d/` fragment dropped.

## Result

- All five checks computed from the pack in `numbers()` (`src/draft.rs`); the two friction checks carry `control` (non-Promptu sessions). Fork W22 (default: count every candidate redirect, since the drafter records no per-candidate judgement).
- Contract §10 amended: a check with no data is listed with `value: null` (was "left out"); `control` named; `feel` and the read-only `sheet.md` opening stated. `week mark --feel` already exists (promptu/019).
- Tests: `numbers_list_every_check...`, `friction_counts_promptu_sessions_and_a_control_apart`, `the_markdown_opens_with_the_numbers_and_the_feel_line` (unit, `src/draft.rs`).
- `spec.md` out of reserve: the status paragraph moved verbatim to `embarch-promptu/spec/status.md`; `promptu/022` closes at the fold.
