# 042 — A reversal row is owed for `embarch-umbrella` decision 3 → 28, and adding it needs a range-file call first

**State:** open — **announced and parked by leg 130, 2026-09-16 23:16, `ts 1789622198.825569`**
(`ops.md` §4). The 30-minute silence window closes at **23:46**; leg 130 intends to execute this as
its last unit if nothing objects. **If a leg ends before the window closes, leave this `open` with
the `ts` above and complete the window rather than restarting it** — re-read the thread with
`/home/gabriel/Github/embarch/embarch-fleet/scripts/fleet-read.py --thread 1789622198.825569`.
**Source:** `umbrella/074`'s reviewer, leg 129, 2026-09-16, filed as
`inbox/doc-umbrella-074-reversal-row-owed.md` and drained here. The supervisor verified the
admission-bar argument independently against `embarch-decision-reversals.md`'s own header and
against both decision bodies before filing this.
**Scope:** suite
**Hardware:** none — one table row and, possibly, one range-file boundary. Nothing is built, no
board, no probe, no live Core, no `doctor` run.
**Owner:** no — but **supervisor-executed**, not dispatchable to a worker.
`embarch-decision-reversals.md` and `reversals/` are shared suite-level docs
(`../../embarch-fleet/protocol.md` §3), so no worker may write them. Whoever takes this owes
`ops.md` §4's announcement-and-park window before executing, like any `suite/` task.

## What is missing

`embarch-umbrella` decision 3 held that `setup` does **not** edit `PATH`, because the release
archive puts all three binaries in one directory and umbrella can find Core as a sibling of itself.
Decision 28 reversed it. Neither number appears in any row of `embarch-decision-reversals.md` or any
of its four `reversals/rows-*.md` range files.

## Why it qualifies, checked against the doc's own bar rather than a paraphrase

The doc's stated admission bar is: *"Every row was caught by a real build, install, capture, or by
reading a real repo's actual files — **never by inspection alone.**"* Decision 28's own opening
sentence says precisely that happened — *"prompted by a real `wsl-host` onboarding run reporting the
wrong Core path, with the repo owner directly requesting the reversal rather than accepting it as a
cosmetic bug"* — and decision 3's own reversal paragraph names what reality showed: **sibling lookup
ties correct operation to wherever the archive happened to be unpacked staying put forever**, and
the printed Core path reported the local Linux sibling instead of the Windows-side binary a
`wsl-host` topology actually needs.

`umb` rows are in scope and plentiful — 6, 8, 9, 58, 71, 77 — and rows 6 and 9 are the same family
(install-time assumptions overturned by a real deployment, both citing `umb 7`).

**The argument that was used to decline it does not hold, and it is worth recording why**, because
it is a reusable mistake. `umbrella/074`'s worker declined on the grounds that the reversal is
*"already handled correctly in its own owning doc"*. But the doc's header says that of **every**
row — *"Every entry is handled correctly in its own owning doc. This page does not restate a
correction's mechanism; it names the assumption, what reality showed, and where to read the rest."*
It is a description of what the page is, not an exclusion criterion. Read as a bar, it would empty
the page.

## The part that is an actual decision, and why this is not a two-minute edit

**Row numbers are permanent identities and range files never re-split.** The four range files cover
1-50, 51-72, 73-92 and 93-109; the newest row is 109 and `reversals/rows-93-109.md` is already
**12,838 B**. So filing row 110 means choosing one of:

1. Extend `rows-93-109.md` to `rows-93-110.md` — renames a file every existing link to it must
   follow, and the index table in `embarch-decision-reversals.md` too.
2. Open a new range file for 110 onward — cheapest structurally, and it is what the existing
   split pattern implies, but it makes a range file with one row in it.
3. Something else, argued.

**And the top-level file is in reserve:** `embarch-decision-reversals.md` is 9,309/10,240 B with
**931 B left**, filed against `tasks/suite/004-compact-suite.md`, **blocked**, due 2026-10-10.
Option 1 costs it almost nothing (one table cell edit); option 2 costs it a whole new table row plus
a link. Either way, check `scripts/check-doc-size.py --pressure` fresh before writing and say in the
report what was spent.

## Done when

- [ ] The range-file question above is answered explicitly, with the reasoning recorded, before any
      row is written.
- [ ] A row for `embarch-umbrella` 3 → 28 exists, in the doc's own voice: the assumption, what
      reality showed, and the owner cell (`umb 3, 28` or whichever form matches its neighbours).
- [ ] The row is placed against one of the eleven recurring shapes if it fits one, or the shape list
      is left alone if it does not — **do not add a twelfth shape to make it fit.**
- [ ] `embarch-decision-reversals.md`'s remaining headroom reported after the edit.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10) — `check-docs.py` in `embarch-doc`; there is
      no code repo for this one.
- [ ] `changelog.d/` fragment.

## Not yours

Nothing here touches `embarch-umbrella`'s own `decisions/install.md`. Decisions 3 and 28 are both
correct and consistent as written, verified in both directions by `umbrella/074`'s worker and again
by its reviewer — **this task adds a catalogue row, it does not amend a decision.**
