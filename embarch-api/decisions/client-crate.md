# embarch-api decisions: The shared client crate

**Status:** active, 2026-09-12.

The runtime stack `embarch-core-client` needed, its extraction out of this repo's own
`core_client.rs`/`config.rs`/`token_discovery.rs`, the one auth-and-send funnel it centralizes,
how it parses an older Core, one WSL2 predicate it delegates, which topology types it names rather
than copies, and where the crate itself lives. Split out of [core-link.md](core-link.md) on
2026-09-11 (`api/067`) along a topical seam, not as a squeeze.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md). Address
resolution and artifact transfer: [core-link.md](core-link.md).

### 36 — The whole runtime moves onto a dedicated 512 MiB-stack thread
A real GATT-sized status call reproduced a known deserialization stack overflow **in production**, crashing the live MCP server repeatedly — each crash silently respawning, so the client saw only a closed connection.

***Rejected, because it does not work:* `Builder::thread_stack_size`.** It sizes only threads the *runtime* spawns. The top-level future driven by `block_on` runs on whatever thread calls it, which for `#[tokio::main] fn main` is the process main thread, at the OS default, **with no knob to change it**.

So `main` spawns the runtime on a thread it sizes itself. **64 MiB was empirically insufficient against a real payload; 512 MiB was needed.** A release build overflowing even on `list-projects` was the same non-resizable-calling-thread issue surfacing through release-mode inlining — one fix, two bugs.

### 37, 38 — `embarch-core-client` extracted, and given the two wrappers nothing here needed
`embarch-ui` needed to reach Core exactly as this crate does — bearer injection, per-call timeouts, the topology-branched flash transport, typed error mapping — so the choice was between duplicating that logic and **both depending on one implementation**. The latter follows the suite's one-implementation-many-call-sites shape rather than reintroducing the mirrored-copy risk that shape exists to eliminate. A plain path dependency, not a Cargo workspace.

Two Core endpoints then turned out to have **no client wrapper anywhere**, because this crate never needed either: enrolled-board listing and dev-bench port. The gap surfaced the moment `embarch-ui` routed *every* hardware-adjacent read through Core rather than only mutations. The port wrapper treats Core's 404 as `Ok(None)`, so a caller rendering "not connected" need not match an error string.

Later additions exposed the cost — seven hand-written mirrors of topology types. **Retired by decision 72 below.**

### 55 — One funnel applies the bearer token; nine routes were exempt from the rule that said so
`send`/`send_no_content` consume the response, so the nine routes giving a status its own meaning (a `404` for "not enrolled", a `409` for a topology mismatch) and the SSE stream could not use them; each applied `.bearer_auth(…)` itself. All nine did send it; `client.rs`'s comment said none existed. **A convention nine of twenty-five sites are exempt from is not one** — and the comment was the worse half, since a new route copies the hand-written form while the sentence a reader trusts says it cannot exist.

So the funnel moves down. `dispatch` applies the token and the timeout and sends; `send`/`send_no_content` are thin readers over it; a route needing typed status handling hands it a `RequestBuilder` and reads the status itself. `bearer_token()` is **retired**. The guard: one `.bearer_auth(…)` in the crate, no send site outside `dispatch`. ***Rejected: `default_headers`*** — it authenticates every request the `reqwest::Client` makes rather than this client's *routes*. **Nothing was unauthenticated before this**; the wire is unchanged.

### 62 — `token_discovery`'s WSL2 check delegates to `embarch_topology::software::detect_wsl2`, dropping its own third signal
This crate's private `is_wsl2` ran its own rule — `/proc/version` containing "microsoft" *or* "wsl", ignoring `$WSL_DISTRO_NAME` — while `resolve_software_topology`, in the same binary, used `detect_wsl2`'s union of kernel-string-or-env-var. The two could disagree: token discovery decides *where the token file is*, topology resolution *which Core to talk to*. No real WSL2 kernel is known to stamp "wsl" without "microsoft", so the extra branch covered no observed case; delegating removes the disagreement at no known cost.

`embarch-topology` decisions 4/8 (crate.md) claimed no two callers could disagree "since there is only one of them" — false while this crate linked the shared crate and ran a second predicate beside it; a crate cannot stop a caller writing one next to the call it never makes.

### 58 — Parsing an older Core is a rule of the crate, not a per-field judgement call
`client.rs` had already made this choice many times before `validate` broke it: `link_port_interface` and `study_designer_schema_version` among others are `#[serde(default)]` on an `Option<T>`, and `an_older_core_body_missing_link_port_interface_still_parses` is a test whose name states the rule out loud. `api/045` added `ValidateResponse::validated_at_utc_ms` as a bare required `u64` — the one field breaking the pattern, not a considered exception to it. Against an `embarch-core` predating that field, every `validate` call then failed at deserialization instead of returning the timestamp Core does send, indistinguishable from a broken client rather than a version skew — on a machine where deployed Core and this crate are known not to move together (the MCP-binary-goes-stale gotcha).

