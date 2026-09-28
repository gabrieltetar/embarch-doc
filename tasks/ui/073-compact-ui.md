# 073 — `embarch-ui/decisions/shell.md` and `topology-boards.md` are in reserve

**State:** done
**Dispatch note (supervisor, 2026-09-28):** **the numbers below are stale.** `decisions/shell.md`
is now **12,538 / 12,288 B — over its cap and past its 2026-09-27 clock**, the last of the files
turning `main`'s `check-doc-size.py` RED (the other two were paid earlier this leg by `ui/071` and
`core/094`). `topology-boards.md` is 12,177 B (111 B left). Re-derive every number, and re-check
`git log` on both files first — the owner last touched them 2026-09-20 (decisions 46–50). Prefer
the split the task names; if a decision moves, update `decisions.md`'s group table and **every
inbound citation, including from other sub-projects' docs** — if one of those is outside `ui`,
do not edit it: drop an inbox file by absolute path and say so in your report, and the supervisor
repoints it at landing. `ui/071` just landed and moved text into `decisions/trace-rows.md` and
`decisions/time-chart.md`; `decisions/shape.md` (94 B left, `069`), `decisions/study-designer.md`
(`072`) and `spec.md` (`069`) are in reserve and not yours — push none of them further in.
**Source:** `scripts/check-doc-size.py`'s reserve floor, crossed by decisions 46 (the open project
as a shell control) and 47 (a board type's row is its build menu), which landed with their code
**Scope:** ui
**Hardware:** none
**Owner:** no
**Compacts:** embarch-ui/decisions/shell.md, embarch-ui/decisions/topology-boards.md
**Size debt due:** 2026-09-27

## What

`decisions/shell.md` is **12,078 / 12,288 B (98.3%), 210 B left** and
`decisions/topology-boards.md` is **12,186 / 12,288 B (99.2%), 102 B left**. Both are out of
reserve when this closes, or the task says why not and what was deleted instead.

Each has a seam, and `DOC-COMPACTION.md` §2 prefers a split to a squeeze:

- **`shell.md`** carries 4, 8, 25, 42 and 46, and **25 alone is most of its mass** — the measured
  contrast ratios, the tracer, the standalone mark, the raster derivation. 8, 25 and 42 are all
  about how the app *looks and is drawn*; 4 and 46 are about how the shell is *arranged* (the
  sections, the fragment, the project control). A verbatim split of 8 + 25 + 42 into
  `decisions/design-system.md` restates nothing.
- **`topology-boards.md`** carries 44 and 47. 44's own tail — the saved bench, the slug rule, the
  retract path — is a different subject from what a board type *is* and what it builds as, which
  is what 47 is entirely about. `decisions/saved-benches.md` is the clean cut.

## Why now

The debt is real once a file is within one amendment of its cap, and recording it is the
mechanism: an unfiled file in reserve is what `check-doc-size.py` fails on, not the reserve
itself. 102 B left on `topology-boards.md` means the next correction to decision 44 or 47 cannot
land without paying first — and 47 is new, so a correction to it is likely rather than
hypothetical.

## In flux: yes, mildly

Decision 47 shipped 2026-09-20 with the code it describes, and the DUT picker is the surface the
bench owner exercises most; a wording correction to it is plausible within the week. The compaction
should therefore prefer the **split** — which moves prose without rewriting it — over a squeeze
that would have to be re-judged against an entry still settling.

## What the pass may not delete

- Decision 25's **measured** numbers: the 1.12:1 brand-vs-danger reading, the 4.84:1 / 4.98:1
  contrast pair, the 6.9 px/char advance in 42. Each is a fact someone took off a real browser,
  and none is recoverable by reasoning.
- Decision 47's **rejected** alternative — a revision list beside a variant list — and the reason
  it is wrong (Zephyr backs a pair only where a file backs it). It is the whole argument for the
  combination select, and deleting it invites the cross product back.
- Decision 46's ordering rule for the project switch (catalog and benches reload with it).

## Done when

- [x] Both files are out of reserve, or the task says why not.
- [x] A split along a named seam was preferred over deleting live reasoning, per
      `DOC-COMPACTION.md` §2 — or the report says why the seam was rejected.
- [x] If it split: every inbound citation still resolves, and `decisions.md`'s group table gained
      the new row(s).
- [x] Byte numbers before and after, for every file touched.
- [x] `DOC-COMPACTION-PASS.md`'s human question answered in the report, in your own words.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10), `changelog.d/` fragment dropped.

## Report

**Both named seams taken, verbatim, both files out of reserve:**

- `decisions/shell.md`: **12,538 B → 5,228 B.** Decisions 8, 25 and 42 (the
  design system, the brand-vs-accent split, the self-hosted typefaces) moved
  verbatim into new `decisions/design-system.md` (**7,770 B**). Shell keeps 4
  and 46 (the sections/fragment-nav arrangement and the open-project control).
- `decisions/topology-boards.md`: **12,177 B → 9,806 B** (`wc -c` gives 10,013
  including the rewritten header; body content unchanged). Decision 44's own
  tail — "Retracting" and "A saved bench" (which carries the slug rule) —
  moved verbatim into new `decisions/saved-benches.md` (**2,648 B**). 44's
  core (role/name split), the validate-pass section, the build_target section
  and all of 47 stay in `topology-boards.md`.
- Every moved section was diffed programmatically against the pre-split file
  at the branch point (`d9b9d246ef91`) by heading: all 12 sections moved
  **byte-for-byte identical**, nothing rewritten or summarised.
- `decisions.md`'s group table: split the `shell.md` row into `shell.md` (4,
  46) and a new `design-system.md` row (8, 25, 42); split the
  `topology-boards.md` row's description (dropped the retract/saved-bench
  clause it no longer covers) and added a `saved-benches.md` row, numbered
  `44 (saved bench)` — the same disambiguation style already used for decision
  10 across `topology-tab.md`/`trace-view.md`/`trace-chart.md`.
