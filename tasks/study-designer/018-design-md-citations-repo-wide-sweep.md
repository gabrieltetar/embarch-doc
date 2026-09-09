# 018 — `design.md §3 decision N` citations remain in 22 other `src/` files

**State:** done, 2026-09-09
**Source:** `tasks/study-designer/017`, while fixing `src/schema_version.rs` — that task's Done-when
bullet 3 required a repo-wide `grep -rn 'design.md' src/` and reporting what is left.
**Scope:** study-designer
**Hardware:** none
**Owner:** no

## Supervisor's dispatch note, leg 058 (2026-09-09, burndown)

**Doc-size reserve in `embarch-study-designer`** — two files are inside the last 10% of their cap.
Both are still writable and the gate still passes; plan around them rather than discovering them:

- `embarch-study-designer/spec.md` — 9,600/10,240 B, **640 B left**
- `embarch-study-designer/open.md` — 4,662/5,120 B, **458 B left**

Both are already filed against `tasks/study-designer/006-compact-study-designer.md` (state `open`,
not blocked), so you owe no new compaction task unless your work pushes a *different* file into
reserve. **This unit should not need either file**: it is a `src/` doc-comment sweep, and the
"update spec.md/decisions.md/open.md" line in the Done-when below is boilerplate, not a checklist.
Touch them only if this sweep genuinely made a statement in one of them false.

**This leg runs in burndown mode: do not author a new numbered decision.** If the sweep turns out
to need one, stop and say so in your report instead. Nothing here should — the correct spelling is
already fixed by `DOC-CONVENTIONS.md` and by unit 017's precedent.

## What

`src/schema_version.rs` is now clean (unit 017), but the same retired `design.md §3 decision N` /
bare `design.md §N.N` form is still present in **290 occurrences across 23 other files** in `src/`
as of this task's filing:

```
study.rs 44, limits.rs 35, streams.rs 34, study_builder.rs 24, result.rs 20, protocol.rs 19,
ffi.rs 17, lib.rs 13, gatt.rs 13, sample.rs 11, gatt_extract.rs 10, outpost.rs 7,
merged_actions.rs 6, eap.rs 6, decoder.rs 6, crc.rs 6, registry.rs 5, bounded.rs 4, ids.rs 3,
vendor.rs 2, gatt_names.rs 1, eap_parse.rs 1, eap_interp.rs 1
```

Two sub-flavors, both need the same fix:

