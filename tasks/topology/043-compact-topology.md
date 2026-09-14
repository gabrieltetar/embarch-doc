# 043 — Compact embarch-topology/spec.md

**State:** open
**Source:** `topology/042` spent `spec.md`'s reserve adding the probe-selection section its
`Done when` boxes required; the dispatch note for `topology/042` (leg 111) named this as the
preferred outcome over shrinking the new section to dodge the line.
**Scope:** topology
**Hardware:** none
**Owner:** no

## What

`embarch-topology/spec.md` is 9,825 / 10,240 B (95.9%, 415 B left) — in reserve. Compact it: the
usual candidates are prose the decision files already carry in full (`spec.md` should state facts,
not re-derive why they're true) and any section whose own decision citation has grown a fuller
restatement over time than the fact needs.

**Compacts:** embarch-topology/spec.md
**Size debt due:** 2026-09-20
**In flux:** no — decision 32 and 33 are closed on both sides of the `embarch-core`/`embarch-topology`
boundary, `core/055` has landed, and nothing about probe selection is expected to move again soon.
**Must not delete:** the new *What each consumer owns now* probe-selection bullet's three-behaviour
list (zero probes / multi-probe / serial-miss) — that is the fact this task's own predecessor
(`topology/042`) added because no other section stated it; do not fold it back down to a bare
decision citation with no content, which would silently re-open `042`. Also keep the *Shape* section's
consumer-call table (Core/api/umbrella's three call sites) — it is the single place a caller sees the
whole cross-repo picture at a glance, and duplicating it into decisions would violate the
no-restatement rule instead of fixing it.

## Why now

`check-doc-size.py --pressure` shows `embarch-topology/spec.md` unfiled in reserve as of `topology/042`
landing. The gate fails on an unfiled file in reserve; this task is what files it (`tasks/README.md`'s
Compaction tasks section, `DOC-COMPACTION.md` §2).

## Done when

- [ ] `embarch-topology/spec.md` is measurably smaller and back under its reserve line (< 90% of
      10,240 B, i.e. under roughly 9,216 B), verified with `check-doc-size.py`.
- [ ] Nothing on the `Must not delete:` list above is gone or reduced to a bare citation.
- [ ] The compactor answers, in the commit message, `DOC-COMPACTION-PASS.md`'s question: can
      `spec.md` alone answer what someone needs to work on this component today?
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `changelog.d/` fragment.
