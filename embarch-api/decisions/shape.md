# embarch-api decisions: Scope and boundaries

**Status:** active, 2026-09-13.

What this crate is, what it deliberately is not, and the two one-way relationships that keep it that way. **How far its tests reach moved to [tests.md](tests.md) on 2026-09-06** — decisions 30, 46 and 54, verbatim — because one file carrying both missions had 7 bytes left against its cap. **Decision 30 moved on again on 2026-09-13, to [smoke-harness.md](smoke-harness.md)**; [../decisions.md](../decisions.md) is what routes a number to its current file, and it is the reference to prefer over any of these paths. **Retired config keys and the one target a `static` project has moved to [config-retirement.md](config-retirement.md) on 2026-09-13** — decisions 53 and 64, verbatim — for the same reason.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md). Test reach: [tests.md](tests.md). Retired config keys: [config-retirement.md](config-retirement.md).

### 1, 6, 8 — Single user, single Core, one TOML file, and this doc as the record
No multi-tenancy, no permission model, no database. Explicitly revisited mid-design — the original framing raised "what if this is multi-tenant, make it full" — and resolved the other way: **each engineer runs their own complete stack**, so there is no multiplexing to design for. With no multi-row data to hold, a single TOML file is the right persistence, not a stepping stone to SQLite.

### 2, 9 — Rust, and dependency choices locked rather than incidental
Matching Core, reusing its structuring patterns, keeping the project to one toolchain. The dependencies are decisions: `rmcp` for MCP rather than hand-rolling JSON-RPC, since the schema and handshake plumbing is not worth re-deriving per project; `reqwest` on **rustls rather than native-tls**, specifically to avoid a system OpenSSL dependency, so this stays trivially buildable on whatever machine an engineer's Core happens to run on; `clap` derive; `toml` + `serde`; `schemars` for the tool schemas `rmcp` requires.

### 3, 10 — Three responsibilities, and a CLI alongside MCP rather than instead of it
MCP tools, the identical capabilities as CLI subcommands, and build orchestration. **Subcommand presence is the mode switch**, which keeps every existing MCP client configuration working unchanged.

The CLI closed a real gap: without it, an engineer with no MCP client in front of them had **no way to invoke build orchestration at all**, and would have had to run the build by hand or call Core's HTTP endpoints directly — bypassing the config-driven build command, the artifact-freshness check, and the timeout and process-group handling entirely. Two front-ends over one set of modules, mirroring what Core already established between its own CLI and HTTP API: neither privileged over the other.

### 4 — MCP over stdio, with the client spawning the process
Chosen over exposing this surface as its own HTTP service with an API key. **The consequence is stated rather than left implicit:** the inbound trust boundary is simply "whoever can spawn the process" — no token, no session, no key protecting the MCP surface itself. A deliberate simplification; if this is ever run detached from an interactive client, this decision needs revisiting. Entirely separate from the *outbound* credential needed to reach Core.

### 7 — Core's address is configurable, never hardcoded to loopback
Core's own design already anticipates moving to a LAN-reachable machine, and this crate must not bake in an assumption that will break when it does.

### 25 — Config resolution happens once, at process start, after a cwd-upward search
True already and probably right — an MCP client's spawn cwd *is* "which repo am I working in" for the session's lifetime — but the cwd-upward search never said so, leaving a reader to infer it. Stated as a property of the design rather than a gap: switching repos mid-session means reconnecting the client, same as any other config change.

**Why the search walks up at all:** an engineer working across several firmware repos has no single `EMBARCH_API_CONFIG` value that is ever correct, and walking up for a conventional filename is the pattern `git` and `west` already use for their own roots. *Rejected: a separate MCP registration per repo* — that is not "no `--config` needed", it is "typed once instead of every call".

### 61 — `dev_bench_hello` gets a CLI twin rather than an amendment to the superset guarantee
`api/036` added `dev_bench_hello` as an MCP tool with **no CLI subcommand at all** — the first capability an agent could reach that a human at the CLI could not, breaking decision 3/10's "identical capabilities" and `spec.md` §1's CLI ⊇ MCP superset (naming `versions` as the sole, opposite-direction exception). `decisions/tool-wrapping.md` 52 leans on that superset explicitly to justify a CLI-only diagnostic; amending 3/10 to admit a second, agent-only exception would have knocked that ground out from under an otherwise-fine decision, for a gap this narrow.

Closed the cheaper way: `dev-bench-hello` (`src/main.rs`, `src/cli.rs`) runs the same `CoreClient::dev_bench_hello()` call the MCP tool does, renders the same `render_hello_ack` text, and surfaces the same 409/502 distinction (`DevBenchBusyError`/`DevBenchHandshakeError`) as CLI exit-1 text instead of an MCP error payload. No new client-layer code — this is a second front-end over the call `api/036` already wrote, exactly the shape decision 3/10 describes for every other tool. `suite/features.md`'s `api-040 — CLI subcommands for every tool` row is true again rather than silently false. `interfaces/tools.md`'s `dev_bench_hello` row is updated to drop the "no CLI twin" line.

3/10 and `spec.md` §1 are unchanged: no second exception was needed, so none was written.

**Amendment, `tasks/api/049`:** the CLI twin's `--json` success object first named this handshake's `schema_version` under the literal key `schema_version`, which `json_out::stamped()` unconditionally overwrites with the envelope's own constant (decision 24/50) — the exact collision decision 52 named and avoided for `versions`. Renamed to `dev_bench_schema_version`; see [../interfaces/tools-dev-bench.md](../interfaces/tools-dev-bench.md)'s `dev_bench_hello` row.
