# 188 — Every probe open steps around Core's own hold

**State:** claimed by agent/core/188-every-probe-open-steps-around-cores-own-hold, 2026-11-27 00:43
**Source:** EMB-592 — Validation and the dev-bench gate open a probe Core is holding (reviewer finding on `core/184`)
**Issue:** EMB-592
**Scope:** core
**Hardware:** verify-only
**Owner:** no

## What

Decision 159 (`core/184`, merge `576cb04`) has Core open each enrolled board's
probe at lease take or study start and keep it open. `hardware::flash`,
`hardware::reset`, `live::with_core` and `live::read_dhcsr` run inside
`probe_hold::around`, which closes the held probe for the call and reopens it
after. Other paths still open the same probe through `embarch-topology`'s
identity gate with no `around`, so they run against Core's own hold:

- `src/api.rs` `POST /validate`: `validate_role_timed` and
  `validate_serial_timed` (around lines 2466 and 2473).
- `src/test_executor.rs` (around lines 570 and 571).
- `src/study.rs`: the dev-bench identity gate, `validate_role` (around 1287),
  and around 1391 and 1568. A study takes its own hold after this gate
  (`study_started`, around 1738), but under a lease the lease's hold is already
  live when the gate runs.

On a probe that allows one open per host, validation under a lease and every
study started under a lease would fail against Core's own hold. Whether a
second open fails on each probe kind is unmeasured.

When this is done: every Core path that opens a held probe runs inside
`probe_hold::around`, or decision 159 names it as uncovered with its reason
and what it does against a held probe. Search for every caller of the
topology identity gate and of the probe opener, not only the lines above: the
reviewer's list came from one reading.

**Not yours:** `embarch-topology` (its identity gate opens the probe itself;
that stays as it is) and every other repo. You never touch hardware.

## Where to look

- `src/probe_hold.rs` (`around`, the fake opener the tests use), the four
  wrapped sites in `src/hardware.rs` and `src/live.rs`
- the sites above in `src/api.rs`, `src/test_executor.rs`, `src/study.rs`
- `embarch-doc/embarch-core/decisions/port-hold.md` (130, 159)

## Where the doc goes

Amend decision 159 in place (`decisions/port-hold.md`, 6,123 B, room): its
list of covered calls, and any site left uncovered with its reason.
**`interfaces/hardware.md` is 11,055 of 12,288 B, 4 B under its reserve
line**: do not grow it; if you must, file
`tasks/core/<NNN>-compact-core.md` in the same commit (`tasks/README.md` has
the shape; number from `scripts/check-task-numbers.py --next core`).
`open.md` is 3,916 B, also 4 B under its reserve line: net-neutral or smaller.
`spec.md` is in reserve and filed against `tasks/core/186`: do not grow it.

## Done when

- [ ] Every site above runs inside `probe_hold::around`, or 159 names it as
      uncovered with its reason.
- [ ] A test with the fake opener shows `POST /validate` under a lease, and a
      study's dev-bench gate under a lease, closing and reopening the held
      probe.
- [ ] The task's hardware-verification debt names validation under a lease and
      a study start under a lease, on a real J-Link and a CMSIS-DAP or ST-Link.
- [ ] Gate green (`cargo build`, `cargo test`, `cargo clippy --all-targets --
      -D warnings`); `changelog.d/` fragment.
