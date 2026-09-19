# 094 — `embarch-core/decisions/handshake.md` is at its cap

**State:** blocked
**Source:** `scripts/check-doc-size.py`'s reserve floor, crossed by decision 74
**Scope:** core
**Hardware:** none
**Owner:** no
**Compacts:** embarch-core/decisions/handshake.md
**Size debt due:** 2026-09-25
**In flux:** yes
**Blocked on:** decision 74 being validated against real hardware — one study run with `requires.outpost` set against a board with an outpost compiled in, which will either confirm the listen/reset budgets and the refusal text or change them. Unparks the moment that run lands.

## What

The handshake decision group is **12,288 / 12,288 B (100.0%), 0 B left**. Out of
reserve when this closes, or the task says why not.

The entry that crossed the floor is **74**, the outpost mode pre-flight. It was
trimmed four times on the way in to fit, and what went was phrasing rather than
substance — but at 0 B left the next correction to any entry in this file cannot
be written at all, which is a worse state than the reserve normally describes.

## Why the seam is a split, not a squeeze

This file already *is* a split — out of `studies.md` on 2026-09-06, on the
argument that "the study loop and what guards its start are two missions". It
now carries three guards, not one: the **version gate** (31), the bench's
**hardware identity** (35, 47, 56), and the **DUT's outpost mode** (74). The
third shares no mechanism with the other two — it reads a serial port and a
firmware's own header frame, where they read `HelloAck` and a JTAG probe — and
it is the newest and most likely to grow, since the listen/reset path has never
run against real hardware.

So: `decisions/outpost-preflight.md`, decision 74 moved verbatim, per
[../../DOC-BUDGET.md](../../DOC-BUDGET.md) §3.

## In flux

**Decision 74 has not met a board.** Its listen budget (3 s), its post-reset
budget (6 s) and the reset fallback itself are reasoned from
`CONFIG_EMBARCH_OUTPOST_HEADER_INTERVAL_MS`'s default and from
`embarch-outpost/interfaces/wire.md`, not measured. A bench run may change any
of the three and will want room to say so, which is an argument for doing the
split before that run rather than after.

## Done when

- [ ] Out of reserve, or the task says why not.
- [ ] **Nothing about why the reset is conditional survives only in prose that
      was cut.** The `HEADER_INTERVAL_MS=0` case, the fatal input-buffer clear
      and the lock-held-across-the-listen argument are the three a later reader
      will try to "simplify away"; each must still be findable.
- [ ] `decisions.md`'s index row and its size column updated.
- [ ] Every inbound reference to 74 still resolves (`check-decision-refs.py`).
- [ ] Byte numbers before and after.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10), `changelog.d/` fragment.
