# 014 — Make the live `shell` tell a silent console, a lost port and an empty success apart

**State:** claimed by agent/atlas/014-shell-tells-silence-lost-port-and-empty-success-apart, 2026-10-29 16:58
**Source:** field use on a USB PD charger board, 2026-09-09 to 2026-10-20 — 23 of 142 `shell` answers were empty, 21 of them followed by a second command only to see whether the first took; 2 said "did not run" for a command that ran
**Scope:** atlas
**Hardware:** verify-only
**Owner:** no

## What

`shell` (`embarch-atlas/src/embarch_atlas/live.py:486`) gives one of four distinguishable answers: the output; "the command printed nothing and returned N" (Zephyr's `retval` command, on by default through `CONFIG_SHELL_CMDS_RETURN_VALUE`, run as a second exchange when the output is empty); "nothing came back, not even the echo", with the cause Core reports; and "the command was sent, then the console port went away", with whatever output arrived. Today an empty output and a silent console both print as an empty block; a missing prompt adds "the output may be cut; pass a longer timeout_ms" (`live.py:493-494`), which is the wrong advice when zero bytes came back; and every `LiveError` prints "The command did not run" (`live.py:491-492`), including a read error after the line was written. `Console.run` (`live.py:467-479`) also moves to the next declared console on any `LiveError`, so with two consoles declared a command whose port dropped after the write would be sent a second time on the other one. `embarch-atlas live shell` and `live reg-read` exit 0 whatever happened (`live.py:885-894`).

## Why now

A budget-setting command that prints nothing on success produced the 23 empty answers; the session could not tell success from a silent refusal and checked each with a status command (21 extra calls). The 2 false "did not run" answers came from a command that switches the DUT's USB device off; the session re-sent it.

**Merged in 2026-10-26: `atlas/022`**, filed that morning from `core/098`'s inbox drop and a subset of this task, so it was folded here rather than queued twice. Core's exchange answer now carries the fields this task waited for (`embarch-core` decision 85): `written`, `port_lost`, `echo_seen`, `bytes_read`, and on a silent reply `port_identity` (VID, PID, product, serial) and `core_state` (DHCSR flags, or why it is unavailable). What 022 added beyond this task: a silent reply prints the echo verdict, the port's VID/PID/product and the core state; and a `500` from an open or write failure means nothing was written, so a resend is safe there and only there.

## Done when

- [ ] A silent body (a fixture carrying `port_identity` and `core_state`) prints the echo verdict, the identity and the core state. (From `atlas/022`.)
- [ ] Unit tests with a fake `embarch-api` reproduce: empty output with prompt seen (answer carries `retval`); zero bytes (no "longer timeout" advice); a `500` or `port_lost` after the write (answer says the command was sent and is not retried on another console).
- [ ] `Console.run` falls through to the next console only when the failure happened before anything was written (port not enumerable, open failed), never after.
- [ ] `retval` is skipped, and the answer says so, when the image has no `retval` command.
- [ ] The CLI verbs exit non-zero when the answer is "did not run", "nothing came back" or "port lost".
- [ ] Bench check: a command that prints nothing returns `0` and a refused one its error code.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `DESIGN.md` "Live" updated, `changelog.d/` fragment dropped. Uses Core's new exchange fields when present (filed as `core-exchange-says-what-happened-on-the-wire`), and works without them from `text` and `until_seen`.
