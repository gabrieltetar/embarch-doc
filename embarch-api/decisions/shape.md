# embarch-api decisions: Scope and boundaries

**Status:** active, 2026-09-02.

What this crate is, what it deliberately is not, and the two one-way relationships that keep it that way.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

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

Shapes: [../interfaces/config.md](../interfaces/config.md), [../interfaces/tools.md](../interfaces/tools.md).

### 46 — A one-module `lib` target, so the mocked suite can reach anything at all
`open.md` carried six recorded acceptance criteria as "specified and unwritten" for weeks. Three of them — the two-pipe drain invariant, truncation on a UTF-8 character boundary, an untouched artifact not counting as fresh — are properties of `build.rs`, and `build.rs` lived in a **binary** crate. Each file under `tests/` compiles as its own crate and can reach a package's `lib` and nothing else, so those three were not merely untested, they were **untestable from an integration test**. The suite was unwritten partly because writing it was blocked and nobody had said so.

`build` therefore moves behind a `lib` target and `main.rs` imports it rather than declaring it a second time — one compiled copy, exercised by the bin and the tests alike. Deliberately **one module wide**: the rest of `main.rs` stays where it is. A whole-crate lib/bin split would have meant moving `Cli`/`Commands`/`TargetSelection` too, which is a refactor of the front end bought for nothing the tests need.

The other three criteria are properties of `CoreClient`, and their tests live in **`embarch-api/tests/`, not `crates/embarch-core-client/tests/`**, deliberately: the core-client crate is a plain path dependency rather than a workspace member, so `cargo test` at the repo root — the command the gate runs and the only one anybody types — would never execute them there.

The mock Core is **hand-rolled on `tokio::net`, not `wiremock`/`httpmock`**. Two of the three invariants cannot be expressed against a well-behaved mock anyway: per-endpoint timeout independence needs a socket that accepts and then goes silent, and the plain-text-on-non-2xx rule needs a response that is deliberately not JSON. Both are a few dozen lines against a dependency this crate already has. **The suite adds no dependency at all**, dev- or otherwise.

Six mutations — one per criterion, each reverted — confirmed every test goes red when its invariant is broken. Two limits worth stating: the four end-to-end tests need a POSIX shell and are `#[cfg(unix)]`, so **Windows runs the direct tests only and covers the two-pipe invariant not at all**; and a `CoreClient` endpoint added without `.bearer_auth(…)` is caught only if the sweep's route list is extended to call it.
