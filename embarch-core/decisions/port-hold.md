# embarch-core decisions: Core holds the bench's serial ports

**Status:** active, 2026-11-25 (`tasks/core/154`, EMB-326; `notes/hil/12-prevention.md` "The root of trust"). Index: [../decisions.md](../decisions.md). Siblings: [lease.md](lease.md) (93), [lease-idle.md](lease-idle.md) (123), [signing.md](signing.md) (110).

### 130 — While a lease or a study is live, Core keeps its serial ports open, and every serial use borrows the handle

Every serial use opened a port, used it and closed it, so the OS kept a second opener out only during a call. A second Core on another HTTP port could reach the bench between two calls of the attested one, and the signed record could not say Core had held the ports. `serialport` 4.9 opens a POSIX port exclusively (TIOCEXCL); a handle kept open keeps the exclusion open too. A Windows COM port is exclusive by the OS **[assumed, unmeasured]**.

**The holder is `port_hold.rs`**: a process-wide set of open handles, owned by a lease and by a study. Taking a lease (`POST /lease`) and a study's start (`LeaseSlot::study_started`, in the three study spawns) open every declared signal's and instrument's port that enumerates; the ports close when the last owner lets go: release, expiry, idle release (decision 123), or `LeaseSlot::study_ended`. A study with no lease holds for its own run; inside a lease it shares the lease's hold. A via-dev-bench signal has no port of its own and is skipped.

**One door.** `port_hold::open(name, baud, timeout)` replaced every `serialport::new(..).open()` for a signal, an instrument or a log port: exchange, instrument, serial log, capture and host-study taps, a device study's signal tap, the outpost preflight. A held port is lent, one borrower at a time (a second borrower gets an error, not a wait: `hw_lock` already serializes callers), reconfigured to the caller's baud, timeout and no flow control, and handed back on drop. An unheld port opens fresh and closes on drop, as before.

**A port absent at the take** is logged and held from its first use: while an owner is live, any port opened through the door is adopted on return and held until the owners end.

**Not held:** bootload ports (`/bootload`, `/bootload/ports`) re-enumerate during a bootload, so a held handle would go stale; they open as before. The dev-bench link (`dev_bench_link.rs`) and the analog samples port (`analog_source.rs`) are opened by a study for its whole life, the link with hardware flow control, and stay exclusive by that. A held port's first flow-control setting is not meant for them.

**Expiry now has a timer.** Decision 93's lazy expiry would leave the ports held after the lease's end until the next check, which locks a second Core out of a bench nobody holds. `LeaseSlot::spawn_expiry_watch` (a tokio task per take) sleeps to the lease's next end (expiry, or idle release) and evaluates it. The lease itself stays in memory and a Core restart still ends it.

**The signed record** lists the ports held at sealing under `observed.ports_held` ([../interfaces/signing.md](../interfaces/signing.md)): Core observed the handles, so it is `observed`, not `claimed`. A run with no hold records `[]`.

**Under test**, `declared_targets` returns nothing and each test thread has its own holder, so no test opens a port the machine declares. The pty test (`port_hold.rs`) shows a second open failing while held, Core's own write going through the held handle, and a second open succeeding after the release. **[unverified on hardware]:** Windows COM ports and a real CDC ACM bench port (debt in `tasks/core/154`).
