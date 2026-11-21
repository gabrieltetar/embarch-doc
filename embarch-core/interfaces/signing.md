# embarch-core: the signed run record and the challenge route

**Status:** active, 2026-11-21 (`tasks/core/129`, [decision 110](../decisions/signing.md)). Index: [../interfaces.md](../interfaces.md).

| Method | Path | Body / query | Response |
|---|---|---|---|
| `POST` | `/auth/challenge` | **No token.** `{"nonce": "<32 to 128 lowercase hex, even count>"}`; nothing else is accepted | `200 {frame, core_nonce, keyid, public_key, signature}`; `400` for a nonce outside that shape. `signature` is lowercase hex of the Ed25519 signature over `frame` = `embarch-core-auth-v1\n<core_nonce>\n<nonce>`. Signs nothing else |
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
| `observed.behaviours` | `measurements.json`'s `behaviours`, `{}` until it exists |
| `claimed.build` | `{commit, dirty, toolchain}` as embarch-api told Core, each null when not sent; `claimed.build` is null when none were |

Verify as any DSSE v1 envelope with the public key whose SHA-256 is `keyid`; then hash each named file and compare. The key file is `signing-key` beside the token files ([embarch-token.md](../../embarch-token.md)).
