# 046 — Citation sweep: `src/` remainder after `study.rs`

**State:** done — leg 111, 2026-09-13, branch `agent/study-designer/046-src-citation-sweep-gatt-extract`.
**Source:** `tasks/study-designer/045`, which swept `src/study.rs` (the second
of four files `044` named) and left the rest.
**Scope:** study-designer
**Hardware:** none — source comments only; nothing is built for a board.
**Owner:** no

## What

`044` counted 435 `decision[s] N`-matching lines across `src/`. Two of the four
files it named are now swept:

```
41  src/schema_version.rs — swept in 044
52  src/study.rs          — swept in 045
35  src/gatt_extract.rs   — not yet swept
34  src/lib.rs            — not yet swept
```

…and ~273 more lines across the rest of `src/` (every other file), also not yet
swept.

Take one file — `src/gatt_extract.rs` next, per `044`'s own ordering — read
every cited decision's body against the sentence around the citation, and fix
what is wrong. Count wrong *numbers* and false *sentences* separately, per the
method below. When you run out of budget, file the next
`tasks/study-designer/<next>` naming exactly which files remain, the same way
this one does.

## Why now

**`check-decision-refs.py` resolves decision numbers only inside `*.md`.** A
wrong number or a stale sentence in a source comment fails no gate and never
has — `embarch-study-designer` is a shared crate (`embarch-api`,
`embarch-core`, `embarch-ui`, `embarch-umbrella` all depend on it), so its
comments are read from four other repos' default citation index, which makes a
bare `decision N` genuinely ambiguous here in a way it is not in a leaf repo.

## Method (carried over from `044`/`045`, confirmed useful both times)

**Read the cited decision's body, then read the sentence around the citation,
in that order.** A number that resolves is not evidence the claim holds — the
real yield across five days of these sweeps in other repos, and both sweeps in
this one, has been prose a decision made false or a citation pointing at the
wrong (but real) decision, not a bare typo. Count the two categories
separately and report both, honestly, even if one or both is zero — "checked
N, found none" is a legitimate result.

