# 005 — `doctor --prune` was decided, and neither half of decision 26 was built

**State:** claimed by agent/umbrella/005-doctor-prune, 2026-09-05 12:08
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

- [ ] Either both halves built, or decision 26 retired per `DOC-CONVENTIONS.md`
      with a one-line tombstone saying why.
- [ ] If built: `spec.md`'s `doctor` row updated, decision 26's implementation
      note updated, and a test that a currently-valid target's build directory is
      never deleted.
- [ ] `status.d/` fragment for `suite/features.md`'s `embarch doctor` row.
- [ ] Gate green; `changelog.d/` fragment dropped.
