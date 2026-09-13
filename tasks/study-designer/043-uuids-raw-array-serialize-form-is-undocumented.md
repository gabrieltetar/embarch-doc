# 043 — `Uuid`'s raw-array `Serialize` form is undocumented anywhere in `embarch-study-designer`

**State:** done — leg 111, 2026-09-13, `agent/study-designer/043-uuid-serialize-form`
**Source:** `ui/045`'s worker, while fixing `embarch-ui/src/study_designer.rs:1524`'s dead `§4.3`
citation for the same fact (repointed to a bare, section-less file citation; that fix does not
touch this finding).
**Scope:** study-designer
**Hardware:** none
**Owner:** no

## What

`embarch-study-designer::Uuid` is `pub struct Uuid(pub [u8; 16])` with a plain `#[derive(Serialize,
Deserialize)]` (`src/ids.rs`) — so its wire/JSON form is a raw 16-element byte array, and the
hyphenated `8-4-4-4-12` text form only exists via `Uuid::to_hyphenated()`/`Uuid::parse()`, called
explicitly at each site that needs it (an authoring parse, a UI display conversion, …). Two repos
depend on knowing this split (`embarch-ui`'s `study_designer.rs:uuid_field` converts raw array to
hyphenated text on load; `embarch-study-designer`'s own authoring/`Raw` row path parses hyphenated
text back into the type) — but nowhere in `embarch-study-designer`'s docs is this stated:

- `interfaces/types.md`, `interfaces/gatt-types.md`, `interfaces/result-types.md`: none mention the
  raw-array-vs-hyphenated split at all (checked by grep for `Uuid`, `hyphenated`, `array`, `16
  bytes`).
- `src/ids.rs`'s own doc comment (the type's home) states the byte-array layout is deliberate
  (`no_std`-friendly, no `uuid`-crate dependency) but doesn't describe the JSON shape that produces
  as a fact a *consumer* needs.
- The retired, pre-split `design.md` (§4, before the 2026-09-02 split) explicitly punted on this:
  "exact byte/UUID representations (`[u8; 16]` vs. a `uuid`-crate newtype, `no_std`-compatible
  either way) are implementation detail, not a design choice left open here" — so this was never
  written down as a design fact even before the split that removed `design.md`'s section numbers.

## Why now

An undocumented serialization form that two repos' code depends on (and that `embarch-ui` had been
citing under a dead section number for as long as the split has existed, per `ui/045`) is a
different and larger problem than the bad pointer to it: the pointer is now fixed, but there is
still nowhere for a reader to *learn* this fact except by reading `src/ids.rs`'s derive macro
directly.

## Done when

- [x] A decision (or an addition to `interfaces/types.md`, since `Uuid` and its raw/hyphenated split
      is squarely study-type material) states plainly: `Uuid`'s `Serialize`/`Deserialize` is the raw
      16-byte-array derived form; hyphenated text is a display/parse-only convenience produced and
      consumed explicitly at each site (name them, or point at the ones this drop found: `src/ids.rs`
      `to_hyphenated`/`parse`, `embarch-ui/src/study_designer.rs::uuid_field`, the authoring `Raw`
      row path in `decisions/authoring.md` decision 37).
- [x] `changelog.d/` fragment.

## Closed

All three source claims re-derived and confirmed, not merely trusted:

- `src/ids.rs` line 15: `pub struct Uuid(pub [u8; 16])` with plain
  `#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]` — confirmed.
- `Uuid::to_hyphenated()`/`Uuid::parse()` are the only text-form crossings — confirmed by grepping
  every call site of both across the crate (`tools/extract_gatt_config.rs`, `src/eap_parse.rs`,
  `src/vendor.rs`, `src/gatt_extract.rs`, `src/gatt.rs`, `src/lib.rs`, `src/study_builder.rs`,
  `src/gatt_names.rs`, `tests/firmware_test_vectors.rs`): every one goes through one of these two
  methods, nothing else converts between forms.
- No `interfaces/*.md` mentioned the raw-array-vs-hyphenated split — confirmed by grepping
  `interfaces/*.md` for `Uuid`, `hyphenated`, `array`, `16 byte(s)`: `types.md` and `gatt-types.md`
  both say UUIDs are "raw, not symbolic" (registry vs. wire), but neither said what that raw
  *serialize* form is or that hyphenated text only exists via an explicit conversion.

Added a prose paragraph to `interfaces/types.md` (not a new decision — this is a statement of what
the code already does, not a design choice being made) stating the split and naming both consumers:
`embarch-ui/src/study_designer.rs::uuid_field` (read at that path, confirmed real — it already cites
`embarch-study-designer/interfaces/types.md` for this exact fact, which is the pointer this task
fills in) and the authoring `Raw` row path, `decisions/authoring.md` decision 37 (read in full,
confirmed: "UUID parsing arrives alongside it, accepting the hyphenated form, bare hex, or the
16-bit shorthand" — covers the citation).

`interfaces/types.md` is now 9733/12288 B (cap is 12K per `check-doc-size.py --report`, not the
10240 B this task's dispatch note assumed) — 79%, not in reserve (`--pressure` confirms it is not
listed). No compaction task filed; none needed.
