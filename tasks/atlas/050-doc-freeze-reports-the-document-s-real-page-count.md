# 050 — `doc freeze` reports the document's real page count

**State:** claimed by agent/atlas/050-doc-freeze-reports-the-document-s-real-page-count, 2026-11-09 22:57
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

- [ ] The cause is named in the task file, then fixed with a test in `tests/test_freeze.py`, or filed as a `bug` if the fix belongs elsewhere.
- [ ] `doc freeze` prints a page count no larger than the document's page count on a synthetic document that reproduces the extra page.
- [ ] Gate green (`../../embarch-fleet/gate.md`, the Python bullet); `changelog.d/` fragment dropped.
