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

- **The DUT's clock can go backwards for two unrelated reasons**, and only one is a defect. A hook reads the counter and *then* reserves its ring slot, so an interrupt preempting that window is stamped before the thread it preempted — a real capture showed one such step of **13 µs**, and a host **must tolerate it**, since refusing the clock over it would refuse every real capture. A step longer than the whole capture means the counter *restarted*, and the test is the other clock rather than a threshold. Core now discards a stale pre-reset prefix on open, though [that clear is not sufficient](../embarch-core/open.md).

  Three further structural limits are already settled, priced, and recorded where they were decided rather than restated here: the manifest's residual dirty-tree hole (`decisions/manifest.md` decision 9, *"What is genuinely given up"*), self-exclusion's uncovered interval and whole-vector ISR limit (`decisions/tracing.md` decision 19, *"What a host sees instead"* and *"Two limits, stated rather than discovered later"*), and the non-zero-offset thread miss (`decisions/naming.md` decision 8, *"What is still not covered"*).

## Deferred with a named trigger

- **This repo has no CI at all** — `.github/workflows` is empty, so nothing runs `tests/run-all.sh` on push, and the toolchain-free legs' now-fixed ordering (decisions/testing.md decision 22) is only ever exercised by a human remembering to. Whether `embarch-outpost` gets a workflow is a suite-scope call (`tasks/suite/021`), not this task's — filed there, not built here.

  Two more deferrals are already recorded, with their own trigger, at their decision rather than here: a DUT staleness check mirroring dev-bench's (`decisions/manifest.md` decision 9, last paragraph) and a vendor-neutral porting layer (`decisions/module.md` decision 1, its rejected alternative).
