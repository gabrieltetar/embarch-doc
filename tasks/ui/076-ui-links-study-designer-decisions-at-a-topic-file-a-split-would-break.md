# `embarch-ui` links two of its decisions straight at a topic file that a future `embarch-study-designer` split would break

**State:** claimed by agent/ui/076-repoint-study-designer-links, 2026-09-29 21:23
**Source:** found while working `study-designer/069` (`decisions/gatt-extract.md` reserve)
**Scope:** ui
**Hardware:** none — prose only.

## What

`embarch-ui/decisions/gatt-capture.md` and `embarch-ui/decisions/designer-panels.md`
link `embarch-study-designer` decisions 33, 56 and 78 straight at
`../../embarch-study-designer/decisions/gatt-extract.md` — the topic-file link
shape `scripts/check-decision-refs.py`'s `check_topic_links` watches for
(the `topology/010` failure mode: a mission split moves a decision number
between topic files without renumbering it, and an old direct link keeps
resolving as a path while naming a file that no longer defines the number).

`study-designer/069` needed to get `decisions/gatt-extract.md` out of its size
reserve. The natural remedy — per DOC-BUDGET.md §"split is the default
remedy" — was splitting it into `decisions/gatt-scan.md` (33, 57) and
`decisions/gatt-resolve.md` (56, 78). That would move 33 out of
`gatt-extract.md`, which would make `designer-panels.md`'s direct link to
decision 33 stale and fail the gate for `embarch-ui` — a repo that task could
not touch. `069` squeezed instead and left the file un-split, so this is not
urgent, but the same wall will be hit again the next time `gatt-extract.md`
(currently 11,053 / 12,288 B) needs to shed weight for real.

## Why now

DOC-CONVENTIONS.md's own fix for this is to link the *index* —
`embarch-study-designer/decisions.md` — instead of a topic file, which stays
correct across any future split. Rewriting those two links now, while nothing
is time-pressured, avoids a forced squeeze-only compaction later when
`gatt-extract.md` is back in reserve and a split is the only remaining seam.

## Done when

- [ ] `embarch-ui/decisions/gatt-capture.md`'s reference to
      `embarch-study-designer` decision 56 links to
      `../../embarch-study-designer/decisions.md`, not the topic file.
- [ ] `embarch-ui/decisions/designer-panels.md`'s references to decisions 33
      and 78 do the same.
- [ ] `scripts/check-decision-refs.py` still green.
- [ ] `changelog.d/` fragment.
