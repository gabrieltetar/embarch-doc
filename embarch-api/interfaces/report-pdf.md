# embarch-api: rendering a report to PDF

**Status:** active, 2026-11-21. Library module `embarch_api::report_pdf` (feature `pdf`, on by default); its caller is `publish` ([publish.md](publish.md)). Why: [decision 110](../decisions/report-pdf.md). Fixed shapes it follows: embarch-study-designer's `hil-pdf.md` and `hil-shapes.md`.

## The module

- `Staging::new()`, `stage_file(src, name)`, `stage_bytes(name, bytes)`, `root()`: a private temp directory of exactly the files a report may read. `stage_file` copies by content and refuses a symlink and a file with more than one hard link; a name must be a plain relative path, and one name stages once.
- `render_report(&Staging, &RenderOptions { ident, timestamp_unix }) -> Result<Vec<u8>, ReportPdfError>`: compiles `report.typ` from the staging root and returns the PDF. `ReportPdfError` is `Stage`, `Compile` (Typst's own diagnostics) or `Pdf`.
- `report_text(&Staging, &RenderOptions)`: the text runs per page, for tests.
- `vendored_files() -> Vec<VendoredFile { path, sha256, bytes }>`: every embedded package file, in path order, for the zip's package list.
- `plot_ticks(lo, hi) -> Result<Ticks, TickError>`, `TICK_TARGET`, `TYPST_VERSION`.

## What the compile does

- The main file is the compile's own: `#set page(footer: context align(center, counter(page).display("1")))` then `#include "/report.typ"`. The footer is the page number alone; a `report.typ` that sets its own footer overrides it, which `publish` refuses.
- When a file named `appendix.typ` is staged, the compile appends it after a page break (`APPENDIX_FILE`): the fixed audit appendix `publish` generates.
- A package path is served from the embedded `typst-packages/`, a project path from the staging directory, nothing else. A path that escapes the root, an absolute path outside it, a file never staged and a non-regular file all fail the compile.
- Fonts are Typst's embedded set. `datetime.today()` and the PDF's `/CreationDate` are `timestamp_unix`; the PDF's id derives from `ident`.

## `@embarch/report:0.1.0`

The one package a report imports besides lilaq. Paths are Typst `path` values, since a package cannot read the project by a string.

- `minmax-plot(path("capture.csv"), x: "col", y: "col", bins: 200, width, height, xlabel, ylabel)`: a lilaq diagram of the per-bin minimum and maximum of `y` over `bins` runs of consecutive rows (a band and its two edges), never an average. Ticks come from `plot-ticks` over the min and max series; tick texts are the helper's, passed to lilaq as labels; linear axes only.
- `plot-ticks(lo, hi)`: `hil-pdf.md`'s algorithm, the same operations as the Rust `plot_ticks`.
- `m("name", path("measurements.json"))`: a measurement's value and unit from `measurements.json` ([hil-shapes.md](../../embarch-study-designer/interfaces/hil-shapes.md)); a unit of `1` prints no unit.
