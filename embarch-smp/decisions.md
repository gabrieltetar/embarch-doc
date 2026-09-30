# embarch-smp: decisions

**Status:** active, 2026-09-30.

Why it is the way it is. Current truth: [spec.md](spec.md). Unresolved: [open.md](open.md).

**Numbers are permanent identifiers**, unique to this sub-project, never renumbered or reused ([DOC-CONVENTIONS.md](../DOC-CONVENTIONS.md)).

## Shape

### 1 — A port of smpclient, not a fresh implementation and not a wrapper around smpmgr
smpclient and `smp` are already exercised against real MCUboot builds, including smpclient's own reference firmware for serial recovery over CDC ACM — the exact case this serves. Porting inherits that behaviour and a test suite to mirror; writing from the protocol description would rediscover the same edge cases on hardware. **Rejected: shelling out to `smpmgr`** the way Core shells out to `nrfutil` (`embarch-core` decision 36). It is about a day instead of three, but it adds a Python-or-portable-exe dependency on the Core machine and a second process on a serial port, which decision 2 rules out. Full comparison: [bootload-proposal.md](../bootload-proposal.md).

### 2 — It never opens a port; every call takes a `Read + Write`
`embarch-topology`'s `hardware` feature is the only code in the suite that opens a serial port (`embarch-topology` decision 8), and this crate does not become a second. The split mirrors the original: `smp` is I/O-free and smpclient owns the transports. Here the transport is whatever stream the caller hands in, so a pipe in a test and a COM port in Core are the same code path.

### 3 — Apache-2.0, not the suite's MIT
The rest of the suite is MIT. This crate is a derivative of two Apache-2.0 works, so it stays Apache-2.0, with a `NOTICE` naming both and a header on every ported file pointing at its original. MIT-licensed crates depend on it without conflict.

### 4 — Serial transport and four commands only, blocking
The first consumer is MCUboot serial recovery, which answers echo, reset, image state and image upload, and only the first and last of those unconditionally. Anything more is surface with no caller. **Blocking, not async**: Core runs every hardware operation inside `spawn_blocking` already, and the Python original's asyncio exists for BLE, which is out of scope.

### 5 — Python generates fixtures; it is never a dependency
Byte-exact agreement with the reference is checked against fixtures the Python `smp` package produced, committed next to the script that produced them. Regenerating is a deliberate act with a diff to review, and `cargo test` needs no Python on the machine.
