# 048 — Two supervisor legs ran concurrently, took the same three units, and nothing detected it

**State:** open
**Filed:** from `inbox/` by leg 096, 2026-09-12, unchanged apart from this line and the number.
**Source:** leg 084, 2026-09-12 ~01:32–02:05, observed first-hand. Leg 084 and leg 085 were alive at
the same time; leg 084 stood down when it worked out what was happening.
**Scope:** doc
**Hardware:** none
**Owner:** required — the fix is in `.claude/` and/or `scripts/`, both owner-reserved.

## What happened

Leg 084 ran step 0 clean: no registered `leg` worktree, no `agent/*` branch on any remote, no
`**State:** claimed` task. It claimed `api/075`, `topology/033` and `ui/032` (three separate claim
commits, each pushed to `origin/main` before dispatch — `483d1d4`, `d720bd4`, `bbf15e1`), created
the worktrees, dispatched three workers, and started the rolling wave.

**Leg 085 then landed and folded all three of those units.** `origin/main` carries
`46cebf2` (topology/033 fold), `4a21b47` (api/075 fold) and `ff95079` (ui/032 fold), plus
`8f34c04`/`2c7c68f` filing and claiming `ui/033` from an inbox drop leg 084's ui worker had just
written. The `supervisor-log.md` entries for all three are leg 085's.

**Nothing was lost and nothing was double-folded.** Each fragment was consumed exactly once,
`history/topology.md` has one entry, and the three log entries are correct. That is luck plus the
fold's own `--only`/`--path` discipline, not a property of the design.

## How leg 084 found out

Not by any check. By a branch appearing on a remote — `agent/ui/033-design-md-comments`, a unit it
had never claimed — and by its own `inbox/` contents changing underneath it. It accused its own ui
worker first; the worker correctly denied it and listed exactly what it had pushed.

## Why the existing interlocks did not fire

1. **The claim commit is a double-*dispatch* interlock, not a double-*supervisor* one.** Leg 085
   did not re-dispatch the claimed tasks — it adopted the pushed branches, which `leg.md`'s own
   positive-presence rule explicitly permits ("a branch present on its remote carrying commits
   means that worker finished — you may gate and land it"). Every step leg 085 took was legal.
2. **Step 1's evidence-on-disk check is a point-in-time read.** Leg 084 passed it because leg 085
   had not started yet. Nothing re-checks, and `ListAgents` — the listener's check — is not
   available to a leg.
3. **Both legs use the same hard-coded worktree path**, `.worktrees/embarch-doc/leg`. Leg 084 left
   an uncommitted fold there and found it reset under it. Two supervisors in one working tree is
   precisely the hazard `--detach` and the separate leg worktree exist to prevent, applied to the
   owner's checkout but not to each other.

## Candidate fixes (the owner picks)

- **A supervisor lock file.** `.fleet/supervisor` written with the leg number and pid at step 0,
  refused if one exists and its pid is live, removed at exit. Cheap, and the pid makes it exact the
  same way `tasks/README.md` makes claim staleness exact.
- **Per-leg worktree path** — `.worktrees/embarch-doc/leg-<NNN>` — so two legs cannot share a tree
  even if both start. Fixes the data hazard without fixing the duplication.
- **Make the claim commit say who holds it and have a leg respect it.** The claim line already
  carries `leg 084`; nothing reads it. A leg that found a claim naming a *different* leg number
  could stop instead of adopting.
- **Find out why the listener spawned a second leg at all**, which is the actual root cause and is
  not visible from inside a leg. `.fleet/tick.log` shows `listener` entries at 01:49:19 and
  02:01:31 interleaved with leg 084's `leg-waiting` ticks.

## Done when

- [ ] A second supervisor cannot start while one is live, or cannot silently take a live leg's
      claimed units if it does.
- [ ] The check is one a leg can actually run — `ListAgents` is not available to it.
- [ ] Whatever causes the listener to spawn a second leg over a live one is named, even if the fix
      is elsewhere.
