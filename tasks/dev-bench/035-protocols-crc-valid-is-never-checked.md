# 035 — `protocols_crc_valid` is computed and never checked

**State:** open
**Source:** `embarch-study-designer/interfaces/seals.md:26` — every seal is checked independently at both hops
**Scope:** dev-bench
**Hardware:** bench
**Owner:** no

## What

`app/src/main.c:1349-1376` gates a `StudyStart` on `steps_crc_valid` and
`streams_crc_valid` and walks past the third. A study whose `protocols` span was
corrupted in flight is executed, which is a hand-written C interpreter running a
state machine that is not the one the host sealed — exactly the class
`embarch-study-designer` decision 58 gives as the reason a `ProtocolDef` is
sealed when a `StructLayout` is not.

When this is done, all three seals gate at that hop, and a mismatch names which
one, the way the other two already do.

## Why now

**It has only just become observable.** Until `suite/045` (2026-09-17) nothing
in the suite produced a non-zero `protocols_crc`: `embarch-api`'s `reseal_study`
skipped it until 2026-08-27 (`embarch-decision-reversals.md` row 76) and
`embarch-ui`'s `seal_crc` skipped it until now. With a correct third seal
arriving on the wire, the missing check is a real gap rather than a check on a
field that was always zero on both sides.

Named as out of scope by the plan that closed the authoring gap, rather than
folded into it: this is firmware, in another repo, and the fix is a ztest and
three lines of C.

## Done when

- [ ] `dbm_decode_frame`/the `StudyStart` handler refuses a `protocols_crc`
      mismatch, naming the seal.
- [ ] A ztest covers a study with a deliberately wrong `protocols_crc`, beside
      the two that already cover the other seals.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `changelog.d/` fragment; `embarch-dev-bench/decisions/protocols.md` notes
      the third gate if it says anything about the other two.
