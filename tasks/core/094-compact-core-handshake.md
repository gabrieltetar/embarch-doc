# 094 — `embarch-core/decisions/handshake.md` is at its cap

**State:** done
**Dispatch note (supervisor, 2026-09-28):** this file is **one of three that turn `main`'s
`check-doc-size.py` RED** — over its cap and past its 2026-09-25 clock — so the unit is judged
first on whether that red is gone. The other two reds (`embarch-ui/open.md`,
`embarch-ui/decisions/shell.md`) are not yours and will still show in your gate run; report them as
pre-existing, not as your failure. Other `core` files in reserve that this unit must **not** touch:
`interfaces/studies.md` (259 B left, `tasks/core/092`), `decisions/surfaces.md` (`091`, blocked),
`decisions/auth.md` (`046`, blocked), `decisions/streams.md` (`093`, blocked). `decisions.md`'s
index row and Size cell for the new file and for `handshake.md` are yours.
**Source:** `scripts/check-doc-size.py`'s reserve floor, crossed by decision 74
**Scope:** core
**Hardware:** none
**Owner:** no
**Compacts:** embarch-core/decisions/handshake.md
**Size debt due:** 2026-09-25
**In flux:** no

## What

The handshake decision group is **12,643 / 12,288 B, 355 B over**, on this
task's clock. Out of reserve when this closes, or the task says why not.

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

## No longer in flux

**Decision 74 met a board on 2026-09-19 and did not move.** Three reads on a
real nff_dev@7 returned the header in 171-258 ms with `after_reset=false`, so
the 3 s listen budget and the reset fallback are both confirmed as written and
neither number is expected to change. The entry is stable; the split is now
ordinary compaction work.

## Done when

- [x] Out of reserve, or the task says why not. **Out of reserve**:
      `check-doc-size.py --pressure` reports `PAID 71.8% embarch-core/decisions/handshake.md
      is out of reserve; close its item`.
- [x] **Nothing about why the reset is conditional survives only in prose that
      was cut.** Moved verbatim — `diff` against the pre-split section shows the
      only removed byte is the file-separator `---` line that sat between
      decisions 56 and 74 in the old file, not decision 74 itself. The
      `HEADER_INTERVAL_MS=0` case, the fatal input-buffer clear and the
      lock-held-across-the-listen argument are all still there, word for word.
- [x] `decisions.md`'s index row and its size column updated. Split the
      `handshake.md` row (now 31, 35, 47, 56 / 8.6 KB) and added a row for
      `decisions/outpost-preflight.md` (74 / 4.5 KB).
- [ ] Every inbound reference to 74 still resolves (`check-decision-refs.py`).
      **Not fully** — one reference is broken by this split and it is not
      `core`'s to fix: `embarch-ui/decisions/firmware-build.md:7` links
      `[embarch-core decision 74](../../embarch-core/decisions/handshake.md)`,
      which now names the wrong file. Filed to
      `/home/gabriel/Github/embarch/embarch-doc/inbox/ui-repoint-firmware-build-decision-74-link.md`
      per `DOC-CONVENTIONS.md`'s own fix (link `embarch-core/decisions.md`, the
      routing table, instead of a topic file). No other inbound reference to 74
      is link-shaped; the rest are bare `(decision 74)` prose that resolves
      against the sub-project regardless of which topic file holds the entry.
- [x] Byte numbers before and after. `decisions/handshake.md`: 12,643 B → 8,819 B
      (cap 12,288 B, was 355 B over). New `decisions/outpost-preflight.md`:
      4,621 B (cap 12,288 B).
- [~] Gate green (`../../embarch-fleet/protocol.md` §10), `changelog.d/`
      fragment added (`core-outpost-preflight-split.changed.md`). Gate is
      **not** all-green: `check-doc-size.py` still shows the two pre-existing
      `embarch-ui` reds named in the dispatch note (`open.md`, `decisions/shell.md`)
      — not this unit's, unchanged by it. `check-decision-refs.py` shows the one
      new `embarch-ui` reference above, filed to inbox rather than fixed here
      (out of `core`'s ownership). Every other one of the 11 gate scripts is
      `PASS`.
