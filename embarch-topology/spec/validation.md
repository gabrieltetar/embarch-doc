# embarch-topology spec: What validation asserts, and what it cannot

**Status:** active, 2026-11-17.

Split verbatim from [../spec.md](../spec.md), 2026-11-17, because `tasks/topology/070` had to
compact it; the section below is unchanged.

## What validation asserts, and what it cannot

- **A role:** the enrolled probe is enumerated and its live identity still matches the recorded one; runs on every flash, reset and handshake.
- **A same-chip link:** the board on the runtime link is the same silicon the JTAG probe verified, comparing its JTAG-read identity against its self-report. **An exact match settles it for any chip** — two mechanisms agreeing byte for byte on a factory-unique value is conclusive on its own. Two chip families additionally have a declared relation, for when the two mechanisms format that same value differently; every chip with neither an exact match nor a declared relation returns *undeclared*, never a pass.
- **A requested chip:** `validate_serial_for_chip` compares the chip a caller asks for with the enrolled row's, by name and ignoring case, **before the probe is opened**; a differing chip is a `RequestedChipMismatch` naming the probe, the enrolled board and the re-enroll call, and equal names fall through to the identity checks unchanged (decision 44).
- **A direct signal route:** the declared serial is enumerable. It **cannot** confirm the DUT's TX pin wire lands on that bridge.
- **A signal Core may write** is `host-to-dut` or `bidirectional` on a direct route (`SignalLink::host_can_write`, decision 37); a signal may declare its own `baud`, else Core's default applies.
- **A signal's origin** is a role or, through `origin_board`, an enrolled role-less bench board by its probe serial; `declare` resolves a board's name to that serial and refuses an unenrolled board, an ambiguous name or a role's probe (`SignalLink::origin`, `find_signal_origin_board`, decision 48).
- **An ID whose words are all the same** is retried once, then read with the core halted for microseconds, then a failed read, never a mismatch (decisions 38, 39). An STM32G0's UID is always read halted (decision 39).
- **Attaching to an ARMv6 STM32** (F0, L0, G0) goes through `hardware::attach::attach`, which never read-modify-writes RCC or DBGMCU on a running core (decision 39).
- **A via-bench route:** validates on the strength of being declared; its carrier is the bench link, whose liveness is the role check's job (decision 18).

**A signal mismatch is not written to the alert log** — an alert's shape is board-specific and a wire has none of them.

A validate call previously carried only the enrolled record's `confirmed_at_utc_ms` — enrolment time, not this check's. `validate_serial_timed`/`validate_role_timed` add `validated_at_utc_ms`, its own pass instant, beside unchanged `validate_serial`/`validate_role` (decision 26). `embarch-core`'s `POST /validate` exposes it via `validate_role_timed`, populating `ValidateOkResponse.validated_at_utc_ms` from the returned `Validation` (`embarch-core` decision 50). `Validation.halts` says how many times the identity gate halted the core (0 if already halted or the family reads without halting), so Core need not infer it (decision 47).
