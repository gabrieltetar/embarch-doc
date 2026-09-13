# ui/040 review finding: two citations re-derived to the wrong sibling decision

**State:** claimed — leg 103, 2026-09-12.
**Source:** reviewer (unit ui/040)
**Scope:** ui
**Hardware:** none — this is a documentation/citation correctness finding; confirming it needs no board.

## What

`assets/app.js` carries two comments citing `` `embarch-study-designer` decision 39 `` for a
claim about **vendor-defined GATT selection by id rather than by typing a UUID**:

- line ~1129: `// Vendor-defined selection (`embarch-study-designer` decision 39): ids, never
  UUIDs — the whole point is that nobody transcribes 6e400002-… by hand.`
- line ~1177: `// type here but the payload (`embarch-study-designer` decision 39). The payload
  is left empty…` (the NUS-prefilled row, same vendor-id reasoning)

`embarch-study-designer` decision 39 (`decisions/streams.md`) is "One generic inbound stream
pipeline; the write direction explicitly not accepted" — about `StreamTap`/`StreamSource`
unification for capture pipelines. Its body never mentions vendor service ids or UUIDs.

Decision 41 (`decisions/gatt.md`), two headings away in the same sub-project, is "A built-in
table of vendor-defined GATT service identities" and its body says verbatim: "So those
identities ship as constants, **picked by id, never by typing a UUID**." That is the exact
claim both comments make.

## Why now

This is the collision class the task brief flagged from `dev-bench/020`: a bare number
re-attributed by subject-matching rather than by re-deriving from the cited decision's own
body. The unit's commit message says every citation was "re-derived from the decision body,
not the heading" — these two were not; 39 was carried over unchanged from the pre-existing
bare cite, and the body it now points at (with a repo name attached, giving it new authority
as a resolved cross-repo citation) does not say what the comment claims. 41 does.

Not a contradiction of a locked decision — both 39 and 41 stand as written, unretired. This is
a mis-citation the unit's own stated method should have caught, now stamped with repo
authority it didn't earn.

## Done when

The two `app.js` sites above cite `` `embarch-study-designer` decision 41 `` instead of 39, or
the owner reviews and disagrees.

## Dispatch note (leg 103)

Re-derive both sites from the decision bodies themselves before editing — that is the method
this finding says the previous unit skipped. If decision 41's body does say "picked by id, never
by typing a UUID", change the two cites; if it does not, leave them and say so.

**Doc-size reserve for `embarch-ui`:** nothing in reserve. If your work pushes an `embarch-ui`
doc into the last 10% of its cap, file `tasks/ui/<NNN>-compact-ui.md` in the same commit.

**Merge SHAs:** code `baebcaf8c33cf80a93112adf7238dfa9643f5ad5` (`embarch-ui`, on
`origin/main`); doc side at `6cf5b58`. Revert of `baebcaf` alone is clean (both sites are
one-line comment edits, no code/logic touched) but oversized — a two-line follow-up fix is
cheaper than reverting all 22 re-attributions to fix 2.
