# 004 — Check 10 tests that a registration exists, which is the one thing decision 23 says is not enough

**State:** claimed by agent/umbrella/004-doctor-mcp-handshake, 2026-09-04 22:58
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

- [ ] Check 10 spawns the registered command and completes (or fails, or times
      out) an `initialize`, with the three outcomes distinguishable in `--json`.
- [ ] A registered-but-unstartable command reads Fail, not Pass — covered by a test.
- [ ] `spec.md`'s check 10 row and decision 23's implementation note updated to
      say it shipped.
- [ ] `status.d/` fragment for `suite/features.md`'s `embarch doctor` row.
- [ ] Gate green; `changelog.d/` fragment dropped.
