# 099 — A bench lease: one session holds the bench across calls, and other callers are refused by name

**State:** open
**Source:** field use on a USB PD charger board, 2026-09-09 to 2026-10-20 — two Claude sessions shared one DUT and one bench Nucleo from 2026-10-08; with no lease in Core they used a `mkdir` lock directory: 62 holds by 8 sessions (6.3 h held in all, the longest 1.4 h), one collision waited out in a shell `until mkdir` loop, and the rule had every session reflash its own image after taking the lock because it could not know what the other had left (80 flashes with an explicit image path from 2026-10-08 on)
**Scope:** core
**Hardware:** verify-only
**Owner:** no

## What

Core serialises single requests and nothing longer. `hw_lock` (`embarch-core/src/api.rs:29`) is taken per handler, waits 500 ms (`HW_LOCK_WAIT_MS`, `api.rs:79`) and then refuses with `503` naming the holding route (`acquire_hw_lock`, `api.rs:107`; decisions 4, 14 and 15); `study_lock` covers a study. A session's real unit of work is a sequence: flash, reset, a dozen exchanges, a register read. Between any two of those calls another session can flash its own image, and every later reply then describes the wrong firmware with nothing to say so. Add a lease. `POST /lease {holder, purpose, ttl_s}` returns a token. While a lease is live, every hardware route (flash, reset, bootload, exchange, serial-log, mem-read, validate, enroll, study submit) refuses a request that does not carry the token with `409` naming the holder, the purpose, the start time and the expiry. The holder renews or releases it, and expiry frees the bench with no human involved. With no lease held, a request without a token behaves exactly as today. `GET /status` reports the lease and, for each board, the last image Core flashed (path, sha256, time, lease holder), so a session that takes the bench can decide whether it needs to reflash. Settle in the decision whether the lease covers the whole bench or one board; the field sessions always used both boards together.

## Why now

On 2026-10-08 the session that hit the collision offered the user a lock file, a one-off message to the other session, or "a lease in embarch-core, the real fix, a few hours"; the lock file was chosen as the stopgap until this lands. It works only while every session and subagent remembers the rule, and it cannot see calls made through `embarch-atlas`'s live tools, which reach Core on their own.

## Done when

- [ ] `POST /lease`, renew and `DELETE` exist; a hardware request without the token while a lease is live is refused with `409` naming holder, purpose, start and expiry, tested with two clients.
- [ ] An expired lease frees the bench without a restart or a human; a crashed holder never blocks the bench past its TTL.
- [ ] With no lease held, every existing route behaves as before (existing tests unchanged).
- [ ] `GET /status` reports the live lease and, per board, the last image Core flashed (path, sha256, time, holder).
- [ ] The client half is filed as an `api` task: the MCP server and CLI take, renew and send the token, in a form `embarch-atlas` live calls inherit (an environment variable or a per-process lease).
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped.
