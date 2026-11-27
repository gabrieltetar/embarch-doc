# embarch-umbrella decisions: Which config `doctor` and `status` read

**Status:** active, 2026-11-27.

Index: [../decisions.md](../decisions.md). Current truth: [../spec/commands.md](../spec/commands.md)'s `doctor` and `status` rows.

### 73 — `doctor` and `status` find `embarch.toml` through `embarch-core-client`'s resolver, so they inspect the file the API loads

`find_config_path` walked up to the first `.git` ancestor and took `<repo>/embarch/embarch.toml`; it read neither `--config` nor `EMBARCH_API_CONFIG`. With either set for the API, `doctor` checks 6, 8 and 10 read another file or none, and `status` resolved its token with `resolve_token(None, None)`, so a config with a custom `token_env` read as "no token" while the API worked [measured by reading the code, EMB-306].

**Chosen:** `config::discover_config_path(explicit)` calls `embarch_core_client::config_discovery::find_config_path_with` (`embarch-api` decision 152): `--config`, then `EMBARCH_API_CONFIG`, then the nearest `embarch/embarch.toml` in the current directory or an ancestor. It returns `Ok(None)` only when nothing was named and the walk found nothing. A named path that is not a file is an error naming it, never a fall-through to another file; `doctor` reports it as check 6 `Fail` (with a fix naming the flag and variable), and `status` as `no-token` with that text.

**Who takes the flag:** `doctor` and `status` only. `init` scaffolds a config at the repo root (`find_repo_root`), reads nothing it did not write (decision 60) and takes no `--config`; it never called `find_config_path`. The walk now stops at the nearest `embarch/embarch.toml`, not the `.git` root, as the API's does.

**`status` resolves its token through the config it found** (`[core].token`, `token_env`), then the env var and file discovery, as `embarch-api` does. A config the walk found but this crate's mirror cannot parse is ignored by `status`, which stays a cheap liveness check; `doctor` check 6 is where a bad file is judged.
