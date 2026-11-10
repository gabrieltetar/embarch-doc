# 048 — A part named in passing on another part's datasheet is not covered by it

**State:** claimed by agent/atlas/048-a-part-named-in-passing-is-not-covered, 2026-11-09 22:02
**Source:** Linear issue EMB-30, filed by a session
**Issue:** EMB-30
**Scope:** atlas
**Hardware:** none
**Owner:** no

## What

A part named only in passing on another part's datasheet — a comparison table or a companion-part sentence on page 2 — is at most proposed (a `missing.md` row to confirm), not covered. A datasheet that names its own part on page 1 or in its title still covers it.

Today a part is covered when a document's part tokens match its MPN. Tokens come from the PDF title, keywords, subject and the first 3 pages, up to 6 per document (`PART_LIMIT`), and a token covers every MPN it prefixes (6 or more characters, 2 or more digits). The `exact` rung also covers when the MPN is anywhere on pages 1-3. So a datasheet naming another part on page 2 lists that part as covered, and `missing.md` stops asking for its datasheet until `embarch-atlas missing --reject <MPN> --file <file>` removes it. `029c41b` changed the `appnote` typing; it did not change this.

## Why now

A false "covered" is silent: the missing datasheet is never asked for.

## Where to look

- `src/embarch_atlas/inventory.py` `detect_ids` — builds `parts` from title, keywords, subject and `pages[:3]`; `PART_LIMIT`
- `src/embarch_atlas/coverage.py` `family_regex`, `doc_patterns`, `covering_docs` — token to MPN match
- `src/embarch_atlas/coverage.py` `_exact`, `FRONT_PAGES` — `exact` covers on pages 1-3
- `tests/test_matching.py` — rung and coverage tests
- `DESIGN.md` "Covered, proposed, missing" — the rule as written

## Dispatch notes

- **Synthetic PDFs only.** The fixture: a datasheet for part A whose page 2 mentions part B's full MPN, a BOM containing both, then `inventory` and `missing`.
- `atlas/047` (the kind classifier) landed first (embarch-atlas `df232e9`); read `main` as it is.
- While in `DESIGN.md`, fix one stale word 047 left in the `appnote` bullet under "Kinds": "only a title saying reference manual comes first" is no longer the only case, since a user's guide that is a reference manual is now tested first too (047's reviewer).
- No `embarch-atlas` doc in `embarch-doc` is in reserve at the split.

## Done when

- [ ] In that fixture, B is proposed or missing, not covered, and A's file is not its covering document.
- [ ] A datasheet that names its own part on page 1 or in its title still covers it.
- [ ] `DESIGN.md` "Covered, proposed, missing" states the rule and `tests/test_matching.py` covers it.
- [ ] Gate green (`../../embarch-fleet/gate.md`, the Python bullet); `changelog.d/` fragment dropped.
