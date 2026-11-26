# embarch-core: image readback

**Status:** active, 2026-11-25. Not a route: `readback` in `src/readback.rs` is called by the smoke check (decisions 142, 143, [decisions/image-readback.md](../decisions/image-readback.md)).

`readback(core, board, entry, list) -> ImageStatus`. `core` is `None` when the board has no probe; `entry` is the board's newest `FlashedEntry`; `list` is the released bench firmware. Serialized as `{"status": "<state>", ...}`.

| Board | `status` | Fields | Means |
|---|---|---|---|
| DUT | `holds` | none | every segment read back equals the one flashed |
| DUT | `differs` | `address`, `length` | the first segment whose bytes differ |
| DUT | `claim` | `reason` | refused read (read-out protection), no probe, no entry, or no segments |
| bench | `released` | `app`, `board`, `version` | the read-back identity is in the list |
| bench | `unreleased` | `scope` | not in the list; `scope` flashed it |
| bench | `unknown` | none | no entry, or no segments, for the board |
| bench | `unverified` | `reason` | no probe, refused read, or no list |

**`EMBARCH_BENCH_FIRMWARE_LIST`**: the path of `bench-firmware.json` (`embarch-study-designer` `hil_image::BenchFirmwareList`, `schema` 1). Unset, unreadable or another schema: bench readbacks are `unverified`. The name is the plan's recommendation and the owner may replace it with a key in Core's config file. [assumed]

Chunk size: `live::MAX_WORDS` (256 words, 1 KiB) per halt.
