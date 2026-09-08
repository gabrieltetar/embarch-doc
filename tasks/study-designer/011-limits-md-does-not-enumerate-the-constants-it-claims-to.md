# Make `interfaces/limits.md` enumerate the constants it claims to, and fix two wrong sizing notes

**State:** done — leg 046
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

- [x] Every `pub const` in `src/limits.rs` has a row, and no row names a constant that does not
      exist. Verified by diffing the two name lists directly: all 44 `pub const`s in
      `src/limits.rs` (26 in the main section, 18 in the `.eap` section — not "twenty" as this
      task's own `What` estimated) now have exactly one row each in
      `embarch-doc/embarch-study-designer/interfaces/limits.md`, and two rows that named
      constants absent from the source (`MAX_BATCH_SAMPLES`, already retired and already
      tombstoned further down the file; `MAX_DECLARED_SERVICES`, which never existed as a
      `pub const` — `DeclaredGatt.services` is host-side only and never gets a fixed-capacity
      bound, per `decisions/seals.md`) are gone from the active table.
- [x] The two contradicting `[measured]` notes are reconciled, with the survivor dated.
      `git log -S` on `src/limits.rs` traces both comments (`declares 2` services,
      `Sensor Data Service) declares up to 7`) to the same commit, `c8bb166`, 2026-08-23 — that
      date is the survivor, superseding the doc's mismatched 2026-08-26/2026-08-20 notes for
      "3 services" / "Device Management Service at 8 characteristics", which the code never said.
- [x] Any derived bound (`MAX_DECODERS_PER_STUDY`, `MAX_EAP_FIELD_NAME_LEN`) is shown as the
      expression rather than a copied number.
- [x] The file stays inside its size cap (10,208/12,288 B, below the 90% reserve line — no new
      compaction task owed).
- [x] Gate green (`../../embarch-fleet/protocol.md` §10): `cargo build`/`test`/`clippy --all-targets
      -- -D warnings` clean in `embarch-study-designer` (no code changes were needed — this was a
      doc-only fix); `scripts/check-docs.py` (10/10), `check-client-names.py --repo <code
      worktree>`, and `check-ownership.py --scope study-designer` / `--code-repo` all pass in
      `embarch-doc`.
- [x] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false. Checked all three: none needed a content
      change — `spec.md`'s pointer to `interfaces/limits.md` and `decisions/limits.md`'s pointer
      to the same file were already accurate and untouched; `open.md` had no bullet about this
      table's completeness to close. Dropped
      `changelog.d/study-designer-limits-enumerate.fixed.md` (185 B). No `status.d/` fragment:
      nothing suite-level changed — this table isn't referenced by value from any shared doc.
