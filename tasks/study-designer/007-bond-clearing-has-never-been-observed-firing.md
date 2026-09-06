# Observe bond clearing actually firing on real hardware

**State:** open
**Source:** `embarch-study-designer/open.md` — "Bond clearing has never been observed firing on real hardware. Decision 11's clearing step has only been reasoned about; nothing has shown a study starts from a genuinely unbonded link rather than one that happened to be clean."
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
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false.
