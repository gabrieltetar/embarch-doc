# 005 — `doctor --prune` was decided, and neither half of decision 26 was built

**State:** done by agent/umbrella/005-doctor-prune, 2026-09-05
**Source:** embarch-umbrella/002 (design-only decisions audit, 2026-09-03) — decision 26 read against the source and found unbuilt
**Scope:** umbrella
**Hardware:** none

**Doc-size reserve (supervisor, 2026-09-05):** both `umbrella` docs are in the last
10% of their caps and **both are already filed against
`tasks/umbrella/009-compact-docs.md`** — `spec.md` 97.6% (243 B left), `open.md`
93.5% (335 B). `spec.md`'s `doctor` row is one of the things this task updates, so
plan for ~243 B: replace text rather than append it. You owe **no new compaction
task** — 009 covers both — but say so in your report if you spent enough of either
reserve that 009 became urgent.

## What

`embarch-umbrella` decision 26 gives `study_results/` retention and per-target
build-directory pruning an explicit policy. Neither half is built: there is no
`--prune` flag on `doctor`, no occurrence of the word in the crate, and — the
part that was never opt-in — **no unconditional reporting either.** Decision 26
says `doctor` *always* reports how many result entries exist and their size, and
how many distinct build-directory combinations exist per project. `doctor`
assembles exactly checks 1–15 and none of them reads `study_results/` or measures
the build tree.

Two separable pieces, and the reporting one is much cheaper:

1. A new check that always reports result count + size and build-directory
   combinations per project. Informational; never fails.
2. `--prune`, opt-in only, deleting results older than a configurable age and
   build directories for target combinations no longer among the project's valid
   targets — **never a currently-valid target's directory regardless of age.**

## Why now

"Grows forever" is still literally what happens, and the reporting half would at
least make it visible. Worth asking first whether decision 26 is still wanted at
all, or should be retired: nothing has reported disk pressure from this.

## Done when

- [x] Either both halves built, or decision 26 retired per `DOC-CONVENTIONS.md`
      with a one-line tombstone saying why. — **Neither: the third option the
      dispatch offered.** The reporting half is built as `doctor` check 16;
      `--prune` is deferred with its blockers named; decision 26 is **amended,
      not retired**, because build-directory growth is still real.
- [x] If built: `spec.md`'s `doctor` row updated, decision 26's implementation
      note updated, and a test that a currently-valid target's build directory is
      never deleted. — first two done. **The third does not apply and must not be
      faked green:** nothing in this change deletes anything, so there is no
      deletion to guard. What stands in its place is that check 16's measuring
      functions are pure over a path, and **every test hands them a temp
      directory** — `cargo test` never resolves a real Core data directory.
- [x] `status.d/` fragment for `suite/features.md`'s `embarch doctor` row. —
      **Not owed, and deliberately not dropped.** `suite/features.md` is
      assembled from `features.d/` now, and that row is this scope's to write:
      `features.d/umbrella-060-*` (checks 17-20, `--prune` deferred) and
      `umbrella-030-*` (decision 17's amendment now blocks two decisions) are
      edited, and `features.d/umbrella-105-doctor-check-16-growth.md` is the new
      row. No other shared suite-level doc carries a fact this change made false
      — `embarch.md`'s umbrella row still reads Shipped, the roadmap and the
      user guide never mention `--prune`, and the user guide's failure table
      names no check numbers.
- [x] Gate green; `changelog.d/` fragment dropped.

## Outcome

**Decision: build the reporting half, defer `--prune`, amend decision 26.** Three
findings, none of which the 2026-09-03 audit could see from inside this repo:

1. **The `study_results/` half of decision 26's premise is dead.**
   `embarch-core` ships `sweep_study_results` / `EMBARCH_STUDY_RESULTS_KEEP`
   (default 50, `0` disables), swept at `POST /study`, unit-tested, and
   documented as a user-facing knob in `suite/studies-guide.md`. Umbrella
   building a second retention policy for a directory it does not own — and
   cannot reach at all on a `remote` topology — would be the mirror-that-drifts
   mistake decision 17's amendment already refused. What survives is that the
   sweep bounds a **count**, not bytes, which is what check 16 reports.
2. **Nothing in this crate can name a valid build directory, only count
   directories.** `crate::zephyr` returns a count and deliberately overcounts;
   it models neither variant names nor cpucluster, so it cannot produce
   `embarch-api`'s `build_dir_name`. The oracle is `embarch-api list-targets`,
   and wiring that shell-out **is decision 17's amendment, itself unbuilt** —
   so `--prune` is blocked behind it rather than behind effort.
3. **The prune rule is under-specified against the name it would judge.**
   `embarch-api` decision 19 later folded snippets and an `extra_args` hash into
   the build-directory name, and every segment can contain `-`
   (`…-ble-shell_wdt31`), so a directory is not parseable back into a target.
   The per-directory `target.json` decision 19 says records the resolution
   **is not written by `embarch-api`** — no occurrence in its source — so a
   build directory carries no provenance either.

**Shipped:** `doctor` check 16 (`study_results/` entry count and bytes, plus
per-project build directories; informational, never fails, deletes nothing);
`config::ProjectConfig::build_dir_root` + `resolved_build_dir_root` mirroring
`embarch-api`; `setup::data_dir_for`, class-aware so a `Remote` Core reports
"not measurable from here" instead of confidently measuring the wrong machine.
Design-only checks 16-19 renumbered to 17-20, which `spec.md` already licensed.

## Verification debt (live install, the owner's — not hardware)

**Check 16 has never resolved a real data directory.** Every test uses a temp
directory on purpose, so nothing host-side can show whether
`setup::data_dir_for(WslHost, false)` really lands on the Windows Core's
`study_results/` from WSL2, or what the count and size read on the real bench.
One `embarch doctor` against the live install answers it — the same run
`open.md` already owes checks 11 and 15. Carried in `embarch-umbrella/open.md`.

## Filed elsewhere

Two drops in `inbox/`, both `Scope: api`, both found while looking for a build
directory's provenance: `api-target-json-not-written.md` (decision 19's
`target.json` is stated as truth in `interfaces/config.md` and written by
nothing) and `api-extra-args-hash-is-not-stable.md` (`DefaultHasher` is not
stable across Rust releases, so a toolchain bump silently orphans every
`-args<hash>` build directory — an orphan that belongs to a *valid* target and
so would be protected from any future `--prune` forever).

## Doc-size reserve spent

Both `umbrella` docs got tighter, and **`009-compact-docs.md` is now urgent for
`open.md`**: 5051/5120 B, **69 B left** (was 335). `spec.md` is 10089/10240 B,
**151 B left** (was 243) — the `doctor` row and the check table were rewritten
rather than appended to, which paid for most of check 16's new row. The next
change to either file has effectively no room.
