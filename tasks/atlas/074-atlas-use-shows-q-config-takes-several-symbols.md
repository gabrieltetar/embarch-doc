# 074 — The atlas-use skill and `MAP.md` show that `q config` takes several symbols

**State:** done
**Source:** Fleet Ready issue: a session read ten Kconfig symbols by parsing an atlas's `kconfig.json` with a throwaway script, because the skill shows `config` with one symbol.
**Issue:** EMB-186
**Scope:** atlas
**Hardware:** none
**Owner:** no

## What

`embarch-atlas q config` already accepts several symbol names, space- or comma-separated, and `*` patterns, and `--vs pinned` lists differences against the pinned build. Nothing a session reads first says so: the atlas-use skill's quick-lookup table lists `config <SYMBOL>`, one symbol, and the tools line of the generated `MAP.md` does the same. Make both show the multi-symbol form and a pattern example, so a session needing a handful of symbols (a driver's enable, the PM symbols, the tick rate) makes one call instead of reaching for `kconfig.json`. No new verb.

Confirm the behaviour against the code and its tests before you write it down: if `q config` does not accept one of the forms the issue names, document what it does accept and say so in this file.

## Why now

The owner moved the issue to Fleet Ready.

## Dispatch notes

- Burndown: no new numbered decision (`embarch-atlas` keeps none anyway).
- Any place that quotes the `config` row or the `MAP.md` tools line (the skill, `mapgen.py`, `README.md`, `DESIGN.md`, `embarch-doc/embarch-atlas/`) should agree with the new wording; a test that pins the tools line text moves with it.

## Done when

- [x] The atlas-use skill's quick-lookup row for Kconfig shows `config <SYM> [<SYM> ...]` and a `*` pattern example, and names `--vs pinned` if the row has room.
- [x] The tools line of a generated `MAP.md` names the multi-symbol form.
- [x] Gate green (`../../embarch-fleet/gate.md`, the Python bullet), `changelog.d/` fragment dropped.

Confirmed against `buildq.names_of`, the `q config` argparse (`symbol` is `nargs="*"`) and `tests/test_buildq.py`: `q config A B USB_*` and `q config A,B,USB_*` both work, `*` `?` `[` patterns work, `--vs pinned` lists differences. All forms in the issue are accepted. The skill row already showed `symbols=[A, B, USB_*]`; it now leads with the multi-symbol form. No test pinned the MAP.md tools line.
