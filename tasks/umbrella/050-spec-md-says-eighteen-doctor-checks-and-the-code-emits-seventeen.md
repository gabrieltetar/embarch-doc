# 050 — `spec.md` says eighteen `doctor` checks; the code emits seventeen

**State:** open
**Source:** refill sweep, leg 088, 2026-09-11. `embarch-umbrella/spec.md` against
`embarch-umbrella/src/doctor.rs` and `embarch-umbrella/interfaces/doctor-chain.md`.
**Scope:** umbrella
**Hardware:** none.
**Owner:** no

## What

`embarch-umbrella/spec.md:64` says *"An ordered chain of eighteen checks; each emits pass/warn/fail
plus a concrete fix line."* The driver in `src/doctor.rs:3367-3370` builds `vec![check1 … check17]`
and stops there; there is no check 18 anywhere in `doctor.rs`.

**`interfaces/doctor-chain.md` already has this right** — it says outright that *"1-17 are what the
code emits; 18 is designed and unbuilt"* — so this is one file in the sub-project disagreeing with
another, and the one that is wrong is the file a reader is sent to first. The clause *"each emits
pass/warn/fail plus a concrete fix line"* is what makes it costly rather than cosmetic: it makes the
unbuilt check read as shipping.

## What to do

Correct `spec.md` to the number the code emits, and say in the same sentence that an eighteenth is
designed and unbuilt, pointing at `interfaces/doctor-chain.md` rather than restating its content.
**Count the vector yourself rather than trusting either doc or this task** — a doc that is wrong
about a count is exactly the thing not to take a count from, and the point of the fix is that the
number came from the source.

**Then check the rest of `spec.md`'s `doctor` paragraph against the chain.** A count that drifted is
rarely the only thing that did; report anything further in this task file rather than widening the
diff silently.

## Why now

`spec.md` is the file that claims to be current truth about the sub-project, and the wrong half of
this pair is the one a newcomer reads. Nothing catches a doc-versus-code count: `umbrella/037` and
`core/042` were both this shape, and `core/042` found a stale count that had survived the very
retirement that should have updated it.

## Done when

- [ ] `spec.md`'s check count matches what `src/doctor.rs`'s driver actually builds, verified by
      reading the vector.
- [ ] The unbuilt eighteenth is named as unbuilt, with the pointer to `interfaces/doctor-chain.md`.
- [ ] Any further drift found in the same paragraph is fixed or named here.
- [ ] No code changes — this is a documentation correction. If the code turns out to disagree with
      `interfaces/doctor-chain.md` too, stop and say so here rather than widening the unit.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10). `changelog.d/` fragment.
