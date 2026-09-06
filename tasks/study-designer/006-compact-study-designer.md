# 006 — Compact `embarch-study-designer/decisions/crate.md`

**State:** blocked
**Source:** `scripts/check-doc-size.py` — `crate.md` entered reserve on the commit that
added decision 65 (`agent/study-designer/005-release-workflow-decision`).
**Scope:** study-designer
**Hardware:** none
**Owner:** no

**Compacts:** embarch-study-designer/decisions/crate.md
**In flux:** yes
**Must not delete:** decision 64's measured `cargo tree -f "{p} {f}"` two-column result and
its counterfactual ("16 errors" against "passes 9/9") — that is the whole evidence the two
narrow cells must be `cargo build`, and it reads as an assumption the moment it is shortened
to its conclusion. Decision 65's two ground facts, **no git tags at all** and **no consumer
carries a `version` key**, both checked 2026-09-06 and both unre-derivable from the prose
around them. Decision 65's rejected arm (write `release.yml` anyway, and why that would be a
check that never runs) — a decision reduced to its conclusion invites this exact task being
re-filed. Decision 8's git-dependency escape hatch, which decision 65 names as a reversal
condition.

## What

`embarch-study-designer/decisions/crate.md` is 11,267 bytes against a 12 KB
`decision-group` cap — inside the last 10%, with about 1 KB of runway. It now carries seven
decisions (1, 2, 5, 7, 8, 23, 64, 65), two of which are long CI entries added in the last
two days. Bring it back under reserve, or split it by mission: **crate shape and boundaries**
(1, 2, 5, 7, 8, 23) and **what CI checks** (64, 65) are two missions sharing one file, and
`DOC-COMPACTION.md` §3's split is the cheaper move here than prose surgery.

## Why now — and why this is blocked

It is blocked because the subsystem this file describes is still moving, with a named
trigger. Both decision 64's `ffi` paragraph and `open.md`'s "nothing proves the FFI staticlib
actually cross-links" bullet state a *current absence*: there is no `--crate-type staticlib`
cross-build root for a Cortex-M33 soft-float triple, so no step can assert the link dev-bench
actually consumes. **When the dev-bench cross-build lands, that paragraph, that bullet, and
possibly decisions 7 and 23 all change.** Compacting now writes a clean statement of
something about to be wrong.

**Unparked by:** the dev-bench FFI staticlib cross-build landing.

Per `tasks/README.md`, a parked file's compaction still **rides in the unit that next writes
it** — the next `study-designer` unit to edit `crate.md` meets the cap mid-flight and should
carry the `Must not delete:` list above rather than squeezing a new entry into the last
kilobyte.

## Done when

- [ ] `crate.md` is out of reserve (`scripts/check-doc-size.py` clean, no allowance taken).
- [ ] Every item in `Must not delete:` survives, in words a reader can still check.
- [ ] Answered in the compaction commit message, in the compactor's own words:
      *can `spec.md` alone answer what someone needs to work on this component today?*
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
