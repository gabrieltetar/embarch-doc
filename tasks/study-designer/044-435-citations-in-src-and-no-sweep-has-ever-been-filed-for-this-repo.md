# 044 — 435 citations in `src/` and no sweep has ever been filed for this repo

**State:** done
**Source:** the leg of 2026-09-13 17:5x, counting every repo's source while filing refill work.
`embarch-study-designer` has the **largest** source citation surface in the suite — 435 lines
matching `decision[s] N` across `src/` — and unlike `embarch-core`, `embarch-umbrella`,
`embarch-ui` and `embarch-dev-bench`, **no sweep of it has ever been filed or run.**
**Scope:** study-designer
**Hardware:** none — source comments only; nothing is built for a board.
**Owner:** no

## What

```
52  src/study.rs
41  src/schema_version.rs
35  src/gatt_extract.rs
34  src/lib.rs
```
…and ~273 more across the rest of `src/`.

**`check-decision-refs.py` resolves decision numbers only inside `*.md`**, so a wrong number in a
source comment fails no gate and never has.

## Why this repo is the one where it matters most

`embarch-study-designer` is a **shared crate** — `embarch-api`, `embarch-core`, `embarch-ui` and
`embarch-umbrella` all depend on it. Its comments are therefore read by people working in four other
repos, and a bare `decision N` in it is ambiguous in a way the same comment in a leaf repo is not:
the reader's default index is whichever repo they came from. That makes the **cross-repo citation
form** the first thing to check here, not an afterthought.

`schema_version.rs` deserves particular care: it is where the wire contract's own versioning is
reasoned about, so its citations are the ones most likely to name another repo's decision and the
ones whose staleness costs most.

## Why this class keeps being worth running

Across four consecutive days of these sweeps the count of wrong *numbers* has been the less
interesting half of every result. The real yield has been **prose a decision made false** —
`umbrella/063` fixed four things and only two were numbers; the other two were sentences that went
false the same day a decision landed. `core/054`, `ui/040` and `dev-bench/020` found the same shape.

So **read the cited decision's body, then read the sentence around the citation**, in that order.
A number that resolves is not evidence the claim holds. Count wrong numbers and false sentences
separately, and report how many held.

## Bounding — read this before you start

**435 is far more than one unit and you are not expected to finish.** Take **one file**, start with
`src/schema_version.rs` (41 citations, highest cross-repo risk per line), and finish it properly.
Then file `tasks/study-designer/<next>` for the next file, naming which ones remain. A single file
swept carefully, with the two categories counted honestly, is the deliverable. **Do not attempt the
whole repo, and do not skim to raise a number.**

If a sweep turns up that a *decision body* in another repo is wrong rather than the citation, that
is an `inbox/` drop written by **absolute path** to `/home/gabriel/Github/embarch/embarch-doc/inbox/`
— not an edit. You own `embarch-study-designer` only.

## Reserve, for planning

`embarch-study-designer/spec.md` is 9,350/10,240 B — **890 B left, 91.3%** — and
`embarch-study-designer/open.md` is 4,659/5,120 B — **461 B left, 91.0%**. Both are filed against
blocked tasks (`032` and `026`). A comment sweep should touch neither; if yours does and leaves one
in the last 10% of its cap unfiled, file `tasks/study-designer/<next>-compact-study-designer.md` in
the same commit — **your own scope**, never `tasks/doc/`.

## Done when

- [x] One named file fully swept, every citation confirmed against the cited body or fixed, with
      **wrong numbers and false sentences counted separately**.
- [x] Cross-repo citations carry their repo name.
- [x] A follow-up task filed naming the files that remain.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `changelog.d/study-designer-*` fragment.

## Result

Swept `src/schema_version.rs` (the highest cross-repo-risk file, per the bounding
note above) in full: ~53 `decision[s] N` citations read against the cited decision's
body, in `decisions/versioning.md`, `wire.md`, `seals.md`, `removed.md`, `study.md`,
`gatt.md`, `ble.md`, `declares.md`, `payload-meaning.md`, `protocols.md`,
`protocol-exec.md`, `streams.md`, plus the cross-repo bodies they point at
(`embarch-outpost` decision 9, `embarch-dev-bench` decisions 7/18/29/39/41,
`embarch-core` decision 35) and `embarch-decision-reversals.md` rows 18/37/68.
Field names, enum discriminants and constant values the prose asserts (e.g.
`MAX_VERSION_OVERRIDES = 2`, `Action` discriminants 5-11, `StudyStart`'s field
order) were checked against `src/` itself, not just against the docs.

- **Wrong numbers: 0.**
- **False sentences: 0.**
- **Unlabelled cross-repo citations: 1, fixed.** A bare `decisions 29/39` (in the
  v11 wire-history entry) cited `embarch-dev-bench`'s decision 29 (the
  generic-inbound-pipeline decision, topically the one the sentence was actually
  about) without naming the repo — and `embarch-study-designer` has its *own*,
  unrelated decision 29 (the fuzz-testing loop), so the bare form was genuinely
  ambiguous rather than just informal. Relabelled to
  `` `embarch-dev-bench` decision 29 and this crate's decision 39 ``.

**Not done, deliberately, per the task's own bounding note:** `src/study.rs` (52
citations), `src/gatt_extract.rs` (35), `src/lib.rs` (34), and ~273 more lines
across the rest of `src/`. Follow-up filed: `tasks/study-designer/045`.
