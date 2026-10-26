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

- [ ] A unit test on `exchange()`'s fake port that accepts at most N bytes per write call, with a delay per call longer than 50 ms, receives the whole line in order.
- [ ] A test where the fake port never accepts the rest fails the exchange by its deadline and reports the bytes written.
- [ ] Bench check: a 960-character line to a Zephyr CDC ACM shell, sent through `POST /signals/{name}/exchange` with the shell echo on, arrives whole: the device's own byte count matches the line length.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md` updated (decision 79 amended for the write deadline), `changelog.d/` fragment dropped.
