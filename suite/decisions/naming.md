# embarch suite decisions: naming and field semantics

**Status:** active, 2026-09-12.

What a field name across two sub-projects is allowed to promise.

Index: [../decisions.md](../decisions.md). Suite overview: [../../embarch.md](../../embarch.md).

## 3 — `rx_utc_ms` keeps its name in both homes, and every home says which clock it is

*Decided 2026-09-12 by `tasks/suite/027`, announced under [ops](../../../embarch-fleet/ops.md) §4 (`ts 1789190763.632399`), window closed with no objection. Suite-scope because the collision is between two sub-projects' files and belongs to neither.*

**One field name carries two different clocks, and both stay.** In an **outpost trace** (`<tap>.arrival.csv`, `<tap>.trace.csv`) `rx_utc_ms` is Core's real epoch clock, stamped per frame by [`embarch-core` decision 30](../../embarch-core/decisions.md). In a **study** CSV, GATT transcript or `Sample`, `rx_utc_ms` is **dev-bench uptime** — milliseconds since that board booted, no epoch, no offset applied ([`embarch-study-designer` decision 72](../../embarch-study-designer/decisions/versioning.md)). Every other `*_utc_ms` field in the suite — `core_rx_utc_ms`, `host_utc_ms`, `started_utc_ms`, `ended_utc_ms`, `confirmed_at_utc_ms` — means real UTC, so the suffix reads as a promise everywhere but the study-side column.

**What this decision buys is disclosure, not a rename.** `suite/016` established what the field carries and said so where a study reader looks; this closes the other half — [`embarch-outpost` decision 17](../../embarch-outpost/decisions/clocks.md), its [spec §5](../../embarch-outpost/spec.md) and its [column listing](../../embarch-outpost/interfaces/integration.md) now each say which clock they mean and name the other one. Decision 17 in particular asserted that a trace's stamp is *"the same wall clock every other stream in a study carries"*, which was false in the direction that invites the join this decision refuses.

**Why not rename the study-side column**, which `tasks/suite/027` names as the obvious move and which this decision does **not** take. The name reaches `embarch-dev-bench`'s wire struct, `embarch-study-designer`'s `Sample` and `GattTranscriptEntry`, Core's `src/stream_store.rs` header and `src/study.rs`'s assertion of it, and `embarch-ui` — a coordinated change across four repos whose firmware half cannot be built anywhere in this fleet — **plus every capture file already on disk, which no code change reaches.** A rename that no already-written file follows replaces one ambiguity with two. It is a real option and it is the owner's, with the board in front of him.

**Reversal condition: the moment dev-bench applies the offset it already receives in `Hello.host_utc_ms`** — one subtraction at the stamp site in `ble_bridge_real.c` — **the collision disappears without a rename**, both columns mean UTC, and the three disclosures added here shrink to nothing. That is the firmware arm `suite/027` and `suite/016` both declined to take unattended, because it makes captures taken before and after it incomparable with no marker in the file saying which side they are on. **If instead the rename is chosen, this decision is superseded rather than amended** — the two are alternatives, not steps.
