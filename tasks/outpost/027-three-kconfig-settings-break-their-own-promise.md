# 027 — Three values the outpost's Kconfig accepts break the promise their option exists for

**State:** done 0
**Source:** DeepSeek V4 Pro review 2026-10-25 (embarch-outpost findings 1, 3 and 6), verified by Opus against embarch-outpost@2968f0c1
**Scope:** outpost
**Hardware:** none — reclassified back from `toolchain` by the supervisor on 2026-11-10, which is `tasks/README.md`'s rule for this repo: `tests/run-all.sh` ran every leg green (unit 6/6 and 9/9, module-off, the end-to-end stream) from a bare `git archive` copy of `main`, with only `WEST=/home/gabriel/Github/embarch/.west-venv/bin/west`, `ZEPHYR_BASE=/home/gabriel/Github/embarch/embarch-dev-bench/workspaces/native_sim/zephyr` (Zephyr 4.4.0, only read) and `/home/gabriel/Github/embarch/.west-venv/bin` prepended to `PATH`. Builds land in `tests/build/`, inside the worktree; the Zephyr tree stayed clean.
**Owner:** no

**Dispatch note (2026-11-10):** `embarch-outpost/spec.md` is in reserve (9,126 of 10,240 B, out of reserve at 9,039 B), and its compaction (`tasks/outpost/028`) is parked partly on this task. Edit `spec.md` only as far as this task needs, and compact it in the same unit if you can without touching the wire section that `open.md`'s layout-4 change will move; keep 028's `Must not delete:` items (the manifest-refusal and unverified-join bullets in §3 with their decision pointers 9, 18, 24, 27, and the measured 1.6% vs 78.1% overhead figures in §4). Decision 9 (`decisions/manifest.md`) has 27 B left before its per-decision limit: if (3) needs it to say more, put the new rule in a new decision that cites 9.

## What

Three settings that stay inside their Kconfig range defeat the guarantee they exist for, and nothing says so:

1. **`EMBARCH_OUTPOST_OVERFLOW_BLOCK=y` livelocks instead of blocking.** When the ring is full, a thread-context producer loops on `k_yield()` (`src/outpost_ring.c:193-196`). `k_yield()` gives the CPU only to a thread of the same or higher priority. The drain thread runs at priority 10 (`Kconfig:59-64`), below `main` (0) and below most application threads. A producer like that, emitting into a full ring, spins forever, and the drain thread that would make room never runs. The guard (`!k_is_in_isr() && !k_is_pre_kernel()`) also lets irq-locked callers and the idle thread through, and Zephyr's own `k_can_yield()` excludes both.
2. **`EMBARCH_OUTPOST_RING_BYTES` from 256 to 319 allocates 320 bytes.** The slot count falls through to the `#else` value of 16 (`src/outpost_ring.c:54,74-76`), and 16 slots × 20 B is 320 B. The Kconfig help promises "rounded down" (`Kconfig:43-52`). `test_ring_is_a_power_of_two_of_slots` would catch it, but only runs at 512.
3. **The marker-list hash is the part of the build ID that truncation removes.** `CMakeLists.txt:113-114` builds `<app describe>+op<module describe>+m<hash>` and then cuts the tail to `BUILD_ID_MAX` (range 16..128). This repo has no tags, so its own describe is 7 to 13 characters. At the default 64, the hash starts losing characters once the app's describe passes about 40 characters, and is gone entirely past about 50. Any `BUILD_ID_MAX` near its minimum loses it outright. The hash is the one component that changes when a marker is renamed in a dirty tree, which is decision 9's verification half.

When done, each of the three either keeps its promise at every value its range allows, or is refused at configure or build time. For (1), the worker chooses between a wait the drain thread can actually end (still dropping where waiting is impossible) and removing the mode, and records why. For (3), any composition that keeps the hash will do, or a build-time refusal that names the cause.

## Why now

(1) contradicts the docs in both directions. `spec.md:59` and decision 5's title (`decisions/transport.md`) say overflow never blocks, while `interfaces/integration.md:29` offers blocking as an opt-in "for a deliberate high-fidelity run". That is the run where a hang costs the most. (2) is the same budget overshoot that the `OUTPOST_SLOT_BYTES` BUILD_ASSERT (`src/outpost_priv.h:203-233`) was restored to stop, still alive at the bottom of the range. (3) weakens decision 9 (`decisions/manifest.md`) without a word, and `integration.md:34` still marks `BUILD_ID_MAX` as `[assumed]`.

## Done when

- [x] A native_sim test with `OVERFLOW_BLOCK=y`: a thread at a priority numerically below the drain thread's emits into a full ring and returns in bounded time with its record in the ring. If the mode is removed instead, its header flag bit is documented as retired in `interfaces/wire.md`.
- [x] `spec.md`, decision 5 and `interfaces/integration.md` agree on whether the module can block, and on which contexts still drop.
- [x] No value in `RING_BYTES`' range gives `slots × OUTPOST_SLOT_BYTES > CONFIG_EMBARCH_OUTPOST_RING_BYTES`, and a build at the range minimum proves it.
- [x] With both describes 60 characters long and `BUILD_ID_MAX` at its range minimum, two marker lists that differ in one name produce different build IDs, or the build fails and says why.
- [x] `tests/run-all.sh` passes every leg.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/` fragment for anything suite-level it made false.
