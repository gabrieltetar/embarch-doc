# 123 — Make `embarch-api signal-exchange` fail loudly when no reply came back

**State:** open
**Source:** field use on a USB PD charger board, 2026-09-09 to 2026-10-20 — 146 Bash calls ran `signal-exchange` (206 invocations in loops); 109 discarded stderr, 109 gave no `--until`, 65 stripped escape codes with `sed`, 7 used `--json`
**Scope:** api
**Hardware:** none
**Owner:** no

## What

The CLI is what test scripts call; the MCP tool already returns the whole JSON. In human mode `signal-exchange` prints `resp.text` and nothing else (`embarch-api/src/cli.rs:1208-1226`): `until_seen` and `truncated` are dropped and the exit code is 0 whether the reply was complete, cut at the deadline, or empty. When done: with `--until`, a reply that never showed it exits with a distinct non-zero code and one stderr line ("no `<until>` within N ms: M bytes read, echo seen/not seen"); zero bytes back exits with its own code; `truncated` likewise. A `--clean` flag gives what the atlas `shell` gives (escape codes out, the echo and the closing prompt dropped), so scripts stop carrying their own `sed` filter. The exit codes are listed in `--help` and in the api's interface docs.

## Why now

Most field scripts (109 of 146 calls) wrapped the call as `signal-exchange ... 2>/dev/null | sed ...`, so an empty reply and a command with no output were the same empty string to the script. The sessions' own notes say "console exchanges sometimes come back empty (unexplained)"; the 10 such replies seen through MCP had five different causes (see `core-exchange-says-what-happened-on-the-wire`), and the CLI ones were never counted because nothing marked them.

## Done when

- [ ] A CLI test against the mock Core reproduces: `until` not seen with bytes, zero bytes, `truncated`; each exits with its documented code and stderr line, and a complete reply still exits 0 with stdout unchanged.
- [ ] `--clean` output matches the atlas `clean()` on the same fixtures (echo found, echo missing, prompt at the end, cursor-move escapes).
- [ ] `--json` output is unchanged apart from any new Core fields passed through.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped.
