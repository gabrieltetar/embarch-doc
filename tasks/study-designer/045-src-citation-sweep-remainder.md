# 045 — Citation sweep: `src/` remainder after `schema_version.rs`

**State:** claimed by agent/study-designer/045-study-rs-citations, 2026-09-13 20:00
**Source:** `tasks/study-designer/044`, which swept `src/schema_version.rs` (the first
of four files it named) and left the rest.
**Scope:** study-designer
**Hardware:** none — source comments only; nothing is built for a board.
**Owner:** no

## What

`044` counted 435 `decision[s] N`-matching lines across `src/`, named four files as the
place to start, and bounded itself to one:

```
52  src/study.rs        — not yet swept
41  src/schema_version.rs — swept in 044
35  src/gatt_extract.rs — not yet swept
34  src/lib.rs          — not yet swept
```

…and ~273 more lines across the rest of `src/` (every other file), also not yet swept.

Take one file — `src/study.rs` next, per `044`'s own ordering — read every cited
decision's body against the sentence around the citation, and fix what is wrong.
Count wrong *numbers* and false *sentences* separately, per the method below. When
you run out of budget, file the next `tasks/study-designer/<next>` naming exactly
which files remain, the same way this one does.

## Why now

**`check-decision-refs.py` resolves decision numbers only inside `*.md`.** A wrong
number or a stale sentence in a source comment fails no gate and never has —
`embarch-study-designer` is a shared crate (`embarch-api`, `embarch-core`,
`embarch-ui`, `embarch-umbrella` all depend on it), so its comments are read from
four other repos' default citation index, which makes a bare `decision N` genuinely
ambiguous here in a way it is not in a leaf repo.

## Method (carried over from `044`, confirmed useful there)

**Read the cited decision's body, then read the sentence around the citation, in
that order.** A number that resolves is not evidence the claim holds — the real
yield across four days of these sweeps in other repos has been prose a decision
made false, not a wrong number. Count the two categories separately and report
both, honestly, even if one or both is zero — "checked N, found none" is a
legitimate result.

**Check cross-repo labelling as the first pass, specifically in this repo.** A bare
`decision N` is same-repo by convention; another repo's decision must read
`<repo> decision N` (e.g. `embarch-core decision 37`) — general form still open,
owner-reserved, `tasks/doc/055`. `044` found exactly one of these: `schema_version.rs`
line ~168 cited a bare "decisions 29/39" where 29 belonged to `embarch-dev-bench`
(topically confirmed: dev-bench's own decision 29 is the generic-inbound-pipeline
decision the sentence was actually about) while `embarch-study-designer`'s *own*
decision 29 — a real, different decision — is about the fuzz-testing loop and has
nothing to do with the sentence. That collision (a same-repo decision existing at
the same number as the intended foreign one) is exactly the failure mode this
repo's cross-repo-first instruction exists to catch, and it is worth checking for
specifically in whatever file you take next.

## Files already swept (do not re-do)

- `src/schema_version.rs` — done in `044`. ~53 citations read against
  `decisions/versioning.md`, `wire.md`, `seals.md`, `removed.md`, `study.md`,
  `gatt.md`, `ble.md`, `declares.md`, `payload-meaning.md`, `protocols.md`,
  `protocol-exec.md`, `streams.md`, plus `embarch-outpost` decision 9,
  `embarch-dev-bench` decisions 7/18/29/39/41, `embarch-core` decision 35, and
  `embarch-decision-reversals.md` rows 18/37/68. Zero wrong numbers, zero false
  sentences, one unlabelled cross-repo citation (fixed).

## Done when

- [ ] One named file (`src/study.rs`, unless a reason is given to reorder) fully
      swept, wrong numbers and false sentences counted separately.
- [ ] Cross-repo citations in it carry their repo name.
- [ ] A follow-up task filed naming the files that remain (or, if this closes out
      `src/`, saying so and closing the sweep).
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `changelog.d/study-designer-*` fragment.

## Reserve, for planning (added at dispatch, 2026-09-13 20:00)

Two `embarch-study-designer` docs are inside the last 10% of their caps, and **both of their
compaction tasks are `blocked`**, so nothing is going to shorten them before you run:

- `embarch-study-designer/spec.md` — 9,350/10,240 B, **890 B left, 91.3%** (`tasks/study-designer/032`, blocked)
- `embarch-study-designer/open.md` — 4,659/5,120 B, **461 B left, 91.0%** (`tasks/study-designer/026`, blocked)

A comment sweep should not need either file, and the expectation is that you touch neither. But
**`open.md` is the one you might reach for by habit** — if this sweep turns up a question worth
recording, file it as `tasks/study-designer/<next>` instead, where there is no cap pressure at all.
461 B is about one bullet. If you do end up spending reserve in any `embarch-study-designer` doc and
nothing has filed for it, file `tasks/study-designer/<next>-compact-study-designer.md` in the same
commit — **your own scope**, never `tasks/doc/`.
