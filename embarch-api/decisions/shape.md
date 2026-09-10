# embarch-api decisions: Scope and boundaries

**Status:** active, 2026-09-06.

What this crate is, what it deliberately is not, the two one-way relationships that keep it that way, and the one target a `static` project has. **How far its tests reach moved to [tests.md](tests.md) on 2026-09-06** — decisions 30, 46 and 54, verbatim — because one file carrying both missions had 7 bytes left against its cap.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md). Test reach: [tests.md](tests.md).

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

### 53 — A `static` project has exactly one target: itself, and `[[projects.targets]]` is retired
Decision 12 left `static` projects an escape hatch — a hand-authored `[[projects.targets]]` menu of `{ name, build_command, chip, artifact_path }` rows that `list_targets` returned verbatim — and **nothing was ever wired to select a row.** A build ran the project-level `build_command` regardless, and decision 51 then made every selection param a `static` project accepts an outright refusal. The config advertised a menu whose every entry was rejected, which reads to a caller as a bug in its own call rather than as a missing feature.

*Rejected: a `target` param that makes the rows selectable.* It is buildable — a row **replaces** the whole argv rather than splicing into it, so decision 51's "no guessing at another build system's flag grammar" objection does not apply. It loses on cost against value: it would add a second, differently-shaped selection grammar to `build`/`flash`/`build_and_flash`/`reset`/`run_study` and the CLI, for a feature **no config in this suite uses** — the rows are not in `config.example.toml`, and every field a row can carry is already expressible as one more `[[projects]]` entry with its own name. One target-selection grammar, scoped to the one toolchain this crate had to learn (decision 12), stays the boundary.

So the rows go, and **two things make the removal lossless rather than merely smaller.** `list_targets` for a `static` project no longer errors demanding a menu — it returns exactly one row, the project itself, with its configured `build_command`, `chip` and *resolved* `artifact_path`, so the tool that answers "what can I build?" answers it for every project kind and the row it names is the build a bare `build` actually runs. And a config still carrying `[[projects.targets]]` **fails at load naming the retirement**, rather than parsing into a field nothing reads: decision 51's reject-rather-than-ignore posture applied to config instead of to a call, since a config that reads as meaningful and is not is the whole defect being closed.

**The remediation branches on `discovery`, and did not at first.** As shipped, one shared sentence told *both* kinds to "declare one `[[projects]]` entry per target, each with its own `name`/`build_command`/`chip`/`artifact_path`" — advice a `zephyr-west` project is refused thirty lines later by the same `validate()`, because decision 12 forbids it those three fields precisely to stop a Zephyr repo's targets being snapshotted into config. The retirement was right; the text remediating it re-proposed the schema decision 12 removed. A `zephyr-west` config carrying rows is now told to **delete them** — its targets are discovered live per call, a caller names one with `board`/`variant`/`revision`/`app`, and `[projects.default_target]` covers the call that names none. The refusal itself stays **one check above the `discovery` match**: it is one invariant, it must fire before the per-kind field errors, and duplicating the condition into two arms is how the two texts drift apart again.

**Why the gate did not catch it**: the commit's own `zephyr-west` test asserted `contains("retired")` — that it refuses, never what it advises — [../../embarch-decision-reversals.md](../../embarch-decision-reversals.md)'s shape 8, a comment naming the right invariant while the text does not implement it. Both tests now pin their own remedy, and the `zephyr-west` one asserts the *absence* of the `static` one, so a future shared tail fails a test rather than shipping.

### 61 — `dev_bench_hello` gets a CLI twin rather than an amendment to the superset guarantee
`api/036` added `dev_bench_hello` as an MCP tool with **no CLI subcommand at all** — the first capability an agent could reach that a human at the CLI could not, breaking decision 3/10's "identical capabilities" and `spec.md` §1's CLI ⊇ MCP superset (naming `versions` as the sole, opposite-direction exception). `decisions/tool-wrapping.md` 52 leans on that superset explicitly to justify a CLI-only diagnostic; amending 3/10 to admit a second, agent-only exception would have knocked that ground out from under an otherwise-fine decision, for a gap this narrow.

Closed the cheaper way: `dev-bench-hello` (`src/main.rs`, `src/cli.rs`) runs the same `CoreClient::dev_bench_hello()` call the MCP tool does, renders the same `render_hello_ack` text, and surfaces the same 409/502 distinction (`DevBenchBusyError`/`DevBenchHandshakeError`) as CLI exit-1 text instead of an MCP error payload. No new client-layer code — this is a second front-end over the call `api/036` already wrote, exactly the shape decision 3/10 describes for every other tool. `suite/features.md`'s `api-040 — CLI subcommands for every tool` row is true again rather than silently false. `interfaces/tools.md`'s `dev_bench_hello` row is updated to drop the "no CLI twin" line.

3/10 and `spec.md` §1 are unchanged: no second exception was needed, so none was written.

**Amendment, `tasks/api/049`:** the CLI twin's `--json` success object first named this handshake's `schema_version` under the literal key `schema_version`, which `json_out::stamped()` unconditionally overwrites with the envelope's own constant (decision 24/50) — the exact collision decision 52 named and avoided for `versions`. Renamed to `dev_bench_schema_version`; see [../interfaces/tools.md](../interfaces/tools.md)'s `dev_bench_hello` row.

### 64 — Retired config keys are refused by name, except one still scaffolded in the field
`[[projects.targets]]` (decision 53) and `soc_chip_overrides` (decision 13) are refused by name at config load. `artifact_path_for_core` — retired separately, decision 15 — is not: with no `deny_unknown_fields` on `ProjectConfig`, it loads, silently unread.

Deliberate, not a gap: `embarch-umbrella` still scaffolds `artifact_path_for_core`, so refusing it by name would break scaffolded configs in the field. **Narrower than "every config", [verified 2026-09-10] in `embarch-umbrella/src`:** `init.rs` emits it for a *static* project on a WSL2 split (`embarch-umbrella` decision 16) and never for `discovery = "zephyr-west"` (its decision 17); umbrella's `doctor` check 9 reads it too. The other two carry no installed base — never scaffolded, and on record as unbuilt/never-wired rather than shipped-then-removed — so refusing them breaks nothing real.

**Default for the next retired key: refuse by name.** Toleration is earned only by an in-the-field installed base a scaffolding tool this crate does not control is still writing — the test `artifact_path_for_core` meets and the other two don't.

**Ends when:** `embarch-umbrella` stops scaffolding `artifact_path_for_core` and no config in the field still carries it — then refuse it too, as a separate load-behaviour task this decision does not authorize.

Shapes: [../interfaces/config.md](../interfaces/config.md), [../interfaces/tools.md](../interfaces/tools.md).
