# 027 — Three values the outpost's Kconfig accepts break the promise their option exists for

**State:** open
**Source:** DeepSeek V4 Pro review 2026-10-25 (embarch-outpost findings 1, 3 and 6), verified by Opus against embarch-outpost@2968f0c1
**Scope:** outpost
**Hardware:** toolchain — reclassified from `none` by the supervisor at filing (2026-10-26): every Done-when item is a `native_sim` or minimum-range build, and the Zephyr tree it needs is one no worktree carries and this suite has never used for outpost. As drafted: all three reproduce on `native_sim` or at configure time; the scheduling rule behind the first is the kernel's, not a SoC's. `tests/run-all.sh` needs `WEST=/home/gabriel/Github/embarch/.west-venv/bin/west` and a `ZEPHYR_BASE` (a Zephyr 4.4 tree with `native_sim`; the dev-bench `native_sim` workspace's `zephyr/` is one, not yet used for this suite).
**Owner:** no

## What

Three settings that stay inside their Kconfig range defeat the guarantee they exist for, and nothing says so:

1. **`EMBARCH_OUTPOST_OVERFLOW_BLOCK=y` livelocks instead of blocking.** When the ring is full, a thread-context producer loops on `k_yield()` (`src/outpost_ring.c:193-196`). `k_yield()` gives the CPU only to a thread of the same or higher priority. The drain thread runs at priority 10 (`Kconfig:59-64`), below `main` (0) and below most application threads. A producer like that, emitting into a full ring, spins forever, and the drain thread that would make room never runs. The guard (`!k_is_in_isr() && !k_is_pre_kernel()`) also lets irq-locked callers and the idle thread through, and Zephyr's own `k_can_yield()` excludes both.
2. **`EMBARCH_OUTPOST_RING_BYTES` from 256 to 319 allocates 320 bytes.** The slot count falls through to the `#else` value of 16 (`src/outpost_ring.c:54,74-76`), and 16 slots × 20 B is 320 B. The Kconfig help promises "rounded down" (`Kconfig:43-52`). `test_ring_is_a_power_of_two_of_slots` would catch it, but only runs at 512.
3. **The marker-list hash is the part of the build ID that truncation removes.** `CMakeLists.txt:113-114` builds `<app describe>+op<module describe>+m<hash>` and then cuts the tail to `BUILD_ID_MAX` (range 16..128). This repo has no tags, so its own describe is 7 to 13 characters. At the default 64, the hash starts losing characters once the app's describe passes about 40 characters, and is gone entirely past about 50. Any `BUILD_ID_MAX` near its minimum loses it outright. The hash is the one component that changes when a marker is renamed in a dirty tree, which is decision 9's verification half.

When done, each of the three either keeps its promise at every value its range allows, or is refused at configure or build time. For (1), the worker chooses between a wait the drain thread can actually end (still dropping where waiting is impossible) and removing the mode, and records why. For (3), any composition that keeps the hash will do, or a build-time refusal that names the cause.

## Why now

(1) contradicts the docs in both directions. `spec.md:59` and decision 5's title (`decisions/transport.md`) say overflow never blocks, while `interfaces/integration.md:29` offers blocking as an opt-in "for a deliberate high-fidelity run". That is the run where a hang costs the most. (2) is the same budget overshoot that the `OUTPOST_SLOT_BYTES` BUILD_ASSERT (`src/outpost_priv.h:203-233`) was restored to stop, still alive at the bottom of the range. (3) weakens decision 9 (`decisions/manifest.md`) without a word, and `integration.md:34` still marks `BUILD_ID_MAX` as `[assumed]`.

## Done when

- [ ] A native_sim test with `OVERFLOW_BLOCK=y`: a thread at a priority numerically below the drain thread's emits into a full ring and returns in bounded time with its record in the ring. If the mode is removed instead, its header flag bit is documented as retired in `interfaces/wire.md`.
- [ ] `spec.md`, decision 5 and `interfaces/integration.md` agree on whether the module can block, and on which contexts still drop.
- [ ] No value in `RING_BYTES`' range gives `slots × OUTPOST_SLOT_BYTES > CONFIG_EMBARCH_OUTPOST_RING_BYTES`, and a build at the range minimum proves it.
- [ ] With both describes 60 characters long and `BUILD_ID_MAX` at its range minimum, two marker lists that differ in one name produce different build IDs, or the build fails and says why.
- [ ] `tests/run-all.sh` passes every leg.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/` fragment for anything suite-level it made false.
