# 122 — zephyr-west discovery drops every single-SoC board whose devicetree is `<board>.dts`

**State:** open
**Source:** field use on a USB PD charger board, 2026-09-09 to 2026-10-20 — `list-targets` on the field repo with `discovery = "zephyr-west"` still answers `success: true, targets: []` (re-run 2026-10-20 on api `f82f8b6`), so the project never left `static`: 471 raw `west build` calls (about 3.0 h) went around EmbArch, against 26 EmbArch builds
**Scope:** api
**Hardware:** none
**Owner:** no

## What

`push_targets_for_soc` keeps a (SoC, cluster, variant) candidate only when `dts_exists` finds `<board>_<soc>[_<cluster>][_<variant>].dts` (`embarch-api/crates/embarch-firmware-build/src/zephyr.rs:359`, `:397`). Zephyr also accepts the shortened `<board>.dts` for a board that declares one SoC (`zephyr/cmake/modules/dts.cmake:138-150`, the `BOARD_${BOARD}_SINGLE_SOC` branch), and most single-SoC boards use it, every ST Nucleo upstream included (`boards/st/nucleo_g0b1re/nucleo_g0b1re.dts`). Both boards in the field repo use it, so every candidate is dropped, `scan` returns `Ok(vec![])`, and `list_targets` reports success with an empty list and no reason. `revision_is_backed` (`zephyr.rs:462-494`) builds the same long stem for revision-suffixed `.overlay`/`.defconfig` files, so a single-SoC board with revisions would lose its revisions the same way. Accept the shortened stem wherever the long one is checked, for a `board.yml` with exactly one SoC, and refuse it for a multi-SoC board the way Zephyr does. Then make "boards found, every candidate dropped" an answer that names each board and the file it looked for, the way decision 63 separated `NoAppDir` from "found no apps".

## Why now

Decision 63 (`d6fec7a`, 2026-09-09) fixed the `apps/` half of this silent empty result on the day the field project reported it, but the board half kept the list empty, so the project stayed on five hand-copied `static` blocks and built every variant by hand: 90 raw builds with `EXTRA_CONF_FILE`, 93 with `ZEPHYR_MODULES`, each then flashed with `--firmware-path` (91 flashes). `extra_args` on a zephyr-west project would have carried all of them.

## Done when

- [ ] A `board.yml` with one SoC and only `<board>.dts` yields its targets, built with `-b <board>/<soc>`; a fixture copies the layout of an upstream single-SoC board (`<board>.dts`, `<board>_defconfig`, `board.yml` with one `socs` entry and no `variants`).
- [ ] A `board.yml` with two or more SoCs and a shortened `<board>.dts` yields no target from that file and says why, matching Zephyr's own `FATAL_ERROR`.
- [ ] A board directory holding both `<board>.dts` and `<board>_<soc>.dts` is refused by name, matching Zephyr's "conflicting file names" error.
- [ ] `revision_is_backed` also checks the shortened revision files Zephyr accepts for a single-SoC board, with a fixture.
- [ ] `list_targets` on a repo whose boards are all dropped returns a per-board reason or an error, never `success: true` with a bare `targets: []`.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped.
