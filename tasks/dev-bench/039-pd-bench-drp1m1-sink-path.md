# 039 — The X-NUCLEO-DRP1M1 gives no VBUS on CN2 while it sinks

**State:** open
**Source:** field use on a USB PD charger board, 2026-09-09 to 2026-10-20 — on 2026-10-14 an electronic load on the DRP1M1's CN2 read about 2.3 V while pd-bench held a 9 V contract as sink, the same for every TCPP03 control value tried, and with the firmware's consumer-path bit matching ST's `tcpp0203.h` (0 = closed); e-load work moved back to the SNK1M1
**Scope:** dev-bench
**Hardware:** required
**Owner:** no

## What

On the DRP1M1, pd-bench sinks through the TCPP03's consumer path: back-to-back N-MOSFETs from VBUS to CN2, gate-driven by the TCPP03. Register 0's GDC bit (bit 3) is 0 for closed. Idle is `0x10`, which keeps the consumer path closed so that the port can sink. The README tells you to put the electronic load on CN2 for the sink role, "as on the SNK1M1 output". On the bench that is false. With a 9 V contract in force as sink, CN2 sits near 2.3 V, whatever control word the firmware writes. The firmware's bits match ST's driver, so the cause is most likely a board setting or a gate-drive condition that UM2891 describes and the bench setup misses.

Find the cause, fix it (in firmware, the jumpers or the solder bridges), and make the README true. If the board cannot do it, say so in the README and in `open.md`.

## Why now

It is the one documented DRP1M1 function that does not work. Until it does, the DRP1M1 cannot be the scriptable PD sink with a load, and a DUT's sink-to-source power role swap under load cannot be tested with one board. The README tells the next user to wire the load to CN2.

## Done when

- [ ] The README's DRP1M1 section stops presenting CN2 as working. Until the cause is fixed it says: "CN2 gives no VBUS while sinking (open.md); use the SNK1M1 for a load".
- [ ] The cause is found and cited against UM2891 Rev 3 with section and figure: the consumer-path parts, any solder bridge or jumper on that path, and what the TCPP03 needs to drive GDC (see the provider and consumer paths section, 1.8 and Fig. 9).
- [ ] Measured at a 9 V contract, with and without a 1 A load: the GDC gate voltage relative to VBUS, VBUS at the connector, and CN2. The numbers go in the decision.
- [ ] Fixed in firmware, in the README's jumper and solder-bridge list, or both. With the fix, CN2 is within 5 % of the connector's VBUS at 5 V and at 9 V, at no load and at 1 A. Or, if the board cannot do it, the README and decision 49 say so and why.
- [ ] A Hard Reset and a PR_Swap from sink to source still open the consumer path before the provider path closes. The TCPP03 refuses both closed, so this guards against a fix that breaks the swap.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped.
