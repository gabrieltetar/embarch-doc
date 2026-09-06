# Make `interfaces/limits.md` enumerate the constants it claims to, and fix two wrong sizing notes

**State:** open
**Source:** owner's repo survey, 2026-09-06 — `interfaces/limits.md:5` claims "Every bound the crate declares"
**Scope:** study-designer
**Hardware:** none
**Owner:** no

## What

`embarch-doc/embarch-study-designer/interfaces/limits.md:5` says it holds "Every bound the crate
declares". Its table omits `MAX_LOG_LINE_LEN`, `MAX_FIRMWARE_VERSION_LEN`, `MAX_VERSION_OVERRIDES`,
`MAX_GATT_CSV_ROW_LEN` and **all twenty `.eap` constants** present in `src/limits.rs:30-213`.

Two rows are also wrong, and these are the part with real evidence: `MAX_DISCOVERED_SERVICES` says
"the real DUT declares 3 services" where `src/limits.rs:80-84` says 2, and `MAX_CHARS_PER_SERVICE`
says "the Device Management Service at 8 characteristics" where `src/limits.rs:85-88` says the
Sensor Data Service at 7.

Every constant gets a row with its value and an `[assumed]` / `[measured <date>]` marker, and the
two sizing notes are reconciled against the code comments they were derived from — the survivor
dated, per `../../DOC-CONVENTIONS.md`.

## Why now

This table is the sizing reference `spec.md` sends readers to for "every capacity bound lives in one
`limits` module", and the `.eap` bounds it omits are the ones that cost dev-bench SRAM. It is
bookkeeping with no failure behind it, filed as such — the value is that the table is currently
unusable as the reference it advertises.

## Done when

- [ ] Every `pub const` in `src/limits.rs` has a row, and no row names a constant that does not exist.
- [ ] The two contradicting `[measured]` notes are reconciled, with the survivor dated.
- [ ] Any derived bound (`MAX_DECODERS_PER_STUDY`, `MAX_EAP_FIELD_NAME_LEN`) is shown as the
      expression rather than a copied number.
- [ ] The file stays inside its size cap.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false.
