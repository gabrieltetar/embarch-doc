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

### 25 — Config resolution happens once, at process start
True already and probably right — an MCP client's spawn cwd *is* "which repo am I working in" for the session's lifetime — but the cwd-upward search never said so, leaving a reader to infer it. Stated as a property of the design rather than a gap: switching repos mid-session means reconnecting the client, same as any other config change.

### 46 — A one-module `lib` target, so the mocked suite can reach anything at all
`open.md` carried six recorded acceptance criteria as "specified and unwritten" for weeks. Three of them — the two-pipe drain invariant, truncation on a UTF-8 character boundary, an untouched artifact not counting as fresh — are properties of `build.rs`, and `build.rs` lived in a **binary** crate. Each file under `tests/` compiles as its own crate and can reach a package's `lib` and nothing else, so those three were not merely untested, they were **untestable from an integration test**. The suite was unwritten partly because writing it was blocked and nobody had said so.

`build` therefore moves behind a `lib` target and `main.rs` imports it rather than declaring it a second time — one compiled copy, exercised by the bin and the tests alike. Deliberately **one module wide**: the rest of `main.rs` stays where it is. A whole-crate lib/bin split would have meant moving `Cli`/`Commands`/`TargetSelection` too, which is a refactor of the front end bought for nothing the tests need.

The other three criteria are properties of `CoreClient`, and their tests live in **`embarch-api/tests/`, not `crates/embarch-core-client/tests/`**, deliberately: the core-client crate is a plain path dependency rather than a workspace member, so `cargo test` at the repo root — the command the gate runs and the only one anybody types — would never execute them there.

The mock Core is **hand-rolled on `tokio::net`, not `wiremock`/`httpmock`**. Two of the three invariants cannot be expressed against a well-behaved mock anyway: per-endpoint timeout independence needs a socket that accepts and then goes silent, and the plain-text-on-non-2xx rule needs a response that is deliberately not JSON. Both are a few dozen lines against a dependency this crate already has. **The suite adds no dependency at all**, dev- or otherwise.

Six mutations — one per criterion, each reverted — confirmed every test goes red when its invariant is broken. Two limits worth stating: the four end-to-end tests need a POSIX shell and are `#[cfg(unix)]`, so **Windows runs the direct tests only and covers the two-pipe invariant not at all**; and a `CoreClient` endpoint added without `.bearer_auth(…)` is caught only if the sweep's route list is extended to call it.
