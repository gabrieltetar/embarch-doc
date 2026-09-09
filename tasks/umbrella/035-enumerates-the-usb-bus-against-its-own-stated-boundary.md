# 035 — `embarch-umbrella` walks `/sys/bus/usb/devices` with its own nine-entry probe-vendor table, in the component whose spec and manifest both say it holds no hardware knowledge

**State:** claimed — leg 060, 2026-09-09, `agent/umbrella/035-usb-boundary`
**Source:** suite review pass 2026-09-06, dimension 4 (layering and dependency direction). Code-confirmed.
**Scope:** umbrella
**Hardware:** none
**Owner:** no

## What

Two identical boundary claims:

- `embarch-umbrella/Cargo.toml` — *"Deliberately absent, and expected to stay absent: probe-rs and
  serialport. **Umbrella holds no hardware knowledge — every hardware-facing capability is a
  shell-out to embarch-core or an HTTP call to its endpoints.**"*
- `embarch-umbrella/spec.md:17` — *"It never links `probe-rs` or `serialport` … **Every** capability
  it appears to have is a shell-out to `embarch-core` or `embarch-api`, or an HTTP call to Core."*

Neither is true of `doctor` check 5. `src/doctor.rs:687` defines `SYSFS_USB_DEVICES`, `:689-708`
defines `DEBUG_PROBE_VENDOR_IDS` — nine vendor IDs meaning *"this is a debug probe"* — and
`:734-779` walks the bus in umbrella's own process. Hardware knowledge, no shell-out, no HTTP.

That also makes umbrella the suite's **second** holder of a probe-vendor fact:
`embarch-topology/src/hardware/port.rs:41,52,60` holds three link VIDs, measured against real
silicon, each with a doc comment explaining why (including why Espressif's is JTAG-only).
Umbrella's `open.md` concedes *"Whether the nine vendor IDs are the right nine is also
unmeasured."*

The `cargo tree` guard everyone cites cannot see this: sysfs is `std::fs`, not a dependency.

Candidate direction: two honest ends, and a worker in this repo can reach either. Correct the two
claims to state their one exception with its reason — which is the minimum and is entirely
umbrella's — or route the question to the process that owns the probe, which is what
`embarch-core` is for. **What must not remain is a stated boundary that the behaviour contradicts.**

## Why now

`embarch-umbrella/decisions/doctor.md` decision 18 justifies *the check* — discovering a permission
problem in `doctor` rather than at flash time, which is sound — and never asks where the list
should live or whether Core should answer it. An engineer whose probe vendor is missing has to work
out which of two repos holds the list, and a reader of either boundary claim is being told
something false.

## Done when

- [x] `embarch-umbrella`'s manifest comment and `spec.md:17` are true, exception and reason
      included, or check 5 no longer enumerates hardware in umbrella's own process.
- [x] A probe vendor ID is named in one place in the suite, or the two places say why they differ.
      (Named in two places, each now stating why it holds its own — umbrella's spec.md/open.md
      say check 5 is a permission-detection exception; the routing question of whether it should
      collapse to one place is filed to `inbox/`, `Scope: suite`.)
- [x] Gate green; `changelog.d/umbrella-*` fragment.

## Closed by leg 060 (burndown)

Took the first honest end per the dispatch note: corrected `Cargo.toml` and `spec.md:17` to state
check 5's sysfs USB read as the one named exception, with its reason (decision 18) and the
unmeasured-vendor-IDs caveat carried into `open.md`. Did not touch check 5 itself, `embarch-topology`,
or `embarch-core`. Filed the routing-to-Core question as `inbox/suite-route-probe-vendor-ids-to-core.md`
(`Scope: suite`) — **a numbered `embarch-umbrella` decision on where the probe-vendor fact belongs is
owed** and not authored here per the burndown constraint. `spec.md`'s correction fit in the 456 B
of reserve left (used 278 B, file now 10062/10240 B); `open.md`'s fit in its 490 B (used 240 B, file
now 4870/5120 B). Neither file needed the `038` compaction pass.

**If the fix turns out to need `embarch-topology` or `embarch-core`,** that crosses a repo
boundary and belongs back in `inbox/` as `Scope: suite` rather than being reached for.

## Supervisor's dispatch note, leg 060 (burndown)

**Take the first of the two honest ends, not the second.** Correct the two boundary claims —
`embarch-umbrella/Cargo.toml`'s comment and `embarch-umbrella/spec.md:17` — to state their one
exception with its reason, and leave check 5 where it is. Routing the probe-vendor question to Core
is the better long-term shape and it is **explicitly out of scope tonight**: it needs a numbered
decision, which [burndown.md](../../../embarch-fleet/burndown.md) forbids this leg, and it reaches
`embarch-core`, which you do not own. **File the routing question as an `inbox/` drop with
`Scope: suite`** — the task's own last paragraph tells you to — and say in your report that a
numbered `embarch-umbrella` decision on where a probe-vendor fact lives is owed.

**Do not claim the nine vendor IDs are right.** `open.md` already concedes they are unmeasured;
carry that caveat into whatever you write, and do not promote it to a measured fact. Second
holder of the same fact is `embarch-topology/src/hardware/port.rs` (three link VIDs, **measured**) —
you may *name* that divergence in the corrected text; you may not edit that repo.

**Doc reserve for `umbrella`, and it constrains you directly:**

- `embarch-umbrella/spec.md` — **9784/10240 B, 456 bytes left**, and `spec.md:17` is precisely the
  line you have to rewrite. Its compaction task
  `tasks/umbrella/038-compact-umbrella.md` is **blocked on `In flux: yes`** (it unparks when
  `tasks/umbrella/033` lands), so nobody else can touch it. **If your correction does not fit in 456
  bytes, compact `spec.md` as part of this unit**, carrying `038`'s `Must not delete:` list verbatim
  — the `doctor` chain table's designed-vs-built distinction **per row**, the `status` row's
  five-state list and its "never a probe count of `0`" clause, and whatever `009`'s list still names
  unanswered — and closing **only** `spec.md`'s item on `038`. **Prefer a split over a squeeze**
  ([DOC-COMPACTION.md](../../DOC-COMPACTION.md) §2); `038` says a 37 B wording shave is not a real
  shave, and this repo has four recorded instances of a squeeze cutting something load-bearing.
- `embarch-umbrella/open.md` — 4630/5120 B, **490 bytes left**, same parked task. Same rule.
- `embarch-umbrella/decisions/bind.md` — 879 bytes left, parked under `tasks/umbrella/009`. Avoid.

**No hardware.** Do not run `doctor`, do not enumerate the real USB bus, do not touch a live Core.
