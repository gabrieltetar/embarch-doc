# 064 — Citation sweep: outside `src/` (`tools/`, `tests/`, `.cargo/config.toml`)

**State:** done — agent/study-designer/064-citation-sweep-outside-src, 2026-09-17
**Source:** `tasks/study-designer/063`, which closed out `src/` (all twenty
files swept, `044` through `063`) and, per its own instruction to note what
else in the repo needs a citation check, found four files outside `src/`
that this chain has never swept.
**Scope:** study-designer
**Hardware:** none — source/config comments only.
**Owner:** no

## What

`grep -rlIE '[Dd]ecisions? [0-9]+' --include='*.rs' --include='*.toml' .`
(excluding `target/`) turns up, besides the twenty now-swept `src/` files and
`Cargo.toml` (re-confirmed correct by every unit from `061` on), four files
never checked by this chain:

```
8  tests/firmware_test_vectors.rs
7  tools/extract_gatt_config.rs
6  .cargo/config.toml
3  tests/eap_worked_protocols.rs
```

(Grep-matching *lines*, same caveat as every prior unit in this chain: not a
citation-instance count, and per `060`'s finding, not a complete count
either — the case-sensitive, singular-only, no-line-wrap grep undercounts. Read
every file, do not only grep it.)

**`.cargo/config.toml` is very likely the same dated-test-count comment
`053`/`059`–`063` tracked in `src/`'s sweep** ("Also worth doing" section of
those task files) — check whether it duplicates or is independent of
whatever `Cargo.toml`'s own hits say, and whether it still reads 125/125
(116 lib + 9 `firmware_test_vectors`) or has drifted again.

Take these four in the same order the size list suggests, or in whatever
order groups naturally (e.g. `tests/firmware_test_vectors.rs` and
`tests/eap_worked_protocols.rs` together, since both are integration tests).

## Method (carried over unchanged from `044`–`063`)

Read the cited decision's body, then the sentence around the citation, in
that order. Check every number and every implementation-status claim in the
cited sentence, not just the decision number. Count wrong numbers and false
sentences separately, report both honestly even if zero. Check cross-repo
labelling first (a bare `decision N` is same-repo by convention); for every
cross-repo citation, also ask whether a same-repo decision already says the
same thing. Read a cited section to its end before judging it off-topic or
correct.

**`063`'s find, carried forward: a wrong number does not require a dramatic
shape to hide in — it can just be a plain wrong number, repeated.** Four
citations across `src/gatt_names.rs` and `src/vendor.rs` cited "decision 57"
(`decisions/gatt-extract.md`, "The extraction scans the repo, not two files
it was told about" — about repo-walk scope, ignore files, and failure
modes) for claims about **service naming and vendor-wins precedence**,
content that is actually decision 56's ("A characteristic gets a name..." —
whose own body states "Services get names by the same mechanism... Two maps
rather than one, because a merged map would have to guess which lookup a
UUID wanted", nearly verbatim against the citing sentences). All four fixed
to decision 56. Unlike `062`'s same-repo-near-duplicate shape (two different
real sentences citing two different real decisions), this was one number,
wrong everywhere it appeared for this specific claim, in two different
files — worth checking whether the same pattern recurs in these four
un-swept files.

Also still carried forward: `056`'s find (a wrong number that's real,
on-topic, cross-repo, and correctly labelled, shadowed by a nearer
same-repo decision saying the same thing), `058`'s find (a citation number
to a real, existing decision that still never said what the comment
claims), `059`'s find (a citation correctly labelled cross-repo, naming the
wrong decision within that repo/file), `055`'s find (a false sentence
misattributing *where* a feature runs, not just which decision covers it).
See `tasks/study-designer/056`–`062`'s copies of these paragraphs for full
accounts.

**Run the continuation-grep fresh, whole-repo, singular-inclusive:**
`grep -rlIE '[Dd]ecisions?[[:space:]]*$'`. As of `063` it hits the same nine
files it has hit since `062` (`Cargo.toml` plus eight `src/` files), all
fully checked — a fresh run for this unit is expected to add nothing unless
one of these four new files gains a hit.

## Done when

- [x] `tools/extract_gatt_config.rs`, `tests/firmware_test_vectors.rs`,
      `tests/eap_worked_protocols.rs`, `.cargo/config.toml` all fully swept,
      wrong numbers and false sentences counted separately per file.
- [x] Cross-repo citations carry their repo name and are checked per the
      method above.
- [x] Continuation-grep run fresh, any hit reported.
- [x] Say plainly whether any citation-bearing file remains unswept anywhere
      in the repo after this unit (a fresh whole-repo grep, not this task's
      list, is the source of truth).
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `changelog.d/study-designer-*` fragment with the same three numbers
      (citation instances checked, wrong numbers, false sentences).

## Resolution

Census note first: this unit's own line-count list above (8/7/6/3) already
came from a case-insensitive, plural-aware pattern
(`[Dd]ecisions? [0-9]+`), so re-running it case-insensitively with plural
support produced the identical four numbers — no discrepancy to correct
here. A per-file continuation-grep (`[Dd]ecisions?[[:space:]]*$`) found no
line-wrapped citation in any of the four files. A whole-repo run of the same
continuation pattern still hits exactly the same nine files `062`/`063`
found (`Cargo.toml` plus eight `src/` files), all previously fully checked —
nothing added.

