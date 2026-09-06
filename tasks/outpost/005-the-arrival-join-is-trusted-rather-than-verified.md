# Verify the arrival join against `frame_bytes` instead of trusting the row

**State:** open
**Source:** `embarch-outpost/spec.md:61` — "A join that cannot be verified stamps nothing", which the reference decoder does not implement
**Scope:** outpost
**Hardware:** none
**Owner:** no

## What

`scripts/decode_outpost.py:180-193` reads only columns 0 and 1 out of the arrival CSV and drops
`frame_bytes` on the floor; `:208` then stamps whatever the row says. `spec.md:88` says `frame_bytes`
"is what lets the post-hoc join be **verified** rather than assumed".

The decoder should compare each frame's actual delimiter-separated chunk length against the
`frame_bytes` column for that index, and on any disagreement leave `rx_utc_ms` empty for the whole
capture — an ordered, untimed trace, which is a real answer — with a loud stderr line naming the
first index that diverged. An `--allow-unverified-join` escape hatch mirrors the existing
`--allow-build-id-mismatch` posture at `:287`.

Pure Python; `tests/cross_decoder.py` runs without west.

## Why now

`spec.md:61` names a trace shifted by three frames as "readable, wrong, and indistinguishable from a
correct one". The reference decoder is the one implementation of that invariant an engineer runs by
hand, and it does not implement it.

## Done when

- [ ] A stream plus an arrival CSV whose `frame_bytes` disagrees at any index produces empty
      `rx_utc_ms` throughout, and a stderr message naming the index.
- [ ] A matching CSV stamps exactly as it does today; `tests/cross_decoder.py` still reports PASS on
      the committed fixtures.
- [ ] A missing or short `frame_bytes` column degrades to today's behaviour rather than refusing,
      and says so.
- [ ] Host-side tests cover match, mismatch, and absent-column.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false.
