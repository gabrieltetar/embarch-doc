# 135 — `serial_log` tells its caller when Core cut the capture short, and config.md stops calling `flash_format` optional for `zephyr-west`

**State:** claimed by agent/api/135-serial-log-reports-truncation-and-config-md-requires-flash-format, 2026-10-26 05:14
**Source:** DeepSeek V4 Pro suite review 2026-10-25 (cross-repo findings 1 and 7), verified by Opus against embarch-api@6d664853 and embarch-core@40a58ccb
**Scope:** api
**Hardware:** none — the change is the client struct, the CLI and the MCP tool, all tested against the mock Core, plus one doc cell.
**Owner:** no

## Dispatch note, 2026-10-26 05:14 leg

**Doc reserve in your scope:** `embarch-api/decisions/client-crate.md` is 11,581 / 12,288 B (707 B left), filed under `tasks/api/140` (open). Decision 58 already states the parse rule this task applies, so this should need no new decision there; if you do need one, put it in another topic file (`failure-reporting.md` or a new one listed in `decisions.md`), not `client-crate.md`. Nothing else in `embarch-api/` is in reserve; `interfaces/config.md` (9.8 K of 12 K) and `interfaces/tools-build-flash.md` have room.

**Shared crate.** `embarch-core-client` is path-depended on by `embarch-ui`. Keep the `SerialLogResponse` change additive (`Option<bool>`, `#[serde(default)]`), so `embarch-ui` builds unchanged; say in your Result whether `embarch-ui` reads this struct anywhere.

**Isolation, not optional.** Tests and any CLI or MCP run go against the crate's mock Core on a port your test owns. Never run the `embarch-api` binary with the owner's config or its default `auto` base-url discovery (that finds the live Core at the WSL2 gateway), never call the `mcp__embarch-api__*` or desk tools, never touch the desk on :4891, real serial ports or probes, and never read or write the owner's data dirs (`~/.config/embarch*`, `~/.local/share/embarch*`). The last two legs each had a worker reach something live; do not be the third.

## What

1. **`serial_log` drops Core's `truncated` flag.** Core's `GET /serial-log` answers `{port, lines, truncated}` and sets `truncated: true` when the byte cap (`EMBARCH_SERIAL_LOG_MAX_BYTES`, default 1 MiB) cut the capture short. `embarch-core-client`'s `SerialLogResponse` has only `port` and `lines`, so serde throws the flag away. Neither the CLI nor the MCP tool can tell a caller that it is reading a prefix. A capture of a chatty console therefore reaches an agent as complete when it is not. Direction: add the field following decision 58's rule for anything an older Core may not send, which means `Option<bool>` with `#[serde(default)]`. Then carry it through. The MCP tool's JSON should carry `truncated`, and its description should say what `true` means. The CLI's `--json` output should carry it too. The CLI's human output should mark a truncated capture the same way `study-streams` already does (`src/cli.rs:1723`, `[TRUNCATED — this capture is short]`). If an older Core returns `None`, say in words that this Core did not report the flag. Never show it as `false`.
2. **`interfaces/config.md` says `flash_format` is required only for `static`.** The field table marks it "yes (static)". `ProjectConfig.flash_format` is a bare `String` with no default, so a `zephyr-west` project that leaves it out fails config load with a missing-field error. `config.example.toml`'s `zephyr-west` example sets it, and `embarch-umbrella`'s mirror requires it on purpose. The doc is the side that is wrong. Change the cell to say it is required for every project.

## Why now

- Core side: `embarch-core` `src/api.rs:820-828` (the response struct and its doc comment) and `:858-862` (where it is set). `embarch-core/interfaces/hardware.md`'s `/serial-log` row says `truncated: true` exists so the caller is not "silently getting a partial capture".
- Client side: `crates/embarch-core-client/src/client.rs:830-834` (no field), `src/cli.rs:1302-1314` and `src/tools.rs:1521-1525` (both emit only `port` and `lines`).
- The parse rule is `decisions/client-crate.md` 58. `tasks/core/040` recorded Core's half and did not reach the client.
- Finding 7: `interfaces/config.md:42` against `crates/embarch-firmware-build/src/config.rs:153`. `config.example.toml:97` and `embarch-umbrella` `src/config.rs:7-11` (at `1e521166`) agree with the code.

## Done when

- [ ] Against the mock Core, a `/serial-log` body with `truncated: true` reaches the MCP tool's JSON as `truncated: true`, and the CLI's human output carries a visible truncation marker. A test covers each.
- [ ] A body with no `truncated` key still parses, and both surfaces report that this Core did not say, rather than `false` (decision 58's shape, with a test named for it).
- [ ] The CLI's `--json` output carries the field.
- [ ] The `serial_log` row in `interfaces/tools-build-flash.md` and the tool's own description say what `truncated` means.
- [ ] `interfaces/config.md`'s `flash_format` row says it is required for every project.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped.
