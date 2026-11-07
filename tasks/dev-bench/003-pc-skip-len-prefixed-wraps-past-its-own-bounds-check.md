# Reject an impossible length prefix in `pc_skip_len_prefixed` instead of wrapping past it

**State:** done
**Source:** owner's repo survey, 2026-09-06 — the one bounds check in a file that states this exact property, written in wrapping arithmetic
**Scope:** dev-bench
**Hardware:** toolchain — host-side C plus `native_sim` ztests, no board. Reclassified from `required` 2026-09-06 (`tasks/doc/020`): the supervisor runs it in the **main checkout**, serialized like a `bench` task.
**Owner:** no

## NOT DISPATCHABLE, and the reason is a toolchain, not a board

Same as the companion `goto_state` drop: this is C plus ztests on `native_sim`, no bench needed, but
`west` is not on bare `PATH` and no `workspaces/*` carries a `.venv` (`embarch-dev-bench/CLAUDE.md`).
A worker cannot build what it writes. Reclassify to `none` once a worker has a runnable `west`.

**This one is hardening, not a bug anyone has hit** — say so when it is worked. A wrapped cursor
yields a garbage decode that the `steps_crc` / `streams_crc` / `protocols_crc` seals will almost
certainly reject, and reaching it needs a crafted frame rather than plausible corruption. What earns
it is that the file claims this property and this function does not hold it.

## What

`app/src/serial_protocol.c:93-105` — `size_t n = (size_t)len * elem_size;` then
`if (*pos + n > in_len)`. Both the multiply (`elem_size` is 16 at the call site on `:1463`) and the
add are unsigned-wrapping, so a crafted 10-byte varint near 2^64 passes the bound check and
`*pos += n` moves the cursor **backwards**. `cobs_decode`'s own comment at `:790-793` states the
file's posture — these bytes are "untrusted… possibly corrupted or crafted" and "must never be able
to overflow" — and the sibling walker does not hold that line.

The length should be checked against the remaining input before any arithmetic that can wrap
(`len > in_len - *pos`, or an explicit overflow guard on the multiply), so a malformed span returns
-1 and the frame is refused rather than re-parsed from an earlier offset.

## Why now

Every `.eap` and `StreamTap` walk routes through this function — nine call sites, `:144`–`:1463`.

## How to run it (`toolchain`, so these are the facts the task carries)

`west` is not on bare `PATH` and no `workspaces/*` carries a `.venv`, so the
fleet has its own, deliberately outside every repo and outside every client
workspace:

    W=/home/gabriel/Github/embarch/.west-venv/bin/west
    cd /home/gabriel/Github/embarch/embarch-dev-bench/workspaces/native_sim
    $W build -b native_sim -d <a scratch build dir> \
        /home/gabriel/Github/embarch/embarch-dev-bench/app/tests/serial_protocol
    <scratch>/zephyr/zephyr.exe        # 57 tests; exit 0 when green

Verified 2026-09-06, 57 of 57. `zephyr.exe` exits non-zero on any failure, so
its exit status is the gate — do not read the summary line and stop.

**In the main checkout, not a worktree**, and that is the whole reason this is
`toolchain`: `workspaces/*/{zephyr,modules,.west}` are gitignored, so a worktree
has no Zephyr tree to build against and a `west` binary alone buys nothing.

## Done when

- [x] A frame carrying a length prefix of ~2^64 (and one of ~2^60 at the `elem_size = 16` site) is
      refused by `dbm_decode_frame`.
- [x] `*pos` is never assigned a value less than its entry value on any path.
- [x] Two new ZTESTs pin both, and the existing suite passes under
      `west twister -p native_sim -T ../../app/tests` (met suite by suite, not by `twister`,
      which could not start: see Done).
- [x] No constant or capacity limit changes.
- [x] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false.

## Done (2026-11-07, the leg's own hands)

Hardening, not a bug anyone hit. `pc_skip_len_prefixed` now refuses `len > (in_len - *pos) /
elem_size` before any arithmetic, so neither the multiply, the `(size_t)` narrowing (32 bits on
`native_sim` and both bench targets) nor the add can wrap. The only change to `*pos` is an add
after that check. The other length-derived cursor sites in `serial_protocol.c` already bound
`len` against a small cap first; none changed.

`test_a_length_prefix_near_2_64_is_refused_not_wrapped` (a protocol name of 2^64 - 1) and
`test_a_uuid_count_near_2_60_is_refused_not_wrapped` (a `BleAdvertise` `service_uuids` count of
2^60) are laid out so the wrapped walk lands on well-formed bytes: with the fix reverted both
decode to 0 and fail, 57 of 59; with it, 59 of 59.

**`west twister` did not run**: the fleet venv lacks twister's Python requirements (`natsort`).
Each of the four suites under `app/tests` was built and run on its own instead, from the main
checkout's `workspaces/native_sim` against this branch's worktree: `serial_protocol` 59/59,
`dev_bench_log` 15/15, `scan_seen_mfg` 7/7, `scan_seen_names` 5/5. The worktree's `app/` built
for `nrf54l15dk/nrf54l15/cpuapp` from `workspaces/nordic`. The ESP32-C5 image did not configure:
Zephyr's Espressif SoC CMake wants `esptool` on `PATH` and the fleet venv has none.

Docs: one invariant line in `embarch-dev-bench/spec.md` §3; no decision entry, since the choice
has no alternative worth recording.