- `design.md §3 decision N` (or `<repo>/design.md §3 decision N` for another sub-project's) — the
  exact defect unit 017 fixed in `schema_version.rs`. Correct spelling: bare `decision N` (own) or
  `<repo> decision N` (another's), per `DOC-CONVENTIONS.md` *Referring to a decision*.
- Bare `design.md §N.N` / `design.md §N` with **no decision number** (e.g. `design.md §4.7`,
  `design.md §4.3a`, `design.md §7`) — these cite a *section* of a file that no longer exists at
  all (split into `spec.md`/`open.md`/`decisions/<mission>.md` on 2026-09-04, with no section
  numbering carried forward). Unit 017 hit exactly one of these (`schema_version.rs` line 239,
  `design.md §5.1`) and resolved it by dropping the stale pointer rather than inventing an
  unverifiable replacement citation — the same approach likely applies here, file by file.

## Why now

This is the same defect class as `tasks/api/040` (embarch-api's six MCP tool descriptions) and
`embarch-study-designer` decision 57's rule for tool descriptions — nothing has swept Rust doc
comments suite-wide, and `cargo doc` does not flag a citation that is merely wrong (only a broken
*intra-doc link*). `embarch-study-designer` decision 68 keeps `cargo doc` warnings out of the gate,
so nothing will ever catch these on its own.

## Scope note

**Doc comments only, in `embarch-study-designer`.** Same rule as unit 017: a citation *about*
another sub-project (e.g. `embarch-dev-bench/design.md §3 decision N`, `embarch-outpost/design.md
§3 decision N`) lives in this crate's file and is fixed in this crate's file — never by editing the
other repo. **Verify every decision number against the named sub-project's current `decisions.md`
index before writing it**, and if a number does not resolve, stop and report it rather than
guessing which number was meant (`tasks/api/040`'s `enroll_probe` trap).

Given the size (290 occurrences, 23 files), this is very likely **more than one unit's worth** —
consider splitting by file or by cluster (e.g. `study.rs`+`study_builder.rs`+`limits.rs` together
since they share many of the same decision numbers) rather than one giant diff.

## Done when

- [x] Every `design.md` occurrence in `src/*.rs` (outside `schema_version.rs`, already done) is
      either a bare `decision N` / `<repo> decision N` citation, or — where it names a section
      number with no decision attached — resolved without inventing a new unverifiable pointer.
- [x] Every decision number verified to resolve against the named sub-project's current
      `decisions.md` index; the task says which ones were checked and how.
- [x] `grep -rn 'design\.md' src/` reports nothing left.
- [x] **The bare `§N.M` section references are swept too**, and `grep -rn '§' src/` says what is
      left. Added by the supervisor at the fold of `study-designer/017`: that unit's Done-when named
      only `§3`, so it left `§4.3a`, `§4.3b` and `§4.8` standing in `schema_version.rs` — three
      section numbers of the *same* deleted `design.md`, now with no file name in front of them to
      show that the file is gone. **A bare `§4.3a` is worse than `design.md §4.3a`, not better**: it
      reads like a section of the file you are in. Whoever runs this sweep must decide, per
      occurrence, which of `spec.md` / `decisions/<mission>.md` now holds that content and cite it —
      or drop the pointer, as `017` did for the one `§5.1`. That is judgement, not a `sed`.
- [x] `cargo doc --no-deps --all-features` (after `cargo clean -p embarch-study-designer`) still 0
      warnings.
- [x] Gate green; `changelog.d/study-designer-*` fragment.

## Closed 2026-09-09

Swept all 290 occurrences across the 23 files named at filing, plus `schema_version.rs`'s
leftover `§4.3a`/`§4.3b`/`§4.8` (unit 017's own residue), plus the same defect found (while
sweeping) in three more places not counted at filing: `Cargo.toml`'s doc comments (~15
occurrences), `tests/eap_worked_protocols.rs`, `tests/firmware_test_vectors.rs`,
`tests/fixtures/*.eap`, `tools/extract_gatt_config.rs`, this crate's own `README.md`, and one
bare `§7` in `.github/workflows/test.yml`. `grep -rn 'design\.md\|§' .` (excluding `target/`)
now reports nothing in this repo outside three lines that legitimately cite `spec.md`'s own
live numbered sections (`§1`, `§3`, `§7` — used where old `design.md §4.x`/`§7` prose mapped
cleanly onto that file's current `## N.` headings) and `CLAUDE.md`'s references into
`embarch-doc`'s still-current `DOC-PROTOCOL.md`/`embarch-dev-workflow.md` sections, which were
never stale.

**Two sub-flavors handled, both file by file, no `sed` over judgement calls:**
- `design.md §3 decision N` / `<repo>/design.md §3 decision N` → bare `decision N` (own repo) or
  `<repo> decision N` (another's), per `DOC-CONVENTIONS.md`. Also handled a bare `§3 decision N`
  form (no `design.md`/repo prefix at all) found alongside the counted occurrences, on the same
  rule.
- Bare `design.md §N.N` (a *section*, no decision attached) → resolved per occurrence against
  what now holds that content: `interfaces/types.md` (Study/Step/Action), `interfaces/gatt-types.md`
  (GATT discovery + transcript types, old §4.3a/§4.3b), `interfaces/taps.md` (stream taps, old
  §4.8), `interfaces/decoders.md` (Sample + struct payload layouts, old §4.7/§4.8a/§5.2),
  `interfaces/eap.md` (`.eap` protocol manifests, old §4.9), `spec.md §1`/`§3`/`§7` where the
  prose matched that file's own current section, `open.md` where it named an actual open
  question, or dropped outright (no replacement invented) where nothing current says the same
  thing — e.g. `ffi.rs`'s stale "BleConnect/DataExchange dispatch deferred" pointer, and several
  `milestone-9.md`/`milestone-11.md`/`embarch-ui/milestone-1.md` references (those files no
  longer exist at all — same treatment as a dead `design.md` section).

**Decision numbers verified by**: for each sub-project a referenced decision named
(`embarch-study-designer`, `embarch-dev-bench`, `embarch-core`, `embarch-outpost`,
`embarch-topology`, `embarch-api`, `embarch-ui`), built the full set of decision numbers that
sub-project's `decisions.md` + `decisions/*.md` headings (`### N — ...`, including comma-joined
headings like `### 4, 10 —`) actually declare, then checked every number cited from this crate
against that set. All resolved — own-repo `embarch-study-designer` numbers used span 2-70,
all present (contiguous 1-70 range); `embarch-dev-bench` 7/8/9/10/11/18/21/27/39 all present
(range has gaps but every cited number is one of the present ones); `embarch-core` 30/31/35;
`embarch-outpost` 4/9/10/11/12; `embarch-topology` 3/18; `embarch-api` 26/36/40; `embarch-ui`
11/15 — all present. None needed reporting as unresolved.

**No new decision authored** (this leg runs in burndown mode, per this task's dispatch note). None
of the section-citation fixes needed one — `DOC-CONVENTIONS.md`'s decision-reference rule and
unit 017's precedent covered every case.

**Found but out of this task's scope, left as-is:** this crate's own `README.md` describes a
`core-validation` feature and `signal`/`validation` modules that no longer exist in `Cargo.toml`
or `src/` at all (removed by decision 48, and `gatt-extract`/`study-ui`/`eap-parse` never added
to the README's Features list) — a real staleness problem, but a content rewrite, not a
citation-format fix, and out of scope for this unit. Filed as
`tasks/study-designer/024-readme-describes-a-feature-set-that-no-longer-exists.md`.

**Gate:** `cargo build`/`cargo test --all-features`/`cargo clippy --all-targets --all-features -- -D warnings`
all clean; `cargo build` also verified individually for `--no-default-features`, `--features
gatt-extract`, `--features study-ui`, `--features eap-parse`, `--features ffi` (the CI feature
matrix, decision 64). `cargo doc --no-deps --all-features` after `cargo clean -p
embarch-study-designer`: 0 warnings. `embarch-doc`'s `scripts/check-docs.py`,
`scripts/check-client-names.py --repo`, and `scripts/check-ownership.py` all green (see commit
for exact output). `spec.md`/`decisions.md`/`open.md` untouched — this unit never made a
statement in them false.
