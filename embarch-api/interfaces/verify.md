# embarch-api: `verify`, the offline check of a published zip

**Status:** active, 2026-11-23. Split verbatim from [publish.md](publish.md) (`tasks/api/173`); the section below is unchanged.

## core-key

`embarch-api core-key [--json]` (CLI only; `src/core_key.rs`) runs `POST /auth/challenge` against the Core `status` reaches, with a fresh random 32-hex nonce and **no token**. It checks the frame, the Ed25519 signature and the `keyid` ([decision 129](../decisions/verify.md)) before printing the raw public key (64 hex, `verify --public-key`'s form) and its SHA-256 fingerprint. `--json`: `{success, public_key, fingerprint}`. A failed check or an unreachable Core exits 1 with `error`. It writes the key nowhere.

## verify

`embarch-api verify <zip> --public-key <hex> [--attested-fingerprint <hex>] [--json]` (CLI only, no MCP tool; `src/verify.rs`, behind `pdf`). It loads **no config and calls no Core**, and reads the zip and the key alone.

- `--public-key`: Core's raw Ed25519 public key (64 hex), got out of band, never read from the zip. Its SHA-256 is the key fingerprint (the DSSE `keyid`). A signature that does not verify under it, or names another `keyid`, fails check 0.
- `--attested-fingerprint`: the fingerprint of Core's elevated install. Equal to the key's, the origin reads attested. Absent or different, the result carries **"origin unattested"**, that the signatures prove integrity only and that the agent can read an unattested Core's key ([decision 119](../decisions/verify.md)).

Exit 0 when **no check failed**, 1 otherwise (a failed check, an unreadable zip or a bad key). `--json`: `{success, complete, zip, produced_by_embarch_api, verified_by_embarch_api, key_fingerprint, attested, origin, checks [{check, name, status, compared, problems}]}`. `success` is "none failed", `complete` is "every check ran in full and passed", so a caller that needs more than "nothing contradicted" reads `complete`. `status` is `pass`, `FAIL`, `partial`, `not checked by this version` or `not applicable`. `produced_by_embarch_api` is the zip's own appendix's claim.

| Check | What this version does |
|---|---|
| 0 signatures | The manifest, `record.dsse.json` and `report-data.dsse.json` verify as DSSE v1 (PAE) under the key; the record's subjects hash to the zip's files and cover `events.json`, `measurements.json`, `study.json` and every `streams/*`; the report-data envelope signs this `report-data.json` |
| 1 manifest | Every Core subject and every `embarch_api_files` entry hashes as listed; every zip file is one or the other; the manifest's `record_sha256` and `report_data_sha256` are the files' |
| 2 measurements | Each declared measurement re-run over `streams/<tap>.csv` with the behaviour `record.dsse.json` names; value, reducer and behaviour compared. **Partial**: a behaviour this build lacks, `interval` and `value_at_marker` (markers need a text tap's arrival stamps), Text and trace taps, and **every step outcome** (`until` and `refused_on` re-evaluation) are reported "not recomputed" ([decision 120](../decisions/verify.md)) |
| 3 verdicts | Not applicable to a Study |
| 4 PDF text | Every number in `report.pdf` (the shared crate's extractor and grammar) matches a signed measurement, a value `report-data.json` or `events.json` holds, a listed number of the prose and `report.typ` rescan, an axis tick `plot_ticks` derives from the plot's signed series, the footer's page number (equal to the page's index) or, **partial**, a number only `appendix.typ` prints; a cited number that does not match, an unreadable glyph or a wrong footer fails ([decision 123](../decisions/verify-report.md)) |
| 6 report claims | Every field of `report-data.json` recomputed from the record, `events.json`, the segment and the manifest; `observed.call_log` (`{head, first_seq, last_seq, count}`) present exactly when the record carries one, a missing or differing one failing by name; the PDF prints the run id, status, step counts, label, `go_by`, `published_by` and revision as it says ([decision 124](../decisions/verify-report.md)) |
| 9 pictures | `report.typ` and `appendix.typ` held to the syntax-tree whitelist `publish` also applies; each plot's file is in the zip; every `typst-packages/` file hashes to this build's list ([decisions 122, 125](../decisions/verify-report.md)) |
| 5 labels | The attestation label, `go_by` and `published_by` recomputed from the run log's segment, the manifest and the record (`adopted` is compared whole in check 6); each note and prose file hashes to the text Core recorded; a notes/prose file nobody adopted fails |
| 7 exports | `junit_xml` and `ocp_jsonl` regenerated from `report-data.json`, `measurements.json` and `events.json`'s steps, byte for byte |
| 8 run log | Every hash, `prev` and `seq` recomputed; the chain ends at the manifest's signed head and length; one `run` entry for this run names `record.dsse.json`'s hash and each capture's; with a `call-log-segment.jsonl`, its header must equal the signed record's `observed.call_log` (`prev`, `head`, `first_seq`, `last_seq`), every hash, `prev` and `seq` recomputes from the signed `prev` to the signed `head` over exactly that range, and every entry the record cites (`call_log.cites`, `{seq, hash}`) is in it; no segment and no range in the record reads "no call log" and passes; a record naming a range with no segment, or a segment with no range, fails; the publish's own entry and any later revision are **not checkable offline** and the result says so |
