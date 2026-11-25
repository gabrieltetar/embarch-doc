# 109 — A `refs` verb lists the atlas's sections, symbols and nodes in one read

**State:** done — refs verb: sections, symbols and nodes in one read; tests, DESIGN.md and design.md
**Source:** EMB-404 — the atlas cannot list its sections, symbols and nodes for another tool
**Issue:** EMB-404
**Scope:** atlas
**Hardware:** none
**Owner:** no

## What

`embarch-atlas refs [--json] [--atlas-dir D] [--atlas <id>]` is a new read-only
verb (`cli.py`'s verb table, its code in a new `src/embarch_atlas/refs.py`)
that prints every datasheet or spec section, Kconfig symbol and devicetree node
the atlas holds, in one call. Today the lookups answer one thing at a time in
markdown (`doc_toc`, `config`, `dt_node` in `query.py`), and another tool that
wants all of them has to re-implement four file shapes and the rule for which
atlas is current.

- **Reuse, do not re-read:** `common.atlas_dir` (a linked worktree reads the
  main clone's atlas), `query.current_atlas`, `query._toc_rows` (which already
  normalises a datasheet's `toc.json` `sections[]` and a reference manual's
  `outline.json` `entries[]`), `stale.py`, and the fields `kconfig.py` and
  `dt.py` write.
- **The JSON shape is fixed in `embarch-promptu`'s `docs/contract.md` §15.3**:
  `{"atlas_refs": 1, "atlas_dir", "atlas", "commit", "stale", "sections",
  "symbols", "nodes"}`. A section is `{doc, kind, part, id, title, level,
  page}`, `page` the first physical page, `kind` and `part` from the
  document's `doc.json`; a symbol `{name, prompt, type}`, `prompt` null when it
  has none; a node `{path, labels, compats, status, aliases}`. Read §15.3 and
  follow it where it is more exact than this paragraph.
- **Sections come from every translated document**, which exist without a
  built atlas; symbols and nodes come from the current atlas only. **No atlas
  folder at all**: `atlas_dir` and `atlas` null, empty lists, exit 0, so a
  caller reads "no atlas" without parsing an error.
- **A stale atlas still answers**, with its reasons in `stale` as the lookups'
  `src:` line gives them.
- **Read-only and quiet**: no model, no network, no `usage.jsonl` row (that
  log records lookups an agent made; this is a list), no file written.
  Without `--json`, one count line per list.
- Time it on the test fixtures (and on a real atlas only if one is already on
  this machine), and write the time in `DESIGN.md` as measured, or say it is
  not.

## Why now

EMB-404: the chat linker's sections kind and its symbols-and-nodes kind
(`embarch-promptu` build step 5, `embarch-doc/embarch-promptu/decisions/chat.md`
16) read this verb. Promptu's contract §15 fixed the shape on 2026-11-25
(`promptu/024`), which was this issue's blocker.

**Burndown leg: no new numbered decision.** The shape and behaviour are fixed
by the issue and the contract; record the verb in `DESIGN.md` and
`embarch-doc/embarch-atlas/design.md` (or its `design/` files). If the work
turns out to need a decision neither states, stop and say so in this file.

## Done when

- [x] A fixture with a datasheet `toc.json` and a reference manual
      `outline.json` gives one `sections` list with each document's `kind`
      and `part`.
- [x] A fixture atlas gives `symbols` with their prompts (null where none) and
      `nodes` with labels, compatibles, status and aliases.
- [x] Run from a linked worktree, the verb reads the main clone's atlas.
- [x] No atlas folder gives null atlas, empty lists and exit 0; translated
      documents with no built atlas give sections and no symbols or nodes.
- [x] An atlas whose commit is not HEAD gives its stale reasons.
- [x] `DESIGN.md`'s CLI table and `embarch-doc/embarch-atlas/` say it.
- [x] Gate green (`../../embarch-fleet/gate.md`), `changelog.d/` fragment
      dropped.
