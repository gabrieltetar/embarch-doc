# 038 — The two probe-selection copies have already drifted; expose one as `pub` so `embarch-core` can stop keeping its own

**State:** open
**Source:** `inbox/core-resolve-probe-duplicates-topology-enroll-selection.md`, itself the follow-up
to `tasks/topology/037` and `embarch-topology` decision 32. Re-confirmed live against both files by
the leg of 2026-09-13 17:5x before filing, which is how the drift below was found — **the drop said
the copies were duplicated; they are duplicated *and already disagree*.**
**Scope:** topology
**Hardware:** none — a code-structure change and a decision. Nothing is attached, flashed or run.
**Owner:** no

## What

`embarch_topology::hardware::validate::enroll` (`src/hardware/validate.rs`, the selection block at
the top of the function) and `embarch-core::resolve_probe` (`embarch-core/src/hardware.rs`,
`pub(crate)`) are two independently maintained implementations of one rule: list every attached
probe, find-by-serial if one is given, else refuse unless exactly one is attached.

`enroll`'s own doc comment already says so, at length, and names the reason it was not fixed:

> **This block is a hand-copy of `embarch-core::resolve_probe` … not a call to it — decision 32.**
> … the dependency runs `embarch-topology` → `embarch-core`, not back, so this crate cannot call
> `embarch-core`'s copy, and the reverse (exposing this as `pub` for `embarch-core` to call) needs
> an edit inside `embarch-core` that is out of a topology-scoped change's reach.

**This task is the half that *is* in reach.** Expose the rule as a `pub` function here.
`embarch-core` adopting it is `tasks/core/055`, which is `blocked` on this landing.

## The drift is real, and reconciling it is the actual work

Do not treat this as a mechanical extraction. Three concrete behavioural differences exist **today**,
and a shared function has to choose on each. Verify all three yourself before you decide — this list
was read off the two sources, not inferred:

1. **Zero probes.** `resolve_probe` special-cases `probes.is_empty()` **first**, before the serial
   lookup, with a message naming the likely cause: *"no debug probe found — check the USB connection
   (and usbipd attach, if Core is on a Pi and the probe is elsewhere)"*. `enroll` has no empty case
   at all — with zero probes and a serial it says *"no attached probe with serial 'X' — is it still
   plugged in?"*, and with zero and no serial it falls through to *"enrollment requires exactly one
   debug probe attached (0 seen)"*. The usbipd hint is the one piece of genuinely diagnostic content
   in either copy and only one of them has it.
2. **The multi-probe predicate.** `resolve_probe` tests `probes.len() > 1` *after* the empty check;
   `enroll` tests `probes.len() != 1`. Equivalent only because of (1) — which is exactly the shape
   that stops being equivalent the moment one copy is edited.
3. **Every error string differs**, and `enroll`'s are enrolment-flavoured (*"plug in only the board
   you mean to enroll"*) where `resolve_probe`'s are operation-neutral. A shared function serving
   both callers cannot keep both wordings without a parameter.

This is `embarch-core` decision 9's own drift class restated one repo over: a rule described as
centralized quietly stops being that, and nothing fails until the copies disagree. There,
"single-probe-only" survived months until a real second probe exposed it. **Here the copies have
already disagreed and no test saw it**, which is the finding worth writing down.

## Shape

Expose the selection rule as a `pub` function in `embarch_topology::hardware` — name and signature
are yours, but two things to settle explicitly in the decision:

- **Does it list, or take a list?** Taking `&[DebugProbeInfo]` (or consuming a `Vec`) makes it
  testable without hardware, which is the difference between a rule that can have a unit test and
  one that cannot. Neither copy is testable today. Prefer the testable shape unless you can say why
  not.
- **How does a caller get its own error wording?** A context string, a caller-supplied noun, or
  simply one reconciled wording that both callers accept. Say which and why; "one wording" is a fine
  answer if you argue it, but say out loud that `enroll` loses *"plug in only the board you mean to
  enroll"* if it is.

Then make `enroll` call it, so this crate proves the extraction on its own caller before
`embarch-core` depends on it. **Keep `enroll`'s observable behaviour unchanged where you can**, and
where the reconciliation changes it, say so in the decision and the changelog fragment.

Add the unit test the testable shape buys: zero probes, one probe, two probes, serial-hit,
serial-miss. Five cases, no hardware.

## Docs

Write a numbered `embarch-topology` decision recording the reconciliation and the three divergences
it closed — derive the next free number with `scripts/check-decision-refs.py` / the sub-project's
`decisions.md` index, **never by eyeballing the highest number you can see**.

Then update, in this same unit:

- **`embarch-topology` decision 32**, which currently records the duplication as documentation. It
  is not superseded outright — `embarch-core` still holds its copy until `core/055` lands — so
  amend it with a dated note saying the topology half is done and naming `tasks/core/055` as the
  remaining half. Do not mark it closed.
- **`enroll`'s doc comment**, the long paragraph quoted above. Its *"this crate cannot call
  `embarch-core`'s copy"* sentence stays true; its *"exposing this as `pub` … is out of a
  topology-scoped change's reach"* sentence becomes **false the moment you land this**. Four
  consecutive units this week found a citation whose filename was repaired while the sentence
  around it had gone false; this is that sentence, and you are the one making it false.
- **`embarch-topology/open.md`**'s matching bullet.

## Reserve, for planning

**No `embarch-topology` doc is in reserve** — nothing of yours is in the pressure list, so you have
room. If your work pushes one into the last 10% of its cap or leaves one there unfiled, file
`tasks/topology/<next>-compact-topology.md` in the same commit — **your own scope**, never
`tasks/doc/`.

## Done when

- [ ] The selection rule is one `pub` function in `embarch-topology`, `enroll` calls it, and all
      three divergences above are reconciled with the choice argued in a numbered decision.
- [ ] Unit tests cover zero / one / two probes and serial-hit / serial-miss.
- [ ] Decision 32 amended (not closed), `enroll`'s doc comment corrected, `open.md` updated.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md` updated, `changelog.d/` fragment dropped.
