# 072 — Search the text of schematic PDF pages

**State:** claimed by agent/atlas/072-search-schematic-pdf-pages, 2026-11-17 19:19
**Source:** EMB-156, an audit finding: `find_text` searches datasheet documents only, so a pin name or a net cannot be looked up on a schematic page
**Issue:** EMB-156
**Scope:** atlas
**Hardware:** none
**Owner:** no

## What

`find_text` searches the translated datasheet documents. The schematic PDFs a
board's netlist is read from are not among them, so a session that needs to
find a pin name or a net on a schematic page has to run `pdftotext -bbox` by
hand.

Make schematic pages searchable: either add the schematic PDFs to `find_text`'s
documents, or add a verb (for example `schematic_text`) whose hits carry the
board, the sheet and the page. Each hit says which file and page it came from.
Choose whichever fits the atlas's existing query surface with less new code,
and say why in `DESIGN.md`.

The `checks.md` flag EMB-156 also asks for is `atlas/071`, not this unit.

**Public repo.** Tests build a synthetic schematic PDF in the test.

**No new numbered decision** (burndown; `embarch-atlas` keeps none anyway). A
real design fork goes to `scripts/fleet-linear.py file --from decision`.

**What you may change.** Only `embarch-atlas` and `embarch-doc/embarch-atlas/`.

**Doc reserve.** Nothing of `embarch-atlas`'s is in reserve at filing.

## Why now

The owner moved EMB-156 to Fleet Ready; `atlas/070` landed the text-layer
recovery this sequence started with.

## Done when

- [ ] A query returns hits from schematic PDF pages, each with its file and page number.
- [ ] A test covers it on a synthetic schematic.
- [ ] The atlas-use skill and `DESIGN.md` name the new search.
- [ ] Gate green (`../../embarch-fleet/gate.md`); `changelog.d/` fragment dropped.
