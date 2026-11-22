# embarch-api decisions: the report's PDF

**Status:** active, 2026-11-21.

Decision 110: a report renders to PDF inside the binary, offline and reproducibly (HIL milestone M1.9, `tasks/api/164`). Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md). Surface: [../interfaces/report-pdf.md](../interfaces/report-pdf.md). Source: `notes/hil/06-report-and-publish.md`, "The report".

### 110 - Typst as a library behind the `pdf` feature, packages embedded and served by this crate's own resolver, the root confined to the staged files

**Versions, picked together** (a mismatch was the expected first failure): `typst`, `typst-pdf`, `typst-layout` 0.15.1; `typst-as-lib` 0.18.0, which requires `typst ^0.15`; lilaq 0.6.0, whose manifest says `compiler = "0.13.0"` and which renders on 0.15.1 (the fixture and its plot are the test).

**lilaq is vendored with what it imports**: `elembic` 1.1.1, `tiptoe` 0.4.0, `zero` 0.6.1, under `typst-packages/preview/`, unpacked from the registry's own tarballs, never written by hand; URLs, tarball SHA-256 and licences (MIT; elembic MIT OR Apache-2.0) are in `typst-packages/PROVENANCE.md`. `suiji` is imported only inside lilaq's `jitter` helper, at call time, and is not vendored: a report calling `jitter` fails with "not found". The packages are embedded with `include_dir`, so an installed binary carries them and no path is configured. `vendored_files()` lists each with its hash, for M1.10's zip.

**No registry client exists in this build.** `typst-as-lib`'s `packages`, `reqwest` and `ureq` features are off, and `report_pdf` brings its own `FileResolver`: a package path is read from the embedded tree, a project path from the staging directory, and nothing else resolves. Not `typst-as-lib`'s `FileSystemResolver`: no link checks, and packages from the user's data directory. Fonts are the ones Typst embeds, never the machine's.

**Staging copies by content and refuses links** (`Staging::stage_file`): a symlink, a file with another hard link and a path swapped between check and open are refused; a name must be plain and relative. The resolver refuses a non-regular file again at read time, so a link planted in the directory later is not followed. A `report.typ` reading `../x`, an absolute path or an unstaged file fails to compile.

**A package cannot read the project by a string path.** A path in a package resolves in the package, so the helper takes Typst's `path` type, resolved where the report wrote it: `minmax-plot(path("capture.csv"), …)`, `m("rate", path("measurements.json"))`. This is the form check 9's whitelist has to admit (a status fragment says so).

**Reproducible**: `RenderOptions` carries `ident` and `timestamp_unix`, set on `PdfOptions` and as Typst's `today`. Two renders in one process, and in two processes, gave identical bytes; **across machines is unmeasured**.

**The page number footer is the compile's**: `report.typ` is included under `#set page(footer: …)` printing the number alone, centred (`hil-pdf.md`).

**`plot_ticks` lives in this crate**, since the shared crate is not this sub-project's; the Typst helper carries the same algorithm and a test holds the two equal. Two refinements of `hil-pdf.md`: **the compare-corrections are f64**, not exact, so `(-0.3, 0.3)` gives step 0.1 (0.15 / 0.1 is 1.4999999999999998) where exact arithmetic gives 0.2; and a step below 1 is `m / 10^-e`, one correctly rounded division.

**The cost of Typst, measured:** cold `cargo build` of the workspace 66 s without it, 147 s with it (debug); release 71 s without, 187 s with the Typst crates built on top; the **release binary 21.5 MB without, 84.3 MB with** (embedded fonts and the packages included), the debug binary linking it not measured. It is a default feature, `pdf`, since `publish` is this binary's job; `--no-default-features` builds without it.

**Not verified:** a 100,000-row capture rendered in 3.6 s (debug); a million rows is not measured. Sizes are for a binary that calls `render_report`; `main.rs` does not yet.
