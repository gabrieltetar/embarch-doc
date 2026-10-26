# 097 — Make a console exchange write its whole line when the device throttles, instead of losing bytes to the 50 ms port timeout

**State:** claimed by agent/core/097-exchange-write-throttled-device, 2026-10-26 00:08
**Source:** field use on an STM32G0 board with a Zephyr USB CDC ACM shell, 2026-10-21: a 357-character `image data` line sent through `signal_exchange` reached the device 16 characters short with the shell echo on and 8 short with echo off; the same device took every 960-character line of a 25.6 KB image intact from pyserial on the same Windows COM port
**Scope:** core
**Hardware:** verify-only
**Owner:** no

## What

`exchange::run` (`embarch-core/src/exchange.rs:214-219` at `40a58cc`) opens the port with `.timeout(Duration::from_millis(50))`, and serialport uses that one timeout for writes as well as reads. `exchange()` then sends the line with a single `write_all` (`exchange.rs:163`). A Zephyr CDC ACM device that is still busy with earlier input stops taking bulk OUT packets until its ring buffer drains, so a long line cannot leave in 50 ms. On Windows the timed-out write is cut short partway through a transfer, and `write_all` sends the bytes it believes are left: the device receives the start and the end of the line with a hole near the end (characters 339-355 of 357 in the echoed text). Nothing in the response says so. When done, the write has its own deadline, bounded by the exchange's `timeout_ms` and independent of the 50 ms read poll, and a write that cannot finish by then fails the exchange with the count of bytes written instead of returning a reply to a damaged line.

## Why now

A host that pastes base64 chunks, configuration lines or long commands through the exchange gets corrupted input that only a payload checksum catches. On this board a CRC check refused every image sent through EmbArch, and the transfer looked like a firmware bug in the image shell until the same lines went through pyserial (blocking writes) and arrived whole. Shorter lines hide it, which is why every command-length exchange so far has looked fine.

## Done when

- [x] A unit test on `exchange()`'s fake port that accepts at most N bytes per write call, with a delay per call longer than 50 ms, receives the whole line in order.
- [x] A test where the fake port never accepts the rest fails the exchange by its deadline and reports the bytes written.
- [ ] Bench check: a 960-character line to a Zephyr CDC ACM shell, sent through `POST /signals/{name}/exchange` with the shell echo on, arrives whole: the device's own byte count matches the line length.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `spec.md`/`decisions.md` updated (decision 79 amended for the write deadline), `changelog.d/` fragment dropped.

## Result

Host half shipped in `embarch-core/src/exchange.rs`: `write_with_deadline` (retries throttled writes until `timeout_ms`, fails with bytes-taken count), `run` sets the port timeout to `timeout_ms` for the write then back to 50 ms. Tests: throttled fake (16 bytes/call, 60 ms stall per call) receives all 357 bytes in order; a fake that stops after 4 bytes fails by the deadline with "only 4 of 10 bytes". Decision 79 amended (`decisions/signal-exchange.md`).

### Hardware-verification debt

Not run (no hardware): on the STM32G0 Zephyr CDC ACM board, send a 960-character line through `POST /signals/{name}/exchange` with shell echo on and `timeout_ms` >= 2000; the device's own byte count must equal 960. Also confirm the Windows `serialport` write honours `set_timeout` mid-session. Native Windows build of `embarch-core` not run (owner's debt).
