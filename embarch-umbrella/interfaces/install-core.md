# embarch-umbrella: `embarch install-core` and `installed-release.json`

**Status:** active, 2026-11-27. Built for EMB-338 (`tasks/umbrella/110`) and EMB-339 (`tasks/umbrella/119`). Why: [decisions 61 and 69](../decisions/install-core.md). Index: [../decisions.md](../decisions.md).

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
| `binary_sha256` | Array of lowercase hex: the SHA-256 of the staged `embarch-core`, empty when the release holds none. The shape Core's `install --service` reads ([installed-release](../../embarch-core/interfaces/installed-release.md)); added by [decision 69](../decisions/install-core.md), `binaries` kept |
| `allow_downgrade` | `--allow-downgrade` was passed |
| `downgraded` | This suite was older than the one it replaced |
| `previous_suite_version` | The replaced version, or `null` for a first install |
| `staging` | `release-staging/<n>`, relative to the data dir |
| `installed_at` | UTC, RFC 3339, whole seconds |

**Order of the elevated half:** create the staging folder restricted; copy or unpack; verify on the copy; compare versions; hash the manifest and binaries; write the record. Any failure removes the staging folder and leaves an existing record as it was. Versions that are not `major.minor.patch[-pre]` cannot be ordered and are refused without `--allow-downgrade`.

**The Windows half** (decision 69), after the record is written, on Windows with the default data dir only: one generated PowerShell script run through `Start-Process -Verb RunAs`, logging to `%TEMP%\embarch-install-core.log` from inside the elevated context. Steps, each logged `STEP <n> OK <name>`: `0 preflight` (refuses an existing store not owned by Administrators, SYSTEM or the service, before any write), `1 binary` (`%ProgramFiles%\EmbArch\core\<version>\`), `2 store`, `3 firmware-staging`, `4 tokens`, `5 register` (`embarch-core install --service --bind <addr>`), `6 start-and-fingerprint` (`core-fingerprint` beside the token files, also printed). A failed step logs `FAILED: step <n> <name>: <why>`; the script ends `=== done ===`. The command exits `1` unless every step reported OK, the end marker and a 64-hex `FINGERPRINT` line are present; a missing transcript is a failure. `--dry-run` prints the paths and ACLs. Elsewhere it prints that the half did not run.
