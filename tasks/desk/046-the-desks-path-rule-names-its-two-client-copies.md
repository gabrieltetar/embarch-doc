# 046 — the desk's path rule names its two client copies

**State:** blocked — waits on `tasks/api/223` and `tasks/chat/053`, which create the copies this names
**Unparks when:** `api/223` and `chat/053` have landed
**Source:** EMB-305 — four clients re-derive the desk's token and port, and one copy has drifted
**Issue:** EMB-305
**Scope:** desk
**Hardware:** none
**Owner:** no

## What

`src/paths.rs` owns where the desk lives (config dir, data dir, port, token
file). After `api/223` and `chat/053` the clients hold exactly two copies of
that rule: one Rust module in `embarch-core-client` and one TypeScript module
in `embarch-chat`. Nothing in the desk says so, so whoever next moves a desk
path or adds an environment override changes the desk alone and both copies
drift silently.

When this is done, the doc comments on `config_dir`, `data_dir`, `port` and
`desk_token` name both copies by path, and the desk's doc that states the
token and port contract says a change to the rule moves both copies in the
same pass. No behaviour changes.

Read `api/223`'s and `chat/053`'s decisions for the exact module names.

**Not yours:** every other repo. You never touch hardware.

## Where to look

- `src/paths.rs`
- `embarch-doc/embarch-desk/interfaces.md`, `interfaces/cli.md`,
  `spec/desks-knowledge-interfaces.md` (whichever states where the token and
  port come from)

## Where the doc goes

In place, in the doc that states the contract. Check
`scripts/check-doc-size.py --pressure` first: desk decision 56 is already over
its per-decision limit, so do not grow it.

## Done when

- [ ] `paths.rs` and the desk's contract doc name both client copies.
- [ ] Gate green (`cargo build`, `cargo test`, `cargo clippy --all-targets --
      -D warnings`); `changelog.d/` fragment.
