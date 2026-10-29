# 112 — `embarch-core` probes.md, spec.md and open.md are in reserve after decision 89

**State:** blocked — `In flux: yes`.
**Unparks when:** `embarch-core/open.md`'s decision-89 bullet closes (a moved-probe hardware run) or the chip-spelling question is measured.
**Source:** `core/111` added decision 89 and crossed the reserve line on three files; `DOC-COMPACTION.md` §2
**Scope:** core
**Hardware:** none
**Owner:** no

**Compacts:** embarch-core/decisions/probes.md, embarch-core/spec.md, embarch-core/open.md
**Size debt due:** 2026-11-09
**In flux:** yes — the requested-chip gate (decision 89) is new and unverified against a moved probe, and its chip-spelling assumption may still force a normalisation in Core. Blocked until `open.md`'s decision-89 bullet closes (hardware run) or the spelling question is measured.
**Must not delete:** decision 89's "assumed, not measured" spelling paragraph and the `409 chip-mismatch` refusal wording; decision 80's ARMv6 RCC reasoning; decision 22's identity-gate relation.

## What

`probes.md` 11,263/12,288 B, `spec.md` 9,225/10,240 B, `open.md` 4,262/5,120 B.

## Why now

`check-doc-size.py` fails on a file in reserve with no task naming it; this is that filing.

## Done when

- [ ] Each file is clear of its reserve line, or a successor confirms `In flux: no` and compacts.
- [ ] Every `Must not delete:` item is still readable.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
