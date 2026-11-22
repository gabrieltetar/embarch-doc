# 170 — `verify <zip>` checks a published Study zip offline: signatures, manifest, measurements, labels, exports, run log

**State:** claimed by agent/api/170-verify-a-published-zip-offline, 2026-11-22 13:38
**Source:** `notes/hil/14-implementation-plan.md`, unit M1.11 ("verify"), its first half; the checks are `notes/hil/06-report-and-publish.md`, "Verify"
**Issue:** EMB-226
**Scope:** api
**Hardware:** none
**Owner:** no

## Dispatch notes

- `tasks/api/167` and `tasks/api/168` built the zip `verify` reads (`embarch-api` decisions 112 to 117, `interfaces/publish.md`): the manifest and its subjects, `report-data.json` and its DSSE, `run-log-segment.jsonl`, `measurements.json`, the two exports as pure functions (`publish_export::{junit_xml, ocp_jsonl}`), the adopted notes and prose and their recorded hashes, and the revision chain.
- `embarch-core` decisions 116 to 119 (`embarch-core/decisions/publish.md`, `interfaces/publish.md`) say what Core signs, how the manifest and the run-log head are written, and the two attestation labels; `embarch-core` decisions 113 to 115 say how `measurements.json` is computed, over the shared crate's `reducers` feature, which this crate may turn on too.
- **This half leaves three checks to `tasks/api/171`**: check 4 (the PDF's text, which needs the shared crate's text extractor and number grammar, `tasks/study-designer/088`), check 6 (`report-data.json` recomputed from the signed records) and check 9 (the syntax-tree whitelist of `report.typ`). Report each as "not checked by this version", never as passing.
- Per-decision budgets near their limit in `embarch-api`: `ledger#98` (15 B left), `bench-exchange#89` (122 B), `failure-reporting#67` (192 B). Put new decisions in a new `decisions/verify.md`, or in `decisions/publish-revisions.md`, rather than growing those. `embarch-api/open.md` is out of reserve at 3,525 of 5,120 B; keep it there.

## What

`embarch-api verify <zip>`, a CLI subcommand that reads only the zip and a key fingerprint the reader got out of band (a flag; never the one the report prints), with no Core call. It answers each check with what it compared and its verdict, names the embarch-api version that produced the zip and the one verifying it, and exits nonzero on any failed check. For a Study zip with no call log, the checks of 06 as they apply:

- **0, the signatures**: Core's signature over the manifest and over the study's record verifies against the given fingerprint; every capture, `events.json`, `measurements.json` and the study file is a subject of a signed record. A key that does not match an attested fingerprint verifies integrity only and says **"origin unattested"**, that its signatures prove integrity only, in the words 06 gives.
- **1, the manifest**: every file's SHA-256 matches.
- **2, the measurements**: every derived measurement recomputed from the raw captures with the behaviour versions the signed records name matches `measurements.json`; a version this build lacks is reported as not recomputed, never as matching. Step outcomes re-evaluated against their recorded replies, as far as a Study's signed study file carries the patterns.
- **3, the verdicts**: not applicable to a Study, and said so.
- **5, the labels**: the attestation label in `report-data.json` matches what the signed records say, and each note and adopted prose file hashes to the text Core recorded.
- **7, the exports**: JUnit XML and OCP T&V regenerated from the signed data match the zip's byte for byte.
- **8, the run log's segment**: the chain recomputes from the segment's first entry to its signed head, and every entry keyed on this run is accounted for; the call-log half answers "no call log". A later revision is not checkable offline, and the result says so.

## Why now

The first half of EMB-226, unblocked when EMB-225 (`tasks/api/167`, `168`) landed. M1.13's guide and M1.14's first real publish need a `verify` to point a reader at.

## Done when

- [ ] `verify` passes a fixture zip that `publish` wrote in a test.
- [ ] It fails each tampered copy, one test each: a changed number in `measurements.json` (check 1 or 2), a forged attestation label (check 5), an edited note or prose file (check 5), a dropped run-log entry (check 8), and a key that is not the given fingerprint (check 0).
- [ ] An unattested key's result carries 06's "origin unattested" wording; checks 4, 6 and 9 read "not checked by this version".
- [ ] `interfaces/` and `spec.md` amended; new numbered decisions.
- [ ] Gate green (`../../embarch-fleet/gate.md`), `changelog.d/` fragment dropped, `status.d/` fragment for anything suite-level it made false.
