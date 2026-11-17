# 068 — A shared datasheet library, and a copy of every file an atlas used

**State:** done on agent/atlas/068-a-shared-datasheet-library-and-a-copy-of-each-file-used, 2026-11-17
**Source:** EMB-198, the build of the owner decision recorded on 2026-11-17 in `embarch-atlas/DESIGN.md`, "Where documents come from"
**Issue:** EMB-198
**Scope:** atlas
**Hardware:** none
**Owner:** no

## What

Two gaps, one decision. `DESIGN.md` "Where documents come from" records it: a
shared library folder the engineer fills by hand and every project reads, plus a
copy of every file an atlas used, keyed by sha256, and still no fetching. Build it.

- **No shared folder.** `inventory` reads only `[project] sources`, relative to
  `fw`, so the same datasheet is copied by hand into each project's sources folder.
- **No copy of what was used.** `doc prep` records the path of the file where it
  lies (`doc.json` `path`), and `doc check`, `doc regparse`, the column reader and
  the second look open the PDF there. A file replaced or deleted in the sources
  folder leaves a frozen distillation reading other bytes, or none.

The issue's direction, which you may change on any point, recording what you
chose in `DESIGN.md`:

1. **Setting.** `[project] library = "/abs/path"` in `atlas.toml`, optional,
   outside any firmware repo. Unset: today's behaviour, byte for byte.
2. **Scan.** `inventory` reads the library beside the sources folder. A library
   file enters the manifest only when a part on the target's boards or the MCU
   role is tied to it (a part token, a rung, a confirmation), with
   `origin = "library"` and `file` relative to the library; the others stay out
   of the manifest and out of "Supplied documents nothing uses", since they serve
   other projects. The same sha256 in both folders: the sources folder's file
   wins and the library's is `duplicate_of` it. Page text goes to
   `inventory/text/` as today; a path, size and mtime index in the atlas directory
   keeps a large library from being hashed again on every run.
3. **Copy.** `doc prep`, and the schematic ingest for a board PDF, copy the file
   they read, from either folder, to `<atlas dir>/files/<sha256>/<file name>`, and
   `doc.json` `path` names the copy. A document prepped before this is copied at
   the next `inventory` when its file still has the sha256 in `doc.json`. The tool
   never deletes a copy.
4. **Answers.** `answers.toml` stays keyed by sha256;
   `missing --confirm <MPN> --file <file>` accepts a library file by its manifest
   name.
5. **Never.** No download, no network call, and no write into the library folder.

Where to look: `project.py` (`sources_dir`, `_current_schematic_shas`),
`inventory.py` (`list_sources`, `sources_of`, `run`, `mark_supersession`),
`missing.py`, `pdftext.py` (`prep`, `resolve_pdf_path`), `secondlook.py`
(`_pdf`), `smartpdf.py`, `stale.py`, `DESIGN.md`, and
`skills/atlas-translate-docs/SKILL.md` (where the engineer is told to drop
documents).

**This is a large unit.** If it cannot all land in one pass, land the setting,
the scan and the copy with their tests, and write what is left into this file as
a follow-up rather than shipping a half-wired path.

**Public repo.** Synthetic fixtures only: a made-up part, a generated PDF. No
real datasheet, no client part list. `test_public_guard` must run, not skip (the
worktree's parent carries the `.atlas-local` link).

**Burndown leg: no new numbered decision.** `embarch-atlas` keeps none; the
decision is the owner's and already written. Describe what you built in
`DESIGN.md`; if a choice you hit is a real design fork the decision does not
settle, file it with `scripts/fleet-linear.py file --from decision` and take the
narrower reading.

**What you may change.** Only `embarch-atlas` and `embarch-doc/embarch-atlas/`.

**Doc reserve.** Nothing of `embarch-atlas`'s is in reserve.

## Why now

The owner moved it to Fleet Ready the day he recorded the decision.

## Done when

- [x] With `[project] library` unset, `inventory` and `missing` write the same files as before, and the existing tests pass unchanged.
- [x] A datasheet present only in the library covers a board part in `missing` and in the join; a library file no board part or MCU role is tied to is neither in the manifest nor under "Supplied documents nothing uses".
- [x] `doc prep` and the schematic ingest copy the file they read under its sha256 in the atlas directory, and `doc.json` `path` names the copy; after the original is deleted or replaced, `doc check`, `doc freeze` and `second-look prompt` still read the copy.
- [x] A library file whose content changed shows in the inventory diff, and a confirmation in `answers.toml` on the old content goes back to proposed, as it does for the sources folder.
- [x] A test runs `inventory`, `missing` and `doc prep` with the library folder read-only and no network, and nothing fails or writes there.
- [x] `DESIGN.md` describes what was built in "Where documents come from", the on-disk layout and the `atlas.toml` section, and its "Not yet built" line for the library is gone.
- [x] Gate green (`../../embarch-fleet/gate.md`, Python bullet); `changelog.d/` fragment dropped.

## Outcome

Built in `embarch-atlas` (`src/embarch_atlas/library.py`, `tests/test_library.py`, `DESIGN.md` "Where documents come from"): the setting, the tied-only scan with its index, the sha256 copy (`doc prep`, `schematic`, and `inventory` for a document prepped earlier), `missing` re-reading the library, board PDFs found in the library.

Readings taken where the task left room:

- The library flag is `library: true` on the manifest record, not `origin = "library"`: `origin` already holds the Zone.Identifier host that `coverage._link` reads.
- The copy is unconditional, library set or not (item 3 says so). One existing assertion, `test_prep_writes_identity_pages_and_toc`, expected `doc.json` `path` to be the original and now expects the copy; no other test changed.
- `missing` runs `inventory` first when a library is set, because ties read the BOM.
- A name both folders have with different content becomes `library/<name>` (with `library_path`).

## Left, as a follow-up

- No test drives the schematic ingest's copy: it needs a real Altium Smart PDF, which no synthetic fixture here is. The wiring is one call in `smartpdf.run`; `keep_copy` itself is exercised through `doc prep`. A `[[boards]] pdf` kept only in the library is found by `project.board_pdf` and tied in the scan, also untested for the same reason.
- `join`/`build` do not refresh the manifest themselves; a library file becomes tied at the next `inventory` or `missing`.
