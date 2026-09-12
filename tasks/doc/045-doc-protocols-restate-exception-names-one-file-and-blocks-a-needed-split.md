# 045 — `DOC-PROTOCOL.md`'s link-don't-restate exception names one file, and that is what blocks `suite/user-guide.md`'s split

**State:** open
**Source:** `tasks/suite/030`, leg 092, 2026-09-11 — found while running that task's announcement
window and attempting its squeeze fork.
**Scope:** doc
**Hardware:** none
**Owner:** required — `DOC-PROTOCOL.md` is owner-reserved (`embarch-fleet/protocol.md` §2). No
worker and no supervisor may write it, which is why this is filed rather than done.

## What

`DOC-PROTOCOL.md` carries the link-don't-restate rule and one exception to it, written **as a
filename** in two places:

- §43 — suite-level docs are enumerated, ending *"and `suite/user-guide.md` — the one doc written
  for a reader not already inside the project, and therefore the one place §5's link-don't-restate
  rule does not apply."*
- §61 — *"Exception: `suite/user-guide.md`, where a getting-started guide that only links is
  useless."*

Both name the file. Neither names the **property** — being written for a reader outside the
project — that earns the exception.

## Why it matters now

`tasks/suite/030` needs to split `suite/user-guide.md` §7 and §7.1 (the MCP tool surface and its
permission split) into a `suite/agent-guide.md`. That is the right move and this task's filing is
the only thing standing in its way:

- The split is **not** blocked by `DOC-BUDGET.md`, which `suite/030` assumed. Line 26's
  `suite/*.md` → 10 KB glob already covers a new suite doc; verified by creating one and running
  `check-doc-size.py`, which counted it and raised nothing.
- It **is** blocked here. A `suite/agent-guide.md` whose whole content is a restated enumeration of
  `embarch-api`'s tool surface would fall under §5's rule with no exception covering it — while the
  identical text is compliant today purely because of the filename in §43 and §61.

`suite/studies-guide.md` is arguably in the same position already and has never been named either.

## Two shapes, and the second is probably right

1. **Add the filename**, making the exception a two- or three-item list. Cheapest; keeps drifting
   every time a suite guide is added.
2. **State the property instead**: the exception applies to `suite/*.md` docs written for a reader
   not already inside the project, and name the current members as examples. That is what §43's own
   wording already reaches for (*"the one doc written for a reader not already inside the
   project"*) — it is a definition with a count of one accidentally frozen into it.

## Also worth fixing in the same pass

`embarch-promptu/design.md` cites `suite/user-guide.md` **§7.1 by section number, twice** (lines 7
and 13). Line 13 explicitly promises not to restate the permission lists *because* that section
holds them. Any split has to repoint both in the same commit or the citations break silently with
the gate green — the failure class `tasks/doc/044` exists for.

## Done when

- [ ] `DOC-PROTOCOL.md` §5/§43/§61's exception no longer depends on a single filename, by whichever
      of the two shapes above the owner prefers.
- [ ] `tasks/suite/030` is unparked, with a line saying the split fork is now available.
- [ ] `changelog.d/` fragment. Gate green (`../../embarch-fleet/protocol.md` §10).
