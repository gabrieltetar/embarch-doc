# embarch-topology decisions: A DUT's bootload ports

**Status:** active, 2026-10-26.

Split verbatim from [link-declares.md](link-declares.md), 2026-10-26, once decision 42 pushed that
file into reserve. Decision 36 is a DUT's two declared bootload USB identities, its own table, a
different mission from a role's link facts; the sub-project's `src/` and
[embarch-core decision](../../embarch-core/decisions/bootload.md) cite it by number.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 36 — A DUT's bootload ports: two declared USB identities, in their own table
Bootloading ([bootload-proposal.md](../../bootload-proposal.md)) needs two ports found by identity: the application's, where an engineer-declared entry command goes, and the bootloader's, where SMP goes. On Windows a device that re-enumerates under a different PID gets a different COM number, so a COM name is not an identity. **Both are declared** as VID:PID plus optional USB serial and interface, the same posture as decision 20, because a DUT built from Zephyr's defaults enumerates as a VID:PID thousands of unrelated boards share.

**A pair that one port could match both of is refused at declaration** — equal VID:PID with no serial or interface to tell them apart. Telling the two apart by disappear-and-reappear timing would be an inference about the DUT; the fix, a distinct bootloader PID, is the firmware's, and saying so at declaration puts it in front of the person who can make it. **A live identity that matches more than one port is an error naming them**, not a pick.

**Its own `bootload_ports` table in `enrollment.toml`, not two more `EnrolledBoard` fields.** A bootloadable DUT may have no probe and no enrolled row, and an `EnrolledBoard` field would have changed struct literals in Core, the UI and the API client for a fact none of them read. The table is skipped when empty, so a store that never declared one is rewritten unchanged. Only the `dut` role takes one.

