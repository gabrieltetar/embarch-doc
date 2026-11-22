# embarch-study-designer: reading numbers back out of the PDF

**Status:** active, 2026-11-20. Part of the HIL file shapes ([hil-shapes.md](hil-shapes.md)). Design, not yet code. **Every constant here is assumed, not measured** (DOC-CONVENTIONS), until M1.9 renders a fixture and M1.11 reads it; a unit that must change one amends it here. Source: `notes/hil/06-report-and-publish.md`, "Verify" check 4 and "The report"; review round 4 delegated these four rules to this doc. Choices: [decisions/hil-shapes.md](../decisions/hil-shapes.md), decision 91.

**One implementation.** The extractor's contract, the grammar and `plot_ticks` live once in the shared crate's host-only half; embarch-api's plot helper (M1.9) and `verify` (M1.11) both call them, so the helper cannot draw a tick `verify` would not derive. **`plot_ticks` lives in embarch-api's `report_pdf` until it moves here** ([embarch-api decision 110](../../embarch-api/decisions/report-pdf.md), 2026-11-21), and the Typst helper carries its own copy, which a test holds equal to the Rust one; `verify` is to call the Rust one. The prose and `report.typ` rescans of check 4 apply the same grammar to source text.

## The text extractor

Its contract, whatever library M1.11 picks (the crate is not named: the contract is):

