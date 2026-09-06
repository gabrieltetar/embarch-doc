# Confirm the nRF54L15 hardware-ID register address against real silicon

**State:** open
**Source:** `embarch-core/open.md` — "The nRF54L15 hardware-ID register address, and the end-to-end validation of the moved identity gate… Relocating the code changed nothing about whether that address is confirmed against real silicon."
**Scope:** topology
**Hardware:** bench
**Owner:** no

## Roles this needs

`dut` and `dev-bench` — **both are nRF54L15**, which is what makes this answerable today.
Validate both before starting; if either is unattached, leave this `open`.

## Bench facts — owner-supplied, do not infer

- Both boards are nRF54L15. `dut` = probe `000852006107`, hardware ID `834f2559f10a6cdf`.
  `dev-bench` = probe `001057729826`, hardware ID `6fcddc36cb781b71`.
- Those two IDs were read live on 2026-09-06 and are **different**, which is the property
  the gate depends on. Do not assume they stay stable across a re-enrol.
- **Read-only.** Nothing here flashes or resets anything.

## What

The address `hardware_id.rs` reads for the nRF54L15 family — `FICR.INFO.DEVICEID`, not the
classic `0x1000_0060` pair — is confirmed by an actual readback rather than by construction,
and `open.md` stops carrying it as unconfirmed. The end-to-end identity gate is exercised in
both directions: a matching board passes, and a **role pointed at the other probe** is
refused by name with both IDs in the message.

Record what was read, marked `[measured 2026-09-06]` per `../../DOC-CONVENTIONS.md`.

## Why now

Two nRF54L15 boards are attached at once, with distinct hardware IDs — the exact
configuration this question needs and the reason it has stayed open. It is read-only, so it
is the cheapest bench unit available.

## Done when

- [ ] The register pair `read` selects for nRF54L15 is confirmed against a live readback on
      both boards, and the value recorded with its provenance.
- [ ] The identity gate is shown to **refuse** a deliberate role/probe mismatch, naming both
      the recorded and the live ID — verified without re-enrolling anything.
- [ ] **Nothing is re-enrolled.** If a mismatch appears that was not deliberately induced,
      stop and alert; re-enrolment is the owner's.
- [ ] `embarch-core/open.md`'s bullet and `embarch-topology/open.md` are updated to what is
      now confirmed and what is still not.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false.
