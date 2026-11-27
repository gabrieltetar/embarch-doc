# embarch-dev-bench decisions: The PD bench

**Status:** active, 2026-10-09.

The second app in this repo, which is a USB PD partner and not a BLE counterpart.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 48 — The PD bench is a second app that speaks a shell, not the dev-bench wire

**A USB PD DUT needs a partner on its cable, and the BLE bench cannot be one.** `pd-bench/` is a Zephyr USB-C sink for a NUCLEO-G0B1RE with an X-NUCLEO-SNK1M1. The host drives it line by line over its console shell with Core's signal exchange ([embarch-host-study-proposal.md](../../embarch-host-study-proposal.md), phase 1).

**It shares nothing with `app/` and does not speak the wire.** A sink has no `Study` to run, and a shell is enough for a host that sends one command and waits for one marker. Every `pd` command ends with `pd: ok` or `pd: error <reason>`. That marker means queued, never accepted, and the contract is read back with `pd status`. The command-by-command contract lives in [`pd-bench/README.md`](../../../embarch-dev-bench/pd-bench/README.md).

**It needs USB-C PD stack fixes that are not upstream yet**, and builds from `workspaces/pd-bench/`, which carries them (decision 58). A bug common to that stack and the DUT's passes unseen, which is why key results still need a third-party partner.

**It is enrolled as a bench board** ([`embarch-topology` decision 41](../../embarch-topology/decisions/enrollment.md)). That lets it be flashed by probe serial without taking `dev-bench` from the nRF54L15DK.

### 49 — Each expansion board is a Zephyr shield inside the app, and the DRP1M1 sources only what CN3 gives it

**The PD bench now runs on two boards: the X-NUCLEO-SNK1M1 (sink) and the X-NUCLEO-DRP1M1 (dual role, TCPP03-M20).** Each is a Zephyr shield under `pd-bench/boards/shields/`, and `-DSHIELD=` picks one; with none given the SNK1M1 builds, unchanged. The Nucleo overlay keeps only what both share (UCPD1 on PA8/PB15). A shield, not an overlay file per variant, because a board's pins, its devicetree nodes and its Kconfig (the DRP1M1 needs `CONFIG_USBC_CSM_DRP` and I2C) travel together.

**The DRP1M1 switches its CN3 supply onto VBUS as it is**, with no regulator, so the bench offers 5 V only (`source-pdos`, 5 V 3 A) and refuses to source unless CN3 reads vSafe5V. A source test above 5 V needs a different supply and a different `source-pdos`, not a command. The TCPP03 is driven over I2C from the app (`src/tcpp03.c`, binding `st,tcpp03`): the tree has no TCPP03 driver, and the bench needs only four control words. The provider and consumer paths are never closed together; a fault opens both and needs the recovery word.

**What the stack cannot do stays out of the shell:** it answers PR_Swap only with Accept or Reject (no Wait), has no Try.SRC or Try.SNK, and has no DPM request for Source_Info, Revision, Source_Cap_Extended, Manufacturer_Info or Battery_Cap.

### 58 — pd-bench builds from its own workspace: Zephyr v4.4.2 plus six carried USB-C patches

**`workspaces/pd-bench/` pins Zephyr v4.4.2 and applies six patches with `west patch`** (`manifest/zephyr/patches.yml`), so a clone of this repo alone builds both shields. v4.4.2 because every patch was written against it and applies there cleanly. It imports only `cmsis_6` and `hal_stm32`, and is named for the app, not a vendor family (decision 2), because its Zephyr is patched.

**The six, in apply order:** the PDO enum bitfield backport, the STM32 UCPD fixes (shared IRQ, prescaler shift, RX overrun), VCONN `-ENOTSUP`, the USB PD R3.2 stack patch (the one pd-bench cannot build without), UCPD Messages by DMA, and UCPD late TXMSGDISC. Each of the last two needs the UCPD patch before it.

**Four the source workspace carries are left out**, because pd-bench uses none: the two dead-battery backports (the Nucleo never boots from VBUS), the UDC shared-IRQ fix (no USB device stack) and the Discover Identity responder (no identity callback).

