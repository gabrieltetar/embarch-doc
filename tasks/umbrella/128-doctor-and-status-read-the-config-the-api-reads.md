# 128 — `doctor` and `status` read the config file the API reads

**State:** claimed by agent/umbrella/128-doctor-and-status-read-the-config-the-api-reads, 2026-11-27 03:48
**Source:** EMB-306 — api, umbrella and ui each resolve `embarch.toml` their own way
**Issue:** EMB-306
**Scope:** umbrella
**Hardware:** none
**Owner:** no

## What

`src/config.rs` `find_config_path` walks up to the first `.git` ancestor and
takes `<repo>/embarch/embarch.toml`; it reads no `--config` and no
`EMBARCH_API_CONFIG`. So with either set for the API, `embarch doctor` checks
6, 8 and 12 read another file or none. And `embarch status` resolves its
token with `resolve_token(None, None)` (`src/main.rs`), so a config with a
custom `token_env` reads as "no token" while the API works.

When this is done, `find_config_path` calls `embarch-core-client`'s config
resolver (`tasks/api/224`), `embarch doctor` and `embarch status` take
`--config <path>` and honour `EMBARCH_API_CONFIG`, and `status` resolves its
token through the config it found, as the API does. Other callers of
`find_config_path` (`init` among them) keep working; say in the decision which
of them take the flag. Tests cover the flag, the variable and the walk for
both commands, and `status` finding a token through a config's `token_env`.

**Not yours:** every other repo. You never touch hardware.

## Where to look

- `src/config.rs` `find_config_path`, `src/init.rs` `find_repo_root`,
  `src/main.rs` (the `status` token read)
- the function `tasks/api/224` adds to `embarch-core-client` (read only)
- `embarch-doc/embarch-umbrella/decisions/reporting.md` (the token gap is
  noted there as an aside)

## Where the doc goes

**`open.md` is in reserve (4,553 of 5,120 B), parked under
`tasks/umbrella/127`.** Do not grow it. `decisions/agent-runtime.md`
(decision 67), `install-core-platforms.md` (72) and `agent-container.md`
(62) are over their per-decision limit; do not touch them.
`decisions/reporting.md` is in reserve too (11,503 of 12,288 B, 785 B left,
filed under `tasks/umbrella/129`, open): if the token-gap aside there needs a
line, keep it net-zero or smaller, and put the new decision in its own topic
file.

## Done when

- [ ] `doctor` and `status` take `--config` and honour `EMBARCH_API_CONFIG`,
      through `embarch-core-client`'s resolver, and inspect the file the API
      loads.
- [ ] `status` resolves its token through the config it found.
- [ ] An umbrella decision records it; `spec` and `interfaces` name the flag.
- [ ] Gate green (`cargo build`, `cargo test`, `cargo clippy --all-targets --
      -D warnings`); `changelog.d/` fragment.
