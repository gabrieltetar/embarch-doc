# 002 — Write the specified-but-missing mocked HTTP test suite

**State:** claimed by agent/api/002-mocked-http-tests, 2026-09-02 21:39
**Source:** [embarch-api/open.md](../../embarch-api/open.md) — "The mocked unit-test suite is specified and unwritten. The acceptance criteria are recorded ... and no test files exist."
**Scope:** api
**Hardware:** none

## What

`embarch-api/tests/` holds two JSON fixtures and **zero `.rs` files** (verified
2026-09-03; the 59 `#[test]` in `src/` are inline unit tests and are not this).
Write the suite `open.md` already specifies, against a mock HTTP server rather
than a live Core.

The acceptance criteria are already recorded and are the task — do not invent
new ones:

- bearer token injection on every outbound call
- per-endpoint timeout independence
- plain-text body surfaced on a non-2xx response
- the two-pipe drain invariant (a child writing heavily to one of stdout/stderr
  while barely touching the other must not hang)
- truncation on a UTF-8 character boundary, never mid-codepoint
- an untouched pre-existing artifact **not** counted as fresh

## Why now

Entirely host-side, fully verifiable without a board, and it closes a gap the
doc has been carrying rather than adding a new surface. The two-pipe invariant
in particular is a real hang this crate already fixed once and nothing guards.

## Done when

- [ ] `embarch-api/tests/` contains real `.rs` tests covering all six criteria.
- [ ] Each test fails if its invariant is broken — check by breaking it locally.
- [ ] Gate green: `cargo build`, `cargo test`, `cargo clippy --all-targets -- -D warnings`.
- [ ] `embarch-api/open.md` updated — the bullet moves from "specified and
      unwritten" to whatever is now true; if the smoke harness is still
      unwritten, say so rather than deleting the bullet.
- [ ] `changelog.d/api-<slug>.added.md` dropped; `status.d/` fragment only if a
      suite-level fact changed.
