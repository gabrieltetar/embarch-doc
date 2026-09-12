# 028 — `embarch-outpost` has no CI at all, and whether it should is a suite-scope call nobody has made

**State:** claimed — leg 087, 2026-09-11. Announced under `ops.md` §4 by leg 084, `ts 1789182061.785499`. The
30-minute window opened at that message. If this leg ends before it closes, **do not restart the
clock**: re-poll that thread and, with no objection and 30 minutes elapsed, execute.
**Source:** `embarch-outpost/open.md`, last bullet — *"Whether `embarch-outpost` should get a
workflow remains undecided and unfiled: it is a suite-scope call
(`../../embarch-fleet/protocol.md` §8), not this sub-project's to file."* Filed by leg 082's refill
sweep, 2026-09-11, which is the first sweep to act on the word **unfiled**.
**Scope:** suite
**Hardware:** none
**Owner:** no

## What

`embarch-outpost` is the only code-bearing sub-project in the suite with **no CI at any commit**.
`.github/workflows` is empty and `git log --all -- '.github/**'` finds nothing, so nothing runs
`tests/run-all.sh` on push; `decisions/testing.md` decision 22's toolchain-free leg ordering — fixed
precisely because it had been wrong — is exercised only when a human remembers to run it.
`embarch.md` §5's table already **states** this alongside every other sub-project's CI position, so
the fact is recorded and is not what is open.

What is open is the decision, and `embarch-outpost/open.md` says in as many words that it is not
that sub-project's to make: a CI position is a suite-level consistency call, so it belongs to the
supervisor under `../../embarch-fleet/protocol.md` §8, not to an `outpost` worker.

## The shape of the call, so whoever takes it does not re-derive it

The interesting constraint is that **a workflow added before the toolchain exists would be a step
unable to fail for the reason it was added** — the same objection `embarch-study-designer/open.md`
raises against a cross-compile job for the FFI staticlib, and the same one this repo's own history
records against tests written ahead of real data. `embarch-outpost` is a Zephyr module: its
`tests/unit` cannot be built from a fleet worktree at all (a standing debt in every recent log
entry), so a naive `cargo`-shaped workflow has nothing to run.

So the honest options are at least these, and the decision should say which and why:

- **A workflow that runs only what a toolchain-free runner can run** — `tests/run-all.sh`'s
  host-side legs, the ones decision 22 reordered — accepting that the Zephyr half stays uncovered
  and saying so in the workflow itself, so nobody reads a green check as more than it is.
- **A container or SDK-provisioning workflow** that can actually build the module, which is real
  cost and a real maintenance surface for a repo whose tests currently run by hand.
- **No CI, recorded as a decision with a trigger** rather than as an absence. This is a legitimate
  answer and may be the right one; what is not legitimate is the current state, where the suite
  cannot tell a considered no from nobody having asked.

## Why now

Every other sub-project's CI position is a decision somebody made. This one is a gap that has
persisted because the only doc that noticed it is also the doc that correctly refused to decide it.
An unfiled item named as unfiled in an `open.md` is invisible to `queue-status.py` and to every
sweep that reads task files — which is why it survived until a sweep read the sentence.

## Done when

- [ ] A numbered decision records the suite's CI position for `embarch-outpost`, in whichever doc
      owns it — and if the answer is "none", it is written as a decision with a trigger, not left
      as an absence.
- [ ] `embarch-outpost/open.md`'s last bullet is replaced by a pointer to it.
- [ ] `embarch.md` §5's CI table agrees with whatever was decided.
- [ ] If a workflow lands, it says in its own file what it does **not** cover.
- [ ] Gate green; `changelog.d/` fragment; `status.d/` fragment for anything suite-level this makes
      false.
