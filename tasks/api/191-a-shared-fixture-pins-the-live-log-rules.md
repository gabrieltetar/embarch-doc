# 191 — A shared fixture pins the live-log rules both writers follow

**State:** open
**Source:** EMB-319 — the atlas live-log writer keeps a verb list the api output already answers
**Issue:** EMB-319
**Scope:** api
**Hardware:** none
**Owner:** no

## What

Two processes write `<repo>/embarch/live/<date>-<session>.jsonl`:
`embarch-api` (`src/live_log.rs`) and `embarch-atlas`
(`src/embarch_atlas/livelog.py`). They share five rules that
`embarch-doc/embarch-api/interfaces/live-log.md` states and nothing tests
across both: the 4096-byte answer cap (cut on a character boundary, the full
answer's length and SHA-256 kept), the `embarch-live/1` schema, the
board-resolution order (a gated call's body, then the tool's arguments, then
the answer), the path rule (the nearest directory up to the git root holding
`embarch/`, else the project's `source_path`, else no line) and the
`<date>-<session>` file name (sliced from the lease's `started_at` text with no
zone conversion, the holder's non-alphanumerics turned to `-`; `<today>-no-lease`
with no lease).

When this is done, `embarch-api/tests/fixtures/live-log/` holds cases that pin
those five rules as data: each case's inputs (the gated calls with their
bodies, statuses and call-log headers, the tool's arguments, the answer text,
the lease, the directory layout) and its expected outputs (the file's path
relative to the case's root, and every contract field of the line except the
ones that differ by writer or by clock: `t`, `writer`, `via`, `sent`). A Rust
test feeds every case through `live_log.rs`'s own code and fails on any
difference; where that code is not yet callable without a live Core or a
clock, split out the pure part (taking `now` as an argument) rather than
copying it into the test. Cover at least: an answer over 4096 bytes with a
multi-byte character at the cut; each step of the board order; a `repeat`
entry; a repo found by walking up, and the `source_path` fallback; a lease
holder with characters to replace, and no lease.

`interfaces/live-log.md` gains a short section saying the fixture exists, what
a case holds, which fields are compared and why the four are not, and that a
second writer's test reads the same files from a sibling checkout. The fixture
is the contract's executable copy, so the doc names it as the place a rule
change has to land first.

## Why now

EMB-319 asks for a test that fails when the two writers disagree. This is its
first half; `atlas/108` reads these files from the atlas and deletes the
atlas's own verb list, and is parked until this lands. Keep the case format
plain JSON a Python test can read without help.

**Burndown leg: no new numbered decision.** The live log has no decision of its
own (the interface says so); record the fixture there.

## Done when

- [ ] `tests/fixtures/live-log/` covers the five rules, and a Rust test runs
      every case through `live_log.rs` and fails on a difference.
- [ ] `interfaces/live-log.md` describes the fixture and the compared fields.
- [ ] Gate green (`../../embarch-fleet/gate.md`), `changelog.d/` fragment
      dropped.
