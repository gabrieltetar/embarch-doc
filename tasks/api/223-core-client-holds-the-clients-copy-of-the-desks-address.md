# 223 — `embarch-core-client` holds the clients' one copy of the desk's address and token rule

**State:** open
**Source:** EMB-305 — four clients re-derive the desk's token and port, and one copy has drifted
**Issue:** EMB-305
**Scope:** api
**Hardware:** none
**Owner:** no

## What

`embarch-desk/src/paths.rs` owns where the desk lives: its config dir
(`EMBARCH_DESK_CONFIG_DIR` taken as the folder itself, else
`$XDG_CONFIG_HOME/embarch-desk` with an empty value read as unset, else
`$HOME/.config/embarch-desk`), its data dir (`EMBARCH_DESK_DATA_DIR`, else
`$XDG_DATA_HOME/embarch-desk`, else `$HOME/.local/share/embarch-desk`), its
port (`EMBARCH_DESK_PORT` parsed as a `u16`, else 4891) and its token file
(`desk-token` in the config dir). `embarch-api/src/session_desk.rs` and
`embarch-ui/src/desk.rs` each spell that out again by hand.

When this is done, `embarch-core-client` has one public module, in the mold of
`token_discovery` (Core keeps its own rule; the clients share one copy of it),
that returns the desk's config dir, data dir, token path, port and base URL
with exactly the desk's precedence, and `session_desk.rs` calls it with its own
copies (`home`, `desk_dir`, `data_dir`, `config_dir`, `desk_port`,
`DESK_DEFAULT_PORT`) deleted. The module reads; it never creates the token,
which stays the desk's job. Tests cover each step of each precedence, the
empty-`XDG_*` case and an unparsable port, without racing other tests over the
process environment (follow whatever the crate already does for env tests).

`embarch-desk` does not take this crate: it has no path dependency today, and
this one would bring `embarch-topology` and `embarch-study-designer` into it.
That, and that chat keeps one TypeScript copy (`tasks/chat/053`), goes in the
decision. `embarch-ui` moves onto the module in `tasks/ui/130`, which waits on
this. The generic XDG base-dir helpers elsewhere in the suite (`user_dirs.rs`
among them) are out of scope; say so in the decision rather than leave it
implied. Reuse `user_dirs.rs` if it fits, but do not change what it returns.

**Not yours:** every other repo. You never touch hardware.

## Where to look

- `src/session_desk.rs` (lines 30 to 80)
- `crates/embarch-core-client/src/token_discovery.rs`, `src/user_dirs.rs`,
  `src/lib.rs`
- `embarch-desk/src/paths.rs` (read only: the rule you copy)
- `embarch-doc/embarch-api/decisions/session-desk.md` (decision 85)

## Where the doc goes

**`decisions/client-crate.md` is in reserve: 11,828 of 12,288 B, 460 B left,
filed under `tasks/api/222`.** Do not grow it. Put the new decision in a new
topic file (for example `decisions/desk-discovery.md`) with an index row, and
keep `decisions/session-desk.md` true about where `session_desk.rs` now gets
the desk's location.

## Done when

- [ ] One public module in `embarch-core-client` returns the desk's config dir,
      data dir, token path, port and base URL, with tests for every precedence
      step; `session_desk.rs` calls it and its own copies are gone.
- [ ] A new api decision records where the clients' rule lives, why the desk
      does not take the crate, that chat holds the one TypeScript copy, and
      that generic XDG helpers are out of scope.
- [ ] Gate green (`cargo build`, `cargo test`, `cargo clippy --all-targets --
      -D warnings` at the workspace root); `changelog.d/` fragment.
