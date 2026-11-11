# 016 — Land the standard document kind, and pick a standard's sections to distil from what sessions read

**State:** done
**Owner's word, 2026-11-10, given directly in his interactive session:** a worker may land the 2026-10-08 `standard` design in `embarch-atlas-wt` as written. That meets the unpark condition above and stands in for this task's first Done-when box (the owner's review).
**Source:** field use on a USB PD charger board, 2026-09-09 to 2026-10-20 — the USB PD R3.2 spec (418 pages) was filed as `other`, distilled by hand as a datasheet into 119 records citing 35 pages, and sessions then read 348 distinct pages of it outside the atlas; the design for a `standard` kind written on 2026-10-08 is still uncommitted in `embarch-atlas-wt`
**Scope:** atlas
**Hardware:** none
**Owner:** no

## What

The owner reviews the uncommitted 2026-10-08 work in `/home/gabriel/Github/embarch/embarch-atlas-wt` (DESIGN.md "Standards and specifications", `skills/atlas-translate-docs/reference/standard-procedure.md`, and the `atlas-translate-docs` and `atlas-use` SKILL.md changes), and the agreed version lands on main together with the code it describes: `inventory` classifies a standard (today the spec falls through to `other`, `embarch-atlas/src/embarch_atlas/inventory.py:397`), `doc sections <doc> --add <sec> --why <text>` writes `worklist.json`, a frozen section is never redone (unit key: section id, its pages' text hashes, procedure version), and `doc check` W compares a requirement's `modality` with the keyword in its quote. On top of that design, add `doc sections <doc> --suggest`: it ranks the undistilled sections by how often sessions' lookups landed in them (the usage log the find-text task writes, plus `doc_section tier=text` pages), so the engineer adds sections from measured use instead of a guess. For reference, the field sessions' lookups would have suggested, by calls that touched each section: §9.2 Policy Engine state diagrams 1,876 (9.2.3 source 417, 9.2.20 dual-role 253, 9.2.4 sink 240, 9.2.5 soft reset 237, 9.2.8 alert 196), §6.5 extended messages 1,015 (6.5.3 Status 247), §9.1 protocol layer 397, §6.3 control messages 332, §4.3 dual-role ports 322, §6.4.2 Request 315, §7.1 reset 250, §4.4 hard reset 203, §7.5 applicability tables 181. The distillation that exists covered §3.2, §4.1, §4.5, §4.7, the PDO/APDO fields and the timer tables.

## Why now

The procedure exists only as uncommitted text, so the next standard a project adds is filed as `other` again and distilled by hand. The field distillation picked its sections before any session had asked a question, and 52% of the later lookups landed on pages it did not cover.

## Done when

- [x] The owner has accepted or changed the 2026-10-08 design, and that version of DESIGN.md, `standard-procedure.md` and both SKILL.md files is on main.
- [x] `inventory` files a synthetic standard (title page with "Specification" and a release line) as `standard`, and a synthetic datasheet that cites an IEC standard in its body as `datasheet`.
- [x] `doc sections --add/--why` writes the worklist; `doc sections` lists each section with pages, tokens and status (todo, frozen, redo); a re-run on unchanged pages redoes nothing.
- [x] `doc sections --suggest` ranks undistilled sections from a fixture usage log, with the call count per section.
- [x] Check W passes and fails on fixture requirements (`shall-not` needs "shall not" or "must not" in the quote).
- [x] A standard's card lists its distilled sections and names `find_text` for the rest.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped.

## Blocked (history)

Parked by the supervisor on 2026-10-29, not by a worker. The task opens with the owner reviewing the 2026-10-08 design, which no agent can do for him, and three legs in a row left it `open` while calling it owner-gated in their log entries. Left `open`, `queue-status.py` counted it, and `atlas/004` and `011` behind it, as dispatchable work no leg would take, so the relay kept spawning legs into a queue it could not drain and never reached the dream that asks him. `embarch-atlas-wt` still held the uncommitted `DESIGN.md`, both `SKILL.md` changes and `standard-procedure.md` on 2026-10-29. Back to `open` the moment he answers.

## Result

Shipped on `agent/atlas/016-standard-sections` (embarch-atlas e3a12bf and 31e1857; branched from `agent/atlas/001-bump-on-head`, which sits on 003, so it lands after both). The atlas has no `spec.md`/`decisions.md`/`open.md`: its contract is the repo's DESIGN.md, plus `embarch-atlas/design.md` here and `changelog.d/atlas-standard-kind.added.md`. No `features.d/` row: atlas has no section in the feature inventory.

- **The design, as written** (e3a12bf): DESIGN.md "Standards and specifications", `standard-procedure.md` and the `atlas-translate-docs` and `atlas-use` SKILL.md changes, copied from `embarch-atlas-wt` (read only, untouched) by `git diff` and a file copy, applied onto current main. Two DESIGN.md hunks met text main had rewritten since 2026-10-08: the doc_id examples gained the standard one, and the `doc check` row kept main's wording with the range now A–W. The `atlas-translate-docs` frontmatter keeps 001's removal of `disable-model-invocation`.
- **Classification** (`inventory.is_standard`): a standards body's designation in the title (the PDF Title and the first three lines of page 1; a designation cited there with "per", "to", "compliant" ... does not count), or a Specification / Standard title (not product, preliminary, objective, device or target specification) with a release line on pages 1–2 and no datasheet heading on pages 1–3. Tested before `datasheet`, after `prd`. Identity: `release_rev` compacts the release line (`r2.0v1.1`, an IEEE/ISO/IEC year without one), `standard_stem` drops revision and date tokens from the file stem; no `part`, no `parts`; `doc prep --kind standard` derives the same doc_id. `coverage` never ties a standard to a part, and `missing` does not list it as a document nothing uses.
- **`doc sections`** (`standard.py`): `--add <sec>[,<sec>] --why <text>` (toc id or title; an unknown one is named, exit 1), a listing with pages, tokens, why, key (section id, its pages' text hashes, `standard-procedure/1`) and status: `todo`, `frozen` (the newest freeze holds `s/<sec>.md` and no page it cites changed), `redo`. `doc freeze` uses `standard-procedure/1`.
- **`--suggest [--used <log>] [--level N]`**: ranks sections not asked for and not distilled by `find_text` hits and `doc_section tier=text` pages in the usage log, credited to the deepest toc section (`--level` rolls up). `doc_section tier=text` now logs `{doc, section, page, tool}`.
- **Check W**: a standard requirement's `modality` against the keyword in its quote; no keyword passes only with a `note`. Standards only, so a PRD's table-borne requirements are not failed. The schema gains `shall-not`, `should-not`, `role` and `cond`; facts.txt shows `role` and `cond`.
- **The card's section list**: `doc sections` and `doc render` rewrite a generated block in `card.md` (distilled sections, asked for and not yet distilled, and `doc_toc` / `find_text` for the rest); `doc freeze` reads the card without the block's body and check M skips it, so the list never thaws the card.
- **Tests** (`tests/test_standard.py`, 16): a synthetic standard PDF filed as `standard` with doc_id `demobus-spec@r2.0v1.1`, a datasheet citing IEC 61000-4-2 on its first page stays `datasheet`, an IEEE designation gives the year; add/why/list, freeze, a re-run on unchanged pages and a change to another section's page keep `frozen`, a change to its own page gives `redo`; suggest from a fixture log with call counts and `--level`; W on nine fixture quotes and through `run_check`; the card block and no thaw. Gate: pytest 762 passed, 3 skipped (`test_public_guard` ran); check-docs, client-names and ownership green.
- **Choices made here**: W on standards only; the card list as a generated block rather than LLM text; a hit on a section already asked for or distilled is not rolled up into its parent by `--level`.
- **Unverified**: classification on a real 400-page specification (only synthetic PDFs here).
