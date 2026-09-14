# 044 — Compact `embarch-topology/spec.md` the last 70 bytes out of reserve

**State:** claimed by agent/topology/044-compact-topology, 2026-09-14 00:36
**Source:** `topology/043` (leg 112, 2026-09-13) compacted `spec.md` from 9,825 B to **9,110 B** and
hit the target its own `Done when` box named — *"under roughly 9,216 B, i.e. 90% of 10,240"*. **That
target was arithmetically wrong**, so the file is still in reserve by 70 bytes and
`check-doc-size.py` went red on the fold. See *Why the predecessor missed* below; the miss is not
the worker's and the sweep it did was clean.
**Scope:** topology
**Hardware:** none
**Owner:** no

## Dispatch note (leg 115)

**In reserve for `topology` right now** — exactly one file, and it is this task's own target:
`embarch-topology/spec.md` 9,110/10,240 B, **1,130 B left** against a 1,200 B floor. Nothing else in
`embarch-topology/` is in reserve, so a clean pass here empties this scope's ledger. **If your work
pushes some other doc file into reserve, or leaves one there that nothing has filed, file
`tasks/topology/<NNN>-compact-topology.md` in the same commit** (`tasks/README.md` has the shape;
`scripts/check-task-numbers.py --next topology` gives a safe number).

## What

`embarch-topology/spec.md` is **9,110 / 10,240 B with 1,130 B left**, and the reserve floor for this
file is **1,200 B**. Get it to **9,040 B or less** — 70 bytes, one sentence.

**Compacts:** embarch-topology/spec.md
**Size debt due:** 2026-09-20
**In flux:** no — unchanged from `043`: decisions 32 and 33 are closed on both sides of the
`embarch-core`/`embarch-topology` boundary, `core/055` has landed, and nothing about probe selection
is expected to move again soon.
**Must not delete:** everything `043`'s own list protected, which `043` did protect and a reviewer
confirmed — the *What each consumer owns now* probe-selection bullet's three-behaviour list (zero
probes / multi-probe / serial-miss), and the *Shape* section's consumer-call table. **Additionally,
do not undo `043`'s seven cuts**; they are recorded verbatim in commit `ad3f642`'s message and each
one was a restatement of a decision file's own reasoning. This task is the remaining 70 bytes, not a
second pass over the same ground.

## Why the predecessor missed, and the general trap

**Reserve is not 10% of the cap.** `check-doc-size.py` computes it as
`max(RESERVE_FLOOR, (100 - RESERVE_PCT)% of the limit)` with `RESERVE_PCT = 90.0` and
**`RESERVE_FLOOR = 1200`**. For a 10,240 B cap, 10% is 1,024 B — **below the floor**, so the floor
wins and the real line is 9,040 B, not 9,216 B. The floor exists because a percentage of a small cap
is not runway; it files debts earlier on purpose.

**So a `Done when` box that computes its own target from the percentage is wrong for every cap under
12,000 B**, which is most of this suite's files. `043`'s did, the worker met it exactly, and the
gate still went red. **Do not recompute the target here — run `python3 scripts/check-doc-size.py` and
believe it.** The general defect is filed for the owner as `tasks/doc/058`.

## Done when

- [ ] `python3 scripts/check-doc-size.py` exits 0 with `embarch-topology/spec.md` no longer listed —
      **that check, not an arithmetic target of your own.**
- [ ] Nothing on the `Must not delete:` list above is gone or reduced to a bare citation, and none of
      `043`'s seven cuts is restored.
- [ ] The compactor answers, in the commit message, `DOC-COMPACTION-PASS.md`'s question: can
      `spec.md` alone answer what someone needs to work on this component today?
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `changelog.d/` fragment.
