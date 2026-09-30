# embarch-smp: open

**Status:** active, 2026-09-30.

Unresolved only. Current truth: [spec.md](spec.md). Why: [decisions.md](decisions.md).

- **Chunk size.** MCUboot serial recovery's receive buffer and maximum line length are Kconfig choices on the DUT. Whether the bootloader reports them or a caller has to declare them is to be read from smpclient's upload path and MCUboot's serial-recovery source before the upload loop is written, not assumed.
- **Header version.** The header carries an SMP version (v1 or v2), and a v2 server can reply with an error shape a v1 server never sends. Which version MCUboot serial recovery answers with, and whether smpclient negotiates down, is to be confirmed from their source the same way.
- **The CBOR crate.** `minicbor` and `ciborium` both fit; the choice is made against the upload request's byte-string field and the fixtures, and recorded as a decision when made.
- **No real bootloader has answered yet.** The first DUT has no MCUboot, so every test is against fixtures and the simulator. A real-hardware run is owed, and its trigger is that DUT's firmware gaining MCUboot.
