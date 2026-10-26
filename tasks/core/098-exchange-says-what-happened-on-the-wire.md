# 098 — Make a console exchange say what happened on the wire: nothing back, the write sent, the port lost, the marker line cut

**State:** done — host-side half shipped 2026-10-26; the bench check is a hardware-verification debt (end of file)
**Reserve, for the worker (2026-10-26):** no `embarch-core` doc file is in reserve, but decision 79
(`decisions/signal-exchange.md`) is already 5,494 B against `DOC-BUDGET.md`'s 4 KB per-decision
cap. Amend 79 only where its existing text becomes false; put the new reasoning (what the answer
reports and why) in a new numbered decision that cites 79. `api/123` runs in parallel and does not
see these fields; the api and atlas follow-ups this task asks for go to `inbox/` as drops.
**Source:** field use on a USB PD charger board, 2026-09-09 to 2026-10-20 — 10 of 122 `signal_exchange` calls came back `text: ""`, `until_seen: false` from five different causes; 2 answered `500` for a command that had run; 14 of 29 replies waiting for a mid-line marker stopped inside that line (`pd: o`)
**Scope:** core
**Hardware:** verify-only
**Owner:** no

## What

`POST /signals/{name}/exchange` answers with enough to tell the failure modes apart without a second tool. Today `ExchangeResponse` (`embarch-core/src/exchange.rs:85`) carries `text`, `until_seen`, `truncated` and `elapsed_ms`, so a console that sent nothing at all looks exactly like a slow command, and a read error after the write (`exchange.rs:197`) becomes a `500` (`api.rs:1351`, `internal_err`) that drops the fact that the line went out and the bytes read before the loss. When done, the response also states: the bytes read; whether the echo of the written line was seen (`exchange.rs:185` already computes it); `written: true` once `write_all` and `flush` succeeded; and `port_lost: true` with the partial text when the port disappeared mid-read, as a `200`, not a `500`. When nothing at all came back, or the port wait of decision 79's amendment runs out, Core adds what it can see without halting: the port's USB identity (VID/PID and product string, so a USB-UART bridge is told from the DUT's own USB device) and, if the signal's role has an enrolled probe, the core's run state from `DHCSR` (`S_HALT`, `S_SLEEP`, `S_LOCKUP`, `S_RESET_ST`, and whether `S_RETIRE_ST` shows instructions retiring). `DHCSR` is a PPB read, so it is correct on a sleeping STM32G0 with no DMA clock, and it never halts. Last, an `until` found in the middle of a line no longer ends the read at the match (`exchange.rs:187-189`): Core reads on until that line ends or the port has been quiet for a short gap (tens of milliseconds), bounded by the deadline, so a marker such as `pd: ` returns the verdict word after it and a prompt with nothing after it still returns at once.

## Why now

The 10 empty replies had five causes, each found only by hand and by other tools: an ST eval board held in reset by a shield jumper, a bench shell starved after cabling, the DUT hung after a Get_Source_Cap, the bench board running the wrong build, and the console signal pointing at a USB-UART bridge while the image's shell was on USB CDC ACM. In the 2 `500`s the command (one that turns the DUT's USB device off) had run, the atlas reported "the command did not run", and the session sent it again; a state-changing command sent twice is the cost. The 14 cut replies came from the PD bench's documented marker `pd: `: each said `until_seen: true` and lost `ok` or `error <reason>`; `dev-bench-pd-bench-shell-contract` changes the README advice, and this closes it in Core for every console.

## Done when

- [x] A unit test on `exchange()`'s fake port reproduces each case and asserts the new fields: zero bytes (no echo); echo seen then silence; the write accepted then a read error (`BrokenPipe`), answered with `written: true`, `port_lost: true` and the bytes read so far.
- [x] The handler maps a read error after a successful write to a `200` with `port_lost`; a failure to open or write stays an error, and its text says nothing was written.
- [x] A unit test feeds `...\r\npd: o` then `k\r\n` in two reads with `until: "pd: "`; the reply ends with `pd: ok\r\n` and `until_seen` is true. A prompt with nothing after it returns after the quiet gap, not at the deadline.
- [x] Zero bytes back, or a port wait that expires, adds the port identity and, when the role has a probe, the `DHCSR` run state read through the guarded attach, with no halt; a test covers the "role has no probe" and "probe absent" branches.
- [ ] Bench check: an exchange to a board held in reset, and to a board halted by a debugger, each name the state; a command that drops the CDC ACM port answers `port_lost` with its first output line.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `spec.md`/`decisions.md`/`open.md` updated (decision 79 amended), `changelog.d/` fragment dropped; follow-ups filed for `embarch-api` (MCP text and CLI) and `embarch-atlas` (`shell`) to print the new fields.

## Hardware-verification debt

- [ ] Bench check (the unticked item above): on a real board, (1) an exchange to a board held in reset returns `core_state.s_reset_st` true and no bytes; (2) to a board halted by a debugger, `s_halt` true; (3) a command that drops the CDC ACM port answers `200` with `port_lost: true` and its first output line. Also confirm the guarded attach does not halt or disturb a running core and that the 40 ms `QUIET_GAP` is long enough for a real shell's verdict word after `pd: `.
- [ ] The native Windows build of `embarch-core` was not run (not possible from a worktree); `read_dhcsr` uses only `core.read_word_32`, nothing platform-specific.

Follow-ups dropped in `embarch-doc/inbox/`: `api-signal-exchange-prints-wire-fields.md`, `atlas-shell-prints-exchange-wire-fields.md`. Decision 85 added; 79 amended by pointer. The mid-line change alters the old `the_prompt_a_shell_prints_on_open...` test's no-echo half (a match on the early prompt now reads to that line's end).
