# Make the dev-bench "not found" error name the declared fact that excluded every candidate

**State:** open
**Source:** owner's repo survey, 2026-09-06 — decision 20's own failure mode, with a remedy that preserves the cause
**Scope:** topology
**Hardware:** none
**Owner:** no

## What

`src/hardware/port.rs:136-142` tells any operator whose candidates were all filtered away to
"re-enroll dev-bench … with only its own probe attached". But the narrowing that emptied the list
may have been a declared `link_port_serial` (hard-narrows at `:316`) or a declared
`link_port_interface` (`:327-329`) — and `src/hardware/validate.rs:331-333` carries both of those
over on re-enrollment keyed by probe serial. **The advice the message gives cannot clear them**, and
`src/hardware/enrollment.rs:205-216` offers no way to unset either.

`NotFound` should carry which rule emptied the candidate list, and its `Display` should send the
operator to the fix that can actually work. That means a way to clear a declared link serial or
interface exists on the crate API and the CLI, rather than requiring a hand edit of a machine-wide
TOML.

**Host-side:** fixture tests over candidate lists, not a bench. Do not enroll anything.

## Why now

This is the exact failure decision 20 records — a stale declared link serial "hard-narrows detection
to a port that cannot exist" — and the message currently routes that operator to a command that
preserves the stale fact.

## Measured on the bench, 2026-09-06 (leg 020, `tasks/topology/006`)

There is a **fourth** case, and it is the one a fleet leg hits every time. Run from WSL with the
board attached and working, `embarch-topology dev-bench` printed:

    Error: no embarch-dev-bench serial port found (0 serial port(s) visible, 0 with a
    recognized link VID ...) — check dev-bench's USB connection

The USB connection was fine. The ports are on the **Windows host**, where the real Core runs;
this process was on neither. **`0 serial port(s) visible` is the tell and the message does not
use it** — zero ports on a developer machine means the enumerator is on the wrong host far more
often than it means every cable fell out.

**The same binary already knows this.** `embarch-topology status`, on that box, in the same
second, resolved Core as `http://172.22.128.1:4884 (wsl-host)` and reported
`Core { authorized: false }`. So the machine has established it is the remote half of a split
setup at the moment its sibling command blames the cable. The `usbipd attach` parenthetical is
in the message, but it trails a sentence that has already sent the reader to the hardware.

## Done when

- [ ] The zero-ports-visible case names the split-host possibility **first**, not as a
      parenthetical, and says what `status` would show — it is already computable.
- [ ] `NotFound` gains a field naming the excluding rule, set at each narrowing site in `select`.
- [ ] `Display` prints the matching remedy per rule; the existing wording stays for the
      role-fallback case.
- [ ] Fixture tests cover: declared serial matches nothing, declared interface matches nothing, and
      no candidate VID at all — each asserting the message routes to a different fix.
- [ ] A way to clear a declared link serial/interface exists on the crate API and the CLI, with a test.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10), including
      `cargo test --no-default-features --features hardware`.
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false.
