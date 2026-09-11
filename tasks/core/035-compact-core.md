# 035 — Compact embarch-core/decisions/flashing.md

**State:** blocked — `In flux: yes`, so nothing here is dispatchable yet.
**Size debt due:** 2026-09-24 (two weeks out; re-check `flash_backend.rs`'s
churn rate then and either compact or extend).
**Source:** `scripts/check-doc-size.py`, run by task `core/017` (2026-09-10):
`embarch-core/decisions/flashing.md` at 11487/12288 B (93.5%, 801 B left), no
debt filed.
**Scope:** core
**Hardware:** none
**Owner:** no

## What

**Compacts:** `embarch-core/decisions/flashing.md`

Shorten `decisions/flashing.md` (`DOC-COMPACTION.md`/`DOC-COMPACTION-PASS.md`)
without deleting a decision number or a distinct finding. The file grew past
90% of its reserve when decision 54 (retiring `Backend::NrfJprog`) landed.

**In flux:** yes. `flash_backend.rs` has had three decisions land in as many
weeks (49, 52, 54) and the vendor-tool discovery path is still where real
hardware surprises keep showing up (WSL PATH bleed, extensionless artifacts,
now a whole unused backend). Whoever compacts this should expect it to still
be moving and should not assume the current set of decisions is final.

**Must not delete:** decision 32's causal-evidence framing (bricked board,
four-for-four correlation, no invented mechanism); decision 36's
licensing/no-bundling rationale; decision 49's nRF54H refusal-vs-topology
distinction; decision 52's dead-arm-removal reasoning; decision 54's
"nothing recorded ever selected it" evidence trail.

## Why now

`check-doc-size.py` names this file with no filed debt; per protocol §5 item 5,
that failure must be filed rather than left silent.

## Done when

- [ ] `embarch-core/decisions/flashing.md` back under reserve (under 90% of
      12288 B), same decision numbers still resolving.
- [ ] `scripts/check-doc-size.py` clean.
- [ ] Gate green.
