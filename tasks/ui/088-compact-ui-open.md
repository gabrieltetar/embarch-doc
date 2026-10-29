# 088 — `embarch-ui/open.md` is in reserve at 4,366 B after `ui/074`

**State:** done — `ui/099` paid it: `open.md` is 3,738 B, under the 3,920 B floor.
**Source:** `ui/074` closed with the file at 4,366 / 5,120 B (754 B left, floor 3,920 B)
**Scope:** ui
**Hardware:** none
**Owner:** no
**Compacts:** embarch-ui/open.md
**Size debt due:** 2026-11-26
**In flux:** no — paid, nothing left to compact.

## What

`ui/074` removed every settled half (754 B). The 11 bullets left are each a distinct open question
with its own trigger or cross-repo pointer. Further size comes only from a trigger firing (probe
unplug run, outpost bridge attached, power capture, owner's stale-prefix hardware session) and
the bullet retiring to a decision, or from a decisions-side pass making a pointer terser.

## Done when

- [ ] `open.md` at or under 3,920 B, no live question tightened or closed by attrition.
- [ ] Gate green, `changelog.d/` fragment.

## Blocked

2026-10-26: nothing further is deletable without shortening a live bullet.
