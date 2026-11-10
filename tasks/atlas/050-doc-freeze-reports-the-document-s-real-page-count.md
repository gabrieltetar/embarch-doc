# 050 — `doc freeze` reports the document's real page count

**State:** done
**Source:** Linear issue EMB-40, filed by a session
**Issue:** EMB-40
**Scope:** atlas
**Hardware:** none
**Owner:** no

## What

The line `embarch-atlas doc freeze <doc_id>` prints ends `... {N} card over {P} pages; ...`, and on one real datasheet `P` was one more than the PDF's page count. Whether every document is off by one is not known.

What is known: `P` is `len(e["page_sha"])` in `cmd_freeze`, and `page_sha` in `freeze` holds one entry per page cited by any unit (`sorted({p for u in us.values() for p in u["pages"]})`). A unit's pages are the pages its record or prose cites, or every page `1..pages` of `doc.json` when it cites none (`units`). So `P` can exceed the page count only if some unit cites a page outside `1..pages` (a `p: 0`, say, or one past the end), or if `pages` in `doc.json` (`doc.page_count` in `pdftext.prep`) is already one too high. Neither is confirmed.

Name the cause, fix it with a test, and make the count printed be the document's real page count.

## Why now

A count that is wrong on one document makes every count it prints suspect.

## Where to look

- `src/embarch_atlas/freeze.py` `freeze` — builds `page_sha` from the units' pages (`"page_sha": {str(p): shas.get(p, "missing") for p in cited}`); a cited page with no page file reads `missing`
- `src/embarch_atlas/freeze.py` `cmd_freeze` — prints the count
- `src/embarch_atlas/freeze.py` `units` — assigns each unit its pages
- `src/embarch_atlas/pdftext.py` `prep` — `doc.json` `pages`
- `tests/test_freeze.py` — where the test goes

## Dispatch notes

- Reproduce on a synthetic document: a unit citing page 0, a unit citing a page past the end, and a unit citing nothing, and see which one makes `P` exceed the page count. The real datasheet is not available to you; what it showed is owed to a real file, written as a debt in the task file.
- If the fix is that an out-of-range cite is a fault in the record rather than in `freeze`, say where it should be refused or reported, and do that or file it, rather than silently dropping the page.
- Burndown is on: no new numbered decision. Amend `DESIGN.md` in place if it states the count.
- The worktree needs `.atlas-local` linked beside it and a `.venv` of its own; `test_public_guard` must run, not skip.

## Done when

- [x] The cause is named in the task file, then fixed with a test in `tests/test_freeze.py`, or filed as a `bug` if the fix belongs elsewhere.
- [x] `doc freeze` prints a page count no larger than the document's page count on a synthetic document that reproduces the extra page.
- [x] Gate green (`../../embarch-fleet/gate.md`, the Python bullet); `changelog.d/` fragment dropped.

## Result

**Cause (reproduced on a synthetic document):** `freeze` built `page_sha` from every page any unit cites, with no check against `1..pages`. A unit citing `p.0` or a page past the end therefore added a page outside the document, and `cmd_freeze` printed `len(page_sha)` as the page count. A unit citing nothing is not the cause (it gets exactly `1..pages`), and `pages` in `doc.json` was not at fault in the synthetic case.

**Fix** (`src/embarch_atlas/freeze.py`): `page_sha` now holds only pages in `1..pages`, so the printed count never exceeds the document's. An out-of-range cite is not dropped silently: it stays in the unit's `pages` (its key reads `missing`, so correcting the cite thaws the unit), is recorded in the entry as `out_of_range` and `doc freeze` prints a warning naming the unit and page on stderr. `thaw_check` compares a missing frozen page as `missing`. Test: `test_page_count_is_never_more_than_the_document_s_pages` in `tests/test_freeze.py`. `DESIGN.md` does not state the count; no decision added.

**Not done:** refusing the cite at `doc check` (where the record fault belongs) is not implemented here.

## Debts

- **Real-file verification owed.** The real datasheet that showed P one over the PDF's page count was not available. Run `embarch-atlas doc freeze <doc_id>` on it: if it now prints the PDF's page count and a `warning: ... cites page ...` line, the cause was an out-of-range cite. If it still prints one too many with no warning, `pages` in `doc.json` (`pdftext.prep`, `doc.page_count`) is itself high and this is a separate bug.
