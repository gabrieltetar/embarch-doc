# 089 — `embarch-ui/spec.md` is back in reserve after `ui/084`

**State:** claimed by agent/ui/089-compact-ui-spec, 2026-10-26 07:43
**Reserve (2026-10-26 leg):** besides the target, `embarch-ui/open.md` has 754 B left, parked under
`ui/088`; leave it alone.
**Source:** `ui/084`'s fold, 2026-10-26. The worker made room for its three new behaviours by dropping
two clauses from the destructive-edit invariant; the supervisor restored "leaving the form filled" on
the branch, and the reviewer then found the second, "a directory it cannot fully read is not
permission to delete", stated nowhere else in `embarch-ui/`. Restoring it in the fold put the file at
9,099 / 10,240 B, 1,141 B left, under the 9,040 B reserve line.
**Scope:** ui
**Hardware:** none
**Owner:** no
**Compacts:** embarch-ui/spec.md
**In flux:** no — the invariants `ui/084` touched are settled by its own fix; nothing in flight rewrites
this file.
**Size debt due:** 2026-11-09

## What

Bring `embarch-ui/spec.md` back under the reserve line (9,040 B) per `DOC-COMPACTION-PASS.md`, quoting
every cut in the commit message. Split first where a seam exists: `spec/tabs.md`,
`spec/capture-rendering.md` and `spec/verification.md` already take verbatim moves from this file, so a
section that belongs with one of them is the cheaper move than squeezing an invariant.

## Must not delete

- The destructive-edit invariant whole: refused naming the studies, `409` with studies and steps,
  leaving the form filled, an unreadable file is unscannable never "no references", an unreadable
  directory is not permission to delete, every declared `.eap` block is scanned, an unparseable taps
  sidecar refuses the load.
- The `firmware_version` write-back's "only after a waved-through mismatch, never over `any`" (40),
  in the run's own repo.

## Done when

- [x] `embarch-ui/spec.md` under the reserve line in `scripts/check-doc-size.py --pressure`.
- [x] Every cut quoted in the commit message; no invariant shortened by attrition.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10), `changelog.d/ui-*` fragment.
