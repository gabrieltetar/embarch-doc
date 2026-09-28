# 072 — `embarch-ui/decisions/study-designer.md` is in reserve

**State:** claimed by agent/ui/072-compact-ui-study-designer-decisions, 2026-09-28 17:01
**Source:** `scripts/check-doc-size.py`'s reserve floor, crossed by decision 11's reversal rewrite
**Scope:** ui
**Hardware:** none
**Owner:** no
**Compacts:** embarch-ui/decisions/study-designer.md
**Size debt due:** 2026-09-25
**In flux:** no

## What

The Study Designer decision group is **11,232 / 12,288 B (91.4%), 1,056 B
left**. Out of reserve when this closes, or the task says why not.

What crossed the floor is decision 11's reflash paragraph being **rewritten
rather than deleted** ([reversals](../../embarch-decision-reversals.md) row
113). The new text is longer than the old because it has to carry both: what
shipped, and why the three options it weighed were each judged correctly while
the list was short by one. Deleting the old reasoning was the cheaper edit and
the wrong one — it is the argument a later reader needs in order to not make the
same omission.

## Why the seam is a split, not a squeeze

This file carries five decisions across four unrelated authoring surfaces:
version fields (11), the step table's security level and the declared-GATT
picker (12), opening a firmware repo (14), the run badge's counter (20) and the
stream-name cap (22). **14 is the obvious one to move** — "which repo is open"
is a property of the whole tab, not of authoring a study, and it is the
decision the new `firmware-build.md` cites most (the Build card matches its
project by that repo's path). A `decisions/project.md` taking 14 verbatim
leaves this file about authoring, per
[../../DOC-BUDGET.md](../../DOC-BUDGET.md) §3.

## Dispatch note (supervisor, 2026-09-28)

Three days past its clock, and it has grown since filing: `check-doc-size.py --pressure` now reads
**11,392 / 12,288 B, 896 B left**, not the 11,232 above. **Also in reserve in `ui`, not yours to
write:** `decisions/shape.md` **94 B left** and `spec.md` at 11,022 / 10,240 B (both
`tasks/ui/069`, open — a separate unit), and `open.md` 253 B left (`tasks/ui/074`, blocked). If
your work pushes any other `ui` file into reserve, file `tasks/ui/<NNN>-compact-ui.md` in the same
commit.

## Done when

- [ ] Out of reserve, or the task says why not.
- [ ] **Decision 11's reversal paragraph is not what gets cut.** It is the
      newest text in the file and the one a reader arriving from the reversals
      page lands on.
- [ ] `decisions.md`'s index row updated for whatever moves.
- [ ] Every inbound reference still resolves (`check-decision-refs.py`).
- [ ] Byte numbers before and after.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10), `changelog.d/` fragment.
