# 224 — `embarch-core-client` holds the one rule for finding `embarch.toml`

**State:** done — embarch-core-client config_discovery::find_config_path is the one rule; API calls it, find_config_upward gone; decision 152
**Source:** EMB-306 — api, umbrella and ui each resolve `embarch.toml` their own way
**Issue:** EMB-306
**Scope:** api
**Hardware:** none
**Owner:** no

## What

Three binaries find the config file three ways. The API takes `--config`,
then `EMBARCH_API_CONFIG`, then walks up from the working directory looking
for `embarch/embarch.toml` (`src/main.rs`, `find_config_upward`). The
umbrella walks up only to the first `.git` ancestor and takes
`<repo>/embarch/embarch.toml` there, reading neither the flag nor the
variable. The ui takes `[build].config_path`, then `EMBARCH_API_CONFIG`, then
the open repo, with no walk. So with one `--config` or the variable set,
`embarch doctor` can pass while the API runs from another file.

When this is done, `embarch-core-client` has one public function, in the mold
of its `token_discovery` module, that returns the config path from an
explicit path, the `EMBARCH_API_CONFIG` value and a start directory, in that
order, and `src/main.rs` calls it with `find_config_upward` deleted. Decide
the walk: the API's (every ancestor) or the umbrella's (stop at the first
`.git` ancestor), and write why; the API's present behaviour is the default
unless the stop is clearly better. Say what an explicit path or a variable
naming a file that does not exist does (an error naming it, not a silent fall
through to the walk, unless the API does otherwise today and something relies
on it). Tests cover each step of the order, an empty variable, and a start
directory with no config above it, without racing other tests over the process
environment (follow what the crate already does for env tests).

`embarch doctor` and `embarch status` move onto the function, gain
`--config` and honour the variable in `tasks/umbrella/128`; the ui moves in
`tasks/ui/132`. Both wait on this.

**Not yours:** every other repo. You never touch hardware.

## Where to look

- `src/main.rs` (`find_config_upward`, and where `--config` and
  `EMBARCH_API_CONFIG` are read)
- `crates/embarch-core-client/src/token_discovery.rs`, `src/lib.rs`
- `embarch-umbrella/src/config.rs` `find_config_path`, `src/init.rs`
  `find_repo_root`; `embarch-ui/src/firmware_build.rs` (read only)

## Where the doc goes

**`decisions/client-crate.md` is in reserve: 11,832 of 12,288 B, filed under
`tasks/api/222`.** Do not grow it. Put the new decision in a new topic file
with an index row. `decisions/lease.md` (decision 90) and
`decisions/test-plans.md` (134) are already over their per-decision limit; do
not touch them.

## Done when

- [x] One public function in `embarch-core-client` returns the config path
      from an explicit path, the variable and a start directory; the API calls
      it and `find_config_upward` is gone; tests cover every step.
- [x] A new api decision records the order, the walk chosen and why, what a
      missing named file does, and that the umbrella and the ui follow.
- [x] Gate green (`cargo build`, `cargo test`, `cargo clippy --all-targets --
      -D warnings` at the workspace root); `changelog.d/` fragment.
