# 021 — The weekly sheet opens with decision 15's numbers, a control beside each, and the owner's feel line

**State:** open
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

## Done when

- [ ] Each of the five checks has a fixture pack with a known answer, and a test.
- [ ] The two friction checks carry a control figure from non-Promptu sessions, with a test.
- [ ] A check with no data that week is null, not zero, and the contract says so.
- [ ] `sheet.md` opens with the numbers and the feel line, marked read-only.
- [ ] Gate green (`../../embarch-fleet/gate.md`), with `cargo test --all-targets` and `cargo clippy --all-targets -- -D warnings`.
- [ ] `spec.md`/`decisions.md`/`interfaces.md` updated where they change, `changelog.d/` fragment dropped.
