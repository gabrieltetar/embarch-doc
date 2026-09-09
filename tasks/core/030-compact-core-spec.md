# 030 — `embarch-core/spec.md` is 108 bytes into its reserve

**State:** open
**Source:** `tasks/core/009` added the `/serial-log` duration/byte-cap row to §5's
constants table, pushing `spec.md` from 9,019 B to 9,148 B against a 10,240 B
cap — 89.3%, into the `max(1,200 B, 10%)` reserve band (`DOC-BUDGET.md`).
**Scope:** core
**Hardware:** none
**Owner:** no

**Compacts:** embarch-core/spec.md
**Size debt due:** 2026-09-23
**In flux:** no — nothing else is currently queued against this file.
**Must not delete:** nothing named yet; the next unit to touch this file
should read it whole before cutting anything (`DOC-COMPACTION-PASS.md`).

## What

`spec.md`'s §5 constants table has grown row by row for a while (12 rows) and
is the most likely place to squeeze: several rows restate "[assumed]" with no
further content, and §2's invariants list has at least one bullet
(`hw_lock`/decision 14 queueing) that carries more measurement narrative than
a *what is true now* doc needs — that reasoning belongs in `decisions.md`,
which already has it. A short pass moving provenance detail out of §2 and
tightening §5's driest rows should clear the reserve without cutting any
constant's value or its `[measured]`/`[assumed]` tag.

## Why now

`check-doc-size.py` fails the gate on a file in reserve with no task naming
it (`DOC-COMPACTION.md` §2). `tasks/core/009` is the unit that spent it, by
adding a genuinely new pair of constants rather than by bloating an existing
row, so the fix here is compaction of what already exists, not reversal of
`009`.

## Done when

- [ ] `spec.md` is clear of the 90%-of-cap reserve line, with no constant's
      value, `[measured]`/`[assumed]` tag, or measurement note lost.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
