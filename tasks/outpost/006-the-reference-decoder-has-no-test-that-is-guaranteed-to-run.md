# Give the outpost decoder a test entry point that runs without west or a Zephyr checkout

**State:** done, agent/outpost/006-decoder-unit-test, 2026-09-06
**Source:** owner's repo survey, 2026-09-06 — `tests/cross_decoder.py:10-18`'s own argument, applied to itself
**Scope:** outpost
**Hardware:** none
**Owner:** no

## What

`tests/run-all.sh:8-9` hard-fails on unset `WEST`/`ZEPHYR_BASE` before any check runs, so three of
its four legs need a Zephyr toolchain. The fourth, `tests/cross_decoder.py:57-62`, returns 0 when the
sibling fixtures are absent. Net: `scripts/decode_outpost.py` — the reference implementation of a
wire format with "three implementations that must agree" (`interfaces/wire.md`) — has **no test
guaranteed to execute**.

Add `tests/decoder_unit.py` (stdlib `unittest`, no pytest dependency) that synthesizes bytes and
asserts the parsing rules that already have scar tissue in comments: COBS round-trip and the
`0xFF`-run case; a bad CRC costing exactly one frame while still consuming a `frame_index`
(`decode_outpost.py:114-127`); a truncated batch counting `bad_body`; an unknown kind rendering as
`unknown_N`; the wrap-vs-gap rule at `:224-230` (a small backwards step from a gap record must
**not** unwrap); and `us` formatting as three fixed decimals (`:262-268`). `run-all.sh` runs it
first, before the west guard, so the host half is always exercised.

**This one verifies itself** — the whole point is that it needs no west, no `ZEPHYR_BASE` and no
siblings.

## Why now

`tests/cross_decoder.py:10-18` argues that a check nobody is forced to run is not a check. The same
argument applies to a decoder whose only two tests need Zephyr or two sibling repos.

## Done when

- [x] `python3 tests/decoder_unit.py` passes from a bare checkout with no west, no `ZEPHYR_BASE`,
      no siblings. 20 tests, run under `env -u WEST -u ZEPHYR_BASE`.
- [x] Reverting the wrap rule at `decode_outpost.py:224-230` to a naive `cycles < last` makes it
      fail (checked, then restored). Two failures, and both show the historical bug verbatim: a
      10-cycle backwards step from a gap record rendered `4990` as `4294972286`, and every record
      after it shifted by 2**32 as well. `test_a_real_wrap_does_unwrap` still passed under the
      break, which is why the gap direction had to be asserted separately.
- [x] Changing `f"{…:.3f}"` to `round(…, 3)` makes it fail (checked, then restored). Four tests,
      seven failures counting subtests: `AssertionError: 1234.0 is not an instance of <class
      'str'>` and `AssertionError: 333333.333 != '333333.333'` — a float against the string every
      other implementation of this column emits.
- [x] `run-all.sh` runs it before the `WEST` guard and still runs the other three legs unchanged.
      Proven by running it with `WEST`/`ZEPHYR_BASE` unset: 20 tests pass, then the guard fires
      (`line 18: WEST: set WEST to a west executable`, exit 1). The diff touches only the header
      comment and the block inserted above the guard.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `spec.md` and `interfaces/wire.md` updated, `changelog.d/` and `features.d/` fragments
      dropped. No `status.d/`: nothing suite-level became false — `embarch.md` §3's outpost row is
      about real-silicon end-to-end and the roadmap's milestone text is unaffected.

## What was and was not done

**No `decisions.md` entry, and no numbered decision.** The rationale is
argument, not a new invariant, and it now lives in `interfaces/wire.md`'s test
section beside the cross-decoder argument it extends. A numbered decision would
have needed a new mission file for one entry.

**`open.md` untouched** — it named nothing about the decoder being untested, so
nothing there closed.

**The three west-gated legs of `run-all.sh` were not executed**: there is no
`west` and no `ZEPHYR_BASE` on this machine. They were confirmed unchanged by
reading the diff, not by running them.
