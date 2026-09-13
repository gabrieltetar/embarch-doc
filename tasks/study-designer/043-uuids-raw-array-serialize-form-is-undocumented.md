# 043 — `Uuid`'s raw-array `Serialize` form is undocumented anywhere in `embarch-study-designer`

**State:** open
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

- [ ] A decision (or an addition to `interfaces/types.md`, since `Uuid` and its raw/hyphenated split
      is squarely study-type material) states plainly: `Uuid`'s `Serialize`/`Deserialize` is the raw
      16-byte-array derived form; hyphenated text is a display/parse-only convenience produced and
      consumed explicitly at each site (name them, or point at the ones this drop found: `src/ids.rs`
      `to_hyphenated`/`parse`, `embarch-ui/src/study_designer.rs::uuid_field`, the authoring `Raw`
      row path in `decisions/authoring.md` decision 37).
- [ ] `changelog.d/` fragment.
