# `build_changelog.py` opens a new `## <window>` heading on every fold, and the gate is green on the result

**State:** open
**Source:** leg 020, `tasks/topology/006` — noticed by reading the assembler's own diff before committing it
**Scope:** doc
**Hardware:** none
**Owner:** required

## What

`scripts/build_changelog.py` prepends a **fresh `## 2026-09` heading and a fresh `### <category>`
section** on every run, instead of merging the run's entries into the window block that is already
there. So a history file accumulates one duplicate window heading per fold.

It is not one file. Counting `^## 2026-09$` across `history/` on `origin/main` at `c2fc30b`:

| file | `## 2026-09` headings | `###` sections |
|---|---|---|
| `history/api.md` | **26** | 29 |
| `history/umbrella.md` | **23** | 26 |
| `history/doc.md` | 14 | 25 |
| `history/suite.md` | 8 | 9 |
| `history/core.md` | 6 | 7 |
| `history/study-designer.md` | 6 | 7 |
| `history/dev-bench.md` | 3 | 5 |
| `history/outpost.md` | 3 | 5 |
| `history/ui.md` | 3 | 3 |
| `history/fleet.md` | 2 | 6 |
| `history/topology.md` | 2 | 2 |

Roughly one heading per fold, in every scope, **since the changelog split on 2026-09-02.** No
content is lost or misfiled — every entry is under a correct category, in the right file, in
newest-first order. What is wrong is the structure the file's own header promises.

## Why it survived

**`build_changelog.py --check` passes, and so do all nine checks in `check-docs.py`.** The
`--check` arm validates *fragments* — that each is named correctly and parses — and never reads
the assembled file it is checking against. So the one script that could catch this is the script
that causes it, and it is looking the other way.

It is also invisible in a fold's own diff unless you look: a fold adds four lines and they read
correctly in isolation. **It is only visible in the assembled file, which nobody re-reads.** That
is the same shape as `tasks/doc/013` and the pipeline-swallows-exit-status defect — the failure is
in what a convenience produced, not in what it reported.

## Why it matters beyond tidiness

Every history file's header says *"newest window first. Capped at 20 KB — older windows roll into
`archive/`."* Both halves are now false in the same way:

- A reader of `history/api.md` sees **26 separate September 2026 windows**, one per fold, and there
  is no way to tell from the file that they are one month. The window is doing the job of a commit,
  which is precisely what `changelog.d/README.md` says the history file is *not* for.
- **The roll is sized in windows.** Rolling "older whole windows into `archive/`" on a file whose
  windows are per-fold rolls an arbitrary slice of one month, not a month — so the cap's behaviour
  is different from the one described, and it has not fired yet only because no history file has
  reached 20 KB.

## Not fixed here, deliberately

`scripts/` is owner-reserved (`../../embarch-fleet/protocol.md` §2), so a leg may not touch the
assembler. **And the eleven files were left as they are rather than hand-merged**: fixing one file
of eleven makes it inconsistent with the corpus and the next fold undoes it. The repair is one pass
after the script is fixed, not eleven hand edits before.

## Done when

- [ ] `build_changelog.py` merges into an existing window block for the same window, and into an
      existing `### <category>` inside it, rather than prepending new headings.
- [ ] Something fails when an assembled `history/*.md` carries two headings for one window —
      whether that is `build_changelog.py --check` growing an assembled-file arm, or a new check.
      Today no check reads the assembled file at all, which is the actual gap.
- [ ] The eleven existing files are merged in one pass, and the pass asserts entry count and order
      are unchanged — no content moves, only headings collapse.
- [ ] Whether the 20 KB roll is sized in windows or in bytes is restated to match what the code does.