**A patch leaves when the pin moves to a release that contains it:** the backport after 8a87e3bde92d, the prescaler part of the UCPD fixes after 9719cc9cbe4f. Building from the workspace the patches came from, as decision 48 had it, left nobody else able to build pd-bench, the fleet included.

### 59 — pd-bench is checked by a build-only twister run and a native_sim test of its pure logic, never by running its stack

**`pd-bench/sample.yaml` builds both shields under twister, build only, and `pd-bench/tests/logic` runs a ztest suite on `native_sim` against `src/pd_logic.c`**: the PDO classifiers, the RDO builders, the `pd max` choice, a choice checked against the caps, the source's Request check and the `pd srccaps` rules. That file makes no shell, kernel or device call, which is what lets it run off-hardware. `main.c` keeps the locking, the stack callbacks and every line the shell prints.

**The USB-C stack does not run off-hardware**: Zephyr v4.4.2 has no TCPC emulator (`drivers/usb_c/tcpc/` holds fusb307, ps8xxx, rt1715, tcpci and two UCPD drivers), and writing one is out of scope. The build check is what catches a patch update or a pin move (decision 58) breaking the build. Neither check is in the fleet's gate (decision 9).

### 68 — `pd idle` puts the bench back to its boot state and `pd hello` names the build; `pd detach` stays out

**`pd idle` restores keep-alive on, `dr accept`, `pr accept`, `answer accept`, the `pd max` choice and the devicetree's Source_Capabilities, drops any contract, and on the DRP1M1 turns VBUS off and discharged through the existing `source_off` path** (a Hard Reset for a sink holding a contract, an ErrorRecovery for a source with a partner attached). It ends `pd: ok`, or `pd: error <what>` when VBUS did not discharge or the request was refused. The list of settings is `PdLogicIdle` in `pd_logic.c`, so the native_sim suite tests it; `main.c` applies it. The HIL design starts every test from a DUT reset plus this command (`notes/hil/03-test.md`).

**`pd hello` prints `pd-bench version <v> commit <c> shield <s>` and then `pd: ok`.** The commit is `git describe --always --dirty` taken by CMake at configure time, `unknown` outside a checkout.

**`pd detach` is not added.** A test could then ask for it as a precondition; the owner may strike this. **Not measured on a board**: the Hard Reset and ErrorRecovery choices are read from the stack, not observed.

### 69 — `pd times` reports PD events on the bench's own clock; extra `pd status` lines were not chosen

**Each PD event the stack reports to the app is stamped with the bench's uptime in microseconds** (`k_uptime_ticks()` converted by `k_ticks_to_us_near64`), because a host stamp through a USB serial bridge is not a sub-millisecond clock (`notes/hil/03-test.md`, "The verdict"). The events: attach (a new power-role start with no partner held), Source_Capabilities received, the Request the stack asked the app for (`policy_get_rdo`), Accept, PS_RDY (`TRANSITION_PS`), a Hard Reset requested of the stack, a Hard Reset received (`HARD_RESET_RECEIVED`, or `SNK_TRANSITION_TO_DEFAULT` not following one the bench sent) and keep-alive stopped (the first PPS keep-alive due and skipped under `pd keepalive off`, so it falls one keep-alive period after the last Request the source saw).

**`pd times` prints up to eight events, `event <name> <us>`, oldest first, then one `<name> <us>` line per interval, then `pd: ok`:** `attach_to_src_caps`, `request_to_ps_rdy`, `keepalive_stopped_to_hard_reset`. An interval runs from the last event of its start kind to the last of its end kind; a missing event, or a start later than its end (a new cycle whose end has not come), gives no line. `pd idle` clears the stamps, so a test starts from none. The arithmetic and the event list are `pd_logic.c`, tested on native_sim over scripted event lists; `main.c` takes the stamps.

**A new command, not extra `pd status` lines**, because `pd status` is read for state and a test parsing one interval should not match it among a dozen unrelated lines; the owner may strike `pd times` for them. **Not measured on a board:** where in the stack's callbacks each event is seen, so what an interval includes, the kernel tick's resolution, and how it compares with a probe on CC; the debt is in `tasks/dev-bench/053`.