So: **every response field this crate deserializes that Core may not yet send is `Option<T>` with `#[serde(default)]`** — matching the existing fields in shape, not merely in having a default. `None` is never presented as a fabricated "validated at 1970" nor silently dropped: a reader is told in words that this Core did not report the value, which is a different fact from validating at an unknown time.

**The check, corrected `api/072`.** The frozen numbers 13/14 are retired: a plain `grep -c 'serde(default)'` counts prose quoting the attribute too, so it drifts as the file grows. The check that stays correct is anchored to the attribute's position: `grep -c '^\s*#\[serde(default)\]' crates/embarch-core-client/src/client.rs`.

### 66 — The crate lives inside `embarch-api`'s own tree, not a tenth repo, and `embarch-ui` path-depends across a repo boundary to reach it
Decisions 37/38 settled that the shared Core client is one implementation, not where it lives. It sits at `crates/embarch-core-client` inside this repo, unlike `embarch-study-designer` (decision 8) and `embarch-topology` (decision 13), each of which got a standalone repo. **Only decision 8 states the FFI/C rationale** — two Cargo dependents plus one FFI/C consumer as the case a standalone shared crate is for. **`embarch-topology` decision 13 states no such reason**: only that a shared crate needs *somewhere* for three consumers to depend on. This crate's three consumers are all plain Cargo path dependents, so decision 8's case does not hold — and the question was never taken up either way: 37/38 left the crate where the extraction happened.

The cost, stated rather than softened (`spec.md:48`): `embarch-ui` path-depends on it from outside this repo, so **a change made here reaches a repo this one does not own**, and `check-ownership.py` does not refuse that move — nothing in the fleet mechanism stops an `api` task editing a crate `embarch-ui` depends on. `suite/decisions.md` 1 documents the gate-spelling cost that follows.

Kept anyway: a tenth repo for Cargo-only consumers with no cross-language boundary pays a cost `embarch-study-designer`/`embarch-topology` accepted for a reason (FFI, independent hardware/software versioning) that does not hold here, and decision 56 already made the crate a workspace member with its own tests in this repo's gate. **Reverses** if a *fourth* Cargo consumer with its own release cadence appears, or an `api`-only change here breaks `embarch-ui` or `embarch-umbrella` silently.

**Corrected at its own fold, 2026-09-10, on the reviewer's finding.** As written it said **two** consumers and triggered reversal on "a third appears" — which had already happened: `embarch-umbrella` path-depends on this crate since `umbrella/036`, calling `token_discovery::resolve_token`. The count is three (`embarch-api`, `embarch-ui`, `embarch-umbrella`) and the trigger is now a fourth. **Conclusion unchanged**: all three are plain Cargo dependents with no FFI/C boundary.

### 72 — The seven mirrored `embarch-topology` types are retired; the tests that pinned them are kept and re-scoped
Decisions 37/38 accepted seven hand-written copies of `embarch_topology::hardware`'s `EnrolledBoard`, `Alert`, `DetectedPort`, `SignalLink`, `Route` and `SignalDirection`, because the originals sat behind that crate's `hardware` feature — which links `probe-rs`/`serialport`, dependencies this crate must never have. `embarch-topology` decision 31 split a `wire` feature out of it: the plain data types, pure serde, no C toolchain. So the copies are gone. This crate depends on `embarch-topology` with `default-features = false, features = ["software", "wire"]` and names the real types; the old `*Response` spellings survive as **aliases**, so no call site moves and the shipped crate keeps its public names.

**The cost was not hypothetical.** `EnrolledBoardResponse` silently dropped `link_port_interface` for a release — the field that exists because an nRF54L15DK's console is on the *higher* VCOM (`embarch-topology` decision 20) — and `tasks/api/032` exists to paper over it. Two structs in two crates that never meet are not comparable by any compiler, which is what "drift" means here.

**The pinning tests are kept, and that is the part that is not a refactor.** Deleting `client.rs`'s three round-trip literals along with the copies would have been natural — the compiler now proves this crate and Core agree, because they name one type. **It proves nothing about agreeing with a Core already deployed.** Rename a field on the shared type and both sides change together and compile clean, while every running Core and every `enrollment.toml` on disk still speaks the old spelling. The literals are the only thing positioned to notice, so they stay — re-scoped from "our copy matches theirs" to "the wire has not moved under a deployed Core".

***Rejected: keeping a mirror for the derives.*** `Alert`/`DetectedPort` lacked `PartialEq`/`Eq` the copies had; adding two derives upstream is smaller than a copy kept alive to carry them.

Naming the original also **gains** `guessed_among` — whether a port was picked among equally-plausible candidates rather than determined. The mirror had no such field, so a caller could not tell a guess from an answer.
