# 078 — Compact ui's spec.md

**State:** blocked — `In flux: yes` (see below); set by the supervisor 2026-09-29, it was filed `open`.
**Size debt due:** 2026-10-13 (two weeks; the file is 5 B inside reserve).
**Source:** tasks/ui/077 restored "served by the binary" in `embarch-ui/spec.md`'s
dev-bench-picker invariant, which pushed the file to 9045/10240 B (88.3%),
inside `check-doc-size.py`'s reserve.
**Scope:** ui
**Hardware:** none
**Owner:** no

**Compacts:** embarch-ui/spec.md

## What

`embarch-ui/spec.md` is in the size reserve (9045/10240 B, 1195 B left). Run a
compaction pass per `DOC-COMPACTION-PASS.md`, quoting every hunk in the commit
message per its quoting rule.

## In flux

Yes. ui/077 (this leg) just edited the "role is a fixed slot" paragraph
(dev-bench-picker invariant) to restore a dropped load-bearing phrase.
Whoever runs this compaction should re-check that paragraph is still current
before touching it, and must not re-drop "served by the binary" or the
"served from the binary like every other vocabulary" tie to
`embarch-ui/decisions/topology-roles.md` — that was the exact loss this task's
predecessor (ui/075 → the ui/077 restore) fixed.

## Must not delete

- The "served by the binary" phrase in the dev-bench-picker sentence
  (the "role is a fixed slot" paragraph).
- Any other named claim currently quoted in `embarch-ui/spec.md`'s invariants
  list — this pass is a squeeze, not a second drop.

## Done when

- [ ] `embarch-ui/spec.md` back under the reserve threshold in
      `scripts/check-doc-size.py`.
- [ ] Every hunk quoted in the commit message per `DOC-COMPACTION-PASS.md`.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
