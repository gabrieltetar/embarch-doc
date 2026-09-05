# embarch-dev-bench decisions: BLE behaviour

**Status:** active, 2026-09-02.

Pairing, addressing, scanning and security — including the header comment that was confidently wrong about all of it.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 11 — Pairing is Just Works, bonds RAM-only, cleared on `Hello` and at study end
Some real DUTs require pairing before certain characteristics are accessible, so v1 needs at least Just Works rather than unencrypted-only. ***Rejected: persisting bonds to flash*** — a study should start from a known, clean pairing state rather than accumulate stale bonds across unrelated studies or reboots. Put up again against a real DUT that requires pairing, where clear-on-every-`Hello` means a full pairing exchange per study, and declined again: a hermetic run from a known state is worth one pairing exchange, and a bench that carries state between studies is the harder thing to debug.

*Amended:* "cleared on `Hello`" is now **also** "cleared at study end" (decision 37), and "nothing clears the bond table mid-study" is no longer unconditionally true, because `Action::BleUnbond` exists precisely so an author can.

### 15 — One DUT connection at a time, enforced in firmware
Testing several DUTs in parallel means several independent Core+bench pairs, not one bench juggling links, and nothing in the type model addresses more than one concurrent DUT anyway. **The enforcement point is firmware** — the connect path refuses a second link while one is live — *not* the controller's link budget, which is a separate board-specific number ([../spec.md](../spec.md)).

### 17 — A static random BLE address, fixed at build/boot time
Reproducibility over privacy realism: the bench is a test fixture, and a stable address makes captures easier to correlate across runs. Plain Zephyr default behaviour, no custom addressing logic.

### 23 — `BleAddress` byte order is stated in the crate that owns the type
The bridge assumes display order and reverses into Zephyr's little-endian address struct — correct, but previously asserted only *here*. Now stated there, so the assumption is backed by the authoritative source instead of standing alone.

### 31 — 16-bit UUIDs were reported two bytes out of place
The expansion wrote a 16-bit value into offsets 0..1, but a 16-bit UUID expands to `0000xxxx-…` — offsets **2 and 3**.

**Not cosmetic, and the failure signature is misleading:** live discovery reported the Device Information Service as `180a0000-…`, while the crate's parser expands `"180a"` correctly — so a `DataExchange` authored against *any* 16-bit UUID could never match a characteristic **plainly visible in its own discovery output**. 128-bit UUIDs take the byte-reversing branch and were never affected, which is why every custom-service study worked.

### 32 — `BleConnect.target_name`, an advertised-name scan filter
The scan callback already received the advertising payload and discarded it; it now parses Local Name elements and connects only to a matching advertiser, ANDed with the pre-existing address filter. Matching is **exact** — a loose match would reintroduce the very failure this exists to remove, just less visibly.

**Names and connectable packets arrive separately.** With active scanning a peripheral's name usually lives in its scan response, which is not itself connectable, so the name and the connectable advertisement are two different callbacks in an order this code does not control. ***Rejected: a single "last address whose name matched" slot, connecting on the next connectable advertisement from it.*** It fails outright — active scanning sets filter-duplicates, so each advertiser is reported at most once per scan and **there is no next advertisement**. Scanning now runs with duplicates unfiltered; the cost is more callbacks per second, bounded by the step's own timeout. Bookkeeping is **keyed by advertiser address**, which removes the ordering dependency entirely — whichever packet completes the pair triggers the connect.

**Reporting what a failed scan saw, at two levels.** The 64-byte `fail_reason` gets a compact name list, and must not spend a third of it echoing the name that was *asked* for. Per-advertiser detail goes through a separate log hook, because a name-only report cannot distinguish **"the DUT is silent"** from **"the DUT is on the air but advertises no name"**, and the second is invisible to a name filter by construction.

`SCAN_SEEN_MAX` is **256** at the repo owner's call: 12 distinct advertisers turned up in three minutes on a real bench, which puts a smaller cap one busy room away from truncating. **A cap that silently truncates defeats the diagnostic entirely** — "not in the list" has to mean "not on the air", not "the list was full". Affordable only because it is a flat table of small entries rather than anything frame-sized.

### 33 — `Hello`'s hard reset now waits for its own disconnect
The reset called disconnect and returned. That only *requests* it: the connection stays populated until the callback runs on Zephyr's BT RX thread. So the next study's connect could execute while the previous connection was still tearing down and fail with **"already connected to a different peer" despite a `Hello` having just been processed**, whose whole documented contract is that it *is* a hard reset.

