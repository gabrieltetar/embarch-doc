# 083 — `embarch-study-designer` GATT decisions and types.md are in reserve after decision 89

**State:** done
**Source:** `study-designer/082` added decision 89 to `decisions/gatt.md` and a sentence to `interfaces/types.md`; `DOC-COMPACTION.md` §2
**Scope:** study-designer
**Hardware:** none
**Owner:** no

**Compacts:** embarch-study-designer/decisions/gatt.md, embarch-study-designer/interfaces/types.md
**Size debt due:** 2026-11-24
**In flux:** no — the monitor-window rules (decisions 36, 53, 89) are settled; the only open piece is Core calling the new check, which changes neither file.
**Must not delete:** in `gatt.md`, decision 53's note that the target-carrying actions are the first with a sequence and the pinned wire vector that proves the C decoder walks them, and decision 83's "measured, not assumed" line; in `types.md`, the dev-bench decision 54/55 pointers on the monitor rows.

## What

`gatt.md` 12,048/12,288 B and `types.md` 11,154/12,288 B.

## Why now

`check-doc-size.py` fails on a file in reserve with no task naming it; this is that filing.

## Done when

- [x] `scripts/check-doc-size.py --pressure` shows both files `PAID` or not at all.
- [x] Every `Must not delete:` item is still readable.
- [x] Can `spec.md` alone answer what someone needs to work on this component today? Answered in the commit message.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).

## Outcome

- `gatt.md` 12,048 -> 10,012 B: decision 41 moved verbatim (11 lines out, 11 in) to `decisions/vendor-identities.md` (2,386 B incl. header); pointer line left; `decisions.md` index row split. Decisions 53 and 83 untouched.
- `types.md` 11,154 -> 10,950 B: trimmed the `BleAddress` dated history and the `Uuid` derive detail. Dev-bench 54/55 pointers untouched.
- Human question: yes for orientation. `spec.md` (8.1 KB) states what the crate is, its invariants, the feature/target split, result storage, the three consumers and where the constants live, each with a pointer to the owning doc. What it lacks is current work: that is in `open.md`.
