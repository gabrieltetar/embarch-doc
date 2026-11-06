# 027 — `atlas build` picks the application image of a multi-image sysbuild

**State:** claimed by agent/atlas/027-build-picks-the-app-image-of-a-multi-image-sysbuild, 2026-11-06 12:30
**Source:** a worker's finding, filed to Fleet Ready
**Issue:** EMB-49
**Scope:** atlas
**Hardware:** none — the image choice is a function of the build directory's layout and its `domains.yaml`, testable on a synthetic build tree; no west run is needed.
**Owner:** no

## What

`embarch-atlas build` fails after a good west build when the target is a sysbuild with more than one image, such as an application plus MCUboot. The west build writes `<build>/<app>/zephyr/edt.pickle` and `<build>/mcuboot/zephyr/edt.pickle`; `run_build` (`src/embarch_atlas/build.py`) looks for `<build>/zephyr/edt.pickle`, then globs `<build>/*/zephyr/edt.pickle` and requires exactly one match, so with two images it raises `no zephyr/edt.pickle under <build>` and writes no atlas.

When this is done, the build picks the application image — from the sysbuild `domains.yaml`, whose `default:` names it, or failing that from the target's app directory name — and pins the atlas to that image. Recording the other images (the bootloader's devicetree and pins) as secondary is optional. When no image can be chosen, the error names the pickles it found instead of saying the file is missing. `src/embarch_atlas/kconfig.py`'s docstring on the directory holding `.config` and `edt.pickle` (`<bdir>/<app>/zephyr` under sysbuild) needs the same image choice, so the two never disagree on which image an atlas describes.

## Why now

Sysbuild with MCUboot is the usual nRF Connect SDK and Zephyr product build. The only workarounds are `--no-sysbuild` or disabling the bootloader, and both pin the atlas to a build the product does not ship.

## Done when

- [ ] `embarch-atlas build` on a two-image sysbuild target writes an atlas pinned to the application image (unit test on a synthetic build tree with `domains.yaml` and two pickles).
- [ ] A single-image build, sysbuild or not, builds as before.
- [ ] When no image can be chosen, the error names the pickles it found.
- [ ] `kconfig.py` reads `.config` from the same image the build chose.
- [ ] `DESIGN.md` and `embarch-doc/embarch-atlas/design.md` say how the image is chosen, where they describe the build directory.
- [ ] Gate green (`../../../embarch-fleet/gate.md`, the Python bullet).
- [ ] `changelog.d/` fragment dropped.
