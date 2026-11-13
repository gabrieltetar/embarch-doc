# 064 — `freeze.py` files a page cite that names another document under that document

**State:** done
**Source:** EMB-109, filed while relaying a burndown leg's report, 2026-11-09
**Issue:** EMB-109
**Scope:** atlas
**Hardware:** none
**Owner:** no

## What

Since EMB-44, a page cite that names another document is checked against the
document it names. The freeze step still collects every cited page number into
the *citing* document's page set: `freeze.py`'s `units()` takes
`sorted(cited_pages(text))` for prose and the card, with `cited_pages` imported
from `check.py`, and nothing there asks which document a cite names. So "see the
reference manual, p. 212" adds page 212 to the datasheet's frozen pages, and a
change to the datasheet's own page 212 thaws a unit that never rested on it.
The landing worker and its reviewer judged this conservative (it freezes more,
not less) and nobody filed it.

Wanted: a cite that names another document contributes its page to that
document's frozen set, or to none, never to the citing document's. Which of the
two is yours to decide, and it is a design choice: write it in the code repo's
`DESIGN.md` with the reason. If "that document's set" means a unit can rest on
another document's pages, say how `thaw-check` reads them.

Where: `embarch-atlas/src/embarch_atlas/freeze.py` (`units()`, `_key_for`) and
whatever in `check.py` already tells a cross-document cite from a local one;
reuse that rather than parse cites a second way. `tests/test_freeze.py`.

**What you may change.** Only `embarch-atlas` and `embarch-doc/embarch-atlas/`.

## Why now

A frozen unit's key is what decides whether the model is asked again. A key
built on the wrong document's pages re-asks for nothing, and it hides which
pages a unit really rests on.

## Done when

- [x] A cite naming another document does not add a page to the citing
      document's frozen set.
- [x] A test covers one same-document cite and one cross-document cite.
- [x] Gate green (`../../embarch-fleet/gate.md`, the Python bullet:
      `test_public_guard` ran, not skipped).
