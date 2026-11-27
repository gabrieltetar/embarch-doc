# embarch-core: the signed run record and the challenge route

**Status:** active, 2026-11-21 (`tasks/core/129`, [decision 110](../decisions/signing.md)). Index: [../interfaces.md](../interfaces.md).

| Method | Path | Body / query | Response |
|---|---|---|---|
| `POST` | `/auth/challenge` | **No token.** `{"nonce": "<32 to 128 lowercase hex, even count>"}`; nothing else is accepted | `200 {frame, core_nonce, mode, keyid, public_key, signature}`; `mode` is `service` or `development` (decision 129), Core's word and outside the signed `frame`; `400` for a nonce outside that shape. `signature` is lowercase hex of the Ed25519 signature over `frame` = `embarch-core-auth-v1\n<core_nonce>\n<nonce>`. Signs nothing else |
| `POST` | `/study`, `/host-studies` | optional query `build_commit` (7 to 64 lowercase hex), `build_dirty` (`true`/`false`), `build_toolchain` (printable, 200 bytes) | unchanged; the three are recorded as `claimed.build`, `400` when malformed |

## `record.dsse.json`

In `study_results/<study_id>/`, written when the run ends and before its status reads `completed`.

```
{ "payloadType": "application/vnd.in-toto+json",
  "payload": "<base64 of the Statement>",
  "signatures": [ { "keyid": "<SHA-256 of the public key, hex>", "sig": "<base64>" } ] }
```

The Statement: `_type` `https://in-toto.io/Statement/v1`; `subject` `[{name, digest: {sha256}}]`, one per file (`events.json`, `measurements.json` and `study.json` if present, every file directly under `streams/`), sorted by `name`; `predicateType` `urn:embarch:predicate:study-run:v1`; `predicate`:

| Key | Holds |
|---|---|
| `schema` | `1` |
| `study_id`, `kind` (`device` or `host`), `ended_utc_ms` | the run |
| `observed.core.version` | this binary's version |
| `observed.provenance` | `events.json`'s `provenance` object (null for a host study) |
| `observed.image_status` | `unverified` in milestone 1 |
| `observed.declarations` | `{witnessed_since_utc_ms, entries: [{what, name, scope, at_utc_ms}]}`; `what` is `role`, `signal`, `instrument`, `bootload_ports` or `dev_bench_link`, `scope` `agent` or `person` |
| `observed.ports_held` | the serial ports Core held when it sealed, sorted names (`[]` when none; decision 130) |
| `observed.probes_held` | the debug-probe serials Core held when it sealed, sorted (`[]` when none; decision 159) |
| `observed.mode` | `service` or `development`: the mode Core ran in (decision 129) |
| `observed.behaviours` | `measurements.json`'s `behaviours`, `{}` until it exists |
| `observed.call_log` | `{prev, head, length, first_seq, last_seq}`: the call log ([call-log.md](call-log.md)) as the run began and ended. `prev` is the head when the run began (the entry before the range; 64 zeros for an empty log), `head` the head when it ended (a pending fold is written first), `length` the log's length then. The range is the entries with `seq` `first_seq` to `last_seq`; both are null when no call was made, and `prev` equals `head`. Absent when the run was sealed with no call log to read, as one recorded before the call log existed (`tasks/core/145`; no `schema` bump) |
| `claimed.build` | `{commit, dirty, toolchain}` as embarch-api told Core, each null when not sent; `claimed.build` is null when none were |

Verify as any DSSE v1 envelope with the public key whose SHA-256 is `keyid`; then hash each named file and compare. The key file is `signing-key` in Core's store, with `public-key` (the raw public key, hex) beside it: `<data dir>/store/` under `run --service`, `<dir>` under `run --store <dir>`, the data dir beside the token files ([embarch-token.md](../../embarch-token.md)) with neither ([decision 129](../decisions/auth.md)).

## `test-runs/<run_id>.test-run.dsse.json`

A Test run's own record ([decision 144](../decisions/test-run-record.md)), in Core's store beside `<run_id>.result.json`, written when the run ends: a finish, a cancel, a deadline, or at the next start for a run Core lost (`interrupted`). The same envelope as above and verified the same way. `subject`: `run.json` (the SHA-256 of its canonical form) and `result.json` when kept. `predicateType` `urn:embarch:predicate:test-run:v1`; `predicate`:

| Key | Holds |
|---|---|
| `schema`, `run_id`, `status`, `reason`, `ended_utc_ms` | the run; `status` is `completed`, `cancelled`, `deadline` or `interrupted` |
| `unit_key` | the DUT's hardware ID the first bench's smoke check read; null when none was |
| `resumes` | the run this one resumes; absent when none |
| `selection` | `{entries: [{test_id, status, reason, expanded}]}` as Core expanded it at the prepare |
| `tests[]` | per `run.json` test: `test_id`, `bench`, `definition_hash`, `requirements`, `verdict` (null for a test with no result), `reason` (the verdict's, or `not_run` / `interrupted`), `note`, `dut_image` (`holds`, `differs`, `claim`; null when the bench was not checked), `study_records` `[{study_id, record_sha256}]` |
| `observed.core.version`, `observed.mode`, `observed.call_log` | as a study record's; `mode` is `service` or `development`, additive (`tasks/core/195`, no `schema` bump) |

Each study record is still `record.dsse.json` in its own folder; its `record_sha256` here is the file's hash. A study record made for a test in a Test run is amended at the run's end ([decision 145](../decisions/test-run-record.md)): `run.json` joins its subjects and its predicate gains `test`: `run_id`, `test_id`, `bench`, `definition_hash`, `run_index`/`run_count`, `run` and `verdict` (`{verdict, reason, qualifiers}`; `run` is this study's, null when none was judged), `note`, `unit_key`, `images`, `identities`, `instruments` (the smoke check's findings; null when the bench was never checked) and `prompts` (`list`, `step`, `prompt_id`, `detail`, `answered_by`, `answered_scope`). A plain study's record has no `test`. The amended file's hash is bound by the run's `test_run` entry ([decision 146](../decisions/test-run-record.md)), not the study's `run` entry.
