# 022 — Citation sweep: the half of the repo `021` never grepped

**State:** open
**Source:** `outpost/021`'s **reviewer**, leg 113, 2026-09-13. That unit called itself a whole-repo
sweep and reported *"23 citations read, 1 wrong, 0 unsettled"*. Both numbers are true **only of the
`.c`/`.h` files its grep scoped to.** The reviewer found `scripts/gen_outpost_manifest.py:613`
carrying the **identical** wrong citation, word for word — the same `(decision 4)` on the same
runtime-vs-Kconfig clock-rate claim that `021` had just corrected in `src/outpost_priv.h`. It was
never counted and was still live on `main` after the sweep closed.
**Scope:** outpost
**Hardware:** none — comments only. **Do not build for a board, do not flash, do not attach a DUT.**
The host-side surface (`tests/decoder_unit.py`, `tests/vocab_check.py`, `tests/run-all.sh`) is the
whole build surface this task needs.
**Owner:** no

## What

**The one defect the reviewer found is already fixed** — leg 113's supervisor repointed
`gen_outpost_manifest.py:613` to `interfaces/wire.md` in the fold (`embarch-outpost` `8f6e667`). **Do
not redo it.** This task is the scope miss behind it.

Counted in the main checkout on 2026-09-13, immediately after `021` closed, these citations live
**outside** the `.c`/`.h` files `021` swept and have never been checked against a decision body:

```
Kconfig:93                              decisions.md decisions 4, 17
scripts/gen_outpost_manifest.py:4       decisions.md decisions 6, 7, 8, 9
scripts/gen_outpost_manifest.py:316     decisions.md decision 8
scripts/gen_outpost_manifest.py:636     decision 9
scripts/decode_outpost.py:268           decisions/clocks.md decision 18
scripts/decode_outpost.py:297           decision 4
tests/vocab_check.py:11                 decisions/wire.md decision 23
tests/vocab_check.py:27                 decisions/testing.md decision 26
tests/decoder_unit.py:366               decisions/clocks.md decision 18
tests/run-all.sh:27, 37, 50, 57, 101    decisions 22, 23, 26
tests/native_sim_stream/assert_stream.py:16, 47   decision 23, decisions.md decision 18
CMakeLists.txt:61, 126                  decision 9, decisions 6/7/8
.github/workflows/host-tests.yml:47     decision 23
```

That is **~19 citations across 9 files** in five languages the original grep never saw. Read each
cited decision's **body** against the sentence around the citation, exactly as `021` did — a number
that resolves is not evidence the claim holds.

## Why this is worth a unit

**The missed file was not an edge case, it was the one that mattered most.** `gen_outpost_manifest.py`
*generates the manifest* whose `record_layout_version` and `cycles_per_sec_config` the whole
decode path depends on. A wrong attribution there points a reader at the record-layout decision for a
clock-rate fact, which is precisely the confusion `021` fixed in the C header — and it survived the
sweep that fixed it.

**And the method lesson generalises past this repo.** Every sweep in this series has scoped its grep
to the language it expected to find comments in. `embarch-outpost` is a Zephyr module whose citations
live in C **and** Python **and** shell **and** CMake **and** Kconfig **and** a CI workflow. When the
next sweep in any repo says "whole repo", the grep should say so too.

## Watch for

- **Check `decisions.md` versus the topic files.** Several of these cite `decisions.md decision N`
  where the decision now lives in a `decisions/*.md` topic file. That form still resolves and is not
  itself wrong — do not churn it — but it means the citing author was reading an older layout, which
  raises the prior that the *claim* drifted too.
- **`tests/run-all.sh` cites decision 26 five times** for why a missing cross-decoder stays a skip
  rather than a failure. Check the decision body once and all five together; if one is wrong they
  probably all are.
- **`decode_outpost.py:297` cites decision 4** — the same decision `021`'s defect misused. Decision 4
  *is* the record-layout decision, so a citation about the four bytes a record pays is plausibly
  correct here. Check it rather than assuming either way.
- **No `embarch-outpost` doc is currently in reserve.** If your pass pushes one in, file
  `tasks/outpost/<NNN>-compact-outpost.md` in the same commit (`scripts/check-task-numbers.py --next
  outpost` for the number — never `ls | tail`).

## Done when

- [ ] Every citation in the list above is read against its cited decision's body, and wrong numbers
      and false sentences are counted and reported **separately**.
- [ ] The report says what the grep covered, in a form the next sweeper can re-run.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10) — for this repo that is the host-side test
      surface, not cargo; `embarch-outpost` has no `Cargo.toml`.
- [ ] `changelog.d/` fragment.
