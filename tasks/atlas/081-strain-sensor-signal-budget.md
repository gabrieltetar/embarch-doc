# 081 — Derive a strain-sensor signal budget from loads and geometry

**State:** claimed by agent/atlas/081-strain-sensor-signal-budget, 2026-11-18 04:09
**Source:** Fleet Ready issue: sessions sizing a strain or load sensor against an ADC's noise keep re-deriving section modulus, strain and bridge output with inline Python, so constants and assumptions drift between reports.
**Issue:** EMB-139
**Scope:** atlas
**Hardware:** none
**Owner:** no

## What

One `embarch-atlas` command, for example `embarch-atlas derive strain-budget <file.toml|json>`, and optionally an MCP tool, that takes a small load-and-section description and returns a table:

- **Load case:** a force with a lever arm, or a bending moment; axial force and torque where given.
- **Section:** solid round, round tube with wall thickness, rectangular flexure; a material modulus (and shear modulus for torsion).
- **Readout:** gauge factor, bridge type (quarter, half, full), excitation voltage, and ADC noise as a density with a bandwidth or as rms at a data rate.
- **Outputs:** section modulus and second moment, bending, axial and torsional strain, strain on a tube's inner wall, tip deflection, bridge output per microstrain, and the noise-limited resolvable strain and signal-to-noise ratio.

Every output value is tagged `(derived)` and names its formula, so a report can cite one source instead of ad hoc arithmetic. It reads no atlas and no document.

## Why now

The owner moved the issue to Fleet Ready, scoped to `atlas`. The atlas already marks numbers `(derived)`; this gives those numbers one formula source.

## Dispatch notes

- **Say where it sits.** The atlas's `DESIGN.md` describes a pipeline over a project's hardware documents; this helper reads none. Add it to `DESIGN.md` and `embarch-doc/embarch-atlas/design.md` as a standalone derive helper outside the build, so the doc does not read as if the pipeline grew a mechanics model.
- Units are explicit in the input and the output (SI), and an input with no unit, or a section that is not one of the three, is refused with one line naming it.
- `embarch-atlas` keeps no numbered decisions; record the command in its `DESIGN.md`/`README.md` and `embarch-doc/embarch-atlas/` as the recent verbs were.
- If an MCP tool is added, update every lookup count and the test that pins the tool count, as `atlas/075` did.
- The public-name guard (`test_public_guard`) must run, not skip: the supervisor links `.atlas-local` beside the worktree.
- No file of this sub-project is in reserve.

## Done when

- [ ] One command returns section modulus, bending, axial and torsional strain, and deflection for solid and tubular round sections and a rectangular flexure, from a load case.
- [ ] The same command returns bridge output per microstrain and the noise-limited resolution, given gauge factor, excitation and ADC noise.
- [ ] Every output value is tagged `(derived)` and names its formula.
- [ ] A test reproduces at least three hand-computed cases (solid rod, thin-wall tube, rectangular flexure) to three significant figures.
- [ ] Gate green (`../../embarch-fleet/gate.md`, the Python bullet); docs updated, `changelog.d/` fragment dropped.
