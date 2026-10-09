# embarch-dev-bench decisions: The PD bench

**Status:** active, 2026-10-09.

The second app in this repo, which is a USB PD partner and not a BLE counterpart.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 48 — The PD bench is a second app that speaks a shell, not the dev-bench wire

**A USB PD DUT needs a partner on its cable, and the BLE bench cannot be one.** `pd-bench/` is a Zephyr USB-C sink for a NUCLEO-G0B1RE with an X-NUCLEO-SNK1M1. The host drives it line by line over its console shell with Core's signal exchange ([embarch-host-study-proposal.md](../../embarch-host-study-proposal.md), phase 1).

**It shares nothing with `app/` and does not speak the wire.** A sink has no `Study` to run, and a shell is enough for a host that sends one command and waits for one marker. Every `pd` command ends with `pd: ok` or `pd: error <reason>`. That marker means queued, never accepted, and the contract is read back with `pd status`. The command-by-command contract lives in [`pd-bench/README.md`](../../../embarch-dev-bench/pd-bench/README.md).

**It builds outside `workspaces/`.** It needs the USB-C PD stack fixes that are not upstream yet, so it builds from a west workspace that carries them. A bug common to that stack and the DUT's passes unseen, which is why key results still need a third-party partner.

**It is enrolled as a bench board** ([`embarch-topology` decision 41](../../embarch-topology/decisions/enrollment.md)). That lets it be flashed by probe serial without taking `dev-bench` from the nRF54L15DK.
