# 016 — Land the standard document kind, and pick a standard's sections to distil from what sessions read

**State:** blocked
**Unparks when:** the owner's word — he has reviewed the uncommitted 2026-10-08 `standard` design in `/home/gabriel/Github/embarch/embarch-atlas-wt` (this task's first Done-when box), or said a worker may land it as written
**Source:** field use on a USB PD charger board, 2026-09-09 to 2026-10-20 — the USB PD R3.2 spec (418 pages) was filed as `other`, distilled by hand as a datasheet into 119 records citing 35 pages, and sessions then read 348 distinct pages of it outside the atlas; the design for a `standard` kind written on 2026-10-08 is still uncommitted in `embarch-atlas-wt`
**Scope:** atlas
**Hardware:** none
**Owner:** no

## What

The owner reviews the uncommitted 2026-10-08 work in `/home/gabriel/Github/embarch/embarch-atlas-wt` (DESIGN.md "Standards and specifications", `skills/atlas-translate-docs/reference/standard-procedure.md`, and the `atlas-translate-docs` and `atlas-use` SKILL.md changes), and the agreed version lands on main together with the code it describes: `inventory` classifies a standard (today the spec falls through to `other`, `embarch-atlas/src/embarch_atlas/inventory.py:397`), `doc sections <doc> --add <sec> --why <text>` writes `worklist.json`, a frozen section is never redone (unit key: section id, its pages' text hashes, procedure version), and `doc check` W compares a requirement's `modality` with the keyword in its quote. On top of that design, add `doc sections <doc> --suggest`: it ranks the undistilled sections by how often sessions' lookups landed in them (the usage log the find-text task writes, plus `doc_section tier=text` pages), so the engineer adds sections from measured use instead of a guess. For reference, the field sessions' lookups would have suggested, by calls that touched each section: §9.2 Policy Engine state diagrams 1,876 (9.2.3 source 417, 9.2.20 dual-role 253, 9.2.4 sink 240, 9.2.5 soft reset 237, 9.2.8 alert 196), §6.5 extended messages 1,015 (6.5.3 Status 247), §9.1 protocol layer 397, §6.3 control messages 332, §4.3 dual-role ports 322, §6.4.2 Request 315, §7.1 reset 250, §4.4 hard reset 203, §7.5 applicability tables 181. The distillation that exists covered §3.2, §4.1, §4.5, §4.7, the PDO/APDO fields and the timer tables.

## Why now

The procedure exists only as uncommitted text, so the next standard a project adds is filed as `other` again and distilled by hand. The field distillation picked its sections before any session had asked a question, and 52% of the later lookups landed on pages it did not cover.

## Done when

- [ ] The owner has accepted or changed the 2026-10-08 design, and that version of DESIGN.md, `standard-procedure.md` and both SKILL.md files is on main.
- [ ] `inventory` files a synthetic standard (title page with "Specification" and a release line) as `standard`, and a synthetic datasheet that cites an IEC standard in its body as `datasheet`.
- [ ] `doc sections --add/--why` writes the worklist; `doc sections` lists each section with pages, tokens and status (todo, frozen, redo); a re-run on unchanged pages redoes nothing.
- [ ] `doc sections --suggest` ranks undistilled sections from a fixture usage log, with the call count per section.
- [ ] Check W passes and fails on fixture requirements (`shall-not` needs "shall not" or "must not" in the quote).
- [ ] A standard's card lists its distilled sections and names `find_text` for the rest.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped.

## Blocked

Parked by the supervisor on 2026-10-29, not by a worker. The task opens with the owner reviewing the 2026-10-08 design, which no agent can do for him, and three legs in a row left it `open` while calling it owner-gated in their log entries. Left `open`, `queue-status.py` counted it, and `atlas/004` and `011` behind it, as dispatchable work no leg would take, so the relay kept spawning legs into a queue it could not drain and never reached the dream that asks him. `embarch-atlas-wt` still held the uncommitted `DESIGN.md`, both `SKILL.md` changes and `standard-procedure.md` on 2026-10-29. Back to `open` the moment he answers.
