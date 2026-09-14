# 041 — Decision 32's amendment and `open.md`'s bullet both went false when `core/055` landed

**State:** claimed by agent/topology/041-close-decision-32, 2026-09-13 19:18
**Source:** `inbox/topology-close-decision-32-open-19-after-core-055.md`, filed by `core/055`'s
worker at landing per that task's "Flag back, do not fix" — a `core` worker may not write
`embarch-topology`. Filed into the queue by the leg of 2026-09-13 18:5x.
**Scope:** topology
**Hardware:** none — a doc-text correction, nothing executed.
**Owner:** no

## What

`core/055` landed 2026-09-13 (code `86345c01a451b0696af36f42c28bf6676478124c` in `embarch-core`):
`resolve_probe` (`embarch-core/src/hardware.rs`) now calls
`embarch_topology::hardware::select_probe` and keeps no inline copy of the probe-selection rule,
threading `"flash"`/`"reset"` as the `action` verb (new `embarch-core` decision 61).

That closes the one thing `embarch-topology` decision 32's 2026-09-13 amendment and `open.md`'s
matching bullet were still waiting on. Both currently say `embarch-core::resolve_probe` **"still
keeps its own copy"** and name `tasks/core/055` as blocked on the topology landing. **Both
sentences are now false.**

## Why now

Decision 32's amendment and the `open.md` bullet each explicitly named `tasks/core/055` as the
remaining half of the close, so both need a dated update the moment it lands rather than later.
This is the exact class four consecutive citation sweeps this week found their real yield in — a
citation whose number still resolves inside a sentence that has gone false — except here it is
known in advance rather than discovered, which makes leaving it the more expensive choice.

**Read the landed `embarch-core` side before writing the correction**, at
`/home/gabriel/Github/embarch/embarch-core/src/hardware.rs`, rather than taking this task's word
for what it does. Decision 32's close should record what `core/055` actually did, including the
`action` threading, not merely that something landed.

## Done when

- [x] `embarch-topology` decision 32 gets a dated note (or a further amendment) recording that
      `core/055` landed and `embarch-core::resolve_probe` now calls `select_probe` — the
      duplication decision 32 opened is fully closed on both sides.
- [x] `open.md`'s matching bullet ("A third instance of the same class is half-closed…") is
      removed or corrected to say the instance is now fully closed.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `changelog.d/` fragment.

## Closed 2026-09-13

Read `embarch-core/src/hardware.rs` directly (commit `86345c01a451b0696af36f42c28bf6676478124c`)
rather than taking this task's word: `resolve_probe` now just enumerates probes with
`Lister::list_all()` and delegates to `embarch_topology::hardware::select_probe`, threading a
caller-supplied `action` (`"flash"`/`"reset"`, mirroring `enroll`'s own `"enroll"`) through
`resolved_serial`/`open_probe` so the multi-probe refusal names the right verb for each caller —
`embarch-core` decision 61. No inline copy of the selection rule remains in either crate.

Added a short closing paragraph after decision 32's existing 2026-09-13 amendment (kept, not
replaced — the amendment still records what `038` alone had closed) rather than rewriting it.
`decisions/crate.md` landed at 12075/12288 B (213 B to spare) — the amendment fit inside
`612` B of headroom without touching `tasks/topology/039`'s size debt, so that task is untouched
in this unit. Removed `open.md`'s matching bullet outright (the instance it tracked is fully
closed, and `open.md` is unresolved-only), rather than rewording it in place.

Note for whoever next reads `tasks/topology/039`: both of its own "Done when" landing conditions
(`tasks/core/055` landed; decision 32 marked closed) are now true, so it can unpark — this unit
did not touch it, since its own condition ("if it does not fit, pay part of `039`") did not fire.

## Reserve, for planning

`embarch-topology/decisions/crate.md` is 11,676/12,288 B — **612 B left, 95.0%** — filed against
blocked `tasks/topology/039`, whose size debt is due **2026-09-20**, the soonest date on the whole
ledger. **Decision 32 lives in `decisions/crate.md`**, so this unit writes into the second-most
pressured file in the suite: keep the amendment to one or two sentences, and if it does not fit,
**the correction still has to happen** — say so and pay part of `topology/039` in the same commit,
carrying its `Must not delete:` list.
