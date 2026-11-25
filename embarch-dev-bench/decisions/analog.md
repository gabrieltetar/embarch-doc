# embarch-dev-bench decisions: The analog source and its USB link

**Status:** active, 2026-11-24.

Sampling one analog input on a dev kit and sending it over a USB device of the bench's own. Decided by the bench owner, 2026-11-24, as route 1 of the [analog-capture proposal](../../embarch-analog-capture-proposal.md); built by EMB-470 to EMB-479, so [the spec](../spec.md) does not describe it until EMB-479 lands. The bench stays generic firmware for any dev kit, one full image per board: this adds a capability, not a project image.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 60 — The analog source is a SoC-neutral interface with one nrfx backend, an exception to portable-APIs-only
The interface takes a channel count (one in v1, and in the block format), a rate and start and stop from the study, and a devicetree input with a label such as "A0". **The only backend is nRF52's: nrfx SAADC in advanced mode on its internal timer** (CC = 16 MHz / rate, 500 for 32 ksps), double-buffered, 12-bit, gain 1/4 against a VDD/4 reference so full scale is VDD, offset calibration at each session start. **The Zephyr ADC driver must not also claim the SAADC.**

**It breaks the invariant that application code calls only portable APIs** (spec §3), and only here: the portable ADC API at 32 ksps was never verified, and a timer-driven double-buffered capture with no gap is what the SAADC's own mode gives. The exception is this backend, no wider. *Rejected:* `adc_*` through Zephyr's driver, unverified at the rate and unable to place a gap. *Later:* nRF54L15 and STM32 backends behind the same interface, and a multi-channel nRF52 one on TIMER and PPI.

### 61 — One USB composite device with three CDC ACM ports and an identity that says what it is
Zephyr 4.5's USB device stack, three CDC ACM ports, each with an interface string naming it: control, samples, SMP. **VID 0xEBAC (local use, not a reserved vendor ID); PID high byte is the EmbArch device type, from a small table (dev bench first), low byte from the board's serial; product "EmbArch dev bench"; serial the chip's unique ID.** So Core and a person tell the bench's ports apart without the SEGGER VID decision 12 matched.

*Rejected:* a sample stream on the control port, which shares 1 Mbaud with logs and transcript (65 to 77 % of it, the proposal's measure); a second USB device per function, which enumerates twice for one board; a PID from a fixed number, which cannot tell two boards apart.

### 62 — The control link is chosen per board, and enrollment records the port's USB identity
A devicetree `chosen` entry names the control link: the J-Link UART or a CDC ACM port. **Core's enrollment records that port's VID:PID:SERIAL plus interface** instead of assuming the SEGGER VID, which amends decision 12 for a CDC control link. **Boards already in use keep the J-Link UART**, so nothing enrolled changes. *Rejected:* CDC for every board, which breaks the nRF54L15 DK, whose SoC has no USB device (decision 6).

### 63 — Image updates over SMP on the third port, through the bootload tool
MCUboot and SMP on the third CDC port, updated by EmbArch's bootload tool; **the J-Link is for the first flash only**. *Rejected:* flashing through the J-Link every time, which needs a probe on a bench that already has USB.

### 64 — The sample block and the start header
**Block, 8 ms at 32 ksps, about 64 kB/s:** 4 B magic, 4 B index of the block's first sample, 4 B event word (marker edges and their sample offset in the block), 256 `int16` per channel, CRC-32/ISO-HDLC over the preceding bytes. **Header, once per session:** rate, resolution, gain, reference, channel count, input name, measured VDD (read once at start), board and image version. **Samples go as raw ADC codes; volts derive from the header**, so the bench never manufactures a claim. A gap is placed by the index, never from arrival times, and each block verifies by its magic and CRC. *Rejected:* volts or scaled samples on the wire, which freeze a calibration into every recording.

### 65 — REGOUT0 is set to 3.3 V once at boot when unset
An nRF52840 DK powered only from its native USB leaves VDD at the regulator's reset default, 1.8 V by the datasheet (not measured on the DK), so an external analog front end would run starved. The image writes UICR REGOUT0 = 3.3 V once at boot **when it is unset**, never on every boot, so the flash write is not repeated. *Rejected:* a board-level jumper or a separate setup flash, either of which a person forgets.
