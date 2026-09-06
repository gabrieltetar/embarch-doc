# Withdraw the `Study.gatt` / `DeclaredGatt` field from the docs, or record it as unbuilt

**State:** open
**Source:** owner's repo survey, 2026-09-06 — three documents describe a shipped feature no code in the suite implements
**Scope:** study-designer
**Hardware:** none
**Owner:** no

## What

`embarch-doc/embarch-study-designer/interfaces/types.md:14` documents `gatt: Option<DeclaredGatt>`
as a `Study` field, `spec.md:58` lists it in "What a study carries", and `interfaces/limits.md:34`
gives it a `MAX_DECLARED_SERVICES` bound. `Study` (`src/study.rs:91-224`) has no such field, and a
suite-wide grep for `DeclaredGatt` / `declared_gatt` / `MAX_DECLARED_SERVICES` — plus
`git log -S DeclaredGatt` — returns nothing at all. **The type has never existed anywhere.**

`spec.md` stops asserting the field, `interfaces/types.md` and `interfaces/limits.md` drop the
phantom row and constant, and decision 45 in `decisions/declares.md` is restated as
designed-but-unbuilt with its trigger — its reasoning preserved, its number never reused.

## Why now

`../../DOC-PROTOCOL.md` makes `spec.md` "what is true now", and this is the largest single
divergence between these docs and the code: three documents describing a reconciliation feature
("live discovery wins, and the difference is reported") a reader could author against and find will
not deserialize.

## Done when

- [ ] No file under `embarch-doc/embarch-study-designer/` names `DeclaredGatt`, `Study.gatt` or
      `MAX_DECLARED_SERVICES` as current truth.
- [ ] Decision 45 is preserved with its reasoning but marked unbuilt, naming what would have to
      exist for it to be true.
- [ ] The unbuilt state appears in `open.md` under an existing heading, phrased as a deferral with a
      trigger.
- [ ] `grep -rn "DeclaredGatt" embarch-doc/embarch-study-designer/` returns only tombstone prose.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false.
