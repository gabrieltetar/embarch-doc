# 028 — `atlas build` does not reuse a build directory after its arguments change

**State:** claimed by agent/atlas/028-build-dir-follows-the-build-arguments, 2026-11-06 12:50
**Source:** a worker's finding, filed to Fleet Ready
**Issue:** EMB-54
**Scope:** atlas
**Hardware:** none — the directory key and the pristine flag are pure functions of the target config, testable without running west.
**Owner:** no

## What

The build directory is `.work/build-<target>-<commit12>` (`run_build`, `src/embarch_atlas/build.py`), keyed on target and commit only, and `west_command` passes `-p auto`. West's `-p auto` does not clear the directory when the change is between sysbuild and a plain build, so a target first built with `--sysbuild` and then rebuilt with `--no-sysbuild` at the same commit (with `--force`, since a built atlas is not rebuilt) fails in CMake with `The source .../CMakeLists.txt does not match the source .../share/sysbuild/CMakeLists.txt used to generate cache`, until the directory is deleted by hand.

When this is done, either the build directory (and its matching `logf`) is keyed on the build arguments as well as target and commit, or the build passes `-p always` when the arguments stamped on the previous run differ from this one's. The worker picks one and says why in a decision if the choice is not obvious from the code.

## Why now

A target's `extra_args` change is an ordinary edit, and the failure it causes reads as a broken toolchain rather than a stale cache.

## Done when

- [ ] Changing a target's `extra_args` between `--sysbuild` and `--no-sysbuild` and rebuilding at the same commit succeeds without a manual delete (unit test on the directory key or the pristine flag).
- [ ] A rebuild with unchanged arguments still reuses its build directory.
- [ ] Any doc that names the `.work/build-<target>-<commit12>` layout says the new key.
- [ ] Gate green (`../../../embarch-fleet/gate.md`, the Python bullet).
- [ ] `changelog.d/` fragment dropped.
