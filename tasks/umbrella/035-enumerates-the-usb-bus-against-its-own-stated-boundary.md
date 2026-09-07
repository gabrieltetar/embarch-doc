# 035 — `embarch-umbrella` walks `/sys/bus/usb/devices` with its own nine-entry probe-vendor table, in the component whose spec and manifest both say it holds no hardware knowledge

**State:** open
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

- [ ] `embarch-umbrella`'s manifest comment and `spec.md:17` are true, exception and reason
      included, or check 5 no longer enumerates hardware in umbrella's own process.
- [ ] A probe vendor ID is named in one place in the suite, or the two places say why they differ.
- [ ] Gate green; `changelog.d/umbrella-*` fragment.

**If the fix turns out to need `embarch-topology` or `embarch-core`,** that crosses a repo
boundary and belongs back in `inbox/` as `Scope: suite` rather than being reached for.
