# 012 — Fix the lookup misses field sessions hit: part_card's board argument, CMSIS register names, undistilled sections, PDF paths

**State:** done on agent/atlas/012-query-misses, 2026-10-29
**Dispatch note:** line numbers below may predate `atlas/017`, `021`, `024` and `006` (all landed 2026-10-29); read the
code on `main`. No `embarch-atlas` doc is in size reserve. The atlas's design doc is `DESIGN.md` in the code repo.
**Source:** field use on a USB PD charger board, 2026-09-09 to 2026-10-20 — 49 of 160 `part_card` calls (9 sessions) never reached the server because the model wrote `"board": }`; 5 `register` misses on CMSIS names such as `UCPD1.CFG1`; 9 `doc_section`/`doc_toc` misses, 5 on toc sections with no distillation and 4 on section numbers or titles the toc does not have; 3 of 208 PDF page reads went to guessed file paths
**Scope:** atlas
**Hardware:** none
**Owner:** no

## What

Four small fixes, each from a measured miss. (1) `part_card`'s `board` parameter documents `""` as "all boards" (`embarch-atlas/src/embarch_atlas/mcp_server.py:48-50`); the model wrote `"board": }` instead, Claude Code rejected the call as invalid JSON, and 33 times the next call was the same failing call. Replace the empty-string sentinel with a value a model writes reliably (`"all"`), and make sure no tool documents `""` as a meaningful value. (2) Firmware names MCU registers by the CMSIS device header's struct members (`UCPD1->CFG1`, `RX_PAYSZ` in the Zephyr UCPD driver), while `register` matches SVD names (`UCPD_CFGR1`, `UCPD_RX_PAYSZR`) and misses (`query.py:556`). Alias each struct member to the SVD register at the same offset, read from the build's CMSIS header. (3) `doc_section` with a section id that `toc.json` has but no `s/` file answers "not found" (`query.py:305-307`); answer instead with the section's title and pages, "not distilled", and the next call (`find_text section=<id>`, or `doc_section tier=text page=<first>`). A reference-manual register section left to the SVD points to `register <PERIPH>.<REG>`; a `doc_toc under=` that matches nothing lists the nearest titles. (4) Cites give a doc id and a page (`ds13560@6 p102`), and the card's Source line gives a bare file name, so a session guessed the PDF path (`<fw>/embarch/hardware/ds13560.pdf`, `<fw>/embarch/atlas/docs/ina700@B/ina700.pdf`) and the `Read` failed. Put the source PDF's path, relative to the firmware repo, in the card's Source line and in `doc_section`'s `src:` line.

## Why now

The first fix alone recovers about a third of `part_card` calls. The other three each turn a dead end into the next call to make.

## Done when

- [x] `part_card` takes `board="all"`; a test asserts that no MCP tool's documentation offers `""` as a value.
- [x] `register UCPD1.CFG1` answers with `UCPD_CFGR1`'s fields, from a synthetic CMSIS header and SVD fixture with a member renamed against the SVD.
- [x] `doc_section` on an undistilled toc section returns its title, pages and the next call; an RM register section points to `register`; `doc_toc under=` with no match lists nearest titles.
- [x] Cards and `doc_section`'s `src:` line name the source PDF path relative to the firmware repo.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped.

## Notes (worker)

- `atlas` has no `spec.md`/`decisions.md`/`open.md` in `embarch-doc`; the contract is the code repo's `DESIGN.md` ("Query surface"), which is updated.
- `"all"` is the documented value; `""` (the CLI's bare `--board`, now `all`) is still accepted so no saved call breaks. `part_card` with no `board` still returns the card alone.
- The CMSIS alias reads the header path `mcu vote --header` recorded in an RM doc's `vote*.json` (no new config). An atlas that never ran `vote` with a header, or whose header file moved, gets no alias and the old "not found". Offsets come from the `<TYPE>_TypeDef` layout (uint8/16/32/64, arrays, natural alignment); a typedef with a nested struct or union is skipped whole rather than guessed. Tested on synthetic header + SVD only, not a real vendor header.
- `find_text` (named in the task) is not a tool in this repo, so "not distilled" answers point to `doc_section tier=text page=<first>` and a PDF Read only.
- The PDF path comes from doc.json's `path` (relative to the atlas dir), shown relative to the firmware repo (`<atlas dir>/../..`), as `pdf=<path>` on the `src:` line of `part_card` and all `doc_section` answers. The card's own `Source:` line is LLM-written prose in `card.md`, left alone.
