# embarch-core decisions: Probes and board identity

**Status:** active, 2026-09-02.

Which physical probe a call means, and whether it is still wired to the board its config claims. Chip mapping and the attach guards (8/34, 80, 89): [chip-mapping.md](chip-mapping.md).

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).


## Probe selection and board identity

### 9 — `open_probe(probe_serial)`, and ambiguity is a named error
Dev-bench *is* a second debug probe, so "more than one attached" is the normal state. More than one with no selector returns an error listing every candidate rather than picking — a wrong-target flash is worse than a loud failure. A `500` not a `400`, since the ambiguity is only discoverable once enumeration runs. This decision described itself as implemented for months while the code still had only single-probe selection; found the first time two probes were genuinely attached, when flashing picked the wrong one.

### 22 — A probe/board identity gate, because a label can go stale with nothing to notice
`probe_serial` says *which probe*; it says nothing about whether that probe is still wired to the board its config **labels** it as. That label is, and can only be, a human's one-time act of physically isolating a board and noting its serial — nothing in a USB descriptor says "I'm wired to the DUT". It goes stale silently when a probe is moved during rework, and `attach(chip)` structurally cannot catch a same-family mismatch the way it catches the wrong architecture.

So a machine-local table keyed by probe serial, holding the chip's own factory-burned ID **read live over the debug port** — independent of which probe or cable answers, so it survives a probe being moved in a way a serial cannot. Enrollment refuses anything but exactly one attached probe: that refusal *is* the enforcement behind "plug in only the board you mean, then confirm". `flash`/`reset`/the handshake compare live against recorded and **fail closed**, naming both values. A role-keyed variant exists because a plain UART bridge has no JTAG capability, so it can never be an enrollment candidate.

*Rejected: an interactive popup at flash time* — Core is a service, so Session-0 isolation needs a second always-running helper plus IPC, and it degrades wrongly for a headless Pi. **Moved wholesale into `embarch-topology`**, because the stale-serial incident that motivated that crate *is* this mechanism's own override path going stale.

### 23 — The four dev-bench env overrides are gone, with no replacement knob
They were the mechanism behind the incident that motivated `embarch-topology`. Removed, not deprecated: decision 22's enrollment fallback was always the stronger signal — a live hardware-ID readback rather than an operator-typed string.

### 26 — Diagnose an unpowered target before attaching
An unpowered board failed every attach with a low-level ARM access-port chain a human has to already know how to read. Core reads the probe's own sensed target voltage before `attach` and fails fast naming the likely cause. Best-effort, not a gate — not every probe supports the reading.

### 61 — `resolve_probe` delegates to `embarch_topology::hardware::select_probe`; `flash`/`reset` each pass their own verb
Decision 9's selection rule stopped being this crate's alone the moment decision 22 moved the board-identity gate into `embarch-topology`: `pub(crate)` couldn't reach the `enroll` counterpart that move left behind, so `enroll` re-implemented the rule from scratch and the two copies silently drifted (`embarch-topology` decisions 32/33 found three concrete divergences on `main` — the zero-probe usbipd hint, `len() > 1` vs `len() != 1`, and every error string — while decision 32 sat open for a session because closing it needed an edit on this side).

`embarch-topology` decision 33 reconciled the drift and exposed the result as `pub fn select_probe(probes, probe_serial, action)`. `resolve_probe` here now enumerates with `Lister::list_all()` and calls straight through to it, keeping no inline copy of the rule. Verified against the landed function before deleting anything, not assumed from the task that requested this: zero probes is checked first and unconditionally, and the usbipd hint (*"check the USB connection (and usbipd attach, if Core is on a Pi and the probe is elsewhere)"*) survives verbatim, additionally echoing the wanted serial when one was given — so the one genuinely diagnostic string either copy had is not lost, only reached through a call instead of a duplicate.

**`action` is threaded from each of `resolve_probe`'s two callers, not collapsed to one word.** `flash`/`reset` now pass `"flash"`/`"reset"` through `resolved_serial`/`open_probe`, so the multi-probe refusal reads *"flash requires exactly one debug probe attached … plug in only the board you mean to flash"* rather than a generic verb standing in for both. This is the same choice `embarch-topology` decision 33 made for `enroll`'s `"enroll"` (*"a caller-supplied noun over a single fixed wording"*) — with only two call sites in this crate, threading costs a second `&str` parameter down two short call chains, not a design fork, and the more specific message is a real improvement a shared generic word would have given up for nothing.

Not de-duplicated further into a single Core-side wrapper that hardcodes one verb: that would reintroduce exactly the divergence risk this decision closes, one crate over, the moment a third caller wanted a different word.

### 124 — A CDC control link is enrolled by its USB identity, through `POST /dev-bench/link`
`POST /dev-bench/link` ([enrollment.md](enrollment.md) decision 27) gains `control_port: {vid, pid, serial?, interface?}` and `clear_control_port: true`, both optional; a request without them behaves as before, and the contradiction of the two is a `400`. Recording one stores the port's USB identity in `embarch-topology` (its decision 50), which then finds the bench by it **alone**; with none recorded the SEGGER-VID path is untouched, so an enrolled bench keeps working. **A recorded identity that matches nothing is the same `404` an unplugged J-Link gets**, and one matching several ports (a composite device's control, samples and SMP ports share a serial) is refused as ambiguous until `interface` says which, never resolved to the first. `DevBenchLink::open` is unchanged: it still passes `DEV_BENCH_BAUD` and its hardware-flow-control request with the CTS fallback. **What a CDC ACM port does with that baud is not established by reading code**, and is owed to a bench run on the nRF52840 DK ([embarch-dev-bench](../../embarch-dev-bench/decisions/analog.md) decision 62). Measured: unit tests with fake enumeration only. *Rejected:* a second endpoint for the control port, which would split one declared link in two.

