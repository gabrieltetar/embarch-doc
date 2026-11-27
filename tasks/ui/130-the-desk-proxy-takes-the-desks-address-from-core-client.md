# 130 — the desk proxy takes the desk's address and token from `embarch-core-client`

**State:** open — `api/223` landed the module this calls (`embarch-core-client::desk_discovery`, api decision 151)
**Source:** EMB-305 — four clients re-derive the desk's token and port, and one copy has drifted
**Issue:** EMB-305
**Scope:** ui
**Hardware:** none
**Owner:** no

## What

`src/desk.rs` re-derives where the desk lives: `DEFAULT_PORT`, `token_path()`
(`EMBARCH_DESK_CONFIG_DIR`, else `$XDG_CONFIG_HOME/embarch-desk`, else
`~/.config/embarch-desk`) and the `EMBARCH_DESK_PORT` parse in `desk_url()`.
`tasks/api/223` puts the clients' one copy of that rule in
`embarch-core-client`, which this crate already depends on. When this is done,
`desk.rs` asks that module for the token path, the port and the base URL, its
own copies are deleted, and the proxy's behaviour is unchanged. The test that
expects `:4891/view` reads the port from the module instead of guessing from
the environment.

Read `api/223`'s decision for the module's names before you start.

**Not yours:** every other repo. You never touch hardware.

## Where to look

- `src/desk.rs` (`DEFAULT_PORT`, `token_path`, `desk_url`, `desk_token`, the
  `the_rest_of_the_path_lands_on_the_desks_own_route` test)
- `embarch-api/crates/embarch-core-client/src/` (the module `api/223` added)
- `embarch-doc/embarch-ui/` — the decision that covers the desk proxy

## Where the doc goes

Amend the ui decision that says how the proxy finds the desk, in place, to
name the shared module. Check `scripts/check-doc-size.py --pressure` before
you edit a decision listed near its limit.

## Done when

- [ ] `desk.rs` holds no copy of the desk's port or token-path rule and calls
      `embarch-core-client`'s.
- [ ] Gate green (`cargo build`, `cargo test`, `cargo clippy --all-targets --
      -D warnings`); decision amended; `changelog.d/` fragment.
