# Proposal: bootloading a DUT over MCUboot serial recovery

**Status:** proposal, 2026-09-30.

**A second way to put firmware on a DUT besides a probe's `POST /flash`: build, then hand the signed image to the DUT's own bootloader — MCUboot serial recovery over its USB CDC ACM port.** Spans four repos — `embarch-smp`, `embarch-topology`, `embarch-core` and `embarch-api` — which is why it sits at this repo's root ([DOC-PROTOCOL.md](DOC-PROTOCOL.md) §3).

## What is built

Every piece of the software path, each in its own sub-project's docs:

- **`embarch-smp`** — the SMP client and the simulated bootloader: [its spec](embarch-smp/spec.md), decisions 1–9.
- **`embarch-topology`** — the DUT's two declared USB identities: decision 36.
- **`embarch-core`** — `POST /bootload` and `/bootload/ports`: decisions 77, 78.
- **`embarch-api`** — `bootload`, `build_and_bootload`, the port tools and `[projects.bootload]`: decisions 80, 81.

## What is left

1. **Hardware validation on the first DUT, once it has MCUboot.** Replaces Core's placeholder timeouts with measured ones, and answers whether the uploaded image should be verified afterwards ([`embarch-core` open.md](embarch-core/open.md)).
2. **Then a UI button**, deliberately after the flow has run on hardware.

This file goes when item 1 lands and item 2 has an owner.
