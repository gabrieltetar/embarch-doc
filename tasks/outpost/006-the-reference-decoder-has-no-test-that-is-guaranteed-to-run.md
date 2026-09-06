# Give the outpost decoder a test entry point that runs without west or a Zephyr checkout

**State:** open
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

- [ ] `python3 tests/decoder_unit.py` passes from a bare checkout with no west, no `ZEPHYR_BASE`,
      no siblings.
- [ ] Reverting the wrap rule at `decode_outpost.py:224-230` to a naive `cycles < last` makes it
      fail (checked, then restored).
- [ ] Changing `f"{…:.3f}"` to `round(…, 3)` makes it fail (checked, then restored).
- [ ] `run-all.sh` runs it before the `WEST` guard and still runs the other three legs unchanged.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false.
