# 025 — Three things `outpost/024` checked, found clean, and correctly refused to fix

**State:** open
**Source:** `outpost/024`'s worker, 2026-09-16. That unit's mandate was decision-number
existence-and-truth, and it closed **8 lines / 21 instances / 0 wrong numbers / 0 false claims**.
Along the way it recorded three things that are *not* wrong numbers and so fell outside its mandate.
It was right to leave all three; it was also right that leaving them in a report leaves them nowhere.
Filed by the supervisor at that unit's fold — the same reason `topology/051` exists.
**Scope:** outpost
**Hardware:** none — C comments, one Kconfig help block and one Python module docstring. Nothing is
built, nothing is flashed, no probe, no live Core, no study, no DUT. Classified fresh at filing;
this is the same file set `outpost/024` classified the same way.
**Owner:** no

**Doc-size reserve for `outpost`: nothing in reserve.** If your work pushes an `outpost` doc into
the last 10% of its cap, file `tasks/outpost/<next free NNN>-compact-outpost.md` in the same commit
per `tasks/README.md`. **`tasks/doc/` is not yours.**

## What

Three items, independent of each other. Each one is a *completeness* defect rather than a
correctness one, which is precisely why no citation sweep has ever been allowed to touch them.

**(1) `Kconfig:93` sources its own sentence from a decision it does not cite.** The help block
carries *"so when it left the ring has no bearing [on when the host says it happened]"*, which is
near-verbatim `decisions/transport.md` decision **20** — *"it carries its own DUT stamp, so when it
left the ring has no bearing on when a host says it happened"* — and the whole block above it
describes decision 20's drain-wait mechanism. The line cites **4 and 17**. Both are independently
true of what they are attached to (4: the per-record DUT stamp; 17: the two-clock split that makes
that stamp authoritative for placement), so there is nothing to correct and something to add.
Decide whether 20 belongs in that citation, and if it does, add it without dropping 4 or 17.

**(2) `src/outpost_hooks.c` implements decision 25 and never names it.** The file's header cites
decisions 2 and 7, both correct and current. The same file implements decision 25's GPIO-dispatch
hooks — `sys_trace_gpio_fire_callbacks_enter_user` and `sys_trace_gpio_fire_callback_user`, matching
`decisions/tracing.md` decision 25 almost line for line — with no citation anywhere, header or
inline. A reader following the header learns what two thirds of the file is for.

**(3) Three headers carry the same `../embarch-doc/...` path at three different depths.**
`include/embarch/outpost.h:10`, `scripts/gen_outpost_manifest.py:4` and `src/outpost.c:10` all write
exactly one `../` before `embarch-doc/embarch-outpost/decisions.md`, but `outpost.h` sits two
directories under the repo root and the other two sit one. Read as literal filesystem paths, the
three resolve to three different places and at most one of them is right.

**Settle (3) before you edit it, and it may not be yours to settle.** `tasks/doc/055` — *settle the
cross-repo citation form for `embarch-doc`* — is `Owner: required` and open, and this is an instance
of exactly that question. If `doc/055` has landed by the time you read this, apply what it decided.
If it has not, **do not invent a convention**: say so, fix nothing in (3), and close the item by
pointing at `doc/055`. Depth-correcting three paths to a form the suite later rejects is more
expensive than leaving them inconsistent, because the wrong form then reads as deliberate.

## Why now

`outpost/024` is the twelfth pass in this chain and the second in a row to return zero defects,
which is the standing doubt the supervisor log keeps raising: is the corpus clean, or is the census
blind? **This task is a third answer to that question.** The worker found three real gaps and none
of them was a wrong number — so a sweep returning zero is not evidence of a clean file, only of a
file with no wrong numbers in it. Whatever this unit finds is worth reporting back into that
argument explicitly.

## Done when

- [ ] (1) Decided, with the decision written down either way: `Kconfig:93` either cites 20 or says
      in the task's closing report why 4 and 17 alone are right.
- [ ] (2) `src/outpost_hooks.c` names decision 25 where it implements it, or the report says why it
      should not.
- [ ] (3) Either resolved per `tasks/doc/055`, or explicitly left alone with `doc/055` named as
      what unblocks it. **Not a guess.**
- [ ] The report says whether these three change the answer to "does a zero-defect sweep mean a
      clean file", since that argument is live in the supervisor log and nothing else is measuring
      it.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10). `embarch-outpost` has no `Cargo.toml` —
      it is a Zephyr C module, so the cargo half selects nothing. Run what does apply:
      `python3 tests/decoder_unit.py`, `python3 tests/vocab_check.py`, and `check-docs.py` in
      `embarch-doc`. **Say plainly what could not be run** — the `west`-gated half of
      `tests/run-all.sh` has no toolchain in this sandbox and that is a standing debt, not a pass.
- [ ] `changelog.d/` fragment dropped. A decision is created or amended only if item (1) or (2)
      turns out to need one, which it probably does not — these are citations, not design.
