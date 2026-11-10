# 044 — A page cite naming another document is checked against that document

**State:** claimed by agent/atlas/044-a-cite-of-another-document-is-checked-there, 2026-11-09 20:38
**Source:** Linear issue EMB-44, filed by a session
**Issue:** EMB-44
**Scope:** atlas
**Hardware:** none
**Owner:** no

## What

Check M anchors a line's numbers on the pages it cites **in the document the cite names**. A conflict row whose Sources cell cites `<other-doc> p.N` (the shape `t_conflict` renders) has its numbers looked up on that document's page N, and no longer fails M. A number on neither document's cited page still fails.

Today `check_markdown_file` reads a line's cites with `cited_pages` — `PAGE_CITE` carries no document name — and anchors every number against `DocText.page_numbers` of the document being checked, so a conflict citing another document's page is `unanchored` and `doc check` exits 1. Not captured from a failing run; it follows from the code.

## Why now

Filed from distilling two documents where one's section carried a conflict row citing the other.

## Where to look

- `src/embarch_atlas/check.py` `check_markdown_file` — anchors a line's numbers on its cited pages
- `src/embarch_atlas/check.py` `cited_pages`, `PAGE_CITE` — no document name in a cite
- `src/embarch_atlas/check.py` `DocText.page_numbers` — one document's pages
- `src/embarch_atlas/render.py` `t_conflict` — the Sources column's shape

## Dispatch notes

- `atlas/039`, `040` and `041` also edit `check.py`; read `main` as it is when you start.

## Done when

- [ ] A conflict row citing `<other-doc> p.N` has its numbers anchored on the other document's page N and does not fail M.
- [ ] A number on neither document's cited page still fails; a test in `tests/test_check.py` covers both, on synthetic documents.
- [ ] Gate green (`../../embarch-fleet/gate.md`, the Python bullet); `DESIGN.md` updated where it describes check M; `changelog.d/` fragment dropped.
