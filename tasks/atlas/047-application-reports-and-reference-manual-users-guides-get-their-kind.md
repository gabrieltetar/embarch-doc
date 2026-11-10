# 047 — An application report is an appnote, and a user's guide that is a reference manual is a reference manual

**State:** claimed by agent/atlas/047-application-reports-and-reference-manual-users-guides-get-their-kind, 2026-11-09 21:19
**Source:** Linear issue EMB-29, filed by a session
**Issue:** EMB-29
**Scope:** atlas
**Hardware:** none
**Owner:** no

## What

The inventory's kind classifier types a vendor "Application Report" as `appnote`, and types a vendor "User's Guide" that is really the MCU's reference manual as `reference-manual` without `--kind`. A plain user's guide stays `appnote`.

Today `classify` calls a PDF `appnote` only when `APPNOTE_WORDS` matches its title, file name or the top of page 1, or an `AN`/`UM`/`TN` number matches. `APPNOTE_WORDS` has `application note`, `app note`, `user guide` / `user's guide` and `technical note`, and no `application report`, so an application report falls through to the later rules (`datasheet` on "features", else `other`). The opposite miss: a title or file name saying "User's Guide" matches `appnote` before the `reference manual` rule on the first page's text is reached, so a reference manual published as a user's guide is `appnote`, which never covers a part and is refused by `--confirm`.

## Why now

Both misses need a hand `--kind` today (`embarch-atlas missing --kind <file> <kind>`), and the second one silently leaves an MCU without a reference manual.

## Where to look

- `src/embarch_atlas/inventory.py` `APPNOTE_WORDS`, `is_appnote`, `classify` — appnote is tested before `reference manual` in the first 2000 characters; only a title saying "reference manual" comes first
- `tests/test_inventory.py` — classifier tests on synthetic PDFs
- `DESIGN.md` "Document kinds and coverage" — the rule as written

## Dispatch notes

- **Synthetic PDFs only**; no vendor file belongs in this public repo.
- State the rule that makes a user's guide a reference manual in `DESIGN.md` (for example, its first page calling itself a reference manual or carrying a register map); the worker picks it and says why in the doc.
- No `embarch-atlas` doc in `embarch-doc` is in reserve at the split.

## Done when

- [ ] A synthetic "Application Report" is typed `appnote`.
- [ ] A synthetic "User's Guide" that identifies itself as a reference manual is typed `reference-manual`, and a plain user's guide stays `appnote`.
- [ ] The rules are in `DESIGN.md` and `tests/test_inventory.py` covers both.
- [ ] Gate green (`../../embarch-fleet/gate.md`, the Python bullet); `changelog.d/` fragment dropped.
