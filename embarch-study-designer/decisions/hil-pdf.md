# embarch-study-designer decisions: the PDF text extractor and number grammar

**Status:** active, 2026-11-22.

What `tasks/study-designer/088` (the plan's M1.11 library half, `notes/hil/14`) decided building the two text halves of [hil-pdf.md](../interfaces/hil-pdf.md). The contract and the grammar are that doc's; what follows is the library and where the doc was silent.

Index: [../decisions.md](../decisions.md). Current truth: [../interfaces/hil-pdf.md](../interfaces/hil-pdf.md).

### 101 — The reader is `lopdf` with its default features off, behind a `pdf-text` feature that implies `std`

`pdf-text = ["std", "dep:lopdf", "dep:unicode-normalization"]`, off by default (**amended 2026-11-25:** `number_grammar` is behind `std` now, for a host step's parse, [decision 108](host-parse.md); the reader stays here); nothing else turns it on, so dev-bench's `no_std` build and the four other consumer feature sets gain no dependency. `lopdf` gives the page tree in order, filters and decryption-free object access; everything that is the *contract* (the content-stream interpreter, the ToUnicode parser, widths, NFKC, lines, words) is this crate's own, so the library can be swapped without touching the contract. *Rejected:* `pdf-extract` and `lopdf`'s own `extract_text`, which re-flow and silently drop glyphs they cannot map, the two things the contract forbids; hand-rolling the object parser. `unicode-normalization` does NFKC. **Not measured on a rendered Typst PDF**: only hand-assembled fixtures have run, until M1.9's fixture exists.

### 102 — What the extractor adds to the doc's contract

A run ends at a `TJ` adjustment that opens a gap over 0.3 `size`, as well as at each string operator; a run carries `x_end` (its last glyph's advance end), from the font's `Widths` or a CID font's `W`/`DW`, and `DEFAULT_GLYPH_WIDTH_EM = 0.5` *(assumed)* where a font gives none, so a word gap between runs is measurable. Form XObjects are followed (depth 8) so a numeral inside one is not invisible; images and paths yield nothing. A font with no ToUnicode map makes every glyph of it unmapped. A text operator naming a font the resources lack is an error, never a skip.

### 103 — What the grammar adds to the doc's

Opaque stripping takes any run of the trailing marks plus one `.` wherever it falls among them. A zero has one significant digit (`0.00` too); the exponent's digits are not counted; a value is `{negative, coefficient, exp10}`, exact, and `normalised()` moves trailing zeros into the exponent so `4.50` and `4.5` compare equal. `+` is a sign but not negative. A sign already consumed by an earlier token (the exponent's) is never taken again.
