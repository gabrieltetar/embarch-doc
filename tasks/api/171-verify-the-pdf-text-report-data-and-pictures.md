# 171 — `verify` checks the PDF's text, recomputes `report-data.json`, and whitelists `report.typ`'s syntax tree

**State:** open
**Source:** `notes/hil/14-implementation-plan.md`, unit M1.11 ("verify"), its second half; `notes/hil/06-report-and-publish.md`, "Verify" checks 4, 6 and 9
**Issue:** EMB-226
**Scope:** api
**Hardware:** none
**Owner:** no

## Dispatch notes

- `tasks/api/170` builds `verify <zip>` with checks 0, 1, 2, 3, 5, 7 and 8, and reports 4, 6 and 9 as "not checked by this version"; this task fills those three in.
- `tasks/study-designer/088` built the PDF text extractor and the number grammar behind the shared crate's `pdf-text` feature (its decisions 101 to 103); turn it on here and call `pdf_text::extract_pages`, `pdf_text::words`, `number_grammar::numbers_in_word` and `number_grammar::numbers_in_text`, as `embarch-study-designer/interfaces/hil-pdf.md` "What is built" names them. `pdf-text` pulls `lopdf` in, a large tree, into this crate only. Its word-gap threshold and 0.5 em width fallback are assumed and have read only hand-assembled PDFs, so check 4 against a Typst-rendered PDF is the first real test. `plot_ticks` stays in this crate's `report_pdf` (decision 110), and check 4 calls it.
- `embarch-api` decisions 114 and 115 left the `footer` refusal and the picture refusal lexical, with check 9's syntax-tree whitelist to M1.11; once the whitelist exists, `publish` refuses by it too (06: "publish refuses a `report.typ` that breaks the rule").

## What

- **Check 4, the PDF's text**: every number in the rendered PDF, as the shared crate's extractor reads it and its grammar finds it, matches a signed measurement, is listed in the appendix, equals a value `report-data.json` holds, is an axis tick `verify` derives from the plot's signed series with `plot_ticks`, or is the page number at the footer's position; citations and tags are rechecked in the prose files and `report.typ`.
- **Check 6, the report's other claims**: `report-data.json` recomputed from the signed records and the run log's segment matches its signed copy, and every verdict word, count, label and the fixed statement the PDF prints matches it. Core builds that file (`embarch-core` decision 119); if recomputing it needs Core's builder, say in the decision whether it moves to the shared crate, and file that move rather than copying it.
- **Check 9, the pictures at the source**: a whitelist of `report.typ`'s syntax tree per 06, refusing `eval`, `read`, every file read, every import but the plot helper's, and any binding or show rule that renames or wraps an admitted call; every carried Typst package hashed against the list in this checkout. `publish` refuses by the same whitelist.

## Why now

The second half of EMB-226. With it, `verify` runs every check 06 gives a Study.

## Done when

- [ ] It fails each tampered copy, one test each: a changed number in the PDF, an embedded image, an aliased plot call, a package off the list, a `report-data.json` that disagrees with the records.
- [ ] `publish` refuses a `report.typ` that the whitelist refuses.
- [ ] `interfaces/` and `spec.md` amended; new numbered decisions.
- [ ] Gate green (`../../embarch-fleet/gate.md`), `changelog.d/` fragment dropped, `status.d/` fragment for anything suite-level it made false.
