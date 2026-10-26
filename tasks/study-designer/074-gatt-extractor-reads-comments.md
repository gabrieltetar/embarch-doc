# 074 — The GATT extractor ignores definitions inside C comments

**State:** open
**Source:** DeepSeek V4 Pro review 2026-10-25 (embarch-study-designer finding 7), verified by Opus against embarch-study-designer@b9a2d5df
**Scope:** study-designer
**Hardware:** none
**Owner:** no

## What

Four of the extractor's scanners match raw file text, comments included: scalar `#define`s, `_UUID_VAL` macros, `bt_uuid_128` variables and `BT_GATT_SERVICE_DEFINE` blocks. Only the property-alias scanner is line-anchored and strips a trailing comment. The scan walks a whole firmware repo (decision 57), so commented-out code is likely to be in what it reads. Three outcomes follow, all from definitions the compiler never sees:

- A commented `#define FOO_BASE 0x…` beside the live one makes every UUID that uses `FOO_BASE` fail with `AmbiguousSymbol`. The error names a definition that is not compiled.
- A commented-out `BT_GATT_SERVICE_DEFINE(...)` block, with its UUID variables still defined, is extracted as a live service. A study author can then pick a characteristic the firmware does not have. This is the silent case.
- A prose comment that names the `BT_GATT_SERVICE_DEFINE(` marker without a balanced closing paren fails the whole scan with `UnbalancedCall`.

When done, the extractor reads each file as the compiler does with respect to comments. One direction: a single comment-stripping pass over `file.text` before any scanner runs. It keeps string and character literals intact and keeps line structure, so `#define` anchoring and line-continuation joining still work. Conditional compilation (`#if 0`, `#if`/`#else`) is out of scope. The extractor already reports conditionals deliberately and does not evaluate them.

## Why now

- `src/gatt_extract.rs:659` (`parse_scalar_constants`), `:677` (`parse_uuid_macros`), `:736` (`parse_uuid_vars`) and `:784-795` (`parse_gatt_services`, which finds blocks with a plain `find`) all scan raw text. Only `:950` (`parse_property_aliases`) is anchored, and it strips comments at `:963-966`.
- The module's own heading at `:36` is "Failing loudly, at the point of use". A commented-out service extracted as live is a silent wrong result, and an `AmbiguousSymbol` that blames a comment is a loud wrong one.

## Done when

- [ ] Fixture tests, each with a live definition plus a commented copy in `//` and in `/* */` form: a scalar constant resolves to the live value. A `_UUID_VAL` macro resolves. A commented-out `BT_GATT_SERVICE_DEFINE` block contributes no service. A comment mentioning the macro name with an unbalanced paren does not fail the scan.
- [ ] A `//` or `/*` inside a string literal does not start a comment. A test covers it.
- [ ] The existing extractor tests and the firmware test vectors pass unchanged.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/` fragment for anything suite-level it made false.