**The failure signature is an asymmetry, and it is why this hid:** the first of two back-to-back studies against different addresses failed, the byte-identical retry passed. This bench already had a known re-run-and-it-works flake, which is exactly the cover a bug like this hides under. Now waits on a semaphore with a fixed bound, fixed rather than caller-supplied because a reset has no timeout budget to draw from, and timing out anyway leaves the behaviour it replaces.

### 34, 37 — Pairing callbacks and `BleSecurity` dispatch; "Just Works needs no auth callbacks" was wrong
The bridge's own header comment stated the opposite as settled design: that elevating a link is not handled here because Zephyr's ATT layer re-runs a request at higher security on an authentication error, and Just Works needs no callbacks. **Both halves fail against a DUT that requires an authenticated link**, and **the comment was deleted rather than amended** — it is the load-bearing kind of wrong, and it is what a reader would otherwise trust.

**The mechanism, and it is a fact about our own code plus Zephyr rather than an inference about any DUT.** With no auth callbacks registered, Zephyr's capability lookup returns no-input-no-output, and the reachability check then refuses L4 outright — so **L4 is unreachable from this bench regardless of what any study asks for**, and no amount of ATT-error-driven retry gets there, because "higher" is still bounded by what the pairing can achieve. The second half fails differently: this DUT does not wait to be asked. It requests L4 itself, 200 ms after connect, so elevation happens before any ATT request has been made to fail.

**Failure signature: connect `Pass`, then "disconnected during service discovery", deterministically** — while the same discovery walked several unrelated devices without trouble. **A failed elevation is invisible to a bench that has no concept of elevation**, so it reads as a discovery bug. The fix registers the callback pair that makes the capability lookup return display-yes-no, and dispatches `BleSecurity`, waiting on the security-changed callback within the step's own timeout and reporting the **achieved** level. A link already at or above the requested level is a `Pass`, since the DUT's own self-elevation regularly wins that race.

**Read out of this workspace's own Zephyr rather than recalled, which mattered:** the display-yes-no row requires *both* function pointers non-NULL, so registering only the confirm half yields no-input-no-output and the method silently resolves to Just Works, capping the link at L3. The entry callback is left NULL for the mirror-image reason: it would select Passkey Entry against a display-only peer, needing six digits only the *peer* displays.

**Auto-confirm is right here and would be wrong almost anywhere else, so it is stated rather than implied.** A bench has no human at it; unattended runs are the entire point. What that buys is protection against a passive eavesdropper on the pairing exchange and **not** against an active man-in-the-middle — nobody compares the digits, so "L4" here names the key strength and the pairing method, not a verified peer. Anyone reading a result that says `L4` should read it that way. The method that actually ran is **logged rather than deduced from the callback set**, which is the only thing that would say so had it landed on Just Works instead.

Three things running it against the DUT changed:

- **`-EBUSY` is not a failure, and this is the one that mattered.** Zephyr returns it when a procedure is already in flight — exactly what decision 34 predicted the DUT would do. It anticipated the *race* and said an already-elevated link is a `Pass`; it did not anticipate arriving in the *middle*, and failing there reports "could not establish security" about a link one second from being secured — worse than useless, because it points at the wrong side. So `-EBUSY` now means *wait for the procedure already running and judge what it reaches*, and only if that settles below what the study asked for, request again. Two attempts, not a retry loop, because the call resets the required level on error so the in-flight procedure targets whatever the peer asked for. **Invisible from any single-peer test where dev-bench asks first.**
- **`BleUnbond` drops the link, and waits for it.** Zephyr's unpair disconnects a peer whose keys it clears, and returning while the connection is still populated is precisely the race decision 33 already had to fix once. Every bond is cleared rather than only the connected peer's: decision 15 holds one connection at a time, so the two are the same set.
- **A study is a bond's lifetime, said in the firmware rather than inferred from the protocol.** Bonds were already effectively per-study *by coincidence* — Core sends a `Hello` before every study. Now cleared explicitly at study end, which removes the failure where a second run of the same study behaves differently from the first. Placed *before* the transcript drain rather than after, because the clear disconnects the peer and that disconnect deserves to reach Core with everything else.

**Auth callbacks are registered before `bt_enable`:** Zephyr latches them the first time it needs a capability, so a peer that paired before registration ran would latch NULL — unauthenticated, with nothing in the failure pointing at registration order. The same class of failure as decision 34's own.

**What is still not claimed:** validation against a DUT that presents no I/O capability at all — [../open.md](../open.md) carries what that would look like.
