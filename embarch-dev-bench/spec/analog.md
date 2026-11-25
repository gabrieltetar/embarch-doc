# embarch-dev-bench: the analog source and the USB device

**Status:** active, 2026-11-24. What is built for audio-rate analog capture. Why: [decisions/analog.md](../decisions/analog.md), decisions 60 to 66. The walkthrough for an engineer: [studies guide](../../suite/studies-guide.md) §5.

**One backend, one board.** The interface is SoC-neutral and N-channel-ready (`analog_source.h`); **the only backend is nRF52's, so the nRF52840 DK is the only board that samples** (decision 60). Any other build links a backend whose prepare returns `-ENOTSUP`. It calls nrfx SAADC directly (advanced mode, internal timer, double-buffered, 12-bit, gain 1/4 on a VDD/4 reference, offset calibration per session): **the one exception to "portable Zephyr APIs only"** ([spec §3](../spec.md)), and the board's `&adc` node is disabled so Zephyr's driver never claims the SAADC.

**Pins, in devicetree.** The input is `chosen embarch,analog-input`, labelled "A0": the Arduino-header pin P0.03 (AIN1), range 0 to VDD, one channel (a request for another is refused). The marker is `chosen embarch,marker-input`, BUTTON2 (P0.12), active low; BUTTON1 stays the MCUboot recovery button. A board with no marker node captures without marker edges.

**Rate.** The timer compare is `round(16 MHz / rate)`, the start header carries `16 MHz / CC`, the rate the hardware really runs (so 44100 Hz asked is 44077 Hz run), and a rate outside CC 80 to 2047 (about 7.8 to 200 kHz) is refused (decision 66). The study starts and stops the source; there is no other control command.

**What goes out.** Once per session a 75-byte start header (rate, resolution, gain, reference, channels, measured VDD, input name, board, image version), then 528-byte blocks of 256 raw `int16` codes (8 ms at 32 ksps, about 66 kB/s), each with a magic, the index of its first sample, an event word (marker edges, level 1 = asserted) and a CRC-32. Volts are never sent; they derive from the header (decision 64). Byte layout: [study-designer analog.md](../../embarch-study-designer/interfaces/analog.md). Per the source, nothing blocks: with no free slot or a sink that refuses, a block is counted lost and the index skips it, which is how a reader finds the gap. How often that happens on a real link is unmeasured.

**VDD.** An nRF52840 DK on native USB only has VDD at the regulator default; the image writes UICR REGOUT0 = 3.3 V once at boot when unset (decision 65, `CONFIG_EMBARCH_DEV_BENCH_REGOUT0_3V3`).

**The USB device (nRF52840 DK).** One composite device, three CDC ACM ports in this order, each named by its interface string: **EmbArch control**, **EmbArch samples** (transmit only; bytes from the host are discarded), **EmbArch SMP** (decision 61). **VID 0xEBAC** (local use, not a reserved ID); **PID = device type in the high byte (0x01 dev bench) and the last byte of the chip's unique ID in the low byte**; manufacturer "EmbArch", product "EmbArch dev bench", serial the unique ID in hex (`usb_ids.h`).

**The control link is chosen per board** by `chosen embarch,control-link` (decision 62): the nRF52840 DK names its control CDC port; the nRF54L15 DK has no USB device and keeps the J-Link UART. Core records a CDC control port's VID:PID:serial and interface at enrollment ([core decision 124](../../embarch-core/decisions/probes.md)) and finds the samples port as the next one after it ([core decision 126](../../embarch-core/decisions/analog-capture.md)). The link protocol on the control port is unchanged.

**Updates.** MCUmgr SMP on the third port (image and OS groups) with MCUboot, through EmbArch's bootload tool; the J-Link is for the first flash only (decision 63).

**Measured, 2026-11-24: nothing on hardware.** Host-side tests only. What no board has yet shown is in [open/analog.md](../open/analog.md).
