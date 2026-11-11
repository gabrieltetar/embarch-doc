# 037 — Give pd-bench a twister build-only gate for both shields and a native_sim test of its pure logic

**State:** done — agent/dev-bench/037-pd-bench-build-gate in embarch-dev-bench and embarch-doc, branched from agent/dev-bench/036-pd-bench-own-west-manifest and landing after it; both twister passes green 2026-11-10
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

- [x] `pd-bench/sample.yaml` has the two scenarios with `build_only: true`, `platform_allow: nucleo_g0b1re` and `integration_platforms: [nucleo_g0b1re]`. `west twister -T pd-bench -p nucleo_g0b1re` from `workspaces/pd-bench/` reports 2 of 2 built.
- [ ] The fleet venv can run twister. Today it lacks Zephyr's `scripts/requirements-run-test.txt`: `natsort` is missing, so twister dies on import. Installing those requirements into `/home/gabriel/Github/embarch/.west-venv` is a change outside every repo, so ask the owner first and record that it was done. The same gap affects `app/tests` under the documented `west twister` line.
- [x] The pure helpers live in `pd-bench/src/pd_logic.{c,h}`, with no shell, kernel or device calls. `main.c` calls them, and its behaviour is unchanged. Both shield builds still pass and the image sizes move by under 1 %.
- [x] `pd-bench/tests/logic/` is a ztest suite on `native_sim` covering:
  - fixed and PPS RDO encoding;
  - `pd srccaps` accepting `5000:1500`;
  - refusing a first PDO that is not 5000 mV, a falling voltage, a voltage not in `source-pdos`, and a current above the devicetree's;
  - `pd max` capping at 3 A;
  - a Request above its PDO's current refused.

  It builds from `workspaces/pd-bench/` and passes.
- [x] `pd-bench/README.md` gains a short "Tests" section with the two commands.
- [x] `open.md` says the USB-C stack is not exercised off-hardware, because upstream has no TCPC emulator.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped.

## Twister

**2026-11-10, third run: both passes green.** The owner's session installed Zephyr's `scripts/requirements-run-test.txt` and `scripts/requirements-build-test.txt` into the fleet venv (`/home/gabriel/Github/embarch/.west-venv`); this worker installed nothing. From `workspaces/pd-bench/` in this branch's worktree:

- `west twister -T pd-bench -p nucleo_g0b1re`: 3 scenarios selected, 1 filtered (`pd_bench.logic`, by its `platform_allow`), 2 built (not run), 0 failed, "with no warnings".
- `west twister -T pd-bench/tests/logic -p native_sim`: 1 of 1 configuration passed, 13 of 13 test cases passed, "with no warnings".

**2026-11-10, second run: twister is still red, now on `junitparser`.** The owner's session installed `scripts/requirements-run-test.txt` into the fleet venv, and `natsort` and `tabulate` now import. Both passes were then run from `workspaces/pd-bench/` in this branch's worktree, and both died on import before building anything: `west twister -T pd-bench -p nucleo_g0b1re` and `west twister -T pd-bench/tests/logic -p native_sim` each end in `ModuleNotFoundError: No module named 'junitparser'`, raised by `scripts/pylib/twister/twisterlib/harness.py` line 21, whose line 23 imports `pytest` too. Both come from Zephyr's `scripts/requirements-build-test.txt` (colorama, ply, gcovr, coverage, pytest, mypy, junitparser, python-dotenv). The fleet venv lacks junitparser, pytest, mypy, gcovr and coverage from that file, so twister needs it as well as the run-test file. Nothing was installed by this worker. After that install, the same two commands finish the task.

**First run, before the run-test install:** the fleet venv (`/home/gabriel/Github/embarch/.west-venv`) lacks `natsort` and `tabulate` from Zephyr's `scripts/requirements-run-test.txt`, so `west twister` dies on import. This task says to ask the owner before installing them, and this worker had no owner to ask, so nothing was installed and no other venv was borrowed. The first two `Done when` boxes stay open. Once the owner says yes, the remainder takes about 5 minutes, from `workspaces/pd-bench/` in a checkout of this branch: install the requirements, run `west twister -T pd-bench -p nucleo_g0b1re` (expect 2 of 2 built, the `native_sim` suite filtered out) and `west twister -T pd-bench/tests/logic -p native_sim`, then tick both boxes and set `done`.

What stood in for twister before the third run, measured 2026-11-10 from a fresh `west init -l manifest && west update && west patch apply` in the branch worktree's `workspaces/pd-bench/`:

- Both `sample.yaml` and `tests/logic/testcase.yaml` validate against twister's own `testsuite-schema.yaml`, loaded through `scripts/pylib/twister/scl.py`.
- `west build` of both scenarios with `-DCONFIG_COMPILER_WARNINGS_AS_ERRORS=y`, the setting twister builds with by default: both pass, 0 warnings.
- `west build -b native_sim -s pd-bench/tests/logic`, then `zephyr.exe`: 13 of 13 pass.

## What shipped (2026-11-10)

- **embarch-dev-bench** `agent/dev-bench/037-pd-bench-build-gate`, one commit on top of 036's: `pd-bench/src/pd_logic.{c,h}`, `main.c` calling them, `pd-bench/sample.yaml`, `pd-bench/tests/logic/`, and a "Tests" section in `pd-bench/README.md`.
- **What moved:** the PDO classifiers, the fixed and PPS RDO builders, `pd max`, the choice check against the caps, the source's Request check, the shell's number parser and the `pd srccaps` rules. `main.c` prints every message as before: a refused `pd srccaps` PDO comes back as a reason code, and `main.c` turns it into the same text. The public names are PascalCase (`PdLogicRdoFixed`), per the owner's Zephyr rules, although `tcpp03.h` and `app/` use snake_case. The moved literals got names in `pd_logic.h`.
- **Sizes against 036's builds:** SNK1M1 128,736 B to 128,856 B flash (+0.09 %), DRP1M1 148,252 B to 148,904 B (+0.44 %), RAM unchanged. `CONFIG_USBC_TCPC_STM32_DMA=y` in both.
- **The suite, 13 tests:** fixed and PPS RDO encoding, checked against the USB PD R3.2 field layout rather than the unions; the classifiers; `pd max` capping at 3 A and breaking ties to the lower voltage; a choice checked against the caps; a Request above its PDO's current refused; `pd srccaps` accepting `5000:1500` and refusing a first PDO not at 5000 mV, a falling voltage, a voltage not in `source-pdos`, a current above the devicetree's, and malformed text.
- **Found: the carried R3.2 patch's `usbc_pd.h` is not self-contained.** It adds `__packed` structs without `#include <zephyr/toolchain.h>`. The ARM builds never saw it, because other includes come first, but `pd_logic.c` alone on `native_sim` failed to compile on it. `pd_logic.h` includes `toolchain.h` first, with a comment. Fixing the patch itself waits on the owner's "which copy leads" question (`open.md`).
- Decision 59, `spec.md` §2, the `open.md` bullet and a changelog fragment. The 036 `open.md` bullet on the carried patches was shortened to keep the file out of its reserve.
- **Gate:** `check-docs.py` 12 of 12 green on the doc branch; `check-client-names.py --repo` and `check-ownership.py --scope dev-bench --code-repo` green on the code branch.
