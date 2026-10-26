# 123 — Make `embarch-api signal-exchange` fail loudly when no reply came back

**State:** claimed by agent/api/123-signal-exchange-cli-silent-on-no-reply, 2026-10-26 00:58
**Reserve, for the worker (2026-10-26):** no `embarch-api` doc is in reserve. `core/098` (Core's
exchange answer gains wire fields) runs in parallel this leg and is not on `main`; build against
the `ExchangeResponse` `embarch-core-client` has today and do not add its future fields.
**Source:** field use on a USB PD charger board, 2026-09-09 to 2026-10-20 — 146 Bash calls ran `signal-exchange` (206 invocations in loops); 109 discarded stderr, 109 gave no `--until`, 65 stripped escape codes with `sed`, 7 used `--json`
**Scope:** api
**Hardware:** none
**Owner:** no

## What

The CLI is what test scripts call; the MCP tool already returns the whole JSON. In human mode `signal-exchange` prints `resp.text` and nothing else (`embarch-api/src/cli.rs:1208-1226`): `until_seen` and `truncated` are dropped and the exit code is 0 whether the reply was complete, cut at the deadline, or empty. When done: with `--until`, a reply that never showed it exits with a distinct non-zero code and one stderr line ("no `<until>` within N ms: M bytes read, echo seen/not seen"); zero bytes back exits with its own code; `truncated` likewise. A `--clean` flag gives what the atlas `shell` gives (escape codes out, the echo and the closing prompt dropped), so scripts stop carrying their own `sed` filter. The exit codes are listed in `--help` and in the api's interface docs.

## Why now

Most field scripts (109 of 146 calls) wrapped the call as `signal-exchange ... 2>/dev/null | sed ...`, so an empty reply and a command with no output were the same empty string to the script. The sessions' own notes say "console exchanges sometimes come back empty (unexplained)"; the 10 such replies seen through MCP had five different causes (see `core-exchange-says-what-happened-on-the-wire`), and the CLI ones were never counted because nothing marked them.

## Done when

- [x] A CLI test against the mock Core reproduces: `until` not seen with bytes, zero bytes, `truncated`; each exits with its documented code and stderr line, and a complete reply still exits 0 with stdout unchanged.
- [x] `--clean` output matches the atlas `clean()` on the same fixtures (echo found, echo missing, prompt at the end, cursor-move escapes).
- [x] `--json` output is unchanged apart from any new Core fields passed through.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped.

## Done

Exit codes 3 (until not seen), 4 (zero bytes), 5 (truncated) in `src/cli.rs`; `--clean` is a Rust port of the atlas `live.clean()` (same five fixtures, checked against the Python output). Tests: `tests/signal_exchange_cli.rs` (mock Core) and a unit test in `cli.rs`. Under `--json` the stdout is unchanged and the exit code and stderr line still apply. No `embarch-core-client` change. Doc: decision 82 amended, `interfaces/tools-topology.md`, `interfaces/tools.md`. `--clean` takes the prompt from `--until` (the atlas reads it from project config); with no `--until` no prompt is dropped. No new `features.d` row (no capability changed maturity).
