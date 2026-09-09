# Repoint the outpost's source-comment references at the four-file docs

**State:** done — leg 048
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

- [x] `grep -rn 'design\.md' --exclude-dir=tests/build` over the repo returns nothing.
- [x] Every decision number cited is unchanged and resolves in
      `embarch-doc/embarch-outpost/decisions.md`.
- [x] No section-citation is repointed to a file that does not contain that content — each is
      spot-checked.
- [x] `tests/unit` still builds and passes. — see note below: not run here, host-side legs pass.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false. — see note below: no content in those three
      files changed (nothing they say was made false by a citation repoint), so none was edited;
      `changelog.d/outpost-design-md-citations.fixed.md` dropped.

## Result

**Count found: 26, not 22.** Re-derived with `grep -rn 'design\.md' --exclude-dir=tests/build .` in
the code repo (2026-09-08): 26 matching lines across 14 files (`CMakeLists.txt`, `Kconfig` ×2,
`README.md` ×2, `cmake/outpost_build_id.h.in`, `include/embarch/outpost.h` ×2,
`scripts/gen_outpost_manifest.py` ×2, `src/outpost.c` ×4, `src/outpost_hooks.c` ×2,
`src/outpost_markers.c`, `src/outpost_priv.h` ×4, `src/outpost_ring.c`, `src/outpost_time.h`,
`tests/native_sim_stream/app.overlay`, `tests/native_sim_stream/assert_stream.py` ×2). The task's
own six named sites match; the count drifted up from 22 (some sites also carry more than one
citation per line than the original survey counted, e.g. `outpost_priv.h`'s self-exclusion comment
appears twice).

**Mechanical decision-number citations** (`design.md §3 decision(s) N[, M…]` → `decisions.md
decision(s) N[, M…]`, decision numbers unchanged): 19 sites, spanning decisions 1, 2, 3, 4, 5, 6, 7,
8, 9, 17, 18, 19, 20 — all confirmed present in `embarch-doc/embarch-outpost/decisions.md`'s index.

**Section citations, spot-checked one at a time by opening the target file:**
- `src/outpost_priv.h:13` (old `§4`, the wire-format-pinned-by-a-test-on-both-sides rule) →
  `interfaces/wire.md`. Confirmed: wire.md's closing sections ("The host decoder's rules are
  tested…", "Two independent decoders agree…") are exactly that rule.
- `Kconfig:3`, `CMakeLists.txt:2`, `scripts/gen_outpost_manifest.py:4`, `src/outpost.c:10` (old
  bare `§5`/`§5.2`/`§5.3`/`§5.4`, all about Kconfig symbols, the build ID, and the manifest
  generator) → `interfaces/integration.md`. Confirmed: its Kconfig table covers every symbol named
  in these files' surrounding text (ring bytes, batch bytes, fill wait, thread priority, build-ID
  pin), and its prose covers the manifest/build-ID relationship.
- `README.md:189` (old `§7`, "the instrumentation overhead is deliberately uncharacterised") →
  `spec.md` §4 ("The instrument's measured cost"). Confirmed: that is the section spec.md now uses
  for exactly this kind of measured-cost claim, per the task's own mapping hint. (Note: `spec.md` §4
  and the README's Status section now disagree on whether the overhead is characterised —
  spec.md says it has been measured on real hardware since 2026-08-27, the README's Status
  section still says "no outpost byte has ever crossed a real UART." That is a **pre-existing
  staleness in README.md's Status section**, not something this repoint introduced or was asked to
  fix — flagging it here rather than silently repairing prose outside this task's scope.)
- `include/embarch/outpost.h` and `src/outpost_hooks.c`/`src/outpost_ring.c`/`src/outpost_time.h`/
  `src/outpost_markers.c`/`tests/native_sim_stream/*` citations were pure decision-number citations
  (no bare section), handled mechanically per above.
- `README.md:28` (generic, undecorated pointer to the whole doc) → rewritten to the four-file form
  already used by this repo's own `CLAUDE.md` (current truth `spec.md`, why `decisions.md`,
  unresolved `open.md`, reference `interfaces/`), rather than picking one arbitrary target file.

**Cross-repo citation** at `src/outpost_priv.h:21` (COBS framing shared with the Core↔dev-bench
link) → repointed only the path, `embarch-study-designer/design.md §3 decision 10` →
`embarch-study-designer/decisions.md decision 10`, confirmed by reading (not editing)
`embarch-doc/embarch-study-designer/decisions/wire.md:11`, which does carry decision 10 (COBS
framing). `embarch-study-designer` itself was not opened for edit and nothing was filed there.

**`tests/unit` (the Zephyr ztest suite) was not built** — no `west`/`ZEPHYR_BASE` toolchain is
available in this worker's environment, and this change touches only comments, no `.c`/`.h`/`.py`
behaviour. What was run instead: `bash tests/run-all.sh`'s three host-only legs — `decoder_unit.py`
(20/20 pass), `vocab_check.py` (pass, sibling repo not checked out so only the module-internal half
ran), `cross_decoder.py` (loud skip, no sibling fixtures/`WEST`, as designed). This is the same
kind of toolchain gap `protocol.md` §7 hands hardware-verification debt for — recording it as a
debt here rather than claiming a build I did not run: **`tests/unit` (native_sim ztest suite) needs
running with a real `west`/`ZEPHYR_BASE` Zephyr toolchain to confirm the comment-only diff did not
regress it** (it should not, since no non-comment byte in any `.c`/`.h`/`.py` changed, verified by
`git diff` review — but this was not independently confirmed by an actual build).

**Reserve:** `open.md` (229 B headroom) was not touched — nothing about this unit is unresolved or
needs a new open question, so its one nearly-full file stays untouched. No `outpost` file was
pushed further into reserve by this change; no new compaction task filed.

**No `spec.md`/`decisions.md`/`open.md` edit was needed**: nothing this unit found or decided
belongs in current truth, rationale, or open questions — it is a mechanical citation repoint with
one incidental finding (README.md's stale Status section, noted above but out of scope) and no
`status.d/` fact to correct, since `embarch.md` §6 already correctly describes design.md as deleted
and folded.

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
