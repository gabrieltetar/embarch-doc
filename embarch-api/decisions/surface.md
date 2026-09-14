# embarch-api decisions: The tool and CLI surface — JSON shape and versioning

**Status:** active, 2026-09-13.

How the two front-ends' `--json` shape is built and versioned — the retired `error_kind`, `schema_version`'s own guarantee, and the one serializer both funnel through. How a failure is reported and attributed split out **verbatim** into its own file once this one crossed its reserve band (`tasks/api/069`): [failure-reporting.md](failure-reporting.md). Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md). Per-tool wrapping decisions (why a given tool exists, its params, what it deliberately isn't): [tool-wrapping.md](tool-wrapping.md).

### 16 — `error_kind` on the `--json` object (retired 2026-09-03, see decision 50)
Core's error code passed through verbatim on a Core-originated failure, one of a small native set otherwise, so a script could branch on failure kind rather than on a finer exit-code taxonomy. **Never built, and retired rather than built** — decision 50 has the argument. A caller branches on `success` plus the exit code; the finer signal is an [open.md](../open.md) item with a prerequisite in another repo.

### 24 — `schema_version` on every `--json` object
It is there **from the start rather than after a consumer depends on an unversioned shape** — an anticipated UI is exactly the external reader that would otherwise have no way to detect a breaking change. Bumped by hand only on a rename, removal or retype; adding a field is not, since a reader that ignores unknown fields is unaffected.

- **`1` means "the shape as of 2026-09-03"**, not "unchanged since the beginning". The surface moved repeatedly while unversioned and no honest earlier number exists, so the counter starts where the guarantee starts.
- **It is this crate's own counter and leans on nothing Core serves.** Core's `/status` carries `core_version` and `study_designer_schema_version` and deliberately **no** contract version — and an upstream number would be the wrong one anyway: this versions *this crate's* `--json` shape, which moves without Core moving.
- **Every NDJSON line of `study-status --follow` carries it too**, not only that stream's `summary` — stronger than this entry's "the `--json` object", and decision 47's own argument: a reader of a live feed has to know the shape from the first record.

### 50 — `schema_version` built, `error_kind` retired, and one serializer to keep the first honest
Decisions 16 and 24 were written together and neither was built, while [tools.md](../interfaces/tools.md) told a caller to read both. The two were **not** equally cheap to keep, so they got different endings.

**`schema_version` is built**, at the cost of a stamp in the one function every `--json` object already funnelled through.

**`error_kind` is retired because its headline half cannot be delivered.** "Core's own error code verbatim" needs Core's structured `{code, message, cause}` body (`embarch-core` decision 12) to *reach* this crate as a code. It does not: **Core serves plain text on every non-2xx**, and that body is deferred-with-a-trigger. `embarch-core-client` parses the shape on `/study/*` and immediately flattens it to prose, so even the one endpoint that tries has no code to hand on. Building it honestly means Core first, then a new public typed error on the shared crate `embarch-ui` also depends on, then a kind chosen at ~43 sites here — and it would still be absent for most failures. **A second documented-but-not-really-there field, at several times the cost of the one that could be kept.**

**The cheap substitute is a trap, and this is the entry that says so.** The only machine-readable signal crossing the api→Core hop today is the HTTP status code, and a kind derived from it is **strictly coarser than decision 12's `code` enum** — one token per status, not per failure mode. Shipping that under decision 16's name is how two vocabularies come to be assumed to be one. If the field returns, it carries Core's codes or a different name. The exit code stays a single `1`; exit-code granularity is open again in [open.md](../open.md), prerequisite named.

**The field is unconditional by construction, not by convention** — the thing whose absence let this rot for the crate's whole life. `json_out` is the only module turning a `serde_json` value into text; `finish`, the NDJSON sites and MCP's `ok_json`/`err_json` route through it, so an emitter gets the stamp by existing. A guard test fails if `cli.rs` or `tools.rs` grows a serializer of its own, `tests/json_surface.rs` drives **every** subcommand through the real binary, and a tripwire on the subcommand count stops a new one being added without being added there. **The same path carries a startup failure** — unreadable config, unresolvable token — which had escaped as `main`'s `anyhow::Error`, printing **nothing at all** under `--json`; MCP mode still returns the error, having no JSON surface to put it on.
