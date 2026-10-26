# 096 — Make `flash` with `erase: true` skip the alias and option-byte NVM regions, so it works on an STM32G0

**State:** open
**Source:** field use on an STM32G0B1VE board, 2026-10-21 — a flash with `erase: true` answered `500` and wrote nothing, and was the only suite path to clear a stale NVS partition that stopped every image from booting
**Scope:** core
**Hardware:** verify-only
**Owner:** no

## What

`hardware::flash` with `erase` set (`embarch-core/src/hardware.rs:212-256` at `40a58cc`) sector-erases every `MemoryRegion::Nvm` in the target's memory map before downloading. For `STM32G0B1VE`, probe-rs 0.31 also declares an option-byte region, `NvmRegion { name: "synthesized for stm32g0x1_sb_opt", range: 0x1fff7800..0x1fff7820, is_alias: true, access: Some(MemoryAccess { read: false, write: false, execute: false, boot: false }) }`, and `flashing::erase` on it fails with "found more than one suitable flash algorithms but none marked as default". The flash answers `500 erasing 0x1fff7800..0x1fff7820 on 'STM32G0B1VE' failed` and the image is never written. Erasing option bytes is never what `erase` means, and on an STM32 it is the region where a wrong write can lock the part.

When done, `erase` only touches NVM regions that are not aliases and that the image could be written to (`access` absent or `write: true`): on the STM32G0B1VE that is main flash `0x08000000..0x08080000`, and never the option bytes. All ranges are filtered and checked against the target's flash algorithms before the first erase, so a region Core cannot erase fails with nothing erased, instead of after earlier regions may already be blank and before any image is written. The response names the ranges it erased. With no region left after filtering, Core refuses as it does today; it never falls back to a chip erase.

## Why now

On 2026-10-21 an image of 504 KB, larger than the board's code region, overwrote the NVS partitions that sit after it. Every image flashed afterwards asserted in its NVS init, before USB came up, so the console never returned and the board looked dead. `erase: true` is the suite's documented way to clear exactly that leftover state (the comment at `hardware.rs:228-232` says so), and it failed on this chip. Recovery took a throwaway build with Zephyr's flash shell and a manual `flash erase` of the partition. Any STM32G0 on the bench hits the same wall.

## Done when

- [ ] A unit test on the region filter, fed the STM32G0B1VE memory map as probe-rs 0.31 declares it, keeps `0x08000000..0x08080000` and drops the `0x1fff7800..0x1fff7820` alias; a second case shows any `is_alias` region or one with `write: false` is dropped.
- [ ] A test shows a region the flash algorithms cannot erase fails the request before any `flashing::erase` call runs.
- [ ] The flash response lists the ranges erased; embarch-api's MCP text prints them.
- [ ] Bench check on an STM32G0: write a non-erased word in a partition the image does not cover, flash with `erase: true`, read that word back as `0xFFFFFFFF` with `mem-read`, and the image boots.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md` updated for what `erase` erases, `changelog.d/` fragment dropped; follow-up filed for embarch-api if its tool description needs the new behaviour.
