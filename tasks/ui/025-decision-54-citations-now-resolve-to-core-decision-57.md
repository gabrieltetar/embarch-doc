# 025 — `embarch-ui`'s "decision 54" citations now resolve to the wrong `embarch-core` decision

**State:** open
**Source:** `inbox/umbrella-ui-decision-54-renumbered-to-57.md`, dropped by the worker on
`core/039` and filed by leg 079. Split from that drop, which spanned two scopes; the `umbrella`
half is `tasks/umbrella/051`.
**Scope:** ui
**Hardware:** none
**Owner:** no

## What

`core/039` renumbered `embarch-core/decisions/surfaces.md`'s decision about
`EnrolledBoardResponse`'s label — "no persisted validation timestamp; the existing field gets an
honest label instead" — from **54** to **57**, because `embarch-core/decisions/flashing.md`
already held an unrelated decision 54 (`Backend::NrfJprog` retired).

Per `embarch-fleet/supervisor-log.md`'s 2026-09-10 17:35 entry (`ui/022`), two `embarch-ui` sites
cite "decision 54" for the same "Enrolled, not Validated" label:

- `src/snapshot.rs`
- `assets/app.js`, above `enrolledTableRows`

The `core` worker had no `embarch-ui` checkout, so those line references are unverified. Grep the
repo and `embarch-doc/embarch-ui/` for "decision 54" rather than trusting the two names, and leave
alone any citation that genuinely means `flashing.md`'s decision 54 — saying in the commit message
which you judged to be which.

## Why now

A bare "decision 54" now resolves ambiguously against `embarch-core`'s decisions, so a reader
following one from `ui` lands on a retired flashing backend rather than the label decision the
code is actually implementing.

## Done when

- [ ] `src/snapshot.rs` and `assets/app.js` citations say "decision 57" where they mean the label.
- [ ] Any other `ui`-scoped "decision 54" citation triaged, with the judgement recorded.
- [ ] `cargo build` / `test` / `clippy --all-targets -- -D warnings` green in `embarch-ui`.
