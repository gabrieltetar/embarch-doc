# 146 — `StatusResponse.last_images` is `Option<Vec<_>>`, so an old Core reads as unknown, not as nothing flashed

**State:** open
**Source:** reviewer finding on api/145 (code `3625584`, doc `71db5e4d`), 2026-10-26. Filed from `inbox/api-last-images-option-per-decision-58.md` in api/145's fold.
**Scope:** api
**Hardware:** none
**Owner:** no

## What

`crates/embarch-core-client/src/client.rs:91` declares `pub last_images: Vec<FlashedImage>` with `#[serde(default)]`. Make it `Option<Vec<FlashedImage>>` (`#[serde(default)]`, skip-when-None where serialized), and have `status` (`src/cli.rs` ~415, `src/tools.rs` ~906) report `null` for a Core that did not send it, distinct from `[]` (Core sent an empty record). Adjust the doc comment ("Empty for a Core that predates it").

## Why now

`embarch-api` decision 58 (`decisions/client-crate.md`): "every response field this crate deserializes that Core may not yet send is `Option<T>` with `#[serde(default)]` ... `None` is never presented as a fabricated value". Its "Applied api/139" paragraph rejects exactly this shape: `FlashResponse.erased` is `Option<Vec<String>>` because "an empty list on an old Core would read as 'nothing erased'... a claim Core never made". Here an old Core yields `last_images: []`, which reads as "nothing flashed", the claim decision 90 itself says must never be made ("an absent chip means unknown, never nothing flashed"). The clause is contradicted, not refined: 58 is not updated in api/145 and the `Vec` is not recorded as an exception. `lease` (`Option`) is compliant. A one-field fix forward is smaller than reverting `3625584`. `embarch-ui` path-depends on this crate; check it does not read `last_images`.

## Done when

- [ ] `last_images` is `Option<Vec<FlashedImage>>`; a test parses an old-Core `/status` body and asserts `None`, and a body with `"last_images": []` asserts `Some(empty)`.
- [ ] `status` output (MCP tool, CLI, `--json`) distinguishes the two.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10), and `embarch-ui` still builds against the crate.
- [ ] Decision 90 says which shape it is, `changelog.d/` fragment dropped.
