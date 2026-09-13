# 029 — Three citation sweeps left bare `§N` pointers at a document that no longer exists

**State:** open
**Source:** `dev-bench/022`'s reviewer, 2026-09-13, asked the question directly and answered it
plainly. Counts below are from the merge result (`embarch-dev-bench` `15c8796`).
**Scope:** dev-bench
**Hardware:** none — comment text in C files. No behaviour, no wire, no board.
**Owner:** no

## What

`dev-bench/019`, `020` and `022` repointed ~200 citations of the deleted
`embarch-study-designer/design.md §3` and `embarch-dev-bench/design.md` filenames. Where a citation
carried a decision **number**, it became `` `<repo>` decision N `` and resolves. Where it carried
only a **section** number — `design.md §4.8`, `§4.3a`, `§4.5`, `§4`, `§1` — the dead filename was
stripped and the bare section number left behind.

**Start by re-deriving the count, because the two that exist disagree.**
`grep -cE '§[0-9]' app/src/main.c app/src/ble_bridge.h app/src/serial_protocol.c
app/tests/serial_protocol/src/main.c` → **5, 6, 6, 5 = 22**, which counts *lines*; `022`'s reviewer
counted **21** post-merge, which is probably *occurrences* — one line carrying two, or one `§`
that is not a citation at all. Neither number has been checked against the other, and this task
family exists because of numbers nobody checked, so do not inherit either. That is the four files
`022` touched; `019` and `020` left more in `eap.h`, `eap_interp.h`, `eap_interp.c`,
`serial_protocol.h` and `ble_bridge_real.c`, and no count exists for those at all.

`ble_bridge.h:88` is the shape: *"the crate's own docs state this explicitly for `Uuid` but not for
`BleAddress` (§4)"* — §4 of what.

## Why now, and why this is not just tidying

**The reviewer's read, which is the reason this is filed rather than accepted:** a bare `§N` is
*"a different dangling reference, not an improvement — it drops the repo name too, so a reader can
no longer even tell which repo's history to search; less traceable than the dead-but-named path it
replaced."*

That is the part worth acting on. The old form was wrong but self-describing: a reader saw
`embarch-study-designer/design.md §4.8`, found no such file, and could search that repo's history
for what §4.8 became. The new form names neither the document nor the repo, so the same reader has
nothing to search. Three units have now applied this treatment on each other's precedent, which is
how a convention gets established by accident.

## Done when

- [ ] A decision is taken and written down about what a section-only citation into a deleted
      document should become. The candidates, and none is obviously right: **(a)** resolve each to
      the decision number that absorbed that section, where one exists; **(b)** name the repo and
      say the section is historical — `` `embarch-study-designer`, historically design.md §4.8 ``
      — which keeps traceability without pretending the file exists; **(c)** delete the pointer
      where the sentence stands without it. Expect the answer to differ per hit.
- [ ] Every bare `§N` in this repo's C sources either resolves, names its repo, or is gone.
- [ ] The count is re-derived, including `019`'s and `020`'s files, not taken from this task.
- [ ] Whatever is decided is recorded as a numbered `embarch-dev-bench` decision, since two earlier
      units already followed the unwritten version of it and a third would make it folklore.
- [ ] Host-side checks green; say what could and could not be run (no `west`, no Zephyr SDK in a
      worker's worktree — standing debt, not introduced here).
- [ ] `changelog.d/` fragment.

## Do not

Do not resurrect `design.md`, and do not invent a section number for a document nobody can read.
Where the original section cannot be identified, option (c) is better than a guess — this whole
task family exists because a citation that looks resolvable and is not costs more than no citation
at all.
