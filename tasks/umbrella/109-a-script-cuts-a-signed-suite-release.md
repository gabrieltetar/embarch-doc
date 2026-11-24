# 109 — A script cuts a signed suite release

**State:** done — script, fake-runner tests and topic file shipped; never run live
**Source:** `embarch-release-signing-proposal.md` — "One script cuts a release (`embarch-umbrella/scripts/`): checks the versions, tags each component that changed, waits for its CI, tags the suite, waits, downloads and verifies the result, and prints the elevated install command"
**Issue:** EMB-344
**Scope:** umbrella
**Hardware:** none
**Owner:** no

## What

A script under `scripts/` in this repo cuts a suite release, **dry run by
default**:

- For each component in `suite.toml`, compare its `Cargo.toml` version with
  its latest release tag; print the tags it would create and the `suite.toml`
  change.
- With `--go`: tag and push each changed component, wait for its release run
  (`gh run watch` or equivalent), and stop on a failure before anything later;
  rewrite `suite.toml` and stop for the owner to commit it; on a second run
  after that commit, tag the suite, wait, download the release, run `embarch
  verify-release` on it, stop if verification fails and say so, and print the
  elevated install line (`embarch install-core <release>`; the owner may
  rename that verb, so print it as the issue gives it).
- **Every `git` and `gh` call goes through one runner**, which the tests fake;
  no test touches the network, a real tag or a real repository.
- The script never approves the `release` environment's run; that click is the
  owner's, and it says so where it waits.

Python 3 with the standard library and `unittest` beside it is the cheapest
fit (`embarch-dev-bench/scripts/` is the precedent); a Rust binary is fine if
you prefer, but no new runtime dependency. Name the gate command you used in
this file, because this repo has had no script tests until now.

## Why now

The owner cuts the rehearsal release and the release the attested Core is
installed from by hand today (EMB-344).

**Burndown leg: no new numbered decision.** Say what the script does in the
spec and an `interfaces/` or `spec/` topic file; if a rule needs a decision
sentence, amend the existing entry in `decisions/release.md` in place. If the
work genuinely needs a new decision, stop and say so in this file.

**Doc-size reserve (dispatch note):** `embarch-umbrella/spec.md` is in reserve
(9,161 of 10,240 B, 1,079 B left) and its compaction, `tasks/umbrella/107`, is
parked on `In flux: yes`. Spend at most one line of `spec.md` naming the script
and pointing at the topic file that describes it, and write `spec.md`'s new
size in this file so the supervisor can update that park at the fold. Umbrella decisions near their
per-decision cap: prune-policy#26 (19 B), deploy#32 (29 B), mirrors#20 (32 B),
probe-vendors#49, sticky-host#48, budgets#44; none is this task's.

## Done when

- [x] With a fake runner, the dry run prints every command and runs none.
- [x] A component whose version equals its latest tag is skipped.
- [x] A failed component run stops the script before the suite tag.
- [x] A failed verification stops it and says so.
- [x] `spec.md` names the script; a topic file says how to run it.
- [x] Gate green (`../../embarch-fleet/gate.md`) plus the script's own tests,
      `changelog.d/` fragment dropped.

## Result

- Script: `scripts/cut-release.py` (Python 3.12 stdlib); doc: `interfaces/cut-release.md`.
- **Gate command for its tests:** `python3 -m unittest discover -s scripts -p 'test_*.py'` in `embarch-umbrella` (8 tests, fake runner).
- **`spec.md` is now 9,272 B of 10,240** (was 9,161; +111 B, one sentence). For `tasks/umbrella/107`'s park.
- No new decision; decision 14 untouched.
- **Debt:** never run against real `gh`/`git`; the first real cut verifies the `gh run list/watch/release download` argument shapes. `embarch install-core` is printed as the issue gives it.
