# 074 — The GATT extractor ignores definitions inside C comments

**State:** done — agent/study-designer/074-gatt-extractor-reads-comments, 2026-10-26
**Source:** DeepSeek V4 Pro review 2026-10-25 (embarch-study-designer finding 7), verified by Opus against embarch-study-designer@b9a2d5df
**Scope:** study-designer
**Hardware:** none
**Owner:** no

## Dispatch note, 2026-10-26 05:14 leg

**Doc reserve in your scope:** `decisions/gatt-extract.md` is 11,053 / 12,288 B, **6 B under its reserve line**, so any addition puts it in reserve. Put a new decision in a new topic file listed in `decisions.md` (`decisions/protocol-exec.md` took the last one for the same reason), or, if it belongs in `gatt-extract.md`, file `tasks/study-designer/<NNN>-compact-study-designer.md` in the same commit. `open.md` is 4,473 / 5,120 B (647 B left) under `tasks/study-designer/026`, blocked; do not grow it unless you close something in it.

**Shared crate, run every `test.yml` cell** (default, alloc, std, gatt-extract, eap-parse, study-ui, and the three clippy cells), not just the default one: the last leg's gate ran them all and found the alloc cell had been red on `main`.

**Isolation:** host-side only; never call the `mcp__embarch-api__*` or desk tools, never touch the live Core, the desk on :4891 or the owner's data dirs. Fixtures, not a real firmware repo from this machine.

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

- [x] Fixture tests, each with a live definition plus a commented copy in `//` and in `/* */` form: a scalar constant resolves to the live value. A `_UUID_VAL` macro resolves. A commented-out `BT_GATT_SERVICE_DEFINE` block contributes no service. A comment mentioning the macro name with an unbalanced paren does not fail the scan.
- [x] A `//` or `/*` inside a string literal does not start a comment. A test covers it.
- [x] The existing extractor tests and the firmware test vectors pass unchanged.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/` fragment for anything suite-level it made false.
