# 051 — `embarch-umbrella`'s "decision 54" citations now resolve to the wrong `embarch-core` decision

**State:** open
**Source:** `inbox/umbrella-ui-decision-54-renumbered-to-57.md`, dropped by the worker on
`core/039` and filed by leg 079. Split from that drop, which spanned two scopes; the `ui` half is
`tasks/ui/025`.
**Scope:** umbrella
**Hardware:** none
**Owner:** no

## What

`core/039` renumbered `embarch-core/decisions/surfaces.md`'s decision about
`EnrolledBoardResponse`'s label — "no persisted validation timestamp; the existing field gets an
honest label instead" — from **54** to **57**, because `embarch-core/decisions/flashing.md`
already held an unrelated decision 54 (`Backend::NrfJprog` retired). Citations of the surfaces
meaning must now say 57.

Two live in `umbrella`'s scope:

- `tasks/umbrella/045-relabel-confirmed-at-utc-ms-if-doctor-ever-renders-it.md` — its state note
  and a `Done when` line both say "decision 54".
- `embarch-umbrella/src/doctor.rs`'s module doc comment, into which that task records the same
  reasoning being folded. Check it and fix it if it cites 54.

Search the whole of `embarch-umbrella` and `embarch-doc/embarch-umbrella/` for "decision 54" —
these two are what the `core` worker could see, not necessarily all of them. Leave any citation
that genuinely means `flashing.md`'s decision 54 alone, and say in the commit message which you
judged to be which.

## Why now

A bare "decision 54" in this repo now resolves ambiguously: `flashing.md` still has its own,
unrelated decision 54, so a reader following the citation lands on a retired flashing backend
instead of a label decision. That is the exact collision `core/039` closed inside `embarch-core`'s
own docs, left open one repo over.

## Done when

- [ ] `tasks/umbrella/045-...md`'s citations say "decision 57".
- [ ] `embarch-umbrella/src/doctor.rs`'s doc comment checked, and corrected if it cited 54.
- [ ] Any other `umbrella`-scoped "decision 54" citation triaged, with the judgement recorded.
- [ ] `cargo build` / `test` / `clippy --all-targets -- -D warnings` green in `embarch-umbrella`.
