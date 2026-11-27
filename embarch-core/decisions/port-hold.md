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

### 159 — The holder also opens each enrolled board's debug probe at the take; a Core call closes it and reopens it, and a vendor tool's window is not covered

A probe was opened per call (`hardware::open_probe`), so a second Core, or a vendor tool, could take it between two calls of the attested one (`notes/hil/12-prevention.md`, "What stays outside prevention": a probe whose software admits a second connection is not covered).

**`probe_hold.rs`** has the owners of decision 130 (`port_hold::acquire` and `release` call it, so the take, the study start and every release path need no new call site). Each enrolled board's probe is opened through probe-rs at the take, keyed by its serial, and closes when the last owner lets go. A probe that fails to open is logged and not held, and is not adopted later (a port is; a probe has no first-use door).

**Deviation from the direction: a Core call closes and reopens, it does not borrow.** The board-identity gate (`embarch-topology`) opens the probe itself, and probe-rs 0.31's `Session` consumes the `Probe` it attaches with no way to hand it back, so neither takes a held handle. `probe_hold::around(serial, Use::Core, f)` closes the held probe, runs the call and reopens it on success and error: `hardware::flash`, `hardware::reset`, `live::with_core` (mem-read) and `read_dhcsr`, and every path that reaches the identity gate on its own: `POST /validate` (role and probe serial), `POST /probes/enroll` with a `probe_serial`, the dev-bench gate (`enforce_dev_bench_gate`: `GET /dev-bench/hello` and `POST /study`) and a test run's smoke-check gate, through `probe_hold::around_role` for a role's probe. Core's call is then the only opener; the gap between the close and Core's own open is **not covered**.

**A vendor backend** (`nrfutil`, J-Link) runs inside the same close; `around(.., Use::VendorTool, ..)` logs a warning that the probe is not held while the tool runs. **Not covered:** that window, the gate's and the attach's opens inside any Core call, and `POST /probes/enroll` with no `probe_serial` (it picks the one attached probe, unknown until it opens it, so a held enrolled probe can be the one it opens). A second connection that takes the probe in a window makes Core's reopen fail: logged, and the probe leaves the hold and the record.

**The signed record** lists the probes held at sealing under `observed.probes_held` ([../interfaces/signing.md](../interfaces/signing.md)), sorted serials, `[]` for none. A probe closed for a call's window still counts.

**Under test** a fake opener counts opens and live handles: one open at the take, a close and a reopen per call, a vendor window closed before the tool and reopened after (also on error), a release during a call not undone, and a role-keyed gate (validation, the dev-bench gate) closing its board's probe and reopening it. **[unverified on hardware]:** real probes (J-Link, CMSIS-DAP, ST-Link) and whether a second Core's open fails while Core holds one (debt in `tasks/core/184`). A fix that closes the windows needs `embarch-topology` to accept a probe the caller already opened.
