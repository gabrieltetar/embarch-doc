# 025 — the README's Layout table omits about a dozen `src/` modules

**State:** claimed — leg 061, worker on `agent/study-designer/025-readme-layout-table`

**Dispatch note (supervisor, leg 061):** enumerate `src/` from the tree, not from the task's or
`024`'s description of it, and check both directions — the defect this fixes is exactly a converse
that nobody checked. **Doc-size reserve for `study-designer`:**
`embarch-study-designer/spec.md` 9,600/10,240 B (640 B left) and
`embarch-study-designer/open.md` 4,662/5,120 B (458 B left), both filed against
`tasks/study-designer/006-compact-study-designer.md` (open, not blocked). The README is in the code
repo and uncapped, so this unit should not need either — if it does, and it spends reserve, file
`tasks/study-designer/<NNN>-compact-study-designer.md` in the same commit.
**Source:** `embarch-reviewer` on `tasks/study-designer/024`, 2026-09-09, leg 059 — found while
checking that unit's claim that the Layout table needed no edit
**Scope:** study-designer
**Hardware:** none
**Owner:** no

## What

`study-designer/024` rewrote the README's **Features** section and left the **Layout** table
alone, on the verified claim that every module the table lists is present in `src/`. That claim is
true. **The reverse was never checked, and it does not hold:** the table omits roughly a dozen
modules that do exist in `src/` — including the ones backing the three features that same unit
had just finished documenting (`gatt-extract`, `study-ui`, `eap-parse`).

So the README now has a Features section that names a capability and a Layout table that does not
say where it lives, which is a worse state than the one before `024` only in the sense that the
gap is now visible. Bring the Layout table into line with `src/`: every module present, each with
the one-line description the table's existing rows use, and nothing listed that is not there.

## Why now

A features list and a module map that disagree is the same class of defect `024` existed to fix,
one level down, and this is the cheap moment to close it — `024`'s own diff establishes what the
feature set actually is, so the mapping question is the only one left.

**A checked claim and its converse are two claims.** `024`'s worker verified "everything listed
exists" and reported it in words that read like "the table is correct"; the reviewer found the
converse false in one pass. That is worth remembering when a unit reports a table as verified.

## Done when

- [ ] Every module in `embarch-study-designer/src/` appears in the README's Layout table, or the
      table states its own scope explicitly (e.g. "public surface only") so the omissions are
      deliberate rather than stale.
- [ ] No module is listed that does not exist, and no retired type is named.
- [ ] The modules backing `gatt-extract`, `study-ui` and `eap-parse` are locatable from the README
      alone.

## In flux: no

## Not in scope

**No numbered decision.** Nothing in this suite decides what a README's module table must contain,
and `024`'s reviewer confirmed no decision governs it — this is an accuracy fix, not a design
question. If it turns out to need one, stop and say so.
