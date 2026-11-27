# 227 — the Test-run verifier reads the attestation by the record's release

**State:** claimed by agent/api/227-the-test-run-verifier-reads-the-attestation-by-the-records-release, 2026-11-27 04:17 — reserve: api decisions/client-crate.md 456 B left (api/222), you should not need it; verify-report.md is not in reserve
**Source:** EMB-332 — a report cannot say which Core signed it; found by `api/225`'s worker and reviewer
**Issue:** EMB-332
**Scope:** api
**Hardware:** none
**Owner:** no

## What

`api/225` taught the Study verifier's check 6 (`src/verify_report.rs`) the new
attestation, keyed on the signed record's `predicate.observed.release`
(decision 124, amended). The **Test-run** verifier was left alone, and Core
writes both kinds of report through one function: `embarch-core`'s
`src/publish.rs` `attestation()` is called by `report_data` and by
`src/test_publish.rs` (around line 401). So when `tasks/core/193` changes that
function, every Test-run report gets the new shape too, and today's
`src/verify_test.rs` rejects it: its report-data comparison (around line 1074)
checks `have["core_attested"] == w["core_attested"]`, and the expected value
built around line 959 is `{ label, core_attested: false }`.

When this is done, the Test-run verifier applies the same rule as check 6:

- The Test-run record's `predicate.observed` **has** a `release` key: the
  report's `attestation` must be `{ label, core_mode, release, reason }`, with
  `core_mode` equal to `observed.mode` and `release` equal to
  `observed.release`, and no `core_attested` key.
- It does **not**: exactly today's `{ label, core_attested: false }`.
- `reason` is not compared. A mismatch names the field
  (`attestation.core_mode`, `attestation.release`, `attestation.core_attested`).

If the Test-run record has no `observed.mode`, say so in this file and stop:
the rule then needs a Core-side answer first. Share the comparison with
`verify_report.rs` rather than writing it twice, if the two fit one helper.

The Test-run appendix (`src/publish_test.rs`, the Attestation rows around line
293) prints Core mode and Release when the attestation carries them, and the
Core attested row only when it carries that, as `api/225` did for a Study.

Record it in the Test-run verify decision (amend in place) and the Test-run
row of `interfaces/verify.md`, or point both at decision 124 if that covers it.

**Not yours:** every other repo, `embarch-core` included. No `schema` bump.
You never touch hardware.

## Why now

`tasks/core/193` (the writing half) waits on this. Landing it first keeps the
rule `api/225` set: no `main` of Core writes a report the `main` of this repo
rejects.

## Where to look

- `src/verify_test.rs` (the expected report-data around line 959, the
  comparison around line 1074), `src/publish_test.rs` (Attestation rows)
- `src/verify_report.rs` (`check_report_claims`, `api/225`'s rule) and its
  test in `tests/verify.rs`
- `embarch-core/src/test_publish.rs` and `src/publish.rs` (read only)
- `embarch-doc/embarch-api/decisions/verify-report.md` (124) and the
  Test-run verify and publish decisions
- **Size:** `decisions/client-crate.md` is in reserve (456 B left,
  `tasks/api/222`); you should not need it.

## Done when

- [ ] A Test-run fixture whose record carries `observed.release` and the new
      attestation verifies, in service and in development mode.
- [ ] Altering `core_mode` or `release` fails, naming the field.
- [ ] A Test-run fixture with no `release` key and today's attestation still
      verifies.
- [ ] The Test-run appendix prints mode, release and reason when present.
- [ ] Decision and `interfaces/verify.md` say so.
- [ ] Gate green (`cargo build`, `cargo test --workspace`, `cargo clippy
      --workspace --all-targets -- -D warnings`); `changelog.d/` fragment.
