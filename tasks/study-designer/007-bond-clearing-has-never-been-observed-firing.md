# Observe bond clearing actually firing on real hardware

**State:** blocked — parked by the owner 2026-09-07: he is taking every bench and
DUT-facing question himself once the fleet has run a while. **Unparked by him saying so**,
and by nothing else — do not dispatch it, and do not read the queue's silence here as a
reason to try the bench again.
**On the substance, so the next reader is not misled**: the owner judged the unbond's
chance of failing low and stood the attempt down. That is a risk accepted, **not an observation** —
leg 039 stopped at step 1 and never connected, so nothing about bond clearing was measured. The
`Done when` list below is unchanged and still unmet.
**Source:** `embarch-dev-bench/open.md` — "Bond clearing has never been observed firing on real hardware. Decision 11's clearing step has only been reasoned about; nothing has shown a study starts from a genuinely unbonded link rather than one that happened to be clean. Attempted 2026-09-07 (leg 039) and stopped at step 1, never connected — the owner then judged the failure risk low and parked the bench work, so this is an accepted risk and still not an observation."
**Scope:** study-designer
**Hardware:** bench
**Owner:** no

## Roles this needs

`dut` and `dev-bench`. Validate both first; if either is unattached, leave this `open`.

## Bench facts — owner-supplied, do not infer

- **DUT: `nff_dev` rev 6** (AS7058 PPG AFE). Owner-stated 2026-09-06.
- Dev bench: **nRF54L15DK**, link **COM17 / VCOM1, interface 2** — the higher interface.
- **`ble speed fast` over NUS before any BDS step**, or the link dies around step 5.
- **`CONFIG_LOG` off** for BDS runs, or the warning storm drops data.
- **The dev-bench console *is* the protocol UART.** Core used to swallow unframed bytes, so a
  reset banner can hide in the deframer — **when a link goes quiet, look in the buffer** before
  concluding the link is dead.
- **Flash what is already built**; do not `west build` the client workspace.

## What

Decision 11's clearing step is shown to *fire*, and to leave the link genuinely unbonded —
not merely to run against a link that happened to already be clean, which is the distinction
`open.md` draws and the reason this has stayed open.

That means establishing a bond first, confirming it exists, then running the clearing step
and confirming the bond is gone — an observation the "happened to be clean" case cannot
produce. If the bench cannot be put into a genuinely bonded state, **say so and stop**: a run
that cannot distinguish the two outcomes does not close this question, and recording it as
though it did is the failure mode here.

## Why now

The bench is attached and the fleet may use it (`../../embarch-fleet/protocol.md` §7,
2026-09-06). Every study the fleet now runs depends on this step behaving as decision 11
assumes.

## Done when

- [ ] A bond is established and confirmed present before the clearing step runs.
- [ ] The clearing step is observed firing, and the link confirmed unbonded afterwards.
- [ ] If the bonded precondition could not be established, that is recorded as the result and
      the question stays open — no inference from a clean-link run.
- [ ] `open.md`'s bullet says what is now observed and what is not.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).

## Bench attempt, leg 039, 2026-09-07 — what was measured, and the one fact that stopped it

**Both roles validated live before anything ran** (`POST /validate`, not the buffer): `dev-bench`
`6fcddc36cb781b71` on probe `001057729826`, `dut` `834f2559f10a6cdf` on probe `000852006107`, both
`ok: true`.

A five-step study was authored and submitted — connect, `BleSecurity{l2}`, `BleUnbond{}`, connect
again, `BleSecurity{l2}`, at `dev_bench_log_level: Info` so the Zephyr BT host's own account of
pairing would reach Core. It ran (study `ee0bb4b6d6d4596c316937613742a6f8`) and **stopped at step 1**:

> `dev-bench stopped the study early: step 'connect first' failed (no name match; on air:
> 'pod-36e017c', 'GABRIEL', 'ECHOMAP UHD 63cv', 'pod-5678212')`

**The scan census, from Core's own log — this is the measurement, and it refutes something:**
dev-bench saw **11 advertisers**, of which exactly **4 advertise a name** (`pod-36e017c`
`70:B6:51:83:81:82` public, `GABRIEL` `5E:AC:EF:23:12:C4` random, `ECHOMAP UHD 63cv`
`C0:8C:56:F6:49:A0` random, `pod-5678212` `70:B6:51:83:49:2A` public) and **7 advertise none**, of
which 4 are connectable random addresses. **Neither BLE name candidate that
`scripts/fleet-hardware.py` prints for this DUT — both marked `[UNCONFIRMED]`, both of the form
`<vendor> <product> <last four hex of the hardware ID>` — was on air at 23:14 UTC.** Those candidates are derived from the
enrolled hardware ID, and this run is the first thing to test them: as *advertised names*, at this
moment, they are wrong. That does not say what the DUT does advertise; it says the derivation does
not produce it.

**What this task needs before it can run, and it is one sentence from someone who knows the
board:** how to reach the DUT over the air — the name it actually advertises, or its address, or
the console command that makes it advertise — and whether the DUT's firmware advertises at all
without being told to. **This was not inferred and must not be**: connecting to whichever nameless
connectable random address happens to answer would produce a bond with an unidentified device and a
result that looks exactly like a passing run. The buffer's `[UNCONFIRMED]` marker is doing its job
here; the fix is a measurement or an owner statement, not a guess.

**One more thing the next taker should know: the owner appears to be working this same question by
hand.** Core's log carries study `5453b390f831119fb3004a5774a2f9c0` at 22:44:41 UTC, ~30 minutes
before this attempt, whose failing step is named `elevate to L2 (pairs, bonds)` — nobody in the
fleet authored that study. It failed differently (`no connection to secure; connect first`, preceded
by `bt_conn: conn ... failed to establish. RF noise?`), which is the same wall from one step further
along. **Check with him before spending another bench sitting on this**: two actors bonding and
unbonding the same DUT would produce results neither can attribute.
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false.
