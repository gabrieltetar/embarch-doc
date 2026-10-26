# 076 — `OutpostManifest` reads the `devices` and `functions` tables, so GPIO records are named in Core's trace CSV as they are in the reference decoder

**State:** claimed by agent/study-designer/076-outpost-manifest-gpio-names, 2026-10-26 02:23
**Source:** DeepSeek V4 Pro suite review 2026-10-25 (cross-repo finding 3), verified by Opus against embarch-study-designer@b9a2d5df and embarch-outpost@2968f0c1
**Scope:** study-designer
**Hardware:** none — a table lookup tested against a literal manifest and literal records. No capture is needed.
**Owner:** no

## What

Manifest schema 2 added two tables: `devices` (a port's `struct device *` → name) and `functions` (a code address → symbol). `embarch-outpost`'s reference decoder uses them to name `GpioDispatch` (9) and `GpioCallbackDone` (10) records. `OutpostManifest` in `src/outpost.rs` has neither field. Serde ignores both tables, and `label()` returns an empty string for both kinds. Core renders every `*.trace.csv` through this type, so a study on firmware with GPIO tracing on (`TRACE_GPIO` defaults to `y`) gets an empty `name` column for every GPIO row. The Python decoder names the same rows. The two decoders give different output for one wire format.

Direction: add `devices` and `functions` as `#[serde(default)]` maps, so a schema-1 manifest still parses. In `label()`, look up kind 9's `a` in `devices`, and look up kind 10's `a` in `functions` with bit 0 masked. `decode_outpost.py` does that masking, and `interfaces/wire.md` requires it ("a decoder must mask before looking a handler up or every one renders unnamed"). An address the manifest does not name stays empty, never guessed, which is the rule `label()` already follows.

**Dispatch note, 2026-10-26:** this is a shared crate (`embarch-core` path-depends on it); keep the
change additive and do not alter a serialized type Core writes, so no wire bump is in play. `open.md`
is in reserve at 4,473 / 5,120 B under `tasks/study-designer/026` (blocked, nothing payable): do not
grow it. Read `check-doc-size.py --pressure` for whichever `decisions/*.md` you file into before you
write, and if it would push that file into reserve, file `tasks/study-designer/<NNN>-compact-study-designer.md`
in the same commit.

## Why now

- Generator: `embarch-outpost` `scripts/gen_outpost_manifest.py:58-61` (schema 2 added both tables), `:620-622` (emits them), keys formatted `0x%08x` at `:543` and `:565`.
- Reference decoder: `scripts/decode_outpost.py:283-284` and `:330-336`.
- Rust: `src/outpost.rs:469-494` (the struct), `:557-587` (`label()`). Core uses it at `embarch-core` `src/outpost_manifest.rs:35-37` (at `40a58ccb`) and path-depends on this crate, so no Core change is needed.
- `embarch-outpost/interfaces/wire.md:7` says the encoder, this crate's decoder and the generator "must agree". `wire.md:36` describes the handler lookup. `embarch-outpost/interfaces/integration.md:26` gives `TRACE_GPIO`'s default.
- No test sees the difference: `embarch-outpost`'s `tests/cross_decoder.py` compares the decoders over a `native_sim` fixture that has no GPIO device.

## Done when

- [ ] A unit test builds a manifest from literal JSON with both tables, and records of kinds 9 and 10 from literal values. The kind-10 pointer has bit 0 set. `to_csv_row` puts the device name and the handler name in the `name` column.
- [ ] A manifest with neither table (schema 1) still parses, and kinds 9 and 10 render with empty names. An address missing from a present table also renders empty.
- [ ] The existing outpost render tests and the committed layout-3 fixtures pass unchanged.
- [ ] If a cross-decoder fixture with GPIO records is wanted, it goes to `inbox/` for whichever repo owns the fixture. It is not written from here.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped.
