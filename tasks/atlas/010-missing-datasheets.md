# 010 — Record the engineer's answers to missing.md, with generic cards for jellybean parts

**State:** claimed by agent/atlas/010-missing-datasheets, 2026-10-29 17:32
**Source:** field use on a USB PD charger board, 2026-09-09 to 2026-10-20 — 27 part numbers on the boards have no document; 133 of 170 `net_trace` answers named at least one part whose pin roles are unknown, and the walk from the board's two main rails stops at a MOSFET or a buck with no datasheet; sessions fetched missing datasheets from vendor sites instead
**Scope:** atlas
**Hardware:** none
**Owner:** no

## What

`missing.md` already asks the right question per part ("Supply it, mark it not needed, or accept a standard-function card?", `embarch-atlas/src/embarch_atlas/missing.py:284`), but nothing records the answer: `inventory/answers.toml` is listed in DESIGN.md:62 and under "Not yet built (deliberately)" (DESIGN.md:520-523). Build it. Per MPN the engineer answers `supplied`, `not-needed` (with why) or `standard-function = "<function>"` with a pin map from the part's pin names to the function's pins. A standard-function card is a small built-in template per function (n-channel MOSFET, p-channel MOSFET, diode, Schottky, TVS, thermistor, inverter, AND, NAND, buffer with output enable, 1-of-2 decoder), giving each pin a role and a `flow` the way a datasheet pin record does; its records carry `prov=engineer-declared` and never a limit or a timing. `net_trace` walks through such a part (an enable through an inverter, a feed through a FET) and marks the hop "generic card, engineer-declared"; `missing.md` shows answered questions as answered and orders the open ones by how many `net_trace` walks stop at the part (`nettrace.py:365` already lists them under "Datasheets needed"), next to the firmware visibility it ranks by today. In the field about two thirds of the 27 part numbers are logic gates, MOSFETs, diodes and protection parts that a generic card covers; the rest (a buck, an LDO, a load switch, a comparator, an LED driver) still need their datasheets, and the ranking says which first.

## Why now

The power-feed walk that landed on 2026-10-06 (45a1ed0) is only as long as the documented parts allow, and most of its answers in the field ended at a part with no pin roles. The answers file is the cheapest way to extend it without guessing pin roles from netlist names, which the 2026-10-06 decision ruled out.

## Done when

- [ ] `inventory/answers.toml` schema, and `embarch-atlas missing --answer <MPN> supplied | not-needed --why <text> | standard-function <fn> --pins <map>`; `missing.md` shows answered items as answered.
- [ ] Generic cards for the functions above, each with pin roles and `flow`; a card is used only for an MPN the engineer answered.
- [ ] `net_trace` walks through a standard-function part and marks the hop; a synthetic two-board fixture shows a rail's feed found through a generic FET and an enable through a generic inverter.
- [ ] `missing.md` orders open firmware-visible questions by walks stopped, with the count shown.
- [ ] DESIGN.md moves `answers.toml` out of "Not yet built".
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped.
