# 087 — Read a reference manual whose chapters sit under one root bookmark and whose register pages are Nordic-style

**State:** claimed by agent/atlas/087-read-a-nordic-style-reference-manual, 2026-11-19 00:00
**Source:** Fleet Ready issue: on a 940-page Nordic product specification that serves as the reference manual, `mcu rm-outline` found 1 chapter across 2,208 sections and `mcu vote` parsed 0 register sections, so that MCU's SVD gets no `conflict`, `quirk` or `rule` records.
**Issue:** EMB-32
**Scope:** atlas
**Hardware:** none
**Owner:** no

## What

`embarch-atlas mcu rm-outline` and `mcu vote` read a second reference-manual layout beside the ST one, the one the owner reported from an nRF54L-series datasheet:

- **Outline.** The PDF has exactly one level-1 bookmark, the file name, and every chapter sits under it at level 2 (Contents, Feature overview, Product overview, Application core, and so on); numbered sections are level 3 and below. `build_outline` counts `level == 1` as chapters, so it sees one. When the outline has a single level-1 entry whose children are the document's chapters, those children are the chapters.
- **Register sections.** A register is a numbered heading carrying the bare register name (`5.6.1.1 TASKS_CONSTLAT`), not a title ending `(PERIPH_REG)`, so `REG_NAME_RE` flags none. Under it the page prints `Address offset: 0x30`, a description line, a `Bit number 31 30 ... 0` row, an `ID` row placing each field's letter under its bits, a `Reset 0x00000000` row followed by one digit per bit, and a field table headed `ID R/W Field Value ID Value Description`, one row per field keyed by its letter, with enumerated values on the rows beneath it.

`parse_register_section` reads that page into the same register record the ST layout yields: offset, reset value, and each field's bit range (from the letter's position in the `ID` row), access and name.

## Why now

The owner pasted the outline's first two levels and one register page on the issue, which is what the earlier send-back asked for.

## Dispatch notes

- Fixtures are **synthetic**: build them in the shape above with invented peripheral and register names. No vendor PDF and no copied page text go into this public repo.
- Find out which register-section signal the outline gives for this layout (a container titled `...Registers` with numbered children, or something else) and say in `DESIGN.md` what the detector keys on.
- The ST fixtures' results must not change. If a heuristic for the single-root outline could misfire on an ST manual (a real ST outline with one level-1 entry), guard it and say how.
- Code: `src/embarch_atlas/rm.py` (`build_outline`, `REG_NAME_RE`, `REG_CONTAINER_RE`), `src/embarch_atlas/vote.py` (`register_sections`, `parse_register_section`, `BIT_RE`), `skills/atlas-translate-docs/reference/rm-procedure.md` if the procedure names the layout.
- No file of this sub-project is in reserve.
- **Owed, owner-side, not a Done-when item:** one `mcu rm-outline` and `mcu vote` run on the real datasheet. Write that into the task file's closing note as a debt.

## Done when

- [ ] A synthetic single-root outline yields its level-2 entries as chapters in `mcu rm-outline`.
- [ ] A synthetic Nordic-style register page is flagged as a register section and parsed by `mcu vote` into offset, reset and fields with correct bit ranges.
- [ ] The ST fixtures' results do not change (`tests/` stays green).
- [ ] `DESIGN.md` ("The MCU's own documents") says which reference-manual layouts are read and what each detector keys on.
- [ ] Gate green (`../../embarch-fleet/gate.md`, the Python bullet); `changelog.d/` fragment dropped; `embarch-doc/embarch-atlas/design.md` updated if it states what layouts are read.
