# 106 — A measured fact shows beside the datasheet claim it bears on, and a disagreement is a finding

**State:** open
**Source:** `notes/hil/05-live.md` ("Writing a finding back") and `notes/atlas/08-measured.md` ("A measured fact"); the write-back built by `atlas/105`
**Issue:** EMB-268
**Scope:** atlas
**Hardware:** none
**Owner:** no

## What

`atlas/105` gave the `measured` plane a writer: `live write-back` appends
`via: live` records to `<atlas dir>/measured.jsonl`, each with a receipt read
from Core's call log and an image ("read back", "as last flashed by Core" or
"unknown"), flagged when measured on a different build. Nothing reads them yet.
When this is done:

- **Lookups that return a claim** (`register`, `find_fact`, `part_card` and
  the like, CLI and MCP alike) show any measured fact bearing on it beside it:
  its value, `via`, its receipt's time and image, its flag if any, and the
  words "development evidence".
- **A check compares** a measured value with the claim it bears on and raises
  a finding in the mismatch report when they disagree. A value that agrees
  raises none and is still shown beside the claim. The finding's class and
  severity are this unit's call; `notes/atlas/09-interactions.md` has the
  open recommendation for naming a new class.
- **A fact measured on another build** is shown as such, and its finding says so.

Where to start: `src/embarch_atlas/measured.py` (105's writer and record
shape), `query.py`, `check.py`, `mismatch.py`, `records.py`; the repo's
`DESIGN.md` "Live".

## Why now

The write-back landed as `atlas/105`; a measured value helps only where a
reader sees it next to the claim it confirms or contradicts.

**Burndown leg: no new numbered decision.** The atlas keeps no numbered
decisions; amend `DESIGN.md` and `embarch-atlas/design.md` in place. If the
work needs a decision the owner must take, stop and say so in this file and in
your report.

## Done when

- [ ] A fixture register whose measured value differs from its datasheet reset value yields a finding in the mismatch report.
- [ ] `register` and `find_fact` show the measured value beside the datasheet's, labelled development evidence.
- [ ] A measured value that agrees yields no finding and is shown beside the claim.
- [ ] A fact measured on another build is shown and reported as such.
- [ ] Gate green (`../../embarch-fleet/gate.md`, the Python bullet), `test_public_guard` run and passed.
- [ ] `embarch-atlas/design.md` updated, `changelog.d/` fragment dropped.
