# Repoint the outpost's source-comment references at the four-file docs

**State:** claimed — leg 048
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

## Dispatch note — leg 048

**The "never `sed`'d blind" line in the What section is the whole task, not a caveat.** Twenty-two
references is exactly the count at which a regex looks like the obvious tool, and this suite has
already paid for the mechanical version of this mistake in the other direction: a citation that
still *resolves* while pointing somewhere the content is not. `check-decision-refs.py` will not save
you — it falls back to "defined somewhere in the sub-project" when the path near the number does not
look like a `decisions.md`-shaped one, so a wrong-but-plausible path passes the gate silently. **Open
the target file and confirm the content is there before you repoint a section citation.** The
decision-number ones (`design.md §3 decision N` → `decisions.md decision N`) are genuinely
mechanical; it is the `§4`/`§5`/`§7` ones that need a human read each.

**Report the count you actually found.** The task says 22 from a 2026-09-06 survey and names six
sites; this queue is old enough that the number will have drifted. Re-derive it with your own
`grep -rn 'design\.md' --exclude-dir=tests/build` and say in the task file what you found versus what
was claimed — a drifted count is a result, not a discrepancy to quietly absorb.

**The cross-repo citation at `outpost_priv.h:21` is citation-only.** It points into
`embarch-study-designer`'s layout. Fix the pointer; do not open, edit, or file anything in that repo
— it is not yours this run.

**Doc-size reserve for `outpost`, so you plan rather than discover.** Four files are in reserve, all
filed under `tasks/outpost/012`: `open.md` **4,891 / 5,120 B (229 B left)**, `decisions/module.md`
7,730 / 8,192 (462 B), `decisions/transport.md` 7,114 / 8,192 (1,078 B), `spec.md` 9,187 / 10,240
(1,053 B). `decisions/tracing.md` is filed separately under `tasks/outpost/008`. **`open.md`'s 229
bytes is the one to watch** — if this unit has anything to say there, say it in fewer words or say
it in the task file instead.

**Reserve rule you owe:** if your work pushes any `outpost` file into reserve, or leaves one there
that nothing has filed, file `tasks/outpost/<next free NNN>-compact-outpost.md` in the same commit.

**This is a comment-only change.** If you find yourself editing a `.c` or a `.h` for anything but a
comment, stop and say why in the task file rather than doing it.
