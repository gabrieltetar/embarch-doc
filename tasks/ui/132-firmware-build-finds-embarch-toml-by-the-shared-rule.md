# 132 — firmware build finds `embarch.toml` by the shared rule

**State:** open — `api/224` landed the function this calls (`embarch_core_client::config_discovery::find_config_path`, api decision 152)
**Source:** EMB-306 — api, umbrella and ui each resolve `embarch.toml` their own way
**Issue:** EMB-306
**Scope:** ui
**Hardware:** none
**Owner:** no

## What

`src/firmware_build.rs` finds the config from `[build].config_path`, then
`EMBARCH_API_CONFIG`, then the open repo, with no walk; the API and the
umbrella each do it differently. `tasks/api/224` puts one resolver in
`embarch-core-client`, which the ui already depends on.

When this is done, the ui's firmware build calls that resolver, with
`[build].config_path` as the explicit path and the open repo as the start
directory, and its own copy of the order is gone. If the shared walk changes
what the ui finds in a case it handles today, say so in the decision and pin
the case with a test.

**Not yours:** every other repo. You never touch hardware.

## Where to look

- `src/firmware_build.rs`
- the function `tasks/api/224` adds to `embarch-core-client` (read only)

## Done when

- [ ] The firmware build resolves the config through `embarch-core-client`'s
      resolver and its own order is gone; tests cover `[build].config_path`,
      the variable and the open repo.
- [ ] A ui decision (or an amended one) records it.
- [ ] Gate green (`cargo build`, `cargo test`, `cargo clippy --all-targets --
      -D warnings`); `changelog.d/` fragment.
