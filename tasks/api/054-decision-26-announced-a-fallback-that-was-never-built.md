# 054 — decision 26 announced a `serial_log` fallback that was never built

**State:** open — **the false claim itself is already gone.** I corrected decision 26's title and
first sentence in `api/041`'s fold, leg 060, 2026-09-09: the heading now reads *"never fell back
to"* and the body says *"No such fallback was ever built — verified by `api/041`, 2026-09-09."*
That was a **22-byte** edit, which is all `decisions/core-link.md` could take — it has 188 bytes
left and its compaction task `tasks/api/026` is blocked on `In flux: yes`.

**What is left for this task is the part that needs room**, and it is worth doing properly rather
than squeezed: decide whether decision 26 should be **retired** rather than corrected. Its title
still promises a mechanism as its subject while its only surviving content is the *intent*
correction (DUT-UART capture was never a supported goal), so the honest end may be a retitled
decision about intent, or a tombstone in `decisions/removed.md` with the intent correction moved
somewhere it reads as the point rather than as an aside. **Retiring a numbered decision is a design
act**; I declined to make it under burndown, at 188 bytes, unattended. Do this one after
`tasks/api/026` clears the file's reserve, or as a split.
**Source:** embarch-reviewer, review of api/041 (merge 5eeb3e8 in embarch-api;
doc merge c8373d4 in embarch-doc leg worktree)
**Scope:** api
**Hardware:** none — this is a documentation-consistency finding; confirming
it needs no board

## What

`embarch-api/decisions/core-link.md` decision 26 is titled **"`serial_log`'s
port falls back to Core's dev-bench port, and the stated intent was
corrected"** and its body opens: *"The fallback chain gained a final step
before erroring."* That is a factual claim, in an `active` decisions file,
that `serial_log` reaches for `GET /dev-bench/port` before giving up.

api/041's own landed diff says the opposite, twice, in the same leg:

- `embarch-doc/embarch-api/interfaces/tools.md` (commit c8373d4), the
  `serial_log` row, now reads: *"no further fallback exists — a `port`
  unresolved either way is a plain error naming the project, not a reach for
  `GET /dev-bench/port`"*.
- `embarch-doc/embarch-api/open.md`'s new "Owed decisions" section (same
  commit) states plainly: *"the correction to `interfaces/tools.md:28`'s
  claim of a `GET /dev-bench/port` fallback that never existed in this
  crate."*

I read `embarch-api/src/tools.rs` (`serial_log`, ~line 925) and
`src/cli.rs`'s `serial_log`: the port resolution is `port.or_else(||
project.serial_port.clone())` then a plain error — there is no
`core.dev_bench_port()` call anywhere in either front end, and
`git log --all -S"dev_bench_port" -- src/tools.rs` in `embarch-api` returns no
hits ever. The fallback decision 26 describes was never implemented in this
crate's history.

## Why this is a contradiction rather than a refinement

Decision 26 is left standing, unmodified, in this same diff/leg, and it is a
decisions file — the thing this crate's own conventions say a description or
interface doc must not depart from silently. The unit's own new prose (in
`open.md`'s owed-decision note) explicitly names the false claim and traces it
to `interfaces/tools.md`, but never to `decisions/core-link.md` #26, which
makes the identical claim as a locked decision rather than as an interface-doc
row. Nothing in this diff amends or tombstones #26, so the suite now has an
`active` decision asserting a mechanism its own interface doc and its own
owed-decision note say never existed. A future reader trusting the decisions
file over the interface table (the usual reading order) will design against a
fallback that isn't there.

## What it would take to undo

Not a revert candidate — the api/041 diff itself (embarch-api 5eeb3e8,
embarch-doc c8373d4) is correct and should stand; nothing here should be
reverted. What's missing is a follow-up edit to
`embarch-doc/embarch-api/decisions/core-link.md` #26: either a tombstone
note (in the same voice #26 already uses for its first correction) stating
the fallback mechanism itself never shipped, only the config-fallback-to-
`serial_port` step did, or a retitling that stops asserting the dev-bench-port
reach as fact. No code SHA needs reverting; the fix is doc-only, in
`embarch-doc/embarch-api/decisions/core-link.md`.
