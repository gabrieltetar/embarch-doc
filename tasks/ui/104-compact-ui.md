# 104 — `embarch-ui/spec.md` and `open.md` are in reserve after decision 101

**State:** done (token zero)
**Source:** EMB-63 added decision 101's service sentence to `spec.md` (9,265 / 10,240 B) and the unit-install bullet to `open.md` (4,226 / 5,120 B)
**Scope:** ui
**Hardware:** none
**Owner:** no
**Compacts:** embarch-ui/spec.md, embarch-ui/open.md
**Size debt due:** 2026-11-12
**In flux:** no — decision 101 is settled; the unit-install bullet in `open.md` waits on the release-archive question beside it, which does not move the text.
**Must not delete:** `open.md`'s unit-install and release-archive bullets and their triggers; `spec.md`'s sentence that the UI binds before it polls Core.

## What

Compact both files back under the reserve: shorten prose, keep every rule, trigger, measured number and decision reference.

## Done when

- [x] `spec.md` at or under 9,040 B and `open.md` at or under 3,920 B, out of reserve.
- [x] Gate green, `changelog.d/` fragment.

## Done

Split, not squeezed. Verbatim moves: the three role/catalog/board-type invariants went to `embarch-ui/spec/roles.md` (pointer bullet left in `spec.md`, 9,265 to 8,290 B); five trace/live-study open bullets went to `embarch-ui/open/trace.md` (pointer added to `open.md`, 4,226 to 2,220 B). Must-not-delete items untouched. No inbound links changed (no anchors pointed at the moved text). No code-repo change.

**Can spec.md alone answer what someone needs to work on this component today?** Yes for the shape, the invariants and what not to link; the role and catalog rules now need one hop to `spec/roles.md`, and the pointer bullet states the gist so the reader knows whether to take it.
