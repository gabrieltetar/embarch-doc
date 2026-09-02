# embarch-outpost: open questions

**Status:** active, 2026-09-02.

Current truth: [spec.md](spec.md). Rationale: [decisions.md](decisions.md).

## The one binding number

- **A burst still overruns the ring under real study load, and the only lever left is the record's size.** A real capture's bursts lose **19.7% of their records across three honestly-drawn gap bands while the link averages 36% busy** — average capacity has never been the constraint. Every cheaper lever is already in: self-exclusion, the fill wait, and the ring at 2048 slots, **which cannot grow further on this DUT** (40 KB against a build already at 81.75% of 256 KB).

  A record costs **9.92 bytes**, and the two largest contributors are both absolute 32-bit values in five-byte varints — the cycle count, and `a` when it is a RAM pointer. Decision 4 rejected a per-record cycle delta **for a reason entirely about emit-path cost, not wire cost**; that reasoning is still correct and **no longer relevant**, since the delta would be computed at drain time. **It is a layout-4 change and is deliberately not made yet.**

## Unmeasured

- **The emit path's own cost is still not measured**, and it is the half that matters most. The *CPU* half is measured — the outpost is 1.6% of a quiet capture — but that counts the drain thread's runs, not the cycles each hook spends inside a context switch or an ISR wrapper. Those are the cycles charged to the path being measured, and nothing has counted them.
- **Whether the manifest reaches a Core running on another machine.** It rides the firmware-artifact path and **inherits that path's gap unchanged**: a remote Core cannot see a local file. Named rather than discovered later.

## Structural, and priced

- **A DUT flashed out-of-band from a *dirty* tree carrying the same `-dirty` string still decodes against the wrong manifest.** That is the one residual hole in the two-mechanism check, it is narrow, and **it is the price of not patching a CRC into the linked image.** If it ever bites for real, the post-link stamp is the known fix and the manifest decision is the record of why it was not paid for up front.
- **Self-exclusion leaves an interval no lane covers** — 1.6% of the reference window — which lands in the load summary's unaccounted total. *Rejected for now: coalescing the drain thread's run into one "the instrument ran here" record.* It would close the hole honestly, and costs a new record kind, three host decoders and a layout bump for something the header flag plus the unaccounted total already communicates. Revisit if the hole confuses a reader in practice.
- **The ISR half of self-exclusion excludes the whole vector**, so anything sharing it goes too; and it needs the devicetree IRQ number to equal the Cortex-M vector number, so it compiles out under multi-level interrupts rather than comparing against an encoded number that does not match.
- **A thread whose `struct k_thread` is a member of something at a non-zero offset is not found.** No build in this suite has one, and finding it would mean claiming an address the kernel was never handed. An image with **no DWARF** falls back to the name match, which resolves 5 objects of 20 — and which path ran is recorded in the manifest's notes.
- **The DUT's clock can go backwards for two unrelated reasons**, and only one is a defect. A hook reads the counter and *then* reserves its ring slot, so an interrupt preempting that window is stamped before the thread it preempted — a real capture showed one such step of **13 µs**, and a host **must tolerate it**, since refusing the clock over it would refuse every real capture. A step longer than the whole capture means the counter *restarted*, and the test is the other clock rather than a threshold. Core now discards a stale pre-reset prefix on open, though [that clear is not sufficient](../embarch-core/open.md).

## Deferred with a named trigger

- **A `doctor`-style staleness check for the DUT**, mirroring the one that already exists for dev-bench firmware: the running firmware reports its outpost version and build ID, and that could be compared against the module revision checked out. **Not built; named because the mechanism is now free.**
- **A vendor-neutral portable core with a porting layer.** Genuinely wider reach, and genuinely more design for a reach nothing needs — both real DUT firmware repos in play are Zephyr. **Revisit when a non-Zephyr DUT is real, not before.**
