# 088 — The shared crate's PDF text extractor and number grammar, for `verify`'s check 4

**State:** done (2026-11-22, agent/study-designer/088-the-pdf-text-extractor-and-number-grammar)
**Source:** `embarch-study-designer/interfaces/hil-pdf.md`, "The text extractor" and "The number grammar" (design, not yet code); `notes/hil/06-report-and-publish.md`, "Verify" check 4; `notes/hil/14-implementation-plan.md`, unit M1.11
**Issue:** EMB-226
**Scope:** study-designer
**Hardware:** none
**Owner:** no

## Dispatch notes

- `hil-pdf.md` says the extractor's contract and the grammar "live once in the shared crate's host-only half", so the plot helper and `verify` cannot disagree. `plot_ticks` stays in `embarch-api`'s `report_pdf` (its decision 110) and is **not** part of this task; moving it touches two repos.
- **Behind a new feature, off by default**, as `reducers` and `verdicts` are: dev-bench's `no_std` firmware build and every consumer that does not turn it on must build unchanged. The PDF library is this unit's choice (`hil-pdf.md` names a contract, not a crate); say in the decision why that one, and keep its dependencies out of every other feature.
- `tasks/api/171` turns the feature on in `embarch-api` for check 4 and is parked until this lands. Name the public API it should call in `interfaces/hil-pdf.md`.
- Per-decision budgets near their limit in this sub-project: `streams#39` (64 B left), `versioning#12` (67 B), `seals#17` (72 B), `protocols#58` (121 B), `authoring#73` (130 B). Put new decisions beside decision 91 in `decisions/hil-shapes.md` if it has room, or in a new topic file.

## What

The two halves of `hil-pdf.md` that are text, built as code in the crate's host-only half:

- **The text extractor**: a PDF's pages in page-tree order, each page's glyph runs in content-stream order as `{text, x, y, size}`; every glyph mapped through the font's ToUnicode map, and one unmapped glyph an error naming its page; NFKC normalisation with U+2212 kept; lines and words split by the thresholds the doc gives, the assumed ones kept as named constants.
- **The number grammar**: the doc's grammar for what is a number in extracted text and in source text (the prose files and `report.typ`, which check 4 rescans with the same rules), with "nothing is exempted by its shape".

## Why now

`verify`'s check 4 (`tasks/api/171`) needs both, and `hil-pdf.md` puts them here so there is one implementation. It runs in parallel with `tasks/api/170`, the rest of `verify`.

## Done when

- [x] Extractor tests over fixture PDFs: page order, content-stream order, the coordinates and size, an unmapped glyph failing with its page, NFKC applied (a full-width digit, a ligature), the line and word thresholds.
- [x] Grammar tests for each rule `hil-pdf.md` states, including a year, a version and a page count read as numbers.
- [x] The crate builds and tests with the new feature on and off, and with `--no-default-features`; every consumer's feature set builds unchanged (`../../embarch-fleet/gate.md`, the shared-crate bullet).
- [x] `interfaces/hil-pdf.md` says what is built and names the API; a new numbered decision for the library and anything the doc left open.
- [x] Gate green, `changelog.d/` fragment dropped, `status.d/` fragment for anything suite-level it made false.

## Outcome

Built behind `pdf-text` (`lopdf`, decisions 101 to 103). Gate: build, test and clippy `-D warnings` green for default, `--no-default-features`, `alloc`, `std,reducers`, `study-ui,gatt-extract,eap-parse`, `pdf-text` and `--all-features`. **Debt:** only hand-assembled fixture PDFs have been read; no Typst-rendered PDF (M1.9's fixture) yet, so the word-gap threshold and the 0.5 em width fallback stay assumed. `tasks/api/171` calls `pdf_text::extract_pages` / `words` and `number_grammar::numbers_in_word` / `numbers_in_text` (hil-pdf.md, "What is built").
