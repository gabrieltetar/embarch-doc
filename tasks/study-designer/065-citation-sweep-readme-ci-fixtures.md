# 065 — Citation sweep: the crate's top-level readme, its CI workflow, and its `.eap` fixtures

**State:** done — agent/study-designer/065-citation-sweep-readme-ci-fixtures, 2026-09-17 13:26
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

- [x] `README.md`, `.github/workflows/test.yml`,
      `tests/fixtures/bds_batch_download.eap`,
      `tests/fixtures/gwf1_batch.eap` all fully swept, wrong numbers and
      false sentences counted separately per file.
- [x] Cross-repo citations (at least `test.yml`'s two, and `README.md`
      line 80 resolved one way or the other) carry their repo name and are
      checked per the method above.
- [x] Continuation-grep run fresh, any hit reported.
- [x] Say plainly whether any citation-bearing file remains unswept anywhere
      in the repo after this unit (a fresh whole-repo grep, not this task's
      list, is the source of truth).
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `changelog.d/study-designer-*` fragment with the same three numbers
      (citation instances checked, wrong numbers, false sentences).

## Resolution

**A clean sweep. Zero wrong numbers, zero false sentences, in all four
files.** Every citation checked was read against its decision's body per the
carried-over method (read the cited decision, then the sentence around the
citation, check every number and every implementation-status claim).

Per file, citation instances checked / wrong numbers / false sentences:

- **`README.md`: 35 / 0 / 0.** Nineteen module-table rows (lines 25-45) all
  cite exactly what `src/`'s own doc comments cite for the same module —
  verified line-for-line against `src/gatt.rs`, `src/eap_interp.rs`,
  `src/eap_parse.rs`, `src/gatt_extract.rs`, `src/registry.rs`,
  `src/merged_actions.rs`, `src/study_builder.rs`, `src/eap.rs`, which this
  chain already checked in `044`-`063`; the README is a mirror, not an
  independent source, and it mirrors correctly everywhere. `decisions
  58-62` (line 39, the `eap` module) is a range naming five real decisions
  (58, 59, 60, 61, 62), all confirmed to be about protocol manifests/
  execution — counted as 5 citations, not 1, since each was individually
  read. Line 14's `decision 17` is a bare format-illustration example
  ("cite it by decision number (`decision 17`)"), not a substantive claim;
  counted and confirmed the number is real. Line 80's cross-repo
  `embarch-dev-bench decision 20 records decision 8 as closed` was already
  checked while this task was filed (see "already checked" note above) and
  is confirmed correct against `embarch-dev-bench/decisions/platform.md`'s
  own decisions 8 and 20 — re-verified here rather than re-opened, counted
  as 1 checked instance per that note's own instruction.
- **`.github/workflows/test.yml`: 16 / 0 / 0.** All ten citing lines check
  out. The two cross-repo citations (`embarch-umbrella decisions 27/29`,
  lines 49 and 73) match `embarch-umbrella/decisions/release.md`'s own text
  almost verbatim ("whichever gains a release workflow first inherits the
  obligation to copy this job"; study-designer is confirmed among "the four
  sub-projects with no release workflow at all"). Same-repo `decision 65`
  (four sites) matches `decisions/ci.md`'s decision 65. `decisions 5, 15, 46`
  (default cell), `decision 46` (alloc cell) and `decisions 7, 23` (ffi cell)
  all match `decisions/ci.md`'s own per-cell descriptions verbatim — this
  workflow file and the crate's own CI decision doc were written to agree,
  and they still do. `decision 23` (line 14, `--locked`/Cargo.lock) matches
  `decisions/ci.md`'s identical phrasing ("this crate being the FFI build
  root (decision 23)") rather than being a defect introduced by this file.
- **`tests/fixtures/gwf1_batch.eap`: 3 / 0 / 0.** `decision 59`'s split
  (host-side render-only primitives below `repeat`) matches
  `decisions/protocols.md` decision 59 exactly. `decision 62`/`decision 52`
  (a frame lowering into a `StructLayout`) matches `decisions/protocol-exec.md`
  decision 62's second half almost verbatim ("a frame flat enough to be one
  lowers into decision 52's own layout").
- **`tests/fixtures/bds_batch_download.eap`: 1 / 0 / 0.** `decision 57`
  ("Structurally the state machine of the real Batch Data Service on
  `reference-dut-fw`... which decision 57 made extractable") reads as
  crediting decision 57's widened repo-wide GATT-extraction scan with making
  `reference-dut-fw` (the same repo `src/gatt_extract.rs`/`tools/
  extract_gatt_config.rs` name) fully scannable — not as claiming the
  protocol state machine itself was extracted, which the file's own header
  explicitly disclaims ("This is a TEST FIXTURE, not a description of that
  firmware's real opcodes"). No contradiction with decision 58's
  never-infer principle. Correct on the more careful reading.

**Total this unit: 55 citation instances checked, 0 wrong numbers, 0 false
sentences.**

**Fresh whole-repo grep run at close (`find . -path ./target -prune -o -type f
-print | xargs grep -lIE '[Dd]ecisions? [0-9]+'`, not restricted to
`*.rs`/`*.toml`): 33 files, all now accounted for** — the 24 `src/*.rs`
files (all swept `044`-`063`, including `eap_interp.rs`/`gatt_names.rs`/
`records.rs`/`vendor.rs`, confirmed via `git log` showing each already
carries a citation-sweep-era fix commit even though `063`'s compressed
"twenty files" summary didn't name all four), `Cargo.toml`, the four files
`064` swept, and the four files this unit swept. **No citation-bearing file
remains unswept anywhere in the repo.** The fresh continuation-grep
(`[Dd]ecisions?[[:space:]]*$`) still hits only the same nine files
(`Cargo.toml` + eight `src/` files) this chain has checked since `062` —
none of this unit's four files, no new hit.

**The nine-unit chain (`057`-`065`) is finished, not a candidate for a
successor.** The evidence is the fresh grep above, which is the source of
truth this and every prior unit in the chain was told to trust over its own
task list: zero unswept files. Chain-wide running total, taken directly from
each unit's own stated numbers (`063`'s own tally for `044`-`062`: 500
instances / 18 wrong / 7 false; `064`'s tally: 27 / 3 / 0; this unit: 55 / 0
/ 0): **582 citation instances checked chain-wide, 21 wrong numbers fixed,
7 false sentences fixed. `065` itself added 55 checked and 0 to both defect
counts** — a clean unit closing a chain that found real defects in most of
its earlier units. Nothing citation-bearing is left to file a `066` against.

Gate: `cargo build --all-targets`, `cargo test`, `cargo clippy --all-targets
-- -D warnings` all green in the code worktree (no source edits — a clean
sweep needs none). `check-docs.py` (11/11), `check-client-names.py --repo`
(code worktree), `check-ownership.py --scope study-designer` (doc) and
`check-ownership.py --code-repo` (code) all green. `check-doc-size.py
--pressure` unchanged from `064`'s note: `spec.md`/`open.md` both still
parked under `032`/`026`, neither touched.

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