- **Inbound citations:** a repo-wide search for `decisions/shell.md` and
  `decisions/topology-boards.md` found one link that needed repointing —
  `changelog.d/ui-brand-token.added.md`'s `[decision 25](../embarch-ui/decisions/shell.md)`,
  now pointed at `../embarch-ui/decisions.md` (the index, per
  `DOC-CONVENTIONS.md`'s rule for history-shaped links, since a changelog
  fragment is exactly that shape). Every other hit cites decision 44 or 47,
  neither of which moved — their numbered headings stayed in
  `topology-boards.md`, so those links (in `embarch-core/decisions/roles.md`,
  `embarch-api/interfaces/tools-topology.md`,
  `embarch-topology/spec/storage-and-roles.md`,
  `embarch-topology/decisions/enrollment.md`, and two other `ui` changelog
  fragments) needed no change. **No inbox drop was needed** — nothing outside
  `ui` cited a decision that actually moved file.
- **Code branch:** grepped `embarch-ui` (the code worktree) for
  `shell.md`/`topology-boards.md`/`decisions/` — zero hits in source, so the
  code branch carries **zero commits**, per the task's own allowance.
- `check-decision-refs.py`: all 3,169 references resolve, all 49
  `[decision N]` topic-file links name a file that defines that number.
  `check-doc-size.py`: both files clear; the one remaining RED
  (`embarch-core/decisions/handshake.md`) is `core/094`'s, not this unit's.
  Full `check-docs.py`: 10 of 11 PASS, same unrelated RED.
  `check-ownership.py --scope ui`: all 6 changed paths owned.
  `check-client-names.py`: clean.
- **`DOC-COMPACTION-PASS.md`'s human question** ("Can `spec.md` alone answer
  what someone needs to work on this component today?") **is unaffected by
  this pass, honestly**: this was a pure verbatim split of `decisions/`
  content to clear the size gate, not a `spec.md` rewrite — `spec.md` was not
  touched (it is `069`'s, already in reserve, and untouched here). The
  question the gate actually poses for a split, per `DOC-COMPACTION-PASS.md`
  ("A split needs none of this... moving a section verbatim deletes nothing"),
  is whether every inbound reference still resolves after the move — it does,
  mechanically checked above.
- `changelog.d/ui-compact-shell-and-boards.changed.md` dropped (147 B).
