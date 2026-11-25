# 045 — The compaction test stops racing, and a failed one stops holding the run

**State:** open
**Source:** EMB-556 — a compaction test races under load and then holds npm test for ten minutes
**Issue:** EMB-556
**Scope:** chat
**Hardware:** none
**Owner:** no

## What

`test/wire.test.mjs`, "a model picked while a /compact waits behind a turn does
not end the hold", asserts that only `slow: a long step` and the `/compact`
have been sent when the next turn ends. On a loaded machine the held rest was
already sent by then, so the assertion fails. The test throws before
`chat.dispose()`, so the scripted CLI (`test/fake-compact.mjs`) stays alive
until the chat's `idleMs` of 600,000 ms, and the run ends only then: about
606 s against about 41 s for a green run. It has failed on the full gate run of
the last two chat units; on the most recent one it was also reported failing
when `wire.test.mjs` ran alone, so first establish whether it fails alone on
`main` today, and if it does, find what changed rather than only widening a
wait.

- **Wait on the event** that ends the running turn rather than a turn count, so
  the assertion reads the state at the moment it means.
- **Dispose every compaction test's chat in a `finally` or `t.after`**, so a
  failed assertion cannot hold the run for the idle timeout.

## Where to look

- `test/wire.test.mjs`, `test/fake-compact.mjs`
- `src/` — the compaction hold and where a held message is released
- `embarch-doc/embarch-chat/decisions/` — the compaction decisions, for what
  the hold is meant to guarantee (the test changes; the guarantee does not)

## Where the doc goes

Nothing in `decisions/` unless the hold's behaviour itself was wrong; a
changelog fragment for the test fix. No `embarch-chat` file is in reserve at
filing.

## Done when

- [ ] The test passes twenty runs in a row of `wire.test.mjs` while a parallel
      `cargo test` (any repo) loads the machine.
- [ ] A forced failure in any compaction test ends the run in under a minute.
- [ ] Gate green, the full `npm test` included.
