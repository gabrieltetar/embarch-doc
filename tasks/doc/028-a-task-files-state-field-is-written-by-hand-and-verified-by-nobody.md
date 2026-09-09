# 028 — A task file's `State:` field is written by hand and verified by nobody, and six instances in two legs say that is not an accident

**State:** open
**Source:** leg 057's closing "Least sure about" (2026-09-09 00:01, `api/034`), which named this class and deliberately did not file it; leg 058 met it twice more the same night
**Scope:** suite
**Hardware:** none
**Owner:** required

## What

Every state a task file carries — `State:`, `In flux:`, `Compacts:`, `Owner:` — is prose written by
hand, by a worker or a supervisor, and **nothing reads it back against what actually happened.**
`queue-status.py` and `check-doc-size.py` *consume* these fields to decide what is dispatchable and
what debt is outstanding, so a wrong one is not cosmetic: it silently removes work from the queue or
silently adds it.

Three distinct failures, all observed, all in the last two legs:

1. **A completed task left at `State: claimed`.** The worker lands the work, pushes both branches,
   ticks its own Done-when boxes, and never touches line 3. The supervisor then either notices at
   the fold or does not. Leg 057 hit this twice (`study-designer/006`-adjacent and one other) and
   fixed both by hand; leg 058 hit it again on `outpost/005` — the worker's own report said
   "Task file's Done-when boxes ticked" and the state line still said `claimed`. **A task left
   `claimed` after its leg dies looks exactly like a live claim**, which recovery then reclaims to
   `open`, which re-dispatches finished work.
2. **An `In flux: yes` compaction task sitting at `State: open`.** `.claude/leg.md` says a task
   whose `In flux:` says yes must be `blocked` and must name what unparks it, and that an `open` one
   means the filer got it wrong. Leg 057 found two.
3. **A paid size-ledger item nobody closed** — the file is out of reserve, the task still claims it.
   Leg 057 found two, and `check-doc-size.py --pressure` already prints `PAID … close its item`
   for exactly this, so the detection exists and only the closing is manual.

## Why now

**Six instances across two legs is a rate, not an anecdote.** Leg 057 found four of them, fixed each
instance, filed none, and wrote in its own log entry that the reason was reluctance to hand the owner
a third `Owner: required` item in one leg — then said plainly that *if a later leg meets any of these
again, the honest reading is that it under-filed, and the right move is a single task naming the
whole class rather than three narrow ones.* Leg 058 met (1) again within forty minutes of that entry
being written. This is that single task.

The cost is not hypothetical. Failure (1) is the one with teeth: a `claimed` task plus a killed leg
is indistinguishable from a live claim, and `ops.md` §3's recovery correctly reclaims it — so the
next leg re-dispatches a unit that already landed, into a repo whose `main` already has the change.
Failures (2) and (3) are quieter and both point the same way: they make the queue's own accounting
wrong in the direction of *less* work being visible.

## Why this is `Owner: required`

Every plausible fix is a reserved path. A checker belongs in `scripts/` (`check-task-state.py`, or
new refusals inside `queue-status.py` and `fold-commit.py`); the rule that a worker must set its own
state belongs in the worker contract in `.claude/`; the rule that a supervisor must verify it at the
fold belongs in `.claude/leg.md` or `protocol.md`. **A supervisor that can edit its own constraints
has none**, so no leg may do any of it. What a leg can do is what this file is.

## Sketch of the fix, for the owner to accept, change or reject

Three candidates, cheapest first — they are not exclusive:

1. **`fold-commit.py` refuses a fold whose unit's task file is not in a terminal state.** It already
   refuses a fold whose log entry drops a field and one that consumed a fragment outside its
   `--path` list, so the shape and the enforcement point both exist. This catches failure (1) at the
   exact moment the truth is known, and costs the supervisor a one-line edit it should be making
   anyway. **This is the one I would build.**
2. **`queue-status.py` reports a contradiction rather than resolving it.** An `In flux: yes` task at
   `State: open`, and a task whose `Compacts:` paths are all out of reserve, are both derivable from
   files the script already parses. Print them as a `CONTRADICTIONS` block the way `LOW QUEUE` is
   printed; do not auto-correct, because the correction is a judgement.
3. **The worker contract makes the state line part of "done".** A worker's last act is pushing both
   branches; setting its own task file's state is the same kind of bookkeeping and belongs beside it.
   Weaker than (1) on its own — it asks the actor who just forgot to remember — but it removes the
   supervisor's silent repair work, which is the thing that has been hiding the rate.

## Done when

- [ ] The owner has decided which of the three (or what else) to build, or decided the manual repair
      is cheap enough to keep — **that decision recorded, either way**, because the current state is
      that six instances were fixed by hand and nothing was written down.
- [ ] If a mechanism is built: it fires on a reconstruction of at least failure (1), and a leg's
      log entry no longer has to say "corrected from `claimed` by the supervisor at the fold".
- [ ] This task's own claim — six instances in two legs — is checkable against
      `supervisor-log.md`'s `2026-09-08` folded entry and leg 058's entries, which is where each was
      recorded.

## Not in scope

Auto-correcting a state field. Every one of these six was fixed by a human-or-supervisor judgement
about what actually happened, and a script that guesses would convert a loud wrong field into a
quiet wrong one.
