# 030 — `embarch-core/spec.md` is 108 bytes into its reserve

**State:** done — leg 062, 2026-09-09
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

- [x] `spec.md` is clear of the 90%-of-cap reserve line, with no constant's
      value, `[measured]`/`[assumed]` tag, or measurement note lost.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).

## What actually happened

Split, not squeeze — `DOC-BUDGET.md`'s "a reference table is not cold — it
moves to `interfaces/`" line fits §5 exactly, and `interfaces.md` already has
the precedent (its own routes table split into `interfaces/<topic>.md` groups
in `tasks/core/020`). §5's whole 12-row constants table plus the paths
paragraph moved **verbatim** to the new `embarch-core/interfaces/constants.md`
(an `interface-group`, 12 KB cap, now 1.8 KB) and `spec.md` §5 became a
four-line pointer. Nothing was cut, squeezed, or reworded — no quoting of
removals is needed because nothing was deleted, only relocated with its link
left behind. `interfaces.md`'s routing table got one added row pointing at the
new file, for discoverability.

`spec.md`: 9,148 B -> 7,977 B (77.9% of its 10 KB cap, clear of the 9,216 B
reserve line). `interfaces/constants.md`: 1,848 B (well under its 12 KB cap).

Did not touch §2's `hw_lock`/decision 14 provenance narrative the task
description flagged as a secondary candidate — the split alone cleared the
reserve with room to spare, so no further cut was needed, and every fact in
§2 stays hot per `DOC-COMPACTION-PASS.md`'s "why" test (it is a constraint
reason, not just evidence).

**Can `embarch-core/spec.md` alone answer what someone needs to work on this
component today?** Yes, and the split does not change that answer either way:
everything that was hot before is still in `spec.md` word-for-word — the
invariants, the module table, the deployment notes, decision pointers. The
constants table was always closer to reference material than to "what must
not be violated" (most rows are bare `[assumed]` with no rule attached to
them); a reader who needs a value follows one link, same as they already do
for the HTTP route tables, interfaces, decisions, and open questions. Nothing
that changes a correctness judgement moved out of reach.

Code worktree: zero diff, docs-only change. `cargo build`/`test`/`clippy` not
run — nothing to build. `check-docs.py`: 10 of 11 PASS; the one RED
(`check-links.py` on `tasks/doc/033-...md` -> `../DOC-CONVENTIONS.md`) predates
this unit and is untouched by this diff. `check-doc-size.py` alone: PASS
(was the only RED-adjacent check before this unit; confirmed clean after).
`check-ownership.py --scope core` and `--code-repo`: both OK.
`check-client-names.py --repo <doc worktree>`: PASS.