- **Input: the PDF's pages in the page tree's order; output, per page, glyph runs in content-stream order**, each `{text, x, y, size}`: `x` and `y` the run's origin in points from the page's bottom-left, `size` its font size. No reading-order heuristic, no re-flow, no de-hyphenation: what the PDF draws, in the order it draws it.
- **Every glyph must map to Unicode** (the font's ToUnicode map). **One glyph with no mapping fails check 4** ("unextractable text on page N"): a numeral that cannot be read back is the failure the check exists to find, so it is never skipped.
- **Text is then normalised**: Unicode NFKC, so a full-width or superscript digit becomes its ASCII digit and a ligature its letters; U+2212 stays as written (the grammar takes it as a sign).
- **Words**: a word is a maximal run of non-whitespace characters on one line. A line break is a change of `y` over 0.5 `size`; a word break is a whitespace character, or a horizontal gap between two glyphs over 0.3 `size` *(assumed)*.
- **Pictures and paths yield no text**, so a numeral drawn as outlines would be invisible here; check 9 refuses that at the source ([06](../../notes/hil/06-report-and-publish.md#verify)).

## The number grammar

Applied to each word, left to right, after the opaque-word rule.

**Opaque words first.** A word, with leading `( [ " '` and trailing `) ] " ' , ; :` and a trailing `.` stripped, that is **byte-equal to a string value** `report-data.json` holds (a date, a hash, an ID, a revision tag) is consumed whole: its digits are not numbers. This is "equals a value `report-data.json` holds" (06). A hash split across a line is two words and fails; the layout must keep an ID on one line *(shape)*.

**Otherwise the numerals of the word are its number tokens:**

```
token    = [ sign ] mantissa [ exponent ]
mantissa = digits [ "." digits ] | "." digits
digits   = [0-9]+                      (ASCII only, after NFKC)
exponent = ( "e" | "E" ) [ sign ] digits
sign     = "-" | "+" | U+2212
```

- **Longest match, left to right, no overlap.** `4.75–5.25` is two tokens (the en dash U+2013 is no sign); `R3.2` is `3.2`; `SHA-256` is `256`; `v2` is `2`; `1,234` is `1` and `234`; `12.` is `12` and the stop is punctuation. **No separator is a digit-group mark and the decimal mark is `.` only** *(shape: conservative, a split only adds tokens that must each match)*.
- **A sign belongs to the token only if** it directly precedes the first digit or a leading `.`, **and** the character before it is not a letter or digit (start of word, `(`, `=`, whitespace). `A-3` is the token `3`; `x=-3` is `-3`; `5-3` is `5` and `3` (a hyphen between numerals is no sign).
- **An exponent is taken only when a digit follows it**; `1e` is `1`.
- **A token yields `{text, value, sig_digits, decimals}`.** `value` is the exact decimal the text writes (not an `f64`); **`sig_digits` counts the written digits after stripping leading zeros, trailing zeros after a decimal point included**, and **an integer's written digits all count**, `1200` having four, so a match by 02's rule ("equals that measurement's value rounded to the significant digits written") never rounds an integer to hundreds *(shape)*; `decimals` the digits after the point.
- **Nothing is exempted by its shape**: a year, a version and a page count are numbers until an opaque-word, citation or measurement match says otherwise. The only structural exemptions are those of check 4's list: the footer's page number and an axis tick.

The unit and value conversions (mV and V) and the match itself are M1.11's and M1.10's; they take `{value, sig_digits}` from here.

## The plot helper's tick algorithm

**`plot_ticks(lo, hi) -> Ticks { step_mantissa, step_exp10, first_k, last_k, decimals, texts }`**, for each axis of each plot, **linear axes only**. `lo` and `hi` are the minimum and maximum of that axis over every series of the plot, as read from the signed file (a per-bin min and max series counts both); no tick list is trusted from the PDF.

1. If `lo` or `hi` is not finite, or `lo > hi`, the plot is refused.
2. **If `lo == hi`: one tick, at `lo`, written with the shortest decimal that round-trips, no exponent.** Done.
3. `raw = (hi - lo) / (TICK_TARGET - 1)`, **`TICK_TARGET = 5`** *(assumed)*.
4. `e = floor(log10(raw))`, corrected so `10^e <= raw < 10^(e+1)` (a compare loop, not the float result alone); `f = raw / 10^e`.
5. **`m = 1` if `f < 1.5`, `2` if `f < 3`, `5` if `f < 7`, else `10` (then `m = 1`, `e = e + 1`).** (Heckbert's rounding thresholds.) `step = m × 10^e`, `m` in {1, 2, 5}.
6. `first_k = floor(lo / step)`, `last_k = ceil(hi / step)`, each corrected by a compare, so `first_k × step <= lo` and `last_k × step >= hi` hold in `f64` (the note below the fixtures). **The axis is drawn from `first_k × step` to `last_k × step`.**
7. **Ticks are `k × step` for `k` from `first_k` to `last_k`.** Each is written **with `decimals = max(0, -e)` digits after the point, no exponent, no digit grouping, an ASCII `-` for a negative** (so it reads as a sign in the grammar), and `-0` written as `0`. The text is produced by integer arithmetic on `k × m` scaled by `10^decimals`, never by formatting an `f64`.
8. **The set of tick texts of every plot of the report is what `verify` admits as axis ticks** for check 4, whatever the page; a number that equals a tick text but sits in prose is still a number to match, since the exemption is by being a tick, and the helper's own tick glyph runs are the ones exempted *(shape)*.

Fixtures M1.9 and M1.11 both carry (hand-computed): `(0, 100)` gives step 20, ticks `0 20 40 60 80 100`; `(0, 3.3)` gives step 1, `0 1 2 3 4`; `(4.75, 5.25)` gives step 0.1, `4.7 4.8 … 5.3`, one decimal; `(-10, 10)` gives step 5, `-10 -5 0 5 10`; `(2, 2)` gives the single tick `2`.

**The arithmetic is `f64`, as M1.9 built it** ([embarch-api decision 110](../../embarch-api/decisions/report-pdf.md), 2026-11-21): the compares in steps 4 and 6 correct `e`, `first_k` and `last_k` against float slack, and step 5 compares the float `f`, so a range whose `f` lands on a threshold takes the float side. `(-0.3, 0.3)` gives `f = 1.4999…` and step 0.1, where decimal arithmetic gives 0.2; it is a fixture, so `verify` derives what the helper drew.

## The footer rule

**The footer's page number is the one number `verify` admits by position**, in the exemption's own words (06 check 4): "the page number at the footer's glyph position, nowhere else, and equal to the 1-based index of its page".

- **The compile wraps `report.typ` in a page setup that prints the page number in a footer**, centred, in ASCII digits with no other character (no "Page", no "of N"); the wrap is embarch-api's (M1.9), and a `report.typ` that sets its own footer is refused at publish *(shape)*.
- **The admitted run** is the one glyph run on a page that is a single word of digits only, whose horizontal centre is within **5 mm of the page's centre** and whose baseline is **between 8 mm and 15 mm above the page's bottom edge** *(assumed; A4 and Letter alike)*.
- **At most one run on a page is admitted**; a second candidate in the band is an ordinary number to match, so a duplicated or faked page number does not hide.
- **Its value must equal the page's 1-based index in the page tree** as the PDF's structure gives it, not what the text says of itself; a mismatch fails check 4 naming the page.
- A page with no admitted run is not an error (a full-bleed plot page); a page number nowhere else is exempt nowhere else.
