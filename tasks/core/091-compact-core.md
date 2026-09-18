# 091 — Compact embarch-core/decisions/surfaces.md

**State:** blocked — `In flux: yes`, so nothing here is dispatchable yet.
**Size debt due:** 2026-10-01 (two weeks out; re-check landing rate then and
either compact or extend).
**Source:** `scripts/check-doc-size.py`, run by task `core/088` (2026-09-17):
`embarch-core/decisions/surfaces.md` at 11579/12288 B (94.2%, 709 B left)
after decision 68 landed. No debt was filed before this; decision 67
(`core/078`) left only 163 B of headroom and decision 68 spent all of it.
**Scope:** core
**Hardware:** none
**Owner:** no

## What

**Compacts:** `embarch-core/decisions/surfaces.md`

Shorten `decisions/surfaces.md` (`DOC-COMPACTION.md`/`DOC-COMPACTION-PASS.md`)
without deleting a decision number or a distinct finding.

**In flux: yes.** This file has taken four edits in one calendar day
(2026-09-17): decision 59's completeness premise corrected (`core/074`),
decision 59's second amendment (`core/077`), decision 67 filed (`core/078`),
and now decision 68 (`core/088`). Whatever else touches `/status`,
`POST /validate`'s `TopologyMismatch`, or decision 12's deferred error body is
likely to land here again rather than somewhere quieter.

**Must not delete:** decision 13's "described as shipped for months when none
were" history and its warn-not-refuse posture; decision 67's rejection of a
git SHA and a build timestamp as candidates, and its "filed rather than
built" split from decision 68; decision 68's shape (`full 64-char lowercase
hex, not truncated`), its dependency finding (`sha2` already resolved
transitively via `probe-rs` → `espflash` at `0.11.0`, not a second hashing
crate), and its `null`-on-read-failure answer; decision 12's cross-repo
`code`-enum trigger; decision 55's "never a real member" retirement; decision
59's `kind` split, its two 2026-09-17 corrections (the probe-open-failure gap
and its `"not_attached"` resolution), and the `embarch-api` inbox drop it
names.

## Why now

`check-doc-size.py` names this file with no filed debt after `core/088`; per
protocol §5 item 5, that failure must be filed rather than left silent.

## Done when

- [ ] `embarch-core/decisions/surfaces.md` back under reserve (under 90% of
      12288 B), same decision numbers still resolving.
- [ ] `scripts/check-doc-size.py` clean.
- [ ] Gate green.
