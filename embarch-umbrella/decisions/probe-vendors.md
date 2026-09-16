# embarch-umbrella decisions: Where a probe-vendor fact belongs

**Status:** active, 2026-09-11.

**New file, not squeezed into [doctor.md](doctor.md).** That file is 11,082/12,288 B — 1,206 B
left, in reserve with its own compaction parked (`tasks/umbrella/048-compact-umbrella.md`) — and
[DOC-BUDGET.md](../../DOC-BUDGET.md)'s split-first rule makes a sibling topic file the default
remedy, squeezing the exception. `umbrella/020` and `umbrella/050` both set that precedent
([DOC-COMPACTION.md](../../DOC-COMPACTION.md) §2). This decision is adjacent to
[decision 18](doctor.md) — it is about check 5's vendor-ID list — but it settles a different
question: not what check 5 concludes, but **which repo is entitled to hold the table it concludes
from.**

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md)'s
"two named exceptions" clause, and `doctor.rs`'s `DEBUG_PROBE_VENDOR_IDS`.

### 49 — `embarch-umbrella` keeps its own debug-probe vendor-ID table, because it is not the same fact `embarch-topology` holds

**The question, as it was asked.** `embarch-umbrella`'s `doctor` check 5 judges USB devices against
its own nine-entry `DEBUG_PROBE_VENDOR_IDS` ([decision 18](doctor.md)), and
`embarch-topology/src/hardware/port.rs` holds three of its own — the shape of a drift bug. Does check
5's list move into `embarch-core`/`embarch-topology`, or stay, and why?

**The premise is false, and that is the answer.** The two lists are not two copies of one fact. They
are two different facts that happen to share one number.

| | `embarch-umbrella`'s nine | `embarch-topology`'s three |
|---|---|---|
| **Question it answers** | is this USB device a **debug probe**? | which enumerated **serial port** is the link? |
| **Consumer** | one `doctor` message | `Filter::resolve`, on every flash/reset/handshake |
| **Read from** | `/sys/bus/usb/devices/*/idVendor`, unprivileged | `serialport`'s enumeration |
| **Cost of a wrong entry** | a misleading warn/fail in a diagnostic | the wrong port; a bench that flashes and times out |

**One value is in both — SEGGER's `0x1366` — and it means something different in each.** In
umbrella it means *this device is a debug probe*; in topology it means *this serial port belongs to a
J-Link's VCOM*, which is why `SILABS_VID` sits beside it although, as `port.rs`'s own doc comment
says, that chip "has no JTAG/debug capability at all". **A list containing a VID that is deliberately
not a probe is not a probe-vendor table**, so there is no shared fact to route: changing one list
correctly would usually be wrong for the other.

**What routing it to `embarch-core` would actually cost.** The technical route exists —
`embarch-umbrella` already path-depends on `embarch-topology` — so this is declined on grounds, not
on impossibility. **The load-bearing cost is a confident verdict about the wrong machine**: check 5
already refuses to scan on `wsl-host` or `remote`, because Core enumerates on one computer and this
host's bus is another (`UsbScan::CoreElsewhere`); routing the *table* to Core moves the scan to the
machine the operator is not sitting at, the direction that makes it worse. A secondary cost: Core's
own probe surface, `probe_rs`'s `Lister`, is the same enumeration check 5 exists to catch the gap in,
so a Core endpoint would inherit it. The fix line check 5 emits — a udev rule — is a fact about the
machine running `doctor`, not about Core.

**What makes keeping it safe, as a rule.** A fact whose wrongness produces a wrong diagnostic belongs
where the diagnostic lives; a fact whose wrongness produces wrong hardware behaviour belongs in the
crate that owns hardware. Umbrella's nine VIDs are load-bearing for one sentence of prose; topology's
three decide which port a study talks to.

**What would change this answer — a trigger, not a hedge.** It moves if **anything other than
`doctor`'s own message consumes the list**, or a check is ever built that needs umbrella's answer and
Core's enumeration to *agree* (which would make them one fact). Neither is true today or planned.

**Two things this deliberately does not settle**, both still in [`../open.md`](../open.md):
**whether the nine vendor IDs are the right nine** — unmeasured, and a question about the list's
*contents*, not its *home* — and **whether the not-permitted fail works**, never exercised against a
real permission-denied probe. Keeping the table here does not make either less owed.

*Rejected: move it to `embarch-core`.* Nothing to route, and the wrong-machine cost above. *Rejected:
extract a shared vendor-ID crate.* The two lists disagree on purpose — a shared table containing
`SILABS_VID` would make umbrella report a USB-UART bridge as a debug probe, and excluding it would
break topology's port selection. *Rejected: leave it undecided.* That is the state this replaces.
