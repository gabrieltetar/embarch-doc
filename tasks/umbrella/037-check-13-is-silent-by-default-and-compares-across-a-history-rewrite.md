# 037 — Check 13 is silent by default on the only bench the suite has, and its comparison cannot survive a history rewrite

**State:** claimed by agent/umbrella/037-check-13-baseline, 2026-09-07 17:38
**Source:** `tasks/umbrella/034`'s bench run, leg 030, 2026-09-07 — the run that closed decision 44's budget debt found two things the debt was hiding
**Scope:** umbrella
**Hardware:** none for the reasoning and the fix; a bench confirms it in one `doctor` run
**Owner:** no

## What

Two independent defects in `doctor` check 13, both measured on the primary `wsl-host` bench with
both boards attached, enrolled and validated.

**1. It never compares anything unless an environment variable is set.** `dev_bench_repo_path` is
`Option<PathBuf>` in `state::State`, `dev_bench_repo_path()` falls back to it from
`EMBARCH_DEV_BENCH_REPO_PATH`, and **nothing in `setup` or `init` ever writes it**. On this machine
the checkout is at `/home/gabriel/Github/embarch/embarch-dev-bench` — two directories from the
binary — and check 13 prints:

    [13] WARN dev-bench firmware matches the local checkout — skipped — no embarch-dev-bench checkout configured

So the check that exists to catch "you changed dev-bench firmware and haven't reflashed it" is a
`warn` on every default install, and has been for its whole life. It reached that arm only because
`umbrella/030` fixed the handshake budget; before that it never got past `HelloOutcome::Unavailable`,
which is why weeks of "check 13 needs a bench" was measuring the wrong thing twice over.

**2. With the override set, the comparison it makes cannot be satisfied.** It is a `FAIL`:

    dev-bench reports firmware_version '49958d34', but /home/gabriel/Github/embarch/embarch-dev-bench is at 'd599453d'

**`49958d34` is not a commit in that repository** — not among its 27 commits, not a tag, not in any
reflog, and its history begins 2026-07-30. The flashed firmware was built from a checkout whose
history no longer exists; the 2026-09-04 client-name scrub is the obvious candidate and is not
proven here. So check 13 compares two `git describe --always --dirty --abbrev=8` values across a
rewrite, and after any rewrite every previously flashed board reads as mismatched forever. Its fix
line — rebuild and reflash — is the only action that clears it, which is the right instruction and
says nothing about why.

## Why now

`decisions/doctor.md` decision 19 states check 13's purpose as catching a mismatch "instead of as a
confusing mid-study failure". As shipped it catches nothing by default, and when it does catch
something it cannot distinguish *stale firmware* from *firmware whose commit was rewritten out of
existence* — and those need different actions from the operator.

## Candidate direction, not a decision

- Have `setup` record `dev_bench_repo_path` when it can see a checkout, or have check 13 say
  *"configured nowhere"* as a `fail`-with-fix rather than a `warn` that reads as "nothing to see".
  **Which of those is right is a judgement**: a machine with no bench should not be nagged.
- Distinguish "not a commit in this repo" from "an older commit in this repo". `git cat-file -e` on
  the reported id answers it in one call, and the two cases want different fix lines. That is the
  half that would have made this run's own result readable without a manual investigation.
- **`decisions/doctor.md` has ~940 bytes and its compaction task (`tasks/umbrella/009`) is blocked
  on `In flux: yes`.** If this unit's decision belongs there, `DOC-COMPACTION.md` §2's ride-along
  applies, and a mission split is this sub-project's established move — `decisions/budgets.md` was
  split off exactly that file on 2026-09-06.

## Supervisor's note, leg 040 — the doc reserve, and the ride-along you are owed

`embarch-umbrella/decisions/doctor.md` is at **11,346/12,288 B — 942 B left**, and its compaction
task `tasks/umbrella/009` is **blocked on `In flux: yes`**. So the reserve is parked but the *file*
is not: your decision almost certainly belongs there, and 942 B will not hold an argued one.

**`DOC-COMPACTION.md` §2's ride-along applies to you, and a mission split is this sub-project's
established move — prefer it over squeezing.** `decisions/bind.md` (2026-09-06, `umbrella/020`),
`decisions/integration.md` (`umbrella/022`) and `decisions/budgets.md` were all split off exactly
this file, each time on the reasoning that **a verbatim split restates nothing, so `In flux: yes`
cannot forbid one**. Decision 42 alone is ~4.9 KB. If a clean seam exists — check 13's firmware-
freshness mission is a plausible one — cut it verbatim into a new topic file and put your decision
there, and say in the commit message which seam you cut and why. **Check the seam before you cut
it**: `grep` the whole suite for inbound links to the decisions you are moving, and do not move one
whose inbound links live in a repo you may not edit. That is the exact mistake `umbrella/022`
avoided by hand.

**If you genuinely cannot find a seam, then compact `decisions/doctor.md` as part of this unit**,
carrying `tasks/umbrella/009`'s `Must not delete:` list — read it in full, it is long and specific
— and close **only** that file's item there, leaving the parked pass and the other three files
alone. Do not flip `umbrella/009`'s `In flux:` field to make the queue move.

`embarch-umbrella/open.md` (4400/5120, **720 B left**) and `spec.md` (9257/10240, **983 B left**)
are also in reserve, filed against the **open** `tasks/umbrella/038`, so file no new debt for those
two — but they are tight and this task's `Done when` asks you to write both. Budget for it.

### Two more things

- **`Hardware: none for the reasoning and the fix.`** Do not attempt a `doctor` run against the
  live bench, and do not treat the absence of one as a gap you must close — the two defects were
  already measured on the primary `wsl-host` bench and both are quoted verbatim above. Your unit is
  the reasoning, the fix and the decision.
- **The "candidate direction" section is deliberately not a decision**, including the judgement it
  names — *a machine with no bench should not be nagged*. Argue it and choose; do not treat the
  bullet as an instruction.

## Done when

- [ ] Check 13 either compares on a default install or says, in a status an operator reads as
      actionable, that it has no baseline configured — with the choice argued in a decision.
- [ ] A reported firmware id that resolves to no object in the checkout is reported as that, not as
      an ordinary mismatch.
- [ ] `spec.md`'s check table row and `open.md`'s bullet updated; `features.d/umbrella-080` too.
- [ ] Gate green; `changelog.d/umbrella-*` fragment.
