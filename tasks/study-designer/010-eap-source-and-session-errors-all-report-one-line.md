# Give `.eap` source and session errors their own source line

**State:** open
**Source:** owner's repo survey, 2026-09-06 — `interfaces/eap.md` states line-accurate errors as a property; it is untrue for a whole class
**Scope:** study-designer
**Hardware:** none
**Owner:** no

## What

`src/eap_parse.rs:1167` computes `line0` as *the first state's* line, then uses it for every
source-scoped error (`:1175`, `:1182`, `:1187`), every session-variable error (`:1322`, `:1328`,
`:1330`) and the protocol-name and validate errors (`:1430`, `:1439`). So a duplicate `source`
declared at line 4 of a long manifest is reported at whatever line the first `state` happens to sit
on. `EapError`'s own doc at `:110-113` says each error carries the source line; the only test of
that (`:1752-1758`) covers a lexer error.

`AstProtocol`'s sources and session variables should carry the line they were parsed at, and
`resolve` should report each error against its own declaration.

## Why now

`decisions/protocols.md` decision 58 justifies a purpose-built grammar over TOML on legibility, and
`interfaces/eap.md` states line-accurate errors as a property of it. This is that property being
untrue for every error an author is most likely to hit.

## Done when

- [ ] Sources and session variables carry a line through the AST, and no resolve-time error for
      either uses `line0`.
- [ ] Tests assert the reported line for a duplicate source, an over-long source name and a
      duplicate session variable, in a manifest where the first `state` is many lines away.
- [ ] The remaining uses of `line0` (protocol name, `validate_protocol`) are either given a real
      line or documented as protocol-wide.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10), including
      `cargo test --no-default-features --features eap-parse`.
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false.
