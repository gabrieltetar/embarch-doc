# 089 — `hil-pdf.md`'s footer band is 8 to 16 mm, measured on a Typst page

**State:** open
**Source:** `embarch-api/decisions/verify-report.md` decision 123 — "the footer's baseline sits at 14.96 mm (11 pt) and just over 15 mm under the appendix's 9 pt, on the edge of `hil-pdf.md`'s 8 to 15 mm band, so this crate uses 8 to 16 mm (filed against the doc)"
**Issue:** EMB-242
**Scope:** study-designer
**Hardware:** none
**Owner:** no

## Dispatch notes

- Docs only: `embarch-doc/embarch-study-designer/`. No code in `embarch-study-designer` names the band (`number_grammar.rs` leaves the footer to its caller), so this unit has no code branch unless you find one that does.
- The band is in `interfaces/hil-pdf.md`, "The footer rule", "The admitted run": "between 8 mm and 15 mm above the page's bottom edge *(assumed; A4 and Letter alike)*". `decisions/hil-shapes.md` decision 91's *Assumed, not measured* line names the same band.
- What was measured, and on what: `extract_pages` over one Typst 0.15.1 page with embarch-api's footer wrapper, this machine's embedded font set, A4 width. 14.96 mm at 11 pt text, just over 15 mm when the appendix sets 9 pt. `embarch-api` decision 123 reads it, and its `verify_report.rs` already uses 8 to 16 mm. Say exactly that much and no more: one font set, one machine, A4 only.
- Decision 123 also says the extractor's word gap (0.3 `size`) and the 0.5 em width fallback "needed no change" on that page. If `hil-pdf.md`'s status line or decision 91's assumed list should now say which constants one real page has met, change it in the same pass; leave the ones nothing measured (the tick target, the 5 mm centring, Letter) marked assumed.
- `embarch-api`'s own docs and its code comment still say `hil-pdf.md` reads 8 to 15 mm. They are not this scope's; the supervisor carries them to `tasks/api/172`. Do not edit them.
- No file in this sub-project is in reserve. Decisions near their limit here: `streams#39`, `versioning#12`, `seals#17` (each under 80 B left); none is one you should need.

## What

The footer band in the PDF text interface reads 8 to 16 mm and says it was measured, on what, and where the measurement is recorded. The band stays a constant of the interface doc, not of a caller.

## Why now

`verify` check 4 (`tasks/api/171`) read the first real Typst page and found the page number on the band's upper edge. The shared doc and its one reader disagree by a millimetre today, and the next reader of `hil-pdf.md` would build to 15.

## Done when

- [ ] `interfaces/hil-pdf.md`'s footer band reads 8 to 16 mm, with the measurement named (Typst 0.15.1, 11 pt and 9 pt, one font set, A4) and the `embarch-api` decision that took it.
- [ ] Decision 91's assumed list in `decisions/hil-shapes.md` agrees with it.
- [ ] Gate green (`../../embarch-fleet/gate.md`), `changelog.d/` fragment dropped.
