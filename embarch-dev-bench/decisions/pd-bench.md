# embarch-dev-bench decisions: The PD bench

**Status:** active, 2026-10-09.

The second app in this repo, which is a USB PD partner and not a BLE counterpart.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 48 — The PD bench is a second app that speaks a shell, not the dev-bench wire

**A USB PD DUT needs a partner on its cable, and the BLE bench cannot be one.** `pd-bench/` is a Zephyr USB-C sink for a NUCLEO-G0B1RE with an X-NUCLEO-SNK1M1. The host drives it line by line over its console shell with Core's signal exchange ([embarch-host-study-proposal.md](../../embarch-host-study-proposal.md), phase 1).

**It shares nothing with `app/` and does not speak the wire.** A sink has no `Study` to run, and a shell is enough for a host that sends one command and waits for one marker. Every `pd` command ends with `pd: ok` or `pd: error <reason>`. That marker means queued, never accepted, and the contract is read back with `pd status`. The command-by-command contract lives in [`pd-bench/README.md`](../../../embarch-dev-bench/pd-bench/README.md).

**It builds outside `workspaces/`.** It needs the USB-C PD stack fixes that are not upstream yet, so it builds from a west workspace that carries them. A bug common to that stack and the DUT's passes unseen, which is why key results still need a third-party partner.

**It is enrolled as a bench board** ([`embarch-topology` decision 41](../../embarch-topology/decisions/enrollment.md)). That lets it be flashed by probe serial without taking `dev-bench` from the nRF54L15DK.

### 49 — Each expansion board is a Zephyr shield inside the app, and the DRP1M1 sources only what CN3 gives it

**The PD bench now runs on two boards: the X-NUCLEO-SNK1M1 (sink) and the X-NUCLEO-DRP1M1 (dual role, TCPP03-M20).** Each is a Zephyr shield under `pd-bench/boards/shields/`, and `-DSHIELD=` picks one; with none given the SNK1M1 builds, unchanged. The Nucleo overlay keeps only what both share (UCPD1 on PA8/PB15). A shield, not an overlay file per variant, because a board's pins, its devicetree nodes and its Kconfig (the DRP1M1 needs `CONFIG_USBC_CSM_DRP` and I2C) travel together.

**The DRP1M1 switches its CN3 supply onto VBUS as it is**, with no regulator, so the bench offers 5 V only (`source-pdos`, 5 V 3 A) and refuses to source unless CN3 reads vSafe5V. A source test above 5 V needs a different supply and a different `source-pdos`, not a command. The TCPP03 is driven over I2C from the app (`src/tcpp03.c`, binding `st,tcpp03`): the tree has no TCPP03 driver, and the bench needs only four control words. The provider and consumer paths are never closed together; a fault opens both and needs the recovery word.

**What the stack cannot do stays out of the shell:** it answers PR_Swap only with Accept or Reject (no Wait), has no Try.SRC or Try.SNK, and has no DPM request for Source_Info, Revision, Source_Cap_Extended, Manufacturer_Info or Battery_Cap.

