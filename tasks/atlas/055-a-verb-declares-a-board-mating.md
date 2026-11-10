# 055 — A verb records an engineer-declared board-to-board mating

**State:** claimed by agent/atlas/055-a-verb-declares-a-board-mating, 2026-11-10 02:10
**Source:** Linear issue EMB-26, filed by a session
**Issue:** EMB-26
**Scope:** atlas
**Hardware:** none
**Owner:** no

## What

When the engineer answers which connectors mate, the only way to record it is to hand-edit `boards/system.json`. `embarch-atlas interfaces` only proposes: it scores each connector pair under four rules (`identity`, `mirror`, `row-swap`, `column-reverse`) and writes the proposals under `proposed`. An engineer's answer goes under `interfaces`, or in a `proposed` entry whose `prov` is `engineer-declared` or `engineer-confirmed`, and `run` never overwrites those.

Add a CLI verb that writes an engineer-declared board-to-board entry — `a` and `b` (`<board>:<connector ref>`, e.g. `A:J2`), `kind` `board-to-board`, either a `rule` or a `pin_map` (contact on a to contact on b), `prov`, and an optional `note` — without disturbing any other entry, and have the two skills that ask the mating question name the verb instead of describing a file edit.

## Why now

A hand edit of JSON is error-prone and leaves no trace of who declared what, and two skills ask the engineer this exact question.

## Where to look

- `src/embarch_atlas/interfaces.py` `run` and the CLI registration — the verb and what `run` keeps
- `src/embarch_atlas/interfaces.py` `interface_pairs`, `mated_pairs`, `ENGINEER_PROV` — how entries are read
- `skills/atlas-translate-docs/SKILL.md` step 4 and `skills/atlas-update/SKILL.md` step 3 — the steps that ask the engineer
- `tests/test_interfaces.py` — the fixture shape for a declared entry (`prov: engineer-declared`)

## Dispatch notes

- Burndown is on: no new numbered decision. The atlas has none anyway; describe the verb where `DESIGN.md` describes `interfaces` and `boards/system.json`, in place.
- Whether the verb also promotes an existing proposal by its id (writing `engineer-confirmed`) is yours to decide; the Done when needs only the declare path. Say which you did.
- The verb must refuse a ref that is not a connector on that board's netlist, and a `rule` that is not one of the four, rather than write an entry `interface_pairs` cannot read.
- The worktree needs `.atlas-local` linked beside it and a `.venv` of its own (both made for you); `test_public_guard` must run, not skip.
- No file in `embarch-doc/embarch-atlas/` is in doc-size reserve.

## Done when

- [ ] A verb writes an engineer-declared board-to-board entry (rule or pin map, with a note) into `boards/system.json` without disturbing other entries, with a test.
- [ ] `embarch-atlas interfaces` run afterwards keeps it and scores it as it does a hand-written one.
- [ ] The two skills name the verb instead of describing a file edit.
- [ ] Gate green (`../../embarch-fleet/gate.md`, the Python bullet); `changelog.d/` fragment dropped.
