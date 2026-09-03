# 003 — `schema_version` and `error_kind` are documented and were never built

**State:** open
**Source:** embarch-api/open.md — "**`schema_version` and `error_kind` are documented and were never built.**"
**Scope:** api
**Hardware:** none

## What

`embarch-api/decisions/surface.md` 16 and 24 and
`embarch-api/interfaces/tools.md` describe `schema_version` and `error_kind` as
fields present on **every** `--json` object. Neither string appears anywhere in
the crate's source, so a caller told to branch on `error_kind` rather than on an
exit code has nothing to branch on, and a caller told to check `schema_version`
cannot detect a surface change at all.

Two honest endings, and the task is to pick one with a reason written down:

- **Build them** — add both fields to every `--json` emitter, with a test that
  fails when a new emitter forgets one (a shared serializer or a trait, not a
  convention).
- **Retire them** — delete the claim from decisions 16/24 and `interfaces/tools.md`,
  record the retirement in `decisions.md` per `DOC-PROTOCOL.md` §7.2, and say in
  `open.md` what a caller should branch on instead.

Prefer whichever is smaller *and* leaves no doc claiming a field that does not
exist. A documented-but-absent field is worse than an absent one either way.

## Why now

This is a contract this crate publishes to agents and scripts. Every other
`--json` consumer in the suite was written from `interfaces/tools.md`, so the
gap is not theoretical — it is the file a caller is told to read.

## Done when

- [ ] Either both fields exist on every `--json` object with a test that keeps
      them there, or every doc claiming them no longer does.
- [ ] `decisions.md` records the choice and why.
- [ ] `open.md`'s "Known wrong, not fixed" entry is removed or rewritten to
      whatever is genuinely still open.
- [ ] Gate green (`embarch-parallel-agents.md` §10).
- [ ] `changelog.d/` fragment dropped.
