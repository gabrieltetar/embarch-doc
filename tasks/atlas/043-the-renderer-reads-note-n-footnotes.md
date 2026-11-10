# 043 — The renderer reads "Note N:" footnotes

**State:** claimed by agent/atlas/043-the-renderer-reads-note-n-footnotes, 2026-11-09 20:34
**Source:** Linear issue EMB-39, filed by a session
**Issue:** EMB-39
**Scope:** atlas
**Hardware:** none
**Owner:** no

## What

A footnote printed as `Note 1: text` is read like the numbered forms: listed under the rendered table and put in the Note column of every row whose `fn` cites it.

Today `FOOTNOTE` in `render.py` accepts only `24. text` and `(1) text` (`^\s{0,6}(?:\((\d{1,3})\)|(\d{1,3})\.)\s+(\S.*)$` on `main` at the split), so a `Note N:` line is dropped.

## Why now

Filed from distilling a real datasheet whose footnotes use that form.

## Where to look

- `src/embarch_atlas/render.py` `FOOTNOTE` — the line pattern
- `src/embarch_atlas/render.py` `footnotes` — reads a page's footnotes; the first occurrence after the row wins
- `tests/test_render.py` — where the test goes

## Done when

- [ ] A page with `Note 1: text` yields the footnote text in the rendered table's notes and the citing row's Note column.
- [ ] The `24.` and `(1)` forms still render; a test in `tests/test_render.py` covers all three.
- [ ] A line that merely starts with the word `Note` and no number is not read as a footnote.
- [ ] Gate green (`../../embarch-fleet/gate.md`, the Python bullet); `DESIGN.md` updated if it lists the footnote forms; `changelog.d/` fragment dropped.
