# 029 — `embarch-outpost/decisions/transport.md` and `decisions/manifest.md` are in reserve

**State:** done
**Source:** `outpost/027` added decisions 28 and 29 and left transport.md at 7,908 of 8,192 B and manifest.md at 7,350 of 8,192 B.
**Scope:** outpost
**Hardware:** none
**Owner:** no

**Compacts:** embarch-outpost/decisions/transport.md, embarch-outpost/decisions/manifest.md
**Size debt due:** 2026-11-26
**In flux:** no, for the verbatim split this task now asks for. Layout 4 will amend decisions 5, 9 and 20, and `open.md` says that change is deliberately not made yet, so a squeeze would restate what is about to change. A split by mission moves those entries whole and restates nothing (`DOC-BUDGET.md`, "a split is the default remedy"), so that objection does not apply to it.
**Must not delete:** decision 9's selection/verification split and decision 28's measured-on-native_sim-only note.

## Update (supervisor, 2026-11-10)

Unparked as a split, not a squeeze. The park waited on layout 4, which has no date: `open.md` says it is deliberately not made yet. `DOC-BUDGET.md` makes a split the default remedy because it restates nothing, and `check-doc-size.py --pressure` asks each park to be re-read against that rule. **Reword nothing.** Move whole decisions, add a one-line pointer where they left, and split the index row in `decisions.md`.

Seams worth checking first (your call; check inbound links before cutting, and run `scripts/check-duplication.py outpost`):

- `decisions/transport.md` (3, 5, 20, 28; 7,908 B, out of reserve at <= 6,991 B): the overflow policy, 5 and 28, is one mission apart from the ring and the drain loop. `spec.md` line 79 cites `decisions/transport.md` for the knobs, so keep that link true.
- `decisions/manifest.md` (9, 24, 29; 7,350 B, out of reserve at <= 6,991 B): 24, the operator's override of both post-hoc refusals, is one mission apart from what the manifest is and how its build ID is cut. Decision 9 is 4,581 B on its own, near the per-decision line, so it stays whole where it is.

## What

Split the two decision files by mission, verbatim, so both leave reserve.

## Why now

`check-doc-size.py` fails on a file in reserve with no debt filed; `outpost/027` spent the reserve.

## Done when

- [x] Both files are clear of reserve, or a successor re-files with a concrete plan.
- [x] Removed lines match added lines apart from headers, pointer lines and index rows.
- [x] Every `Must not delete:` item is still readable.
- [x] Can `spec.md` alone answer what someone needs to work on this component today? Answered in the commit message.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).

## Shipped

Verbatim split by mission. Decisions 5 and 28 moved to `decisions/overflow.md` (transport.md 7,908 -> 5,402 B), decision 24 to `decisions/override.md` (manifest.md 7,350 -> 5,666 B); both leave reserve. One-line pointers stay where each left, the index row is split in `decisions.md`, and the one inbound link to 24 (`decisions/clocks.md`) now points at `override.md`. Other inbound links (spec.md line 79 -> decision 20, wire.md and open.md -> decision 9, glossary) still land on a decision that did not move. No code comment cites a moved decision by file (`grep` over `embarch-outpost`, read-only). `check-duplication.py outpost` clean beforehand.

How the verbatim claim was checked: `git diff -U0` shows removed lines match the moved bodies; `comm -13` of the sorted unique lines of the old files against the two new files leaves only the new file headers, intro and index lines. The only edits to moved-adjacent text are the pointer lines, the "decision 24" sentence at the end of decision 9 (now links `override.md`) and the link in clocks.md. Must-not-delete items intact: decision 9 whole in manifest.md; decision 28's measured-on-native_sim-only note in overflow.md.

spec.md question: it answers current behaviour and how to work on the component; why a rule holds is in decisions/, reached by the index.
