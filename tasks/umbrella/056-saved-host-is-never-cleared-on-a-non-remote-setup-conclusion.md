# 056 — `saved.host` outlives the run that gave it, and whether `apply_plan` should drop it is unsettled

**State:** claimed by agent/umbrella/056-saved-host-clearing, 2026-09-12 01:21
**Source:** `embarch-umbrella/open.md` — "**`saved.host` is still never cleared on a non-`remote`
`setup` conclusion** (decision 48 in `decisions/sticky-host.md`): an old `--host` can outlive the run
that gave it. … whether `apply_plan` should drop it on a `local`/`wsl-host` conclusion is not
[settled]."
**Scope:** umbrella
**Hardware:** none for the decision and the code. The bullet's own "verify on a real machine" note
covers end-to-end confirmation only, and that half is **not** this task.
**Owner:** no

## What

Decision 48 made `--host` sticky, which is right for the `remote` case it was built for. What it
did not settle is the other direction: a run that concludes `local` or `wsl-host` leaves a
previously-saved `host` in place, so a stale `--host` from an earlier session can outlive the run
that produced it and steer a later one.

**Settle it either way and record why.** Both answers are defensible — clearing it means a sticky
value is only ever as old as the last remote conclusion; keeping it means a user who alternates
machines does not retype. What is not defensible is leaving it unstated, because the current
behaviour is an accident of where the write is rather than a call anyone made.

## Why now

It is a one-branch change in `apply_plan` guarded by a unit test over the state transition, and it
is the kind of stale-configuration bug that presents as "setup picked the wrong machine" — which
reads as a detection defect rather than a persistence one. `embarch-umbrella` has three decision
files on the topic already, so there is a home for the record.

## Done when

- [ ] `apply_plan` either clears `saved.host` on a `local`/`wsl-host` conclusion or explicitly
      keeps it, and **which, and why, is a numbered decision** in `decisions/sticky-host.md`.
- [ ] A unit test covers the state transition in both directions — a `remote` run that saves, and a
      subsequent non-`remote` run — so the chosen behaviour cannot regress silently.
- [ ] `embarch-umbrella/open.md`'s bullet is struck.
- [ ] `cargo build` / `test` / `clippy --all-targets -- -D warnings` green; gate green;
      `changelog.d/` fragment.

**Reserve note:** `embarch-umbrella/decisions/bind.md` is at 93.2% behind a blocked compaction task
(`tasks/umbrella/009`). Do not relocate text into it; if this work spends a reserve, file
`tasks/umbrella/<NNN>-compact-umbrella.md` in the same commit.
