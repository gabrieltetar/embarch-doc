# embarch-dev-bench decisions: Addressing and scan-time discovery

**Status:** active, 2026-09-02.

The bench's own BLE address, GATT UUID byte order, and how it finds and reports on the DUT before a connection exists: name filtering and the advertiser census. Pairing and security after connection are a separate mission: [ble.md](ble.md).

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 17 — A static random BLE address, fixed at build/boot time
Reproducibility over privacy realism: the bench is a test fixture, and a stable address makes captures easier to correlate across runs. Plain Zephyr default behaviour, no custom addressing logic.

### 23 — `BleAddress` byte order is stated in the crate that owns the type
The bridge assumes display order and reverses into Zephyr's little-endian address struct — correct, but previously asserted only *here*. Now stated there, so the assumption is backed by the authoritative source instead of standing alone.

**Amended 2026-09-07: this decision claimed the crate-side statement had already landed; it had not.** `src/ids.rs`'s `BleAddress` doc comment stated only the field layout, with no order, until `embarch-study-designer` landed it on 2026-09-06 (`79a4c00`) — **no numbered decision in that crate covers it**, which is part of why this one could claim it prematurely and nothing noticed. What landed: display order, most-significant first, `C4:82:E1:42:B1:26` as `[0xc4, 0x82, 0xe1, 0x42, 0xb1, 0x26]`, same order for both `BleAddressKind`s, derived serde carries `bytes` in index order, nothing in that crate reverses it. That is what closes this decision; it did not touch `embarch-dev-bench`.

### 31 — 16-bit UUIDs were reported two bytes out of place
The expansion wrote a 16-bit value into offsets 0..1, but a 16-bit UUID expands to `0000xxxx-…` — offsets **2 and 3**.

**Not cosmetic, and the failure signature is misleading:** live discovery reported the Device Information Service as `180a0000-…`, while the crate's parser expands `"180a"` correctly — so a `DataExchange` authored against *any* 16-bit UUID could never match a characteristic **plainly visible in its own discovery output**. 128-bit UUIDs take the byte-reversing branch and were never affected, which is why every custom-service study worked.

### 32 — `BleConnect.target_name`, an advertised-name scan filter
The scan callback already received the advertising payload and discarded it; it now parses Local Name elements and connects only to a matching advertiser, ANDed with the pre-existing address filter. Matching is **exact** — a loose match would reintroduce the very failure this exists to remove, just less visibly.

**Names and connectable packets arrive separately.** With active scanning a peripheral's name usually lives in its scan response, which is not itself connectable, so the name and the connectable advertisement are two different callbacks in an order this code does not control. ***Rejected: a single "last address whose name matched" slot, connecting on the next connectable advertisement from it.*** It fails outright — active scanning sets filter-duplicates, so each advertiser is reported at most once per scan and **there is no next advertisement**. Scanning now runs with duplicates unfiltered; the cost is more callbacks per second, bounded by the step's own timeout. Bookkeeping is **keyed by advertiser address**, which removes the ordering dependency entirely — whichever packet completes the pair triggers the connect.

**Reporting what a failed scan saw, at two levels.** The 64-byte `fail_reason` gets a compact name list, and must not spend a third of it echoing the name that was *asked* for. Per-advertiser detail goes through a separate log hook, because a name-only report cannot distinguish **"the DUT is silent"** from **"the DUT is on the air but advertises no name"**, and the second is invisible to a name filter by construction.

`SCAN_SEEN_MAX` is **256** at the repo owner's call: 12 distinct advertisers turned up in three minutes on a real bench, which puts a smaller cap one busy room away from truncating. **A cap that silently truncates defeats the diagnostic entirely** — "not in the list" has to mean "not on the air", not "the list was full". Affordable only because it is a flat table of small entries rather than anything frame-sized.

### 44 — Manufacturer Specific Data joins the census, capped at 4 bytes
`report_scan_seen()` logs `BT_DATA_MANUFACTURER_DATA`'s company ID and payload, parsed in `scan_seen_mfg.c` — no BT host, so a ztest pins it under native_sim, where `ble_bridge_real.c` never builds. Absence differs from a zero-length element; bytes past the cap say so. Costs 2,816 B [measured] SRAM (spec.md).

**Client firmware reads the payload as `s_ficr_id[6..7]`, matching the name suffix — read off source, unconfirmed on air.** `tasks/api/029` tests this first.

### 45 — Two markers for two truncations, and the name list is bounded before it is written
`dev-bench/007`: the 64-byte `fail_reason`'s name list was cut silently by `snprintk`'s own return-length check, which fires *after* `snprintk` has already deposited whatever fit — a partial name, or a bare trailing separator, stayed in the buffer. `scan_seen_names_append()` (`scan_seen_names.c`, no BT host, ztest-pinned under native_sim) formats each entry into scratch first and copies it in only whole, so a rejected entry changes nothing.

Two distinct overflow conditions now get two distinct markers: `(truncated)` means the name list itself hit the 64-byte cap (three or four names, the common case); `(census full)` means `SCAN_SEEN_MAX` (256, decision 32) was exceeded — unrelated, and needs 256 advertisers to ever fire. **Rejected: one combined marker.** It would say something was cut without saying which — a `BUILD_ASSERT` in `ble_bridge_real.c` holds room for whichever applies before the name list is even formatted, so the final `outcome_fail` write never truncates the marker away either.
