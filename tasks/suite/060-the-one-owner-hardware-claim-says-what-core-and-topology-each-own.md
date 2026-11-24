# 060 — The one-owner hardware claim says what Core and topology each own

**State:** claimed by agent/suite/060-the-one-owner-hardware-claim-says-what-core-and-topology-each-own, 2026-11-24 13:13 — window ts 1795543398.128079 closed 11:33 with no reply; executed by the supervisor in its leg worktree
**Source:** the 2026-11-23 suite audit — `embarch.md` §4 says `embarch-topology`'s `hardware` feature is the only code that touches `probe-rs` or a serial port, and Core opens both itself
**Issue:** EMB-304
**Scope:** suite
**Hardware:** none
**Owner:** no

## What

Three places state that `embarch-topology`'s `hardware` feature is the only
code in the suite that touches `probe-rs` or opens a serial port:
`embarch.md` §4, `embarch-smp/decisions.md` (decision 2's "does not become a
second") and `embarch-smp/spec.md` ("stays the only code that opens a serial
port"). The code shows a narrower split: `embarch-core` depends on `probe-rs`
and `serialport` itself and opens probes in `src/hardware.rs` and ports in
`src/serial.rs`, `dev_bench_link.rs`, `exchange.rs`, `capture.rs` and
`bootload.rs`, while topology detects, enumerates and validates and lists ports
without opening one for I/O.

When this is done the three places say what holds: topology decides which
device and enforces identity before any open; Core is the only component that
opens a probe or a port; `embarch-smp` never opens one (unchanged). `embarch.md`
§4 states it once and the two `embarch-smp` lines point there. §4 also gains a
short edge table beside its sketch, leaving the sketch as it is: each
cross-sub-project runtime edge the sketch omits (api to desk, ui to desk, atlas
to the api CLI, chat to desk and ui, desk to promptu), with direction, hard or
soft, and whether it is in the runtime path. Each edge is checked against the
code before it is written.

`embarch-topology/decisions/link-declares.md`'s "nothing here opens a port" is
true of that module and stays as written.

## Why now

The suite's overview states as an invariant something the code contradicts
(EMB-304). Docs only; moving the opens into topology is the larger alternative
and is not proposed.

**Executed by the supervisor (protocol.md §8), docs only, no new numbered
decision** (burndown leg): `embarch-smp` decision 2 is amended in place.
`embarch.md` is 22,863 B, 177 B under its reserve line; an edge table pushes it
in, so the same fold either trims §4 to stay out or files the compaction debt.

## Done when

- [ ] `embarch.md` §4, `embarch-smp` decision 2 and `embarch-smp/spec.md` no
      longer claim a single owner of probe and port access, and say what Core
      and topology each own.
- [ ] §4 carries an edge table naming each cross-sub-project runtime edge and
      whether it is hard or soft.
- [ ] `check-docs.py` green.
