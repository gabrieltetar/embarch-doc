# 023 — Atlas decodes `core-state` PCs into symbols against the board's ELF

**State:** claimed by agent/atlas/023-core-state-symbol-decode, 2026-10-29 17:15
**Source:** core/103 (decision 97): `/live/core-state` returns raw `pc_samples` and `registers.pc`/`lr`; resolving them against the ELF the board runs (the `live_stacks` flash check) was deliberately left out of Core. Filed from `inbox/atlas-core-state-symbol-decode.md` by the 2026-10-26 08:09 leg, in core/103's fold.
**Scope:** atlas
**Hardware:** none — testable against a stub Core and a fixture ELF.
**Owner:** no

## What

The atlas's live module calls Core's `POST /live/core-state`, resolves each PC sample, `PC` and `LR` to function and line using the ELF that the `live_stacks` flash check has confirmed the board runs, and decodes `scb_icsr` and `dhcsr` bits by name. When done, "where is it hung" comes back as symbols, with the sample histogram.

## Why now

Raw PCs still need a manual `addr2line`; the 2026-10-14 hunt ended on six raw `DWT_PCSR` words read by hand.

## Done when

- [ ] PC samples resolve to symbols, refusing (by name) when the ELF is not the one flashed.
- [ ] `ICSR`/`DHCSR` decoded by field name.
- [ ] Gate green, and `check_public.py` clean.
