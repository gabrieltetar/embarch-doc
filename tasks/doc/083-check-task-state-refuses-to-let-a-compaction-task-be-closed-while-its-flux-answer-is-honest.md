# 083 — `check-task-state.py` cannot close a compaction task paid as a ride-along without falsifying its `In flux:` answer

**State:** open
**Source:** leg 141, 2026-09-17, hit while closing `tasks/core/079-compact-core.md` after
`core/078` paid its debt inside its own unit. Found by the gate refusing the fold, not by reading
the script.
**Scope:** doc
**Hardware:** none — one `elif` in one script, or one sentence in `tasks/README.md`.
**Owner:** required — the fix is in `scripts/check-task-state.py` and/or `tasks/README.md`, both
owner-reserved (`protocol.md` §3). Filed rather than fixed; a supervisor that edited the check
deciding what it may write would be editing its own interlock.

## What

`scripts/check-task-state.py` enforces *"`In flux: yes` implies `blocked`"*, exempting exactly one
case — `Owner: required` — on the stated grounds that ownership already keeps every agent off the
task, so `blocked` would protect nothing.

**`done` deserves the same exemption for the same reason, and does not have it.** Nothing dispatches
a completed task, so the field gates nothing there either. The check as written refuses:

```
tasks/core/079-compact-core.md
    `In flux: yes` but state is 'done'
```

**This is not hypothetical and it is not rare — it is the expected end state of a rule
`.claude/leg.md` actively instructs.** That file says a blocked compaction task parks the *pass*,
not the reserve: when a unit must write into a file whose compaction task is blocked on
`In flux: yes`, that unit's worker compacts the file inside its own unit, carrying the parked task's
`Must not delete:` list. **The debt is then paid while the flux answer is still honestly `yes`** —
indeed *because* it is: the whole argument for the ride-along is that the actor making the flux is
the only one who can compress what it is rewriting. So every successful application of that rule
produces a task that is finished and cannot be marked finished.

**The workaround the supervisor used, and why it is bad.** Flip the field to `no` and keep the
original answer verbatim in a block quote underneath. `tasks/core/079` now reads that way. It passes
the gate and it tells a human the truth, but **the machine-readable field is now false**, which is
precisely the property `tasks/doc/030` established the field must have (*"`In flux:` is answered PER
FILE … `check-task-state.py` enforces the whole of what follows"*). A check that can only be
satisfied by lying to it is worse than no check on that axis.

**Leaving the task `blocked` instead is worse still**, which is why the flip was chosen. `core/079`
carries **Size debt due: 2026-09-24**. `.claude/leg.md` makes an overdue ledger entry a leg's
**first unit, blocked or not** — that is the whole point of giving parks a clock. So a `blocked`
task whose debt was already paid does not sit harmlessly; it pre-empts a future leg's first unit for
work that has happened. `check-doc-size.py` would not list the file (it is out of reserve), so
nothing would contradict the stale park.

## Why now

Second-order, cheap, and it sits directly on top of two rules the fleet uses constantly. The
ride-along rule has now fired at least twice in two legs — `tasks/ui/066` in leg 140 and
`tasks/core/079` here — so whatever leg 140 did to close `ui/066` is worth reading alongside this,
because it faced the same refusal and its log entry says it *"discharg[ed] its `In flux` answer
rather than overriding it"*, which may be a third, better workaround nobody wrote down.

## Done when

- [ ] Either `check-task-state.py` exempts `done` from the `In flux: yes` ⇒ `blocked` rule the way
      it exempts `Owner: required`, or `tasks/README.md` states the sanctioned way to close a
      compaction task whose flux answer was honestly `yes` when the debt was paid — and
      `.claude/leg.md`'s ride-along paragraph points at it, since that paragraph is what creates the
      state.
- [ ] `tasks/core/079`'s flipped field is reconciled with whatever is decided — either restored to
      `yes` once the check allows it, or its block-quoted original is blessed as the pattern.
- [ ] Check what leg 140 did to close `tasks/ui/066` (`embarch-doc@3e7e15cf`, entry in
      `embarch-fleet/supervisor-log.md`) and fold that in; if it found a cleaner route, this task is
      a documentation fix rather than a script one.
- [ ] Gate green.