**Check cross-repo labelling as the first pass, specifically in this repo.** A
bare `decision N` is same-repo by convention; another repo's decision must
read `<repo> decision N` (e.g. `embarch-dev-bench decision 38`) — general form
still open, owner-reserved, `tasks/doc/055`. `044` found one in
`schema_version.rs` (a bare "decisions 29/39" where 29 was
`embarch-dev-bench`'s); `045` found a second, structurally identical one in
`study.rs`: a bare "Decision 38" whose content matched `embarch-dev-bench`'s
own decision 38 verbatim, while this repo's *own* decision 38 (a real, unrelated
decision — the saved-study library) sat two paragraphs below, correctly bare.
Two same-repo collisions in two files sweeping the same four-file set is
enough to say: check every bare `decision N` against *this crate's own*
decisions.md/decisions/*.md first, whether or not the topic looks foreign.

**A wrong number is not always a nearby-digit typo.** `045` found three: one
cited a real decision in the wrong *repo* (`embarch-api decision 26`, an
unrelated field, where `embarch-api` decisions 27/28 was the actual match);
one attributed a structural rule to the decision that used it rather than the
decision that established it (`decision 39` instead of `decision 17`, where
decision 58's own text names decision 17 explicitly); one over-cited a paired
decision from a different table row (`decisions 20/21` where the crate's own
Was/Becomes table pairs 20 with 25 for a different channel and attributes the
cited variant to 21 alone). All three needed the decision's own body compared
against the specific claim, not just "does N exist."

## Files already swept (do not re-do)

- `src/schema_version.rs` — done in `044`. ~53 citations. Zero wrong numbers,
  zero false sentences, one unlabelled cross-repo citation (fixed).
- `src/study.rs` — done in `045`. 52 citations read against
  `decisions/seals.md`, `study.md`, `declares.md`, `removed.md`, `ble.md`,
  `gatt.md`, `streams.md`, `protocols.md`, `protocol-exec.md`,
  `payload-meaning.md`, `authoring.md`, plus `embarch-dev-bench` decisions
  18/38/39, `embarch-api` decisions 26(wrong→27/28)/36, `embarch-topology`
  decision 3, and `embarch-decision-reversals.md` row 37. **3 wrong numbers, 0
  false sentences, 1 unlabelled cross-repo citation — all fixed.**

## Done when

- [x] One named file (`src/gatt_extract.rs`, unless a reason is given to
      reorder) fully swept, wrong numbers and false sentences counted
      separately. **36 citations read against `decisions/gatt-extract.md` (33,
      56, 57), `decisions/gatt.md` (31, 32), `decisions/seals.md` (18),
      `decisions/crate.md` (23). 3 wrong numbers (a design fact belonging
      solely to decision 56 — service identifiers get names "by the same
      mechanism" as characteristics — was additionally credited to decision 57
      in three separate comments: `GattSymbolKind`'s doc, `parse_gatt_services`'s
      doc, and a test doc comment. `git log --follow -p` on
      `decisions/gatt-extract.md` confirmed the service-naming text was folded
      into decision 56 "amended the same session" as characteristics, with no
      connection to decision 57, which is entirely about repo-wide scan scope).
      2 false sentences (the module doc's "Two failure modes decision 57 adds
      outright" undercounts — the decision's own text names three, the third
      — `NoSourceFilesFound` — already documented a few lines above under its
      own citation; and `ExtractedGatt`'s doc claimed decision 33 "exists to
      provide" *byte-for-byte* comparability, which decision 33's own text
      explicitly disclaims — "weaker than this decision claimed... compare
      them as sets" — while a second doc comment 20 lines below already used
      the corrected framing). 0 unlabelled cross-repo citations (the file's
      one cross-repo cite, `embarch-ui decision 17`, was already correctly
      labelled and verified against `embarch-ui/decisions/gatt-capture.md`'s
      decision 17). All 5 fixed.**
- [x] Cross-repo citations in it carry their repo name. (Already did; verified
      correct against the source repo.)
- [x] A follow-up task filed naming the files that remain (or, if this closes
      out `src/`, saying so and closing the sweep). `tasks/study-designer/047`
      names `src/lib.rs` next, plus the rest of `src/` unchanged.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10). `cargo build`,
      `cargo test` (18/18 `gatt_extract` tests, full suite), `cargo clippy
      --all-targets --all-features -- -D warnings` all clean.
- [x] `changelog.d/study-designer-*` fragment.

## Reserve, for planning

`embarch-study-designer/spec.md` and `open.md` were both inside the last 10%
of their caps as of `045`'s dispatch, with both compaction tasks (`032`, `026`)
blocked. Check `scripts/check-doc-size.py` fresh rather than trusting this
number — a comment sweep should not need either file regardless. If this sweep
turns up a question worth recording, file it as `tasks/study-designer/<next>`
rather than adding to `open.md`.

## Dispatch note — leg 111, 2026-09-13

**Reserve, re-checked today and unchanged in substance.** `embarch-study-designer/spec.md`
**9,350/10,240 B (890 B left)** and `embarch-study-designer/open.md` **4,659/5,120 B (461 B left)**
are both in reserve, and both are filed against `blocked` compaction tasks (`032` and `026`
respectively, each `In flux: yes`). A source-comment sweep should touch neither. **If it does,**
`.claude/leg.md`'s rule applies: a blocked compaction task parks the pass, not the reserve, so the
file you write into is the file you compact in the same unit, carrying that task's
`Must not delete:` list.

**The next free number in this scope is 047**, so the remainder task you file at the end of your
budget is `tasks/study-designer/047-…` — **in `tasks/study-designer/`, your own scope**, never
`tasks/doc/`, which `check-ownership.py` refuses to every worker.

**Sweep `src/gatt_extract.rs` (35 lines) — that is `044`'s ordering and it is the file to take.**
Only move on to `src/lib.rs` if it is genuinely cheap once `gatt_extract.rs` is finished; a
complete file beats two half-swept ones, and the remainder task is how the rest gets carried.

**One repo, one branch, one task.** Code in `embarch-study-designer`, docs in `embarch-doc`, both
on `agent/study-designer/046-src-citation-sweep-gatt-extract`. `embarch-study-designer` has no
path-dep siblings, so its worktree needs no symlinks.
