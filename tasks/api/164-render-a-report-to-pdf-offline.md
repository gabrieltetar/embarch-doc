# 164 — embarch-api renders a report to PDF offline, with Typst built in and its root confined to the staged files

**State:** done on agent/api/164-render-a-report-to-pdf-offline, 2026-11-21
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
- **A fetch no permission rule allows is refused, not prompted**, because the fleet runs unattended. If lilaq's source cannot be fetched by an allowed route, stop and report `blocked` with what you tried; never write the package yourself.
- **Typst is a large dependency.** Whether it sits behind a cargo feature, and what that costs `cargo build` time and the binary, is this unit's decision; record it with the numbers you measured.
- **Read `measurements.json`'s shape from `interfaces/hil-shapes.md`** for the fixture run; do not invent a second shape.
- **Decisions near their size limit**: `ledger` #98 (15 B left), `bench-exchange` #89 (122 B), `failure-reporting` #67 (192 B). A new report topic file is the expected home. In reserve, filed against `tasks/api/165`: `decisions/client-crate.md` (10 B left) and `interfaces/config.md` (920 B); do not add to either.
- Out of scope: the zip and `publish` (M1.10), `verify` (M1.11), anything Core writes.

## Done when

- [x] A fixture run's `report.typ` renders to PDF with no network (a test, with the network unavailable or the registry unreachable by construction).
- [x] A `report.typ` reading a file outside the staging root fails, and a staged symlink is refused.
- [x] Rendering the same fixture twice gives byte-identical PDFs.
- [x] `spec.md`, `decisions/`, `interfaces/` updated; `changelog.d/` fragment dropped.
- [x] Gate green (`../../embarch-fleet/gate.md`; `check-ownership.py --scope api` on both branches; `check-client-names.py --repo` on the code worktree, since vendored files are new text).

## Done

- `src/report_pdf.rs`, `typst-packages/` (lilaq 0.6.0 plus elembic, tiptoe, zero from the registry's tarballs, hashes in `PROVENANCE.md`; EmbArch's `@embarch/report` helper), `tests/report_pdf.rs` (10 tests) and its fixture. Decision 110, `interfaces/report-pdf.md`.
- Feature `pdf`, default on. Measured: cold debug workspace build 66 s to 147 s; release 71 s to 187 s; release binary 21.5 MB to 84.3 MB.
- Gate: `cargo build`, `cargo test`, `cargo clippy --all-targets -- -D warnings` green, `cargo check --no-default-features` green; `check-docs.py`, `check-client-names.py`, `check-ownership.py` green.

## Findings for others

- A Typst package cannot read the project by a string path, so the helper takes `path("capture.csv")`; check 9's whitelist (M1.11) must admit `path()`. Dropped as `status.d/api-report-pdf-helper-shape.md`.
- `hil-pdf.md`'s tick algorithm: f64 compare-corrections are not exact, e.g. `(-0.3, 0.3)` gives step 0.1; `plot_ticks` lives in embarch-api, not the shared crate (not this sub-project's). Same fragment.
- Not measured: byte identity across machines, a million-row capture. The hand-off to M1.10: `main.rs` does not call `render_report` yet, so the binary-size figure is for a binary that does.

## Hardware-verification debt

None; no hardware.
