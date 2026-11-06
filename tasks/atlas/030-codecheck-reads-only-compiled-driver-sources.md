# 030 — `codecheck` reads only the driver sources the build compiled

**State:** open
**Source:** a worker's finding, filed to Fleet Ready
**Issue:** EMB-51
**Scope:** atlas
**Hardware:** none — `gather_files` and `classify` take a source tree and a compile database, both of which a test can write.
**Owner:** no

## What

`codecheck` (`src/embarch_atlas/codecheck.py`) compares register constants from every C file in a driver's directory, not only the files the build compiled, against the one part the devicetree node resolves to. `gather_files` seeds from `src.listdir(_dirname(f))` beside each driver translation unit, plus quoted includes, and `analyze` calls `gather_files(src, u.drivers)`. On a board using the Zephyr BQ2518x charger driver, 71 of 89 mismatch candidates were `reg-address-unknown` entries from other chargers' drivers in the same directory (bq24190, bq25713, pf1550, max20335, pca9422, sbs), none compiled into the build, each compared against the BQ25188 register map. The real candidates were buried.

When this is done, the sources are limited to the translation units in `compile_commands.json` plus the headers they include (or the driver file named by the node's compatible), and constants that are plainly not register addresses (`*_UA`, `*_UV`, `*_MV`, `*_MAX_*`, `*_STEP_*`) are skipped by `classify`. The module docstring's "The driver's directory is scanned: every `.c`/`.h` in it" says the new rule.

## Why now

A candidate list that is 80% noise teaches the reader to skip it, which is the failure a mismatch report exists to prevent.

## Done when

- [ ] Constants from a driver file that is not in `compile_commands.json` and not included by a compiled file are not compared (unit test with a two-driver directory and a one-entry compile database).
- [ ] A header the compiled driver includes is still read.
- [ ] A `*_UA`, `*_UV`, `*_MV`, `*_MAX_*` or `*_STEP_*` constant is not reported as a register address.
- [ ] The module docstring and any design doc that states the scan rule say the new one.
- [ ] Gate green (`../../../embarch-fleet/gate.md`, the Python bullet).
- [ ] `changelog.d/` fragment dropped.
