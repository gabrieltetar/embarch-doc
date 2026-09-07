# Bring a study up green end to end, and record the sequence it actually took

**State:** open — **the bench half is done and the remaining step is the owner's, not an
agent's.** See `## Progress 2026-09-06 — leg 025` at the bottom: the attribution this task has
been waiting on cannot be made by anything in the fleet, and leg 025 established *why* rather
than failing at it again. Read that section before running this.
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

## Progress 2026-09-06 — supervisor, leg 025

**Both roles validated live and matched exactly** before anything ran: `dut` `834f2559f10a6cdf`
on probe `000852006107`, `dev-bench` `6fcddc36cb781b71` on `001057729826`. Nothing was flashed
and nothing was built; every study below ran at `reflash`'s `none` default.

**The census leg 021 asked for was re-run, twice, and it does not say what leg 021 read it as
saying.** Studies `458c7df0dd599bce574d1d4264bee485` and `6d15c4896b733f7480ea579b64e7210d`, five
minutes apart, both 20 s: **10 advertisers on the air, 2 of them named.** The `fail_reason` was
`no name match; on air: 'GABRIEL', 'pod-36e017c'` — **47 of its 64 bytes**, so this time nothing
was truncated, and eight advertisers were absent from it anyway, four of them connectable.
`scan_seen_names_summary()` in `ble_bridge_real.c` `continue`s past every entry with an empty
name. **So "not one of them attributable to the DUT" was drawn from a list that structurally
cannot contain a nameless DUT**, and `target_name` cannot reach one either. Filed as
`tasks/dev-bench/008`; `suite/studies-guide.md` §3a is corrected.

**Connect-by-address works and reaches exactly what the census cannot.** `C4:82:E1:42:B1:26`
(public, connectable, **no name advertised**) connected and its `GattDiscover` returned three
services and eight characteristics — study `bd39085d9aa34162a1a555494642ae43`, both steps `Pass`,
written up as `studies-guide.md` §3b along with the byte order, which is a stated contract on both
sides rather than something to re-derive.

**Why this still stops short of the attribution, and it is not a missing measurement.** Two
routes could join an advertiser to the enrolled `dut`, and neither exists:

- **By name** — ruled out above.
- **By making the DUT change state and watching which advertiser changes with it.** `reset` (and
  `run_study --reflash dut`) are aimed at a **project build target** and require
  `board`/`variant`/`revision`/`app`. The enrolled `dut` role knows the board by probe serial and
  hardware ID. **Nothing takes a role and resets it.** This task supplies `nff_dev` rev 6 and not
  an app directory, so aiming that call would mean inferring a DUT fact — refused, per this task's
  own rule and `protocol.md` §7.

**That is the same missing join as the BLE one, in a second place.** But **do not read it as "only
the owner can unblock this"** — a reviewer corrected me on exactly that framing. **`validate` *is*
role-keyed and *does* reach the DUT**: `POST /validate` → `embarch_topology::hardware::validate_role`
opens the enrolled probe, attaches the chip and reads FICR over SWD, under the same `hw_lock` as
flash and reset. It neither halts nor resets, so it cannot make the DUT change BLE state and route
two above stays closed — but it establishes that **a role-keyed probe-side read of the DUT already
exists and is already wired to the enrolled `dut`.**

**So the join may be a readback nobody has built rather than a capability EmbArch lacks.** Whether a
BLE address can be read off this DUT that way is a *DUT fact this task does not carry* — do not
assume it, and do not derive it from firmware source. **What is worth doing next is establishing
that fact, not guessing it**: ask the owner whether his DUT's advertised address is derivable from
a register the existing probe path can already read. If it is, the attribution becomes a feature an
agent can build; if it is not, it stays a sentence only he can supply.

**Two defects found and filed rather than fixed here**, both from this sitting:

- `tasks/core/016` — a step that **times out** and stops a study is reported as
  `"the StepResult saying which step failed did not arrive"`. It arrived: Core's own
  `events.json.partial` for study `dd340b2a36a39aeba94f4f15b4da61f0` holds
  `{"step_name":"connect","outcome":"TimedOut", …}`. `last_failed_step` records only
  `Outcome::Fail`, so `TimedOut` takes the lost-frame arm. **A confident wrong diagnosis pointing
  at the transport**, which is a shape this suite has already paid for.
- `tasks/dev-bench/008` — the census blind spot above.

**One incidental measurement worth keeping, and I got its rule wrong before a reviewer fixed it.**
Across the two censuses all four **public** addresses were identical, and **four of the six random
ones were too.** I wrote that a random address rotates and that `target_address` is therefore
durable only when public. **False, and harmfully so**: the top two bits of a random address's
leftmost byte say which sub-type it is, and `11` is *static random* — the address a Zephyr
peripheral with privacy off advertises, which is `embarch-dev-bench` decision 17's own choice. The
three `11` addresses here survived; the two that vanished were `74:92:…` (`01`, resolvable private
— what my stale-address connect timed out on) and `34:BA:…` (`00`, non-resolvable), and I had
counted only one of those two departures. The correct rule is decision 43's and no broader: a
*rotating private* address cannot be authored ahead of time; a random address in general can be.
`studies-guide.md` §3b now says that.

## What is left — restated 2026-09-07, and it is no longer one sentence

**The DUT is not advertising connectably, so there is nothing on the air to
name.** That is a different blocker from the one this section carried, and it was
measured rather than reasoned — four studies against a validated bench, written
up in full in the `dev-bench` census drop filed the same day. Briefly:

- Nothing matching the DUT's expected name prefix was on the air. The census returned
  `'pod-36e017c'` and `'pod-5678212'`, both public `70:B6:51:83:xx:xx`, neither
  suffix a commit in the client firmware repo.
- The only two static-random connectable candidates, `EC:FA:99:A8:6A:2E` and
  `D9:61:3E:92:C5:36`, both timed out on connect at 15 s.
- `C4:82:E1:42:B1:26`, which leg 025 reached, is definitively **not** the DUT:
  its three services are `0x1800`, `0x1801` and `0x1910`, and study-designer's
  decision 43 already records a `0x1910` table as one of the wrong devices the
  name filter exists to exclude.

**So the owner's step is a board, not a sentence:** get the client
application running and advertising on the DUT — power it out of whatever state
it is in, or flash a known-good build onto probe `000852006107` — and say which
build it is. Both roles validate over the debug probe right now
(`834f2559f10a6cdf` / `6fcddc36cb781b71`), so this is not an enrolment problem.

**And the name will then be derivable rather than asked for.** The firmware
advertises its configured device name followed by `%02X%02X` of
`hwinfo_get_device_id()` bytes 6 and 7, and puts those same two bytes in a manufacturer-data element of the primary
advert. For the enrolled hardware ID `834f2559f10a6cdf` that predicts
the suffix **`6CDF`**, or **`2559`** if Core's byte order is the
32-bit-word-swapped one dev-bench's self-report shows. `fleet-hardware.py` now
carries both candidates, marked UNCONFIRMED. **They are read off client source,
so they are predictions until a connect confirms one** — which is exactly the
rule this task states at the top, applied to itself.
