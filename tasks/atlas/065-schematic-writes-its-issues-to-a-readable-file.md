# 065 — `atlas schematic` writes its extraction issues to a readable file

**State:** done
**Source:** EMB-179, filed by an audit while tracing an MCU control line to a FET on a rebuilt board atlas
**Issue:** EMB-179
**Scope:** atlas
**Hardware:** none
**Owner:** no

## What

`embarch-atlas schematic` ends with "N issues -> boards/<label>" but writes no
issues file: the list lives only in `boards/<label>/netlist.json`'s `issues`
array (geometry disagreements, nets joined only by a label, ports with no
partner on another sheet). A session that finds a net in `nets.md` looking wrong
has to load `netlist.json` with an inline `python3 -c` to learn whether the
extractor already flagged it, and no lookup returns these issues: `q` and the
MCP lookups cover nets, pins and checks, not the extractor's own warnings.

Make them readable straight away. The issue's direction, which you may improve
on and must say so if you do: `schematic` writes `boards/<label>/issues.md`
beside `nets.md` and `parts.md`, one issue per line naming its net, sheet and
page, prints that file's path, and `MAP.md` links each board's issues file. A
`q schematic-issues <board>` lookup is optional; if you add one, it serves the
same list.

The summary line is printed from `src/embarch_atlas/smartpdf.py` (search for
`issues`); `mapgen.py` writes `MAP.md`.

**Public repo.** Tests use synthetic fixtures only; `test_public_guard` must
run, not skip (the worktree's parent carries the `.atlas-local` link).

**What you may change.** Only `embarch-atlas` and `embarch-doc/embarch-atlas/`.

**Doc reserve.** Nothing of `embarch-atlas`'s is in reserve.

## Why now

The owner moved it to Fleet Ready; extraction issues are what explains a wrong
net, and today reading them costs a script.

## Done when

- [x] `embarch-atlas schematic` writes the board's issues to a markdown file and prints its path.
- [x] `MAP.md` links each board's issues file.
- [x] Each issue line names its net, sheet and page (or says which of the three an issue kind does not carry).
- [x] A test covers the file's content and the `MAP.md` link, over a synthetic board.
- [x] Gate green (`../../embarch-fleet/gate.md`, Python bullet).
- [x] `changelog.d/` fragment dropped; `embarch-atlas/design.md` or the code repo's `DESIGN.md` updated if the board atlas layout is described there.

## What shipped

- `schematic` writes `boards/<label>/issues.md` (also rewritten by nothing else; `declare-pin-name` leaves it alone since it does not change issues) and the summary line prints its path.
- Each line: `<board>: <kind> net=<..> sheet=<..> page=<..> | <issue text verbatim>`. Issues are plain strings in `netlist.json`, so `smartpdf.classify_issue` derives kind/net/sheet from the text by pattern; page comes from the text or the sheet's page in `netlist.json`. `-` marks what a kind does not carry (part-level kinds such as MPN disagreements, the missing-popups notice). Unmatched text is kind `other`.
- `MAP.md` boards section appends `issues: boards/<label>/issues.md` to each board line.
- Design choice vs. the issue's direction: none beyond the above; the optional `q schematic-issues` lookup was not added. `DESIGN.md` updated. Debt: MAP.md links the file even for an atlas whose board was extracted before this change until `schematic` is re-run.
