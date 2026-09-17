# 041 — Consider a systematic completeness sweep, distinct from the existing correctness sweeps

**State:** open
**Source:** `outpost/025`'s worker, 2026-09-16, dropped into `inbox/` at that unit's own instruction
("whether to spin up that sweep is not this unit's call") and filed here by the supervisor at that
unit's fold. Not something an `outpost`-scoped worker may decide or act on itself.
**Scope:** suite
**Hardware:** none — a proposal about doc-review process, no code and no hardware involved.
**Owner:** required — a new recurring sweep across every sub-project is a suite-level initiative,
and it is the kind of commitment a supervisor may not make on the owner's behalf.

## What

`outpost/024` swept 8 lines / 21 decision-number citations for wrong *numbers* and found zero, then
flagged three things outside its mandate that were not wrong numbers: a citation gap, an uncited
implementation, and a depth-inconsistent path trio. `outpost/025` fixed the first two and confirmed
both were real:

- `Kconfig`'s `EMBARCH_OUTPOST_FILL_WAIT_MS` help block paraphrased `decisions/transport.md`
  decision 20 near-verbatim without citing it — citing only 4 and 17, which are correct but adjacent.
- `src/outpost_hooks.c`'s header cited decisions 2 and 7, both correct, but the file's GPIO-dispatch
  hooks (`sys_trace_gpio_fire_callbacks_enter_user`, `sys_trace_gpio_fire_callback_user`) implement
  decision 25 line-for-line with no citation anywhere in the file.

Neither defect is something `check-decision-refs.py` — or any other suite gate — can catch. That
script confirms a *cited* decision number exists and is current. Nothing checks the other direction:
whether a file's actual implementation cites every decision it embodies. Two units in a row, on one
small file set in one sub-project, each found a real completeness gap on first look.

## Why now

The supervisor log has carried an open question across several handoffs — does a run of zero-defect
citation sweeps mean the corpus is clean, or the census is blind? `outpost/025`'s answer is that the
number-correctness sweeps are not blind for what they check, but they were never designed to check
completeness at all, and the two real gaps found here suggest that dimension has real defects
sitting in it, unswept, suite-wide.

**Read the evidence for what it is.** Two hits on one small file set in one sub-project is weak
evidence, and it is the only evidence anyone has gathered, because nobody has swept for this before.
It is also the opposite failure mode from the one the chain has been worrying about: the risk in a
completeness sweep is *inventing* a citation for a sentence a decision does not actually back, which
is the `study-designer/056` defect created rather than found.

## Done when

Not prescribing a mechanism — designing one is the point.

- [ ] A decision made, either way: is a systematic completeness sweep (source file implementation
      against the decisions it plausibly embodies, per sub-project) worth commissioning as its own
      recurring pass alongside the existing number-correctness sweeps?
- [ ] If yes: a scoping task filed. The mechanism is likely not mechanically checkable the way
      citation existence is — it needs a read of each source file against its sub-project's
      `decisions/` tree — so the scoping task has to say what bounds one pass.
- [ ] If no: the reasoning recorded somewhere durable, so the next unit that reopens this question
      does not start from zero.
