# 013 — Make `reg_read` say when a peripheral's clock is off instead of decoding zeros as "at reset"

**State:** claimed by agent/atlas/013-reg-read-says-when-the-clock-is-off, 2026-10-29 17:22
**Source:** field use on a USB PD charger board, 2026-09-09 to 2026-10-20 — 3 times a session read the RCC enable register by hand next to a peripheral read (`VREFBUF` with `RCC.APBENR2`, `SYSCFG.CFGR1` after `RCC.APBENR2`, raw `mem_read` of `RCC_APBENR1`/`AHBENR`) to know whether the peripheral's words meant anything
**Scope:** atlas
**Hardware:** verify-only
**Owner:** no

## What

On STM32 a peripheral whose RCC enable bit is clear does not give back its register contents; the debug read is still acknowledged, and what comes back (usually 0) is not the register. `reg_read` (`embarch-atlas/src/embarch_atlas/live.py:354-410`) decodes those zeros like any value, and for a whole peripheral prints "(N fields at reset)", which reads as "configured at reset values" rather than "not readable now". When done, `reg_read PERIPH[.REG]` adds the RCC register that holds the peripheral's enable bit to the same halted snapshot (the SVD has the fields: `RCC.APBENR1.UCPD1EN`, `RCC.APBENR2.SYSCFGEN`, `RCC.IOPENR.GPIOAEN`, `RCC.AHBENR.DMA1EN`, found by the `<PERIPH>EN` name, with a small table for the exceptions such as `VREFBUF` on `SYSCFGEN`). When the bit is 0 the answer says "clock off (`RCC.APBENR1.UCPD2EN` = 0): these words are not the register's contents" and does not mark fields as at or off reset. When no enable bit is found, the answer says the clock state is unknown.

## Why now

It costs one extra word in a read that already halts the core, and today the only guard is the caller remembering to check RCC; the sessions did it by hand around 3 of the 23 MCU register reads, and nothing marked the other 20 as checked.

## Done when

- [ ] Unit test with a fake `mem-read` answer: `UCPD2` with `UCPD2EN` = 0 reports "clock off" and no reset markers; with `UCPD2EN` = 1 it decodes as today.
- [ ] Every SVD peripheral of the atlas's MCU either maps to an enable field or is listed as unknown, checked by a test over the SVD records (blocks with no enable bit of their own, such as `RCC`, `EXTI` and `IWDG`, are listed on purpose).
- [ ] Bench check on a peripheral the image leaves off (for example `TIM1` when `RCC.APBENR2.TIM1EN` is 0): the answer says "clock off".
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `DESIGN.md` "Live" updated, `changelog.d/` fragment dropped.
