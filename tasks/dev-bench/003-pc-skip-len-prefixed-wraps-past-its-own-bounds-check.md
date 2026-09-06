# Reject an impossible length prefix in `pc_skip_len_prefixed` instead of wrapping past it

**State:** open
**Source:** owner's repo survey, 2026-09-06 — the one bounds check in a file that states this exact property, written in wrapping arithmetic
**Scope:** dev-bench
**Hardware:** required
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

## Done when

- [ ] A frame carrying a length prefix of ~2^64 (and one of ~2^60 at the `elem_size = 16` site) is
      refused by `dbm_decode_frame`.
- [ ] `*pos` is never assigned a value less than its entry value on any path.
- [ ] Two new ZTESTs pin both, and the existing suite passes under
      `west twister -p native_sim -T ../../app/tests`.
- [ ] No constant or capacity limit changes.
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false.
