# 020 — `interfaces/wire.md` says one host-only test and its leg arithmetic is short; there are three and six

**State:** done
**Source:** leg 106 refill sweep, 2026-09-13, scout-verified against `run-all.sh` and the CI
workflow. The scout did **not execute** either script — see "Not verified" below. **And
"scout-verified" is one reader, which has already been wrong once**: the same scout, same sweep,
reported a quoted source comment as never having existed when it had existed and was later
rewritten (`umbrella/058`). Re-derive the leg count from the script.
**Scope:** outpost
**Hardware:** none — one documentation section. No code, no board.
**Owner:** no

## Dispatch note (supervisor, leg 107)

**No `embarch-outpost` doc file is in reserve** — you have headroom, so this unit has no
compaction obligation unless your edit pushes a file past 90% of its cap, in which case file
`tasks/outpost/<next free NNN>-compact-outpost.md` in the same commit.

**Re-derive the leg count yourself; the scout's numbers are a floor, not a fact.** The task says
so and names the reason (`umbrella/058`). Run `grep -n '^echo "=== ' embarch-outpost/tests/run-all.sh`
against the checkout you are given and read the west guard's position in that script, rather than
trusting "six" because it is written above.

**You cannot execute `run-all.sh`, and that is expected, not a blocker.** The `embarch-outpost`
Zephyr toolchain is absent from a worker's worktree — a standing fleet debt, recorded in every
recent log entry. Derive the layout by reading the script and the CI workflow, say in your report
that nothing was executed, and do **not** report a leg as passing or failing.

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

- [x] The three statements match `run-all.sh` as it is now: the leg count, which legs are host-only,
      and what each of the rest actually requires — distinguishing "needs a Zephyr toolchain" from
      "needs two sibling checkouts", which are different obstacles with different fixes. Confirmed
      six legs (`grep -n '^echo "=== ' tests/run-all.sh` → decoder unit, vocab check, cross-decoder,
      unit ztest, module off, end-to-end stream); the west guard sits at `tests/run-all.sh:69`, after
      the first three. Rewrote `embarch-doc/embarch-outpost/interfaces/wire.md`'s heading and its two
      following paragraphs (former `:73`, `:76`, `:79`) to state six legs, that decoder_unit and
      vocab_check need nothing external at all, and that cross-decoder needs no toolchain but does
      need two sibling checkouts to check anything for real — a different requirement, not the same
      absence.
- [x] Derived by reading `run-all.sh` and `.github/workflows/host-tests.yml`, with the leg names
      quoted from the script rather than paraphrased.
- [x] **Run what you can**: `decoder_unit.py` and `vocab_check.py` are claimed to need nothing but
      host Python. Ran both from the code worktree: `decoder_unit.py` — 31 tests, all pass, exit 0;
      `vocab_check.py` — exit 0, prints its loud sibling-skip note (`embarch-study-designer` not
      checked out beside it) and `PASS: 11 kinds and 8 flag bits agree`. Neither needed anything
      beyond host Python; the claim holds.
- [x] Suite decision 2 is cited correctly if referenced — through `suite/decisions.md`, never
      through the topic file that holds the text, or `check-decision-refs.py` will not resolve it.
      Cited as `[suite decision 2](../../suite/decisions.md)`; `check-decision-refs.py` passes.
- [x] Gate green; `changelog.d/` fragment.

## Not verified by the scout

It read the "needs no toolchain" claim off `vocab_check.py`'s imports, its skip path
(`tests/vocab_check.py:141`) and the CI workflow — **not from a run**. That is why running the two
host legs is a `Done when` item rather than an optional extra.

## Do not

Do not add a leg to `host-tests.yml` or change what CI runs. Suite decision 2 deliberately leaves
the cross-decoder and the three `west`-dependent legs out, with its own stated reason (a permanent
skip is worse than an absence) and its own reversal condition. Changing that is a suite-scope call,
not this repo's.
