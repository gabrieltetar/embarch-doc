# 195 — the Test-run record carries Core's mode

**State:** open
**Source:** EMB-597 — the Test-run record carries no `observed.mode`; found by `api/227`'s worker
**Issue:** EMB-597
**Scope:** core
**Hardware:** none
**Owner:** no

## What

`src/test_run_record.rs` (around line 126) builds the Test-run predicate with
`observed: { core: { version }, call_log }`. A Study record also carries
`observed.mode`, set from `crate::token_store::mode()` in `src/signing.rs`
(around line 374). EMB-332 makes every report name the mode of the Core that
signed it, checked against the signed record, and `embarch-api`'s Test-run
verifier (`tasks/api/227`) cannot check a Test-run report's mode against a
record that does not carry one.

When this is done, the Test-run record's `predicate.observed` carries `mode`,
set exactly as a Study record's is. Additive, like `call_log`: no `schema`
bump. Today's `embarch-api` verifier reads only `observed.call_log` from a
Test-run record, so a record carrying the extra key still verifies; pin that
with a test if Core has one that round-trips a record through its own reader.

**Only the record.** Do not change `report-data.json`'s `attestation` or
`publish.rs`'s `attestation()`: that is `tasks/core/193`, which waits on
`api/227`, which waits on this. Writing the new attestation before the API
accepts it would give a `main` of Core whose Test-run reports the `main` of
`embarch-api` rejects.

Record it in the Test-run record's decision (`decisions/test-run-record.md`,
amend in place) and its interface doc (`interfaces/signing.md` or wherever the
Test-run predicate's fields are listed).

**Not yours:** every other repo, `embarch-api` included. You never touch
hardware.

## Why now

The three-step order for EMB-332's Test-run half: this, then `api/227` (the
verifier), then `core/193` (the attestation).

## Where to look

- `src/test_run_record.rs` (the predicate), `src/signing.rs` (the Study
  record's `observed.mode`), `src/token_store.rs` (`mode()`)
- `embarch-doc/embarch-core/decisions/test-run-record.md`,
  `interfaces/signing.md`
- **Size:** `spec.md` is 31 B under its reserve line; you should not need it.
  `decisions/signing.md`'s decision 110 is over its own limit; do not grow it.

## Done when

- [ ] A Test-run record's `predicate.observed.mode` is present, in service and
      in development mode, equal to what a Study record would carry.
- [ ] No other field of the record or of `report-data.json` changes.
- [ ] The decision and interface doc say so.
- [ ] Gate green (`cargo build --workspace`, `cargo test --workspace`,
      `cargo clippy --workspace --all-targets -- -D warnings`);
      `changelog.d/` fragment.
