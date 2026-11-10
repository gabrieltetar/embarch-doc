# 051 — `doc check` reports a cite of a page outside the document

**State:** open
**Source:** Linear issue EMB-120, filed by the supervisor landing `atlas/050`
**Issue:** EMB-120
**Scope:** atlas
**Hardware:** none
**Owner:** no

## What

A record or prose file that cites a page outside its document passes `embarch-atlas doc check` silently. Since `atlas/050` (`embarch-atlas` `bfeae59`), `doc freeze` keeps such a page out of its count, records it as `out_of_range` in the frozen entry and warns on stderr naming the unit and page. But the fault is in the record, and nothing reports it where the record is checked: the first sign is a warning at freeze time, after the record was accepted.

Make `doc check` report every unit that cites a page outside `1..pages` of the document's `doc.json`, naming the unit and the page. A cite of page 0 or one past the last page is the case to cover.

## Why now

An out-of-range cite can never match a real page, so its unit's key reads `missing` and it re-runs on every thaw. The check is the one place that would catch it before freeze.

## Where to look

- `src/embarch_atlas/freeze.py` `freeze` — already computes `out_of_range` per unit; reuse that test rather than writing a second one
- `src/embarch_atlas/check.py` — where a record is refused or reported today, and how `print_summary` / `run_check` report a fault
- `src/embarch_atlas/pdftext.py` `prep` — `doc.json` `pages`
- `tests/test_check.py`, `tests/test_freeze.py` — where the tests go
- `DESIGN.md` — wherever it lists what `doc check` checks

## Dispatch notes

- Decide whether an out-of-range cite is a failure or a warning in `doc check` by what `check.py` already does with a cite that names a page the number is not on; say which you chose and why in the task file. Amend `DESIGN.md` in place where it lists the checks.
- Burndown is on: no new numbered decision.
- The worktree needs `.atlas-local` linked beside it and a `.venv` of its own (both made for you); `test_public_guard` must run, not skip.
- No file in `embarch-doc/embarch-atlas/` is in doc-size reserve.

## Done when

- [ ] `doc check` reports a unit that cites a page outside `1..pages`, naming the unit and the page.
- [ ] A test covers a cite of page 0 and one past the end.
- [ ] Gate green (`../../embarch-fleet/gate.md`, the Python bullet); `changelog.d/` fragment dropped.
