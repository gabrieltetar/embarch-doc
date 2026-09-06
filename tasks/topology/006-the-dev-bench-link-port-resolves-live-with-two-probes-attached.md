# Resolve the dev-bench link port live, with two probes attached and `guessed_among` visible

**State:** open
**Source:** owner's bench session 2026-09-06 — decision 20's `guessed_among` exists because "the guess used to be invisible", and two probes attached is the case that exercises it
**Scope:** topology
**Hardware:** bench
**Owner:** no

## Roles this needs

`dev-bench` (and `dut` attached, which is the point — it is what makes detection ambiguous).
Validate both first; if either is unattached, leave this `open`.

## Bench facts — owner-supplied, do not infer

- Dev bench: **nRF54L15DK**. Its link is **COM17 / VCOM1, interface 2** — the *higher*
  interface, not the lowest. It is enrolled with `link_port_interface=2`, and that value is
  there because this DK exposes two VCOMs and the lowest one is the wrong one.
- `dev-bench` = probe `001057729826`; `dut` = probe `000852006107`.
- This is exactly the ambiguity decision 20 was written for: a bench that "flashed, booted,
  ran, and timed out" because a guessed port was reported as a determination.
- **Read-only.** No flash, no study, and **nothing is re-enrolled** — a declared
  `link_port_interface` that no longer matches is a finding, not something to fix here.

## What

The dev-bench link port is resolved live with both probes attached, and the resolution is
recorded: which port, by which rule (`detected_by`), and **whether `guessed_among` was set**.
With two probes present this is the configuration where a guess is most likely, so it is the
one that tells you whether the declared `link_port_interface=2` is doing real work or whether
detection would have landed there anyway.

There is a companion host-side task to make the CLI *print* `guessed_among`; this one is
about what the value actually is on this bench. If the CLI does not surface it, read it from
the API and say so.

## Why now

Two probes are attached — the ambiguous case — and the boards will be unplugged. The declared
interface is a hand-supplied fact that nothing has re-checked since it was recorded.

## Done when

- [ ] The resolved port, its `detected_by` provenance, and `guessed_among` are all recorded
      with provenance per `../../DOC-CONVENTIONS.md`.
- [ ] Whether `link_port_interface=2` was load-bearing on this bench is stated plainly —
      i.e. what detection would have chosen without it.
- [ ] **Nothing is re-enrolled and no declared fact is edited.** A mismatch is reported.
- [ ] `embarch-topology/open.md` records what is now observed.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false.
