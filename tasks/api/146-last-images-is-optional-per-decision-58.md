# 146 — `StatusResponse.last_images` is `Option<Vec<_>>`, so an old Core reads as unknown, not as nothing flashed

**State:** done on agent/api/146-last-images-optional, 2026-10-26
**Source:** reviewer finding on api/145 (code `3625584`, doc `71db5e4d`), 2026-10-26. Filed from `inbox/api-last-images-option-per-decision-58.md` in api/145's fold.
**Scope:** api
**Hardware:** none
**Owner:** no

## Dispatch note, 2026-10-26 07:07 leg

**Shared crate.** `embarch-core-client` is path-depended on by `embarch-ui`; this change is a public field
type change. `grep -rn last_images` in the `embarch-ui` main checkout (read only) found no use as of
dispatch, so `ui` should still build, and the leg builds `embarch-ui` against the merge. Keep the change to
that field and its readers; do not rename or reshape anything else in the crate.

**Reserve.** `embarch-api/decisions/client-crate.md` is 11,581 / 12,288 B (707 B left, filed under
`api/140`); `embarch-api/open.md` 4,297 / 5,120 B (823 B left, filed under `api/144`). Decision 90 lives in
`decisions/lease.md`, which has room: record the shape there. If you must touch decision 58's "Applied"
list in `client-crate.md`, one line, no more.

**Isolation.** Do not reach the owner's live services. No live Core (no request to the Windows service
or any running Core, no CLI or MCP call against one), no desk on `:4891`, no geckodriver on `:4444` and no
UI on `:4899`, no real serial ports or debug probes, no owner data directories (any instance you start
gets a fresh temp dir), and no MCP tools at all. Test against fixtures and stubs only. Kill only processes
you started, by PID.

## What

`crates/embarch-core-client/src/client.rs:91` declares `pub last_images: Vec<FlashedImage>` with `#[serde(default)]`. Make it `Option<Vec<FlashedImage>>` (`#[serde(default)]`, skip-when-None where serialized), and have `status` (`src/cli.rs` ~415, `src/tools.rs` ~906) report `null` for a Core that did not send it, distinct from `[]` (Core sent an empty record). Adjust the doc comment ("Empty for a Core that predates it").

## Why now

`embarch-api` decision 58 (`decisions/client-crate.md`): "every response field this crate deserializes that Core may not yet send is `Option<T>` with `#[serde(default)]` ... `None` is never presented as a fabricated value". Its "Applied api/139" paragraph rejects exactly this shape: `FlashResponse.erased` is `Option<Vec<String>>` because "an empty list on an old Core would read as 'nothing erased'... a claim Core never made". Here an old Core yields `last_images: []`, which reads as "nothing flashed", the claim decision 90 itself says must never be made ("an absent chip means unknown, never nothing flashed"). The clause is contradicted, not refined: 58 is not updated in api/145 and the `Vec` is not recorded as an exception. `lease` (`Option`) is compliant. A one-field fix forward is smaller than reverting `3625584`. `embarch-ui` path-depends on this crate; check it does not read `last_images`.

## Done when

- [x] `last_images` is `Option<Vec<FlashedImage>>`; a test parses an old-Core `/status` body and asserts `None`, and a body with `"last_images": []` asserts `Some(empty)`.
- [x] `status` output (MCP tool, CLI, `--json`) distinguishes the two.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10), and `embarch-ui` still builds against the crate.
- [x] Decision 90 says which shape it is, `changelog.d/` fragment dropped.
