# 011 — The `embarch-topology` CLI performs four hardware and store mutations that two recorded decisions place inside Core

**State:** open
**Source:** suite review pass 2026-09-06, dimension 4 (layering and dependency direction). Code-confirmed.
**Scope:** topology
**Hardware:** none. The change is a routing decision in the CLI; confirming the wsl-host store divergence on the real machine needs the owner's session, but the flaw was found by reading two `#[cfg]` arms and needs no board to fix.
**Owner:** no

## What

`embarch-topology`'s own CLI is the last surface outside Core that links `probe-rs`/`serialport`,
and it still performs four mutations that this crate's own decision record says belong to Core:

- `bin/main.rs:162` → `hardware::enroll`
- `bin/main.rs:168` → `validate_role`
- `bin/main.rs:180` / `:184` → `set_dev_bench_link_port_serial` / `..._interface`

The rule is written down, and was enforced against every *other* surface.
`embarch-topology/decisions/enrollment.md:15`: *"real hardware I/O and the system-file write it
produces should be done by Core, **which already does exactly that under its own hardware lock.**
A second process calling the identical function **does not share that lock**… This crate's UI
reverted to fully read-only."* `embarch-core/decisions/surfaces.md:30` repeats it verbatim for
Core's retired enroll page. `embarch-core/interfaces.md:12` confirms `/probes/enroll`,
`/validate` and `/dev-bench/link` all take `hw_lock`, and
`embarch-core/decisions/platform.md:46` confirms the lock is `Arc<Mutex<()>>` — in-process only,
so it cannot see a second process at all.

**Two concrete consequences.** Run the CLI while Core is mid-flash and two processes hold one
probe with no lock, no queue and no message. And on the suite's one validated topology the CLI
writes a *different store than Core reads*: `src/hardware/paths.rs:16-27` resolves
`#[cfg(windows)] %ProgramData%\embarch` and `#[cfg(unix)] /var/lib/embarch`, so
`embarch-topology enroll` run from WSL lands in `/var/lib/embarch/topology/enrollment.toml` while
the Windows-service Core reads `%ProgramData%\embarch\topology\enrollment.toml`. The same applies
to `validate`'s durable alert, which lands in an `alerts.jsonl` nothing serves.

Candidate direction: reads may stay in-process — they are diagnostics, and
`resolve_dev_bench_port`/`recent_alerts` are fine. A **mutation** should reach the process
holding the lock and owning the store, through Core's three existing endpoints, or refuse with the
reason when a Core is reachable and this is not it. The crate already computes the class
(`resolve_software_topology`) and `embarch-topology status` prints `wsl-host` in the same second.
Keep the local-bootstrap case working — which is why this is a property and not a rewrite, and
the worker should design the fallback.

## Why now

`tasks/topology/004` is queued to add a **fifth** mutation to this surface, and the owner runs
this CLI by hand on the bench (that task records it). The `cargo tree -e normal` guards the suite
relies on were written for api/ui/umbrella and cannot see this: topology legitimately owns the
hardware feature, and decision 8 justifies the CLI as *one implementation* of the logic, which is
true and says nothing about which process or which machine runs it.

## Done when

- [ ] No `embarch-topology` CLI subcommand opens a probe or writes the enrollment store in its own
      process while a Core owns them, or the case where it must is named with its reason.
- [ ] Running `enroll` / `validate` / `set-dev-bench-link` from WSL on a `wsl-host` machine
      affects the store Core reads, or says why it cannot.
- [ ] `decisions/enrollment.md` decision 15 no longer reads as though the rule were fully applied.
- [ ] Gate green; `changelog.d/topology-*` fragment.
