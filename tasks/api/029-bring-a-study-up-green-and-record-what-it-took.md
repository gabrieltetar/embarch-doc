# Bring a study up green end to end, and record the sequence it actually took

**State:** open — half done and **not blocked**, see `## Progress 2026-09-06` at
the bottom. What it needs next is a board and one attribution the operator makes.
**Source:** owner's bench session 2026-09-06 — three other `bench` tasks depend on a study that runs; nothing records the bring-up sequence
**Scope:** api
**Hardware:** bench
**Owner:** no

## Roles this needs

`dut` and `dev-bench`. **Validate both before starting** (`../../embarch-fleet/protocol.md` §7).
If either is unattached, leave this `open` and say so once — do not mark it blocked.

## Bench facts — owner-supplied, do not infer or re-derive

- **DUT: `nff_dev` rev 6**, stated by the owner 2026-09-06. rev6 carries the **AS7058** PPG
  AFE; rev7 carries the MAX86178. **Never infer the revision from source** — if a step needs
  a revision-dependent fact this task does not give you, stop and say so.
- DUT console: **uart20, TX P1.05 / RX P1.04** (either revision).
- Dev bench: **nRF54L15DK**, link **COM17 / VCOM1, interface 2** — the *higher* interface,
  not the lowest. Enrolled with `link_port_interface=2`.
- Enrolled identities as of 2026-09-06: `dut` probe `000852006107`, hardware ID
  `834f2559f10a6cdf`; `dev-bench` probe `001057729826`, hardware ID `6fcddc36cb781b71`.
- **`ble speed fast` over NUS before any BDS step.** The DUT's HCI `0x08` failures are its own
  slow connection interval; without this a study dies around step 5, with it 14 of 14 pass.
- **`meas_sched stop` before `hrm_start`.** Otherwise `hrm_start` races the measurement
  scheduler and returns `ERR_PERMISSION` on roughly a 120 s coin flip.
- **`CONFIG_LOG` off for BDS runs**, or the warning storm drops BDS data. Note the outpost
  snippet already compiles `CONFIG_LOG` out, so NUS `log …` returns "command not found" —
  that is expected, not a fault.
- **Flash what is already built.** Do not `west build` the client workspace; if no artifact
  exists, leave this `open` and say so.
- **Never flash Nordic RRAM parts with `probe-rs`.** Core picks the board's declared vendor
  runner per chip family; let it.

## What

One study runs end to end against the bench and its result is recorded — and, more
importantly, **the exact sequence that made it work is written down** where the next bench
task can follow it. Today that sequence exists only in the owner's head and in the facts
above; three other `bench` tasks (`ui`, `outpost`, `study-designer`) each need a green study
and would otherwise each rediscover it.

Write the sequence into `embarch-doc/suite/studies-guide.md` (or `embarch-api/spec.md` if
that is the better home — say which and why), with each step's provenance marked per
`../../DOC-CONVENTIONS.md`.

## Why now

The boards are attached and the owner has granted the fleet hardware
(`../../embarch-fleet/protocol.md` §7, 2026-09-06). A plugged-in bench expires; this is the
task that makes the other three cheap.

## Done when

- [ ] Both roles validated live before any step.
- [ ] A study completes, and the step-by-step sequence that got there is recorded, including
      which of the facts above turned out to be load-bearing and which were not needed.
- [ ] Any step that failed is recorded with its actual error, not a paraphrase.
- [ ] If the study could **not** be brought up, that is a complete answer: record exactly
      where it stopped and what the DUT reported, leave the task `open`, and do not guess at
      a cause.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false.

## Progress 2026-09-06 — supervisor, leg 021

**Both roles validated live and matched their enrolled identities exactly**:
`dut` `834f2559f10a6cdf` on probe `000852006107`, `dev-bench` `6fcddc36cb781b71`
on `001057729826`. No mismatch either side, boards attached throughout.

**A study ran end to end and passed**: the two-step `BleAdvertise` self-test,
study `3785bd198cc3a62dccd1780fd552e988`, `reflash` left at its `none` default so
**nothing was built and nothing was flashed**. 2 of 2 steps `Pass`. Provenance
came back `dev_bench_source: ReportedByDevBench`, `dev_bench_version: 49958d34`,
`firmware_source: Declared`, `firmware_version: any`. Written up as
`suite/studies-guide.md` §3a.

**So the bench half of the bring-up sequence is now measured, and it needed none
of the lore above.** No `ble speed fast`, no `meas_sched stop`, no `CONFIG_LOG`
change, no baud setting: **every DUT-side fact in this task is still unexercised,
because no step in that study connects to anything.** Do not read "a study ran
green" as "a study reached the DUT" — the three bench tasks that depend on this
one need the second thing.

**A second study then measured what is on the air.** A `BleConnect` with a
`target_name` no device could have — the documented way to ask (study-designer
decision 43) — failed as intended and returned `no name match; on air:` followed
by **three named advertisers**. That is a real census from this bench, not a
reasoned claim.

**Where it stopped, exactly, and it is not a missing capability.** None of those
three names is attributable to the DUT, and **nothing in EmbArch joins a BLE
advertiser to an enrolled probe** — enrolment knows the board by hardware ID and
probe serial, the census knows it by advertised name, and no code relates them.
Picking one is the operator's call. Decision 43 also records, as a measured
finding, that **the DUT's real advertised name was not its configured one**, so
reading `CONFIG_BT_DEVICE_NAME` out of the firmware would be both inference and
probably wrong.

**So the next step is a bench sitting, not a decision.** Whoever runs it: re-run
the census, connect to each candidate by name in turn, and `GattDiscover` — the
DUT is the one whose table is the DUT's. That is three cheap steps and it needs
the boards attached, which is why this stays `open` rather than `blocked`. The
three tasks behind it (`ui/007`, `outpost/002`, `study-designer/007`) are **not
blocked either**; that was this entry's own earlier error.

**Two defects observed and filed rather than fixed here:** the completed study
reported `current_step: 1` against `total_steps: 2` with both steps passing
(`tasks/core/012`), and the census `fail_reason` hit its 64-byte cap exactly,
ending mid-list on a trailing comma with nothing marking the truncation
(`tasks/dev-bench/007`).

**What this entry got wrong before a reviewer caught it**, recorded because the
error is more instructive than the result: it claimed there is no scan action in
the vocabulary and therefore no way to measure the name — derived from reading
the `Action` enum and stopping there. Decision 43's own final paragraph closes
that gap and `embarch-dev-bench` implements it. **The false sentence was the
untagged one sitting directly under a `[measured …]` tag**, which is exactly
where the provenance discipline has no grip.
