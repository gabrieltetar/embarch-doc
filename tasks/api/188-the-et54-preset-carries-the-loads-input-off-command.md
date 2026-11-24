# 188 — The et54 preset carries the load's input-off command

**State:** blocked — no source on disk gives the ET54's input-off command
**Unparks when:** the owner records the ET54-series load's input-off command, as its programming manual gives it, in this file or on EMB-334; and `tasks/api/187` has landed
**Source:** EMB-334's second half, split out at the split (2026-11-24)
**Issue:** EMB-334
**Scope:** api
**Hardware:** verify-only
**Owner:** no

## What

The `et54` preset (`src/instrument.rs`, `PRESETS`, `preset`) fills an ET54-series
load's measured line facts. Once the tools carry a safe-off (`api/187`), the
preset should also fill the load's input-off command, marked "unverified on the
bench" in the tool doc until the owner's bench session checks it.

## Blocked

At the split, nothing in `embarch-api`, `embarch-doc` or the private notes
gives the command (searched for the preset name, the model and the SCPI input
verbs). The issue asks for the command "taken from the instrument's programming
manual"; writing it from memory would state an instrument fact nobody measured
or read, so this waits for the owner to supply it.

## Done when

- [ ] The `et54` preset fills `safe_off` with the recorded command, and an
      explicit `safe_off` still wins.
- [ ] `interfaces/tools-instruments.md` says the preset's line is unverified on
      the bench.
- [ ] A hardware-verification debt is left for the line on the real load.
- [ ] Gate green (`../../embarch-fleet/gate.md`); `changelog.d/` fragment
      dropped.
