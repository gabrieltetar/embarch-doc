# 052 — 320 citations point at a `design.md` this repo no longer has

**State:** open
**Source:** supervisor, leg 059, 2026-09-09 — found while fixing the miscitation the `api/031`
reviewer filed
**Scope:** api
**Hardware:** none
**Owner:** no

## What

`embarch-api`'s docs were split into `spec.md` / `open.md` / `decisions.md` / `decisions/*` /
`interfaces/*`; **there is no `embarch-api/design.md` and there has not been for days.** A grep
across the `embarch-api` code repo (excluding `target/`) finds **320 occurrences of `design.md`**,
overwhelmingly in the form `design.md §N.N decision M` — comments in `src/`, `crates/`, and
`config.example.toml`.

This is the same defect `tasks/study-designer/018` swept out of its own repo on 2026-09-09, where
the count was **522 changed lines across 32 files** against a task filed for 290 in 23 — so expect
this one to be larger than the number above too, and expect occurrences outside `src/`
(`Cargo.toml`, `tests/`, `tools/`, `.github/workflows/`) that a `src/`-scoped grep never reaches.

**The section numbers did not survive the split**, so every `§N.N` in those citations has been
pointing at nothing. Nothing catches it: `check-decision-refs.py` reads markdown, not code-repo
comments, and `embarch-api` keeps `cargo doc` warnings out of its gate.

## The half that is worse than a dead pointer

`api/031`'s reviewer found a **live misattribution** hiding inside this convention, which is why
this task is worth more than a mechanical sweep. `config.example.toml`'s `probe_serial` comment
cited `design.md §3 decision 9` for probe ambiguity. That content is **`embarch-core`'s decision
9** (`embarch-core/decisions/probes.md`); `embarch-api`'s *own* decision 9 is about locked
dependency choices and is entirely unrelated. Dropping the repo qualifier did not produce a dead
link — it produced a citation to a **real, permanent, wrong decision.** Fixed in place at leg 059
(`embarch-api` `61e2b42`), and it is the only one anybody has checked.

**So this sweep is not a find-and-replace.** Every citation has to be resolved against the current
decisions index before its `design.md §N` prefix is stripped, exactly as `study-designer/018`'s
reviewer did by sampling: stripping the prefix off an already-wrong number leaves a wrong number
that now reads as authoritative. Cross-repo content cited without a repo qualifier is the specific
thing to hunt.

## Done when

- [ ] No `design.md` reference remains anywhere in the `embarch-api` repo — verified by a
      repo-wide grep at the merge SHA, not a `src/`-scoped one.
- [ ] Every citation touched was resolved against the current decisions index, and any that named
      another repo's decision now says which repo.
- [ ] The diff is comment-only where it touches `.rs` — the cheap structural proof is
      `git diff -U0 -- '*.rs' | grep` for changed non-comment lines returning nothing, which
      `study-designer/018` used and which this log recommends for any sweep this size.

## In flux: no
