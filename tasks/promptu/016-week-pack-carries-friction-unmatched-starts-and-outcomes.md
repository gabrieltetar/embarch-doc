# 016 — `promptu week pack` carries friction, unmatched starts and outcomes

**State:** done — week pack builds session, unmatched, outcome and carried events; fork W16
**Source:** decisions 14 and 15 (`decisions/learning.md`); `embarch-promptu` `docs/contract.md`'s pack records (written by `promptu/011`, built by `promptu/013`)
**Issue:** EMB-274
**Scope:** promptu
**Hardware:** none
**Owner:** no

## What

Decision 14 learns from friction in sessions, from task starts no pattern
matched, and from outcomes, not only from rendered runs. `promptu/013` built
`week pack` with one record per rendered run, and left the session, unmatched,
outcome and carried counts at 0 until this unit. When this is done, the pack
also carries, for every session in the window:

- **Friction**, as the contract defines it: at least a plan the owner
  rejected, and an interrupt followed by a real next prompt (not "continue",
  "go" or "yes"). Each event keeps the follow-up text, for the drafter to
  label.
- **Unmatched task starts**: a session's first owner prompt with no footer, or
  with `— promptu none`.
- **Outcome**: a commit in the session or in one of its subagents.
- **Whether the session started with Promptu**, so decision 15 can compare
  corrections per prompt against the sessions that did not.

Where to start: `src/calls.rs` (reading a session and its subagents' tool
calls; its `git` class has no commit yet), `src/used.rs` `footers` (what counts
as an owner's message), and the pack's session records in `docs/contract.md`.
Fill the counts `promptu/013` left at 0 and say in the contract where they now
come from.

## Why now

The weekly drafter (`promptu/017`) and decision 15's numbers both read these
events. `week pack`'s run records landed as `promptu/013`.

**Burndown leg: no new numbered decision.** Where the contract leaves a choice
open, record it as a fork in `docs/forks.md` on a default, as `promptu/011` and
`promptu/013` did. If the work needs a new decision, stop and say so in this
file and in your report.

## Done when

- [x] Each event kind has an invented transcript fixture and a test.
- [x] A commit made by a subagent counts as its session's outcome.
- [x] Each session in the pack says whether it started with Promptu.
- [x] The pack still makes no model call and no network call.
- [x] `docs/contract.md`'s session records match what the pack writes.
- [x] Gate green (`../../embarch-fleet/gate.md`), with `cargo test
      --all-targets` and `cargo clippy --all-targets -- -D warnings`.
- [x] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment
      dropped.
