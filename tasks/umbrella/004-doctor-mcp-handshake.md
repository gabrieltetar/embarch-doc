# 004 — Check 10 tests that a registration exists, which is the one thing decision 23 says is not enough

**State:** done, 2026-09-04 — agent/umbrella/004-doctor-mcp-handshake
**Source:** embarch-umbrella/002 (design-only decisions audit, 2026-09-03) — decision 23 read against the source and found unbuilt
**Scope:** umbrella
**Hardware:** none

**Doc-size reserve at dispatch (supervisor, leg 009):** `embarch-umbrella/spec.md`
is **in reserve — 9761/10240 B, 479 B of headroom**, already filed against
`tasks/umbrella/009-compact-docs.md` (which is `blocked`, `In flux: yes`). Plan
your `spec.md` edit against those 479 B: this task's `Done when` requires a check
10 row update and a decision 23 implementation note, so prefer *replacing* text in
the existing row over adding a paragraph. `embarch-umbrella/open.md` is out of
reserve (88.5%). Because 009 already carries the debt for `spec.md`, you do **not**
owe a new `tasks/doc/<NNN>-compact-umbrella.md` for it — but if any *other*
`embarch-umbrella` file enters reserve on your commit, file one.

## What

`embarch-umbrella` decision 23 says check 10 spawns the registered MCP command
with a short timeout, sends a minimal `initialize`, and reports success, failure
and timeout distinctly. **It does not.** `check_mcp` in `src/doctor.rs` runs
`claude mcp get embarch` and returns Pass on a zero exit. Nothing in the crate
spawns the registered command; the only handshake in `doctor` is the dev-bench
serial one checks 11 and 13 share.

Build what decision 23 describes: spawn the exact registered command, one
round-trip JSON-RPC `initialize` over stdio, short timeout, and three distinct
outcomes. A full MCP client is explicitly not needed.

## Why now

The check's stated reason for existing is to catch **registered but broken**, and
that is precisely the state it currently reports as Pass. `open.md` also records
that MCP registration has never been verified for real — which is a second,
smaller gap sitting on top of this one.

## Done when

- [x] Check 10 spawns the registered command and completes (or fails, or times
      out) an `initialize`, with the three outcomes distinguishable in `--json`.
- [x] A registered-but-unstartable command reads Fail, not Pass — covered by a test.
- [x] `spec.md`'s check 10 row and decision 23's implementation note updated to
      say it shipped.
- [x] The feature-inventory rows — written directly as `features.d/` fragments, **not** a
      `status.d/` request: `suite/features.md` is assembled now, and
      `features.d/umbrella-*` is this worker's to write. The whole-chain row
      (`umbrella-060`) drops check 10 from its unbuilt list, and a new
      `umbrella-065` row covers the check itself.
- [x] Gate green; `changelog.d/` fragment dropped.

## What shipped

`src/doctor.rs`. `check_mcp` splits into three testable pieces: `mcp_registration`
(runs `claude mcp get embarch` and parses the command line out of it),
`mcp_initialize` (spawns it, writes one JSON-RPC `initialize`, reads a matching
response, 10 s budget, kills the child either way), and `judge_mcp` (the verdict).
`Check` gains a `code` field, rendered into `--json` for every check as
`null`-or-string, so the three handshake outcomes are distinguishable without
matching on `detail` — that is new **decision 37**, and decision 23 is now marked
built.

Six unit tests: the parse, the quoted-argument split, the verdict mapping, the
`--json` codes, and a real-spawn test that fabricates six shell-script servers —
answering, exiting-broken, absent, hanging, wrong-id, JSON-RPC-error — and
asserts they land on Answered / Failed / TimedOut correctly. `cargo test`: 121
passed.

## Verification debt (not hardware)

**Nothing in this suite has ever seen `claude mcp get`'s output**, so the format
`parse_registered_command` reads is assumed, not measured. That is why an output
it cannot parse is a `Warn` with code `unreadable-entry` rather than either a
pass or a fail — a wrong guess must not be able to invent a verdict about the
server. It needs **one `embarch doctor` run from an environment with the agent
CLI installed and `embarch` registered** (no board, no Core, no probe involved);
`open.md` carries it. `claude` is not on `PATH` in a worker's environment, which
is why this could not be settled here.

The 10 s handshake budget is likewise assumed rather than measured against a real
`embarch-api` cold start; the timeout is reported under its own code so a wrong
budget shows up as itself.

## Gate: one RED, and it is structural, not this change

`scripts/check-docs.py` is **7 of 8 green, `build_features.py --check` RED.**
That red is not fixable from a worker branch. Adding a `features.d/` row makes
`suite/features.md` stale by construction, and `check-ownership.py --scope
umbrella` refuses `suite/features.md` for every worker scope — so the two halves
of the gate ask for opposite things. Assembling it and committing it fails the
ownership check; not assembling it fails `check-docs.py`. This branch chose the
second: a boundary violation is worse than a mechanical red.

**To land it: run `scripts/build_features.py` as part of the fold**, which
consumes `umbrella-060` (edited) and `umbrella-065` (new) and turns the check
green. Everything else is green — see below.

Dropped in `inbox/doc-features-gate-conflicts-with-ownership.md`, because it
will hit every worker that ships a feature and is `scripts/`-owner work.

## Gate result

- `cargo build`, `cargo test` (121 passed), `cargo clippy --all-targets -- -D warnings` — green.
- `scripts/check-docs.py` — 7 of 8; `build_features.py --check` red, above.
- `scripts/check-ownership.py --scope umbrella` (doc) and `--code-repo` (code) — green.
- No native Windows build: this is not `embarch-core`.
