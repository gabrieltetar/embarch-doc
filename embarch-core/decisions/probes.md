# embarch-core decisions: Probes, board identity, and chip mapping

**Status:** active, 2026-09-02.

Which physical probe a call means, whether it is still wired to the board its config claims, and how a Zephyr SoC name becomes a probe-rs target.

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

---


## Chip mapping

### 8, 34 — The SoC→chip table lives here, compiled in, plus `chip-list` as its human fallback
`embarch-api` is about to call `/flash` anyway, so resolving here costs nothing extra and keeps one copy in the one process that links probe-rs and can therefore validate a mapping against the real target database rather than trusting a hardcoded string. Matched case-insensitively and **exactly**: a plausible-but-wrong fuzzy match would silently pick the wrong physical target. A test checks every entry against the real registry, so drift fails a test run rather than a live call. `chip-list [filter]` exposes that same in-process database, because finding a probe-rs target name for an unmapped SoC otherwise meant `cargo install probe-rs-tools` — a toolchain install in the middle of a download-a-binary onboarding. *Not a UI dropdown instead*: that needs an endpoint too, so it is strictly more work and can be layered on this.

**The table is a source `const`, and that is the whole configuration story** (amended 2026-09-05). Until then this entry grounded `chip-list` in *configuring an override*, and pointed at a per-project `embarch-api` field to put the answer in. That field — [`embarch-api`](../../embarch-api/decisions/zephyr.md) decision 13's `soc_chip_overrides` — was **retired unbuilt on 2026-09-05**, and a config still declaring it now fails at load. So the remedy `chip-list` feeds is unchanged in substance and different in destination: run it, then add the SoC/target pair to `SOC_TO_CHIP` in `chip_resolve.rs`, rebuild and redeploy. `chip-list` itself is untouched — it produces exactly the string the new remedy asks for.

***Rejected: give the table a config path here instead***, so an unmapped SoC needs no rebuild. It is the same escape hatch `embarch-api` 13 just retired, moved one repo over, and it re-opens the hole that retirement closed: a config-supplied mapping consulted before the table would bypass the registry validation this entry's first paragraph exists for. 13's tombstone already names **a Core the operator cannot rebuild** as the condition that reverses it — this suite rebuilds and redeploys Core routinely, so the rebuild requirement is a recorded choice, not a gap. Reverse *that* first, and the hatch belongs in Core's own machine-scoped config and still registry-validated. What this amendment fixes is only the text: `chip-list --help` and two `chip_resolve.rs` comments had gone on naming a field that no longer exists, sending an operator to write a key that stops `embarch-api` starting.

---
