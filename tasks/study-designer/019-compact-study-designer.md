# 019 — Compact `embarch-study-designer/decisions/registry.md`

**State:** open
**Source:** `scripts/check-doc-size.py` — `registry.md` entered reserve on the commit that
added decision 69 (`agent/study-designer/015-duplicate-field-name`).
**Scope:** study-designer
**Hardware:** none
**Owner:** no

**Compacts:** embarch-study-designer/decisions/registry.md
**Size debt due:** 2026-10-07
**In flux:** no — `study-designer/015` closed the third of this family's rules (35, 66, 67,
69) with no fourth one named or pending; `open.md` carries nothing about `ActionRegistry` or
`RegisteredAction`. Nothing here is expected to become false soon, so a compaction pass now
would not need to guess at content still moving.
**Must not delete:** decision 35's durable principle paragraph (no EmbArch component infers
hardware/firmware behaviour from source and presents it as fact — cross-referenced from
`decisions.md`'s own closing paragraph, so a copy must survive somewhere reachable even if
shortened here). Decision 66's saturating-arithmetic evidence (the panic-in-debug/wrap-in-release
distinction and why the un-overflowing 4 GB case is the real hazard, not the overflow). Decision
67's splice example (`[0xA1, 0xA2]` / `[0xB1, 0xB2]` → `[0x00, 0xA1, 0xB1, 0xB2]`) and its
"declaration order, not offsets" correction — the two are easy to conflate and the test this
cites (`an_overlapping_registry_the_builder_never_validated_splices_two_values`) exists because
the conflated version was wrong. Decision 69's two-outcome mechanism (a `HashMap` keyed by
`field.name` collapsing two fields to one entry — the silent double-write vs. the misleading
`UnknownFieldChoice`) and its standalone-vs-amendment argument citing 66/67 as the precedent.

## What

`embarch-study-designer/decisions/registry.md` is 11,827 / 12,288 B — 461 B left, inside the
`max(1.2 KB, 10%)` reserve floor (`DOC-COMPACTION.md` §3). It now carries four decisions (35,
66, 67, 69) and has grown one rule at a time as `validate` grew a rule at a time; nothing in it
has been through a hot/cold pass yet (`DOC-COMPACTION-PASS.md`'s second pass). Bring it back
under reserve — the hot/cold split is the likely tool, per that doc's second pass, since this
file is one mission already (not a multi-mission split the way `crate.md`/`ci.md` was) and its
four entries are of a piece, not independent enough to move apart.

## Why now

Reserve reached mechanically, by `015`'s decision 69 entry — not urgent on its own terms
(§10's gate does not fail on it), but named per `tasks/README.md` rather than left for the next
unit that opens this file to rediscover.

## Done when

- [ ] `registry.md` is out of reserve (`scripts/check-doc-size.py` clean, no allowance taken).
- [ ] Every item in `Must not delete:` survives, in words a reader can still check.
- [ ] `DOC-COMPACTION-PASS.md`'s human question answered honestly: can `spec.md` alone answer
      what someone needs to work on this component today? (`spec.md` does not currently mention
      the registry at all — worth resolving explicitly rather than leaving implicit.)
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
