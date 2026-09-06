# Repoint the outpost's source-comment references at the four-file docs

**State:** open
**Source:** owner's repo survey, 2026-09-06 — `outpost_priv.h` calls itself a wire specification and its pointer to the rationale is dead
**Scope:** outpost
**Hardware:** none
**Owner:** no

## What

22 references to a deleted file across the outpost tree — `src/outpost_priv.h:13`
("../embarch-doc/embarch-outpost/design.md §4"), `Kconfig:3` ("Every symbol here is documented in
…/design.md"), `CMakeLists.txt:2`, `README.md:28`, `scripts/gen_outpost_manifest.py:4`,
`tests/native_sim_stream/assert_stream.py:39`, and 16 more (`grep -rn 'design\.md'`). `embarch.md`
§6 records those docs as deleted and folded into `spec.md` / `decisions/` / `interfaces/`.

Decision numbers are preserved **verbatim** — they address the sub-project, not a file — so the
mechanical form is `design.md §3 decision N` → `decisions.md decision N`. The handful that cite a
*section* rather than a decision (`§4`, `§5`, `§7`) are repointed to the file that now holds that
content (`interfaces/wire.md`, `interfaces/integration.md`, `spec.md` §4), **spot-checked one at a
time, never `sed`'d blind.** The cross-repo one at `outpost_priv.h:21` points into
`embarch-study-designer`'s current layout — repoint the citation only; do not touch that repo.

Comment-only: no `.c`/`.h`/`.py` behaviour changes.

## Why now

`outpost_priv.h` calls itself the specification of a wire three implementations must agree on, and
its pointer to the rationale is dead. This repo's `CLAUDE.md` already uses the four-file form, so
the tree contradicts itself.

## Done when

- [ ] `grep -rn 'design\.md' --exclude-dir=tests/build` over the repo returns nothing.
- [ ] Every decision number cited is unchanged and resolves in
      `embarch-doc/embarch-outpost/decisions.md`.
- [ ] No section-citation is repointed to a file that does not contain that content — each is
      spot-checked.
- [ ] `tests/unit` still builds and passes.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false.
