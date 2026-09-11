# 064 — `surface.md` decision 67 cites `release.md` for decision 14, which lives in `install.md`

**State:** open
**Source:** `embarch-reviewer`, during leg 082's `tasks/suite/019` review, 2026-09-11. Filed to
`inbox/` by the reviewer and numbered into the queue by that leg. **The reviewer's own header said
it was spawned by an owner-session review pass; it was not — it was spawned by the supervisor
alongside a supervisor-executed `suite` unit.** Corrected here rather than left, because a task's
`Source:` is how a later reader judges how much weight the finding carries.
**Scope:** api
**Hardware:** none
**Owner:** no

## What

`embarch-api/decisions/surface.md` decision 67 (already landed, not part of `suite/019`'s
diff) cites `embarch-umbrella/decisions/release.md` for the claim that "the suite's own release
workflow does not ship" `embarch-ui`. That file is the wrong target: `embarch-umbrella`'s own
`decisions.md` index lists decision 14 (the suite release archive) under
`decisions/install.md`, not `decisions/release.md` — confirmed by reading `release.md` in full,
which holds only decisions 1, 2, 27, 29. `suite/019` (uncommitted at review time) was about to
repeat the identical wrong path in a new bullet it added to `embarch-ui/open.md`; that one was
caught and corrected before landing, but decision 67's own citation, already merged, was not
fixed by that unit and is out of its scope.

## Why now

A reviewer reading `suite/019`'s diff traced the citation to verify a different claim and found
the pattern already present upstream. Left uncorrected, the next doc that cites "the suite
release archive" via decision 67's own wording is likely to copy the same wrong path forward
(exactly what nearly happened here).

## Done when

- [ ] `embarch-api/decisions/surface.md` decision 67's `(embarch-umbrella/decisions/release.md)`
      parenthetical points at `embarch-umbrella/decisions/install.md` instead.
- [ ] A quick grep for `embarch-umbrella/decisions/release.md` elsewhere in the suite for the
      same mis-citation (decision 14 specifically) turns up nothing else.
