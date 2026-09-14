# 021 — Citation sweep: all of `embarch-outpost`'s source, in one pass

**State:** done
**Source:** leg 112's refill sweep, 2026-09-13. `queue-status.py --refill-owed --wave 6` reported
five distinct scopes against a wave of six, with `outpost` holding nothing dispatchable —
`tasks/outpost/002` is `blocked` and `tasks/outpost/018` is `Hardware: required`. The citation-sweep
series has never touched this repo.
**Scope:** outpost
**Hardware:** none — source comments only. **Do not build for a board, do not flash, do not attach a
DUT.** The host-side unit tests under `tests/unit/` are the whole build surface this task needs.
**Owner:** no

## What

Counted in the main checkout on 2026-09-13, **23 lines match `[Dd]ecisions? [0-9]+` across the entire
repo** — small enough that this task is the whole sweep rather than the first slice of one:

```
8  src/outpost_priv.h
5  src/outpost.c
4  src/outpost_hooks.c
2  include/embarch/outpost.h
1  tests/unit/src/main.c
1  src/outpost_time.h
1  src/outpost_ring.c
1  src/outpost_markers.c
```

Read every one against the cited decision's **body**. Recount before you start — the number above is
one grep on one day, and the method below is what the unit is judged on, not the arithmetic.

## Why this repo is worth a sweep despite being small

**It is the sharpest available test of the series' hypothesis, in the direction nobody has tested.**
The results so far — `core/054` (`api.rs`) 3 wrong in 54 · `umbrella/065` (`doctor.rs`) 2 in ~129 ·
`study-designer/044` 0 in ~53 · `ui/049` 0 in 74 · `umbrella/066` 113 held / 1 wrong ·
**`core/056` (`study.rs`) 10 in 109** — support a hypothesis first guessed by `ui/049`: **the dirty
files are the ones that restate other repos' decisions; the clean ones explain their own code.**

Every test of that so far has been a *host-side Rust* file. `embarch-outpost` is C, it is a leaf, and
it is the one component in the suite that ships **inside someone else's firmware**. Two specific
things to check rather than assume:

- **The record-layout version history is a known trap.** Layout 2 removed every DUT timestamp; layout
  3 restored it, because the objection was to the lock and not to the clock, and **the version went
  2 → 3 rather than back to 1** (reversals rows 62, 80, 86). A comment that cites the decision behind
  layout 2 while describing layout 3's behaviour would resolve cleanly and be false. That is exactly
  the false-sentence shape the series keeps finding.
- **The wire is shared with `embarch-core`'s decoder and `embarch-study-designer`'s stream
  contract**, so any comment about what the host does with a record is narrating another repo's
  decision from outside it — the dirty side of the hypothesis, in a repo the hypothesis predicts
  should otherwise be clean.

**Report the count either way.** A clean sweep here is real evidence, and this repo is small enough
that "checked 23, found none" is a complete and honest product for one unit.

## Method (carried from `core/054`, `core/056`, `umbrella/065`, `umbrella/066`, `study-designer/046`)

**Read the cited decision's body, then read the sentence around the citation, in that order.** A
number that resolves is not evidence the claim holds. **Count wrong *numbers* and false *sentences*
separately and report both.**

**Check cross-repo labelling.** A bare `decision N` is same-repo by convention; another repo's
decision must read `<repo> decision N`. The general form is still open and owner-reserved
(`tasks/doc/055`), so do not invent a new form — use the labelled one already in use. **Check every
bare `decision N` against `embarch-outpost`'s own decision set first**, whatever the topic looks
like. Given how much of this repo's comment surface is about the host half of the wire, expect the
bare/labelled question to be most of the yield here if there is any.

**Git history of the decisions file is worth checking when a citation's credit looks off** —
`git log --follow -p -- embarch-outpost/decisions/<file>.md`. `study-designer/046` resolved both of
its false-sentence findings that way: one decision walking back its own earlier claim, one fact
folded into an *earlier* number "the same session".

**Four shapes found so far, none of them a typo:** a real decision cited in the wrong *repo*; a
structural rule attributed to the decision that *used* it rather than the one that *established*
it; an over-cited pair from a different table row; and — `umbrella/067` — **a citation that
resolves, to a real decision, in the right repo, that has nothing to do with the code it
annotates.** Only reading the body detects the fourth. **Deleting such a citation is a legitimate
fix.**

**And do not adjudicate your own doubt in your own favour.** `umbrella/066` reported 114/0; a
reviewer sampling 12 found one the worker had flagged as "defensible either way" and folded into the
zero. The honest tally was 113/1. **A zero-defect sweep's characteristic failure is the sweeper
resolving an ambiguity toward zero.** Report anything you cannot settle as unsettled.

## Watch for

