# 112 — `embarch-core` probes.md, spec.md and open.md are in reserve after decision 89

**State:** done — verbatim split: chip mapping (8/34, 80, 89) to decisions/chip-mapping.md; spec §4 module table to interfaces/modules.md
**Source:** `core/111` added decision 89 and crossed the reserve line on three files; `DOC-COMPACTION.md` §2
**Scope:** core
**Hardware:** none
**Owner:** no

**Compacts:** embarch-core/decisions/probes.md, embarch-core/spec.md
**Size debt due:** 2026-11-09
**In flux:** no — for a verbatim split. Decision 89 (the requested-chip gate) is still unverified against a moved probe and its chip-spelling assumption may still force a change in Core, so its *text* is in flux; a split moves it word for word and restates nothing, so that flux does not forbid one (`DOC-BUDGET.md`, split first). No squeeze of decision 89 or of anything it touches.
**Must not delete:** decision 89's "assumed, not measured" spelling paragraph and the `409 chip-mismatch` refusal wording; decision 80's ARMv6 RCC reasoning; decision 22's identity-gate relation.

## What

`probes.md` 11,263/12,288 B, `spec.md` 9,225/10,240 B, `open.md` 4,262/5,120 B.

## 2026-10-29 note

`open.md` was compacted by `core/124` to 3,918 B, out of reserve, and is removed from `Compacts:`; its `Must not delete:` items were untouched.

## Why now

`check-doc-size.py` fails on a file in reserve with no task naming it; this is that filing.

## 2026-11-09 unpark note

**Unparked on its due date** by the leg that began at `fa94400b`, which had a free slot no other scope could fill (the queue held `atlas`, `chat` and `desk` only). Due today, overdue tomorrow; paying it now spares the first leg after midnight its first unit.

**Split, do not squeeze.** `decisions/probes.md` has two missions and a seam between them: "Probe selection and board identity" (9, 22, 23, 26, 61) and "Chip mapping" (8/34, 80, 89). Moving the second verbatim into its own topic file under `decisions/` clears the file. `spec.md` needs about 750 B out (reserve line 9,039 B); find a seam the same way, as `core/030` did for §5's constants, and move it verbatim. Check inbound links to every moved heading first, update `decisions.md`'s index, and if the gate prints a pin `NOTE:`, report it rather than editing `scripts/`. Leave `open.md` alone.

## Done when

- [x] Each file is clear of its reserve line, or a successor confirms `In flux: no` and compacts.
- [x] Every `Must not delete:` item is still readable.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