Per file, citation instances / wrong numbers / false sentences:

- **`tools/extract_gatt_config.rs`: 7 / 2 / 0.** Two citations of "decision
  57" (`decisions/gatt-extract.md`, "The extraction scans the repo, not two
  files it was told about" — repo-walk scope and failure modes) for claims
  about **service naming**: the module doc's "the service names ... by
  decision 57" and the `service_names` field's own doc comment "Keyed by
  hyphenated service UUID (decision 57)". Both are decision 56's content
  instead — "Services get names by the same mechanism... Two maps rather
  than one, because a merged map would have to guess which lookup a UUID
  wanted" is decision 56's own body, near-verbatim against both citing
  sentences. This is `063`'s exact carried-forward shape (same wrong number,
  same misattributed claim, recurring in a fifth and sixth place) — fixed
  both to decision 56. The "scan report" half of the same module-doc
  sentence correctly cited decision 57 (its body is entirely the repo-walk
  report) and was left unchanged, split out from the service-names half
  rather than folded under one number.
- **`tests/firmware_test_vectors.rs`: 10 / 1 / 0.** "Dumps a `StudyStart`
  carrying schema v12's two new actions (decisions 50/51)" — the two new
  actions the test body actually constructs are `BleSecurity` and
  `BleUnbond`, which are decisions 44 and 50 (`decisions/ble.md`) — decision
  51 (`decisions/study.md`, `Study.dev_bench_log_level`) is a field, not an
  action, and is that same test's schema-v13 addition per its own inline
  comment three lines below ("schema v13's new field is pinned here"), not
  one of the "two new actions" the doc comment is describing. Fixed to
  "decisions 44/50". All other citations checked and correct: decision 36
  (`gatt.md`, the both-languages wire-pinning rule) at two sites, decision 39
  (`streams.md`, `StepResult`'s two retired fields) at one, decision 42
  (`study.md`, `Step.delay_before_ms`) at one, decisions 52/53
  (`payload-meaning.md`'s `StreamEncoding::Struct` + `gatt.md`'s
  `GattMonitorSelected`) together for schema v14, decision 58
  (`protocols.md`, the third seal) and decision 62 (`protocol-exec.md`, the
  reported protocol outcome) each at one.
- **`tests/eap_worked_protocols.rs`: 4 / 0 / 0.** Three comment citations
  (decision 59 twice, decision 61 once) plus one citation embedded in a test
  function's own name (`decision_52s_struct_layout`, no space — caught only
  by reading the file, not by either grep pattern) all check out against
  `decisions/protocols.md` and `decisions/payload-meaning.md`.
- **`.cargo/config.toml`: 6 / 0 / 0.** Independent of `Cargo.toml`'s own
  hits, not a duplicate — `Cargo.toml` carries no dated stack/test-count
  comment at all. Its dated test-count claim ("[Re-measured 2026-09-16] ...
  116 lib + 9 integration = 125") was re-measured today rather than trusted:
  `cargo test --lib -- --list` gives 116, `cargo test --test
  firmware_test_vectors -- --list` gives 9, and a plain `cargo test --
  --list` (default features) confirms 116 + 0 (the `eap-parse`-gated
  integration file compiles to zero tests without the feature) + 9 = 125,
  matching the file's own arithmetic exactly. Decisions 63 (×3), 15, 46 and
  49 all check out against `decisions/limits.md`.

**Total: 27 citation instances checked, 3 wrong numbers, 0 false
sentences.**

**Unswept files remaining in the repo, found by a fresh whole-repo grep (not
restricted to `*.rs`/`*.toml`) run while closing this unit:** `README.md`
(21 matching lines), `.github/workflows/test.yml` (10), and both `.eap`
fixtures under `tests/fixtures/` (2 and 1). None of the twenty-nine files
this chain has now checked (twenty `src/` files, `Cargo.toml`, and these
four) account for those. Filed as `tasks/study-designer/065`. Also checked,
and resolved rather than left for `065`: `README.md`'s "`embarch-dev-bench`
decision 20 records decision 8 as closed" line — the bare `decision 8`
correctly inherits the `embarch-dev-bench` label from the clause before it
(matching `Cargo.toml`'s own already-swept citation of the identical fact),
not a same-repo mislabel against `embarch-study-designer`'s own,
unrelated, decision 8.

Gate: `cargo build --all-targets`, `cargo test --all-targets`, `cargo
clippy --all-targets -- -D warnings` all green in the code worktree (no
source or test logic touched, only doc-comment text). `check-docs.py`,
`check-ownership.py --scope study-designer`, `check-client-names.py` all
green in the doc worktree. `check-doc-size.py --pressure` shows no change
from `064`'s own note — `spec.md`/`open.md` untouched, both still parked
under `032`/`026`.

## Reserve, for planning

`embarch-study-designer/spec.md` and `open.md` are both in the last 10% of
their caps, filed as `tasks/study-designer/032`/`026`, both blocked. As of
`063` neither needed touching for a comment sweep; check fresh
(`scripts/check-doc-size.py --pressure`) rather than trusting this note.
