# 023 — Atlas decodes `core-state` PCs into symbols against the board's ELF

**State:** done
**Source:** core/103 (decision 97): `/live/core-state` returns raw `pc_samples` and `registers.pc`/`lr`; resolving them against the ELF the board runs (the `live_stacks` flash check) was deliberately left out of Core. Filed from `inbox/atlas-core-state-symbol-decode.md` by the 2026-10-26 08:09 leg, in core/103's fold.
**Scope:** atlas
**Hardware:** none — testable against a stub Core and a fixture ELF.
**Owner:** no

## What

The atlas's live module calls Core's `POST /live/core-state`, resolves each PC sample, `PC` and `LR` to function and line using the ELF that the `live_stacks` flash check has confirmed the board runs, and decodes `scb_icsr` and `dhcsr` bits by name. When done, "where is it hung" comes back as symbols, with the sample histogram.

## Why now

Raw PCs still need a manual `addr2line`; the 2026-10-14 hunt ended on six raw `DWT_PCSR` words read by hand.

## Done when

- [x] PC samples resolve to symbols, refusing (by name) when the ELF is not the one flashed.
- [x] `ICSR`/`DHCSR` decoded by field name.
- [x] Gate green, and `check_public.py` clean. (`check_public.py` does not exist in embarch-atlas; read as `test_public_guard` running, plus `check-client-names.py --repo`, both clean.)

## Done

`live core-state` (CLI) and `core_state` (MCP, listed only when Core answers) in `embarch-atlas/src/embarch_atlas/corestate.py`; contract in the repo's `DESIGN.md` (Live section and the verb table).

- Core's side is read through `embarch-api core-state --json`, not the HTTP route directly, as the rest of `live.py` does.
- The flash check is `live.image_check` (the `live_stacks` one). It is one halted `mem-read`, taken *after* the state so the sample is undisturbed, and skipped when no address needs naming. A mismatch, missing ELF or other chip prints "Refused to name symbols: ..." with the reason; addresses and the bit names stay.
- ELF reading: `nm` (existing `footprint.image`) plus `addr2line` beside it when the toolchain has one (exact line); otherwise the symbol's definition line, marked. No new dependency.
- LR is resolved as the call (`LR-2`); an `EXC_RETURN` LR is named, not resolved.

## Debts

- **Hardware-verification debt:** never run against a real board or Core. To verify on the DUT bench: `embarch-atlas live core-state` and `--halt`, with the flashed build's dir, against a deployed Core with `/live/core-state` (core/103), and confirm (a) `addr2line` is found beside the build's `nm` (it is derived by name from `CMAKE_NM`, tested only with a fake), (b) a deliberately different build is refused. DWT_PCSR sample addresses are assumed to carry no Thumb bit and are masked with `~1` either way.
