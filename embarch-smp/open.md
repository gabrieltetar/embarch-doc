# embarch-smp: open

**Status:** active, 2026-09-30.

Unresolved only. Current truth: [spec.md](spec.md). Why: [decisions.md](decisions.md).

- **No real bootloader has answered yet.** The first DUT has no MCUboot, so every test is against fixtures and the simulator. A real-hardware run is owed, and its trigger is that DUT's firmware gaining MCUboot. It is also what measures the one number the simulator cannot: wall-clock time per request on a real CDC ACM link, which decides whether a 1,423-request default upload is tolerable or the buffer size has to be declared.
- **The simulator is modelled on `boot_serial.c` as read, not as run.** Where the two disagree, the simulator is wrong; the first hardware run is also its check.
