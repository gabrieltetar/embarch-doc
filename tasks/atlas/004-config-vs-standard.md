# 004 — Check firmware configuration against a standard's requirements

**State:** blocked
**Unparks when:** `tasks/atlas/016` lands the `standard` kind this task's `requirement` records belong to
**Source:** field use on a USB PD charger board, 2026-09-09 to 2026-10-20 — 564 spec lookups outside the atlas came within three calls of a devicetree or Kconfig read by the same agent, and the engineer's curation notes list about 50 commit-message corrections from the review rounds, about half of them a USB PD rule restated wrongly (a timer value, a Required or Recommended level, which PDOs a power rule allows at a given PDP)
**Scope:** atlas
**Hardware:** none
**Owner:** no

## What

The join already checks the schematic, the devicetree and the datasheets against each other and reports candidates in `mismatch_report`. Extend it to a standard's requirements that a configuration value can break. A `requirement` record of a standard (or a `check` record that names one) may carry `fw_check`: inputs named by devicetree path and property (from `dt.json`, for example a `usb-c-connector` node's `source-pdos` and `sink-pdos`) or by Kconfig symbol (from `kconfig.json`), an `applies_when` guard (for example `CONFIG_USBC_CSM_DRP=y`), and an expression evaluated with the existing `check` evaluator (`embarch-atlas/src/embarch_atlas/check.py:671`), extended with list access and per-standard decode helpers (USB PD: a PDO or APDO word to its type, voltage and current). Values the standard's rules depend on but the firmware does not state (a port's Port Maximum PDP, which DT node is which port) are declared by the engineer in `atlas.toml` and marked engineer-declared. Each failed check is a mismatch candidate of a new class, `config-vs-standard`, that cites the requirement's page and the file:line that set the value (`dt_node` and `config` already resolve those). The first USB PD rules to encode, as a worked example in the procedure: fixed PDO voltages and currents against the power-rules table for the declared PDP, PPS and AVS APDO ranges against theirs, the first Source_Capabilities' 5 V current against the Rp current, and a role chosen in Kconfig against the sequences the applicability records make Normative for that role (atlas-protocol-records).

## Why now

In the field this cross-check ran by hand in every review round, and the errors it missed were found by the next round instead. The atlas already holds both sides, the build's `dt.json` and `kconfig.json` and the spec's requirement records, and joins neither to the other.

## Done when

- [ ] Schema: `fw_check` (inputs, `applies_when`, expression) on `requirement` and `check` records; DESIGN.md updated.
- [ ] `atlas.toml` takes engineer-declared values per standard (ports, PDP), validated at join.
- [ ] Join evaluates every `fw_check` against the pinned build, and against a named build when `mismatch_report` is given one; `checks.md` shows ran and passed per rule.
- [ ] A failed check appears in `mismatch_report` as `config-vs-standard` with both cites and what would settle it.
- [ ] Synthetic tests: a fixture devicetree whose PDO set breaks an invented power rule and one that passes; a guard that skips the rule when its Kconfig symbol is off.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped.

## Blocked

Parked by the supervisor on 2026-10-29, not by a worker: the `requirement` records of a standard this checks against come from the `standard` kind `tasks/atlas/016` lands, and that task waits on the owner's review. Back to `open` when 016 is done.
