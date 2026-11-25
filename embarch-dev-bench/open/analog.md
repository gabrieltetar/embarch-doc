# embarch-dev-bench: open, analog capture

**Status:** active, 2026-11-24.

What is unresolved about the analog source and its USB device, and what would close it. Current truth: [../spec/analog.md](../spec/analog.md). Rationale: [../decisions/analog.md](../decisions/analog.md).

Built and tested host-side only (EMB-470 to EMB-477); [spec/analog.md](../spec/analog.md). Each closes with a bench run on an nRF52840 DK.

- **The block rate and lost blocks at 32 ksps.** Nothing has shown the SAADC's double buffer, the slot queue and the samples port keep up, or how many blocks a 5-minute session loses.
- **CDC ACM throughput**, about 66 kB/s needed; no figure exists anywhere in the suite (the proposal's assumption).
- **The analog noise floor, DC/DC on and off** (EMB-478), and **VDD accuracy**: the header's `vdd_mv` is one reading at start; REGOUT0 at 3.3 V and the 1.8 V reset default (decision 65) are the datasheet's, not measured.
- **Which order the host OS lists the three ports in**, and which interface number it reports for a CDC function: Core finds the samples port as the one after the control port ([core decision 126](../../embarch-core/decisions/analog-capture.md)).
- **What a CDC ACM control port does with the 1 Mbaud setting Core still passes**, and whether an MCUboot image update over SMP works end to end (decisions 62, 63).
- **A rate that is not a divisor of 16 MHz** runs near, not at, the request (decision 66); whether any study needs the exact one is open.

