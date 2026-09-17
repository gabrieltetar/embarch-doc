# 065 — Citation sweep: the crate's top-level readme, its CI workflow, and its `.eap` fixtures

**State:** claimed by agent/study-designer/065-citation-sweep-readme-ci-fixtures, 2026-09-17 13:26
**Source:** `tasks/study-designer/064`, which closed the four files `063`
found outside `src/` (`tools/extract_gatt_config.rs`,
`tests/firmware_test_vectors.rs`, `tests/eap_worked_protocols.rs`,
`.cargo/config.toml` — 27 citation instances, 3 wrong numbers, 0 false
sentences) and, per its own `Done when` item to say plainly whether any
citation-bearing file remains unswept, ran the whole-repo grep (not
restricted to `*.rs`/`*.toml`) and found four more this chain has never
touched.
**Scope:** study-designer
**Hardware:** none — doc/config/text comments only.
**Owner:** no

## What

`find . -path ./target -prune -o -type f -print | xargs grep -lIE
'[Dd]ecisions? [0-9]+'` (case-insensitive, plural-aware per `064`'s method)
turns up, besides the 20 `src/` files, `Cargo.toml` and the four files `064`
swept, four files never checked by this chain:

```
21  README.md
10  .github/workflows/test.yml
 2  tests/fixtures/gwf1_batch.eap
 1  tests/fixtures/bds_batch_download.eap
```

(Line count from the pattern above, same caveat as every prior unit: not a
citation-instance count — `README.md`'s `decisions 7, 23` line and its
`decisions 34/35` line are each one line and two citations, and neither a
plural nor a mid-sentence continuation is ruled out just because this pass
did not find one. Read every file; do not only grep it.)

**`.github/workflows/test.yml` has this chain's first cross-repo citations
outside `src/`'s own handful:** line 49's `embarch-umbrella decisions 27/29`
and line 73's `embarch-umbrella decisions 27/29; embarch-study-designer
decision 65` are both explicitly labelled — check them against
`embarch-umbrella/decisions.md` the way `056`/`059` checked cross-repo
citations in `src/`.

**`README.md` line 80 already checked while filing this task, reported so
the next unit does not re-open it:** `` `embarch-dev-bench` decision 20
records decision 8 as closed, and the real `` — the bare `decision 8` reads
as inheriting `embarch-dev-bench`'s label from the clause before it, not as
`embarch-study-designer`'s own decision 8 (`crate.md`'s — a path-dependency
choice, unrelated). Confirmed correct: `Cargo.toml`'s own comment (already
swept, `06x` chain) makes the identical cross-repo claim in full — "embarch-
dev-bench decision 8 is closed and the handler is at src/ffi.rs:37" — so
this is the same fact, same repo, label carried by convention rather than
missing. No defect; still count it as one checked instance in this unit's
tally rather than skipping it as pre-resolved.

## Method (carried over unchanged from `044`–`064`)

Read the cited decision's body, then the sentence around the citation, in
that order. Check every number and every implementation-status claim in the
cited sentence, not just the decision number. Count wrong numbers and false
sentences separately, report both honestly even if zero. Check cross-repo
labelling first (a bare `decision N` is same-repo by convention); for every
cross-repo citation, also ask whether a same-repo decision already says the
same thing. Read a cited section to its end before judging it off-topic or
correct.

Run a fresh whole-repo grep at the end (case-insensitive, plural-inclusive,
continuation-inclusive per `064`'s three carried lessons) and report any hit
outside the files this chain has now swept — `README.md`, `test.yml`, and
the two `.eap` fixtures are the last ones this pass knows about, but this
task's own count is not the source of truth for the next unit; a fresh grep
is.

## Done when

- [ ] `README.md`, `.github/workflows/test.yml`,
      `tests/fixtures/bds_batch_download.eap`,
      `tests/fixtures/gwf1_batch.eap` all fully swept, wrong numbers and
      false sentences counted separately per file.
- [ ] Cross-repo citations (at least `test.yml`'s two, and `README.md`
      line 80 resolved one way or the other) carry their repo name and are
      checked per the method above.
- [ ] Continuation-grep run fresh, any hit reported.
- [ ] Say plainly whether any citation-bearing file remains unswept anywhere
      in the repo after this unit (a fresh whole-repo grep, not this task's
      list, is the source of truth).
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `changelog.d/study-designer-*` fragment with the same three numbers
      (citation instances checked, wrong numbers, false sentences).

## Reserve, for planning

`embarch-study-designer/spec.md` and `open.md` are both in the last 10% of
their caps, filed as `tasks/study-designer/032`/`026`, both blocked. As of
`064` neither needed touching for a comment sweep; check fresh
(`scripts/check-doc-size.py --pressure`) rather than trusting this note.

## Supervisor notes (leg 137, 2026-09-17)

1. **Reserve, read by me at dispatch:** `embarch-study-designer/spec.md`
   **9,350/10,240 B (890 B left)** and `open.md` **4,659/5,120 B (461 B
   left)**, both filed and both blocked — **do not write into either.** If
   your work pushes a third file into the band, file
   `tasks/study-designer/<NNN>-compact-study-designer.md` in the same commit.
   Almost all of this unit's edits should land in the code repo, not in
   `embarch-doc`.
2. **A clean sweep is a real result.** Four of this chain's recent units found
   zero defects and four found real ones; do not manufacture a correction to
   have something to report. Report the three numbers honestly per file.
3. **Say plainly whether the chain should continue.** The suite has no single
   added-up figure for this nine-unit chain and the last few handoffs have
   asked whether it is still earning its keep. Your `Done when`'s fresh
   whole-repo grep is the evidence: if nothing citation-bearing remains
   unswept, say so and say the chain is finished rather than filing a
   successor out of habit.
4. You own exactly one sub-project: `embarch-study-designer`.
