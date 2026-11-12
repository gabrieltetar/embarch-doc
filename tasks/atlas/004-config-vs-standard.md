# 004 — Check firmware configuration against a standard's requirements

**State:** done — 2026-11-11, on agent/atlas/004-config-vs-standard (code branch cut from agent/atlas/016-standard-sections; lands after it)
**Source:** field use on a USB PD charger board, 2026-09-09 to 2026-10-20 — 564 spec lookups outside the atlas came within three calls of a devicetree or Kconfig read by the same agent, and the engineer's curation notes list about 50 commit-message corrections from the review rounds, about half of them a USB PD rule restated wrongly (a timer value, a Required or Recommended level, which PDOs a power rule allows at a given PDP)
**Scope:** atlas
**Hardware:** none
**Owner:** no

## What

The join already checks the schematic, the devicetree and the datasheets against each other and reports candidates in `mismatch_report`. Extend it to a standard's requirements that a configuration value can break. A `requirement` record of a standard (or a `check` record that names one) may carry `fw_check`: inputs named by devicetree path and property (from `dt.json`, for example a `usb-c-connector` node's `source-pdos` and `sink-pdos`) or by Kconfig symbol (from `kconfig.json`), an `applies_when` guard (for example `CONFIG_USBC_CSM_DRP=y`), and an expression evaluated with the existing `check` evaluator (`embarch-atlas/src/embarch_atlas/check.py:671`), extended with list access and per-standard decode helpers (USB PD: a PDO or APDO word to its type, voltage and current). Values the standard's rules depend on but the firmware does not state (a port's Port Maximum PDP, which DT node is which port) are declared by the engineer in `atlas.toml` and marked engineer-declared. Each failed check is a mismatch candidate of a new class, `config-vs-standard`, that cites the requirement's page and the file:line that set the value (`dt_node` and `config` already resolve those). The first USB PD rules to encode, as a worked example in the procedure: fixed PDO voltages and currents against the power-rules table for the declared PDP, PPS and AVS APDO ranges against theirs, the first Source_Capabilities' 5 V current against the Rp current, and a role chosen in Kconfig against the sequences the applicability records make Normative for that role (atlas-protocol-records).

## Why now

In the field this cross-check ran by hand in every review round, and the errors it missed were found by the next round instead. The atlas already holds both sides, the build's `dt.json` and `kconfig.json` and the spec's requirement records, and joins neither to the other.

## Done when

- [x] Schema: `fw_check` (inputs, `applies_when`, expression) on `requirement` and `check` records; DESIGN.md updated.
- [x] `atlas.toml` takes engineer-declared values per standard (ports, PDP), validated at join.
- [x] Join evaluates every `fw_check` against the pinned build, and against a named build when `mismatch_report` is given one; `checks.md` shows ran and passed per rule.
- [x] A failed check appears in `mismatch_report` as `config-vs-standard` with both cites and what would settle it.
- [x] Synthetic tests: a fixture devicetree whose PDO set breaks an invented power rule and one that passes; a guard that skips the rule when its Kconfig symbol is off.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped.

## Result

Shipped on `agent/atlas/004-config-vs-standard` in embarch-atlas (cut from the 016 tip, lands after it), with this branch in embarch-doc.

- **Schema** (`schemas/record.schema.json`): `fw_check` on `requirement`; on `check` with `refs` naming the requirements it encodes, `expr`/`expect` then optional. `$defs/fw_check` (`inputs`, `applies_when`, `expr`) and `$defs/fw_input` (exactly one of `dt`+`prop` [+`decode`], `kconfig`, `declared`). Doc check X now evaluates only a check that has an `expr`.
- **Evaluator**: `check.safe_eval` takes `funcs`, `attrs`, `nodes` keyword arguments; the invariant's own surface is unchanged (a test holds it). `fwcheck.py` widens it with slices, dict literals and the USB PD decode helpers `pd_pdo` / `pd_sink_pdo` (fixed, battery, variable, PPS, EPR AVS, SPR AVS). A `CONFIG_<SYM>` name in an expression reads that symbol directly.
- **atlas.toml** `[standards."<doc_id or slug>"]` with `ports.<name>` (`node` plus values of its own), validated at join: unknown document, a port node that is not exactly one okay node, a non-scalar value, and declared keys no rule reads.
- **Join**: `mismatch.run` runs `fwcheck.run_join` on the pinned build; one checks row per rule (`config vs standard: <rid>`, ran and passed per DT node), a "Firmware configuration vs standards" section in `checks.md`, guard skips folded with the symbol's value and line, unrunnable rules under Not run. `mismatch_report build=<dir | pinned>` (q verb, MCP tool) runs the rules in memory on that build. Class `config-vs-standard` cites the requirement's doc and page, each value with the file:line that set it, the engineer-declared values, and settles by re-reading the page against the line.
- **Docs**: DESIGN.md "Firmware configuration against a standard" (under Standards and specifications), the Records rows, `atlas.toml`, Query surface, the CLI table and Not yet built; the worked example in `standard-procedure.md` (invented values; a test parses it); one paragraph in `embarch-atlas/design.md`. Atlas has no `spec.md`/`decisions.md`/`open.md`: that box is DESIGN.md plus `changelog.d/atlas-config-vs-standard.added.md`.
- **Tests**: `tests/test_fwcheck.py`, 13 tests: decode of invented words by type; the evaluator's surface; schema; a PDO set inside an invented power rule (passes) and one breaking it (candidate with both cites, checks.md row and section, `mismatch_report` line); the Kconfig guard skipping the rule when the symbol is `n` or absent and running it when `y`; per-port declared values; declaration validation; not-run reasons; a `check` record with `refs`; a named build in memory, writing nothing; the procedure's example.

Gate, 2026-11-11: `.venv/bin/pytest -q` 775 passed, 3 skipped (baseline 762 + 3; the skips are the real-workspace, real-atlas and vendor-SVD ones, `test_public_guard` ran); `check-client-names.py --repo .` clean; `check-ownership.py --scope atlas --code-repo` OK; in embarch-doc `check-docs.py` all green and `check-ownership.py --scope atlas` OK.

Choices made without the owner: a `dt` selector matches exactly (path, label, alias or chosen, compatible; no substring fallback) and only okay nodes; several matches run the rule per node, and a port's declared values come from the port whose `node` is that node, else the standard's table; a declared table is found by doc_id, else slug, so a new revision keeps it; a guard-skipped rule is folded as expected, not a check row; candidate severity is `check` for every modality (the graph shows only `check` and `info`); `CONFIG_*` names need no input; no `CONFIG_X=y` shorthand, only expressions.

Not verified: the PDO bit layout is written from the public USB PD layout as remembered, with no spec PDF in reach (no web, no client material); the tests prove the decode is self-consistent, not that it matches the spec. Check it against the standard's PDO tables once they are distilled. Not built: the numbers inside a fw_check expression are not anchored to the page, and rule 4 of the worked example (a Kconfig role against the sequences applicability records make Normative) waits for those records (tasks/atlas/011); both are in DESIGN.md Not yet built.

Follow-up filed by the owner, 2026-11-11: **EMB-159**, check the PDO/APDO decode against the standard's PDO tables once the standard is distilled in an atlas.

## Blocked (history)

Parked by the supervisor on 2026-10-29, not by a worker: the `requirement` records of a standard this checks against come from the `standard` kind `tasks/atlas/016` lands, and that task waits on the owner's review. Back to `open` when 016 is done.
