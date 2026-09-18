# 045 — `RunProtocol` is a served built-in, and `build_study` takes a protocol catalogue

**State:** done — landed 2026-09-17 by the owner's session, both halves back to back.
**Source:** embarch-study-designer/open.md — "`Study.protocols` has no path in the Study Designer UI"
**Scope:** suite
**Hardware:** none
**Owner:** no

## What

`build_study`'s signature changed, and its only two non-test callers are both in
`embarch-ui` — so the crate commit and its UI counterpart are a lockstep pair
landed back to back, crate first. The precedent is `suite/017`, which changed
`MergedAction::BuiltIn`'s shape and its `app.js` consumer the same way.

`BuiltInActionKind` gains `RunProtocol`; `RowAction::BuiltIn` gains
`protocol`/`entry_state`, both by name; `build_study` takes the repo's `.eap`
catalogue and **derives** what the study carries from the rows that name it.

## Why now

The trigger `embarch-study-designer/open.md` names fired on 2026-08-27: a real
manifest drove a real DUT through 34 request/pump/consume cycles, built by a
throwaway Rust program because nothing in the suite could author one.

## Done when

- [x] `embarch-study-designer` f2fa849 — the variant, the two fields, the fifth
      parameter, five `BuildStudyError` variants with asserted `Display`
      strings, and the false `validate_protocol` claim on `Action::RunProtocol`
      corrected.
- [x] `embarch-ui` 0d9dabf — `eap-parse` on, `sd.protocols()`/`protocol_defs()`,
      every `build_study` caller updated.
- [x] Gate green in both repos (`cargo test`, `clippy --all-targets -D warnings`).
- [x] `embarch-study-designer` decisions 75/76 and the authoring amendment;
      `open.md`'s bullet closed and the divergence question opened;
      `changelog.d/` fragments; `features.d` rows.
