# embarch-api decisions: A bench board by its own name

**Status:** active, 2026-10-28.

Index: [../decisions.md](../decisions.md). Builds on `embarch-core` decision 103 and `embarch-topology` decision 48, which are where a bench board's signal, live reads and validate are resolved.

### 95 — `declare_signal` takes `origin_board`; `validate`, `mem_read` and `core_state` take `probe_serial` (`tasks/suite/046`)

A role-less bench board (a USB PD bench Nucleo, 2026-10) could be flashed and reset by probe serial, but its console had to be declared from a role it did not hold, and a halted read or a validate of it had no form at all.

**The tools and their CLI subcommands take a second form beside the role, and exactly one of the two.** `declare_signal`/`declare-signal` take `origin_board` (a bench board's enrolled name or probe serial) or `origin_role`; `validate` takes `probe_serial` or `role`; `mem_read` and `core_state` take `probe_serial` or `role`, still defaulting to the DUT when given neither. Both forms at once, or neither where there is no default, is refused before any request. This crate resolves nothing itself: a board name goes to Core as given and topology resolves it (decision 94's rule for signals, kept).

**`embarch-core-client` gains `Board` (a role or a probe serial) and `validate_board`, `mem_read_board` and `core_state_board`;** `validate`, `mem_read` and `core_state` keep their signatures and delegate, so `embarch-ui` is unaffected. The request carries exactly one of `role` and `probe_serial`, the other omitted.

**An older Core is caught, not trusted.** A Core before core decision 103 ignores `probe_serial` on a live read and reads the DUT, its default role, so a by-probe answer naming another probe is refused as a stale Core rather than handed on as the bench board's; the read itself has already halted and resumed the DUT once by then. A by-probe validate fails there with Core's own `422`, since that Core requires `role`. A Core before topology decision 48 drops `origin_board` and stores the signal with an empty role, answering `204`, so `declare_signal` reads the row back and refuses one stored without its board.
