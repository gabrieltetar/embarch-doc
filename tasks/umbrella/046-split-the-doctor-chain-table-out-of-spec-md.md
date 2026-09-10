# 046 — Move the `doctor` chain table verbatim out of `spec.md` into its own file

**State:** claimed — leg 067
**Source:** leg 067, taking option 2 of the three leg 066 wrote into `tasks/umbrella/038`
**Scope:** umbrella
**Hardware:** none
**Owner:** no

## Why this exists rather than dispatching `038`

`tasks/umbrella/038` is the compaction task for these files and it is **`blocked`, correctly**:
its `In flux: yes` argument holds (`tasks/umbrella/033` is open and is exactly a check-17
`doctor`-chain row change), and a compaction *pass* — which rewrites and shortens argument — must
not run over a table that is about to be rewritten.

**A verbatim mission split is a different operation and the flux argument cannot forbid it**
([DOC-COMPACTION.md](../../DOC-COMPACTION.md) §2, and `.claude/leg.md`'s split-first rule): moving
text unchanged restates nothing, so there is no argument to get wrong. `outpost/008` did exactly
this to `decisions/tracing.md` under flux on 2026-09-10 and it held.

**`038` stays `blocked` and is not yours.** This task does not close it. It buys `spec.md` room so
that the wall — **96 bytes left** as of `umbrella/036` — stops being one row-edit away, and it
gives the volatile table its own file to grow in.

## What

`embarch-umbrella/spec.md` is **10,144 / 10,240 B (99.1%)**. Its `## The `doctor` chain` section
(from the `## The `doctor` chain` heading to just before `## Token handling`) is **~4,561 B** — an
eighteen-row table plus its lead-in. Move that section **verbatim** into a new file:

`embarch-umbrella/interfaces/doctor-chain.md` (create `interfaces/` if the sub-project has none;
match whatever sibling sub-projects name this kind of file — check before inventing a path).

Leave in `spec.md`, in place of the moved section, a short pointer section: the heading, one
sentence saying what the chain is and that each check emits pass/warn/fail plus a concrete fix
line, and a link to the new file. Nothing else.

## The rules that make this a split and not a rewrite

- **Not one character of the table's cells changes.** Same rows, same order, same numbering, same
  decision citations, same emphasis. If you find something in it you believe is wrong, that is an
  `inbox/` drop, not an edit in this unit.
- **Every inbound link keeps working.** Grep the whole suite for links and references into
  `embarch-umbrella/spec.md`'s doctor section — including anchors like `#the-doctor-chain` — and
  repoint them at the new file. `python3 scripts/check-docs.py` must be green, which includes
  `check-links.py` and `check-decision-refs.py`.
- **The new file gets whatever front matter the doc protocol requires of a file in its position**
  ([DOC-PROTOCOL.md](../../DOC-PROTOCOL.md)) — title, one-line purpose, and a link back to
  `spec.md`. Read the protocol; do not copy a sibling's shape from memory.

## Doc-size reserve for `umbrella` — read before you write

- `embarch-umbrella/spec.md` — **96 B left** (10,144/10,240). This unit is the one that fixes that;
  it must end **well** below 90%.
- `embarch-umbrella/open.md` — **124 B left** (4,996/5,120). **Do not grow it.** If this unit needs
  to record a question, it goes in the new file or an `inbox/` drop, not here.
- `embarch-umbrella/decisions/bind.md` — 879 B left (11,409/12,288).
- The new `doctor-chain.md` starts near-empty and has a full cap.

If your work leaves any `umbrella` file in reserve that nothing has filed against, file
`tasks/umbrella/<NNN>-compact-umbrella.md` in the same commit (`tasks/README.md` has the shape).
`038` already covers `spec.md` and `open.md`, so you owe a new one only for a *different* file.

## Is this a new decision?

**No, and do not write one.** A mission split is a doc-mechanics move that `DOC-COMPACTION.md` §2
already authorises. Record it in a `changelog.d/umbrella-*` fragment and in the commit message.

## Done when

- [ ] `embarch-umbrella/spec.md` is **below 90%** of its cap (`python3 scripts/check-doc-size.py`).
- [ ] The eighteen rows exist exactly once in the suite, verbatim, in the new file — verify with a
      `git show HEAD:embarch-umbrella/spec.md` diff against the new file's table body.
- [ ] `spec.md` still tells a reader the `doctor` chain exists and where to read it.
- [ ] `open.md` is not larger than it was.
- [ ] `python3 scripts/check-docs.py` green.
- [ ] `changelog.d/umbrella-*` fragment dropped.
