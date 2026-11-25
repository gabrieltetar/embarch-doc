# embarch-umbrella: `embarch install-core` and `installed-release.json`

**Status:** active, 2026-11-25. Built for EMB-338 (`tasks/umbrella/110`). Why: [decision 61](../decisions/install-core.md). Index: [../decisions.md](../decisions.md).

`embarch install-core <SOURCE> [--allow-downgrade] [--dry-run] [--data-dir DIR] [--trusted-root FILE | --refresh-trust-root]`. `SOURCE` is an unpacked release folder or its archive. Exit `0` only when the release verified and the record was written; `1` otherwise, with the reason on stderr.

**Files, under the data dir** (`/var/lib/embarch` or `%ProgramData%\embarch`):

- `release-staging/<n>/`: one verified copy per successful run, `n` counting up from 1. Owner-only on Unix; Administrators and SYSTEM on Windows. A failed run removes its own folder.
- `installed-release.json`: the last install, replaced by temp file and rename.

**The record** (`schema_version` 1):

| Field | Meaning |
|---|---|
| `suite_version` | From the verified manifest |
| `manifest_sha256` | SHA-256 of the staged `embarch-manifest.json` |
| `identity`, `issuer` | The certificate identity and OIDC issuer that signed it |
| `log_time` | The transparency log entry's time, or `null` |
| `binaries` | File name to SHA-256, for each of `embarch`, `embarch-core`, `embarch-api` present in the release |
| `allow_downgrade` | `--allow-downgrade` was passed |
| `downgraded` | This suite was older than the one it replaced |
| `previous_suite_version` | The replaced version, or `null` for a first install |
| `staging` | `release-staging/<n>`, relative to the data dir |
| `installed_at` | UTC, RFC 3339, whole seconds |

**Order of the elevated half:** create the staging folder restricted; copy or unpack; verify on the copy; compare versions; hash the manifest and binaries; write the record. Any failure removes the staging folder and leaves an existing record as it was. Versions that are not `major.minor.patch[-pre]` cannot be ordered and are refused without `--allow-downgrade`.
