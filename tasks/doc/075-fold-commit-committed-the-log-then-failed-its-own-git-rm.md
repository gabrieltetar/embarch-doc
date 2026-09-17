# 075 — `fold-commit.py` committed the log and then failed its own `git rm`, leaving the log-only commit it documents as impossible

**State:** open
**Source:** `dev-bench/034` (leg 131, 2026-09-17). Reproduced twice in one unit; recovered by hand.
Filed from `inbox/` by leg 132.
**Scope:** doc
**Hardware:** none — a Python script's ordering. Nothing is built, no board, no probe, no live Core.
**Owner:** required — the fix is in `scripts/fold-commit.py`, and `scripts/` is owner-reserved. A
supervisor that reorders the script guarding its own folds has no guard, so this is filed rather
than fixed.

## What

`.claude/leg.md` states the invariant plainly:

> the script settles every path *before* it commits the log, so a bad path list now costs nothing
> instead of leaving a log-only commit to undo by hand

**It did not hold.** Sequence, exactly as it happened:

1. **First attempt**, `--path history/dev-bench.md --path changelog.d/...` (task file **not** in the
   list). Refused with the state check — *"this fold says dev-bench/034 landed, but
   tasks/dev-bench/034-...md still says `claimed`"* — and said *"Nothing has been written."* That
   refusal was correct, useful, and clean. The worker had left its own `State:` line at `claimed`.
2. I edited the state line to `done` in the working tree.
3. **Second attempt**, same message, task file now **added** to `--path`. It failed with:

   ```
   git rm -q -- tasks/dev-bench/034-...md failed in .../leg:
   error: the following file has local modifications:
       tasks/dev-bench/034-...md
   (use --cached to keep the file, or -f to force removal)
   ```

   No mention of the log either way.
4. I ran `git rm -qf` on the task file myself and retried. **Third attempt** refused with
   *"supervisor-log.md has no uncommitted change, so this unit's entry is either already committed
   or was never written."*

So attempt 2 **committed the log and then failed**, and attempt 3 could not proceed because of it.
`git log` in `embarch-fleet` confirmed one log-only commit (`1220200`) carrying the unit's full
entry with no corresponding instance commit. Recovered by committing the instance side by hand with
the same paths and message (`2225371`), which is exactly the *"undo by hand"* the invariant exists
to prevent.

## Two separate things, and the second is the one that cost recovery

**(a) A `git rm` of a locally-modified task file fails, and the modification is the supervisor's own
fix for the check in step 1.** This is the same shape as `tasks/doc/050` (*fold-commit cannot retire
a task file the fold itself corrected*) and `tasks/doc/072` (*the supervisor edits its task file in
the working tree*), reached from a third direction: the script's own state check **demands** the edit
that then breaks its `git rm`. Those two tasks are open and `Owner: required`; this is evidence for
both, and the fix may be a single `-f`, or staging the edit, or removing with `--cached`.

**(b) The log commit is not ordered after path settlement, at least on this path.** That is the
documented invariant, it is what makes a bad `--path` list cheap, and it is what left a log-only
commit here. A caller who did not know to check `git log` in the fleet repo would have re-written
the entry, or concluded the fold never happened.

## Done when

- [ ] `git rm` of a `done` task file succeeds when the supervisor has just corrected its `State:`
      line — by `-f`, by staging first, or by refusing earlier with an instruction to stage.
- [ ] Either the log commit genuinely happens after every path is settled, **or** `.claude/leg.md`'s
      sentence is corrected to say what the script actually does. Right now the doc and the script
      disagree and the doc is the one a supervisor trusts mid-fold.
- [ ] The *"supervisor-log.md has no uncommitted change"* refusal says what to do about it. It is
      accurate and it is a dead end as written: the recovery is "commit the instance side by hand
      with the same paths", and nothing says so.
- [ ] Check whether `tasks/doc/050` and `tasks/doc/072` are the same underlying defect as (a) and
      should be merged rather than tracked three times.

## Not yours

Do not change what a fold may stage or what the state check demands — the check in step 1 is
correct and caught a real defect (a landed unit whose task file still read as a live claim, which
the next leg's recovery would have reclaimed and re-dispatched; `tasks/doc/028` has six prior
instances). This is about the script's ordering and its `git rm` flags, not about relaxing a gate.
