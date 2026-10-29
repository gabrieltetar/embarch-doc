# 025 — The clock-gate word never tips a `reg_read` into refusal, and matches only an enable register

**State:** claimed by agent/atlas/025-clock-gate-word-never-tips-a-read-into-refusal, 2026-10-29 17:48
**Source:** `atlas/013`'s review (2026-10-29 fold of `atlas/013`, code `0f68b0a`): two residuals the reviewer named and judged minor, filed rather than left in the log
**Scope:** atlas
**Hardware:** none — both halves are planning and lookup logic over SVD records, testable with the fixture SVDs and the fake `mem-read` `tests/test_live.py` already uses.
**Owner:** no

## What

`atlas/013` made `reg_read` add the RCC register holding a peripheral's `<PERIPH>EN` bit to the same halted read (`live.py`, `clock_gate` and the `extra` list before `plan`). Two edges it left:

- **The extra word counts against the read's limits.** `ranges = plan(to_read + extra, skip)` is checked against `MAX_RANGES` (32) and `MAX_WORDS` (256) after the gate register is added, so a peripheral that needed exactly the limit before now answers "spans N words in M ranges ... Ask for its registers by name" where it used to read. The clock word is a diagnostic, not the thing asked for: when adding it would cross a limit, read the peripheral without it and say the clock state is unknown because the read had no room, rather than refusing the read.
- **`<PERIPH>EN` is matched against every RCC register's fields**, lowest address first, not only the clock-enable registers. On the one vendor SVD `atlas/013` measured, the only collision was `RTCEN` in the backup-domain control register (handled by the exceptions table); on another family a same-named field in a non-enable register would be picked up and its value reported as the clock state. Restrict the match to the registers an SVD marks as peripheral clock enables (by name pattern `*ENR*` excluding the sleep-mode `*SMENR*`, or by the register description, whichever the fixture SVDs support), and keep the exceptions table for what that cannot reach.

## Why now

Both are cheap while `atlas/013` is fresh, and the second is the one that would report a wrong clock state as measured on a part nobody has checked yet.

## Done when

- [ ] A fixture peripheral that fills `MAX_RANGES` (or `MAX_WORDS`) exactly still reads, and its answer says the clock state is unknown because the read had no room for the enable word.
- [ ] A fixture SVD with a `<PERIPH>EN`-named field in a non-enable RCC register does not report it as the clock state.
- [ ] The opt-in `EMBARCH_ATLAS_REAL_SVD` test still passes against the vendor SVD `atlas/013` used (`/home/gabriel/STMicroelectronics/STM32Cube/STM32CubeProgrammer/SVD/`, read-only; never name the part in the repo).
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `DESIGN.md` "Live" clock-gate bullet updated, `changelog.d/` fragment dropped.
