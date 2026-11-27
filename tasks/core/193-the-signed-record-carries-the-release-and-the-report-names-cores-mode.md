# 193 — the signed record carries the release, and the report names Core's mode

**State:** open — `api/227` landed (`embarch-api` `1faf5be`): the Test-run verifier and appendix take the new attestation by the record's `observed.release`, through check 6's own helper; `api/225` (Study reports) landed earlier
**Source:** EMB-332 — a report cannot say which Core signed it
**Issue:** EMB-332
**Scope:** core
**Hardware:** none
**Owner:** no

## What

`publish.rs`'s `attestation()` writes `core_attested: false` with milestone
1's reason on every report. When this is done, a report names the Core that
signed it: its mode, and the release it was installed from.

**Both report kinds.** `attestation()` is called by `report_data` and by
`src/test_publish.rs`, so a Test-run report changes with a Study report.
`embarch-api` accepts the new shape for a Study since `api/225` (check 6) and
for a Test run once `api/227` lands, which is why this waits on `api/227`. A
Test-run record's `observed` gains `release` by the same rule as a study's; it
carries `mode` since `tasks/core/195` (which `api/227` waits on), and a
Test-run report's `core_mode` is copied from that, as a Study report's is.

The shape is fixed by `tasks/api/225`, which lands first and makes
`embarch-api`'s check 6 accept it (its task file is retired when it lands;
`embarch-api`'s `decisions/verify-report.md` then carries the rule). Build
against exactly this:

- The signed record's `predicate.observed` gains `release`: `null` for a Core
  with no `<data dir>/installed-release.json` that lists its own binary, else
  `{ "suite_version": <string>, "manifest_sha256": <hex string> }` taken from
  that file. The key is always present, `null` included: its presence is what
  tells check 6 a record is the new shape. `observed.mode` is unchanged.
- `report-data.json`'s `attestation` becomes `{ label, core_mode, release,
  reason }`, with `core_mode` and `release` copied from the signed record, and
  drops `core_attested`.
- `reason` by mode. Service: "signed by a service Core installed from
  <release>; attested only where `verify` matches the fingerprint the engineer
  gave". Development: unattested, as today, saying why.

Amend core decision 119 (`decisions/publish.md`) and the record's decision in
`decisions/signing.md` in place, and update `interfaces/publish.md` and the
record's interface doc. If `installed-release.json`'s shape
(`interfaces/installed-release.md`) does not carry a suite version and a
manifest SHA-256, say so in this file and stop: that file's writer is a
signed-release install, not this task.

**Not yours:** every other repo, `embarch-api` included. No record `schema`
bump: `observed.call_log` was added the same way, as an additive key. You
never touch hardware.

## Why now

The owner filed it from the HIL attested phase's plan
(`notes/hil/14-implementation-plan.md`; `notes/hil/12-prevention.md`, "The root
of trust").

## Where to look

- `src/publish.rs` (`attestation`, `report_data`), `src/signing.rs` (the
  record's `observed`), `src/service.rs` (`RELEASE_RECORD_FILE`,
  `check_release_record`)
- `embarch-doc/embarch-core/decisions/publish.md` (119),
  `decisions/signing.md`, `interfaces/publish.md`,
  `interfaces/installed-release.md`
- **Size:** `decisions/signing.md`'s decision 110 is 2,486 B over its own
  limit; touch it only if this changes what it says, and do not grow it.
  `spec.md` is 9,008 of 10,240 B, 31 B under its reserve line since
  `core/186` compacted it; any growth puts it back in reserve, so file the
  debt in the same commit if it does.

## Done when

- [ ] The signed record carries `observed.release`, `null` in development and
      in tests with no release file, the file's two values when it lists this
      binary.
- [ ] Publishes from a service-mode and a development-mode record write the
      new attestation, with the reason by mode.
- [ ] Decisions and interface docs say so.
- [ ] Gate green (`cargo build`, `cargo test`, `cargo clippy --all-targets --
      -D warnings`); `changelog.d/` fragment.
