# 037 — Give pd-bench a twister build-only gate for both shields and a native_sim test of its pure logic

**State:** open
**Source:** field use on a USB PD charger board, 2026-09-09 to 2026-10-20 — eight pd-bench commits landed on `main` with no build anyone but their author could repeat; decision 9 records that nothing mechanical checks a change to this repo before it lands
**Scope:** dev-bench
**Hardware:** toolchain
**Owner:** no

## What

Once `workspaces/pd-bench/` exists (the pd-bench west manifest task, filed with this one), a change to `pd-bench/` gets a check that runs without a board.

**The build check.** A `pd-bench/sample.yaml` with two build-only scenarios on `nucleo_g0b1re`: `pd_bench.snk1m1`, and `pd_bench.drp1m1` with `extra_args: SHIELD=x_nucleo_drp1m1`. `west twister -T pd-bench -p nucleo_g0b1re` then builds both.

**The logic test.** A ztest suite on `native_sim` for the part of `main.c` that is pure: the RDO builders, the PDO classifiers, the `pd srccaps` parser and its rules, the `pd max` choice, and the source's Request check. Those move into their own file, and `main.c` calls them.

**Why the stack itself cannot run on `native_sim`.** Zephyr v4.4.2 has no TCPC emulator: `drivers/usb_c/tcpc/` holds only fusb307, ps8xxx, rt1715, tcpci and the two UCPD drivers. A run-time test of the stack needs one, and that is out of scope here. The task says so in `open.md` rather than leaving it as an implied gap.

## Why now

The patch set and the pin are about to change hands: they are leaving the client workspace for this repo. The first build after each patch update or pin move is the moment a silent break gets in. The build check was proven feasible on 2026-10-20: a scratch copy of `pd-bench/` with this `sample.yaml` built both scenarios under twister against v4.4.2 plus the six patches.

## Done when

- [ ] `pd-bench/sample.yaml` has the two scenarios with `build_only: true`, `platform_allow: nucleo_g0b1re` and `integration_platforms: [nucleo_g0b1re]`. `west twister -T pd-bench -p nucleo_g0b1re` from `workspaces/pd-bench/` reports 2 of 2 built.
- [ ] The fleet venv can run twister. Today it lacks Zephyr's `scripts/requirements-run-test.txt`: `natsort` is missing, so twister dies on import. Installing those requirements into `/home/gabriel/Github/embarch/.west-venv` is a change outside every repo, so ask the owner first and record that it was done. The same gap affects `app/tests` under the documented `west twister` line.
- [ ] The pure helpers live in `pd-bench/src/pd_logic.{c,h}`, with no shell, kernel or device calls. `main.c` calls them, and its behaviour is unchanged. Both shield builds still pass and the image sizes move by under 1 %.
- [ ] `pd-bench/tests/logic/` is a ztest suite on `native_sim` covering:
  - fixed and PPS RDO encoding;
  - `pd srccaps` accepting `5000:1500`;
  - refusing a first PDO that is not 5000 mV, a falling voltage, a voltage not in `source-pdos`, and a current above the devicetree's;
  - `pd max` capping at 3 A;
  - a Request above its PDO's current refused.

  It builds from `workspaces/pd-bench/` and passes.
- [ ] `pd-bench/README.md` gains a short "Tests" section with the two commands.
- [ ] `open.md` says the USB-C stack is not exercised off-hardware, because upstream has no TCPC emulator.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped.
