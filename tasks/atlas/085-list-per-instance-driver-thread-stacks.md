# 085 — `q stacks` lists a driver's per-instance thread stack

**State:** done, 2026-11-18
**Source:** Fleet Ready issue: `embarch-atlas q stacks` omits every thread stack a driver defines once per devicetree instance, so its count and noinit total are too low for any driver that owns a thread.
**Issue:** EMB-27
**Scope:** atlas
**Hardware:** none
**Owner:** no

## What

`stack_rows` in `src/embarch_atlas/footprint.py` keeps a symbol only if its section is `noinit` and its name matches `STACK_NAME` (`^_k_thread_stack_`, `stacks?$`, `stack_area`, `_stk$`). A driver that writes `K_THREAD_STACK_DEFINE(<driver>_stack_##inst, CONFIG_<DRIVER>_THREAD_STACK_SIZE)` inside its `*_INIT(inst)` macro, expanded by `DT_INST_FOREACH_STATUS_OKAY`, produces a symbol named `<driver>_stack_0` (then `_1`, ...). It lands in `noinit` and passes the section filter; the instance suffix makes the name fail every alternative of `STACK_NAME`, so the stack is dropped.

Reproduced by the owner on a real Zephyr build (current atlas main): two such stacks, 0x400 B each, `nm -l -S --defined-only` giving `B <driver>_stack_0  drivers/<driver>/<driver>.c:<line>` and `objdump -t` putting both in `noinit`; `q stacks` listed 14 stacks and neither of them.

Make `STACK_NAME` (or the filter) accept a stack name followed by a numeric instance suffix, so `demo_drv_stack_0` and `demo_drv_stack_1` in `noinit` are listed with their size, defining line and likely `*_STACK_SIZE` option, and count in the first line's total.

## Why now

The issue's reproduction supplies the real symbol shape the fleet could not see before.

## Dispatch notes

- The fixture is generic: add `demo_drv_stack_0` (and a `_1`) to the canned `nm` / `objdump` fixture in `tests/test_footprint.py`, in `noinit`, with a `CONFIG_DEMO_DRV_THREAD_STACK_SIZE` of the same size, and assert the rows and the total. No client driver name anywhere.
- Do not widen the match so far that a non-stack noinit symbol ending in a digit is taken; a test with one such symbol (a buffer named like `demo_rx_buf_0`) staying out is the guard.
- The option match is by size and name word; check that the instance suffix does not stop `_words` from pairing the stack with its `*_THREAD_STACK_SIZE` option, and say in the output's `how` what matched as before.
- No file of this sub-project is in reserve.

## Done when

- [x] A per-instance stack symbol (`<name>_stack_<N>` in `noinit`) appears in `stack_rows` and in `q stacks`, with its option matched as for any other stack.
- [x] The fixture in `tests/test_footprint.py` carries that symbol shape, and a non-stack noinit symbol with a numeric suffix stays out.
- [x] `q stacks`'s count and noinit total include the per-instance stacks.
- [x] Gate green (`../../embarch-fleet/gate.md`, the Python bullet); `DESIGN.md` updated if it lists the name patterns; `changelog.d/` fragment dropped.
