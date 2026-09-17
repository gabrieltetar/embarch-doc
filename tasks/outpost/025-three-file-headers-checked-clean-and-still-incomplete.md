# 025 — Three things `outpost/024` checked, found clean, and correctly refused to fix

**State:** claimed by agent/outpost/025-three-headers-incomplete, 2026-09-16 22:01
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

- [x] (1) Decided, with the decision written down either way: `Kconfig:93` either cites 20 or says
      in the task's closing report why 4 and 17 alone are right.
      **Decided: 20 belongs, added.** Verified `decisions/transport.md` decision 20 against
      `Kconfig`'s `EMBARCH_OUTPOST_FILL_WAIT_MS` help block: the whole paragraph ("the trade is
      latency, and only latency... a record carries its own DUT stamp... Layout 2's only clock was
      the frame's arrival time") is a near-verbatim restatement of decision 20's own text, and the
      option it documents *is* decision 20's mechanism. 4 (per-record `cycles` stamp) and 17 (the
      two-clock split) are correctly cited too — they are what makes the trade free — so nothing
      was dropped. Added `(decisions.md decision 20)` at the sentence naming the trade itself,
      leaving `(decisions.md decisions 4, 17)` attached to the specific timestamp-independence
      claim they actually support, rather than merging all three numbers into one parenthetical
      that would blur which decision backs which sentence.
- [x] (2) `src/outpost_hooks.c` names decision 25 where it implements it, or the report says why it
      should not.
      **Named.** Verified `decisions/tracing.md` decision 25 ("GPIO dispatch traced as a handler
      timeline, not pin sampling") against `sys_trace_gpio_fire_callbacks_enter_user` /
      `sys_trace_gpio_fire_callback_user`: the two-hook split (`GpioDispatch` on entry,
      `GpioCallbackDone` on exit) and the 8-bit pin-mask truncation both match line for line. Added
      a one-line pointer in the file header ("The GPIO dispatch hooks below implement decision 25")
      alongside the existing, still-correct "decisions 2 and 7", plus an inline citation directly
      on the GPIO block's own comment, since that's where a reader following the code (not the
      header) lands first.
- [x] (3) Either resolved per `tasks/doc/055`, or explicitly left alone with `doc/055` named as
      what unblocks it. **Not a guess.**
      **Left alone.** `tasks/doc/055` is still `State: open`, `Owner: required`. Verified the three
      sites match the task's description exactly: `include/embarch/outpost.h:10` sits two
      directories under the repo root (`include/embarch/`), `scripts/gen_outpost_manifest.py:4` and
      `src/outpost.c:10` sit one (`scripts/`, `src/`), and all three write exactly one `../` before
      `embarch-doc/embarch-outpost/decisions.md`. On a plain sibling-checkout layout
      (`.../embarch/embarch-outpost/` next to `.../embarch/embarch-doc/`) neither depth is actually
      served by one `../`: a depth-1 file needs two, a depth-2 file needs three — so this is not
      "one of the three happens to be right," all three are short, and by a different amount each.
      Left the paths untouched per the task's explicit instruction; `doc/055` is what would settle
      whether the fix is depth-correction or a switch to the suite-root-relative form that has no
      depth to get wrong.
- [x] The report says whether these three change the answer to "does a zero-defect sweep mean a
      clean file", since that argument is live in the supervisor log and nothing else is measuring
      it.
      **Answered below, closing report.**
- [x] Gate green (`../../embarch-fleet/protocol.md` §10). `embarch-outpost` has no `Cargo.toml` —
      it is a Zephyr C module, so the cargo half selects nothing. Run what does apply:
      `python3 tests/decoder_unit.py`, `python3 tests/vocab_check.py`, and `check-docs.py` in
      `embarch-doc`. **Say plainly what could not be run** — the `west`-gated half of
      `tests/run-all.sh` has no toolchain in this sandbox and that is a standing debt, not a pass.
      `decoder_unit.py`: 31/31 pass. `vocab_check.py`: PASS (skips the study-designer cross-check,
      that repo isn't checked out beside this one — pre-existing, unrelated to this unit).
      `check-docs.py`: 11/11 green. `check-client-names.py --repo` (code worktree): clean.
      `check-ownership.py --scope outpost` (doc worktree) and `--code-repo` (code worktree): both
      OK. **Not run: anything under `tests/run-all.sh` that is `west`-gated** — no `west` and no
      Zephyr SDK in this sandbox, so the Zephyr build legs did not execute. Standing debt, not a
      pass; this unit touched a C comment header and a Kconfig help string, neither of which a
      build would exercise differently.
- [x] `changelog.d/` fragment dropped. A decision is created or amended only if item (1) or (2)
      turns out to need one, which it probably does not — these are citations, not design.
      Dropped `changelog.d/outpost-fill-wait-and-gpio-hooks-citations.fixed.md`, 98 bytes. No
      decision created or amended — both (1) and (2) are citation additions to existing decisions,
      not new design, exactly as anticipated.

## Closing report

**Items (1) and (2) were both real, both fixed. Item (3) verified and correctly left alone,
pointing at `tasks/doc/055`.**

**Does this change the answer to "does a zero-defect sweep mean a clean file"?** No — it sharpens
the same answer `outpost/024` already gave, from a different angle. `outpost/024` swept for wrong
*numbers* and found none, then flagged three completeness gaps outside its mandate. This unit went
and fixed two of those three, and both turned out to be real, non-trivial omissions: a Kconfig help
block silently paraphrasing a decision it didn't cite, and a source file implementing a whole hook
family (two thirds of its GPIO-tracing logic) under decisions 2/7 only, with the actual mechanism —
decision 25 — invisible to a reader following citations instead of code. Neither defect trips any
existing check: `check-decision-refs.py` confirms cited numbers exist and are current, never that
*every* decision a file implements is cited. **Completeness is not a one-off here — it is a whole
class of defect this suite has never swept for, because nothing measures "coverage" the way
`check-decision-refs.py` measures "correctness."** Two units in a row (`024`, `025`) each found
completeness gaps on the first look, in a small file set that had already passed every
number-correctness sweep run against it. That is enough signal to say a systematic completeness
sweep — walking each source file's implementation against the decisions it plausibly implements,
not just checking the citations already present — would very likely find more, elsewhere in
`outpost` and probably in other sub-projects. Recording this judgment here; whether to spin up that
sweep is not this unit's call.
