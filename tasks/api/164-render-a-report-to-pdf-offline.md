# 164 — embarch-api renders a report to PDF offline, with Typst built in and its root confined to the staged files

**State:** open
**Source:** Fleet Ready issue: embarch-api cannot render a report to PDF offline. `notes/hil/14-implementation-plan.md`, unit M1.9 (after M1.1, landed as `tasks/study-designer/084`); `notes/hil/06-report-and-publish.md`; `embarch-study-designer/interfaces/hil-pdf.md` for the plot helper's tick algorithm and the footer rule.
**Issue:** EMB-224
**Scope:** api
**Hardware:** none
**Owner:** no

## What

- **Typst as a library** (`typst`, `typst-pdf`, `typst-as-lib`), so a report renders with no `typst` binary and no network.
- **lilaq vendored under a local package root**, resolved by Typst from there and never from the package registry at render time.
- **EmbArch's plot helper** drawing per-bin min and max, with the tick algorithm and footer rule `hil-pdf.md` fixes.
- **Staging by content**: the files a report reads are copied into a staging directory by content, with symlinks and hard links refused, and **Typst's root confined to the staged files**, so a `report.typ` reading outside the root fails.
- **`PdfOptions.ident` and `timestamp` set**, so the same inputs render the same PDF.

## Why now

M1.10 (`publish`, the zip) needs it, and it depends only on M1.1, so it can run beside the Core units.

## Dispatch notes

- **Fetching lilaq's source to vendor it is part of the task**: pin one version, record where it came from and its hash, and check its licence is compatible before committing it. Pick the Typst, `typst-as-lib` and lilaq versions together; a mismatch is the likely first failure.
- **Typst is a large dependency.** Whether it sits behind a cargo feature, and what that costs `cargo build` time and the binary, is this unit's decision; record it with the numbers you measured.
- **Read `measurements.json`'s shape from `interfaces/hil-shapes.md`** for the fixture run; do not invent a second shape.
- **Decisions near their size limit**: `ledger` #98 (15 B left), `bench-exchange` #89 (122 B), `failure-reporting` #67 (192 B). A new report topic file is the expected home.
- Out of scope: the zip and `publish` (M1.10), `verify` (M1.11), anything Core writes.

## Done when

- [ ] A fixture run's `report.typ` renders to PDF with no network (a test, with the network unavailable or the registry unreachable by construction).
- [ ] A `report.typ` reading a file outside the staging root fails, and a staged symlink is refused.
- [ ] Rendering the same fixture twice gives byte-identical PDFs.
- [ ] `spec.md`, `decisions/`, `interfaces/` updated; `changelog.d/` fragment dropped.
- [ ] Gate green (`../../embarch-fleet/gate.md`; `check-ownership.py --scope api` on both branches; `check-client-names.py --repo` on the code worktree, since vendored files are new text).
