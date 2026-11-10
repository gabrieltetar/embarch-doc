# 049 — A document's own header names its revision and number, and `doc check` says when K could not run

**State:** open
**Source:** Linear issue EMB-42, filed by a session
**Issue:** EMB-42
**Scope:** atlas
**Hardware:** none
**Owner:** no

## What

A non-chip datasheet (a battery cell's) got its revision and document number from the inventory, while its own header printed `REV. A` and `DOC NO. 001`. It has no outline and no MIN/TYP/MAX tables, so check K checks nothing on it and the `doc check` summary does not say so.

1. **Identity.** `prep` takes part, revision and document number from the inventory manifest entry when there is one (`_manifest_entry`, then `ident.update(...)`), and from `derive_identity` only when there is none. The manifest's values come from `detect_ids`, whose conventions are vendor ones (`DS20005678B`, literature numbers, `DS`/`RM`/`AN` prefixes, a `Rev` text match). A header of the form `REV. A` / `DOC NO. 001` is not among them. A first page printing that form should give rev `A` and doc_no `001` in the manifest and in `doc.json`.
2. **K that did not run.** `DocText.columns` returns `no-header` for each row of such a document and K reports `not checkable`, but the `doc check` summary shows no K line at all. It should state that K did not run.

## Why now

A document's own header is the best evidence of its identity, and a check that silently runs on nothing reads as a check that passed.

## Where to look

- `src/embarch_atlas/inventory.py` `detect_ids` — doc_no and rev for the manifest
- `src/embarch_atlas/pdftext.py` `prep` — manifest entry beats `derive_identity`
- `src/embarch_atlas/pdftext.py` `derive_identity` — `_REV_TEXT`, `_ST_DOC`
- `src/embarch_atlas/check.py` `DocText.columns` — header detection, `no-header`; and wherever the `doc check` summary is assembled
- `tests/test_inventory.py`, the check tests — synthetic PDFs, as `atlas/047` and `atlas/048` built them
- `DESIGN.md` — wherever identity or the K check's reporting is described

## Dispatch notes

- Synthetic PDFs only: no real vendor file is needed or should be committed. What a real header of this form reads like is owed to a real file; write that as a debt in the task file.
- Do not let the new pattern match ordinary prose ("rev. a of the board" in a sentence): anchor it the way `_REV_TEXT` anchors its own.
- Burndown is on: no new numbered decision. Amend `DESIGN.md` in place.
- Link `.atlas-local` is in the worktree's parent and the worktree has its own `.venv`; `test_public_guard` must run, not skip.

## Done when

- [ ] A first page printing `REV. A` and `DOC NO. 001` gives rev `A` and doc_no `001` in the manifest and in `doc.json`; a test in `tests/test_inventory.py` covers it.
- [ ] On a document with no MIN/TYP/MAX header, `doc check` states that K did not run, instead of showing no K line.
- [ ] Gate green (`../../embarch-fleet/gate.md`, the Python bullet); `changelog.d/` fragment dropped.
