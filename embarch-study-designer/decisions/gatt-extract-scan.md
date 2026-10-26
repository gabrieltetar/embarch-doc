# embarch-study-designer decisions: What the GATT extractor reads

**Status:** active, 2026-10-26.

What text the extractor treats as source. Index: [../decisions.md](../decisions.md). The scan itself: [gatt-extract.md](gatt-extract.md).

### 85 — The extractor strips C comments once, before any scanner runs

Four scanners (scalar `#define`s, `_UUID_VAL` macros, `bt_uuid_128` variables, `BT_GATT_SERVICE_DEFINE` blocks) matched raw file text, comments included, and only the property-alias scanner stripped one. Decision 57 walks a whole firmware repo, so commented-out code is in what it reads, and three results followed from definitions the compiler never sees: a commented `#define FOO_BASE` beside the live one made every user of it `AmbiguousSymbol` (a loud wrong answer naming an uncompiled line); a commented-out service block whose UUID variables were still live was **extracted as a live service** (the silent one: a study author could pick a characteristic the firmware does not have); a prose comment naming `BT_GATT_SERVICE_DEFINE(` with no closing paren failed the whole scan with `UnbalancedCall`.

`extract_from_files` now runs `strip_c_comments` over each file's text first. A `//` comment is dropped to its newline; a `/* */` comment becomes one space plus the newlines it held, so `#define` anchoring and continuation joining behave as on the original; string and character literals pass through untouched, so `"http://"` and `"/*"` do not open a comment. An unterminated `/*` runs to end of file, as in C.

**Not done, deliberately:** conditional compilation. `#if 0` is still read as live, as every `#if`/`#else` is (decision 78 reports those rather than evaluating them). A `//` comment ending in a backslash does not swallow the next line, as a real preprocessor would; the cost is reading one extra line in a case nobody writes. Neither is measured against a real repo; both are assumed rare.
