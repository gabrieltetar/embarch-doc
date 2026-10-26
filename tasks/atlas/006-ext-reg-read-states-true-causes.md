# 006 — Make an external `reg_read` state the true cause: a missing I2C shell is not a NACK, another register's flag is not this one's

**State:** open
**Source:** field use on a USB PD charger board, 2026-09-09 to 2026-10-20 — 29 builds in 20 sessions carried an extra conf only to get `CONFIG_I2C_SHELL` and friends into the image; 1 config register refused and then reported as "cleared by the read" when nothing was cleared
**Scope:** atlas
**Hardware:** none
**Owner:** no

## What

Two answers of `ext_reg_read` (`embarch-atlas/src/embarch_atlas/live.py:656-724`) name a cause that is not the one that happened.

- **Image prerequisite.** External reads run `i2c read_byte` / `i2c read` on the board's shell, which exists only with `CONFIG_I2C_SHELL`. Without it the shell answers `i2c: command not found`; `_parse_read` (`live.py:617-625`) raises with that line, and the handler (`live.py:707-711`) appends the device's `device list` state and "Nothing answered at 0x.. on i2c@...", so the answer reads as an I2C NACK from a device the board lists as ready. When done, the first external read on a `Console` checks once that the `i2c` command exists (one exchange, cached for the call), and a missing one answers "the image on the board has no I2C shell: build it with `CONFIG_I2C_SHELL=y`", with nothing about the bus. "Nothing answered" is kept for the shell's own `Failed to read from device` line.
- **Read-to-clear attribution.** `READ_CLEARS_TEXT` (`live.py:50-52`) matches "until read" anywhere in a field's text, and `_ext_effects` (`live.py:592-611`) charges the match to the field that carries the text. BQ25730 `ChargeOption0.EN_CMP_LATCH` is a read-write config bit whose description says another register's flag (`STAT_COMP`, REG0x22) stays set "until read by host" (bq25730 datasheet p47). The guard refused `ChargeOption0`, and with `allow_clear=true` the answer said "this read cleared: EN_CMP_LATCH", which is false. When done, a clear-on-read sentence that names another register or field (`REG0x22`, `STAT_COMP`) is charged to that one, and the guard's reason quotes the sentence it matched.

## Why now

The prerequisite is paid as a build option every time (29 builds carried it, with the GPIO and sensor shells), and a session that forgets it would get a bus diagnosis for a firmware configuration. A false "this read cleared" teaches callers to pass `allow_clear=true` by habit, which is how the guard stops protecting the registers it exists for (a driver that reads a fault latch such as the TPS55288 `STATUS` on purpose loses the fault to a stray read).

## Done when

- [ ] Unit test: a fake console answering `i2c: command not found` gives the "no I2C shell" answer with no "Nothing answered" and no `device list` call.
- [ ] Unit test over the BQ25730 records: `ChargeOption0` is not guarded; `ProchotStatus` (which holds `STAT_COMP`) still is; `ChargerStatus`, `ChargeOption4`, INA700 `ALERT_DIAG` and TPS55288 `STATUS` keep their reasons.
- [ ] A test runs the guard over every external part in the fixture atlases and pins the list of guarded registers, so a regex change shows its effect.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `DESIGN.md` "Live" updated, `changelog.d/` fragment dropped.
