# 020 — `interfaces/wire.md` says one host-only test and its leg arithmetic is short; there are three and six

**State:** open
**Source:** leg 106 refill sweep, 2026-09-13, scout-verified against `run-all.sh` and the CI
workflow. The scout did **not execute** either script — see "Not verified" below.
**Scope:** outpost
**Hardware:** none — one documentation section. No code, no board.
**Owner:** no

## What

`embarch-doc/embarch-outpost/interfaces/wire.md`'s test section describes a test layout the repo
has outgrown, in three places:

- **`:73`** — the heading *"…and one of the two tests always runs"*. There are **six** legs:
  `grep -n '^echo "=== ' embarch-outpost/tests/run-all.sh` → decoder unit, vocab check,
  cross-decoder, ztest unit, module-off compile, end-to-end.
- **`:76`** — *"`tests/decoder_unit.py` … is the only check here with **no** external
  requirement"*. `vocab_check.py` has none either: `run-all.sh:47-52` runs it with the comment
  *"Host Python only… Never needs west or ZEPHYR_BASE"*, and `.github/workflows/host-tests.yml`
  runs it toolchain-free on every push (suite decision 2). The cross-decoder needs no toolchain
  either but does need two sibling checkouts, which is a different kind of requirement — say which.
- **`:79`** — *"the other three legs need a Zephyr toolchain and the cross-decoder leg needs two
  sibling checkouts"*, which accounts for **5** legs against 6. `run-all.sh:32` says *"All three of
  the next legs are deliberately ahead of the west guard below"*.

## Why now

This section is what tells a reader — and a fleet worker with no Zephyr toolchain in its worktree —
which legs it can run and which it must record as a debt. Getting it wrong in the safe direction
(claiming fewer host-only checks than exist) means work that could have been verified is reported
as unverifiable, which is exactly the standing `embarch-outpost` debt this fleet keeps carrying
forward. `outpost/019` landed the adjacent correction (decision 26's CI premises) on 2026-09-13 and
did not reach this file.

## Done when

- [ ] The three statements match `run-all.sh` as it is now: the leg count, which legs are host-only,
      and what each of the rest actually requires — distinguishing "needs a Zephyr toolchain" from
      "needs two sibling checkouts", which are different obstacles with different fixes.
- [ ] Derived by reading `run-all.sh` and `.github/workflows/host-tests.yml`, with the leg names
      quoted from the script rather than paraphrased.
- [ ] **Run what you can**: `decoder_unit.py` and `vocab_check.py` are claimed to need nothing but
      host Python. Run both and say what happened — if either turns out to need something, that is
      the more interesting finding and it changes the fix.
- [ ] Suite decision 2 is cited correctly if referenced — through `suite/decisions.md`, never
      through the topic file that holds the text, or `check-decision-refs.py` will not resolve it.
- [ ] Gate green; `changelog.d/` fragment.

## Not verified by the scout

It read the "needs no toolchain" claim off `vocab_check.py`'s imports, its skip path
(`tests/vocab_check.py:141`) and the CI workflow — **not from a run**. That is why running the two
host legs is a `Done when` item rather than an optional extra.

## Do not

Do not add a leg to `host-tests.yml` or change what CI runs. Suite decision 2 deliberately leaves
the cross-decoder and the three `west`-dependent legs out, with its own stated reason (a permanent
skip is worse than an absence) and its own reversal condition. Changing that is a suite-scope call,
not this repo's.
