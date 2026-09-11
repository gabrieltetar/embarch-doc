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
`embarch-topology/src/hardware/port.rs` holds three vendor-ID constants of its own. Two sub-projects
holding independent vendor-ID lists with no stated relationship is the shape of a drift bug: an
engineer whose probe is misidentified has to guess which repo to fix, and the one that does not get
fixed silently falls out of step. So: does check 5's list move into `embarch-core`/`embarch-topology`,
or does umbrella keep it, and why?

**The premise is false, and that is the answer.** The two lists are not two copies of one fact. They
are two different facts that happen to share one number.

| | `embarch-umbrella`'s nine | `embarch-topology`'s three |
|---|---|---|
| **Question it answers** | is this USB device a **debug probe**? | which enumerated **serial port** is the link? |
| **Consumer** | one `doctor` message | `Filter::resolve`, on every flash/reset/handshake |
| **Read from** | `/sys/bus/usb/devices/*/idVendor`, unprivileged | `serialport`'s enumeration |
| **Contents** | SEGGER, CMSIS-DAP, ST-Link, LPC-Link2, EDBG, RPi Debug Probe, Black Magic, XDS110, ULINK | `SEGGER_VID`, `ESPRESSIF_VID`, `SILABS_VID` |
| **Cost of a wrong entry** | a misleading warn/fail in a diagnostic | the wrong port; a bench that flashes, boots, runs and times out |

**One value is in both — SEGGER's `0x1366` — and it means something different in each.** In
umbrella it means *this device is a debug probe*. In topology it means *this serial port belongs to a
J-Link's VCOM*, which is why `SILABS_VID` sits beside it although, as `port.rs`'s own doc comment
says, that chip "has no JTAG/debug capability at all", and why `ESPRESSIF_VID` is there while being
explicitly **not** a link candidate. **A list containing a VID that is deliberately not a probe is
not a probe-vendor table.** `links-port.md` decision 24 is the same crate being careful about
precisely this: it added a fourth `detected_by` constant because labelling a result `vid-match` when
the VID gate never ran named a rule that did not happen.

So there is no shared fact to route, and no drift to prevent: changing one list correctly would
usually be wrong for the other.

**What routing check 5's list to `embarch-core` would actually cost, taken on its merits.** The
technical route exists — `embarch-umbrella` already path-depends on `embarch-topology` — so this is
declined on grounds, not on impossibility:

- **The natural way for Core to answer it is the under-reporting way, though not the only way.**
  Check 5 exists because probe enumeration *silently under-reports* a probe nobody has permission to
  open; its whole mechanism is that sysfs attributes are world-readable while `/dev/bus/usb/...` is
  the node a udev rule grants ([decision 18](doctor.md)). Core's existing probe surface is
  `probe_rs`'s `Lister` — exactly the enumeration whose gap this check was built to expose — so a
  Core endpoint answering "which probe vendors do you see" over that surface would inherit the blind
  spot. **This is a statement about the path of least resistance, not a structural impossibility**:
  `/sys/bus/usb/devices` is as readable from Core's process as from umbrella's, and Core could carry
  a second, parallel sysfs reader. That option is rejected on its own terms — it is the same fifty
  lines relocated, for no architectural gain, into a process on a machine the operator may not be
  sitting at. **The argument below about the wrong machine is the load-bearing one; this bullet is
  a cost, not a proof.**
- **It would risk a confident verdict about the wrong machine.** Check 5 already refuses to scan on
  `wsl-host` or `remote`, because Core enumerates on one computer and this host's bus is another —
  `UsbScan::CoreElsewhere` exists for that, and [decision 31](doctor.md) names it as check 14's
  mistake with a different peripheral. Routing the *table* to Core does not remove that hazard; it
  moves the scan to the machine the operator is not sitting at, which is the direction that makes it
  worse.
- **The permission question is about the user running `doctor`, not about Core.** The fix line check 5
  emits is a udev rule for *this* user. That is a fact about the machine `doctor` runs on.

**What makes keeping it safe, stated as the rule rather than as this instance.** **A fact whose
wrongness produces a wrong diagnostic message belongs where the diagnostic lives; a fact whose
wrongness produces wrong hardware behaviour belongs in the crate that owns hardware.** Umbrella's
nine VIDs are load-bearing for one sentence of prose and nothing else — a wrong entry makes `doctor`
say "no probe found" where it could have said "attached but not permitted", which is the warn the
check already replaced and not a regression past it. Topology's three decide which port a study
talks to. `spec.md`'s "never links `probe-rs` or `serialport`" boundary is intact either way: check 5
reads a text file.

**What would change this answer — a trigger, not a hedge.** It moves if **anything other than
`doctor`'s own message ever consumes the list**, or if a check is ever built that requires
umbrella's answer and Core's enumeration to *agree* (which would make them one fact, and one fact
belongs in one place). Neither is true today and neither is planned.

**Two things this deliberately does not settle**, both still in [`../open.md`](../open.md):
**whether the nine vendor IDs are the right nine** — unmeasured, and a question about the list's
*contents*, not its *home* — and **whether the not-permitted fail works**, never exercised against a
real permission-denied probe. Keeping the table here does not make either less owed.

**What carries this decision, stated plainly so a later reader does not lean on the wrong leg.**
The *sufficient* argument is the first one: **there is no shared fact to route.** Everything after it
is cost, and the strongest of those costs is the wrong-machine hazard, not the blind-spot one — which
a reviewer correctly cut down to size before this was committed.

*Rejected: move it to `embarch-core` and have check 5 call it.* Nothing to route (the two lists are
different facts), and the costs above — chiefly answering about the wrong machine. *Rejected: extract a shared vendor-ID crate.* It would have to merge two lists
that disagree on purpose — a shared table containing `SILABS_VID` would make umbrella report a
USB-UART bridge as a debug probe, and one excluding it would break topology's port selection.
*Rejected: leave it undecided and keep the `open.md` caveat.* That is the state this replaces; a
routing question nobody has answered gets re-asked by the next reader of either file.
