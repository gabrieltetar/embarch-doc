# 007 — Search a document's page text from the atlas, with page and section cites

**State:** claimed by agent/atlas/007-find-text, 2026-10-29 16:39
**Source:** field use on a USB PD charger board, 2026-09-09 to 2026-10-20 — 3,332 calls (3,278 shell commands, mostly `grep` and `sed -n`, and 54 `Read`s) against `pdftotext` dumps of the 418-page USB PD R3.2 spec, 16.5 M result characters, 94% of them from 122 subagents in 6 sessions, against 121 atlas calls on the same document over the same weeks
**Scope:** atlas
**Hardware:** none
**Owner:** no
**Also owed (from `atlas/012`, landed 2026-10-29):** `doc_section`'s "not distilled" answers and `doc_toc`'s
nearest-title answers point to `doc_section tier=text page=<first>` and a PDF Read only, because `find_text` did not
exist yet. When it lands, add `find_text <doc> ... section=<id>` to those next-call hints (`query.py`), with a test.

## What

Add a lookup `find_text <doc> <pattern> [section=<id>] [context=<n>] [offset]` (MCP tool, and `embarch-atlas q find-text`) that searches every page of a document's text layer, which `doc prep` already writes (`docs/<doc>/pages/p<NNN>.txt`; 419 files for the spec above), and returns each hit as one block: the physical page, the deepest `toc.json` section that holds the line (id and title), whether that section is distilled (`s/<file>` or "not distilled"), the line, and `context` lines around it. The pattern is plain words or a regex; `section=` limits the search to that section's pages; the answer is cut at the tool budget with `next=` like the others. `find_fact` stays the first step. `find_text` is the step after it, for a term `find_fact` reports as `unmatched=` and for any section with no distillation. Each call appends `{doc, section, page}` of what it returned to a usage log under the atlas dir, so the standard-sections task can rank undistilled sections by use.

## Why now

The spec was distilled on 2026-10-08 (119 records citing 35 pages), and the field sessions kept reading it through text dumps afterwards. 1,743 of those calls (52%) touched no distilled page, 348 distinct pages were read, and only 288 calls (9%) stayed on distilled pages. The atlas already holds every page's text, but reads it one page at a time (`doc_section tier=text page=N`, `embarch-atlas/src/embarch_atlas/query.py:283`, used 12 times), and `find_fact` searches only facts and distilled prose (`query.py:409-415`). The sessions' own memory file told them to grep a dump for anything outside the distillation, because the atlas had nothing to offer there.

## Done when

- [ ] `find_text` answers with `src: <doc> text-layer, <n> pages` and one block per hit: `p<N> §<id> <title> [s/<file> | not distilled]`, the matching line, and its context lines.
- [ ] Synthetic fixture test (an invented 3-page document with a toc): a plain-word hit, a regex hit, a hit in an undistilled section, `section=` narrowing, and a budget cut that continues with `next=`.
- [ ] On a 400-page document, a symbol, a state name and a table title each answer in under 0.5 s.
- [ ] The usage log records `{doc, section, page, tool}` per answer and is never read back into an answer.
- [ ] `atlas-use` SKILL.md, the MAP protocol line (`mapgen.py`) and DESIGN.md "Query surface" name `find_text` as the step after `find_fact`.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped.
