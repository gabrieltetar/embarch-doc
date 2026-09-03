# 003 — `schema_version` and `error_kind` are documented and were never built

**State:** done on agent/api/003-schema-version-error-kind, 2026-09-03 — **split, not one ending**: `schema_version` built, `error_kind` retired (embarch-api decision 50)
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

- [x] Either both fields exist on every `--json` object with a test that keeps
      them there, or every doc claiming them no longer does. **Both, one field
      each.** `schema_version` is on every `--json` object, every NDJSON line
      and every JSON MCP result, stamped by `json_out` — the only module that
      turns a `serde_json` value into text; `tests/json_surface.rs` runs the
      real binary for all 22 subcommands and asserts the field on what each
      printed, a `cli.rs` guard test fails if `cli.rs`/`tools.rs` grows its own
      serializer, and a tripwire on the subcommand count stops a new subcommand
      being added without being added there. No doc claims `error_kind` any
      more (`decisions/surface.md` 16 is a tombstone, `interfaces/tools.md`
      says outright there is none).
- [x] `decisions.md` records the choice and why. Decision **50** in
      `decisions/surface.md`, indexed in `decisions.md`; 16 retired per
      DOC-PROTOCOL §7.4, 24 updated to what was actually built.
- [x] `open.md`'s "Known wrong, not fixed" entry is removed, replaced by an
      "Unfinished couplings" entry for what is genuinely still open — a failure
      *kind* for a scripted caller, whose prerequisite is in `embarch-core`,
      not here.
- [x] Gate green (`embarch-parallel-agents.md` §10). `cargo build`,
      `cargo test` (7+63+12+8+3+16 pass), `cargo clippy --all-targets -D
      warnings`, all six doc checks, `check-ownership.py` both sides.
- [x] `changelog.d/` fragment dropped. Two: `api-json-schema-version.decided`
      and `api-json-startup-failure.fixed`.

## Why the split, in one paragraph

Retiring both was smaller; building both was not available at this cost.
`schema_version` was ~10 lines because the CLI already funnelled every
`--json` object through one function, and its motivating reader (an
"anticipated UI") now exists — retiring a correct, nearly-free decision
because nobody had wired it up would have been the wrong economy. `error_kind`
is the opposite: its headline half is "Core's own error code verbatim", and
Core serves plain text on every non-2xx with its `{code, message, cause}` body
deferred rather than built, so delivering it means Core first, then a new
public typed error on `embarch-core-client` (which `embarch-ui` also depends
on), then a kind chosen at ~43 error sites here — and the field would still be
empty for most real failures. That is a second documented-but-absent field at
several times the cost of the one that could be kept. Decision 50 also records
the trap: an `error_kind` derived from the HTTP status code is a *coarser*
vocabulary than decision 12's and must not ship under decision 16's name.

## Found in the same pass, fixed here

A CLI startup failure — unreadable config, unresolvable token — escaped as
`main`'s `anyhow::Error`, so `--json` printed **nothing at all** and exited 1,
while `interfaces/tools.md` promised that failure as an object on stdout. It
is the class a script hits first on a fresh machine. Now routed through the
same emitter; MCP mode still returns the error, having no JSON surface. Two
tests pin it.

## Not verified, and how

**No hardware debt.** Every claim here is host-side and is covered by a test
that runs under `cargo test`. One thing is deliberately *not* pinned end to
end: a live NDJSON **event** line under `study-status --follow` needs a Core
emitting SSE frames, so the test covers the path against a closed port (its
`transport` items and error object) while `json_out::line` is unit-tested.
That is the same gap `open.md`'s "the study event stream has never met a real
embarch-core" already carries; this task does not widen it.
