# Let the stale-prefix drop meet a real stale prefix

**State:** open
**Source:** `embarch-ui/open.md` — "**Hardware debt, the owner's own session:** run a study on the bench, open its Trace tab, and check the axis note reports a dropped prefix"
**Scope:** ui
**Hardware:** bench
**Owner:** no

## Roles this needs

`dut` and `dev-bench`. **This needs a study that runs** — see the companion `api` bench task
that brings one up green and records the sequence; do that one first if it has not landed.
Validate both roles before starting; if either is unattached, leave this `open`.

## Bench facts — owner-supplied, do not infer

- **DUT: `nff_dev` rev 6** (AS7058 PPG AFE; rev7 is MAX86178). Owner-stated 2026-09-06.
- **`ble speed fast` over NUS before any BDS step**, or the study dies around step 5 on the
  DUT's own slow connection interval.
- **`meas_sched stop` before `hrm_start`**, or `ERR_PERMISSION` on a ~120 s coin flip.
- **`CONFIG_LOG` off for BDS runs**, or the warning storm drops BDS data.
- Outpost link tops out at **460800 baud** — the bridge refuses above 750000 and the SoC has
  no rate between 460800 and 921600. Keep the DUT's current speed and `EMBARCH_SIGNAL_BAUD`
  in step **by hand**; nothing does it for you.
- **Reading an outpost trace CSV**: drop the stale pre-reset prefix, calibrate the ~1 MHz
  clock against `rx_utc_ms`, and check frame loss before trusting any lane conclusion.
- **Do not reuse rev7 lane identity.** On `nff_dev@7` the PPG AFE is `spim_21` + `gpiote_20`;
  `gpiote_30`/`twim_30` are PMIC + accel + temp and prove nothing about PPG. **This board is
  rev6 and its lane identity is not established** — if a conclusion needs it, say so and stop.
- **Flash what is already built**; do not `west build` the client workspace.

## What

`decision 19`'s stale-prefix drop is exercised against the case it was built for: the ~18
records a real capture opens with, buffered inside the USB-UART bridge past Core's open-time
purge. Run a study, open its Trace tab, and check the axis note reports a dropped prefix
where the capture previously fell back to the millisecond clock.

Then say what the run taught about `STALE_PREFIX_MAX_ROWS = 512`, which `open.md` calls "an
assumption about a bridge FIFO nobody has measured". **A single observation does not make it
measured** — record the prefix length actually seen and update the bullet to what is now
known, not to a conclusion the sample does not support.

## Why now

`open.md` files this explicitly as a hardware debt for the owner's own session, and the fleet
now has the bench (`../../embarch-fleet/protocol.md` §7, 2026-09-06). The four drop conditions
are known sufficient to leave good captures alone but **not known necessary** to catch the
real one — which only a real one can settle.

## Done when

- [ ] A study runs and its trace is opened; whether a stale prefix appeared at all is stated.
- [ ] If one appeared: the axis note reports it, and the observed prefix length is recorded
      with provenance.
- [ ] If none appeared: that is a real result — say so, and do **not** conclude the mechanism
      works from a capture that never exercised it.
- [ ] `open.md`'s `STALE_PREFIX_MAX_ROWS` bullet reflects exactly what one observation
      supports and what it does not.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false.
