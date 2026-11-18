# 079 — Worst-case RC threshold-crossing time from board parts and facts

**State:** done
**Source:** Fleet Ready issue: a firmware session wrote inline Python to work out the worst-case time for an RC node to cross a gate's input threshold, from component tolerances and the supply's accuracy, when the atlas already holds most of the inputs.
**Issue:** EMB-195
**Scope:** atlas
**Hardware:** none
**Owner:** no

## What

An `embarch-atlas` verb, for example `rc_timing <board:node>` (CLI and MCP), that reports the minimum and maximum time for one board node to cross the receiving gate's input threshold, charging from 0 V or discharging from the rail, from `tau * ln(V / (V - Vth))` taken at each worst-case corner. It joins what the atlas already has and no verb joins today:

- the series resistance and the capacitance on the node, from the board's netlist and parts (`parts` already returns value and tolerance per reference);
- the capacitor's temperature characteristic where its description carries one;
- the supply rail's accuracy, from the regulator's datasheet fact;
- the receiving pin's guaranteed VIH or VIL at that supply, from the receiving part's datasheet fact.

Every input in the answer is cited to its record, or named as **assumed** with why — for example a tolerance read from a part number because no datasheet or schematic parameter carries it. The result is `(derived)` and names its formula. No margin is added unless the caller passes one, and a margin passed is printed beside the result.

## Why now

The owner moved the issue to Fleet Ready. The atlas's `parts` lookup already says it exists so that "a worst-case divider or filter calculation" has each part's tolerance; this is that calculation, done once and cited, instead of re-derived per session.

## Dispatch notes

- **Handle the simple network only, and say so when it is not.** A node that is not one series R into one C to a reference (or a C to ground behind one R) is reported as not handled, naming the parts found on it, rather than approximated. A missing threshold or regulator fact is a named gap, never a typical value.
- Use the existing tolerance fields (`bomvals.py`) and fact records; do not add a second tolerance parser.
- `embarch-atlas` keeps no numbered decisions; record the verb in its `DESIGN.md`/`README.md` and `embarch-doc/embarch-atlas/` as the recent `q` verbs were.
- An MCP tool changes the lookup counts: update every count and the test that pins the tool count, as `atlas/075` did.
- Tests use a synthetic board, netlist and facts, never a client document. Include one hand-computed case checked to three significant figures. The public-name guard (`test_public_guard`) must run, not skip: the supervisor links `.atlas-local` beside the worktree.
- No file of this sub-project is in reserve.

## Done when

- [x] The atlas answers a worst-case RC crossing time range for a node, with each input cited or named as assumed.
- [x] A node that is not a single R and C, or that lacks a threshold or regulator fact, gets an answer naming what is missing or unsupported.
- [x] A test reproduces a hand-computed case to three significant figures.
- [x] Gate green (`../../embarch-fleet/gate.md`, the Python bullet); docs updated, `changelog.d/` fragment dropped.

## Outcome

`q rc_timing` / MCP `rc_timing` shipped (lookups 21 to 22). Handles charging (R to a rail, C to ground) and discharging (R to ground, `rail=` names the supply). Inputs: `bom.json` tolerances via `bomvals`, rail range from the regulator's VOUT `limit` record (min/max, or nominal with an accuracy record), VIH `min` / VIL `max` from the receiving part. Assumed and labelled: caller-passed `r_tol`/`c_tol`, and the EIA temperature class table (C0G/NP0, X7R, X5R, X7S, X6S, X7T, Y5V, Z5U). No feature-inventory row: `features.d` has no atlas section.
