# 134 — embarch-api: print the erased ranges from `POST /flash`, and describe the new `erase` behaviour

**State:** claimed by agent/api/134-flash-print-erased-ranges, 2026-10-26 00:39
**Reserve, for the worker:** no `embarch-api` doc is in reserve today (`open.md` 3,780 / 5,120 B after `api/113`).
**Source:** `core/096`, 2026-10-25 (embarch-core decision 84)
**Scope:** api
**Hardware:** none — tool text and a parameter description, tested against the mock Core.
**Owner:** no

*Header completed by the supervisor at filing (2026-10-26): the worker's drop had no `State:`, no `Owner:` and `Hardware: no`; the body is unchanged.*

## What

Core's `POST /flash` response is now `{ flashed, chip, erased }`, `erased` a list of strings like `"0x08000000..0x08080000"` (empty without `erase`, or when a vendor tool flashed). `erase: true` now skips alias and non-writable NVM regions (STM32 option bytes) and fails before any erase if a region has no usable flash algorithm. embarch-api's `flash` MCP tool text should print the erased ranges when present, and its `erase` tool description should say it never touches option bytes and never chip-erases. The field is additive; an older API ignores it.

## Done when

- [ ] The MCP flash result text lists the erased ranges when `erased` is non-empty.
- [ ] The `erase` parameter description matches Core decision 84.
