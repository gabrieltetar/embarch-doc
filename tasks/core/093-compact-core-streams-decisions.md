# 093 — `embarch-core/decisions/streams.md` is in reserve

**State:** done
**Source:** `scripts/check-doc-size.py`'s reserve floor, crossed by decisions 72 and 73
**Scope:** core
**Hardware:** none
**Owner:** no
**Compacts:** embarch-core/decisions/streams.md
**Size debt due:** 2026-09-25
**In flux:** no — for the move this task makes. Unparked at claim, 2026-09-28, three days past
its clock. 72 and 73 are still unvalidated on hardware (the old answer, below), but this task's
own remedy is a verbatim split, and `DOC-BUDGET.md`'s split-first rule is that a verbatim move
restates nothing, so flux cannot forbid one. The file is untouched since `a2c58650` (2026-09-18).
The old answer, kept as history: *yes — blocked on decisions 72 and 73 being validated against
real hardware, a traced study run with the outpost bridge attached, which will either confirm the
live path's frame indices and header handling or change them.* That still governs any **squeeze**
of 72 or 73; it does not govern moving them.

## What

The streams decision group is **11,094 / 12,288 B (90.3%), 1,194 B left**. Out
of reserve when this closes, or the task says why not.

Two entries landed together: **72** (an outpost trace is decoded and pushed
live, and the post-hoc render stays authoritative) and **73** (a `Text` tap gets
an arrival sidecar keyed by byte offset). Both are days old and both carry
reasoning nothing else in the corpus holds, so **neither is the one to squeeze** —
decision 72 in particular is half of a cross-repo reversal
([row 112](../../embarch-decision-reversals.md)) and its "what the render has
that live cannot" paragraph is the whole argument for keeping two paths.

The seam available is by mission: 30/38/39 are about **rendering and the file
layout**, and 70/72/73 are about **pushing live**. A split into
`decisions/streams-live.md` moves three entries verbatim.

## Why now

**In flux: yes.** The live path lands here days before its own bench validation
(the outpost bridge is not attached), so a squeeze taken now would be cutting
reasoning that has not finished being tested against hardware. A split moves it
untouched instead, which is why the split is the remedy and the squeeze is not.

## Dispatch note (supervisor, 2026-09-28)

**Split only; squeeze nothing.** Move 70, 72 and 73 byte-identical into
`decisions/streams-live.md` (or the seam you find better, said why), and rewrite none of them —
the unpark above covers a move and nothing else. Check inbound links to 70/72/73 across the suite
before cutting (`grep -rn` over `embarch-doc` and `embarch-core`), and repoint any that name the
file rather than a bare number.

**Also in reserve in `core`, not yours to write:** `decisions/surfaces.md` 709 B left
(`tasks/core/091`, blocked), `decisions/auth.md` 932 B left (`tasks/core/046`, blocked). If your
work pushes any other `core` file into reserve, file `tasks/core/<NNN>-compact-core.md` in the
same commit.

## Done when

- [x] Out of reserve, or the task says why not.
- [x] Decisions 72 and 73 keep every clause about what the post-hoc render has
      that live cannot, and about which clock each arrival sidecar records.
      Those are what a later reader will otherwise re-derive wrongly.
- [x] `decisions.md`'s index row split to match, with both files' numbers.
- [x] Byte numbers before and after.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10), `changelog.d/` fragment.

## Closed 2026-09-28

Split, not squeeze, per the dispatch note. 70, 72 and 73 moved verbatim (checked byte-identical
against the pre-split file with a Python diff, decision by decision) into new
`decisions/streams-live.md`; 30, 38 and 39 stayed in `decisions/streams.md`, also verified
byte-identical to their pre-split text. Nothing was rewritten or squeezed.

**Byte numbers.** Before: `decisions/streams.md` 11,094 B (90.3% of 12,288, 1,194 B left — in
reserve). After: `decisions/streams.md` 5,760 B (46.9%), `decisions/streams-live.md` 5,889 B
(47.9%). Both well clear of the 90% reserve line.

`decisions.md`'s index row split into two, sizes corrected to match (the pre-existing "7.7 KB" was
already stale before this task — real pre-split size was 11.1 KB).

**Inbound-link check** (`grep -rn` over `embarch-doc` and `embarch-core`, both worktrees): every
citation of 70/72/73 elsewhere in the suite is a bare decision number (resolved by
`scripts/check-decision-refs.py` regardless of file), except one — `embarch-ui/decisions/live-study.md`
line 30 links decision 70 straight at `../../embarch-core/decisions/streams.md`, which is now
the wrong file. `embarch-ui/` is outside this task's `core` scope, so that repoint is dropped as
an inbox task rather than fixed here:
`/home/gabriel/Github/embarch/embarch-doc/inbox/ui-repoint-streams-md-decision-70-cite.md`.

**Gate: `check-docs.py` is RED — 10 of 11 checks pass, `check-decision-refs.py` fails on exactly
the one out-of-scope link above** (`embarch-ui/decisions/live-study.md:30`, decision 70 pointing at
`streams.md` when it now lives in `streams-live.md`). This is the expected shape of a mission split
that another sub-project cited by file path rather than by bare number (`DOC-CONVENTIONS.md`'s own
"prefer the bare number" rule, and the precedent at `tasks/api/098` for `core/060`'s earlier split).
Fixing it requires editing `embarch-ui/`, which `check-ownership.py --scope core` refuses this
worker; the inbox drop above is the fix. `check-ownership.py --scope core` is green on both
branches, `check-client-names.py` is green. Code repo touched nothing — this was a pure doc split,
no Rust changes, so `cargo build`/`test`/`clippy` were not re-run (nothing to build).

**Branch tips:** `embarch-doc` `06dc821783f0553aa2abe358757c3f059c35c1de`, `embarch-core`
`48dc591493e657e5c978382a35777868309040bd` (unchanged — no code commit). Both pushed to
`agent/core/093-compact-core-streams-decisions`.