- **Do not file a numbered decision for this.** A citation sweep decides nothing. If it turns up
  something that genuinely needs deciding, file `tasks/outpost/<next>` and say so in your closing
  section (`check-task-numbers.py --next outpost` picks the number; `ls | tail` does not, because a
  `done` task's file is gone).
- **No `embarch-outpost` doc is currently in reserve**, so you have headroom. If your pass pushes one
  in, file `tasks/outpost/<next>-compact-outpost.md` in the same commit.
- **This repo compiles into a DUT's firmware and this task must not change what it compiles to.**
  Comments only. If a citation is wrong because the *code* is wrong, that is a finding for
  `inbox/` — written to `/home/gabriel/Github/embarch/embarch-doc/inbox/` by absolute path — not a
  change to make here.

## Done when

- [x] Every source and header file listed above read, every `decision N` citation checked against the
      cited decision's body rather than merely resolved.
- [x] Wrong numbers and false sentences counted and reported separately, with the total read, and any
      citation you could not settle reported as unsettled rather than folded into either count.
- [x] The record-layout 2 → 3 history checked specifically, per *Why this repo* above.
- [x] Cross-repo citations carry the labelled `<repo> decision N` form; same-repo ones stay bare.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `changelog.d/` fragment — including if the answer was zero defects, because the count is the
      product of this unit.

## Closed 2026-09-13

Recounted first: `grep -rn -E '[Dd]ecisions? [0-9]+' --include='*.c' --include='*.h' .` still returns
the same 23 lines across the same 8 files the task lists. Read all 12 `decisions/*.md` files' bodies
(every decision the repo owns: 1–9, 14, 17–26) and checked each of the 23 citations against the cited
decision's body, not just that the number resolves.

**23 read, 1 wrong number, 0 unsettled.**

- **The one defect** — `src/outpost_priv.h`, the `cycles_per_sec` field comment: "the Kconfig is
  legitimately 0 on targets that read their timer frequency at runtime **(decision 4)**." Decision 4
  (`decisions/layout.md`) is the record-layout decision — cycles stamp, ring slot size, the 2→3 version
  history — and never once mentions `CONFIG_SYS_CLOCK_HW_CYCLES_PER_SEC` or a build-time-vs-runtime rate
  read. The actual fact is stated, word for word, in `interfaces/wire.md` (`cycles_per_sec` is read at
  runtime... which legitimately defaults to 0...) with no decision number attached at all — it was never
  a numbered decision, just an interface fact. This is the fourth shape from the method section: a
  citation that resolves, to a real decision, in the right repo, with nothing to do with the line it
  annotates. Fixed by repointing the citation from `(decision 4)` to `(interfaces/wire.md)`, the doc that
  actually carries the claim — a bare deletion would have thrown away a citation a reader can still use.
- **The record-layout 2 → 3 history** (the specific trap this task's *Why this repo* section named): all
  four citations touching it — `outpost_priv.h`'s `OUTPOST_RECORD_LAYOUT_VERSION` block (decision 4,
  twice), `tests/unit/src/main.c`'s varint worst-case test (decision 4), and `outpost_time.h`'s clock-read
  constraint (decisions 3 and 4) — hold. None describes layout 2's behaviour under a decision-4 citation
  or otherwise gets the lock-vs-clock distinction backwards.
- **The one cross-repo citation** — `outpost_priv.h`'s COBS-framing note, `embarch-study-designer/
  decisions.md decision 10` — checked against that repo's actual `decisions/wire.md` decision 10
  ("COBS-framed postcard..."), and it is exactly the decision being cited, correctly labelled. No bare
  `decision N` in this repo's source turned out to actually mean another repo's decision.
- **The other 21** all check out: each cited decision's body contains the specific claim the comment
  attributes to it (several — `outpost_priv.h`'s decision-20 hint-not-fact paragraph, decision 9's
  no-manifest-CRC paragraph — are near word-for-word restatements of the decision text, which is the
  clean-file signature the series' hypothesis predicts for code that explains itself rather than
  restating another repo's decision).

No decision needed filing — this stayed inside "check a citation," never "decide something new." No doc
pushed into reserve (`check-doc-size.py` stayed green through `check-docs.py`), so no compaction task
filed. Nothing found here belongs to another sub-project's decision set, so no `inbox/` drop was
necessary this time.

**Gate:** `python3 scripts/check-docs.py` — 11/11 green. `check-decision-refs.py` — 1979 refs resolve
(872 ambiguous, non-error), 35 topic-file links and 16 reversal-row citations all resolve.
`check-client-names.py --repo` on both worktrees — clean. `check-ownership.py --scope outpost` (doc) and
`--code-repo` (code) — both OK. This repo has no `Cargo.toml`; the host-side build surface is
`tests/decoder_unit.py` (31 tests) and `tests/vocab_check.py` (11 kinds / 8 flag bits), both run and
green after the fix — no board build, no flash, no DUT touched, per this unit's hardware note.
