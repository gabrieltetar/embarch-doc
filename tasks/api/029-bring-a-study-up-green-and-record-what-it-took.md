# Bring a study up green end to end, and record the sequence it actually took

**State:** claimed by the supervisor (bench, no branch), 2026-09-06 16:10
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
