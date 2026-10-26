# embarch-core decisions: Writing to a declared signal

**Status:** active, 2026-10-06.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md). HTTP surface: [../interfaces/topology.md](../interfaces/topology.md).

### 79 — `POST /signals/{name}/exchange`: one written line and its reply, inside one `hw_lock` hold

An agent working a DUT needs its shell: write `kernel uptime`, read the reply. Until now that meant a hand-written serial script on the Core machine per session, outside Core and outside its lock, racing anything Core did to the same board. The DUT's console is a declared signal ([`embarch-topology`](../../embarch-topology/decisions.md) decision 37 makes a direct `host-to-dut` or `bidirectional` one writable), so the write belongs on the signal routes.

**An exchange, not a session.** The port is opened, the line written, the reply read until `until` appears or `timeout_ms` passes, and the port closed, all inside one `hw_lock` hold. A held-open session would keep the lock across an agent's thinking time and block every flash and reset on the bench; a shell is command-and-reply anyway. `timeout_ms` defaults to 2,000 and is capped at `serial::MAX_DURATION_MS` (10,000) for `/serial-log`'s reason (decision 58): under the shared client's 15 s timeout. A request is checked before the lock: an empty or over-4 KiB `write`, an empty `until`, a timeout outside the range are `400`s.

**Bytes in, bytes out.** The reply is lossy UTF-8 with the DUT's escape codes left in (`embarch-outpost` decision 11's pass-through posture): stripping colour or matching a prompt is the caller's job, and a caller that wants the raw console still has it. Pending input is discarded before the write by default, so the reply is this command's, not an earlier log line's tail. DTR is asserted, because a Zephyr CDC ACM shell may wait for it; a bridge without the control line is not refused. The read is capped at 256 KiB.

**The rate is the signal's own** (`baud` in the declaration), else `EMBARCH_SIGNAL_BAUD`; the same rule now applies where a study opens a signal tap and where the outpost pre-flight reads its header.

**`until` is matched only after the echo of what was written** (`match_after_echo`, on by default). Found on the first real DUT: a Zephyr CDC ACM shell prints a fresh prompt the moment the port opens and DTR rises, before the command's echo and output, so a plain match ended every read on that prompt with an empty reply. A console that does not echo turns it off.

`404` when nothing is declared under the name; `409` when the signal is declared but not writable, or its port is not enumerable now.

**Rejected: a raw `?port=` write like `/serial-log`'s read.** A write is the one operation that can change a board's state; naming it by a declared signal means the port, the direction and the rate are facts someone stated, and a `dut-to-host` trace can never be written by mistake.

**Amended 2026-10-06: `port_wait_ms`.** A caller that has just flashed or reset the DUT finds its USB CDC ACM console gone for a few seconds while the device re-enumerates, and the exchange answered `409` at once, so every agent wrote a sleep-and-retry loop. `port_wait_ms` (default 0, max 10,000, checked before `hw_lock`) makes Core poll enumeration every 250 ms for that long, and only for a declared direct port that is missing (`embarch-topology` decision 40's `SignalMismatch`); any other failure answers at once. The wait holds `hw_lock`, as the exchange it precedes does. The client adds it to the request's timeout.


**Amended 2026-10-26: the write has its own deadline (`core` task 097).** `serialport` uses one timeout for both directions, and the port was opened at 50 ms for the read poll. A Zephyr CDC ACM device still draining earlier input stops taking bulk OUT packets, so a 357-character line outran 50 ms, the Windows write was cut short mid-transfer, and `write_all` resent from a count that no longer matched what had left: the device saw the line with a hole near the end and the exchange answered as if nothing was wrong. Now the port's timeout is set to the request's `timeout_ms` for the write, then back to 50 ms for the read; the write loops on `TimedOut`/`WouldBlock`/zero-length results until the same `timeout_ms` deadline, and past it the exchange fails naming how many of the line's bytes were taken, instead of returning a reply to a damaged line. The read's own deadline starts after the write. Measured: only against a fake port that stalls and takes short bursts (unit tests); the real-device behaviour is a hardware-verification debt (task 097).
