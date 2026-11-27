# 225 — check 6 reads the attestation by the signed record's mode and release

**State:** done — check 6 reads the attestation by the record release key; fixtures, appendix, decision 124 amended, verify.md row 6
**Source:** EMB-332 — a report cannot say which Core signed it
**Issue:** EMB-332
**Scope:** api
**Hardware:** none
**Owner:** no

## What

Every published report's `report-data.json` carries
`attestation: { label, core_attested: false, reason }`, and `verify` check 6
(`src/verify_report.rs`) recomputes `label` and `core_attested` and nothing
else. Once a service Core exists the report should name **the Core's mode and
the release it came from**, and leave the word "attested" to `verify` and the
fingerprint. Core writes that claim and this repo checks it. This task is the
checking half, and it lands **first**, so that no `main` of Core ever writes a
report the `main` of this repo rejects. `tasks/core/193` is the writing half
and waits on this one.

**The shape, fixed here so both halves build against it:**

- A Core that writes the new claim also puts a `release` key in the signed
  record's `predicate.observed`: either `null` or
  `{ "suite_version": <string>, "manifest_sha256": <hex string> }`.
  `predicate.observed.mode` (`"service"` or `"development"`) is already there.
- When the signed record's `observed` **has** a `release` key, `report-data.json`'s
  `attestation` must be `{ label, core_mode, release, reason }`, with
  `core_mode` equal to `observed.mode` and `release` equal to `observed.release`,
  and **no** `core_attested` key.
- When it does **not** (every record a Core writes today, milestone-1 and Live
  zips included), check 6 expects exactly what it expects today:
  `{ label, core_attested: false }`, `reason` not compared.
- `reason` stays Core's wording and is not compared, as now.
- A `report-data.json` whose attestation does not match fails check 6 and
  names the field (`attestation.core_mode`, `attestation.release`,
  `attestation.core_attested`), the way `observed.<sub>` is named today.

The appendix (`src/publish_report.rs`, the attestation rows) prints Mode,
Release and Reason when the attestation carries them, and the Core attested
row only when it carries that. If the PDF claim list in check 6 can name the
mode it prints, add it there.

Record the rule as an `embarch-api` decision (a new one, or amend decision 124
in place if it fits in a sentence), and update `interfaces/verify.md` row 6.

**Not yours:** every other repo, `embarch-core` included. No `schema` bump of
`report-data.json` or of the record: the discriminator is the record's own
`release` key. If you find that is not enough, stop and say so in this file
rather than bump a version. You never touch hardware.

## Why now

The owner filed it from the HIL attested phase's plan
(`notes/hil/14-implementation-plan.md`; `notes/hil/12-prevention.md`, "The root
of trust": what makes a run attested is its key, not a mark in its record).

## Where to look

- `src/verify_report.rs`, check 6 (`check_report_claims`)
- `src/publish_report.rs`, the attestation rows (around line 320)
- `embarch-core/src/publish.rs` `attestation()` and `embarch-core/src/signing.rs`
  (read only): what Core writes today
- `embarch-doc/embarch-api/decisions/verify-report.md` (decision 124),
  `interfaces/verify.md` row 6
- **Size:** `decisions/client-crate.md` is in reserve (456 B left,
  `tasks/api/222`); you should not need it.

## Done when

- [x] Fixture zips built from a service-mode record and from a
      development-mode record, each carrying `observed.release` and the new
      attestation, pass check 6.
- [x] The same zip with `core_mode` altered fails check 6, naming
      `attestation.core_mode`; likewise `release`.
- [x] A fixture with no `release` key in its record and today's attestation
      still passes check 6.
- [x] The appendix prints the mode, the release and the reason when present.
- [x] Decision recorded; `interfaces/verify.md` row 6 says what check 6 compares.
- [x] Gate green (`cargo build`, `cargo test --workspace`, `cargo clippy
      --workspace --all-targets -- -D warnings`); `changelog.d/` fragment.
